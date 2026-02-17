"""End-to-end pipeline tests with mocked external dependencies.

Verifies the full VoiceReach processing pipeline:
  keyboard input -> IAL -> LLM orchestrator -> TTS
without requiring cameras, microphones, LLM servers, or internet.
"""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import numpy as np
import pytest

from voicereach.engine.gaze.gaze_estimator import GazeResult
from voicereach.engine.gaze.mediapipe_tracker import FaceData
from voicereach.engine.pipeline import Pipeline
from voicereach.models.context import ConversationEntry
from voicereach.models.events import (
    Candidate,
    CandidateSet,
    CandidateUpdate,
    EventType,
    GenerationStage,
    IALEvent,
    InputSource,
    IntentAxis,
    TTSReady,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_candidate_set(
    request_id: str = "req-001",
    stage: GenerationStage = GenerationStage.LOCAL_FAST,
    is_final: bool = False,
) -> CandidateSet:
    """Create a realistic CandidateSet for testing."""
    return CandidateSet(
        candidates=[
            Candidate(
                text="元気だよ",
                intent_axis=IntentAxis.EMOTIONAL_RESPONSE,
                confidence=0.8,
                generation_stage=stage,
                latency_ms=150,
            ),
            Candidate(
                text="最近どう？",
                intent_axis=IntentAxis.QUESTION,
                confidence=0.7,
                generation_stage=stage,
                latency_ms=150,
            ),
            Candidate(
                text="ちょっと疲れてるかな",
                intent_axis=IntentAxis.SELF_REFERENCE,
                confidence=0.6,
                generation_stage=stage,
                latency_ms=150,
            ),
            Candidate(
                text="何か食べたいな",
                intent_axis=IntentAxis.ACTION_REQUEST,
                confidence=0.5,
                generation_stage=stage,
                latency_ms=150,
            ),
        ],
        stage=stage,
        request_id=request_id,
        is_final=is_final,
    )


def _make_face_data() -> FaceData:
    """Create synthetic FaceData that exercises the heuristic gaze path."""
    num_landmarks = 478  # 468 face + 10 iris
    landmarks = np.random.rand(num_landmarks, 3).astype(np.float32) * 100

    # Make eye landmarks plausible by placing them with some width
    # Left eye outer (33) and inner (133)
    landmarks[33] = [30, 50, 0]
    landmarks[133] = [50, 50, 0]
    # Right eye outer (362) and inner (263)
    landmarks[362] = [60, 50, 0]
    landmarks[263] = [80, 50, 0]

    return FaceData(
        landmarks=landmarks,
        left_eye_patch=np.random.rand(64, 64).astype(np.float32),
        right_eye_patch=np.random.rand(64, 64).astype(np.float32),
        left_iris=np.array([40.0, 50.0], dtype=np.float32),
        right_iris=np.array([70.0, 50.0], dtype=np.float32),
        head_pose=np.array([0.0, 0.0, 0.0], dtype=np.float32),
        face_bbox=(20, 30, 80, 80),
        confidence=1.0,
    )


async def _mock_generate_candidates(context, num_candidates=4):
    """Async generator that yields a single CandidateSet."""
    cs = _make_candidate_set()
    yield cs


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestPipelineInitialization:

    @pytest.mark.asyncio
    async def test_initialize_and_shutdown(self):
        """Pipeline initializes all sub-components and shuts down cleanly."""
        pipeline = Pipeline()
        await pipeline.initialize()

        # After initialization the IAL should have the keyboard adapter
        assert InputSource.KEYBOARD in pipeline._ial.active_sources

        await pipeline.shutdown()

    @pytest.mark.asyncio
    async def test_pipeline_sets_message_callback(self):
        """Pipeline accepts a message callback."""
        pipeline = Pipeline()
        callback = AsyncMock()
        pipeline.set_message_callback(callback)
        assert pipeline._message_callback is callback


class TestKeyboardToCandidate:

    @pytest.mark.asyncio
    async def test_key_select_dispatches_ial_event(self):
        """Pressing '1' produces a SELECT IAL event with target_id=0."""
        pipeline = Pipeline()
        await pipeline.initialize()

        events: list[IALEvent] = []
        pipeline._ial.subscribe(events.append)

        pipeline.handle_key("1")

        assert len(events) == 1
        assert events[0].event_type == EventType.SELECT
        assert events[0].target_id == 0
        assert events[0].source == InputSource.KEYBOARD

        await pipeline.shutdown()

    @pytest.mark.asyncio
    async def test_key_confirm_dispatches_confirm(self):
        pipeline = Pipeline()
        await pipeline.initialize()

        events: list[IALEvent] = []
        pipeline._ial.subscribe(events.append)

        pipeline.handle_key("Space")

        assert len(events) == 1
        assert events[0].event_type == EventType.CONFIRM

        await pipeline.shutdown()

    @pytest.mark.asyncio
    async def test_key_escape_dispatches_emergency(self):
        pipeline = Pipeline()
        await pipeline.initialize()

        events: list[IALEvent] = []
        pipeline._ial.subscribe(events.append)

        pipeline.handle_key("Escape")

        assert len(events) == 1
        assert events[0].event_type == EventType.EMERGENCY

        await pipeline.shutdown()


class TestCandidateSelectionTriggersTTS:

    @pytest.mark.asyncio
    async def test_select_candidate_triggers_tts(self):
        """Selecting a candidate synthesizes speech and sends TTSReady."""
        pipeline = Pipeline()
        await pipeline.initialize()

        # Set up a known candidate set
        cs = _make_candidate_set(request_id="tts-test-001")
        pipeline._current_candidates = cs
        pipeline._current_request_id = cs.request_id

        # Mock TTS to return a fake path
        fake_audio_path = Path("/tmp/fake_audio.wav")
        pipeline._tts_router.synthesize = AsyncMock(return_value=fake_audio_path)

        # Mock LLM cancel
        pipeline._llm.cancel_pending = AsyncMock()

        # Capture messages
        sent_messages = []

        async def capture(msg):
            sent_messages.append(msg)

        pipeline.set_message_callback(capture)

        await pipeline.handle_candidate_selected("tts-test-001", 0)

        # TTS was called
        pipeline._tts_router.synthesize.assert_awaited_once_with("元気だよ")

        # TTSReady was sent
        assert len(sent_messages) == 1
        assert isinstance(sent_messages[0], TTSReady)
        assert sent_messages[0].text == "元気だよ"
        assert "fake_audio" in sent_messages[0].audio_url

        await pipeline.shutdown()

    @pytest.mark.asyncio
    async def test_select_out_of_range_does_nothing(self):
        """Selecting an invalid candidate index should not crash."""
        pipeline = Pipeline()
        await pipeline.initialize()

        cs = _make_candidate_set(request_id="oob-test")
        pipeline._current_candidates = cs
        pipeline._llm.cancel_pending = AsyncMock()

        sent = []
        pipeline.set_message_callback(lambda msg: sent.append(msg))

        # Index 10 is out of range for 4 candidates
        await pipeline.handle_candidate_selected("oob-test", 10)
        assert len(sent) == 0

        await pipeline.shutdown()

    @pytest.mark.asyncio
    async def test_select_wrong_request_id_does_nothing(self):
        """Selecting with a mismatched request_id should be a no-op."""
        pipeline = Pipeline()
        await pipeline.initialize()

        cs = _make_candidate_set(request_id="correct-id")
        pipeline._current_candidates = cs
        pipeline._llm.cancel_pending = AsyncMock()

        sent = []
        pipeline.set_message_callback(lambda msg: sent.append(msg))

        await pipeline.handle_candidate_selected("wrong-id", 0)
        assert len(sent) == 0

        await pipeline.shutdown()


class TestPartnerUtteranceTriggers:

    @pytest.mark.asyncio
    async def test_partner_utterance_adds_to_history(self):
        """add_partner_utterance appends to conversation history."""
        pipeline = Pipeline()
        # We don't need full initialization for this test; the method
        # directly modifies context and creates a task.
        with patch.object(pipeline, "trigger_generation", new_callable=AsyncMock):
            pipeline.add_partner_utterance("こんにちは")

        assert len(pipeline._context.conversation_history) == 1
        assert pipeline._context.conversation_history[0].role == "partner"
        assert pipeline._context.conversation_history[0].text == "こんにちは"

    @pytest.mark.asyncio
    async def test_partner_utterance_triggers_generation(self):
        """add_partner_utterance triggers LLM candidate generation."""
        pipeline = Pipeline()
        await pipeline.initialize()

        sent_messages = []

        async def capture(msg):
            sent_messages.append(msg)

        pipeline.set_message_callback(capture)

        # Mock the orchestrator to yield a known candidate set
        pipeline._llm.generate_candidates = _mock_generate_candidates

        # Trigger generation (the task is created via asyncio.create_task)
        pipeline.add_partner_utterance("お元気ですか？")

        # Give the background task a moment to complete
        await asyncio.sleep(0.1)

        assert len(pipeline._context.conversation_history) == 1
        assert pipeline._context.conversation_history[0].text == "お元気ですか？"

        # Candidates should have been sent
        assert len(sent_messages) >= 1
        assert isinstance(sent_messages[0], CandidateUpdate)
        assert sent_messages[0].candidate_set.candidates[0].text == "元気だよ"

        await pipeline.shutdown()


class TestGazeToZoneMapping:

    @pytest.mark.asyncio
    async def test_process_face_data_returns_zone(self):
        """process_face_data returns a ZoneResult via heuristic path."""
        pipeline = Pipeline()
        # Initialize the gaze estimator in heuristic mode (no ONNX model)
        pipeline._gaze_estimator.initialize()

        face_data = _make_face_data()
        result = pipeline.process_face_data(face_data)

        assert result is not None
        assert 0 <= result.zone_id < 4
        assert 0.0 <= result.confidence <= 1.0

        pipeline._gaze_estimator.close()

    def test_handle_gaze_update_returns_zone(self):
        """handle_gaze_update updates context and returns a ZoneResult."""
        pipeline = Pipeline()
        result = pipeline.handle_gaze_update(zone_id=2, confidence=0.9)

        assert result is not None
        assert pipeline._context.current_zone_id == 2


class TestEmergencyEvent:

    @pytest.mark.asyncio
    async def test_escape_produces_emergency_ial_event(self):
        """Pressing Escape produces an EMERGENCY IAL event."""
        pipeline = Pipeline()
        await pipeline.initialize()

        events: list[IALEvent] = []
        pipeline._ial.subscribe(events.append)

        pipeline.handle_key("Escape")

        assert len(events) == 1
        assert events[0].event_type == EventType.EMERGENCY

        await pipeline.shutdown()

    @pytest.mark.asyncio
    async def test_emergency_event_is_handled_by_pipeline(self, caplog):
        """The pipeline's _on_ial_event logs EMERGENCY events."""
        pipeline = Pipeline()
        await pipeline.initialize()

        with caplog.at_level(logging.WARNING):
            pipeline.handle_key("Escape")

        assert any("EMERGENCY" in r.message for r in caplog.records)

        await pipeline.shutdown()


class TestConversationHistory:

    @pytest.mark.asyncio
    async def test_history_grows_with_partner_and_patient(self):
        """Conversation history grows when partner speaks and patient selects."""
        pipeline = Pipeline()
        await pipeline.initialize()

        # Partner utterance
        with patch.object(pipeline, "trigger_generation", new_callable=AsyncMock):
            pipeline.add_partner_utterance("今日はいい天気だね")

        assert len(pipeline._context.conversation_history) == 1

        # Simulate patient selection
        cs = _make_candidate_set(request_id="hist-test")
        pipeline._current_candidates = cs
        pipeline._llm.cancel_pending = AsyncMock()
        pipeline._tts_router.synthesize = AsyncMock(return_value=Path("/tmp/test.wav"))
        pipeline.set_message_callback(AsyncMock())

        await pipeline.handle_candidate_selected("hist-test", 0)

        assert len(pipeline._context.conversation_history) == 2
        assert pipeline._context.conversation_history[0].role == "partner"
        assert pipeline._context.conversation_history[1].role == "patient"
        assert pipeline._context.conversation_history[1].text == "元気だよ"

        await pipeline.shutdown()


class TestFullRoundTrip:

    @pytest.mark.asyncio
    async def test_round_trip_partner_to_tts(self):
        """Full round trip: partner utterance -> candidates -> selection -> TTS."""
        pipeline = Pipeline()
        await pipeline.initialize()

        # Track all messages
        messages = []

        async def capture(msg):
            messages.append(msg)

        pipeline.set_message_callback(capture)

        # Step 1: Partner utterance triggers generation
        pipeline._llm.generate_candidates = _mock_generate_candidates
        pipeline.add_partner_utterance("お元気ですか？")
        await asyncio.sleep(0.1)

        assert len(messages) >= 1
        assert isinstance(messages[0], CandidateUpdate)
        candidate_set = messages[0].candidate_set

        # Step 2: Select candidate 0
        pipeline._llm.cancel_pending = AsyncMock()
        fake_path = Path("/tmp/round_trip.wav")
        pipeline._tts_router.synthesize = AsyncMock(return_value=fake_path)

        await pipeline.handle_candidate_selected(
            candidate_set.request_id, 0
        )

        # Step 3: Verify TTS was triggered
        pipeline._tts_router.synthesize.assert_awaited_once()

        # Step 4: Verify TTSReady sent
        tts_messages = [m for m in messages if isinstance(m, TTSReady)]
        assert len(tts_messages) == 1
        assert tts_messages[0].text == "元気だよ"

        # Step 5: Verify conversation history
        assert len(pipeline._context.conversation_history) == 2
        assert pipeline._context.conversation_history[0].role == "partner"
        assert pipeline._context.conversation_history[0].text == "お元気ですか？"
        assert pipeline._context.conversation_history[1].role == "patient"
        assert pipeline._context.conversation_history[1].text == "元気だよ"

        await pipeline.shutdown()

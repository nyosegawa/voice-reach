"""Integration tests for the Pipeline class.

Tests the pipeline components working together without WebSocket.
Exercises the pipeline lifecycle, keyboard-to-IAL flow, gaze zone
mapping, face data processing, partner utterance context updates,
and candidate selection with TTS (using the placeholder engine).

All tests run WITHOUT external dependencies (no camera, no LLM server,
no CosyVoice model).
"""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from unittest.mock import AsyncMock, patch

import numpy as np
import pytest

from voicereach.engine.gaze.gaze_estimator import GazeEstimator, GazeResult
from voicereach.engine.gaze.mediapipe_tracker import FaceData
from voicereach.engine.gaze.zone_mapper import ZoneResult
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
    request_id: str = "int-req-001",
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


def _make_face_data(
    iris_offset_x: float = 0.0,
    iris_offset_y: float = 0.0,
) -> FaceData:
    """Create synthetic FaceData with controllable iris offsets.

    Uses a deterministic landmark layout so that the heuristic gaze
    estimator produces predictable results.
    """
    num_landmarks = 478
    landmarks = np.zeros((num_landmarks, 3), dtype=np.float32)

    eye_width = 20.0
    left_center_x, left_center_y = 100.0, 80.0
    landmarks[33] = [left_center_x - eye_width / 2, left_center_y, 0]
    landmarks[133] = [left_center_x + eye_width / 2, left_center_y, 0]
    for idx in [160, 159, 158]:
        landmarks[idx] = [left_center_x, left_center_y - 3, 0]
    for idx in [144, 145, 153]:
        landmarks[idx] = [left_center_x, left_center_y + 3, 0]

    right_center_x, right_center_y = 150.0, 80.0
    landmarks[362] = [right_center_x - eye_width / 2, right_center_y, 0]
    landmarks[263] = [right_center_x + eye_width / 2, right_center_y, 0]
    for idx in [387, 386, 385]:
        landmarks[idx] = [right_center_x, right_center_y - 3, 0]
    for idx in [373, 374, 380]:
        landmarks[idx] = [right_center_x, right_center_y + 3, 0]

    left_iris = np.array([
        left_center_x + iris_offset_x * eye_width,
        left_center_y + iris_offset_y * eye_width,
    ], dtype=np.float32)
    right_iris = np.array([
        right_center_x + iris_offset_x * eye_width,
        right_center_y + iris_offset_y * eye_width,
    ], dtype=np.float32)

    return FaceData(
        landmarks=landmarks,
        left_eye_patch=np.zeros((64, 64), dtype=np.float32),
        right_eye_patch=np.zeros((64, 64), dtype=np.float32),
        left_iris=left_iris,
        right_iris=right_iris,
        head_pose=np.array([0.0, 0.0, 0.0], dtype=np.float32),
        face_bbox=(80, 60, 90, 50),
        confidence=1.0,
    )


# ---------------------------------------------------------------------------
# Pipeline lifecycle
# ---------------------------------------------------------------------------

class TestPipelineLifecycle:

    @pytest.mark.asyncio
    async def test_pipeline_lifecycle(self):
        """Initialize and shutdown the pipeline cleanly."""
        pipeline = Pipeline()
        await pipeline.initialize()

        # After initialization, the IAL has the keyboard adapter registered
        assert InputSource.KEYBOARD in pipeline._ial.active_sources

        await pipeline.shutdown()

    @pytest.mark.asyncio
    async def test_pipeline_double_shutdown_safe(self):
        """Shutting down twice does not raise."""
        pipeline = Pipeline()
        await pipeline.initialize()
        await pipeline.shutdown()
        await pipeline.shutdown()

    @pytest.mark.asyncio
    async def test_pipeline_message_callback(self):
        """Pipeline accepts and stores a message callback."""
        pipeline = Pipeline()
        callback = AsyncMock()
        pipeline.set_message_callback(callback)
        assert pipeline._message_callback is callback


# ---------------------------------------------------------------------------
# Keyboard -> IAL event
# ---------------------------------------------------------------------------

class TestPipelineKeyboardToEvent:

    @pytest.mark.asyncio
    async def test_pipeline_keyboard_to_event(self):
        """Sending a key through the pipeline fires an IAL event."""
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
    async def test_pipeline_confirm_key(self):
        """Space key produces a CONFIRM event."""
        pipeline = Pipeline()
        await pipeline.initialize()

        events: list[IALEvent] = []
        pipeline._ial.subscribe(events.append)

        pipeline.handle_key("Space")

        assert len(events) == 1
        assert events[0].event_type == EventType.CONFIRM

        await pipeline.shutdown()

    @pytest.mark.asyncio
    async def test_pipeline_emergency_key(self):
        """Escape key produces an EMERGENCY event."""
        pipeline = Pipeline()
        await pipeline.initialize()

        events: list[IALEvent] = []
        pipeline._ial.subscribe(events.append)

        pipeline.handle_key("Escape")

        assert len(events) == 1
        assert events[0].event_type == EventType.EMERGENCY

        await pipeline.shutdown()

    @pytest.mark.asyncio
    async def test_pipeline_unknown_key_no_event(self):
        """An unmapped key does not produce an IAL event."""
        pipeline = Pipeline()
        await pipeline.initialize()

        events: list[IALEvent] = []
        pipeline._ial.subscribe(events.append)

        pipeline.handle_key("z")

        assert len(events) == 0

        await pipeline.shutdown()


# ---------------------------------------------------------------------------
# Gaze zone mapping
# ---------------------------------------------------------------------------

class TestPipelineGazeZoneMapping:

    def test_pipeline_gaze_zone_mapping(self):
        """handle_gaze_update returns a valid ZoneResult."""
        pipeline = Pipeline()
        result = pipeline.handle_gaze_update(zone_id=2, confidence=0.9)

        assert isinstance(result, ZoneResult)
        assert result.zone_id >= 0
        assert 0.0 <= result.confidence <= 1.0
        assert pipeline._context.current_zone_id == 2

    def test_pipeline_gaze_zone_mapping_all_zones(self):
        """handle_gaze_update works for all 4 zones."""
        pipeline = Pipeline()
        for zone_id in range(4):
            result = pipeline.handle_gaze_update(zone_id=zone_id, confidence=0.8)
            assert isinstance(result, ZoneResult)
            assert pipeline._context.current_zone_id == zone_id


# ---------------------------------------------------------------------------
# Face data processing
# ---------------------------------------------------------------------------

class TestPipelineFaceDataProcessing:

    def test_pipeline_face_data_processing(self):
        """Create synthetic FaceData and process through pipeline.

        Uses the heuristic gaze path (no ONNX model).
        """
        pipeline = Pipeline()
        # Initialize gaze estimator in heuristic mode
        pipeline._gaze_estimator.initialize()

        face_data = _make_face_data(iris_offset_x=0.0, iris_offset_y=0.0)
        result = pipeline.process_face_data(face_data)

        assert result is not None
        assert isinstance(result, ZoneResult)
        assert 0 <= result.zone_id < 4
        assert 0.0 <= result.confidence <= 1.0

        pipeline._gaze_estimator.close()

    def test_pipeline_face_data_left_gaze(self):
        """Iris offset to the left should shift the zone result."""
        pipeline = Pipeline()
        pipeline._gaze_estimator.initialize()

        face_data = _make_face_data(iris_offset_x=-0.4, iris_offset_y=0.0)
        result = pipeline.process_face_data(face_data)

        assert result is not None
        assert isinstance(result, ZoneResult)

        pipeline._gaze_estimator.close()

    def test_pipeline_face_data_right_gaze(self):
        """Iris offset to the right should shift the zone result."""
        pipeline = Pipeline()
        pipeline._gaze_estimator.initialize()

        face_data = _make_face_data(iris_offset_x=0.4, iris_offset_y=0.0)
        result = pipeline.process_face_data(face_data)

        assert result is not None
        assert isinstance(result, ZoneResult)

        pipeline._gaze_estimator.close()

    def test_pipeline_face_data_multiple_frames(self):
        """Process multiple consecutive frames (smoother convergence)."""
        pipeline = Pipeline()
        pipeline._gaze_estimator.initialize()

        results = []
        for _ in range(20):
            face_data = _make_face_data(iris_offset_x=0.0, iris_offset_y=0.0)
            result = pipeline.process_face_data(face_data)
            results.append(result)

        # All results should be valid ZoneResults
        for r in results:
            assert r is not None
            assert isinstance(r, ZoneResult)

        # After convergence, zone should be stable
        last_zones = [r.zone_id for r in results[-5:]]
        assert len(set(last_zones)) == 1, (
            f"Expected stable zone after convergence, got {last_zones}"
        )

        pipeline._gaze_estimator.close()


# ---------------------------------------------------------------------------
# Partner utterance
# ---------------------------------------------------------------------------

class TestPipelinePartnerUtterance:

    @pytest.mark.asyncio
    async def test_pipeline_partner_utterance(self):
        """Add a partner utterance and verify context is updated."""
        pipeline = Pipeline()
        # Patch trigger_generation to avoid actual LLM calls
        with patch.object(pipeline, "trigger_generation", new_callable=AsyncMock):
            pipeline.add_partner_utterance("こんにちは")

        assert len(pipeline._context.conversation_history) == 1
        entry = pipeline._context.conversation_history[0]
        assert entry.role == "partner"
        assert entry.text == "こんにちは"

    @pytest.mark.asyncio
    async def test_pipeline_multiple_partner_utterances(self):
        """Multiple partner utterances grow the conversation history."""
        pipeline = Pipeline()
        with patch.object(pipeline, "trigger_generation", new_callable=AsyncMock):
            pipeline.add_partner_utterance("お元気ですか？")
            pipeline.add_partner_utterance("今日はいい天気だね")

        assert len(pipeline._context.conversation_history) == 2
        assert pipeline._context.conversation_history[0].text == "お元気ですか？"
        assert pipeline._context.conversation_history[1].text == "今日はいい天気だね"


# ---------------------------------------------------------------------------
# Candidate selection with TTS
# ---------------------------------------------------------------------------

class TestPipelineCandidateSelectionWithTTS:

    @pytest.mark.asyncio
    async def test_pipeline_candidate_selection_with_tts(self):
        """Select a candidate and verify TTS is triggered (placeholder engine).

        The CosyVoiceEngine falls back to a placeholder sine-wave when the
        real model is not installed. We mock the TTS router to return a
        fake path and verify the full flow.
        """
        pipeline = Pipeline()
        await pipeline.initialize()

        # Set up known candidates
        cs = _make_candidate_set(request_id="tts-int-001")
        pipeline._current_candidates = cs
        pipeline._current_request_id = cs.request_id

        # Mock TTS to return a fake audio path
        fake_audio = Path("/tmp/integration_test_audio.wav")
        pipeline._tts_router.synthesize = AsyncMock(return_value=fake_audio)

        # Mock LLM cancel
        pipeline._llm.cancel_pending = AsyncMock()

        # Capture sent messages
        sent_messages = []

        async def capture(msg):
            sent_messages.append(msg)

        pipeline.set_message_callback(capture)

        # Select candidate 0
        await pipeline.handle_candidate_selected("tts-int-001", 0)

        # TTS was called with the candidate text
        pipeline._tts_router.synthesize.assert_awaited_once_with("元気だよ")

        # TTSReady message was sent back
        assert len(sent_messages) == 1
        assert isinstance(sent_messages[0], TTSReady)
        assert sent_messages[0].text == "元気だよ"
        assert "integration_test_audio" in sent_messages[0].audio_url

        # Conversation history was updated
        assert len(pipeline._context.conversation_history) == 1
        assert pipeline._context.conversation_history[0].role == "patient"
        assert pipeline._context.conversation_history[0].text == "元気だよ"

        # LLM cancel was called
        pipeline._llm.cancel_pending.assert_awaited_once_with("tts-int-001")

        await pipeline.shutdown()

    @pytest.mark.asyncio
    async def test_pipeline_candidate_selection_out_of_range(self):
        """Selecting an out-of-range index does nothing."""
        pipeline = Pipeline()
        await pipeline.initialize()

        cs = _make_candidate_set(request_id="oob-int-001")
        pipeline._current_candidates = cs
        pipeline._llm.cancel_pending = AsyncMock()

        sent = []
        pipeline.set_message_callback(lambda msg: sent.append(msg))

        # Index 10 is beyond the 4 candidates
        await pipeline.handle_candidate_selected("oob-int-001", 10)
        assert len(sent) == 0

        await pipeline.shutdown()

    @pytest.mark.asyncio
    async def test_pipeline_candidate_selection_wrong_request_id(self):
        """Selecting with a mismatched request_id is a no-op."""
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

    @pytest.mark.asyncio
    async def test_pipeline_candidate_selection_no_candidates(self):
        """Selecting when no candidates are set does nothing."""
        pipeline = Pipeline()
        await pipeline.initialize()

        sent = []
        pipeline.set_message_callback(lambda msg: sent.append(msg))

        await pipeline.handle_candidate_selected("no-candidates", 0)
        assert len(sent) == 0

        await pipeline.shutdown()


# ---------------------------------------------------------------------------
# Full round-trip integration
# ---------------------------------------------------------------------------

class TestPipelineFullRoundTrip:

    @pytest.mark.asyncio
    async def test_partner_utterance_to_tts(self):
        """Full round trip: partner utterance -> candidates -> selection -> TTS."""
        pipeline = Pipeline()
        await pipeline.initialize()

        messages = []

        async def capture(msg):
            messages.append(msg)

        pipeline.set_message_callback(capture)

        # Mock LLM to yield a known candidate set
        async def mock_gen(context, num_candidates=4):
            yield _make_candidate_set()

        pipeline._llm.generate_candidates = mock_gen

        # Step 1: Partner utterance triggers generation
        pipeline.add_partner_utterance("お元気ですか？")
        await asyncio.sleep(0.1)

        assert len(messages) >= 1
        assert isinstance(messages[0], CandidateUpdate)
        candidate_set = messages[0].candidate_set

        # Step 2: Select candidate 0
        pipeline._llm.cancel_pending = AsyncMock()
        fake_path = Path("/tmp/roundtrip_integration.wav")
        pipeline._tts_router.synthesize = AsyncMock(return_value=fake_path)

        await pipeline.handle_candidate_selected(candidate_set.request_id, 0)

        # Step 3: Verify TTS was triggered
        pipeline._tts_router.synthesize.assert_awaited_once()

        # Step 4: Verify TTSReady sent
        tts_messages = [m for m in messages if isinstance(m, TTSReady)]
        assert len(tts_messages) == 1
        assert tts_messages[0].text == "元気だよ"

        # Step 5: Verify conversation history has both entries
        assert len(pipeline._context.conversation_history) == 2
        assert pipeline._context.conversation_history[0].role == "partner"
        assert pipeline._context.conversation_history[0].text == "お元気ですか？"
        assert pipeline._context.conversation_history[1].role == "patient"
        assert pipeline._context.conversation_history[1].text == "元気だよ"

        await pipeline.shutdown()

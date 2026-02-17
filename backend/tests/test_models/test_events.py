"""Tests for event and candidate models."""

import json

from voicereach.models.events import (
    Candidate,
    CandidateSet,
    EventType,
    GenerationStage,
    GazeUpdate,
    IALEvent,
    InputSource,
    IntentAxis,
    ScrollDirection,
)


class TestIALEvent:
    def test_create_select_event(self):
        event = IALEvent(
            event_type=EventType.SELECT,
            source=InputSource.GAZE,
            target_id=2,
            confidence=0.87,
        )
        assert event.event_type == EventType.SELECT
        assert event.target_id == 2
        assert event.confidence == 0.87

    def test_create_emergency_event(self):
        event = IALEvent(
            event_type=EventType.EMERGENCY,
            source=InputSource.FINGER,
        )
        assert event.event_type == EventType.EMERGENCY
        assert event.target_id is None
        assert event.confidence == 1.0

    def test_create_scroll_event(self):
        event = IALEvent(
            event_type=EventType.SCROLL,
            source=InputSource.KEYBOARD,
            scroll_direction=ScrollDirection.DOWN,
        )
        assert event.scroll_direction == ScrollDirection.DOWN

    def test_confidence_bounds(self):
        import pytest
        with pytest.raises(Exception):
            IALEvent(
                event_type=EventType.SELECT,
                source=InputSource.GAZE,
                confidence=1.5,
            )

    def test_roundtrip_json(self, sample_ial_event: IALEvent):
        data = sample_ial_event.model_dump_json()
        restored = IALEvent.model_validate_json(data)
        assert restored == sample_ial_event


class TestCandidate:
    def test_create_candidate(self):
        c = Candidate(
            text="何で表彰されたの？",
            intent_axis=IntentAxis.QUESTION,
            confidence=0.7,
            generation_stage=GenerationStage.LOCAL_QUALITY,
            latency_ms=350,
        )
        assert c.intent_axis == IntentAxis.QUESTION
        assert c.generation_stage == GenerationStage.LOCAL_QUALITY

    def test_all_intent_axes(self):
        axes = list(IntentAxis)
        assert len(axes) == 7

    def test_all_generation_stages(self):
        assert GenerationStage.LOCAL_FAST == 1
        assert GenerationStage.LOCAL_QUALITY == 2
        assert GenerationStage.CLOUD == 3


class TestCandidateSet:
    def test_max_candidates(self):
        candidates = [
            Candidate(
                text=f"候補{i}",
                intent_axis=IntentAxis.EMOTIONAL_RESPONSE,
                confidence=0.8,
                generation_stage=GenerationStage.LOCAL_FAST,
                latency_ms=150,
            )
            for i in range(4)
        ]
        cs = CandidateSet(
            candidates=candidates,
            stage=GenerationStage.LOCAL_FAST,
            request_id="req-001",
        )
        assert len(cs.candidates) == 4

    def test_over_max_candidates_rejected(self):
        import pytest
        candidates = [
            Candidate(
                text=f"候補{i}",
                intent_axis=IntentAxis.EMOTIONAL_RESPONSE,
                confidence=0.8,
                generation_stage=GenerationStage.LOCAL_FAST,
                latency_ms=150,
            )
            for i in range(5)
        ]
        with pytest.raises(Exception):
            CandidateSet(
                candidates=candidates,
                stage=GenerationStage.LOCAL_FAST,
                request_id="req-001",
            )

    def test_roundtrip_json(self, sample_candidate_set: CandidateSet):
        data = sample_candidate_set.model_dump_json()
        restored = CandidateSet.model_validate_json(data)
        assert restored.request_id == sample_candidate_set.request_id
        assert len(restored.candidates) == len(sample_candidate_set.candidates)


class TestWebSocketMessages:
    def test_gaze_update(self):
        msg = GazeUpdate(zone_id=3, confidence=0.9, timestamp_ms=1234567890)
        data = json.loads(msg.model_dump_json())
        assert data["type"] == "gaze_update"
        assert data["zone_id"] == 3

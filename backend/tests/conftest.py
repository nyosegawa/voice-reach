"""Shared test fixtures for VoiceReach backend tests."""

import pytest

from voicereach.models.events import (
    Candidate,
    CandidateSet,
    GenerationStage,
    IALEvent,
    EventType,
    InputSource,
    IntentAxis,
)
from voicereach.models.context import ContextFrame, PatientState


@pytest.fixture
def sample_ial_event() -> IALEvent:
    return IALEvent(
        event_type=EventType.SELECT,
        source=InputSource.GAZE,
        target_id=2,
        confidence=0.87,
    )


@pytest.fixture
def sample_candidate() -> Candidate:
    return Candidate(
        text="すごいじゃん！",
        intent_axis=IntentAxis.EMOTIONAL_RESPONSE,
        confidence=0.8,
        generation_stage=GenerationStage.LOCAL_QUALITY,
        latency_ms=350,
    )


@pytest.fixture
def sample_candidate_set(sample_candidate: Candidate) -> CandidateSet:
    return CandidateSet(
        candidates=[sample_candidate],
        stage=GenerationStage.LOCAL_QUALITY,
        request_id="test-req-001",
    )


@pytest.fixture
def sample_context_frame() -> ContextFrame:
    return ContextFrame(
        patient=PatientState(),
        current_zone_id=2,
    )

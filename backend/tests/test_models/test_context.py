"""Tests for context models."""

from voicereach.models.context import (
    ALSStage,
    ContextFrame,
    ConversationEntry,
    EmotionState,
    EnvironmentContext,
    PatientState,
)


class TestPatientState:
    def test_defaults(self):
        state = PatientState()
        assert state.als_stage == ALSStage.STAGE_1
        assert state.active_input_source == "gaze"
        assert state.emotion.valence == 0.0
        assert state.fatigue_level == 0.0

    def test_als_stages(self):
        for stage in ALSStage:
            state = PatientState(als_stage=stage)
            assert state.als_stage == stage


class TestContextFrame:
    def test_defaults(self):
        frame = ContextFrame()
        assert frame.patient.als_stage == ALSStage.STAGE_1
        assert frame.conversation_history == []
        assert frame.pvp_text is None

    def test_with_conversation(self):
        frame = ContextFrame(
            conversation_history=[
                ConversationEntry(role="partner", text="今日は調子どう？"),
                ConversationEntry(role="patient", text="まあまあだよ"),
            ]
        )
        assert len(frame.conversation_history) == 2

    def test_roundtrip_json(self, sample_context_frame: ContextFrame):
        data = sample_context_frame.model_dump_json()
        restored = ContextFrame.model_validate_json(data)
        assert restored.current_zone_id == sample_context_frame.current_zone_id

    def test_with_environment(self):
        frame = ContextFrame(
            environment=EnvironmentContext(
                location="hospital",
                people_present=["wife", "doctor"],
                activity="medical_consultation",
            )
        )
        assert frame.environment.location == "hospital"
        assert len(frame.environment.people_present) == 2

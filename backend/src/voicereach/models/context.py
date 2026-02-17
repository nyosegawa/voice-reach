"""Context and state models for VoiceReach."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ALSStage(int, Enum):
    """ALS progression stage (based on ALSFRS-R hand writing score)."""
    STAGE_1 = 1  # Strong: normal fine motor
    STAGE_2 = 2  # Weakening: slow but all functions
    STAGE_3 = 3  # Minimal: severe limitations
    STAGE_4 = 4  # No movement: requires full assistance


class EmotionState(BaseModel):
    """Estimated emotional state from 4-channel detection."""
    valence: float = Field(ge=-1.0, le=1.0, default=0.0)
    arousal: float = Field(ge=-1.0, le=1.0, default=0.0)
    confidence: float = Field(ge=0.0, le=1.0, default=0.0)


class ConversationEntry(BaseModel):
    """A single entry in the conversation history."""
    role: str  # "patient" or "partner"
    text: str
    timestamp: datetime = Field(default_factory=datetime.now)
    was_selected: bool = True  # False if typed via character input


class PatientState(BaseModel):
    """Current state of the patient for context-aware generation."""
    als_stage: ALSStage = ALSStage.STAGE_1
    active_input_source: str = "gaze"
    emotion: EmotionState = Field(default_factory=EmotionState)
    fatigue_level: float = Field(ge=0.0, le=1.0, default=0.0)


class EnvironmentContext(BaseModel):
    """Environment information from VLM or manual setting."""
    location: str = "home"
    people_present: list[str] = Field(default_factory=list)
    time_of_day: str = "daytime"
    activity: str = ""
    description: str = ""


class ContextFrame(BaseModel):
    """Complete context for candidate generation.

    Assembled by the pipeline coordinator and passed to the prompt builder.
    """
    patient: PatientState = Field(default_factory=PatientState)
    environment: EnvironmentContext = Field(default_factory=EnvironmentContext)
    conversation_history: list[ConversationEntry] = Field(default_factory=list)
    current_zone_id: int = 0
    pvp_text: str | None = None
    template_sentences: list[str] = Field(default_factory=list)

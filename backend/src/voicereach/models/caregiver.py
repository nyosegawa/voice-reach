"""Caregiver-facing models for notifications and logs."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class NotificationLevel(str, Enum):
    """Notification urgency levels."""
    INFO = "info"
    WARNING = "warning"
    EMERGENCY = "emergency"


class Notification(BaseModel):
    """Push notification to caregiver."""
    level: NotificationLevel
    title: str
    body: str
    timestamp: datetime = Field(default_factory=datetime.now)
    requires_ack: bool = False


class SpeechLogEntry(BaseModel):
    """A logged speech event for the caregiver to review."""
    text: str
    timestamp: datetime = Field(default_factory=datetime.now)
    generation_stage: int = 1
    was_spoken: bool = True
    emotion_valence: float = 0.0


class PatientStatusSummary(BaseModel):
    """Summary of patient status for caregiver dashboard."""
    is_online: bool = True
    last_activity: datetime | None = None
    utterances_today: int = 0
    avg_selection_time_ms: int = 0
    current_emotion: str = "neutral"
    active_input: str = "gaze"
    battery_level: float | None = None

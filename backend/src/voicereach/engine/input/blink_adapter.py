"""Blink-based input adapter using Eye Aspect Ratio (EAR).

Detects intentional blinks from MediaPipe landmarks for IAL events.
Used as fallback when finger input is no longer available.

Detection method: Eye Aspect Ratio (EAR)
- EAR < threshold for sustained duration = intentional blink
- Differentiates single/double/long blink patterns

Accuracy target: 98.03% (docs/10_PROGRESSIVE_ADAPTATION.md)
"""

from __future__ import annotations

import logging
import time

import numpy as np

from voicereach.models.events import EventType, IALEvent, InputSource

logger = logging.getLogger(__name__)

# MediaPipe landmark indices for EAR calculation
LEFT_EYE_EAR = [33, 160, 158, 133, 153, 144]   # p1-p6
RIGHT_EYE_EAR = [362, 385, 387, 263, 373, 380]  # p1-p6


def compute_ear(landmarks: np.ndarray, indices: list[int]) -> float:
    """Compute Eye Aspect Ratio.

    EAR = (|p2-p6| + |p3-p5|) / (2 * |p1-p4|)

    Returns ~0.25-0.3 for open eyes, < 0.2 for closed.
    """
    pts = landmarks[indices, :2]
    v1 = np.linalg.norm(pts[1] - pts[5])  # |p2-p6|
    v2 = np.linalg.norm(pts[2] - pts[4])  # |p3-p5|
    h = np.linalg.norm(pts[0] - pts[3])   # |p1-p4|

    if h < 1e-6:
        return 0.0
    return (v1 + v2) / (2.0 * h)


class BlinkAdapter:
    """Blink detection adapter using Eye Aspect Ratio."""

    def __init__(
        self,
        ear_threshold: float = 0.21,
        min_blink_duration_ms: int = 100,
        max_blink_duration_ms: int = 500,
        long_blink_duration_ms: int = 800,
        double_blink_window_ms: int = 600,
    ) -> None:
        self._ear_threshold = ear_threshold
        self._min_duration = min_blink_duration_ms
        self._max_duration = max_blink_duration_ms
        self._long_duration = long_blink_duration_ms
        self._double_window = double_blink_window_ms

        self._callback = None
        self._running = False

        # State
        self._eye_closed = False
        self._close_start_ms = 0
        self._last_blink_ms = 0
        self._blink_count = 0

    @property
    def source(self) -> InputSource:
        return InputSource.BLINK

    def set_callback(self, callback) -> None:
        self._callback = callback

    async def start(self) -> None:
        self._running = True
        logger.info("Blink adapter started")

    async def stop(self) -> None:
        self._running = False

    def process_landmarks(self, landmarks: np.ndarray) -> None:
        """Process facial landmarks to detect blinks.

        Call this for each frame with the full landmark array.
        """
        if not self._running or self._callback is None:
            return

        left_ear = compute_ear(landmarks, LEFT_EYE_EAR)
        right_ear = compute_ear(landmarks, RIGHT_EYE_EAR)
        avg_ear = (left_ear + right_ear) / 2.0

        now_ms = int(time.time() * 1000)

        if avg_ear < self._ear_threshold:
            if not self._eye_closed:
                self._eye_closed = True
                self._close_start_ms = now_ms
        else:
            if self._eye_closed:
                self._eye_closed = False
                duration = now_ms - self._close_start_ms
                self._handle_blink(duration, now_ms)

    def _handle_blink(self, duration_ms: int, now_ms: int) -> None:
        """Classify blink and emit IAL event."""
        if duration_ms < self._min_duration:
            return  # Too short, likely involuntary

        if duration_ms > self._long_duration:
            # Long blink = CANCEL
            self._emit(EventType.CANCEL, now_ms)
            self._blink_count = 0
            return

        if duration_ms > self._max_duration:
            return  # Too long for regular blink, too short for long

        # Regular blink
        if now_ms - self._last_blink_ms < self._double_window:
            self._blink_count += 1
        else:
            self._blink_count = 1

        self._last_blink_ms = now_ms

        if self._blink_count >= 3:
            self._emit(EventType.EMERGENCY, now_ms)
            self._blink_count = 0
        elif self._blink_count == 2:
            self._emit(EventType.CONFIRM, now_ms)
            self._blink_count = 0
        # Single blink: don't emit immediately, wait for double window

    def _emit(self, event_type: EventType, timestamp_ms: int) -> None:
        """Emit an IAL event."""
        if self._callback:
            self._callback(IALEvent(
                event_type=event_type,
                source=InputSource.BLINK,
                timestamp_ms=timestamp_ms,
            ))

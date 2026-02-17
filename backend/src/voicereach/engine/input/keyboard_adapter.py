"""Keyboard input adapter for development.

Maps keyboard keys to IAL events so the full system can be
tested without any special hardware.

Key mappings:
- Space = CONFIRM (single tap)
- Backspace = CANCEL (double tap)
- 1-4 = SELECT candidate 1-4
- Escape = EMERGENCY (triple tap)
- Arrow keys = SCROLL
"""

from __future__ import annotations

import asyncio
import logging
import time

from voicereach.models.events import EventType, IALEvent, InputSource, ScrollDirection

logger = logging.getLogger(__name__)


class KeyboardAdapter:
    """Keyboard-based input adapter for development mode."""

    def __init__(self) -> None:
        self._callback = None
        self._running = False
        self._task: asyncio.Task | None = None

    @property
    def source(self) -> InputSource:
        return InputSource.KEYBOARD

    def set_callback(self, callback) -> None:
        self._callback = callback

    async def start(self) -> None:
        """Start listening for keyboard events."""
        self._running = True
        logger.info("Keyboard adapter started (dev mode)")
        logger.info("Keys: Space=CONFIRM, Backspace=CANCEL, 1-4=SELECT, Esc=EMERGENCY, Arrows=SCROLL")

    async def stop(self) -> None:
        """Stop listening."""
        self._running = False
        if self._task:
            self._task.cancel()

    def handle_key(self, key: str) -> None:
        """Process a key press and emit corresponding IAL event.

        This is called externally (e.g., from the WebSocket handler
        when receiving keyboard events from the Electron app).
        """
        if not self._callback:
            return

        event = self._key_to_event(key)
        if event:
            self._callback(event)

    def _key_to_event(self, key: str) -> IALEvent | None:
        """Convert a key string to an IAL event."""
        ts = int(time.time() * 1000)

        if key == " " or key == "Space":
            return IALEvent(
                event_type=EventType.CONFIRM,
                source=InputSource.KEYBOARD,
                timestamp_ms=ts,
            )

        if key == "Backspace":
            return IALEvent(
                event_type=EventType.CANCEL,
                source=InputSource.KEYBOARD,
                timestamp_ms=ts,
            )

        if key == "Escape":
            return IALEvent(
                event_type=EventType.EMERGENCY,
                source=InputSource.KEYBOARD,
                timestamp_ms=ts,
            )

        if key in ("1", "2", "3", "4"):
            return IALEvent(
                event_type=EventType.SELECT,
                source=InputSource.KEYBOARD,
                target_id=int(key) - 1,
                timestamp_ms=ts,
            )

        scroll_map = {
            "ArrowUp": ScrollDirection.UP,
            "ArrowDown": ScrollDirection.DOWN,
            "ArrowLeft": ScrollDirection.LEFT,
            "ArrowRight": ScrollDirection.RIGHT,
        }
        if key in scroll_map:
            return IALEvent(
                event_type=EventType.SCROLL,
                source=InputSource.KEYBOARD,
                scroll_direction=scroll_map[key],
                timestamp_ms=ts,
            )

        return None

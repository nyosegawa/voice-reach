"""Input Abstraction Layer (IAL) - unified input event bus.

Aggregates input events from all sources (gaze, finger, blink, keyboard)
into a unified IALEvent stream via pub/sub pattern.

Design principles (docs/02_EYE_TRACKING_AND_INPUT.md):
1. Unified events: All inputs map to common event types
2. Hot-swap: Input source switching without restart
3. Plugin architecture: New adapters via InputAdapter protocol
"""

from __future__ import annotations

import asyncio
import logging
from typing import Callable, Protocol, runtime_checkable

from voicereach.models.events import IALEvent, InputSource

logger = logging.getLogger(__name__)

EventCallback = Callable[[IALEvent], None]


@runtime_checkable
class InputAdapter(Protocol):
    """Protocol for input source adapters."""

    @property
    def source(self) -> InputSource: ...

    async def start(self) -> None: ...

    async def stop(self) -> None: ...

    def set_callback(self, callback: EventCallback) -> None: ...


class IAL:
    """Input Abstraction Layer.

    Central event bus that aggregates events from registered input adapters.
    Subscribers receive all events regardless of source.
    """

    def __init__(self) -> None:
        self._adapters: dict[InputSource, InputAdapter] = {}
        self._subscribers: list[EventCallback] = []
        self._running = False

    def register_adapter(self, adapter: InputAdapter) -> None:
        """Register an input adapter."""
        source = adapter.source
        if source in self._adapters:
            logger.warning("Replacing existing adapter for %s", source)
        self._adapters[source] = adapter
        adapter.set_callback(self._on_event)
        logger.info("Registered adapter: %s", source)

    def subscribe(self, callback: EventCallback) -> None:
        """Subscribe to all IAL events."""
        self._subscribers.append(callback)

    def unsubscribe(self, callback: EventCallback) -> None:
        """Unsubscribe from IAL events."""
        self._subscribers.remove(callback)

    async def start(self) -> None:
        """Start all registered adapters."""
        self._running = True
        for source, adapter in self._adapters.items():
            try:
                await adapter.start()
                logger.info("Started adapter: %s", source)
            except Exception:
                logger.exception("Failed to start adapter: %s", source)

    async def stop(self) -> None:
        """Stop all adapters."""
        self._running = False
        for source, adapter in self._adapters.items():
            try:
                await adapter.stop()
            except Exception:
                logger.exception("Failed to stop adapter: %s", source)

    def _on_event(self, event: IALEvent) -> None:
        """Internal callback when an adapter emits an event."""
        if not self._running:
            return
        for subscriber in self._subscribers:
            try:
                subscriber(event)
            except Exception:
                logger.exception("Error in IAL subscriber")

    @property
    def active_sources(self) -> list[InputSource]:
        """List of registered input sources."""
        return list(self._adapters.keys())

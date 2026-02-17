"""Tests for IAL and input adapters."""

import asyncio

import pytest

from voicereach.engine.input.ial import IAL
from voicereach.engine.input.keyboard_adapter import KeyboardAdapter
from voicereach.models.events import EventType, IALEvent, InputSource


class TestKeyboardAdapter:
    def test_space_is_confirm(self):
        adapter = KeyboardAdapter()
        events = []
        adapter.set_callback(events.append)
        adapter.handle_key("Space")
        assert len(events) == 1
        assert events[0].event_type == EventType.CONFIRM

    def test_number_keys_are_select(self):
        adapter = KeyboardAdapter()
        events = []
        adapter.set_callback(events.append)
        for key in ("1", "2", "3", "4"):
            adapter.handle_key(key)
        assert len(events) == 4
        assert all(e.event_type == EventType.SELECT for e in events)
        assert [e.target_id for e in events] == [0, 1, 2, 3]

    def test_escape_is_emergency(self):
        adapter = KeyboardAdapter()
        events = []
        adapter.set_callback(events.append)
        adapter.handle_key("Escape")
        assert events[0].event_type == EventType.EMERGENCY

    def test_backspace_is_cancel(self):
        adapter = KeyboardAdapter()
        events = []
        adapter.set_callback(events.append)
        adapter.handle_key("Backspace")
        assert events[0].event_type == EventType.CANCEL

    def test_arrows_are_scroll(self):
        adapter = KeyboardAdapter()
        events = []
        adapter.set_callback(events.append)
        adapter.handle_key("ArrowUp")
        assert events[0].event_type == EventType.SCROLL

    def test_unknown_key_ignored(self):
        adapter = KeyboardAdapter()
        events = []
        adapter.set_callback(events.append)
        adapter.handle_key("q")
        assert len(events) == 0


class TestIAL:
    @pytest.mark.asyncio
    async def test_register_and_start(self):
        ial = IAL()
        adapter = KeyboardAdapter()
        ial.register_adapter(adapter)
        await ial.start()
        assert InputSource.KEYBOARD in ial.active_sources
        await ial.stop()

    @pytest.mark.asyncio
    async def test_event_propagation(self):
        ial = IAL()
        adapter = KeyboardAdapter()
        ial.register_adapter(adapter)

        received = []
        ial.subscribe(received.append)

        await ial.start()
        adapter.handle_key("Space")
        assert len(received) == 1
        assert received[0].event_type == EventType.CONFIRM
        await ial.stop()

    @pytest.mark.asyncio
    async def test_unsubscribe(self):
        ial = IAL()
        adapter = KeyboardAdapter()
        ial.register_adapter(adapter)

        received = []
        ial.subscribe(received.append)
        await ial.start()

        adapter.handle_key("Space")
        assert len(received) == 1

        ial.unsubscribe(received.append)
        adapter.handle_key("Space")
        assert len(received) == 1  # No new events
        await ial.stop()

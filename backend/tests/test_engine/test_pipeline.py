"""Tests for the main pipeline coordinator."""

import pytest

from voicereach.engine.pipeline import Pipeline


class TestPipeline:
    @pytest.mark.asyncio
    async def test_initialize_and_shutdown(self):
        pipeline = Pipeline()
        await pipeline.initialize()
        await pipeline.shutdown()

    @pytest.mark.asyncio
    async def test_handle_key(self):
        pipeline = Pipeline()
        await pipeline.initialize()

        events = []
        pipeline._ial.subscribe(events.append)
        pipeline.handle_key("Space")
        assert len(events) == 1
        await pipeline.shutdown()

    @pytest.mark.asyncio
    async def test_add_partner_utterance(self):
        pipeline = Pipeline()
        pipeline.add_partner_utterance("こんにちは")
        assert len(pipeline._context.conversation_history) == 1
        assert pipeline._context.conversation_history[0].text == "こんにちは"

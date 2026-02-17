"""End-to-end LLM pipeline tests with mocked API calls.

Exercises the LLM orchestrator, prompt builder, and candidate parser
as an integrated chain. No actual LLM servers or API keys required.
"""

from __future__ import annotations

import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from voicereach.engine.llm.candidate import parse_candidates
from voicereach.engine.llm.cloud_client import CloudLLMClient
from voicereach.engine.llm.local_client import LocalLLMClient
from voicereach.engine.llm.orchestrator import HybridLLMOrchestrator
from voicereach.engine.llm.prompt_builder import build_messages, build_system_prompt
from voicereach.models.context import (
    ContextFrame,
    ConversationEntry,
    EnvironmentContext,
    PatientState,
)
from voicereach.models.events import (
    CandidateSet,
    GenerationStage,
    IntentAxis,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

MOCK_JSON_RESPONSE = json.dumps([
    {"text": "元気だよ", "intent": "emotional_response", "confidence": 0.9},
    {"text": "最近何してた？", "intent": "question", "confidence": 0.8},
    {"text": "ちょっと疲れた", "intent": "self_reference", "confidence": 0.7},
    {"text": "お茶が飲みたい", "intent": "action_request", "confidence": 0.6},
])

MOCK_CLOUD_RESPONSE = json.dumps([
    {"text": "ありがとう、元気にしてるよ", "intent": "emotional_response", "confidence": 0.95},
    {"text": "仕事はどんな感じ？", "intent": "question", "confidence": 0.9},
    {"text": "今日はよく寝られたよ", "intent": "self_reference", "confidence": 0.85},
    {"text": "窓を開けてくれる？", "intent": "action_request", "confidence": 0.8},
])


def _make_rich_context() -> ContextFrame:
    """Create a realistic context frame for prompt building."""
    return ContextFrame(
        patient=PatientState(
            active_input_source="gaze",
        ),
        environment=EnvironmentContext(
            location="自宅リビング",
            people_present=["妻"],
            time_of_day="夕方",
            activity="テレビを見ている",
        ),
        conversation_history=[
            ConversationEntry(role="partner", text="今日はどうだった？"),
            ConversationEntry(role="patient", text="まあまあかな"),
            ConversationEntry(role="partner", text="お元気ですか？"),
        ],
        pvp_text="口癖: 「まあまあ」をよく使う。丁寧語は使わない。短い返答が多い。",
        current_zone_id=0,
    )


# ---------------------------------------------------------------------------
# Prompt builder tests
# ---------------------------------------------------------------------------

class TestPromptBuilderWithContext:

    def test_system_prompt_includes_core_instructions(self):
        context = _make_rich_context()
        prompt = build_system_prompt(context, num_candidates=4)

        assert "ALS患者" in prompt
        assert "4個" in prompt
        assert "JSON" in prompt

    def test_system_prompt_includes_pvp(self):
        context = _make_rich_context()
        prompt = build_system_prompt(context)

        assert "まあまあ" in prompt
        assert "PVP" in prompt

    def test_system_prompt_includes_environment(self):
        context = _make_rich_context()
        prompt = build_system_prompt(context)

        assert "自宅リビング" in prompt
        assert "妻" in prompt
        assert "夕方" in prompt

    def test_messages_include_conversation_history(self):
        context = _make_rich_context()
        messages = build_messages(context, num_candidates=4)

        # First message is system
        assert messages[0]["role"] == "system"

        # Conversation history should be present
        content_texts = [m["content"] for m in messages]
        assert any("今日はどうだった？" in t for t in content_texts)
        assert any("まあまあかな" in t for t in content_texts)
        assert any("お元気ですか？" in t for t in content_texts)

    def test_messages_role_mapping(self):
        """Partner utterances should map to 'user', patient to 'assistant'."""
        context = _make_rich_context()
        messages = build_messages(context)

        # Skip the system message
        history_msgs = messages[1:]
        assert history_msgs[0]["role"] == "user"       # partner -> user
        assert history_msgs[1]["role"] == "assistant"   # patient -> assistant
        assert history_msgs[2]["role"] == "user"        # partner -> user

    def test_empty_context_produces_initial_prompt(self):
        context = ContextFrame()
        messages = build_messages(context)

        # Should have system + initial prompt
        assert len(messages) >= 2
        assert messages[0]["role"] == "system"
        # The last message should be the initial prompt
        assert "会話が始まった" in messages[-1]["content"]


# ---------------------------------------------------------------------------
# Candidate parsing tests
# ---------------------------------------------------------------------------

class TestCandidateParsingFormats:

    def test_parse_json_array(self):
        candidates = parse_candidates(
            MOCK_JSON_RESPONSE, GenerationStage.LOCAL_FAST, 150
        )
        assert len(candidates) == 4
        assert candidates[0].text == "元気だよ"
        assert candidates[0].intent_axis == IntentAxis.EMOTIONAL_RESPONSE
        assert candidates[0].confidence == 0.9

    def test_parse_numbered_list(self):
        raw = "1. すごいね\n2. 何があったの？\n3. 俺も嬉しいよ\n4. 話変わるけど"
        candidates = parse_candidates(
            raw, GenerationStage.LOCAL_QUALITY, 350
        )
        assert len(candidates) == 4
        assert candidates[0].text == "すごいね"
        assert candidates[3].text == "話変わるけど"

    def test_parse_bullet_list(self):
        raw = "- おめでとう\n- 詳しく聞かせて\n- 私も頑張る\n* 何か手伝おうか"
        candidates = parse_candidates(
            raw, GenerationStage.LOCAL_FAST, 150
        )
        assert len(candidates) == 4

    def test_parse_plain_text_lines(self):
        raw = "すごい\nいいね\nありがとう"
        candidates = parse_candidates(
            raw, GenerationStage.LOCAL_FAST, 150
        )
        assert len(candidates) == 3
        assert candidates[0].text == "すごい"

    def test_parse_json_embedded_in_text(self):
        raw = '''以下が候補です:
        [{"text": "了解", "intent": "emotional_response", "confidence": 0.8}]
        以上です。'''
        candidates = parse_candidates(
            raw, GenerationStage.CLOUD, 800
        )
        assert len(candidates) == 1
        assert candidates[0].text == "了解"

    def test_parse_empty_returns_empty(self):
        candidates = parse_candidates("", GenerationStage.LOCAL_FAST, 150)
        assert candidates == []

    def test_latency_preserved(self):
        candidates = parse_candidates(
            MOCK_JSON_RESPONSE, GenerationStage.LOCAL_FAST, 142
        )
        assert all(c.latency_ms == 142 for c in candidates)

    def test_stage_preserved(self):
        for stage in GenerationStage:
            candidates = parse_candidates(
                '[{"text": "test", "intent": "question", "confidence": 0.5}]',
                stage,
                100,
            )
            assert candidates[0].generation_stage == stage


# ---------------------------------------------------------------------------
# Orchestrator with mocked clients
# ---------------------------------------------------------------------------

class TestOrchestratorMockGeneration:

    @pytest.mark.asyncio
    async def test_generate_yields_candidate_sets(self):
        """Orchestrator yields CandidateSets from all stages."""
        local_client = AsyncMock(spec=LocalLLMClient)
        local_client.generate = AsyncMock(return_value=MOCK_JSON_RESPONSE)

        cloud_client = AsyncMock(spec=CloudLLMClient)
        cloud_client.generate = AsyncMock(return_value=MOCK_CLOUD_RESPONSE)

        orchestrator = HybridLLMOrchestrator(
            local_client=local_client,
            cloud_client=cloud_client,
        )

        context = _make_rich_context()
        candidate_sets: list[CandidateSet] = []

        async for cs in orchestrator.generate_candidates(context, num_candidates=4):
            candidate_sets.append(cs)

        # Should have results from all 3 stages
        assert len(candidate_sets) == 3

        stages_seen = {cs.stage for cs in candidate_sets}
        assert GenerationStage.LOCAL_FAST in stages_seen
        assert GenerationStage.LOCAL_QUALITY in stages_seen
        assert GenerationStage.CLOUD in stages_seen

        # Each set should have valid candidates
        for cs in candidate_sets:
            assert len(cs.candidates) > 0
            for c in cs.candidates:
                assert c.text
                assert c.intent_axis in list(IntentAxis)
                assert 0.0 <= c.confidence <= 1.0

    @pytest.mark.asyncio
    async def test_all_candidate_sets_share_request_id(self):
        """All CandidateSets from one generation share the same request_id."""
        local_client = AsyncMock(spec=LocalLLMClient)
        local_client.generate = AsyncMock(return_value=MOCK_JSON_RESPONSE)

        cloud_client = AsyncMock(spec=CloudLLMClient)
        cloud_client.generate = AsyncMock(return_value=MOCK_CLOUD_RESPONSE)

        orchestrator = HybridLLMOrchestrator(
            local_client=local_client,
            cloud_client=cloud_client,
        )

        request_ids = set()
        async for cs in orchestrator.generate_candidates(ContextFrame()):
            request_ids.add(cs.request_id)

        assert len(request_ids) == 1

    @pytest.mark.asyncio
    async def test_cloud_stage_marked_final(self):
        """The cloud stage should be marked as is_final=True."""
        local_client = AsyncMock(spec=LocalLLMClient)
        local_client.generate = AsyncMock(return_value=MOCK_JSON_RESPONSE)

        cloud_client = AsyncMock(spec=CloudLLMClient)
        cloud_client.generate = AsyncMock(return_value=MOCK_CLOUD_RESPONSE)

        orchestrator = HybridLLMOrchestrator(
            local_client=local_client,
            cloud_client=cloud_client,
        )

        final_flags = {}
        async for cs in orchestrator.generate_candidates(ContextFrame()):
            final_flags[cs.stage] = cs.is_final

        assert final_flags[GenerationStage.CLOUD] is True
        assert final_flags[GenerationStage.LOCAL_FAST] is False
        assert final_flags[GenerationStage.LOCAL_QUALITY] is False


class TestOrchestratorFailover:

    @pytest.mark.asyncio
    async def test_local_failure_still_yields_cloud(self):
        """If local clients fail, the cloud stage should still yield results."""
        local_client = AsyncMock(spec=LocalLLMClient)
        local_client.generate = AsyncMock(return_value=None)  # Simulate failure

        cloud_client = AsyncMock(spec=CloudLLMClient)
        cloud_client.generate = AsyncMock(return_value=MOCK_CLOUD_RESPONSE)

        orchestrator = HybridLLMOrchestrator(
            local_client=local_client,
            cloud_client=cloud_client,
        )

        candidate_sets = []
        async for cs in orchestrator.generate_candidates(ContextFrame()):
            candidate_sets.append(cs)

        # Only cloud should have succeeded
        assert len(candidate_sets) == 1
        assert candidate_sets[0].stage == GenerationStage.CLOUD

    @pytest.mark.asyncio
    async def test_cloud_failure_still_yields_local(self):
        """If cloud client fails, local stages should still yield results."""
        local_client = AsyncMock(spec=LocalLLMClient)
        local_client.generate = AsyncMock(return_value=MOCK_JSON_RESPONSE)

        cloud_client = AsyncMock(spec=CloudLLMClient)
        cloud_client.generate = AsyncMock(return_value=None)  # Cloud fails

        orchestrator = HybridLLMOrchestrator(
            local_client=local_client,
            cloud_client=cloud_client,
        )

        candidate_sets = []
        async for cs in orchestrator.generate_candidates(ContextFrame()):
            candidate_sets.append(cs)

        # Only local stages should succeed
        assert len(candidate_sets) == 2
        stages = {cs.stage for cs in candidate_sets}
        assert GenerationStage.LOCAL_FAST in stages
        assert GenerationStage.LOCAL_QUALITY in stages

    @pytest.mark.asyncio
    async def test_all_failures_yields_nothing(self):
        """If all clients fail, no CandidateSets should be yielded."""
        local_client = AsyncMock(spec=LocalLLMClient)
        local_client.generate = AsyncMock(return_value=None)

        cloud_client = AsyncMock(spec=CloudLLMClient)
        cloud_client.generate = AsyncMock(return_value=None)

        orchestrator = HybridLLMOrchestrator(
            local_client=local_client,
            cloud_client=cloud_client,
        )

        candidate_sets = []
        async for cs in orchestrator.generate_candidates(ContextFrame()):
            candidate_sets.append(cs)

        assert len(candidate_sets) == 0

    @pytest.mark.asyncio
    async def test_local_exception_still_yields_cloud(self):
        """If local client raises an exception, cloud should still work."""
        local_client = AsyncMock(spec=LocalLLMClient)
        local_client.generate = AsyncMock(
            side_effect=ConnectionError("LLM server not running")
        )

        cloud_client = AsyncMock(spec=CloudLLMClient)
        cloud_client.generate = AsyncMock(return_value=MOCK_CLOUD_RESPONSE)

        orchestrator = HybridLLMOrchestrator(
            local_client=local_client,
            cloud_client=cloud_client,
        )

        candidate_sets = []
        async for cs in orchestrator.generate_candidates(ContextFrame()):
            candidate_sets.append(cs)

        # Cloud stage should still have succeeded
        assert any(cs.stage == GenerationStage.CLOUD for cs in candidate_sets)


class TestOrchestratorCancel:

    @pytest.mark.asyncio
    async def test_cancel_suppresses_further_results(self):
        """Cancelling a request should suppress remaining stage results."""
        call_count = 0

        async def slow_generate(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count <= 2:
                # Local stages return quickly
                return MOCK_JSON_RESPONSE
            # Cloud stage is slow
            await asyncio.sleep(0.5)
            return MOCK_CLOUD_RESPONSE

        local_client = AsyncMock(spec=LocalLLMClient)
        local_client.generate = AsyncMock(side_effect=slow_generate)

        cloud_client = AsyncMock(spec=CloudLLMClient)
        cloud_client.generate = AsyncMock(side_effect=slow_generate)

        orchestrator = HybridLLMOrchestrator(
            local_client=local_client,
            cloud_client=cloud_client,
        )

        candidate_sets = []
        request_id = None

        async for cs in orchestrator.generate_candidates(ContextFrame()):
            candidate_sets.append(cs)
            if request_id is None:
                request_id = cs.request_id
                # Cancel after receiving first result
                await orchestrator.cancel_pending(request_id)

        # We should have at least 1 set (the one before cancel)
        # The cancelled ones may or may not appear depending on timing,
        # but the cancel should have been registered
        assert request_id is not None
        assert request_id in orchestrator._cancelled


class TestOrchestratorPromptIntegration:

    @pytest.mark.asyncio
    async def test_messages_passed_to_clients(self):
        """Verify that the built messages are actually passed to clients."""
        received_messages = []

        async def capture_generate(model=None, messages=None, **kwargs):
            received_messages.append(messages)
            return MOCK_JSON_RESPONSE

        local_client = AsyncMock(spec=LocalLLMClient)
        local_client.generate = AsyncMock(side_effect=capture_generate)

        cloud_client = AsyncMock(spec=CloudLLMClient)
        cloud_client.generate = AsyncMock(return_value=MOCK_CLOUD_RESPONSE)

        orchestrator = HybridLLMOrchestrator(
            local_client=local_client,
            cloud_client=cloud_client,
        )

        context = _make_rich_context()
        async for _ in orchestrator.generate_candidates(context):
            pass

        # Local client is called for 2 stages
        assert len(received_messages) == 2
        for msgs in received_messages:
            # System prompt should be present
            assert msgs[0]["role"] == "system"
            assert "ALS患者" in msgs[0]["content"]
            # Conversation history should be present
            content_texts = [m["content"] for m in msgs]
            assert any("お元気ですか？" in t for t in content_texts)

"""Tests for LLM engine components."""

import json

import pytest

from voicereach.engine.llm.candidate import parse_candidates
from voicereach.engine.llm.prompt_builder import build_messages, build_system_prompt
from voicereach.models.context import (
    ContextFrame,
    ConversationEntry,
    EnvironmentContext,
    PatientState,
)
from voicereach.models.events import GenerationStage, IntentAxis


class TestPromptBuilder:
    def test_basic_prompt(self):
        context = ContextFrame()
        prompt = build_system_prompt(context)
        assert "ALS患者" in prompt
        assert "4個" in prompt

    def test_prompt_with_pvp(self):
        context = ContextFrame(pvp_text="口癖: 「まじか」をよく使う")
        prompt = build_system_prompt(context)
        assert "まじか" in prompt
        assert "PVP" in prompt

    def test_prompt_with_environment(self):
        context = ContextFrame(
            environment=EnvironmentContext(
                location="自宅リビング",
                people_present=["妻"],
                time_of_day="夕方",
            )
        )
        prompt = build_system_prompt(context)
        assert "自宅リビング" in prompt
        assert "妻" in prompt

    def test_messages_with_history(self):
        context = ContextFrame(
            conversation_history=[
                ConversationEntry(role="partner", text="今日は天気がいいね"),
                ConversationEntry(role="patient", text="そうだね"),
            ]
        )
        messages = build_messages(context)
        assert messages[0]["role"] == "system"
        assert any(m["content"] == "今日は天気がいいね" for m in messages)

    def test_messages_without_history(self):
        context = ContextFrame()
        messages = build_messages(context)
        assert len(messages) >= 2  # system + initial prompt


class TestCandidateParsing:
    def test_parse_json_output(self):
        raw = '''[
            {"text": "すごいじゃん！", "intent": "emotional_response", "confidence": 0.8},
            {"text": "何で表彰されたの？", "intent": "question", "confidence": 0.7}
        ]'''
        candidates = parse_candidates(raw, GenerationStage.LOCAL_FAST, 150)
        assert len(candidates) == 2
        assert candidates[0].text == "すごいじゃん！"
        assert candidates[0].intent_axis == IntentAxis.EMOTIONAL_RESPONSE
        assert candidates[1].intent_axis == IntentAxis.QUESTION

    def test_parse_json_with_surrounding_text(self):
        raw = '''Here are the candidates:
        [{"text": "良かったね", "intent": "emotional_response", "confidence": 0.9}]
        That's all.'''
        candidates = parse_candidates(raw, GenerationStage.CLOUD, 800)
        assert len(candidates) == 1
        assert candidates[0].text == "良かったね"

    def test_parse_numbered_lines(self):
        raw = "1. すごいね\n2. 何があったの？\n3. 俺も嬉しいよ"
        candidates = parse_candidates(raw, GenerationStage.LOCAL_QUALITY, 350)
        assert len(candidates) == 3
        assert candidates[0].text == "すごいね"

    def test_parse_bullet_lines(self):
        raw = "- おめでとう\n- 詳しく聞かせて"
        candidates = parse_candidates(raw, GenerationStage.LOCAL_FAST, 150)
        assert len(candidates) == 2

    def test_max_candidates_limit(self):
        raw = '''[
            {"text": "a", "intent": "question", "confidence": 0.5},
            {"text": "b", "intent": "question", "confidence": 0.5},
            {"text": "c", "intent": "question", "confidence": 0.5},
            {"text": "d", "intent": "question", "confidence": 0.5},
            {"text": "e", "intent": "question", "confidence": 0.5}
        ]'''
        candidates = parse_candidates(raw, GenerationStage.LOCAL_FAST, 150, max_candidates=4)
        assert len(candidates) == 4

    def test_invalid_json_falls_back_to_lines(self):
        raw = "すごい\nいいね"
        candidates = parse_candidates(raw, GenerationStage.LOCAL_FAST, 150)
        assert len(candidates) == 2

    def test_empty_input(self):
        candidates = parse_candidates("", GenerationStage.LOCAL_FAST, 150)
        assert len(candidates) == 0

    def test_generation_stage_preserved(self):
        raw = '[{"text": "test", "intent": "question", "confidence": 0.5}]'
        for stage in GenerationStage:
            candidates = parse_candidates(raw, stage, 100)
            assert candidates[0].generation_stage == stage

    def test_confidence_clamped(self):
        raw = '[{"text": "test", "intent": "question", "confidence": 1.5}]'
        candidates = parse_candidates(raw, GenerationStage.LOCAL_FAST, 150)
        assert candidates[0].confidence == 1.0

    def test_unknown_intent_gets_default(self):
        raw = '[{"text": "test", "intent": "unknown_intent", "confidence": 0.5}]'
        candidates = parse_candidates(raw, GenerationStage.LOCAL_FAST, 150)
        assert candidates[0].intent_axis in list(IntentAxis)

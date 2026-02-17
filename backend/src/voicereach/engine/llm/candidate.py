"""Candidate parsing and validation.

Parses LLM output into structured Candidate objects.
Handles various output formats (JSON, plain text).
"""

from __future__ import annotations

import json
import logging
import re

from voicereach.models.events import Candidate, GenerationStage, IntentAxis

logger = logging.getLogger(__name__)

VALID_INTENTS = {axis.value for axis in IntentAxis}

DEFAULT_INTENT_CYCLE = [
    IntentAxis.EMOTIONAL_RESPONSE,
    IntentAxis.QUESTION,
    IntentAxis.SELF_REFERENCE,
    IntentAxis.ACTION_REQUEST,
]


def parse_candidates(
    raw_text: str,
    stage: GenerationStage,
    latency_ms: int,
    max_candidates: int = 4,
) -> list[Candidate]:
    """Parse LLM output into Candidate objects.

    Tries JSON parsing first, then falls back to line-based parsing.
    """
    candidates = _try_parse_json(raw_text, stage, latency_ms)
    if not candidates:
        candidates = _try_parse_lines(raw_text, stage, latency_ms)

    return candidates[:max_candidates]


def _try_parse_json(
    raw_text: str, stage: GenerationStage, latency_ms: int
) -> list[Candidate]:
    """Try to parse JSON array output."""
    # Find JSON array in output
    match = re.search(r'\[[\s\S]*?\]', raw_text)
    if not match:
        return []

    try:
        items = json.loads(match.group())
    except json.JSONDecodeError:
        return []

    candidates = []
    for i, item in enumerate(items):
        if not isinstance(item, dict) or "text" not in item:
            continue

        intent_str = item.get("intent", "")
        intent = _resolve_intent(intent_str, i)
        confidence = float(item.get("confidence", 0.7))
        confidence = max(0.0, min(1.0, confidence))

        candidates.append(Candidate(
            text=item["text"].strip(),
            intent_axis=intent,
            confidence=confidence,
            generation_stage=stage,
            latency_ms=latency_ms,
        ))

    return candidates


def _try_parse_lines(
    raw_text: str, stage: GenerationStage, latency_ms: int
) -> list[Candidate]:
    """Fallback: parse numbered or plain text lines."""
    lines = raw_text.strip().split("\n")
    candidates = []

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        # Remove common prefixes: "1. ", "- ", "* ", etc.
        cleaned = re.sub(r'^[\d]+[.\)]\s*', '', line)
        cleaned = re.sub(r'^[-*]\s*', '', cleaned)
        cleaned = cleaned.strip().strip('"').strip("\u300c").strip("\u300d")

        if not cleaned or len(cleaned) > 100:
            continue

        candidates.append(Candidate(
            text=cleaned,
            intent_axis=DEFAULT_INTENT_CYCLE[i % len(DEFAULT_INTENT_CYCLE)],
            confidence=0.5,
            generation_stage=stage,
            latency_ms=latency_ms,
        ))

    return candidates


def _resolve_intent(intent_str: str, index: int) -> IntentAxis:
    """Resolve intent string to IntentAxis enum."""
    if intent_str in VALID_INTENTS:
        return IntentAxis(intent_str)
    # Fallback: cycle through default intents
    return DEFAULT_INTENT_CYCLE[index % len(DEFAULT_INTENT_CYCLE)]

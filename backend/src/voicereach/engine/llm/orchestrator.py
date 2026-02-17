"""Three-stage hybrid LLM orchestrator.

Coordinates concurrent inference across local and cloud LLMs:
  Stage 1: Qwen3-0.6B (Q5_K_M) ~150ms - tentative candidates
  Stage 2: Qwen3-1.7B (Q4_K_M) ~350ms - improved candidates
  Stage 3: Gemini 2.5 Flash     ~800ms - high-quality candidates

All stages run concurrently. Results are yielded as they complete.
"""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import AsyncIterator
from uuid import uuid4

from voicereach.config import settings
from voicereach.engine.llm.candidate import parse_candidates
from voicereach.engine.llm.cloud_client import CloudLLMClient
from voicereach.engine.llm.local_client import LocalLLMClient
from voicereach.engine.llm.prompt_builder import build_messages
from voicereach.models.context import ContextFrame
from voicereach.models.events import CandidateSet, GenerationStage

logger = logging.getLogger(__name__)


class HybridLLMOrchestrator:
    """Three-stage hybrid LLM inference pipeline."""

    def __init__(
        self,
        local_client: LocalLLMClient | None = None,
        cloud_client: CloudLLMClient | None = None,
    ) -> None:
        self._local = local_client or LocalLLMClient()
        self._cloud = cloud_client or CloudLLMClient()
        self._cancelled: set[str] = set()

    async def generate_candidates(
        self,
        context: ContextFrame,
        num_candidates: int = 4,
    ) -> AsyncIterator[CandidateSet]:
        """Generate candidates through three concurrent stages.

        Yields CandidateSets as each stage completes.
        Earlier stages yield first for immediate display.
        """
        request_id = uuid4().hex[:12]
        messages = build_messages(context, num_candidates)

        # Launch all stages concurrently
        tasks = {
            GenerationStage.LOCAL_FAST: asyncio.create_task(
                self._run_stage(
                    stage=GenerationStage.LOCAL_FAST,
                    messages=messages,
                    model=settings.local_llm_model_fast,
                    temperature=settings.stage1_temperature,
                    timeout_ms=settings.stage1_timeout_ms,
                    request_id=request_id,
                    num_candidates=num_candidates,
                )
            ),
            GenerationStage.LOCAL_QUALITY: asyncio.create_task(
                self._run_stage(
                    stage=GenerationStage.LOCAL_QUALITY,
                    messages=messages,
                    model=settings.local_llm_model_quality,
                    temperature=settings.stage2_temperature,
                    timeout_ms=settings.stage2_timeout_ms,
                    request_id=request_id,
                    num_candidates=num_candidates,
                )
            ),
            GenerationStage.CLOUD: asyncio.create_task(
                self._run_cloud_stage(
                    messages=messages,
                    temperature=settings.stage3_temperature,
                    timeout_ms=settings.stage3_timeout_ms,
                    request_id=request_id,
                    num_candidates=num_candidates,
                )
            ),
        }

        # Yield results as they complete
        completed_stages: set[GenerationStage] = set()
        for coro in asyncio.as_completed(tasks.values()):
            try:
                result = await coro
                if result and request_id not in self._cancelled:
                    completed_stages.add(result.stage)
                    is_final = result.stage == GenerationStage.CLOUD
                    result.is_final = is_final
                    yield result
            except asyncio.CancelledError:
                break
            except Exception:
                logger.exception("Stage failed")

        # Cancel any remaining tasks
        for task in tasks.values():
            if not task.done():
                task.cancel()

    async def cancel_pending(self, request_id: str) -> None:
        """Mark a request as cancelled (remaining stages will be skipped)."""
        self._cancelled.add(request_id)

    async def _run_stage(
        self,
        stage: GenerationStage,
        messages: list[dict[str, str]],
        model: str,
        temperature: float,
        timeout_ms: int,
        request_id: str,
        num_candidates: int,
    ) -> CandidateSet | None:
        """Run a local LLM stage."""
        start = time.monotonic()

        raw = await self._local.generate(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=200,
            timeout_s=timeout_ms / 1000,
        )

        if not raw:
            return None

        latency = int((time.monotonic() - start) * 1000)
        candidates = parse_candidates(raw, stage, latency, num_candidates)

        if not candidates:
            return None

        return CandidateSet(
            candidates=candidates,
            stage=stage,
            request_id=request_id,
        )

    async def _run_cloud_stage(
        self,
        messages: list[dict[str, str]],
        temperature: float,
        timeout_ms: int,
        request_id: str,
        num_candidates: int,
    ) -> CandidateSet | None:
        """Run the cloud LLM stage."""
        start = time.monotonic()

        raw = await self._cloud.generate(
            messages=messages,
            temperature=temperature,
            max_tokens=200,
            timeout_s=timeout_ms / 1000,
        )

        if not raw:
            return None

        latency = int((time.monotonic() - start) * 1000)
        candidates = parse_candidates(raw, GenerationStage.CLOUD, latency, num_candidates)

        if not candidates:
            return None

        return CandidateSet(
            candidates=candidates,
            stage=GenerationStage.CLOUD,
            request_id=request_id,
        )

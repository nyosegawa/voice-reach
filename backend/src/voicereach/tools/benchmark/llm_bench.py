"""Benchmark local LLM inference via the vllm-mlx server.

Measures time-to-first-token (TTFT), tokens-per-second throughput,
and memory usage for the configured local LLM models.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass

import numpy as np

from voicereach.config import settings

logger = logging.getLogger(__name__)


@dataclass
class LLMBenchResult:
    """Results from an LLM inference benchmark run."""

    model: str
    ttft_ms: float  # Time to first token (via streaming)
    tokens_per_second: float
    total_tokens: int
    total_time_ms: float
    prompt_tokens: int
    memory_mb: float | None  # If psutil available


async def _measure_streaming_ttft(
    base_url: str,
    model: str,
    messages: list[dict[str, str]],
    max_tokens: int,
    timeout_s: float = 10.0,
) -> tuple[float, int, float]:
    """Measure TTFT and throughput using the streaming API directly.

    Returns:
        (ttft_ms, total_tokens, total_time_ms)
    """
    from openai import AsyncOpenAI

    client = AsyncOpenAI(base_url=base_url, api_key="not-needed")

    t_start = time.perf_counter()
    ttft: float | None = None
    token_count = 0

    try:
        stream = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.5,
            max_tokens=max_tokens,
            stream=True,
            timeout=timeout_s,
        )

        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                if ttft is None:
                    ttft = (time.perf_counter() - t_start) * 1000.0
                token_count += 1

        total_time_ms = (time.perf_counter() - t_start) * 1000.0
    finally:
        await client.close()

    if ttft is None:
        ttft = total_time_ms

    return ttft, token_count, total_time_ms


async def _measure_non_streaming(
    base_url: str,
    model: str,
    messages: list[dict[str, str]],
    max_tokens: int,
    timeout_s: float = 10.0,
) -> tuple[int, float]:
    """Measure total generation time using non-streaming API.

    Returns:
        (total_tokens, total_time_ms)
    """
    from openai import AsyncOpenAI

    client = AsyncOpenAI(base_url=base_url, api_key="not-needed")

    try:
        t_start = time.perf_counter()
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.5,
            max_tokens=max_tokens,
            timeout=timeout_s,
        )
        total_time_ms = (time.perf_counter() - t_start) * 1000.0

        content = response.choices[0].message.content or ""
        # Rough token estimate: each chunk from streaming ~= 1 token.
        # For non-streaming, estimate from character count (Japanese ~1.5 char/token).
        total_tokens = max(1, len(content))
        if response.usage:
            total_tokens = response.usage.completion_tokens or total_tokens

        return total_tokens, total_time_ms
    finally:
        await client.close()


def _get_memory_mb() -> float | None:
    """Get current process memory usage in MB, or None if psutil unavailable."""
    try:
        import psutil

        process = psutil.Process()
        return process.memory_info().rss / (1024 * 1024)
    except (ImportError, Exception):
        return None


async def run_llm_benchmark(
    model: str | None = None,
    prompt: str = "日本語で、今日の天気について短く答えてください。",
    num_runs: int = 5,
    max_tokens: int = 100,
) -> LLMBenchResult | None:
    """Run an LLM inference benchmark against the local vllm-mlx server.

    Args:
        model: Model name. Defaults to settings.local_llm_model_fast.
        prompt: Prompt text for generation.
        num_runs: Number of runs to take median from.
        max_tokens: Maximum tokens per generation.

    Returns:
        LLMBenchResult with timing stats, or None if the server is unreachable.
    """
    from voicereach.engine.llm.local_client import LocalLLMClient

    model = model or settings.local_llm_model_fast
    base_url = settings.local_llm_base_url

    # Health check first
    client = LocalLLMClient(base_url=base_url)
    if not await client.health_check():
        logger.warning(
            "Local LLM server at %s is not reachable. Skipping LLM benchmark.",
            base_url,
        )
        return None

    messages = [{"role": "user", "content": prompt}]

    ttft_values: list[float] = []
    token_counts: list[int] = []
    total_times: list[float] = []

    # Try streaming measurement first
    use_streaming = True
    try:
        ttft, tokens, total_ms = await _measure_streaming_ttft(
            base_url, model, messages, max_tokens
        )
        # If it works, we got our first sample
        ttft_values.append(ttft)
        token_counts.append(tokens)
        total_times.append(total_ms)
    except Exception:
        logger.info("Streaming API not available, falling back to non-streaming")
        use_streaming = False

    remaining_runs = num_runs - len(ttft_values)

    for _ in range(remaining_runs):
        try:
            if use_streaming:
                ttft, tokens, total_ms = await _measure_streaming_ttft(
                    base_url, model, messages, max_tokens
                )
                ttft_values.append(ttft)
                token_counts.append(tokens)
                total_times.append(total_ms)
            else:
                tokens, total_ms = await _measure_non_streaming(
                    base_url, model, messages, max_tokens
                )
                # Without streaming we cannot measure TTFT, estimate it
                ttft_values.append(total_ms)
                token_counts.append(tokens)
                total_times.append(total_ms)
        except Exception:
            logger.exception("LLM benchmark run failed")
            continue

    if not ttft_values:
        logger.error("All LLM benchmark runs failed")
        return None

    arr_ttft = np.array(ttft_values)
    arr_tokens = np.array(token_counts)
    arr_times = np.array(total_times)

    # Compute tokens/second for each run, then take median
    tps_values = arr_tokens / (arr_times / 1000.0)  # tokens / seconds

    # Estimate prompt tokens (~1.5 chars per token for Japanese)
    prompt_tokens = max(1, len(prompt) * 2 // 3)

    memory_mb = _get_memory_mb()

    return LLMBenchResult(
        model=model,
        ttft_ms=float(np.median(arr_ttft)),
        tokens_per_second=float(np.median(tps_values)),
        total_tokens=int(np.median(arr_tokens)),
        total_time_ms=float(np.median(arr_times)),
        prompt_tokens=prompt_tokens,
        memory_mb=memory_mb,
    )

"""Benchmark TTS synthesis performance.

Measures cold-start latency, average synthesis time, and P95 latency
for the CosyVoice engine (or placeholder fallback).
"""

from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass

import numpy as np

logger = logging.getLogger(__name__)

DEFAULT_TEXTS = [
    "はい",
    "ありがとうございます",
    "今日の調子は良いです",
    "少し喉が渇きました。水をください。",
    "明日の午後に、リハビリの予定があります。準備をお願いします。",
]


@dataclass
class TTSBenchResult:
    """Results from a TTS synthesis benchmark run."""

    engine: str  # "cosyvoice" or "placeholder"
    first_synthesis_ms: float  # Cold start
    avg_synthesis_ms: float
    p95_synthesis_ms: float
    samples_generated: int
    sample_rate: int


async def run_tts_benchmark(
    texts: list[str] | None = None,
    num_runs: int = 10,
) -> TTSBenchResult:
    """Run a TTS synthesis benchmark.

    Args:
        texts: List of texts to synthesize. Defaults to a standard set of
               short/medium/long Japanese sentences.
        num_runs: Number of full cycles through all texts.

    Returns:
        TTSBenchResult with cold-start, average, and P95 latency stats.
    """
    from voicereach.engine.tts.cosyvoice import CosyVoiceEngine

    if texts is None:
        texts = DEFAULT_TEXTS

    engine = CosyVoiceEngine()
    await engine.initialize()

    engine_name = "cosyvoice" if engine.is_available else "placeholder"
    sample_rate = 24000  # CosyVoice default; placeholder also uses 24kHz

    latencies: list[float] = []
    first_synthesis_ms: float = 0.0
    temp_files: list[str] = []

    try:
        for run_idx in range(num_runs):
            for text in texts:
                t0 = time.perf_counter()
                result = await engine.synthesize(text)
                t1 = time.perf_counter()

                latency_ms = (t1 - t0) * 1000.0
                latencies.append(latency_ms)

                # Track first synthesis as cold start metric
                if run_idx == 0 and len(latencies) == 1:
                    first_synthesis_ms = latency_ms

                # Track temp files for cleanup
                if result is not None:
                    temp_files.append(str(result))

        samples_generated = len(latencies)

        if samples_generated == 0:
            return TTSBenchResult(
                engine=engine_name,
                first_synthesis_ms=0.0,
                avg_synthesis_ms=0.0,
                p95_synthesis_ms=0.0,
                samples_generated=0,
                sample_rate=sample_rate,
            )

        arr = np.array(latencies)
        return TTSBenchResult(
            engine=engine_name,
            first_synthesis_ms=first_synthesis_ms,
            avg_synthesis_ms=float(np.mean(arr)),
            p95_synthesis_ms=float(np.percentile(arr, 95)),
            samples_generated=samples_generated,
            sample_rate=sample_rate,
        )
    finally:
        # Clean up temporary audio files
        for path in temp_files:
            try:
                os.unlink(path)
            except OSError:
                pass

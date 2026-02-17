"""End-to-end pipeline benchmark (simulated).

Measures per-component latency and total round-trip time for the
VoiceReach gaze-to-speech pipeline. Runs fully in synthetic mode
without requiring cameras, LLM servers, or TTS models.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field

import numpy as np

logger = logging.getLogger(__name__)

# Design-doc estimated latencies (ms) for components not available locally
ESTIMATED_LATENCIES = {
    "llm_stage1_local_fast": 150.0,
    "llm_stage2_local_quality": 350.0,
    "llm_stage3_cloud": 800.0,
    "tts_cosyvoice": 200.0,
}


@dataclass
class PipelineBenchResult:
    """Results from an end-to-end pipeline benchmark."""

    gaze_to_zone_ms: float  # Gaze processing + zone mapping
    zone_to_candidates_ms: float  # IAL event -> LLM generation start
    total_round_trip_ms: float  # Full cycle simulated
    components: dict[str, float] = field(default_factory=dict)


def _bench_smoother(num_iterations: int = 1000) -> float:
    """Benchmark DualAxisSmoother throughput.

    Returns:
        Median latency per update in milliseconds.
    """
    from voicereach.engine.gaze.smoother import DualAxisSmoother

    smoother = DualAxisSmoother()
    rng = np.random.default_rng(42)

    # Generate realistic gaze coordinates with occasional saccades
    pitches = rng.normal(0.0, 5.0, num_iterations).astype(float)
    yaws = rng.normal(0.0, 5.0, num_iterations).astype(float)
    # Add saccades every ~50 frames
    for i in range(0, num_iterations, 50):
        pitches[i] += rng.normal(0, 30)
        yaws[i] += rng.normal(0, 30)

    latencies = []
    for i in range(num_iterations):
        t0 = time.perf_counter()
        smoother.update(float(pitches[i]), float(yaws[i]))
        t1 = time.perf_counter()
        latencies.append((t1 - t0) * 1000.0)

    return float(np.median(latencies))


def _bench_zone_mapper(num_iterations: int = 1000) -> float:
    """Benchmark ZoneMapper throughput.

    Returns:
        Median latency per map() call in milliseconds.
    """
    from voicereach.engine.gaze.zone_mapper import ZoneMapper

    mapper = ZoneMapper(num_zones=4)
    rng = np.random.default_rng(42)

    xs = rng.uniform(0.0, 1.0, num_iterations)
    ys = rng.uniform(0.0, 1.0, num_iterations)

    latencies = []
    for i in range(num_iterations):
        t0 = time.perf_counter()
        mapper.map(float(xs[i]), float(ys[i]))
        t1 = time.perf_counter()
        latencies.append((t1 - t0) * 1000.0)

    return float(np.median(latencies))


def _bench_ial_dispatch(num_iterations: int = 500) -> float:
    """Benchmark IAL event dispatch latency.

    Returns:
        Median latency per event dispatch in milliseconds.
    """
    from voicereach.engine.input.ial import IAL
    from voicereach.models.events import EventType, IALEvent, InputSource

    ial = IAL()
    received_count = 0

    def _callback(event: IALEvent) -> None:
        nonlocal received_count
        received_count += 1

    ial.subscribe(_callback)
    ial._running = True  # Enable dispatch without starting adapters

    latencies = []
    for _ in range(num_iterations):
        event = IALEvent(
            event_type=EventType.SELECT,
            source=InputSource.GAZE,
            target_id=0,
            confidence=0.9,
        )
        t0 = time.perf_counter()
        ial._on_event(event)
        t1 = time.perf_counter()
        latencies.append((t1 - t0) * 1000.0)

    return float(np.median(latencies))


async def _bench_llm_if_available() -> tuple[float | None, str]:
    """Try to benchmark actual LLM generation.

    Returns:
        (latency_ms or None, description)
    """
    try:
        from voicereach.engine.llm.local_client import LocalLLMClient
        from voicereach.config import settings

        client = LocalLLMClient()
        if not await client.health_check():
            return None, "server_unavailable"

        messages = [{"role": "user", "content": "こんにちは"}]
        t0 = time.perf_counter()
        result = await client.generate(
            model=settings.local_llm_model_fast,
            messages=messages,
            max_tokens=30,
            timeout_s=10.0,
        )
        t1 = time.perf_counter()

        if result is not None:
            return (t1 - t0) * 1000.0, "measured"
        return None, "generation_failed"
    except Exception:
        return None, "error"


async def run_pipeline_benchmark(
    use_synthetic: bool = True,
) -> PipelineBenchResult:
    """Run an end-to-end pipeline benchmark.

    Measures each component independently and combines into a simulated
    round-trip time. When use_synthetic=True (default), runs entirely
    without hardware or external services.

    Args:
        use_synthetic: Use synthetic data and estimates for unavailable
                       components. When False, attempts to use real LLM server.

    Returns:
        PipelineBenchResult with per-component and total timing.
    """
    components: dict[str, float] = {}

    # 1. Smoother benchmark
    smoother_ms = _bench_smoother()
    components["smoother"] = smoother_ms

    # 2. Zone mapper benchmark
    zone_mapper_ms = _bench_zone_mapper()
    components["zone_mapper"] = zone_mapper_ms

    # 3. IAL dispatch benchmark
    ial_ms = _bench_ial_dispatch()
    components["ial_dispatch"] = ial_ms

    # Gaze-to-zone = smoother + zone_mapper
    gaze_to_zone_ms = smoother_ms + zone_mapper_ms

    # 4. LLM latency
    llm_ms: float
    if not use_synthetic:
        measured, status = await _bench_llm_if_available()
        if measured is not None:
            llm_ms = measured
            components["llm_generation"] = llm_ms
            components["llm_source"] = 0.0  # marker: 0 = measured
        else:
            logger.info(
                "LLM server not available (%s), using design-doc estimates", status
            )
            llm_ms = ESTIMATED_LATENCIES["llm_stage1_local_fast"]
            components["llm_generation"] = llm_ms
            components["llm_source_estimated"] = 1.0
    else:
        llm_ms = ESTIMATED_LATENCIES["llm_stage1_local_fast"]
        components["llm_generation"] = llm_ms
        components["llm_source_estimated"] = 1.0

    # 5. TTS latency (estimated in synthetic mode)
    tts_ms = ESTIMATED_LATENCIES["tts_cosyvoice"]
    components["tts_synthesis"] = tts_ms
    components["tts_source_estimated"] = 1.0

    # Zone-to-candidates = IAL dispatch + LLM generation
    zone_to_candidates_ms = ial_ms + llm_ms

    # Total simulated round trip
    total_round_trip_ms = gaze_to_zone_ms + ial_ms + llm_ms + tts_ms

    return PipelineBenchResult(
        gaze_to_zone_ms=gaze_to_zone_ms,
        zone_to_candidates_ms=zone_to_candidates_ms,
        total_round_trip_ms=total_round_trip_ms,
        components=components,
    )

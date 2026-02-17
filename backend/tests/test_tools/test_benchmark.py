"""Tests for the VoiceReach benchmark suite.

All tests run WITHOUT cameras, LLM servers, or ML models.
They validate dataclass construction, CLI parsing, and the TTS
benchmark using the placeholder engine.
"""

from __future__ import annotations

import argparse

import pytest

from voicereach.tools.benchmark.gaze_bench import GazeBenchResult
from voicereach.tools.benchmark.llm_bench import LLMBenchResult
from voicereach.tools.benchmark.tts_bench import TTSBenchResult
from voicereach.tools.benchmark.pipeline_bench import PipelineBenchResult
from voicereach.tools.benchmark.cli import build_parser


class TestGazeBenchResult:
    def test_creation(self):
        result = GazeBenchResult(
            fps=120.0,
            latency_p50_ms=5.0,
            latency_p95_ms=7.5,
            latency_p99_ms=12.0,
            frames_processed=1200,
            frames_dropped=5,
            resolution=(640, 480),
        )
        assert result.fps == 120.0
        assert result.latency_p50_ms == 5.0
        assert result.latency_p95_ms == 7.5
        assert result.latency_p99_ms == 12.0
        assert result.frames_processed == 1200
        assert result.frames_dropped == 5
        assert result.resolution == (640, 480)

    def test_zero_frames(self):
        result = GazeBenchResult(
            fps=0.0,
            latency_p50_ms=0.0,
            latency_p95_ms=0.0,
            latency_p99_ms=0.0,
            frames_processed=0,
            frames_dropped=0,
            resolution=(640, 480),
        )
        assert result.frames_processed == 0
        assert result.fps == 0.0


class TestLLMBenchResult:
    def test_creation(self):
        result = LLMBenchResult(
            model="Qwen/Qwen3-0.6B",
            ttft_ms=45.0,
            tokens_per_second=30.0,
            total_tokens=50,
            total_time_ms=1500.0,
            prompt_tokens=20,
            memory_mb=512.0,
        )
        assert result.model == "Qwen/Qwen3-0.6B"
        assert result.ttft_ms == 45.0
        assert result.tokens_per_second == 30.0
        assert result.total_tokens == 50
        assert result.total_time_ms == 1500.0
        assert result.prompt_tokens == 20
        assert result.memory_mb == 512.0

    def test_creation_without_memory(self):
        result = LLMBenchResult(
            model="Qwen/Qwen3-1.7B",
            ttft_ms=80.0,
            tokens_per_second=20.0,
            total_tokens=30,
            total_time_ms=2000.0,
            prompt_tokens=15,
            memory_mb=None,
        )
        assert result.memory_mb is None


class TestTTSBenchResult:
    def test_creation(self):
        result = TTSBenchResult(
            engine="placeholder",
            first_synthesis_ms=10.0,
            avg_synthesis_ms=5.0,
            p95_synthesis_ms=8.0,
            samples_generated=50,
            sample_rate=24000,
        )
        assert result.engine == "placeholder"
        assert result.first_synthesis_ms == 10.0
        assert result.avg_synthesis_ms == 5.0
        assert result.p95_synthesis_ms == 8.0
        assert result.samples_generated == 50
        assert result.sample_rate == 24000

    def test_cosyvoice_engine_name(self):
        result = TTSBenchResult(
            engine="cosyvoice",
            first_synthesis_ms=50.0,
            avg_synthesis_ms=30.0,
            p95_synthesis_ms=45.0,
            samples_generated=100,
            sample_rate=24000,
        )
        assert result.engine == "cosyvoice"


class TestPipelineBenchResult:
    def test_creation(self):
        result = PipelineBenchResult(
            gaze_to_zone_ms=0.05,
            zone_to_candidates_ms=150.5,
            total_round_trip_ms=350.5,
            components={
                "smoother": 0.02,
                "zone_mapper": 0.03,
                "ial_dispatch": 0.01,
                "llm_generation": 150.0,
                "tts_synthesis": 200.0,
            },
        )
        assert result.gaze_to_zone_ms == 0.05
        assert result.zone_to_candidates_ms == 150.5
        assert result.total_round_trip_ms == 350.5
        assert len(result.components) == 5
        assert result.components["smoother"] == 0.02

    def test_default_components(self):
        result = PipelineBenchResult(
            gaze_to_zone_ms=0.1,
            zone_to_candidates_ms=200.0,
            total_round_trip_ms=400.0,
        )
        assert result.components == {}


class TestCLIParser:
    def test_gaze_defaults(self):
        parser = build_parser()
        args = parser.parse_args(["gaze"])
        assert args.command == "gaze"
        assert args.duration == 10.0
        assert args.synthetic is False

    def test_gaze_with_options(self):
        parser = build_parser()
        args = parser.parse_args(["gaze", "--duration", "5.0", "--synthetic"])
        assert args.duration == 5.0
        assert args.synthetic is True

    def test_llm_defaults(self):
        parser = build_parser()
        args = parser.parse_args(["llm"])
        assert args.command == "llm"
        assert args.model is None
        assert args.runs == 5

    def test_llm_with_options(self):
        parser = build_parser()
        args = parser.parse_args(["llm", "--model", "Qwen/Qwen3-1.7B", "--runs", "3"])
        assert args.model == "Qwen/Qwen3-1.7B"
        assert args.runs == 3

    def test_tts_defaults(self):
        parser = build_parser()
        args = parser.parse_args(["tts"])
        assert args.command == "tts"
        assert args.runs == 10

    def test_tts_with_options(self):
        parser = build_parser()
        args = parser.parse_args(["tts", "--runs", "2"])
        assert args.runs == 2

    def test_pipeline_defaults(self):
        parser = build_parser()
        args = parser.parse_args(["pipeline"])
        assert args.command == "pipeline"
        assert args.synthetic is True

    def test_pipeline_no_synthetic(self):
        parser = build_parser()
        args = parser.parse_args(["pipeline", "--no-synthetic"])
        assert args.synthetic is False

    def test_all_command(self):
        parser = build_parser()
        args = parser.parse_args(["all"])
        assert args.command == "all"

    def test_no_command(self):
        parser = build_parser()
        args = parser.parse_args([])
        assert args.command is None


class TestTTSBenchmarkIntegration:
    """Integration test: runs the actual TTS benchmark with the placeholder engine."""

    @pytest.mark.asyncio
    async def test_run_tts_benchmark_placeholder(self):
        from voicereach.tools.benchmark.tts_bench import run_tts_benchmark

        result = await run_tts_benchmark(num_runs=2)
        assert result.engine == "placeholder"
        assert result.samples_generated > 0
        assert result.first_synthesis_ms > 0.0
        assert result.avg_synthesis_ms > 0.0
        assert result.p95_synthesis_ms > 0.0
        assert result.sample_rate == 24000

    @pytest.mark.asyncio
    async def test_run_tts_benchmark_custom_texts(self):
        from voicereach.tools.benchmark.tts_bench import run_tts_benchmark

        texts = ["テスト", "こんにちは"]
        result = await run_tts_benchmark(texts=texts, num_runs=1)
        assert result.samples_generated == 2
        assert result.engine == "placeholder"


class TestPipelineBenchmarkIntegration:
    """Integration test: runs the pipeline benchmark in synthetic mode."""

    @pytest.mark.asyncio
    async def test_run_pipeline_benchmark_synthetic(self):
        from voicereach.tools.benchmark.pipeline_bench import run_pipeline_benchmark

        result = await run_pipeline_benchmark(use_synthetic=True)
        assert result.gaze_to_zone_ms > 0.0
        assert result.zone_to_candidates_ms > 0.0
        assert result.total_round_trip_ms > 0.0
        assert "smoother" in result.components
        assert "zone_mapper" in result.components
        assert "ial_dispatch" in result.components
        assert "llm_generation" in result.components
        assert "tts_synthesis" in result.components

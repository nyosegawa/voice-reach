"""CLI entry point for the VoiceReach benchmark suite.

Usage:
    voicereach-bench gaze [--duration SECS] [--synthetic]
    voicereach-bench llm  [--model MODEL] [--runs N]
    voicereach-bench tts  [--runs N]
    voicereach-bench pipeline [--synthetic]
    voicereach-bench all
"""

from __future__ import annotations

import argparse
import asyncio
import sys


# ── Formatting helpers ──────────────────────────────────────────────

BOX_WIDTH = 52


def _top() -> str:
    return f"\u2554{'=' * BOX_WIDTH}\u2557"


def _mid() -> str:
    return f"\u2560{'=' * BOX_WIDTH}\u2563"


def _bot() -> str:
    return f"\u255a{'=' * BOX_WIDTH}\u255d"


def _row(text: str) -> str:
    return f"\u2551 {text:<{BOX_WIDTH - 1}}\u2551"


def _title(text: str) -> str:
    return f"\u2551{text:^{BOX_WIDTH}}\u2551"


def _print_header() -> None:
    print(_top())
    print(_title("VoiceReach Benchmark Results"))
    print(_mid())


def _print_footer() -> None:
    print(_bot())


def _print_section(title: str, rows: list[tuple[str, str]]) -> None:
    print(_row(title))
    for label, value in rows:
        print(_row(f"  {label:<26} {value}"))
    print(_mid())


# ── Subcommand runners ──────────────────────────────────────────────

def _run_gaze(args: argparse.Namespace) -> dict | None:
    """Run gaze tracking benchmark."""
    from voicereach.tools.benchmark.gaze_bench import run_gaze_benchmark

    try:
        result = run_gaze_benchmark(
            duration_s=args.duration,
            use_synthetic=args.synthetic,
        )
    except RuntimeError as e:
        print(f"[SKIP] Gaze benchmark: {e}", file=sys.stderr)
        return None

    rows = [
        ("FPS:", f"{result.fps:.1f}"),
        ("P50 latency:", f"{result.latency_p50_ms:.2f} ms"),
        ("P95 latency:", f"{result.latency_p95_ms:.2f} ms"),
        ("P99 latency:", f"{result.latency_p99_ms:.2f} ms"),
        ("Frames processed:", str(result.frames_processed)),
        ("Frames dropped:", str(result.frames_dropped)),
        ("Resolution:", f"{result.resolution[0]}x{result.resolution[1]}"),
    ]
    _print_section("Gaze Tracking", rows)
    return {
        "fps": result.fps,
        "p50_ms": result.latency_p50_ms,
        "p95_ms": result.latency_p95_ms,
        "p99_ms": result.latency_p99_ms,
    }


def _run_llm(args: argparse.Namespace) -> dict | None:
    """Run LLM inference benchmark."""
    from voicereach.tools.benchmark.llm_bench import run_llm_benchmark

    result = asyncio.run(run_llm_benchmark(
        model=args.model,
        num_runs=args.runs,
    ))

    if result is None:
        rows = [("Status:", "Server not reachable")]
        _print_section("LLM Inference", rows)
        return None

    rows = [
        ("Model:", result.model),
        ("TTFT:", f"{result.ttft_ms:.1f} ms"),
        ("Tokens/sec:", f"{result.tokens_per_second:.1f}"),
        ("Total tokens:", str(result.total_tokens)),
        ("Total time:", f"{result.total_time_ms:.1f} ms"),
        ("Prompt tokens:", f"~{result.prompt_tokens}"),
    ]
    if result.memory_mb is not None:
        rows.append(("Process memory:", f"{result.memory_mb:.1f} MB"))
    _print_section("LLM Inference", rows)
    return {
        "model": result.model,
        "ttft_ms": result.ttft_ms,
        "tokens_per_second": result.tokens_per_second,
    }


def _run_tts(args: argparse.Namespace) -> dict | None:
    """Run TTS synthesis benchmark."""
    from voicereach.tools.benchmark.tts_bench import run_tts_benchmark

    result = asyncio.run(run_tts_benchmark(num_runs=args.runs))

    rows = [
        ("Engine:", result.engine),
        ("Cold start:", f"{result.first_synthesis_ms:.2f} ms"),
        ("Avg synthesis:", f"{result.avg_synthesis_ms:.2f} ms"),
        ("P95 synthesis:", f"{result.p95_synthesis_ms:.2f} ms"),
        ("Samples generated:", str(result.samples_generated)),
        ("Sample rate:", f"{result.sample_rate} Hz"),
    ]
    _print_section("TTS Synthesis", rows)
    return {
        "engine": result.engine,
        "cold_start_ms": result.first_synthesis_ms,
        "avg_ms": result.avg_synthesis_ms,
        "p95_ms": result.p95_synthesis_ms,
    }


def _run_pipeline(args: argparse.Namespace) -> dict | None:
    """Run pipeline benchmark."""
    from voicereach.tools.benchmark.pipeline_bench import run_pipeline_benchmark

    result = asyncio.run(run_pipeline_benchmark(
        use_synthetic=args.synthetic,
    ))

    rows = [
        ("Gaze -> Zone:", f"{result.gaze_to_zone_ms:.3f} ms"),
        ("Zone -> Candidates:", f"{result.zone_to_candidates_ms:.2f} ms"),
        ("Total round trip:", f"{result.total_round_trip_ms:.1f} ms"),
    ]
    # Add component breakdown
    for name, value in result.components.items():
        if name.endswith("_estimated"):
            continue
        label = name.replace("_", " ").title() + ":"
        estimated = result.components.get(f"{name}_estimated")
        suffix = " (est)" if estimated else ""
        rows.append((f"  {label}", f"{value:.3f} ms{suffix}"))

    _print_section("Pipeline (end-to-end)", rows)
    return {
        "gaze_to_zone_ms": result.gaze_to_zone_ms,
        "zone_to_candidates_ms": result.zone_to_candidates_ms,
        "total_round_trip_ms": result.total_round_trip_ms,
    }


# ── Main CLI ────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser. Exposed for testing."""
    parser = argparse.ArgumentParser(
        prog="voicereach-bench",
        description="VoiceReach benchmark suite",
    )
    sub = parser.add_subparsers(dest="command")

    # voicereach-bench gaze
    gaze_p = sub.add_parser("gaze", help="Benchmark gaze tracking")
    gaze_p.add_argument(
        "--duration", type=float, default=10.0,
        help="Benchmark duration in seconds (default: 10)",
    )
    gaze_p.add_argument(
        "--synthetic", action="store_true",
        help="Use synthetic face images instead of camera",
    )

    # voicereach-bench llm
    llm_p = sub.add_parser("llm", help="Benchmark LLM inference")
    llm_p.add_argument(
        "--model", type=str, default=None,
        help="Model name (default: settings.local_llm_model_fast)",
    )
    llm_p.add_argument(
        "--runs", type=int, default=5,
        help="Number of benchmark runs (default: 5)",
    )

    # voicereach-bench tts
    tts_p = sub.add_parser("tts", help="Benchmark TTS synthesis")
    tts_p.add_argument(
        "--runs", type=int, default=10,
        help="Number of full cycles (default: 10)",
    )

    # voicereach-bench pipeline
    pipe_p = sub.add_parser("pipeline", help="Benchmark full pipeline")
    pipe_p.add_argument(
        "--synthetic", action="store_true", default=True,
        help="Use synthetic data (default: True)",
    )
    pipe_p.add_argument(
        "--no-synthetic", dest="synthetic", action="store_false",
        help="Attempt to use real LLM server",
    )

    # voicereach-bench all
    sub.add_parser("all", help="Run all benchmarks")

    return parser


def main() -> None:
    """Entry point for the voicereach-bench CLI."""
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    _print_header()

    if args.command == "gaze":
        _run_gaze(args)
    elif args.command == "llm":
        _run_llm(args)
    elif args.command == "tts":
        _run_tts(args)
    elif args.command == "pipeline":
        _run_pipeline(args)
    elif args.command == "all":
        # Run all benchmarks with sensible defaults for "all" mode
        gaze_args = argparse.Namespace(duration=5.0, synthetic=True)
        _run_gaze(gaze_args)

        llm_args = argparse.Namespace(model=None, runs=3)
        _run_llm(llm_args)

        tts_args = argparse.Namespace(runs=5)
        _run_tts(tts_args)

        pipe_args = argparse.Namespace(synthetic=True)
        _run_pipeline(pipe_args)

    _print_footer()


if __name__ == "__main__":
    main()

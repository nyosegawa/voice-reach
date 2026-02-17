"""CLI for VoiceReach recording quality tools.

Usage:
    voicereach-rec analyze <wav_file>
    voicereach-rec session create <patient_id> [--output-dir DIR]
    voicereach-rec session status <patient_id> <session_id> [--output-dir DIR]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from voicereach.tools.recording.quality_checker import analyze_file


def cmd_analyze(args: argparse.Namespace) -> None:
    """Analyze a WAV file."""
    path = Path(args.wav_file)
    if not path.exists():
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)

    result = analyze_file(path)

    status = "PASS" if result.is_acceptable else "FAIL"
    print(f"\n{'='*50}")
    print(f"  Recording Quality Analysis: {status}")
    print(f"{'='*50}")
    print(f"  File:        {path.name}")
    print(f"  Duration:    {result.duration_seconds:.1f}s")
    print(f"  Sample Rate: {result.sample_rate} Hz")
    print(f"  Bit Depth:   {result.bit_depth}-bit")
    print(f"  Channels:    {result.channels}")
    print(f"{'─'*50}")
    print(f"  SNR:         {result.snr_db:.1f} dB")
    print(f"  Peak Level:  {result.peak_level_db:.1f} dB")
    print(f"  RMS Level:   {result.rms_level_db:.1f} dB")
    print(f"  Noise Floor: {result.noise_floor_db:.1f} dB")
    print(f"  Clipping:    {'Yes' if result.has_clipping else 'No'}")
    if result.has_clipping:
        print(f"               ({result.clipping_count} clipped samples)")

    if result.warnings:
        print(f"{'─'*50}")
        print("  Warnings:")
        for w in result.warnings:
            print(f"    - {w}")

    print(f"{'='*50}\n")


def cmd_session_create(args: argparse.Namespace) -> None:
    """Create a recording session."""
    from voicereach.tools.recording.session_manager import SessionManager

    mgr = SessionManager(args.output_dir)
    session = mgr.create_session(args.patient_id)
    print(f"Created session: {session.session_id}")
    print(f"Directory: {Path(args.output_dir) / args.patient_id / session.session_id}")


def cmd_session_status(args: argparse.Namespace) -> None:
    """Show session status."""
    from voicereach.tools.recording.session_manager import SessionManager

    mgr = SessionManager(args.output_dir)
    try:
        session = mgr.load_session(args.patient_id, args.session_id)
    except FileNotFoundError:
        print("Error: Session not found", file=sys.stderr)
        sys.exit(1)

    print(f"\nSession: {session.session_id}")
    print(f"Patient: {session.patient_id}")
    print(f"Created: {session.created_at}")
    print(f"Recordings: {len(session.entries)}")
    print(f"Total Duration: {session.total_duration_seconds:.1f}s")

    acceptable = sum(1 for e in session.entries if e.quality and e.quality.is_acceptable)
    print(f"Quality Pass: {acceptable}/{len(session.entries)}")


def main() -> None:
    """Main entry point for voicereach-rec CLI."""
    parser = argparse.ArgumentParser(
        prog="voicereach-rec",
        description="VoiceReach recording quality tools",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # analyze
    p_analyze = subparsers.add_parser("analyze", help="Analyze a WAV file")
    p_analyze.add_argument("wav_file", help="Path to WAV file")

    # session
    p_session = subparsers.add_parser("session", help="Recording session management")
    session_sub = p_session.add_subparsers(dest="session_command", required=True)

    p_create = session_sub.add_parser("create", help="Create a new session")
    p_create.add_argument("patient_id", help="Patient identifier")
    p_create.add_argument("--output-dir", default="data/recordings", help="Output directory")

    p_status = session_sub.add_parser("status", help="Show session status")
    p_status.add_argument("patient_id", help="Patient identifier")
    p_status.add_argument("session_id", help="Session identifier")
    p_status.add_argument("--output-dir", default="data/recordings", help="Output directory")

    args = parser.parse_args()

    if args.command == "analyze":
        cmd_analyze(args)
    elif args.command == "session":
        if args.session_command == "create":
            cmd_session_create(args)
        elif args.session_command == "status":
            cmd_session_status(args)


if __name__ == "__main__":
    main()

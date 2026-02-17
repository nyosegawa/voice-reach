"""Recording session manager for voice preservation.

Manages recording sessions with metadata tracking, quality monitoring,
and progress persistence.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path

from voicereach.tools.recording.phoneme_coverage import PhonemeCoverageTracker
from voicereach.tools.recording.quality_checker import RecordingQuality, analyze_file


@dataclass
class RecordingEntry:
    """Metadata for a single recording within a session."""
    filename: str
    sentence_id: int | None = None
    sentence_text: str = ""
    emotion: str = "neutral"
    quality: RecordingQuality | None = None
    recorded_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Session:
    """A recording session with multiple WAV files."""
    session_id: str
    patient_id: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    entries: list[RecordingEntry] = field(default_factory=list)
    total_duration_seconds: float = 0.0
    notes: str = ""


class SessionManager:
    """Manages recording sessions on disk."""

    def __init__(self, base_dir: str | Path) -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self._coverage = PhonemeCoverageTracker()

    def create_session(self, patient_id: str, session_id: str | None = None) -> Session:
        """Create a new recording session."""
        if session_id is None:
            session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        session = Session(session_id=session_id, patient_id=patient_id)
        session_dir = self.base_dir / patient_id / session_id
        session_dir.mkdir(parents=True, exist_ok=True)

        self._save_session(session)
        return session

    def add_recording(
        self,
        patient_id: str,
        session_id: str,
        wav_path: str | Path,
        sentence_text: str = "",
        sentence_id: int | None = None,
        emotion: str = "neutral",
    ) -> RecordingEntry:
        """Add a recording to an existing session and analyze quality."""
        session = self.load_session(patient_id, session_id)
        quality = analyze_file(wav_path)

        entry = RecordingEntry(
            filename=Path(wav_path).name,
            sentence_id=sentence_id,
            sentence_text=sentence_text,
            emotion=emotion,
            quality=quality,
        )

        session.entries.append(entry)
        session.total_duration_seconds += quality.duration_seconds

        if sentence_text:
            self._coverage.add_text(sentence_text)

        self._save_session(session)
        return entry

    def load_session(self, patient_id: str, session_id: str) -> Session:
        """Load a session from disk."""
        meta_path = self.base_dir / patient_id / session_id / "session.json"
        if not meta_path.exists():
            raise FileNotFoundError(f"Session not found: {meta_path}")

        with open(meta_path) as f:
            data = json.load(f)

        entries = []
        for e in data.get("entries", []):
            q_data = e.pop("quality", None)
            quality = RecordingQuality(**q_data) if q_data else None
            entries.append(RecordingEntry(**e, quality=quality))

        return Session(
            session_id=data["session_id"],
            patient_id=data["patient_id"],
            created_at=data.get("created_at", ""),
            entries=entries,
            total_duration_seconds=data.get("total_duration_seconds", 0.0),
            notes=data.get("notes", ""),
        )

    def get_coverage(self):
        """Get current phoneme coverage report."""
        return self._coverage.report()

    def _save_session(self, session: Session) -> None:
        """Save session metadata to disk."""
        session_dir = self.base_dir / session.patient_id / session.session_id
        session_dir.mkdir(parents=True, exist_ok=True)

        meta_path = session_dir / "session.json"
        data = asdict(session)
        with open(meta_path, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

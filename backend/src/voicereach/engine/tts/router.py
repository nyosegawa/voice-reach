"""TTS routing: cache check -> streaming -> batch synthesis."""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path

from voicereach.config import settings

logger = logging.getLogger(__name__)


class TTSRouter:
    """Routes TTS requests through cache or synthesis engine."""

    def __init__(self, cache_dir: Path | None = None) -> None:
        self._cache_dir = cache_dir or settings.cache_dir / "tts"
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._engine = None

    def set_engine(self, engine) -> None:
        """Set the TTS synthesis engine."""
        self._engine = engine

    async def synthesize(
        self,
        text: str,
        speaker_id: str = "default",
        emotion: dict | None = None,
    ) -> Path | None:
        """Synthesize text to speech, using cache if available.

        Returns path to the audio file, or None if synthesis failed.
        """
        cache_key = self._cache_key(text, speaker_id)
        cached = self._check_cache(cache_key)
        if cached:
            logger.debug("TTS cache hit: %s", text[:20])
            return cached

        if self._engine is None:
            logger.warning("No TTS engine configured")
            return None

        try:
            audio_path = await self._engine.synthesize(text, speaker_id, emotion)
            if audio_path:
                self._save_cache(cache_key, audio_path)
            return audio_path
        except Exception:
            logger.exception("TTS synthesis failed")
            return None

    def _cache_key(self, text: str, speaker_id: str) -> str:
        """Generate a cache key from text and speaker."""
        raw = f"{speaker_id}:{text}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def _check_cache(self, key: str) -> Path | None:
        """Check if audio is in cache."""
        path = self._cache_dir / f"{key}.wav"
        return path if path.exists() else None

    def _save_cache(self, key: str, source_path: Path) -> None:
        """Copy audio to cache."""
        import shutil
        dest = self._cache_dir / f"{key}.wav"
        shutil.copy2(source_path, dest)

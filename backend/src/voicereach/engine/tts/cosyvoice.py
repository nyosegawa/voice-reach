"""CosyVoice TTS wrapper.

For MVP: uses default speaker with basic synthesis.
CosyVoice 2/3 integration will be added when the model is available locally.
This module provides a consistent interface that works with or without
the actual CosyVoice model installed.
"""

from __future__ import annotations

import logging
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf

from voicereach.config import settings

logger = logging.getLogger(__name__)


class CosyVoiceEngine:
    """CosyVoice TTS engine wrapper.

    Falls back to a placeholder tone if CosyVoice is not installed.
    """

    def __init__(self) -> None:
        self._model = None
        self._available = False

    async def initialize(self) -> None:
        """Load the CosyVoice model."""
        try:
            # CosyVoice import will be available after model setup
            # For now, log and mark as unavailable
            logger.info("CosyVoice model not yet configured, using placeholder")
            self._available = False
        except Exception:
            logger.warning("CosyVoice not available, using placeholder TTS")
            self._available = False

    async def synthesize(
        self,
        text: str,
        speaker_id: str = "default",
        emotion: dict | None = None,
    ) -> Path | None:
        """Synthesize text to audio file.

        Returns path to generated WAV file.
        """
        if self._available and self._model:
            return await self._synthesize_cosyvoice(text, speaker_id, emotion)
        return self._synthesize_placeholder(text)

    async def _synthesize_cosyvoice(
        self, text: str, speaker_id: str, emotion: dict | None
    ) -> Path | None:
        """Synthesize using actual CosyVoice model."""
        # TODO: Implement when CosyVoice is set up
        return None

    def _synthesize_placeholder(self, text: str) -> Path:
        """Generate a placeholder tone for development.

        Generates a short sine wave so the pipeline can be tested
        end-to-end without the actual TTS model.
        """
        sr = 24000
        duration = min(0.5 + len(text) * 0.1, 5.0)
        t = np.linspace(0, duration, int(sr * duration), endpoint=False)
        audio = 0.3 * np.sin(2 * np.pi * 440 * t).astype(np.float32)

        # Simple envelope
        fade_len = int(sr * 0.05)
        audio[:fade_len] *= np.linspace(0, 1, fade_len)
        audio[-fade_len:] *= np.linspace(1, 0, fade_len)

        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        sf.write(tmp.name, audio, sr)
        return Path(tmp.name)

    @property
    def is_available(self) -> bool:
        return self._available

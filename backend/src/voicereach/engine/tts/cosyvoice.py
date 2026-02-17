"""CosyVoice TTS wrapper.

CosyVoice 2/3 integration for Japanese voice synthesis.
Supports multiple synthesis modes:
  1. Standard TTS (inference_sft) - basic text-to-speech
  2. Zero-shot voice cloning (inference_zero_shot) - preserves patient's voice
  3. Cross-lingual / Instruct modes (future)

Falls back to a placeholder sine-wave tone when the CosyVoice model
is not installed or the model directory is missing, so the full pipeline
can still be exercised during development.

References:
  - docs/08_VOICE_PRESERVATION.md  (voice cloning rationale)
  - docs/04_AI_CANDIDATE_GENERATION.md  (TTS in the generation pipeline)
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

    Falls back to a placeholder tone if CosyVoice is not installed or
    the model directory does not exist.
    """

    def __init__(self, model_dir: str | None = None) -> None:
        self._model_dir = model_dir or str(settings.tts_model_dir)
        self._model = None
        self._available = False

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def initialize(self) -> None:
        """Try to load CosyVoice model.  Falls back to placeholder if unavailable."""
        try:
            from cosyvoice.cli.cosyvoice import CosyVoice  # type: ignore[import-untyped]

            model_path = Path(self._model_dir)
            if model_path.exists():
                self._model = CosyVoice(str(model_path))
                self._available = True
                logger.info("CosyVoice loaded from %s", model_path)
            else:
                logger.info(
                    "CosyVoice model dir not found at %s, using placeholder",
                    model_path,
                )
        except ImportError:
            logger.info("CosyVoice package not installed, using placeholder TTS")
        except Exception:
            logger.warning(
                "CosyVoice initialization failed, using placeholder", exc_info=True
            )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def synthesize(
        self,
        text: str,
        speaker_id: str = "default",
        emotion: dict | None = None,
    ) -> Path | None:
        """Synthesize *text* to a WAV file and return its path."""
        if self._available and self._model:
            return await self._synthesize_cosyvoice(text, speaker_id, emotion)
        return self._synthesize_placeholder(text)

    async def synthesize_with_reference(
        self,
        text: str,
        reference_audio: Path,
        reference_text: str,
    ) -> Path | None:
        """Zero-shot voice cloning with reference audio.

        This is the key feature for Voice Preservation
        (see docs/08_VOICE_PRESERVATION.md).  The patient's pre-recorded
        voice is used as the reference so that synthesised speech retains
        their vocal identity.
        """
        if not self._available or not self._model:
            logger.warning("CosyVoice not available for zero-shot synthesis")
            return self._synthesize_placeholder(text)

        try:
            import torch  # type: ignore[import-untyped]
            import torchaudio  # type: ignore[import-untyped]

            output = self._model.inference_zero_shot(
                text, reference_text, str(reference_audio)
            )

            audio_chunks: list = []
            for chunk in output:
                audio_chunks.append(chunk["tts_speech"])

            if not audio_chunks:
                return self._synthesize_placeholder(text)

            audio = torch.cat(audio_chunks, dim=1)
            tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            torchaudio.save(tmp.name, audio, sample_rate=22050)
            return Path(tmp.name)
        except Exception:
            logger.exception("Zero-shot synthesis failed")
            return self._synthesize_placeholder(text)

    # ------------------------------------------------------------------
    # Internal: real model path
    # ------------------------------------------------------------------

    async def _synthesize_cosyvoice(
        self,
        text: str,
        speaker_id: str,
        emotion: dict | None,
    ) -> Path | None:
        """Synthesize using the actual CosyVoice model.

        CosyVoice supports several modes:
          1. Zero-shot  -- with reference audio  (see synthesize_with_reference)
          2. Cross-lingual
          3. Instruct mode
          4. Standard TTS (inference_sft)

        For MVP we use standard TTS mode.
        """
        import torch  # type: ignore[import-untyped]
        import torchaudio  # type: ignore[import-untyped]

        try:
            output = self._model.inference_sft(text, speaker_id)

            # CosyVoice returns a generator of dicts with 'tts_speech' tensor
            audio_chunks: list = []
            for chunk in output:
                audio_chunks.append(chunk["tts_speech"])

            if not audio_chunks:
                return self._synthesize_placeholder(text)

            audio = torch.cat(audio_chunks, dim=1)

            tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            torchaudio.save(tmp.name, audio, sample_rate=22050)
            return Path(tmp.name)
        except Exception:
            logger.exception(
                "CosyVoice synthesis failed, falling back to placeholder"
            )
            return self._synthesize_placeholder(text)

    # ------------------------------------------------------------------
    # Internal: development placeholder
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def is_available(self) -> bool:
        return self._available

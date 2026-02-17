"""Tests for TTS engine components."""

import tempfile
from pathlib import Path

import numpy as np
import pytest
import soundfile as sf

from voicereach.engine.tts.audio_postprocess import normalize_loudness
from voicereach.engine.tts.cosyvoice import CosyVoiceEngine
from voicereach.engine.tts.router import TTSRouter


class TestCosyVoiceEngine:
    @pytest.mark.asyncio
    async def test_placeholder_synthesis(self):
        engine = CosyVoiceEngine()
        await engine.initialize()
        result = await engine.synthesize("テスト")
        assert result is not None
        assert result.exists()
        assert result.suffix == ".wav"
        # Verify it's a valid audio file
        data, sr = sf.read(str(result))
        assert sr == 24000
        assert len(data) > 0

    @pytest.mark.asyncio
    async def test_placeholder_duration_scales_with_text(self):
        engine = CosyVoiceEngine()
        await engine.initialize()
        short = await engine.synthesize("あ")
        long = await engine.synthesize("これは長いテスト文です")
        short_data, _ = sf.read(str(short))
        long_data, _ = sf.read(str(long))
        assert len(long_data) > len(short_data)

    def test_not_available_initially(self):
        engine = CosyVoiceEngine()
        assert not engine.is_available


class TestTTSRouter:
    @pytest.mark.asyncio
    async def test_cache_miss_then_hit(self, tmp_path: Path):
        engine = CosyVoiceEngine()
        await engine.initialize()

        router = TTSRouter(cache_dir=tmp_path / "cache")
        router.set_engine(engine)

        # First call: cache miss, synthesize
        result1 = await router.synthesize("テスト")
        assert result1 is not None

        # Second call: should use cache
        result2 = await router.synthesize("テスト")
        assert result2 is not None
        assert result2.exists()

    @pytest.mark.asyncio
    async def test_no_engine(self, tmp_path: Path):
        router = TTSRouter(cache_dir=tmp_path / "cache")
        result = await router.synthesize("テスト")
        assert result is None


class TestAudioPostprocess:
    def test_normalize_loudness(self, tmp_path: Path):
        sr = 24000
        t = np.linspace(0, 1, sr, endpoint=False)
        # Quiet audio
        audio = 0.01 * np.sin(2 * np.pi * 440 * t).astype(np.float32)
        path = tmp_path / "quiet.wav"
        sf.write(str(path), audio, sr)

        result = normalize_loudness(path, target_lufs=-16.0)
        data, _ = sf.read(str(result))
        # Should be louder now
        assert np.sqrt(np.mean(data ** 2)) > np.sqrt(np.mean(audio ** 2))

    def test_prevent_clipping(self, tmp_path: Path):
        sr = 24000
        t = np.linspace(0, 1, sr, endpoint=False)
        audio = 0.9 * np.sin(2 * np.pi * 440 * t).astype(np.float32)
        path = tmp_path / "loud.wav"
        sf.write(str(path), audio, sr)

        result = normalize_loudness(path, target_lufs=-6.0)
        data, _ = sf.read(str(result))
        assert np.max(np.abs(data)) <= 0.999

"""Tests for recording quality tools."""

import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf

from voicereach.tools.recording.quality_checker import analyze_file
from voicereach.tools.recording.phoneme_coverage import PhonemeCoverageTracker


def _make_wav(path: Path, samples: np.ndarray, sr: int = 48000) -> None:
    """Helper to write a WAV file."""
    sf.write(str(path), samples, sr, subtype="PCM_24")


class TestQualityChecker:
    def test_clean_recording(self, tmp_path: Path):
        """A clean recording with speech-like signal/silence should pass."""
        sr = 48000
        duration = 2.0
        n_samples = int(sr * duration)
        rng = np.random.default_rng(42)

        # Create speech-like pattern: alternating signal and silence
        # First half: sine wave at -12 dB (signal)
        # Second half: near silence (noise only)
        t_signal = np.linspace(0, duration / 2, n_samples // 2, endpoint=False)
        signal_part = 0.25 * np.sin(2 * np.pi * 440 * t_signal).astype(np.float32)
        silence_part = np.zeros(n_samples // 2, dtype=np.float32)

        audio = np.concatenate([signal_part, silence_part])
        # Add very low noise throughout
        noise = rng.normal(0, 0.0005, len(audio)).astype(np.float32)
        audio = audio + noise

        wav_path = tmp_path / "clean.wav"
        _make_wav(wav_path, audio, sr)

        result = analyze_file(wav_path)
        assert result.snr_db > 30
        assert not result.has_clipping
        assert result.sample_rate == 48000
        assert result.bit_depth == 24
        assert result.is_acceptable

    def test_clipped_recording(self, tmp_path: Path):
        """A clipped recording should fail."""
        sr = 48000
        t = np.linspace(0, 1, sr, endpoint=False)
        audio = np.sin(2 * np.pi * 440 * t).astype(np.float32)  # Full amplitude -> clips

        wav_path = tmp_path / "clipped.wav"
        _make_wav(wav_path, audio, sr)

        result = analyze_file(wav_path)
        assert result.has_clipping
        assert result.clipping_count > 0
        assert not result.is_acceptable

    def test_noisy_recording(self, tmp_path: Path):
        """A noisy recording should have low SNR."""
        sr = 48000
        duration = 2.0
        t = np.linspace(0, duration, int(sr * duration), endpoint=False)
        signal = 0.1 * np.sin(2 * np.pi * 440 * t).astype(np.float32)
        noise = np.random.default_rng(42).normal(0, 0.05, len(t)).astype(np.float32)
        audio = signal + noise

        wav_path = tmp_path / "noisy.wav"
        _make_wav(wav_path, audio, sr)

        result = analyze_file(wav_path)
        assert result.snr_db < 35


class TestPhonemeCoverage:
    def test_basic_coverage(self):
        tracker = PhonemeCoverageTracker()
        tracker.add_text("あいうえお")
        report = tracker.report()
        assert report.covered_morae >= 5

    def test_katakana_to_hiragana(self):
        tracker = PhonemeCoverageTracker()
        tracker.add_text("アイウエオ")
        report = tracker.report()
        assert report.covered_morae >= 5

    def test_yoon_coverage(self):
        tracker = PhonemeCoverageTracker()
        tracker.add_text("きゃりーぱみゅぱみゅ")
        assert "きゃ" in tracker.covered

    def test_particle_coverage(self):
        tracker = PhonemeCoverageTracker()
        tracker.add_text("そうだよ。")
        tracker.add_text("いいね。")
        assert "よ" in tracker.covered_particles
        assert "ね" in tracker.covered_particles

    def test_full_coverage_report(self):
        tracker = PhonemeCoverageTracker()
        text = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん"
        tracker.add_text(text)
        report = tracker.report()
        assert report.basic_coverage == 100.0

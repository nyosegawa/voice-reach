"""Audio recording quality checker for voice preservation.

Analyzes WAV recordings to ensure they meet the quality requirements
for voice synthesis model training (CosyVoice 2/3, GPT-SoVITS v4).

Quality targets (from docs/08_VOICE_PRESERVATION.md):
- SNR >= 30 dB (minimum), >= 35 dB (recommended)
- Peak level < -3 dB
- RMS level: -20 to -16 dB
- No clipping (samples >= 0.99)
- Sample rate: 44.1kHz+ (48kHz recommended)
- Bit depth: 16-bit+ (24-bit recommended)
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import soundfile as sf


@dataclass
class RecordingQuality:
    """Results of audio quality analysis."""
    snr_db: float
    peak_level_db: float
    rms_level_db: float
    noise_floor_db: float
    has_clipping: bool
    clipping_count: int
    sample_rate: int
    channels: int
    bit_depth: int
    duration_seconds: float
    is_acceptable: bool
    warnings: list[str]


def _compute_snr(samples: np.ndarray, sr: int, frame_ms: int = 30) -> float:
    """Compute SNR using energy-based VAD.

    Segments audio into frames. The noise floor is estimated from the
    quietest 20% of frames (likely silence/background). Signal frames
    are those with energy significantly above this noise floor.
    """
    frame_size = int(sr * frame_ms / 1000)
    num_frames = len(samples) // frame_size
    if num_frames < 2:
        return 0.0

    frames = samples[: num_frames * frame_size].reshape(num_frames, frame_size)
    energies = np.mean(frames ** 2, axis=1)

    # Use the 20th percentile as noise floor estimate, then set threshold
    # well above it to separate signal from noise.
    sorted_energies = np.sort(energies)
    noise_floor = np.mean(sorted_energies[: max(1, num_frames // 5)])
    threshold = noise_floor * 10  # ~10 dB above noise floor

    signal_mask = energies > threshold
    noise_mask = energies <= noise_floor * 2  # Frames near noise floor

    if not np.any(signal_mask) or not np.any(noise_mask):
        return 0.0

    rms_signal = np.sqrt(np.mean(energies[signal_mask]))
    rms_noise = np.sqrt(np.mean(energies[noise_mask]))

    if rms_noise < 1e-10:
        return 60.0  # Very clean recording

    return 20 * np.log10(rms_signal / rms_noise)


def _detect_clipping(samples: np.ndarray, threshold: float = 0.99) -> tuple[bool, int]:
    """Detect clipped samples."""
    clipped = np.sum(np.abs(samples) >= threshold)
    return bool(clipped > 0), int(clipped)


def _db(value: float) -> float:
    """Convert linear amplitude to dB."""
    if value < 1e-10:
        return -100.0
    return 20 * np.log10(value)


def _estimate_noise_floor(samples: np.ndarray, sr: int, frame_ms: int = 30) -> float:
    """Estimate noise floor from the quietest 10% of frames."""
    frame_size = int(sr * frame_ms / 1000)
    num_frames = len(samples) // frame_size
    if num_frames < 10:
        return -60.0

    frames = samples[: num_frames * frame_size].reshape(num_frames, frame_size)
    energies = np.mean(frames ** 2, axis=1)

    sorted_energies = np.sort(energies)
    bottom_10 = sorted_energies[: max(1, num_frames // 10)]
    noise_rms = np.sqrt(np.mean(bottom_10))

    return _db(noise_rms)


def _get_bit_depth(info: sf.SoundFile) -> int:
    """Get bit depth from soundfile info."""
    subtype = info.subtype
    if "24" in subtype:
        return 24
    if "32" in subtype:
        return 32
    if "FLOAT" in subtype:
        return 32
    return 16


def analyze_file(wav_path: str | Path) -> RecordingQuality:
    """Analyze a WAV file for recording quality.

    Args:
        wav_path: Path to the WAV file.

    Returns:
        RecordingQuality with all metrics and warnings.
    """
    wav_path = Path(wav_path)
    warnings: list[str] = []

    with sf.SoundFile(str(wav_path)) as f:
        sample_rate = f.samplerate
        channels = f.channels
        bit_depth = _get_bit_depth(f)
        samples = f.read(dtype="float32")

    # Convert to mono if needed
    if samples.ndim > 1:
        samples = np.mean(samples, axis=1)

    duration = len(samples) / sample_rate

    # Metrics
    peak = float(np.max(np.abs(samples)))
    rms = float(np.sqrt(np.mean(samples ** 2)))
    snr = _compute_snr(samples, sample_rate)
    has_clipping, clipping_count = _detect_clipping(samples)
    noise_floor = _estimate_noise_floor(samples, sample_rate)

    peak_db = _db(peak)
    rms_db = _db(rms)

    # Warnings
    if snr < 30:
        warnings.append(f"SNR {snr:.1f} dB < 30 dB (minimum requirement)")
    elif snr < 35:
        warnings.append(f"SNR {snr:.1f} dB < 35 dB (recommended)")

    if has_clipping:
        warnings.append(f"Clipping detected: {clipping_count} samples")

    if peak_db > -3:
        warnings.append(f"Peak level {peak_db:.1f} dB > -3 dB (too loud)")

    if rms_db < -23:
        warnings.append(f"RMS level {rms_db:.1f} dB < -23 dB (too quiet)")
    elif rms_db > -16:
        warnings.append(f"RMS level {rms_db:.1f} dB > -16 dB (too loud)")

    if sample_rate < 44100:
        warnings.append(f"Sample rate {sample_rate} Hz < 44100 Hz")

    if bit_depth < 16:
        warnings.append(f"Bit depth {bit_depth} < 16-bit")

    if duration < 1.0:
        warnings.append(f"Duration {duration:.1f}s too short")

    is_acceptable = snr >= 30 and not has_clipping and peak_db < -3

    return RecordingQuality(
        snr_db=round(snr, 2),
        peak_level_db=round(peak_db, 2),
        rms_level_db=round(rms_db, 2),
        noise_floor_db=round(noise_floor, 2),
        has_clipping=has_clipping,
        clipping_count=clipping_count,
        sample_rate=sample_rate,
        channels=channels,
        bit_depth=bit_depth,
        duration_seconds=round(duration, 2),
        is_acceptable=is_acceptable,
        warnings=warnings,
    )

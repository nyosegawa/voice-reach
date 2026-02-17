"""Audio post-processing: loudness normalization.

Implements ITU-R BS.1770 inspired loudness normalization
for consistent playback volume.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import soundfile as sf


def normalize_loudness(
    audio_path: Path,
    target_lufs: float = -16.0,
    output_path: Path | None = None,
) -> Path:
    """Normalize audio file loudness.

    Args:
        audio_path: Input audio file.
        target_lufs: Target loudness in LUFS (default -16).
        output_path: Output path (overwrites input if None).

    Returns:
        Path to normalized audio file.
    """
    samples, sr = sf.read(str(audio_path), dtype="float32")

    if samples.ndim > 1:
        samples = np.mean(samples, axis=1)

    # Compute current RMS (simplified LUFS approximation)
    rms = np.sqrt(np.mean(samples ** 2))
    if rms < 1e-10:
        return audio_path

    current_db = 20 * np.log10(rms)
    target_db = target_lufs + 10  # LUFS to approximate RMS dB
    gain_db = target_db - current_db
    gain = 10 ** (gain_db / 20)

    normalized = samples * gain

    # Prevent clipping
    peak = np.max(np.abs(normalized))
    if peak > 0.99:
        normalized *= 0.99 / peak

    out = output_path or audio_path
    sf.write(str(out), normalized, sr)
    return out

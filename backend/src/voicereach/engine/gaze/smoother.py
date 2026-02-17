"""Adaptive Kalman filter for gaze smoothing.

Adapts gain based on saccade detection: high velocity relaxes the filter,
low velocity tightens it for stability.
"""

from __future__ import annotations

import numpy as np


class GazeSmoother:
    """1D Kalman filter with adaptive process noise for gaze signals."""

    def __init__(
        self,
        process_noise: float = 0.1,
        measurement_noise: float = 1.0,
        saccade_threshold: float = 15.0,
        saccade_noise_multiplier: float = 10.0,
    ) -> None:
        self._q_base = process_noise
        self._r = measurement_noise
        self._saccade_threshold = saccade_threshold
        self._saccade_multiplier = saccade_noise_multiplier

        # State
        self._x = 0.0  # estimated value
        self._p = 1.0  # estimation error covariance
        self._prev_measurement = 0.0
        self._initialized = False

    def update(self, measurement: float) -> float:
        """Update filter with new measurement and return smoothed value."""
        if not self._initialized:
            self._x = measurement
            self._prev_measurement = measurement
            self._initialized = True
            return measurement

        # Detect saccade (rapid eye movement)
        velocity = abs(measurement - self._prev_measurement)
        is_saccade = velocity > self._saccade_threshold

        # Adaptive process noise
        q = self._q_base * self._saccade_multiplier if is_saccade else self._q_base

        # Predict
        x_pred = self._x
        p_pred = self._p + q

        # Update
        k = p_pred / (p_pred + self._r)  # Kalman gain
        self._x = x_pred + k * (measurement - x_pred)
        self._p = (1 - k) * p_pred

        self._prev_measurement = measurement
        return self._x

    def reset(self) -> None:
        """Reset filter state."""
        self._initialized = False
        self._x = 0.0
        self._p = 1.0


class DualAxisSmoother:
    """Smooths 2D gaze (pitch, yaw) with independent Kalman filters."""

    def __init__(self, **kwargs) -> None:
        self._pitch_filter = GazeSmoother(**kwargs)
        self._yaw_filter = GazeSmoother(**kwargs)

    def update(self, pitch: float, yaw: float) -> tuple[float, float]:
        """Update with new pitch/yaw and return smoothed values."""
        return (
            self._pitch_filter.update(pitch),
            self._yaw_filter.update(yaw),
        )

    def reset(self) -> None:
        self._pitch_filter.reset()
        self._yaw_filter.reset()

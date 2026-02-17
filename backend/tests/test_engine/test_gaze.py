"""Tests for gaze engine components."""

import numpy as np
import pytest

from voicereach.engine.gaze.calibration import GazeCalibrator
from voicereach.engine.gaze.smoother import DualAxisSmoother, GazeSmoother
from voicereach.engine.gaze.zone_mapper import ZoneMapper


class TestGazeSmoother:
    def test_first_measurement_passes_through(self):
        s = GazeSmoother()
        assert s.update(5.0) == 5.0

    def test_smoothing_reduces_noise(self):
        s = GazeSmoother(process_noise=0.01, measurement_noise=1.0)
        s.update(0.0)
        values = [s.update(0.0 + np.random.normal(0, 0.5)) for _ in range(50)]
        # Smoothed values should have less variance than raw
        assert np.std(values) < 0.5

    def test_saccade_passes_through(self):
        s = GazeSmoother(saccade_threshold=5.0)
        s.update(0.0)
        # Large jump should pass through quickly
        result = s.update(20.0)
        assert result > 10.0  # Should be close to 20

    def test_dual_axis(self):
        d = DualAxisSmoother()
        p, y = d.update(5.0, 10.0)
        assert p == 5.0
        assert y == 10.0


class TestZoneMapper:
    def test_4_zones_center_top(self):
        zm = ZoneMapper(num_zones=4)
        result = zm.map(0.5, 0.1)
        assert result.zone_id == 0  # top

    def test_4_zones_right(self):
        zm = ZoneMapper(num_zones=4)
        result = zm.map(0.9, 0.5)
        assert result.zone_id == 1  # right

    def test_4_zones_bottom(self):
        zm = ZoneMapper(num_zones=4)
        result = zm.map(0.5, 0.9)
        assert result.zone_id == 2  # bottom

    def test_4_zones_left(self):
        zm = ZoneMapper(num_zones=4)
        result = zm.map(0.1, 0.5)
        assert result.zone_id == 3  # left

    def test_hysteresis_prevents_chattering(self):
        zm = ZoneMapper(num_zones=4, hysteresis_margin=0.05)
        zm.map(0.5, 0.1)  # Enter top zone
        # Slightly move towards boundary but within hysteresis
        result = zm.map(0.5, 0.33)
        assert result.zone_id == 0  # Should stay in top due to hysteresis

    def test_9_zones(self):
        zm = ZoneMapper(num_zones=9)
        result = zm.map(0.5, 0.5)
        assert result.zone_id == 4  # center of 3x3 grid

    def test_confidence(self):
        zm = ZoneMapper(num_zones=4)
        result = zm.map(0.5, 0.2)  # Near center of top zone
        assert result.confidence > 0.5

    def test_change_layout(self):
        zm = ZoneMapper(num_zones=4)
        zm.set_num_zones(9)
        result = zm.map(0.5, 0.5)
        assert result.zone_id == 4


class TestCalibration:
    def test_calibrate_with_5_points(self):
        cal = GazeCalibrator()
        # Perfect correspondence (identity-like)
        gaze_pts = [(0, 0), (1, 0), (0.5, 0.5), (0, 1), (1, 1)]
        screen_pts = [(0.1, 0.1), (0.9, 0.1), (0.5, 0.5), (0.1, 0.9), (0.9, 0.9)]
        result = cal.calibrate(gaze_pts, screen_pts)
        assert result.success
        assert result.points_used == 5

    def test_not_calibrated_initially(self):
        cal = GazeCalibrator()
        assert not cal.is_calibrated

    def test_apply_without_calibration(self):
        cal = GazeCalibrator()
        result = cal.apply([(0.5, 0.5)])
        assert result.shape == (1, 2)

    def test_too_few_points(self):
        cal = GazeCalibrator()
        result = cal.calibrate([(0, 0), (1, 1)], [(0, 0), (1, 1)])
        assert not result.success

    def test_reset(self):
        cal = GazeCalibrator()
        cal.calibrate(
            [(0, 0), (1, 0), (0.5, 0.5)],
            [(0.1, 0.1), (0.9, 0.1), (0.5, 0.5)],
        )
        assert cal.is_calibrated
        cal.reset()
        assert not cal.is_calibrated

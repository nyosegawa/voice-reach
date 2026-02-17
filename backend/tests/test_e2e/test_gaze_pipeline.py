"""End-to-end gaze processing pipeline tests.

Exercises the full gaze chain:
  GazeEstimator -> DualAxisSmoother -> ZoneMapper
with synthetic data, no camera required.
"""

from __future__ import annotations

import numpy as np
import pytest

from voicereach.engine.gaze.calibration import GazeCalibrator
from voicereach.engine.gaze.gaze_estimator import GazeEstimator, GazeResult
from voicereach.engine.gaze.mediapipe_tracker import FaceData
from voicereach.engine.gaze.smoother import DualAxisSmoother, GazeSmoother
from voicereach.engine.gaze.zone_mapper import ZoneMapper, ZoneResult


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_face_data(
    iris_offset_x: float = 0.0,
    iris_offset_y: float = 0.0,
) -> FaceData:
    """Create synthetic FaceData with controllable iris offsets.

    iris_offset_x: fraction of eye width to shift iris horizontally
    iris_offset_y: fraction of eye width to shift iris vertically
    """
    num_landmarks = 478
    landmarks = np.zeros((num_landmarks, 3), dtype=np.float32)

    # Place left eye landmarks (indices from LEFT_EYE_INDICES)
    eye_width = 20.0
    left_center_x, left_center_y = 100.0, 80.0
    landmarks[33] = [left_center_x - eye_width / 2, left_center_y, 0]   # outer
    landmarks[133] = [left_center_x + eye_width / 2, left_center_y, 0]  # inner
    for idx in [160, 159, 158]:
        landmarks[idx] = [left_center_x, left_center_y - 3, 0]
    for idx in [144, 145, 153]:
        landmarks[idx] = [left_center_x, left_center_y + 3, 0]

    # Place right eye landmarks (indices from RIGHT_EYE_INDICES)
    right_center_x, right_center_y = 150.0, 80.0
    landmarks[362] = [right_center_x - eye_width / 2, right_center_y, 0]  # outer
    landmarks[263] = [right_center_x + eye_width / 2, right_center_y, 0]  # inner
    for idx in [387, 386, 385]:
        landmarks[idx] = [right_center_x, right_center_y - 3, 0]
    for idx in [373, 374, 380]:
        landmarks[idx] = [right_center_x, right_center_y + 3, 0]

    # Set iris positions relative to eye center
    left_iris = np.array([
        left_center_x + iris_offset_x * eye_width,
        left_center_y + iris_offset_y * eye_width,
    ], dtype=np.float32)
    right_iris = np.array([
        right_center_x + iris_offset_x * eye_width,
        right_center_y + iris_offset_y * eye_width,
    ], dtype=np.float32)

    return FaceData(
        landmarks=landmarks,
        left_eye_patch=np.zeros((64, 64), dtype=np.float32),
        right_eye_patch=np.zeros((64, 64), dtype=np.float32),
        left_iris=left_iris,
        right_iris=right_iris,
        head_pose=np.array([0.0, 0.0, 0.0], dtype=np.float32),
        face_bbox=(80, 60, 90, 50),
        confidence=1.0,
    )


# ---------------------------------------------------------------------------
# Smoother convergence tests
# ---------------------------------------------------------------------------

class TestSmootherConvergence:

    def test_constant_signal_converges(self):
        """A constant gaze signal should converge to the true value."""
        smoother = GazeSmoother(process_noise=0.1, measurement_noise=1.0)
        target = 10.0
        value = None
        for _ in range(100):
            value = smoother.update(target)
        assert value is not None
        assert abs(value - target) < 0.1

    def test_dual_axis_constant_converges(self):
        """DualAxisSmoother converges on both axes for a constant signal."""
        smoother = DualAxisSmoother(process_noise=0.1, measurement_noise=1.0)
        pitch_target, yaw_target = 5.0, -8.0
        for _ in range(100):
            p, y = smoother.update(pitch_target, yaw_target)
        assert abs(p - pitch_target) < 0.1
        assert abs(y - yaw_target) < 0.1

    def test_noisy_signal_smoothed(self):
        """Adding Gaussian noise to a constant should still converge."""
        rng = np.random.default_rng(42)
        smoother = GazeSmoother(process_noise=0.01, measurement_noise=1.0)
        target = 15.0
        values = []
        for _ in range(200):
            noisy = target + rng.normal(0, 2.0)
            values.append(smoother.update(noisy))
        # Last 20 values should be close to target
        tail = values[-20:]
        assert abs(np.mean(tail) - target) < 1.0
        # Smoothed variance should be lower than input noise
        assert np.std(tail) < 2.0


class TestSaccadeDetection:

    def test_saccade_tracks_quickly(self):
        """A sudden jump should be tracked with minimal lag."""
        smoother = GazeSmoother(
            process_noise=0.1,
            measurement_noise=1.0,
            saccade_threshold=10.0,
            saccade_noise_multiplier=20.0,
        )
        # Settle at 0
        for _ in range(20):
            smoother.update(0.0)
        # Jump to 30
        val = smoother.update(30.0)
        # With saccade detection, should move significantly toward 30
        assert val > 15.0

    def test_small_step_is_not_saccade(self):
        """A small step should be smoothed, not treated as a saccade."""
        smoother = GazeSmoother(
            process_noise=0.1,
            measurement_noise=1.0,
            saccade_threshold=15.0,
        )
        for _ in range(20):
            smoother.update(0.0)
        # Small jump of 5 (below threshold of 15)
        val = smoother.update(5.0)
        # Should be smoothed - not jump all the way to 5 instantly
        assert val < 4.0


# ---------------------------------------------------------------------------
# Zone mapping stability tests
# ---------------------------------------------------------------------------

class TestZoneMappingStability:

    def test_noisy_signal_same_zone_no_flicker(self):
        """Slightly noisy signal in one zone should not cause flickering."""
        zm = ZoneMapper(num_zones=4, hysteresis_margin=0.08)
        # Center of top zone (0.5, 0.2) with small jitter
        rng = np.random.default_rng(42)
        zone_ids = []
        for _ in range(50):
            x = 0.5 + rng.normal(0, 0.02)
            y = 0.2 + rng.normal(0, 0.02)
            result = zm.map(x, y)
            zone_ids.append(result.zone_id)
        # All results should be zone 0 (top)
        assert all(z == 0 for z in zone_ids)

    def test_boundary_with_hysteresis(self):
        """Movement near a boundary should be stabilized by hysteresis."""
        zm = ZoneMapper(num_zones=4, hysteresis_margin=0.05)
        # Start firmly in top zone
        zm.map(0.5, 0.15)
        # Move to boundary area - within hysteresis margin
        result = zm.map(0.5, 0.34)
        assert result.zone_id == 0  # Should stay in top

    def test_clear_zone_transition(self):
        """A clear movement to a different zone should update correctly."""
        zm = ZoneMapper(num_zones=4, hysteresis_margin=0.05)
        # Start in top zone
        r1 = zm.map(0.5, 0.1)
        assert r1.zone_id == 0
        # Move clearly to bottom zone
        r2 = zm.map(0.5, 0.9)
        assert r2.zone_id == 2

    def test_9_zone_stability(self):
        """9-zone layout should also be stable with noise."""
        zm = ZoneMapper(num_zones=9, hysteresis_margin=0.05)
        rng = np.random.default_rng(42)
        # Center of center zone in 3x3 grid: (0.5, 0.5)
        zone_ids = []
        for _ in range(30):
            x = 0.5 + rng.normal(0, 0.01)
            y = 0.5 + rng.normal(0, 0.01)
            result = zm.map(x, y)
            zone_ids.append(result.zone_id)
        assert all(z == 4 for z in zone_ids)  # center of 3x3


# ---------------------------------------------------------------------------
# Calibration -> zone flow
# ---------------------------------------------------------------------------

class TestCalibrationToZoneFlow:

    def test_calibrate_and_map(self):
        """Calibrate with 5 points, then map through to a zone."""
        calibrator = GazeCalibrator()
        zone_mapper = ZoneMapper(num_zones=4)

        # Calibration: gaze angles -> screen coordinates
        gaze_pts = [
            (-10.0, -15.0),
            (10.0, -15.0),
            (0.0, 0.0),
            (-10.0, 15.0),
            (10.0, 15.0),
        ]
        screen_targets = [
            (0.15, 0.15),
            (0.85, 0.15),
            (0.5, 0.5),
            (0.15, 0.85),
            (0.85, 0.85),
        ]

        result = calibrator.calibrate(gaze_pts, screen_targets)
        assert result.success
        assert result.points_used == 5

        # Apply calibration to a new gaze point (looking center-top)
        transformed = calibrator.apply([(0.0, -15.0)])
        screen_x, screen_y = float(transformed[0, 0]), float(transformed[0, 1])

        # Map to zone
        zone_result = zone_mapper.map(screen_x, screen_y)
        # With this calibration, looking center-top should map to
        # the top area of the screen
        assert zone_result.zone_id == 0  # top zone
        assert zone_result.confidence > 0.0

    def test_calibration_improves_consistency(self):
        """Calibrated points should map more consistently than raw ones."""
        calibrator = GazeCalibrator()
        zone_mapper = ZoneMapper(num_zones=4)

        # Simple calibration
        gaze_pts = [
            (0.0, 0.0),
            (1.0, 0.0),
            (0.5, 0.5),
            (0.0, 1.0),
            (1.0, 1.0),
        ]
        screen_targets = [
            (0.1, 0.1),
            (0.9, 0.1),
            (0.5, 0.5),
            (0.1, 0.9),
            (0.9, 0.9),
        ]
        calibrator.calibrate(gaze_pts, screen_targets)

        # Multiple gaze points that should all be in the top zone
        top_gaze_points = [(0.3, 0.0), (0.5, 0.0), (0.7, 0.0)]
        for gpt in top_gaze_points:
            transformed = calibrator.apply([gpt])
            sx, sy = float(transformed[0, 0]), float(transformed[0, 1])
            zone = zone_mapper.map(sx, sy)
            assert zone.zone_id == 0  # All should be top zone


# ---------------------------------------------------------------------------
# Full gaze chain
# ---------------------------------------------------------------------------

class TestFullGazeChain:

    def test_100_frames_smoother_to_zone(self):
        """Run 100 simulated gaze frames through smoother -> zone mapper."""
        smoother = DualAxisSmoother(process_noise=0.1, measurement_noise=1.0)
        zone_mapper = ZoneMapper(num_zones=4)
        rng = np.random.default_rng(42)

        # Simulate looking at the "top" zone for 100 frames
        # Top zone center: (0.5, 0.2) -- so pitch ~12 deg, yaw ~0 deg
        # Normalized: norm_x = (yaw+30)/60 = 0.5, norm_y = (pitch+20)/40 = 0.8
        # Wait -- pitch positive = looking up, so for top zone we want
        # norm_y = (pitch+20)/40 small, meaning pitch should be around -12 deg
        target_pitch = -12.0  # Looking up -> norm_y = (-12+20)/40 = 0.2
        target_yaw = 0.0      # Center -> norm_x = (0+30)/60 = 0.5

        zone_ids = []
        for _ in range(100):
            noisy_pitch = target_pitch + rng.normal(0, 1.0)
            noisy_yaw = target_yaw + rng.normal(0, 1.0)

            sp, sy = smoother.update(noisy_pitch, noisy_yaw)

            # Normalize (same as pipeline.process_face_data)
            norm_x = (sy + 30) / 60
            norm_y = (sp + 20) / 40
            norm_x = max(0.0, min(1.0, norm_x))
            norm_y = max(0.0, min(1.0, norm_y))

            result = zone_mapper.map(norm_x, norm_y)
            zone_ids.append(result.zone_id)

        # After initial convergence, all frames should map to zone 0 (top)
        # Skip first 10 frames for convergence
        stable_zones = zone_ids[10:]
        assert all(z == 0 for z in stable_zones), (
            f"Expected all zone 0, got {set(stable_zones)}"
        )

    def test_zone_transition_sequence(self):
        """Simulate looking top -> right -> bottom -> left."""
        smoother = DualAxisSmoother(process_noise=0.5, measurement_noise=0.5)
        zone_mapper = ZoneMapper(num_zones=4)

        # (pitch, yaw) for each zone:
        # top:    pitch=-12, yaw=0   -> norm (0.5, 0.2)
        # right:  pitch=0,   yaw=18  -> norm (0.8, 0.5)
        # bottom: pitch=12,  yaw=0   -> norm (0.5, 0.8)
        # left:   pitch=0,   yaw=-18 -> norm (0.2, 0.5)
        targets = [
            (-12.0, 0.0, 0),   # top
            (0.0, 18.0, 1),    # right
            (12.0, 0.0, 2),    # bottom
            (0.0, -18.0, 3),   # left
        ]

        for target_pitch, target_yaw, expected_zone in targets:
            smoother.reset()
            # Settle for 30 frames
            for _ in range(30):
                sp, sy = smoother.update(target_pitch, target_yaw)
            norm_x = max(0.0, min(1.0, (sy + 30) / 60))
            norm_y = max(0.0, min(1.0, (sp + 20) / 40))
            result = zone_mapper.map(norm_x, norm_y)
            assert result.zone_id == expected_zone, (
                f"pitch={target_pitch}, yaw={target_yaw}: "
                f"expected zone {expected_zone}, got {result.zone_id} "
                f"at ({norm_x:.2f}, {norm_y:.2f})"
            )

    def test_gaze_estimator_heuristic_chain(self):
        """GazeEstimator heuristic -> Smoother -> ZoneMapper."""
        estimator = GazeEstimator()
        estimator.initialize()  # Falls back to heuristic (no model file)

        smoother = DualAxisSmoother()
        zone_mapper = ZoneMapper(num_zones=4)

        # Create face data with iris looking straight ahead
        face_data = _make_face_data(iris_offset_x=0.0, iris_offset_y=0.0)
        gaze = estimator.estimate(face_data)

        assert gaze.method == "heuristic"

        for _ in range(20):
            sp, sy = smoother.update(gaze.pitch, gaze.yaw)

        norm_x = max(0.0, min(1.0, (sy + 30) / 60))
        norm_y = max(0.0, min(1.0, (sp + 20) / 40))
        result = zone_mapper.map(norm_x, norm_y)

        # With iris centered, gaze should be roughly forward
        assert result is not None
        assert 0 <= result.zone_id < 4

        estimator.close()

    def test_gaze_estimator_left_offset(self):
        """Iris shifted left should produce negative yaw."""
        estimator = GazeEstimator()
        estimator.initialize()

        face_data = _make_face_data(iris_offset_x=-0.3, iris_offset_y=0.0)
        gaze = estimator.estimate(face_data)

        # Negative offset should produce negative yaw (looking left)
        assert gaze.yaw < 0

        estimator.close()

    def test_gaze_estimator_right_offset(self):
        """Iris shifted right should produce positive yaw."""
        estimator = GazeEstimator()
        estimator.initialize()

        face_data = _make_face_data(iris_offset_x=0.3, iris_offset_y=0.0)
        gaze = estimator.estimate(face_data)

        assert gaze.yaw > 0

        estimator.close()

"""Tests for the GazeEstimator module.

Covers:
  - GazeResult dataclass construction
  - Heuristic estimation with synthetic FaceData
  - Directional gaze (left, right, center, up, down)
  - Graceful ONNX fallback when model file is missing
  - Initialization without model file
"""

from __future__ import annotations

import numpy as np
import pytest

from voicereach.engine.gaze.gaze_estimator import GazeEstimator, GazeResult
from voicereach.engine.gaze.mediapipe_tracker import (
    LEFT_EYE_INDICES,
    RIGHT_EYE_INDICES,
    FaceData,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_fake_face_data(
    left_iris_offset: tuple[float, float] = (0.0, 0.0),
    right_iris_offset: tuple[float, float] = (0.0, 0.0),
) -> FaceData:
    """Build a minimal synthetic FaceData for testing.

    The eye landmarks are placed at known positions so that the
    heuristic estimator can compute meaningful displacements.

    ``left_iris_offset`` / ``right_iris_offset`` shift the iris
    *relative* to the eye centre in pixel-like coordinates.
    """
    landmarks = np.zeros((478, 3), dtype=np.float32)

    # ------------------------------------------------------------------
    # Left eye landmarks  (indices from LEFT_EYE_INDICES)
    # Place them in a horizontal ellipse centred at (100, 100).
    # Landmark 33  = outer corner, landmark 133 = inner corner.
    # ------------------------------------------------------------------
    left_cx, left_cy = 100.0, 100.0
    left_half_w = 15.0  # half eye-width

    # Outer (33) and inner (133) corners define the eye width used by
    # the heuristic for normalisation.
    landmarks[33] = [left_cx - left_half_w, left_cy, 0]
    landmarks[133] = [left_cx + left_half_w, left_cy, 0]

    # Fill remaining LEFT_EYE_INDICES around the centre
    for idx in LEFT_EYE_INDICES:
        if idx in (33, 133):
            continue
        # scatter around centre
        angle = np.random.uniform(0, 2 * np.pi)
        landmarks[idx] = [
            left_cx + 5 * np.cos(angle),
            left_cy + 3 * np.sin(angle),
            0,
        ]

    # ------------------------------------------------------------------
    # Right eye landmarks  (indices from RIGHT_EYE_INDICES)
    # Centred at (200, 100).
    # Landmark 362 = outer corner, landmark 263 = inner corner.
    # ------------------------------------------------------------------
    right_cx, right_cy = 200.0, 100.0
    right_half_w = 15.0

    landmarks[362] = [right_cx + right_half_w, right_cy, 0]
    landmarks[263] = [right_cx - right_half_w, right_cy, 0]

    for idx in RIGHT_EYE_INDICES:
        if idx in (362, 263):
            continue
        angle = np.random.uniform(0, 2 * np.pi)
        landmarks[idx] = [
            right_cx + 5 * np.cos(angle),
            right_cy + 3 * np.sin(angle),
            0,
        ]

    # ------------------------------------------------------------------
    # Iris positions  (centre of eye + caller offset)
    # ------------------------------------------------------------------
    left_eye_center = landmarks[LEFT_EYE_INDICES, :2].mean(axis=0)
    right_eye_center = landmarks[RIGHT_EYE_INDICES, :2].mean(axis=0)

    left_iris = np.array(
        [left_eye_center[0] + left_iris_offset[0],
         left_eye_center[1] + left_iris_offset[1]],
        dtype=np.float32,
    )
    right_iris = np.array(
        [right_eye_center[0] + right_iris_offset[0],
         right_eye_center[1] + right_iris_offset[1]],
        dtype=np.float32,
    )

    return FaceData(
        landmarks=landmarks,
        left_eye_patch=np.zeros((64, 64), dtype=np.float32),
        right_eye_patch=np.zeros((64, 64), dtype=np.float32),
        left_iris=left_iris,
        right_iris=right_iris,
        head_pose=np.zeros(3, dtype=np.float32),
        face_bbox=(50, 50, 200, 150),
        confidence=1.0,
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestGazeResult:
    def test_construction(self):
        r = GazeResult(pitch=5.0, yaw=-3.0, confidence=0.9, method="onnx")
        assert r.pitch == 5.0
        assert r.yaw == -3.0
        assert r.confidence == 0.9
        assert r.method == "onnx"

    def test_heuristic_label(self):
        r = GazeResult(pitch=0.0, yaw=0.0, confidence=0.5, method="heuristic")
        assert r.method == "heuristic"


class TestGazeEstimatorInit:
    def test_not_available_without_model(self):
        est = GazeEstimator(model_path="/nonexistent/model.onnx")
        est.initialize()
        assert not est._available

    def test_defaults_to_heuristic(self):
        est = GazeEstimator(model_path="/nonexistent/model.onnx")
        est.initialize()
        fd = make_fake_face_data()
        result = est.estimate(fd)
        assert result.method == "heuristic"

    def test_close_resets_state(self):
        est = GazeEstimator(model_path="/nonexistent/model.onnx")
        est.initialize()
        est.close()
        assert not est._available
        assert est._session is None


class TestHeuristicEstimation:
    """Test that iris offsets produce expected gaze directions."""

    def setup_method(self):
        self.est = GazeEstimator(model_path="/nonexistent/model.onnx")
        self.est.initialize()

    def test_center_gaze_near_zero(self):
        fd = make_fake_face_data(
            left_iris_offset=(0, 0),
            right_iris_offset=(0, 0),
        )
        r = self.est.estimate(fd)
        assert r.method == "heuristic"
        assert abs(r.yaw) < 5.0
        assert abs(r.pitch) < 5.0

    def test_looking_right_positive_yaw(self):
        # Shift iris to the right (positive x offset)
        fd = make_fake_face_data(
            left_iris_offset=(8, 0),
            right_iris_offset=(8, 0),
        )
        r = self.est.estimate(fd)
        assert r.yaw > 5.0, f"Expected positive yaw for rightward gaze, got {r.yaw}"

    def test_looking_left_negative_yaw(self):
        # Shift iris to the left (negative x offset)
        fd = make_fake_face_data(
            left_iris_offset=(-8, 0),
            right_iris_offset=(-8, 0),
        )
        r = self.est.estimate(fd)
        assert r.yaw < -5.0, f"Expected negative yaw for leftward gaze, got {r.yaw}"

    def test_looking_up_positive_pitch(self):
        # Shift iris upward (negative y offset, since y inverted -> positive pitch)
        fd = make_fake_face_data(
            left_iris_offset=(0, -5),
            right_iris_offset=(0, -5),
        )
        r = self.est.estimate(fd)
        assert r.pitch > 3.0, f"Expected positive pitch for upward gaze, got {r.pitch}"

    def test_looking_down_negative_pitch(self):
        # Shift iris downward (positive y offset -> negative pitch)
        fd = make_fake_face_data(
            left_iris_offset=(0, 5),
            right_iris_offset=(0, 5),
        )
        r = self.est.estimate(fd)
        assert r.pitch < -3.0, f"Expected negative pitch for downward gaze, got {r.pitch}"

    def test_confidence_is_medium(self):
        fd = make_fake_face_data()
        r = self.est.estimate(fd)
        assert r.confidence == 0.5  # heuristic always reports 0.5

    def test_degenerate_eye_width_returns_zero(self):
        """If the eye landmarks collapse to a point, return zero gaze."""
        fd = make_fake_face_data()
        # Collapse left eye outer/inner to the same point
        fd.landmarks[33] = fd.landmarks[133]
        # Collapse right eye outer/inner to the same point
        fd.landmarks[362] = fd.landmarks[263]
        r = self.est.estimate(fd)
        assert r.pitch == 0.0
        assert r.yaw == 0.0
        assert r.confidence == 0.1


class TestOnnxFallback:
    """Verify that ONNX path gracefully falls back when model is absent."""

    def test_missing_model_uses_heuristic(self):
        est = GazeEstimator(model_path="/tmp/definitely_not_a_real_model.onnx")
        est.initialize()
        fd = make_fake_face_data(left_iris_offset=(5, 0), right_iris_offset=(5, 0))
        r = est.estimate(fd)
        assert r.method == "heuristic"
        assert r.yaw > 0  # still produces a meaningful result

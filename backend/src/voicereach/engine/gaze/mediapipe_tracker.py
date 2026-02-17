"""MediaPipe Face Mesh wrapper for facial landmark extraction.

Extracts 468 facial landmarks + iris landmarks from camera frames.
Provides eye region patches and head pose estimation.

Performance target: ~5ms per frame (docs/02_EYE_TRACKING_AND_INPUT.md)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import cv2
import numpy as np

logger = logging.getLogger(__name__)

# Key landmark indices
LEFT_EYE_INDICES = [33, 133, 160, 159, 158, 144, 145, 153]
RIGHT_EYE_INDICES = [362, 263, 387, 386, 385, 373, 374, 380]
LEFT_IRIS_CENTER = 468
RIGHT_IRIS_CENTER = 473

# Head pose reference points (nose tip, chin, left/right eye outer, left/right mouth)
HEAD_POSE_INDICES = [1, 152, 33, 263, 61, 291]

# 3D model points for PnP (generic face model, mm)
MODEL_POINTS = np.array([
    [0.0, 0.0, 0.0],          # Nose tip
    [0.0, -330.0, -65.0],     # Chin
    [-225.0, 170.0, -135.0],  # Left eye outer
    [225.0, 170.0, -135.0],   # Right eye outer
    [-150.0, -150.0, -125.0], # Left mouth corner
    [150.0, -150.0, -125.0],  # Right mouth corner
], dtype=np.float64)


@dataclass
class FaceData:
    """Extracted face data from a single frame."""
    landmarks: np.ndarray           # (468+10, 3) all landmarks
    left_eye_patch: np.ndarray      # (64, 64) normalized eye region
    right_eye_patch: np.ndarray     # (64, 64) normalized eye region
    left_iris: np.ndarray           # (2,) iris center normalized
    right_iris: np.ndarray          # (2,) iris center normalized
    head_pose: np.ndarray           # (3,) pitch, yaw, roll in degrees
    face_bbox: tuple[int, int, int, int]  # x, y, w, h
    confidence: float


class MediaPipeTracker:
    """Wrapper around MediaPipe Face Mesh for landmark extraction."""

    def __init__(
        self,
        max_num_faces: int = 1,
        refine_landmarks: bool = True,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ) -> None:
        self._max_faces = max_num_faces
        self._refine = refine_landmarks
        self._min_detect = min_detection_confidence
        self._min_track = min_tracking_confidence
        self._face_mesh = None
        self._frame_size: tuple[int, int] | None = None

    def initialize(self) -> None:
        """Initialize MediaPipe Face Mesh."""
        import mediapipe as mp
        self._face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=self._max_faces,
            refine_landmarks=self._refine,
            min_detection_confidence=self._min_detect,
            min_tracking_confidence=self._min_track,
        )
        logger.info("MediaPipe Face Mesh initialized")

    def process_frame(self, frame: np.ndarray) -> FaceData | None:
        """Process a camera frame and extract face data.

        Args:
            frame: BGR image from camera (H, W, 3)

        Returns:
            FaceData if a face is detected, None otherwise.
        """
        if self._face_mesh is None:
            raise RuntimeError("Call initialize() first")

        h, w = frame.shape[:2]
        self._frame_size = (w, h)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb.flags.writeable = False
        results = self._face_mesh.process(rgb)

        if not results.multi_face_landmarks:
            return None

        face_lm = results.multi_face_landmarks[0]
        landmarks = np.array(
            [(lm.x * w, lm.y * h, lm.z * w) for lm in face_lm.landmark],
            dtype=np.float32,
        )

        left_patch = self._extract_eye_patch(frame, landmarks, LEFT_EYE_INDICES)
        right_patch = self._extract_eye_patch(frame, landmarks, RIGHT_EYE_INDICES)

        left_iris = landmarks[LEFT_IRIS_CENTER, :2] if len(landmarks) > LEFT_IRIS_CENTER else np.zeros(2)
        right_iris = landmarks[RIGHT_IRIS_CENTER, :2] if len(landmarks) > RIGHT_IRIS_CENTER else np.zeros(2)

        head_pose = self._estimate_head_pose(landmarks, w, h)

        face_pts = landmarks[:468, :2]
        x_min, y_min = face_pts.min(axis=0).astype(int)
        x_max, y_max = face_pts.max(axis=0).astype(int)

        return FaceData(
            landmarks=landmarks,
            left_eye_patch=left_patch,
            right_eye_patch=right_patch,
            left_iris=left_iris,
            right_iris=right_iris,
            head_pose=head_pose,
            face_bbox=(x_min, y_min, x_max - x_min, y_max - y_min),
            confidence=1.0,
        )

    def _extract_eye_patch(
        self,
        frame: np.ndarray,
        landmarks: np.ndarray,
        indices: list[int],
        patch_size: int = 64,
    ) -> np.ndarray:
        """Extract and normalize an eye region patch."""
        eye_pts = landmarks[indices, :2]
        center = eye_pts.mean(axis=0)
        eye_w = np.linalg.norm(eye_pts[0] - eye_pts[1])  # eye width
        margin = eye_w * 0.5

        x1 = max(0, int(center[0] - margin))
        y1 = max(0, int(center[1] - margin * 0.7))
        x2 = min(frame.shape[1], int(center[0] + margin))
        y2 = min(frame.shape[0], int(center[1] + margin * 0.7))

        if x2 <= x1 or y2 <= y1:
            return np.zeros((patch_size, patch_size), dtype=np.float32)

        patch = frame[y1:y2, x1:x2]
        gray = cv2.cvtColor(patch, cv2.COLOR_BGR2GRAY) if len(patch.shape) == 3 else patch
        resized = cv2.resize(gray, (patch_size, patch_size))
        return resized.astype(np.float32) / 255.0

    def _estimate_head_pose(
        self, landmarks: np.ndarray, frame_w: int, frame_h: int
    ) -> np.ndarray:
        """Estimate head pose (pitch, yaw, roll) using PnP."""
        image_points = np.array(
            [landmarks[i, :2] for i in HEAD_POSE_INDICES],
            dtype=np.float64,
        )

        focal_length = frame_w
        center = (frame_w / 2, frame_h / 2)
        camera_matrix = np.array(
            [[focal_length, 0, center[0]],
             [0, focal_length, center[1]],
             [0, 0, 1]],
            dtype=np.float64,
        )
        dist_coeffs = np.zeros((4, 1))

        success, rotation_vec, _ = cv2.solvePnP(
            MODEL_POINTS, image_points, camera_matrix, dist_coeffs,
            flags=cv2.SOLVEPNP_ITERATIVE,
        )

        if not success:
            return np.zeros(3, dtype=np.float32)

        rotation_mat, _ = cv2.Rodrigues(rotation_vec)
        pose_mat = cv2.hconcat([rotation_mat, np.zeros((3, 1))])
        _, _, _, _, _, _, euler_angles = cv2.decomposeProjectionMatrix(
            cv2.hconcat([pose_mat, np.array([[0, 0, 0, 1]], dtype=np.float64).T])[:3]
        )

        pitch = float(euler_angles[0][0])
        yaw = float(euler_angles[1][0])
        roll = float(euler_angles[2][0])

        return np.array([pitch, yaw, roll], dtype=np.float32)

    def close(self) -> None:
        """Release MediaPipe resources."""
        if self._face_mesh:
            self._face_mesh.close()
            self._face_mesh = None

"""Gaze direction estimator using MobileOne + L2CS-Net.

Takes eye patches from MediaPipeTracker and estimates pitch/yaw gaze angles.
Falls back to an iris-center heuristic if the ONNX model is not available.

Performance target: ~3 ms per inference (docs/02_EYE_TRACKING_AND_INPUT.md)

Architecture overview:
  MediaPipeTracker  ->  FaceData (eye patches + iris positions)
                          |
                    GazeEstimator
                    /            \\
             ONNX path      heuristic path
           (L2CS-Net)    (iris displacement)
                    \\            /
                     GazeResult(pitch, yaw, confidence, method)
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from voicereach.config import settings
from voicereach.engine.gaze.mediapipe_tracker import (
    LEFT_EYE_INDICES,
    RIGHT_EYE_INDICES,
    FaceData,
)

logger = logging.getLogger(__name__)


@dataclass
class GazeResult:
    """Estimated gaze direction."""

    pitch: float  # degrees, positive = looking up
    yaw: float  # degrees, positive = looking right
    confidence: float
    method: str  # "onnx" or "heuristic"


class GazeEstimator:
    """Estimates gaze direction from eye patches or face data.

    When an ONNX model (L2CS-Net) is available, it is used for
    high-accuracy estimation.  Otherwise an iris-displacement
    heuristic provides a rough approximation.
    """

    def __init__(
        self,
        model_path: str | None = None,
    ) -> None:
        self._model_path = model_path or settings.gaze_model_path
        self._session = None  # onnxruntime.InferenceSession | None
        self._available = False

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def initialize(self) -> None:
        """Load the ONNX model for gaze estimation."""
        model_file = Path(self._model_path)
        if not model_file.exists():
            logger.info(
                "Gaze model not found at %s, using heuristic",
                model_file,
            )
            return

        try:
            import onnxruntime as ort  # type: ignore[import-untyped]

            providers = ort.get_available_providers()
            # Prefer CoreML on macOS (Apple Silicon) or CUDA on Linux/Windows
            preferred = [
                p
                for p in [
                    "CoreMLExecutionProvider",
                    "CUDAExecutionProvider",
                    "CPUExecutionProvider",
                ]
                if p in providers
            ]
            self._session = ort.InferenceSession(
                str(model_file), providers=preferred
            )
            self._available = True
            logger.info("Gaze estimator loaded with providers: %s", preferred)
        except ImportError:
            logger.info("onnxruntime not installed, using heuristic gaze estimation")
        except Exception:
            logger.warning(
                "Failed to load gaze model, using heuristic", exc_info=True
            )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def estimate(self, face_data: FaceData) -> GazeResult:
        """Estimate gaze direction from face data."""
        if self._available and self._session is not None:
            return self._estimate_onnx(face_data)
        return self._estimate_heuristic(face_data)

    # ------------------------------------------------------------------
    # ONNX path (L2CS-Net)
    # ------------------------------------------------------------------

    def _estimate_onnx(self, face_data: FaceData) -> GazeResult:
        """ONNX-based gaze estimation (L2CS-Net architecture).

        L2CS-Net expects (B, 3, 224, 224) RGB input.  Our eye patches
        are 64x64 grayscale, so we resize and replicate across channels.
        """
        import cv2  # already a project dependency

        left = face_data.left_eye_patch  # (64, 64) float32 [0, 1]
        right = face_data.right_eye_patch

        # Resize to L2CS expected resolution
        left_resized = cv2.resize(left, (224, 224))
        right_resized = cv2.resize(right, (224, 224))

        # Grayscale -> pseudo-RGB: (1, 3, 224, 224)
        left_rgb = np.stack([left_resized] * 3, axis=0)[np.newaxis]
        right_rgb = np.stack([right_resized] * 3, axis=0)[np.newaxis]

        try:
            input_name = self._session.get_inputs()[0].name

            left_out = self._session.run(
                None, {input_name: left_rgb.astype(np.float32)}
            )
            right_out = self._session.run(
                None, {input_name: right_rgb.astype(np.float32)}
            )

            # L2CS outputs: gaze_pitch, gaze_yaw (each as bin probabilities)
            # Average both eyes for final estimate
            left_pitch, left_yaw = self._decode_gaze(left_out)
            right_pitch, right_yaw = self._decode_gaze(right_out)

            pitch = (left_pitch + right_pitch) / 2
            yaw = (left_yaw + right_yaw) / 2

            return GazeResult(
                pitch=pitch, yaw=yaw, confidence=0.9, method="onnx"
            )
        except Exception:
            logger.warning("ONNX inference failed, falling back to heuristic")
            return self._estimate_heuristic(face_data)

    @staticmethod
    def _decode_gaze(outputs) -> tuple[float, float]:
        """Decode L2CS bin probabilities to continuous angles.

        L2CS uses 90 bins covering -180 to 180 degrees.  A softmax over
        the logits followed by a weighted sum gives the predicted angle.
        """
        pitch_logits = outputs[0][0]  # (90,)
        yaw_logits = outputs[1][0]  # (90,)

        num_bins = len(pitch_logits)
        bin_width = 2 * 180.0 / num_bins
        bins = np.arange(num_bins) * bin_width - 180.0 + bin_width / 2

        # Softmax
        pitch_probs = np.exp(pitch_logits - pitch_logits.max())
        pitch_probs /= pitch_probs.sum()
        yaw_probs = np.exp(yaw_logits - yaw_logits.max())
        yaw_probs /= yaw_probs.sum()

        pitch = float(np.sum(bins * pitch_probs))
        yaw = float(np.sum(bins * yaw_probs))

        return pitch, yaw

    # ------------------------------------------------------------------
    # Heuristic path (iris displacement)
    # ------------------------------------------------------------------

    def _estimate_heuristic(self, face_data: FaceData) -> GazeResult:
        """Iris-center based gaze heuristic (no model needed).

        Uses the iris position relative to the eye bounding box centre
        as a simple proxy for gaze direction.
        """
        landmarks = face_data.landmarks

        # Eye centres (average of boundary landmarks)
        left_eye_center = landmarks[LEFT_EYE_INDICES, :2].mean(axis=0)
        left_iris = face_data.left_iris

        right_eye_center = landmarks[RIGHT_EYE_INDICES, :2].mean(axis=0)
        right_iris = face_data.right_iris

        # Eye widths for normalisation
        # Landmark 33 = left eye outer, 133 = left eye inner
        left_eye_width = float(
            np.linalg.norm(landmarks[33, :2] - landmarks[133, :2])
        )
        # Landmark 362 = right eye outer, 263 = right eye inner
        right_eye_width = float(
            np.linalg.norm(landmarks[362, :2] - landmarks[263, :2])
        )

        if left_eye_width < 1 or right_eye_width < 1:
            return GazeResult(
                pitch=0.0, yaw=0.0, confidence=0.1, method="heuristic"
            )

        left_dx = (left_iris[0] - left_eye_center[0]) / left_eye_width
        left_dy = (left_iris[1] - left_eye_center[1]) / left_eye_width
        right_dx = (right_iris[0] - right_eye_center[0]) / right_eye_width
        right_dy = (right_iris[1] - right_eye_center[1]) / right_eye_width

        # Average both eyes and map to approximate degrees
        dx = (left_dx + right_dx) / 2
        dy = (left_dy + right_dy) / 2

        yaw = float(dx * 60.0)  # ~60 degrees full horizontal range
        pitch = float(-dy * 40.0)  # ~40 degrees full vertical range (y inverted)

        return GazeResult(
            pitch=pitch, yaw=yaw, confidence=0.5, method="heuristic"
        )

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Release ONNX runtime resources."""
        self._session = None
        self._available = False

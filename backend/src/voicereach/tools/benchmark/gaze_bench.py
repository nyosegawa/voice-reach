"""Benchmark MediaPipe Face Mesh gaze tracking performance.

Measures FPS, per-frame latency percentiles, and frame drop rate
using either a live camera feed or synthetic face images.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass

import cv2
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class GazeBenchResult:
    """Results from a gaze tracking benchmark run."""

    fps: float
    latency_p50_ms: float
    latency_p95_ms: float
    latency_p99_ms: float
    frames_processed: int
    frames_dropped: int  # where no face was detected
    resolution: tuple[int, int]


def _generate_synthetic_face(width: int = 640, height: int = 480) -> np.ndarray:
    """Generate a synthetic face image for benchmarking without a camera.

    Draws an oval face with circle eyes on a neutral background.
    This is sufficient to trigger MediaPipe Face Mesh detection in most cases,
    though detection is not guaranteed on every synthetic frame.
    """
    frame = np.full((height, width, 3), 200, dtype=np.uint8)

    # Face oval
    center_x, center_y = width // 2, height // 2
    cv2.ellipse(
        frame,
        (center_x, center_y),
        (120, 160),
        0, 0, 360,
        (180, 150, 130),
        -1,
    )

    # Left eye
    cv2.circle(frame, (center_x - 45, center_y - 30), 18, (255, 255, 255), -1)
    cv2.circle(frame, (center_x - 45, center_y - 30), 8, (60, 40, 20), -1)
    cv2.circle(frame, (center_x - 45, center_y - 30), 4, (0, 0, 0), -1)

    # Right eye
    cv2.circle(frame, (center_x + 45, center_y - 30), 18, (255, 255, 255), -1)
    cv2.circle(frame, (center_x + 45, center_y - 30), 8, (60, 40, 20), -1)
    cv2.circle(frame, (center_x + 45, center_y - 30), 4, (0, 0, 0), -1)

    # Nose
    pts = np.array([
        [center_x, center_y - 5],
        [center_x - 10, center_y + 20],
        [center_x + 10, center_y + 20],
    ], dtype=np.int32)
    cv2.fillPoly(frame, [pts], (170, 140, 120))

    # Mouth
    cv2.ellipse(
        frame,
        (center_x, center_y + 55),
        (30, 10),
        0, 0, 360,
        (150, 100, 100),
        -1,
    )

    return frame


def run_gaze_benchmark(
    camera_id: int = 0,
    duration_s: float = 10.0,
    warmup_frames: int = 30,
    use_synthetic: bool = False,
) -> GazeBenchResult:
    """Run a gaze tracking benchmark.

    Args:
        camera_id: Camera device index (ignored when use_synthetic=True).
        duration_s: How long to run the benchmark in seconds.
        warmup_frames: Number of warmup frames to discard before timing.
        use_synthetic: Use synthetic face images instead of a live camera.

    Returns:
        GazeBenchResult with FPS, latency percentiles, and drop stats.

    Raises:
        RuntimeError: If camera cannot be opened (when use_synthetic=False).
    """
    from voicereach.engine.gaze.mediapipe_tracker import MediaPipeTracker

    tracker = MediaPipeTracker()
    tracker.initialize()

    cap = None
    synthetic_frame: np.ndarray | None = None

    if use_synthetic:
        synthetic_frame = _generate_synthetic_face()
        resolution = (synthetic_frame.shape[1], synthetic_frame.shape[0])
    else:
        cap = cv2.VideoCapture(camera_id)
        if not cap.isOpened():
            tracker.close()
            raise RuntimeError(
                f"Cannot open camera {camera_id}. "
                "Use --synthetic to benchmark without a camera."
            )
        resolution = (
            int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        )

    try:
        # Warmup phase
        for _ in range(warmup_frames):
            if use_synthetic:
                frame = synthetic_frame
            else:
                ret, frame = cap.read()
                if not ret:
                    break
            tracker.process_frame(frame)

        # Benchmark phase
        latencies: list[float] = []
        frames_dropped = 0
        start_time = time.perf_counter()

        while (time.perf_counter() - start_time) < duration_s:
            if use_synthetic:
                frame = synthetic_frame
            else:
                ret, frame = cap.read()
                if not ret:
                    break

            t0 = time.perf_counter()
            result = tracker.process_frame(frame)
            t1 = time.perf_counter()

            latency_ms = (t1 - t0) * 1000.0
            latencies.append(latency_ms)

            if result is None:
                frames_dropped += 1

        elapsed = time.perf_counter() - start_time
        frames_processed = len(latencies)

        if frames_processed == 0:
            return GazeBenchResult(
                fps=0.0,
                latency_p50_ms=0.0,
                latency_p95_ms=0.0,
                latency_p99_ms=0.0,
                frames_processed=0,
                frames_dropped=0,
                resolution=resolution,
            )

        arr = np.array(latencies)
        return GazeBenchResult(
            fps=frames_processed / elapsed,
            latency_p50_ms=float(np.percentile(arr, 50)),
            latency_p95_ms=float(np.percentile(arr, 95)),
            latency_p99_ms=float(np.percentile(arr, 99)),
            frames_processed=frames_processed,
            frames_dropped=frames_dropped,
            resolution=resolution,
        )
    finally:
        tracker.close()
        if cap is not None:
            cap.release()

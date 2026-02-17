"""Zone mapping with hysteresis for gaze-based UI navigation.

Maps continuous gaze coordinates to discrete screen zones.
Hysteresis prevents chattering at zone boundaries.

Zone layouts (from docs/02_EYE_TRACKING_AND_INPUT.md):
- 4 zones: top, right, bottom, left (MVP)
- 9 zones: 3x3 grid
- 16 zones: 4x4 grid (advanced)
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class ZoneResult:
    """Result of zone mapping."""
    zone_id: int
    confidence: float
    center_x: float
    center_y: float


class ZoneMapper:
    """Maps gaze position to screen zones with hysteresis."""

    def __init__(
        self,
        num_zones: int = 4,
        hysteresis_margin: float = 0.05,
    ) -> None:
        self._num_zones = num_zones
        self._hysteresis = hysteresis_margin
        self._current_zone = -1
        self._zones = self._build_zones(num_zones)

    def map(self, screen_x: float, screen_y: float) -> ZoneResult:
        """Map normalized screen coordinates (0-1) to a zone.

        Args:
            screen_x: Horizontal position, 0=left, 1=right
            screen_y: Vertical position, 0=top, 1=bottom

        Returns:
            ZoneResult with zone ID and confidence.
        """
        best_zone = -1
        best_dist = float("inf")

        for zone_id, (cx, cy, x1, y1, x2, y2) in self._zones.items():
            # Check if point is in zone (with hysteresis)
            margin = -self._hysteresis if zone_id == self._current_zone else self._hysteresis
            in_zone = (
                x1 - margin <= screen_x <= x2 + margin
                and y1 - margin <= screen_y <= y2 + margin
            )

            dist = np.sqrt((screen_x - cx) ** 2 + (screen_y - cy) ** 2)
            if in_zone and dist < best_dist:
                best_zone = zone_id
                best_dist = dist

        if best_zone == -1:
            # Fallback: nearest zone center
            for zone_id, (cx, cy, *_) in self._zones.items():
                dist = np.sqrt((screen_x - cx) ** 2 + (screen_y - cy) ** 2)
                if dist < best_dist:
                    best_zone = zone_id
                    best_dist = dist

        self._current_zone = best_zone

        cx, cy = self._zones[best_zone][0], self._zones[best_zone][1]
        max_dist = np.sqrt(0.5)  # max possible distance in normalized space
        confidence = max(0.0, 1.0 - best_dist / max_dist)

        return ZoneResult(
            zone_id=best_zone,
            confidence=round(confidence, 3),
            center_x=cx,
            center_y=cy,
        )

    def set_num_zones(self, num_zones: int) -> None:
        """Change the zone layout."""
        self._num_zones = num_zones
        self._zones = self._build_zones(num_zones)
        self._current_zone = -1

    def _build_zones(self, n: int) -> dict[int, tuple[float, float, float, float, float, float]]:
        """Build zone definitions: {id: (center_x, center_y, x1, y1, x2, y2)}."""
        if n == 4:
            return {
                0: (0.5, 0.2, 0.2, 0.0, 0.8, 0.35),    # top
                1: (0.8, 0.5, 0.65, 0.2, 1.0, 0.8),     # right
                2: (0.5, 0.8, 0.2, 0.65, 0.8, 1.0),     # bottom
                3: (0.2, 0.5, 0.0, 0.2, 0.35, 0.8),     # left
            }

        # Grid layout for 9, 16
        cols = int(np.sqrt(n))
        rows = (n + cols - 1) // cols
        zones = {}
        idx = 0
        for r in range(rows):
            for c in range(cols):
                if idx >= n:
                    break
                x1 = c / cols
                y1 = r / rows
                x2 = (c + 1) / cols
                y2 = (r + 1) / rows
                cx = (x1 + x2) / 2
                cy = (y1 + y2) / 2
                zones[idx] = (cx, cy, x1, y1, x2, y2)
                idx += 1
        return zones

    @property
    def current_zone(self) -> int:
        return self._current_zone

import { useEffect, useCallback } from "react";
import { useAppStore } from "../stores/appStore";

/**
 * Hook for managing gaze zone state.
 * In production: receives gaze data via WebSocket from backend.
 * In dev mode: simulates gaze zones from mouse position.
 */
export function useGazeZone(opts?: { devMode?: boolean }) {
  const setGazeZone = useAppStore((s) => s.setGazeZone);
  const devMode = opts?.devMode ?? process.env.NODE_ENV === "development";

  const mapMouseToZone = useCallback(
    (e: MouseEvent) => {
      const x = e.clientX / window.innerWidth;
      const y = e.clientY / window.innerHeight;

      // 4-zone layout: top(0), right(1), bottom(2), left(3)
      if (y < 0.35 && x > 0.2 && x < 0.8) {
        setGazeZone(0); // top
      } else if (x > 0.65 && y > 0.2 && y < 0.8) {
        setGazeZone(1); // right
      } else if (y > 0.65 && x > 0.2 && x < 0.8) {
        setGazeZone(2); // bottom
      } else if (x < 0.35 && y > 0.2 && y < 0.8) {
        setGazeZone(3); // left
      } else {
        setGazeZone(-1); // no zone
      }
    },
    [setGazeZone]
  );

  useEffect(() => {
    if (!devMode) return;

    window.addEventListener("mousemove", mapMouseToZone);
    // Show cursor in dev mode
    document.body.style.cursor = "crosshair";

    return () => {
      window.removeEventListener("mousemove", mapMouseToZone);
      document.body.style.cursor = "none";
    };
  }, [devMode, mapMouseToZone]);
}

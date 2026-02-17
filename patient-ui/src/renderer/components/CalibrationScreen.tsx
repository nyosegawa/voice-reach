import { useState } from "react";

const CALIBRATION_POINTS = [
  { x: 10, y: 10 },   // top-left
  { x: 90, y: 10 },   // top-right
  { x: 50, y: 50 },   // center
  { x: 10, y: 90 },   // bottom-left
  { x: 90, y: 90 },   // bottom-right
];

export function CalibrationScreen() {
  const [currentPoint, setCurrentPoint] = useState(0);

  // Advance to next calibration point (called by gaze dwell or click)
  const advancePoint = () => setCurrentPoint((p) => p + 1);

  const point = CALIBRATION_POINTS[currentPoint];
  if (!point) {
    return (
      <div className="calibration-screen">
        <div className="calibration-screen__complete">
          校正完了
        </div>
      </div>
    );
  }

  return (
    <div className="calibration-screen">
      <div
        className="calibration-point__wrapper"
        style={{ left: `${point.x}%`, top: `${point.y}%` }}
      >
        <div className="calibration-point" onClick={advancePoint} />
        <div className="calibration-screen__instruction">
          この点を見つめてください ({currentPoint + 1}/{CALIBRATION_POINTS.length})
        </div>
      </div>
    </div>
  );
}

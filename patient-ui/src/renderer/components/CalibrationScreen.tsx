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

  const point = CALIBRATION_POINTS[currentPoint];
  if (!point) {
    return (
      <div style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        height: "100%",
        fontSize: "2rem",
      }}>
        校正完了
      </div>
    );
  }

  return (
    <div style={{ position: "absolute", inset: 0, background: "#0a0a1a" }}>
      <div
        style={{
          position: "absolute",
          left: `${point.x}%`,
          top: `${point.y}%`,
          transform: "translate(-50%, -50%)",
        }}
      >
        <div
          style={{
            width: "40px",
            height: "40px",
            borderRadius: "50%",
            background: "#3b82f6",
            border: "4px solid #93c5fd",
            animation: "pulse 1.5s ease-in-out infinite",
          }}
        />
        <div
          style={{
            textAlign: "center",
            marginTop: "16px",
            fontSize: "1rem",
            opacity: 0.7,
          }}
        >
          この点を見つめてください ({currentPoint + 1}/5)
        </div>
      </div>

      <style>{`
        @keyframes pulse {
          0%, 100% { transform: scale(1); opacity: 1; }
          50% { transform: scale(1.3); opacity: 0.7; }
        }
      `}</style>
    </div>
  );
}

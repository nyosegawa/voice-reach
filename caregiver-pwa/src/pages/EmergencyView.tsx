import { useEffect } from "react";
import { useCaregiverStore } from "../stores/caregiverStore";

interface EmergencyViewProps {
  onAcknowledge: () => void;
  onDismiss: () => void;
}

export function EmergencyView({ onAcknowledge, onDismiss }: EmergencyViewProps) {
  const emergencyActive = useCaregiverStore((s) => s.emergencyActive);
  const emergencyTimestamp = useCaregiverStore((s) => s.emergencyTimestamp);
  const emergencyCategory = useCaregiverStore((s) => s.emergencyCategory);

  // Vibrate device on mount if supported
  useEffect(() => {
    if ("vibrate" in navigator) {
      navigator.vibrate([200, 100, 200, 100, 400]);
    }
  }, []);

  // If emergency is no longer active, show resolved state
  if (!emergencyActive) {
    return (
      <div
        style={{
          position: "fixed",
          inset: 0,
          background: "#166534",
          color: "#fff",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          zIndex: 1000,
        }}
      >
        <div style={{ fontSize: "3rem", marginBottom: "16px" }}>OK</div>
        <h1 style={{ fontSize: "1.5rem", fontWeight: 700, marginBottom: "12px" }}>
          緊急対応完了
        </h1>
        <p style={{ fontSize: "1rem", marginBottom: "24px", opacity: 0.8 }}>
          緊急通報は確認されました
        </p>
        <button onClick={onDismiss} style={dismissButtonStyle}>
          ダッシュボードに戻る
        </button>
      </div>
    );
  }

  const handleAcknowledge = () => {
    // Stop vibration
    if ("vibrate" in navigator) {
      navigator.vibrate(0);
    }
    onAcknowledge();
  };

  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        background: "#dc2626",
        color: "#fff",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 1000,
      }}
    >
      <div style={{ fontSize: "4rem", marginBottom: "24px" }}>!!</div>
      <h1 style={{ fontSize: "2rem", fontWeight: 700, marginBottom: "16px" }}>
        緊急通報
      </h1>

      {/* Emergency category */}
      {emergencyCategory && (
        <p
          style={{
            fontSize: "1.5rem",
            fontWeight: 600,
            marginBottom: "12px",
            background: "rgba(255,255,255,0.15)",
            padding: "8px 24px",
            borderRadius: "8px",
          }}
        >
          {emergencyCategory}
        </p>
      )}

      <p style={{ fontSize: "1.25rem", marginBottom: "8px" }}>
        患者からの緊急呼び出し
      </p>

      {/* Timestamp */}
      {emergencyTimestamp && (
        <p style={{ fontSize: "0.875rem", opacity: 0.7, marginBottom: "32px" }}>
          {formatTimestamp(emergencyTimestamp)}
        </p>
      )}

      <button onClick={handleAcknowledge} style={ackButtonStyle}>
        確認しました
      </button>
    </div>
  );
}

function formatTimestamp(ts: string): string {
  try {
    const date = new Date(ts);
    return date.toLocaleString("ja-JP", {
      month: "long",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  } catch {
    return ts;
  }
}

const ackButtonStyle: React.CSSProperties = {
  padding: "16px 48px",
  fontSize: "1.25rem",
  fontWeight: 700,
  background: "#fff",
  color: "#dc2626",
  border: "none",
  borderRadius: "12px",
  cursor: "pointer",
};

const dismissButtonStyle: React.CSSProperties = {
  padding: "12px 32px",
  fontSize: "1rem",
  fontWeight: 600,
  background: "rgba(255,255,255,0.2)",
  color: "#fff",
  border: "2px solid rgba(255,255,255,0.4)",
  borderRadius: "12px",
  cursor: "pointer",
};

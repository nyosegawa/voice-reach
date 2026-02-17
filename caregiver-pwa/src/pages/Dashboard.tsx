import { useCaregiverStore } from "../stores/caregiverStore";
import type { ConnectionStatus } from "../stores/caregiverStore";

interface DashboardProps {
  onNavigateEmergency: () => void;
}

export function Dashboard({ onNavigateEmergency }: DashboardProps) {
  const connectionStatus = useCaregiverStore((s) => s.connectionStatus);
  const patientStatus = useCaregiverStore((s) => s.patientStatus);
  const emergencyActive = useCaregiverStore((s) => s.emergencyActive);

  return (
    <div>
      <h2 style={{ fontSize: "1.25rem", fontWeight: 700, margin: "16px 0" }}>
        患者ステータス
      </h2>

      {/* Connection status */}
      <div style={cardStyle}>
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <div style={connectionDotStyle(connectionStatus)} />
          <span>{connectionLabel(connectionStatus)}</span>
        </div>
        {patientStatus && (
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "8px",
              marginTop: "8px",
            }}
          >
            <div
              style={{
                width: "10px",
                height: "10px",
                borderRadius: "50%",
                background: patientStatus.is_online ? "#22c55e" : "#ef4444",
              }}
            />
            <span style={{ fontSize: "0.875rem" }}>
              患者: {patientStatus.is_online ? "オンライン" : "オフライン"}
            </span>
          </div>
        )}
      </div>

      {/* Utterances today */}
      <div style={cardStyle}>
        <h3 style={cardLabelStyle}>本日の発話数</h3>
        <div style={{ fontSize: "2rem", fontWeight: 700 }}>
          {patientStatus?.utterances_today ?? 0}
        </div>
      </div>

      {/* Current emotion */}
      <div style={cardStyle}>
        <h3 style={cardLabelStyle}>現在の感情</h3>
        <div style={{ fontSize: "1.25rem" }}>
          {patientStatus?.current_emotion ?? "---"}
        </div>
      </div>

      {/* Input method */}
      <div style={cardStyle}>
        <h3 style={cardLabelStyle}>入力方式</h3>
        <div style={{ fontSize: "1.25rem" }}>
          {patientStatus?.active_input ?? "---"}
        </div>
      </div>

      {/* Last activity */}
      <div style={cardStyle}>
        <h3 style={cardLabelStyle}>最終アクティビティ</h3>
        <div style={{ fontSize: "1rem" }}>
          {patientStatus?.last_activity
            ? formatTimestamp(patientStatus.last_activity)
            : "---"}
        </div>
      </div>

      {/* Emergency quick-access button */}
      {emergencyActive && (
        <button
          onClick={onNavigateEmergency}
          style={{
            width: "100%",
            padding: "16px",
            fontSize: "1.125rem",
            fontWeight: 700,
            background: "#dc2626",
            color: "#fff",
            border: "none",
            borderRadius: "12px",
            cursor: "pointer",
            marginTop: "8px",
            animation: "pulse 1.5s infinite",
          }}
        >
          緊急通報を確認する
        </button>
      )}
    </div>
  );
}

function connectionDotStyle(status: ConnectionStatus): React.CSSProperties {
  const colorMap: Record<ConnectionStatus, string> = {
    connected: "#22c55e",
    connecting: "#eab308",
    disconnected: "#ef4444",
  };
  return {
    width: "12px",
    height: "12px",
    borderRadius: "50%",
    background: colorMap[status],
  };
}

function connectionLabel(status: ConnectionStatus): string {
  const labelMap: Record<ConnectionStatus, string> = {
    connected: "接続中",
    connecting: "接続試行中...",
    disconnected: "切断",
  };
  return labelMap[status];
}

function formatTimestamp(ts: string): string {
  try {
    const date = new Date(ts);
    return date.toLocaleString("ja-JP", {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch {
    return ts;
  }
}

const cardStyle: React.CSSProperties = {
  background: "#fff",
  borderRadius: "12px",
  padding: "16px",
  marginBottom: "12px",
  boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
};

const cardLabelStyle: React.CSSProperties = {
  fontSize: "0.875rem",
  opacity: 0.6,
  marginBottom: "4px",
};

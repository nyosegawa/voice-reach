import { useAppStore } from "../stores/appStore";

export function StatusBar() {
  const connectionStatus = useAppStore((s) => s.connectionStatus);
  const inputMode = useAppStore((s) => s.inputMode);

  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        right: 0,
        height: "48px",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0 24px",
        background: "rgba(0, 0, 0, 0.5)",
        zIndex: 100,
        fontSize: "0.875rem",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
        <span style={{ fontWeight: 700 }}>VoiceReach</span>
        <span style={{ opacity: 0.6 }}>|</span>
        <span style={{ opacity: 0.8 }}>{inputMode}</span>
      </div>

      <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
        <div
          style={{
            width: "8px",
            height: "8px",
            borderRadius: "50%",
            background:
              connectionStatus === "connected"
                ? "#22c55e"
                : connectionStatus === "reconnecting"
                  ? "#eab308"
                  : "#ef4444",
          }}
        />
        <span style={{ opacity: 0.7 }}>
          {connectionStatus === "connected"
            ? "接続中"
            : connectionStatus === "reconnecting"
              ? "再接続中..."
              : "未接続"}
        </span>
      </div>
    </div>
  );
}

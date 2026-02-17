import { useAppStore } from "../stores/appStore";

export function StatusBar() {
  const connectionStatus = useAppStore((s) => s.connectionStatus);
  const inputMode = useAppStore((s) => s.inputMode);

  const indicatorClass = connectionStatus === "connected"
    ? "status-bar__indicator--connected"
    : connectionStatus === "reconnecting"
      ? "status-bar__indicator--connecting"
      : "status-bar__indicator--disconnected";

  const statusText = connectionStatus === "connected"
    ? "接続中"
    : connectionStatus === "reconnecting"
      ? "再接続中..."
      : "未接続";

  return (
    <div className="status-bar">
      <div className="status-bar__left">
        <span className="status-bar__brand">VoiceReach</span>
        <span className="status-bar__separator">|</span>
        <span className="status-bar__mode">{inputMode}</span>
      </div>

      <div className="status-bar__right">
        <div className={`status-bar__indicator ${indicatorClass}`} />
        <span className="status-bar__status-text">{statusText}</span>
      </div>
    </div>
  );
}

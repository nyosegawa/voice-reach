import { useAppStore } from "../stores/appStore";

export function GazeDebugOverlay() {
  const gazeZone = useAppStore((s) => s.gazeZone);
  const connectionStatus = useAppStore((s) => s.connectionStatus);

  return (
    <div
      style={{
        position: "absolute",
        top: "56px",
        right: "16px",
        padding: "12px",
        background: "rgba(0, 0, 0, 0.8)",
        borderRadius: "8px",
        fontSize: "0.75rem",
        fontFamily: "monospace",
        zIndex: 200,
      }}
    >
      <div>Zone: {gazeZone}</div>
      <div>WS: {connectionStatus}</div>
    </div>
  );
}

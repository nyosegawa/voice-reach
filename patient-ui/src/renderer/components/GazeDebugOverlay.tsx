import { useAppStore } from "../stores/appStore";

export function GazeDebugOverlay() {
  const gazeZone = useAppStore((s) => s.gazeZone);
  const connectionStatus = useAppStore((s) => s.connectionStatus);

  return (
    <div className="gaze-debug">
      <div>Zone: {gazeZone}</div>
      <div>WS: {connectionStatus}</div>
    </div>
  );
}

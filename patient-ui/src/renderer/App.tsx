import { useEffect } from "react";
import { useAppStore } from "./stores/appStore";
import { useWebSocket } from "./hooks/useWebSocket";
import { useGazeZone } from "./hooks/useGazeZone";
import { useCandidates } from "./hooks/useCandidates";
import { useEmergency } from "./hooks/useEmergency";
import { FloatingBubble } from "./components/FloatingBubble";
import { StatusBar } from "./components/StatusBar";
import { ConversationLog } from "./components/ConversationLog";
import { EmergencyScreen } from "./components/EmergencyScreen";
import { CalibrationScreen } from "./components/CalibrationScreen";
import { GazeDebugOverlay } from "./components/GazeDebugOverlay";

export function App() {
  const mode = useAppStore((s) => s.inputMode);
  const { sendCandidateSelected, sendInputEvent } = useWebSocket();

  // Initialize gaze tracking (mouse simulation in dev mode)
  useGazeZone({ devMode: true });

  // Candidate interaction
  const { confirmGazedCandidate } = useCandidates(sendCandidateSelected);

  // Emergency mode
  const { triggerEmergency } = useEmergency(sendInputEvent);

  // Keyboard shortcuts for development
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      switch (e.key) {
        case " ":
          e.preventDefault();
          confirmGazedCandidate();
          break;
        case "Escape":
          triggerEmergency();
          break;
        case "1":
        case "2":
        case "3":
        case "4": {
          const index = parseInt(e.key) - 1;
          const requestId = useAppStore.getState().requestId;
          if (requestId) sendCandidateSelected(requestId, index);
          break;
        }
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [confirmGazedCandidate, triggerEmergency, sendCandidateSelected]);

  return (
    <div style={{ width: "100%", height: "100%", position: "relative" }}>
      <StatusBar />

      {mode === "candidate" && <FloatingBubble />}
      {mode === "emergency" && <EmergencyScreen />}
      {mode === "calibration" && <CalibrationScreen />}

      <ConversationLog />

      {process.env.NODE_ENV === "development" && <GazeDebugOverlay />}
    </div>
  );
}

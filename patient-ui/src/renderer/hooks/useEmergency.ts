import { useCallback } from "react";
import { useAppStore } from "../stores/appStore";

/**
 * Hook for emergency mode management.
 */
export function useEmergency(sendInputEvent: (event: Record<string, unknown>) => void) {
  const setInputMode = useAppStore((s) => s.setInputMode);
  const inputMode = useAppStore((s) => s.inputMode);

  const triggerEmergency = useCallback(() => {
    setInputMode("emergency");
    sendInputEvent({
      event_type: "EMERGENCY",
      source: "keyboard",
      confidence: 1.0,
      timestamp_ms: Date.now(),
    });
  }, [setInputMode, sendInputEvent]);

  const cancelEmergency = useCallback(() => {
    setInputMode("candidate");
  }, [setInputMode]);

  return {
    isEmergencyMode: inputMode === "emergency",
    triggerEmergency,
    cancelEmergency,
  };
}

import { useCallback } from "react";
import { useAppStore } from "../stores/appStore";

/**
 * Hook for candidate interaction logic.
 * Manages candidate selection and confirmation.
 */
export function useCandidates(sendCandidateSelected: (requestId: string, index: number) => void) {
  const candidates = useAppStore((s) => s.candidates);
  const requestId = useAppStore((s) => s.requestId);
  const gazeZone = useAppStore((s) => s.gazeZone);
  const addSpeechEntry = useAppStore((s) => s.addSpeechEntry);
  const clearCandidates = useAppStore((s) => s.clearCandidates);

  const selectCandidate = useCallback(
    (index: number) => {
      if (!requestId || index < 0 || index >= candidates.length) return;

      const candidate = candidates[index];
      sendCandidateSelected(requestId, index);

      addSpeechEntry({
        text: candidate.text,
        timestamp: Date.now(),
        wasSpoken: true,
      });

      clearCandidates();
    },
    [candidates, requestId, sendCandidateSelected, addSpeechEntry, clearCandidates]
  );

  const confirmGazedCandidate = useCallback(() => {
    if (gazeZone >= 0 && gazeZone < candidates.length) {
      selectCandidate(gazeZone);
    }
  }, [gazeZone, candidates.length, selectCandidate]);

  return { selectCandidate, confirmGazedCandidate };
}

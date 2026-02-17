import { create } from "zustand";

export type InputMode = "candidate" | "hiragana" | "emergency" | "calibration";
export type ConnectionStatus = "connected" | "disconnected" | "reconnecting";

interface CandidateItem {
  text: string;
  intentAxis: string;
  confidence: number;
  generationStage: number;
}

interface SpeechEntry {
  text: string;
  timestamp: number;
  wasSpoken: boolean;
}

interface AppState {
  // Connection
  connectionStatus: ConnectionStatus;
  setConnectionStatus: (status: ConnectionStatus) => void;

  // Input mode
  inputMode: InputMode;
  setInputMode: (mode: InputMode) => void;

  // Gaze
  gazeZone: number;
  setGazeZone: (zone: number) => void;

  // Candidates
  candidates: CandidateItem[];
  requestId: string | null;
  setCandidates: (candidates: CandidateItem[], requestId: string) => void;
  clearCandidates: () => void;

  // Conversation
  conversationHistory: SpeechEntry[];
  addSpeechEntry: (entry: SpeechEntry) => void;
}

export const useAppStore = create<AppState>((set) => ({
  connectionStatus: "disconnected",
  setConnectionStatus: (status) => set({ connectionStatus: status }),

  inputMode: "candidate",
  setInputMode: (mode) => set({ inputMode: mode }),

  gazeZone: -1,
  setGazeZone: (zone) => set({ gazeZone: zone }),

  candidates: [],
  requestId: null,
  setCandidates: (candidates, requestId) => set({ candidates, requestId }),
  clearCandidates: () => set({ candidates: [], requestId: null }),

  conversationHistory: [],
  addSpeechEntry: (entry) =>
    set((state) => ({
      conversationHistory: [...state.conversationHistory.slice(-49), entry],
    })),
}));

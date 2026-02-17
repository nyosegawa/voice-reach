import { create } from "zustand";
import type {
  PatientStatusSummary,
  SpeechLogEntry,
  Notification as AppNotification,
} from "@shared/types";

const MAX_SPEECH_LOG_ENTRIES = 100;

export type ConnectionStatus = "connecting" | "connected" | "disconnected";

export interface CaregiverStore {
  // Connection
  connectionStatus: ConnectionStatus;
  setConnectionStatus: (status: ConnectionStatus) => void;

  // Patient
  patientStatus: PatientStatusSummary | null;
  setPatientStatus: (status: PatientStatusSummary) => void;

  // Speech log
  speechLog: SpeechLogEntry[];
  addSpeechLogEntry: (entry: SpeechLogEntry) => void;

  // Notifications
  notifications: AppNotification[];
  addNotification: (n: AppNotification) => void;
  removeNotification: (index: number) => void;

  // Emergency
  emergencyActive: boolean;
  emergencyTimestamp: string | null;
  emergencyCategory: string | null;
  setEmergencyActive: (active: boolean) => void;
  setEmergencyDetails: (timestamp: string, category: string | null) => void;
}

export const useCaregiverStore = create<CaregiverStore>((set) => ({
  // Connection
  connectionStatus: "disconnected",
  setConnectionStatus: (connectionStatus) => set({ connectionStatus }),

  // Patient
  patientStatus: null,
  setPatientStatus: (patientStatus) => set({ patientStatus }),

  // Speech log
  speechLog: [],
  addSpeechLogEntry: (entry) =>
    set((state) => ({
      speechLog: [entry, ...state.speechLog].slice(0, MAX_SPEECH_LOG_ENTRIES),
    })),

  // Notifications
  notifications: [],
  addNotification: (n) =>
    set((state) => ({
      notifications: [...state.notifications, n],
    })),
  removeNotification: (index) =>
    set((state) => ({
      notifications: state.notifications.filter((_, i) => i !== index),
    })),

  // Emergency
  emergencyActive: false,
  emergencyTimestamp: null,
  emergencyCategory: null,
  setEmergencyActive: (emergencyActive) => set({ emergencyActive }),
  setEmergencyDetails: (emergencyTimestamp, emergencyCategory) =>
    set({ emergencyTimestamp, emergencyCategory }),
}));

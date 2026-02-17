/**
 * Shared type definitions for VoiceReach.
 * These mirror the Python Pydantic models in backend/src/voicereach/models/
 */

// --- IAL Events ---

export type EventType = "SELECT" | "CONFIRM" | "CANCEL" | "EMERGENCY" | "SCROLL";
export type InputSource = "gaze" | "finger" | "blink" | "keyboard";
export type ScrollDirection = "up" | "down" | "left" | "right";

export interface IALEvent {
  event_type: EventType;
  source: InputSource;
  target_id: number | null;
  confidence: number;
  timestamp_ms: number;
  scroll_direction?: ScrollDirection;
}

// --- Candidates ---

export type IntentAxis =
  | "emotional_response"
  | "question"
  | "self_reference"
  | "other_reference"
  | "action_request"
  | "humor"
  | "topic_change";

export type GenerationStage = 1 | 2 | 3;

export interface Candidate {
  text: string;
  intent_axis: IntentAxis;
  confidence: number;
  generation_stage: GenerationStage;
  latency_ms: number;
}

export interface CandidateSet {
  candidates: Candidate[];
  stage: GenerationStage;
  request_id: string;
  timestamp_ms: number;
  is_final: boolean;
}

// --- WebSocket Messages ---

// Client -> Server
export interface GazeUpdateMessage {
  type: "gaze_update";
  zone_id: number;
  confidence: number;
  timestamp_ms: number;
}

export interface InputEventMessage {
  type: "input_event";
  event: IALEvent;
}

export interface CandidateSelectedMessage {
  type: "candidate_selected";
  request_id: string;
  candidate_index: number;
}

export type ClientMessage = GazeUpdateMessage | InputEventMessage | CandidateSelectedMessage;

// Server -> Client
export interface CandidateUpdateMessage {
  type: "candidate_update";
  request_id: string;
  candidate_set: CandidateSet;
  is_final: boolean;
}

export interface TTSReadyMessage {
  type: "tts_ready";
  audio_url: string;
  text: string;
  duration_ms: number;
}

export interface EmergencyAckMessage {
  type: "emergency_ack";
  notified_caregivers: string[];
}

export interface ErrorMessage {
  type: "error";
  detail: string;
}

export type ServerMessage =
  | CandidateUpdateMessage
  | TTSReadyMessage
  | EmergencyAckMessage
  | ErrorMessage;

// --- Context ---

export type ALSStage = 1 | 2 | 3 | 4;

export interface EmotionState {
  valence: number;
  arousal: number;
  confidence: number;
}

export interface PatientState {
  als_stage: ALSStage;
  active_input_source: string;
  emotion: EmotionState;
  fatigue_level: number;
}

// --- Caregiver ---

export type NotificationLevel = "info" | "warning" | "emergency";

export interface Notification {
  level: NotificationLevel;
  title: string;
  body: string;
  timestamp: string;
  requires_ack: boolean;
}

export interface SpeechLogEntry {
  text: string;
  timestamp: string;
  generation_stage: number;
  was_spoken: boolean;
  emotion_valence: number;
}

export interface PatientStatusSummary {
  is_online: boolean;
  last_activity: string | null;
  utterances_today: number;
  avg_selection_time_ms: number;
  current_emotion: string;
  active_input: string;
}

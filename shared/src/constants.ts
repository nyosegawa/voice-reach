/**
 * Shared constants for VoiceReach.
 */

/** Maximum number of candidates per set */
export const MAX_CANDIDATES = 4;

/** Default WebSocket backend URL */
export const DEFAULT_WS_URL = "ws://127.0.0.1:8765";

/** Stage latency targets (ms) */
export const STAGE_LATENCY = {
  LOCAL_FAST: 150,
  LOCAL_QUALITY: 350,
  CLOUD: 800,
} as const;

/** Eye tracking zone layouts */
export const ZONE_LAYOUTS = {
  SIMPLE: 4,
  STANDARD: 9,
  ADVANCED: 16,
} as const;

/** Calibration points for 5-point calibration */
export const CALIBRATION_POINTS = [
  { x: 0.1, y: 0.1 },
  { x: 0.9, y: 0.1 },
  { x: 0.5, y: 0.5 },
  { x: 0.1, y: 0.9 },
  { x: 0.9, y: 0.9 },
] as const;

/** Emergency categories */
export const EMERGENCY_CATEGORIES = [
  { id: 0, label: "呼吸が苦しい" },
  { id: 1, label: "強い痛み" },
  { id: 2, label: "吸引が必要" },
  { id: 3, label: "人を呼んで" },
] as const;

/** Intent axis labels (Japanese) */
export const INTENT_AXIS_LABELS: Record<string, string> = {
  emotional_response: "感情表現",
  question: "質問",
  self_reference: "自己言及",
  other_reference: "他者言及",
  action_request: "行動依頼",
  humor: "ユーモア",
  topic_change: "話題転換",
} as const;

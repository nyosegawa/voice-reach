import { useEffect, useRef, useCallback } from "react";
import { useAppStore } from "../stores/appStore";

const WS_URL = "ws://127.0.0.1:8765/ws/patient";
const RECONNECT_DELAY_MS = 3000;
const MAX_RECONNECT_ATTEMPTS = 10;

type ServerMessage = {
  type: string;
  [key: string]: unknown;
};

export function useWebSocket() {
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectAttempts = useRef(0);
  const reconnectTimer = useRef<ReturnType<typeof setTimeout>>();

  const setConnectionStatus = useAppStore((s) => s.setConnectionStatus);
  const setCandidates = useAppStore((s) => s.setCandidates);
  const setInputMode = useAppStore((s) => s.setInputMode);

  const connect = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return;

    setConnectionStatus("reconnecting");
    const ws = new WebSocket(WS_URL);

    ws.onopen = () => {
      setConnectionStatus("connected");
      reconnectAttempts.current = 0;
    };

    ws.onclose = () => {
      setConnectionStatus("disconnected");
      wsRef.current = null;
      scheduleReconnect();
    };

    ws.onerror = () => {
      ws.close();
    };

    ws.onmessage = (event) => {
      try {
        const msg = JSON.parse(event.data) as ServerMessage;
        handleMessage(msg);
      } catch {
        console.warn("Invalid WS message:", event.data);
      }
    };

    wsRef.current = ws;
  }, [setConnectionStatus]);

  const scheduleReconnect = useCallback(() => {
    if (reconnectAttempts.current >= MAX_RECONNECT_ATTEMPTS) {
      setConnectionStatus("disconnected");
      return;
    }
    reconnectAttempts.current++;
    reconnectTimer.current = setTimeout(connect, RECONNECT_DELAY_MS);
  }, [connect, setConnectionStatus]);

  const handleMessage = useCallback(
    (msg: ServerMessage) => {
      switch (msg.type) {
        case "candidate_update": {
          const cs = msg.candidate_set as {
            candidates: Array<{
              text: string;
              intent_axis: string;
              confidence: number;
              generation_stage: number;
            }>;
          };
          const requestId = msg.request_id as string;
          setCandidates(
            cs.candidates.map((c) => ({
              text: c.text,
              intentAxis: c.intent_axis,
              confidence: c.confidence,
              generationStage: c.generation_stage,
            })),
            requestId
          );
          break;
        }
        case "tts_ready": {
          const audioUrl = msg.audio_url as string;
          // Play audio
          const audio = new Audio(`http://127.0.0.1:8765${audioUrl}`);
          audio.play().catch(console.error);
          break;
        }
        case "emergency_ack": {
          // Return to candidate mode after emergency is acknowledged
          setTimeout(() => setInputMode("candidate"), 5000);
          break;
        }
        default:
          break;
      }
    },
    [setCandidates, setInputMode]
  );

  const send = useCallback((data: Record<string, unknown>) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(data));
    }
  }, []);

  const sendGazeUpdate = useCallback(
    (zoneId: number, confidence: number) => {
      send({
        type: "gaze_update",
        zone_id: zoneId,
        confidence,
        timestamp_ms: Date.now(),
      });
    },
    [send]
  );

  const sendCandidateSelected = useCallback(
    (requestId: string, index: number) => {
      send({
        type: "candidate_selected",
        request_id: requestId,
        candidate_index: index,
      });
    },
    [send]
  );

  const sendInputEvent = useCallback(
    (event: Record<string, unknown>) => {
      send({ type: "input_event", event });
    },
    [send]
  );

  useEffect(() => {
    connect();
    return () => {
      if (reconnectTimer.current) clearTimeout(reconnectTimer.current);
      wsRef.current?.close();
    };
  }, [connect]);

  return { send, sendGazeUpdate, sendCandidateSelected, sendInputEvent };
}

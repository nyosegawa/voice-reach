import { useEffect, useRef, useCallback } from "react";
import { DEFAULT_WS_URL } from "@shared/constants";
import type {
  PatientStatusSummary,
  SpeechLogEntry,
  Notification as AppNotification,
} from "@shared/types";
import { useCaregiverStore } from "../stores/caregiverStore";

/** Reconnect backoff: 1s, 2s, 4s, 8s, 16s max */
const INITIAL_RECONNECT_MS = 1000;
const MAX_RECONNECT_MS = 16000;

interface IncomingMessage {
  type: string;
  payload?: unknown;
  [key: string]: unknown;
}

export function useCaregiverWebSocket(url?: string) {
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const reconnectDelayRef = useRef(INITIAL_RECONNECT_MS);
  const mountedRef = useRef(true);

  const {
    connectionStatus,
    patientStatus,
    speechLog,
    notifications,
    emergencyActive,
    setConnectionStatus,
    setPatientStatus,
    addSpeechLogEntry,
    addNotification,
    setEmergencyActive,
    setEmergencyDetails,
  } = useCaregiverStore();

  const wsUrl = url ?? `${DEFAULT_WS_URL}/ws/caregiver`;

  const connect = useCallback(() => {
    if (!mountedRef.current) return;

    // Clean up existing connection
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }

    setConnectionStatus("connecting");

    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onopen = () => {
      if (!mountedRef.current) return;
      setConnectionStatus("connected");
      reconnectDelayRef.current = INITIAL_RECONNECT_MS;
    };

    ws.onclose = () => {
      if (!mountedRef.current) return;
      setConnectionStatus("disconnected");
      scheduleReconnect();
    };

    ws.onerror = () => {
      // onclose will fire after onerror, so reconnect is handled there
    };

    ws.onmessage = (event: MessageEvent) => {
      if (!mountedRef.current) return;
      try {
        const msg = JSON.parse(event.data as string) as IncomingMessage;
        handleMessage(msg);
      } catch {
        // Ignore malformed messages
      }
    };
  }, [wsUrl]); // eslint-disable-line react-hooks/exhaustive-deps

  const scheduleReconnect = useCallback(() => {
    if (!mountedRef.current) return;
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
    const delay = reconnectDelayRef.current;
    reconnectTimeoutRef.current = setTimeout(() => {
      if (mountedRef.current) {
        connect();
      }
    }, delay);
    // Exponential backoff
    reconnectDelayRef.current = Math.min(delay * 2, MAX_RECONNECT_MS);
  }, [connect]);

  const handleMessage = useCallback(
    (msg: IncomingMessage) => {
      switch (msg.type) {
        case "patient_status_update": {
          const status = msg.payload as PatientStatusSummary;
          setPatientStatus(status);
          break;
        }
        case "speech_log_entry": {
          const entry = msg.payload as SpeechLogEntry;
          addSpeechLogEntry(entry);
          break;
        }
        case "notification": {
          const notification = msg.payload as AppNotification;
          addNotification(notification);
          if (notification.level === "emergency") {
            setEmergencyActive(true);
            setEmergencyDetails(
              notification.timestamp,
              notification.title,
            );
          }
          break;
        }
        case "emergency_ack": {
          setEmergencyActive(false);
          break;
        }
        default:
          break;
      }
    },
    [setPatientStatus, addSpeechLogEntry, addNotification, setEmergencyActive, setEmergencyDetails],
  );

  const sendMessage = useCallback((data: Record<string, unknown>) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(data));
    }
  }, []);

  const acknowledgeEmergency = useCallback(() => {
    sendMessage({ type: "acknowledge_emergency" });
  }, [sendMessage]);

  const acknowledgeNotification = useCallback(
    (index: number) => {
      sendMessage({ type: "acknowledge_notification", index });
      useCaregiverStore.getState().removeNotification(index);
    },
    [sendMessage],
  );

  // Connect on mount, clean up on unmount
  useEffect(() => {
    mountedRef.current = true;
    connect();

    return () => {
      mountedRef.current = false;
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (wsRef.current) {
        wsRef.current.close();
        wsRef.current = null;
      }
    };
  }, [connect]);

  return {
    connectionStatus,
    patientStatus,
    speechLog,
    notifications,
    emergencyActive,
    acknowledgeEmergency,
    acknowledgeNotification,
  };
}

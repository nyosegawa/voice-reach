import { useState, useEffect, useRef } from "react";
import { Dashboard } from "./pages/Dashboard";
import { ConversationLog } from "./pages/ConversationLog";
import { EmergencyView } from "./pages/EmergencyView";
import { useCaregiverWebSocket } from "./hooks/useWebSocket";
import { usePushNotification } from "./hooks/usePushNotification";

type Page = "dashboard" | "log" | "emergency";

export function App() {
  const [currentPage, setCurrentPage] = useState<Page>("dashboard");
  const previousPageRef = useRef<Page>("dashboard");

  const {
    emergencyActive,
    notifications,
    acknowledgeEmergency,
  } = useCaregiverWebSocket();

  const { isSupported, isPermissionGranted, requestPermission, showNotification } =
    usePushNotification();

  // Request notification permission on first interaction
  useEffect(() => {
    if (isSupported && !isPermissionGranted) {
      // Prompt on first load — browsers may block without user gesture,
      // but we try anyway; user can grant later via a UI action
      requestPermission();
    }
  }, [isSupported, isPermissionGranted, requestPermission]);

  // Auto-navigate to emergency page when emergencyActive becomes true
  useEffect(() => {
    if (emergencyActive) {
      previousPageRef.current = currentPage;
      setCurrentPage("emergency");

      // Also push a system notification
      showNotification("緊急通報", {
        body: "患者からの緊急呼び出しがあります",
        tag: "emergency",
        requireInteraction: true,
      });
    }
  }, [emergencyActive]); // eslint-disable-line react-hooks/exhaustive-deps

  // Trigger push notification for emergency-level notifications
  const lastNotifCountRef = useRef(0);
  useEffect(() => {
    if (notifications.length > lastNotifCountRef.current) {
      const newNotifications = notifications.slice(lastNotifCountRef.current);
      for (const n of newNotifications) {
        if (n.level === "emergency") {
          showNotification(n.title, {
            body: n.body,
            tag: "emergency",
            requireInteraction: true,
          });
        } else if (n.level === "warning") {
          showNotification(n.title, {
            body: n.body,
            tag: `warning-${Date.now()}`,
          });
        }
      }
    }
    lastNotifCountRef.current = notifications.length;
  }, [notifications, showNotification]);

  const handleEmergencyAcknowledge = () => {
    acknowledgeEmergency();
  };

  const handleEmergencyDismiss = () => {
    setCurrentPage(previousPageRef.current);
  };

  const unreadCount = notifications.length;

  return (
    <div>
      <header
        style={{
          background: "#1e3a5f",
          color: "#fff",
          padding: "12px 16px",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        <h1 style={{ fontSize: "1.125rem", fontWeight: 700 }}>VoiceReach</h1>
        <nav style={{ display: "flex", gap: "16px", fontSize: "0.875rem", alignItems: "center" }}>
          <button
            onClick={() => setCurrentPage("dashboard")}
            style={navStyle(currentPage === "dashboard")}
          >
            ダッシュボード
          </button>
          <button
            onClick={() => setCurrentPage("log")}
            style={navStyle(currentPage === "log")}
          >
            発話ログ
          </button>

          {/* Notification badge */}
          {unreadCount > 0 && (
            <span
              style={{
                background: "#ef4444",
                color: "#fff",
                fontSize: "0.625rem",
                fontWeight: 700,
                minWidth: "18px",
                height: "18px",
                borderRadius: "9px",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                padding: "0 5px",
              }}
            >
              {unreadCount > 99 ? "99+" : unreadCount}
            </span>
          )}
        </nav>
      </header>

      {currentPage === "emergency" ? (
        <EmergencyView
          onAcknowledge={handleEmergencyAcknowledge}
          onDismiss={handleEmergencyDismiss}
        />
      ) : (
        <main style={{ padding: "16px", maxWidth: "600px", margin: "0 auto" }}>
          {currentPage === "dashboard" && (
            <Dashboard onNavigateEmergency={() => setCurrentPage("emergency")} />
          )}
          {currentPage === "log" && <ConversationLog />}
        </main>
      )}
    </div>
  );
}

function navStyle(active: boolean): React.CSSProperties {
  return {
    background: "none",
    border: "none",
    color: active ? "#fff" : "rgba(255,255,255,0.6)",
    cursor: "pointer",
    fontWeight: active ? 700 : 400,
    textDecoration: active ? "underline" : "none",
    textUnderlineOffset: "4px",
  };
}

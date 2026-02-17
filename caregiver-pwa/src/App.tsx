import { useState } from "react";
import { Dashboard } from "./pages/Dashboard";
import { ConversationLog } from "./pages/ConversationLog";
import { EmergencyView } from "./pages/EmergencyView";

type Page = "dashboard" | "log" | "emergency";

export function App() {
  const [currentPage, setCurrentPage] = useState<Page>("dashboard");

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
        <nav style={{ display: "flex", gap: "16px", fontSize: "0.875rem" }}>
          <button onClick={() => setCurrentPage("dashboard")} style={navStyle(currentPage === "dashboard")}>
            ダッシュボード
          </button>
          <button onClick={() => setCurrentPage("log")} style={navStyle(currentPage === "log")}>
            発話ログ
          </button>
        </nav>
      </header>

      <main style={{ padding: "16px", maxWidth: "600px", margin: "0 auto" }}>
        {currentPage === "dashboard" && <Dashboard />}
        {currentPage === "log" && <ConversationLog />}
        {currentPage === "emergency" && <EmergencyView />}
      </main>
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

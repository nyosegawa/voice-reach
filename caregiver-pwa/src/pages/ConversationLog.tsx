export function ConversationLog() {
  // TODO: Connect via WebSocket to get speech log
  return (
    <div>
      <h2 style={{ fontSize: "1.25rem", fontWeight: 700, margin: "16px 0" }}>
        発話ログ
      </h2>

      <div
        style={{
          textAlign: "center",
          padding: "48px 16px",
          color: "#999",
        }}
      >
        まだ発話がありません
      </div>
    </div>
  );
}

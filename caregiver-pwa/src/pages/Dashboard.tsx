export function Dashboard() {
  // TODO: Connect via WebSocket to get patient status
  return (
    <div>
      <h2 style={{ fontSize: "1.25rem", fontWeight: 700, margin: "16px 0" }}>
        患者ステータス
      </h2>

      <div style={cardStyle}>
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <div
            style={{
              width: "12px",
              height: "12px",
              borderRadius: "50%",
              background: "#ef4444",
            }}
          />
          <span>オフライン</span>
        </div>
      </div>

      <div style={cardStyle}>
        <h3 style={{ fontSize: "0.875rem", opacity: 0.6, marginBottom: "4px" }}>
          本日の発話数
        </h3>
        <div style={{ fontSize: "2rem", fontWeight: 700 }}>0</div>
      </div>

      <div style={cardStyle}>
        <h3 style={{ fontSize: "0.875rem", opacity: 0.6, marginBottom: "4px" }}>
          現在の感情
        </h3>
        <div style={{ fontSize: "1.25rem" }}>---</div>
      </div>

      <div style={cardStyle}>
        <h3 style={{ fontSize: "0.875rem", opacity: 0.6, marginBottom: "4px" }}>
          入力方式
        </h3>
        <div style={{ fontSize: "1.25rem" }}>---</div>
      </div>
    </div>
  );
}

const cardStyle: React.CSSProperties = {
  background: "#fff",
  borderRadius: "12px",
  padding: "16px",
  marginBottom: "12px",
  boxShadow: "0 1px 3px rgba(0,0,0,0.1)",
};

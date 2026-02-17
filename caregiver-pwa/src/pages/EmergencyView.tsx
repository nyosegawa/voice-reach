export function EmergencyView() {
  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        background: "#dc2626",
        color: "#fff",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 1000,
      }}
    >
      <div style={{ fontSize: "4rem", marginBottom: "24px" }}>
        !!
      </div>
      <h1 style={{ fontSize: "2rem", fontWeight: 700, marginBottom: "16px" }}>
        緊急通報
      </h1>
      <p style={{ fontSize: "1.25rem", marginBottom: "32px" }}>
        患者からの緊急呼び出し
      </p>
      <button
        style={{
          padding: "16px 48px",
          fontSize: "1.25rem",
          fontWeight: 700,
          background: "#fff",
          color: "#dc2626",
          border: "none",
          borderRadius: "12px",
          cursor: "pointer",
        }}
      >
        確認しました
      </button>
    </div>
  );
}

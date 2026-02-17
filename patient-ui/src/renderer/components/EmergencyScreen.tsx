import { useAppStore } from "../stores/appStore";

const EMERGENCY_OPTIONS = [
  { id: 0, label: "呼吸が苦しい", icon: "🫁" },
  { id: 1, label: "強い痛み", icon: "⚡" },
  { id: 2, label: "吸引が必要", icon: "💨" },
  { id: 3, label: "人を呼んで", icon: "🔔" },
];

export function EmergencyScreen() {
  const gazeZone = useAppStore((s) => s.gazeZone);

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        background: "rgba(220, 38, 38, 0.95)",
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gridTemplateRows: "1fr 1fr",
        gap: "16px",
        padding: "48px",
      }}
    >
      {EMERGENCY_OPTIONS.map((option) => (
        <div
          key={option.id}
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            borderRadius: "24px",
            background:
              gazeZone === option.id
                ? "rgba(255, 255, 255, 0.3)"
                : "rgba(255, 255, 255, 0.1)",
            border:
              gazeZone === option.id
                ? "4px solid #fff"
                : "2px solid rgba(255, 255, 255, 0.3)",
            transition: "all 0.15s ease-out",
          }}
        >
          <div style={{ fontSize: "4rem" }}>{option.icon}</div>
          <div style={{ fontSize: "2rem", marginTop: "16px", fontWeight: 700 }}>
            {option.label}
          </div>
        </div>
      ))}
    </div>
  );
}

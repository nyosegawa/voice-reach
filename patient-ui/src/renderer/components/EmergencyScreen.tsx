import { useAppStore } from "../stores/appStore";

const EMERGENCY_OPTIONS = [
  { id: 0, label: "呼吸が苦しい", icon: "\uD83E\uDEC1" },
  { id: 1, label: "強い痛み", icon: "\u26A1" },
  { id: 2, label: "吸引が必要", icon: "\uD83D\uDCA8" },
  { id: 3, label: "人を呼んで", icon: "\uD83D\uDD14" },
];

export function EmergencyScreen() {
  const gazeZone = useAppStore((s) => s.gazeZone);

  return (
    <div className="emergency-screen">
      <div className="emergency-screen__grid">
        {EMERGENCY_OPTIONS.map((option) => (
          <div
            key={option.id}
            className={`emergency-screen__option ${gazeZone === option.id ? 'emergency-screen__option--gazed' : ''}`}
          >
            <div className="emergency-screen__option-icon">{option.icon}</div>
            <div className="emergency-screen__option-label">
              {option.label}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

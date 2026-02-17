import { useAppStore } from "../stores/appStore";
import { CandidateCard } from "./CandidateCard";

const POSITIONS = [
  { top: "15%", left: "50%", transform: "translateX(-50%)" },      // top
  { top: "50%", right: "10%", transform: "translateY(-50%)" },     // right
  { bottom: "15%", left: "50%", transform: "translateX(-50%)" },   // bottom
  { top: "50%", left: "10%", transform: "translateY(-50%)" },      // left
];

export function FloatingBubble() {
  const candidates = useAppStore((s) => s.candidates);
  const gazeZone = useAppStore((s) => s.gazeZone);

  if (candidates.length === 0) {
    return (
      <div style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        height: "100%",
        fontSize: "1.5rem",
        opacity: 0.5,
      }}>
        会話相手の発話を待っています...
      </div>
    );
  }

  return (
    <div style={{ position: "absolute", inset: 0 }}>
      {candidates.map((candidate, index) => (
        <div
          key={index}
          style={{
            position: "absolute",
            ...POSITIONS[index],
          }}
        >
          <CandidateCard
            text={candidate.text}
            intentAxis={candidate.intentAxis}
            isHighlighted={gazeZone === index}
            index={index}
          />
        </div>
      ))}
    </div>
  );
}

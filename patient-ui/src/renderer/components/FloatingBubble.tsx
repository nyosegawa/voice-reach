import { useAppStore } from "../stores/appStore";
import { CandidateCard } from "./CandidateCard";

export function FloatingBubble() {
  const candidates = useAppStore((s) => s.candidates);
  const gazeZone = useAppStore((s) => s.gazeZone);

  if (candidates.length === 0) {
    return (
      <div className="floating-bubble__waiting">
        会話相手の発話を待っています...
      </div>
    );
  }

  return (
    <div className="floating-bubble__container">
      {candidates.map((candidate, index) => (
        <CandidateCard
          key={index}
          text={candidate.text}
          intentAxis={candidate.intentAxis}
          isHighlighted={gazeZone === index}
          index={index}
        />
      ))}
    </div>
  );
}

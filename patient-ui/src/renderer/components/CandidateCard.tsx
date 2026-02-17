interface CandidateCardProps {
  text: string;
  intentAxis: string;
  isHighlighted: boolean;
  index: number;
}

export function CandidateCard({ text, intentAxis, isHighlighted, index }: CandidateCardProps) {
  return (
    <div
      className={`candidate-card ${isHighlighted ? 'candidate-card--gazed' : ''}`}
    >
      <div className="candidate-card__text">{text}</div>
      <div className="candidate-card__meta">
        {index + 1} | {intentAxis}
      </div>
    </div>
  );
}

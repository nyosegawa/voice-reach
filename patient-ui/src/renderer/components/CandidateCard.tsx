interface CandidateCardProps {
  text: string;
  intentAxis: string;
  isHighlighted: boolean;
  index: number;
}

export function CandidateCard({ text, intentAxis, isHighlighted, index }: CandidateCardProps) {
  return (
    <div
      style={{
        padding: "24px 32px",
        borderRadius: "16px",
        background: isHighlighted ? "#2563eb" : "rgba(255, 255, 255, 0.1)",
        border: isHighlighted ? "3px solid #60a5fa" : "2px solid rgba(255, 255, 255, 0.2)",
        color: "#fff",
        fontSize: "1.5rem",
        maxWidth: "400px",
        textAlign: "center",
        transition: "all 0.15s ease-out",
        transform: isHighlighted ? "scale(1.05)" : "scale(1)",
        boxShadow: isHighlighted ? "0 8px 32px rgba(37, 99, 235, 0.4)" : "none",
      }}
    >
      <div style={{ fontSize: "2rem", lineHeight: 1.4 }}>{text}</div>
      <div
        style={{
          fontSize: "0.75rem",
          opacity: 0.6,
          marginTop: "8px",
        }}
      >
        {index + 1}
      </div>
    </div>
  );
}

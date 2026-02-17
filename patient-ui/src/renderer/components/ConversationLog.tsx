import { useAppStore } from "../stores/appStore";

export function ConversationLog() {
  const history = useAppStore((s) => s.conversationHistory);

  if (history.length === 0) return null;

  return (
    <div
      style={{
        position: "absolute",
        bottom: 0,
        left: 0,
        right: 0,
        maxHeight: "200px",
        overflow: "hidden",
        padding: "16px 24px",
        background: "linear-gradient(transparent, rgba(0, 0, 0, 0.7))",
        zIndex: 50,
      }}
    >
      {history.slice(-3).map((entry, i) => (
        <div
          key={i}
          style={{
            padding: "4px 0",
            opacity: 0.5 + (i / 3) * 0.5,
            fontSize: "1.125rem",
          }}
        >
          {entry.text}
        </div>
      ))}
    </div>
  );
}

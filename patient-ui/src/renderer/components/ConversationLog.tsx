import { useAppStore } from "../stores/appStore";

export function ConversationLog() {
  const history = useAppStore((s) => s.conversationHistory);

  if (history.length === 0) return null;

  return (
    <div className="conversation-log">
      {history.slice(-3).map((entry, i) => (
        <div
          key={i}
          className="conversation-log__entry"
        >
          <span className="conversation-log__text">{entry.text}</span>
        </div>
      ))}
    </div>
  );
}

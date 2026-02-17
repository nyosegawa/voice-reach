import { useEffect, useRef } from "react";
import { useCaregiverStore } from "../stores/caregiverStore";

const STAGE_LABELS: Record<number, string> = {
  1: "即時",
  2: "標準",
  3: "高品質",
};

const STAGE_COLORS: Record<number, string> = {
  1: "#3b82f6",
  2: "#8b5cf6",
  3: "#10b981",
};

/**
 * Map emotion valence (-1 to 1) to a subtle background color.
 * Negative = cool blue tint, positive = warm orange tint, neutral = transparent.
 */
function valenceColor(valence: number): string {
  if (valence < -0.3) return "rgba(59, 130, 246, 0.06)";
  if (valence > 0.3) return "rgba(249, 115, 22, 0.06)";
  return "transparent";
}

export function ConversationLog() {
  const speechLog = useCaregiverStore((s) => s.speechLog);
  const listRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to top (latest) when new entries arrive
  useEffect(() => {
    if (listRef.current) {
      listRef.current.scrollTop = 0;
    }
  }, [speechLog.length]);

  if (speechLog.length === 0) {
    return (
      <div>
        <h2 style={{ fontSize: "1.25rem", fontWeight: 700, margin: "16px 0" }}>
          発話ログ
        </h2>
        <div
          style={{
            textAlign: "center",
            padding: "48px 16px",
            color: "#999",
          }}
        >
          まだ発話がありません
        </div>
      </div>
    );
  }

  return (
    <div>
      <h2 style={{ fontSize: "1.25rem", fontWeight: 700, margin: "16px 0" }}>
        発話ログ
        <span
          style={{
            fontSize: "0.75rem",
            fontWeight: 400,
            opacity: 0.5,
            marginLeft: "8px",
          }}
        >
          ({speechLog.length}件)
        </span>
      </h2>

      <div
        ref={listRef}
        style={{
          maxHeight: "calc(100vh - 180px)",
          overflowY: "auto",
          WebkitOverflowScrolling: "touch",
        }}
      >
        {speechLog.map((entry, i) => (
          <div
            key={`${entry.timestamp}-${i}`}
            style={{
              background: valenceColor(entry.emotion_valence),
              borderRadius: "10px",
              padding: "12px 14px",
              marginBottom: "8px",
              boxShadow: "0 1px 2px rgba(0,0,0,0.06)",
              borderLeft: `3px solid ${STAGE_COLORS[entry.generation_stage] ?? "#ccc"}`,
            }}
          >
            {/* Header row: timestamp + stage badge */}
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginBottom: "6px",
              }}
            >
              <span style={{ fontSize: "0.75rem", color: "#888" }}>
                {formatTime(entry.timestamp)}
              </span>
              <span
                style={{
                  fontSize: "0.625rem",
                  fontWeight: 600,
                  padding: "2px 8px",
                  borderRadius: "9999px",
                  background: STAGE_COLORS[entry.generation_stage] ?? "#ccc",
                  color: "#fff",
                }}
              >
                {STAGE_LABELS[entry.generation_stage] ?? `Stage ${entry.generation_stage}`}
              </span>
            </div>

            {/* Text */}
            <div
              style={{
                fontSize: "1rem",
                lineHeight: 1.5,
                color: entry.was_spoken ? "#333" : "#999",
                fontStyle: entry.was_spoken ? "normal" : "italic",
              }}
            >
              {entry.text}
              {!entry.was_spoken && (
                <span
                  style={{
                    fontSize: "0.75rem",
                    marginLeft: "6px",
                    opacity: 0.6,
                  }}
                >
                  (未発声)
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function formatTime(ts: string): string {
  try {
    const date = new Date(ts);
    return date.toLocaleTimeString("ja-JP", {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    });
  } catch {
    return ts;
  }
}

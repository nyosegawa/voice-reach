import { useState } from "react";
import { useAppStore } from "../stores/appStore";

const HIRAGANA_GROUPS = [
  { label: "あ行", chars: ["あ", "い", "う", "え", "お"] },
  { label: "か行", chars: ["か", "き", "く", "け", "こ"] },
  { label: "さ行", chars: ["さ", "し", "す", "せ", "そ"] },
  { label: "た行", chars: ["た", "ち", "つ", "て", "と"] },
  { label: "な行", chars: ["な", "に", "ぬ", "ね", "の"] },
  { label: "は行", chars: ["は", "ひ", "ふ", "へ", "ほ"] },
  { label: "ま行", chars: ["ま", "み", "む", "め", "も"] },
  { label: "や行", chars: ["や", "ゆ", "よ", "っ", "ん"] },
  { label: "ら行", chars: ["ら", "り", "る", "れ", "ろ"] },
  { label: "わ行", chars: ["わ", "を", "ー", "゛", "゜"] },
];

export function HiraganaInput() {
  const [selectedGroup, setSelectedGroup] = useState<number | null>(null);
  const [inputText, setInputText] = useState("");
  const gazeZone = useAppStore((s) => s.gazeZone);

  if (selectedGroup === null) {
    // Stroke 1: group selection
    return (
      <div style={{ position: "absolute", inset: 0, padding: "64px" }}>
        <div style={{ textAlign: "center", fontSize: "1.5rem", marginBottom: "24px" }}>
          {inputText || "文字を入力"}
        </div>
        <div style={{
          display: "grid",
          gridTemplateColumns: "repeat(5, 1fr)",
          gridTemplateRows: "repeat(2, 1fr)",
          gap: "12px",
          height: "calc(100% - 80px)",
        }}>
          {HIRAGANA_GROUPS.map((group, i) => (
            <div
              key={i}
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                borderRadius: "12px",
                background: gazeZone === i ? "#2563eb" : "rgba(255, 255, 255, 0.1)",
                border: gazeZone === i ? "3px solid #60a5fa" : "2px solid rgba(255, 255, 255, 0.2)",
                fontSize: "2rem",
                transition: "all 0.15s ease-out",
              }}
            >
              {group.label}
            </div>
          ))}
        </div>
      </div>
    );
  }

  // Stroke 2: character selection within group
  const group = HIRAGANA_GROUPS[selectedGroup];
  return (
    <div style={{ position: "absolute", inset: 0, padding: "64px" }}>
      <div style={{ textAlign: "center", fontSize: "1.5rem", marginBottom: "24px" }}>
        {inputText || "文字を入力"} | {group.label}
      </div>
      <div style={{
        display: "flex",
        gap: "16px",
        justifyContent: "center",
        alignItems: "center",
        height: "calc(100% - 80px)",
      }}>
        {group.chars.map((char, i) => (
          <div
            key={i}
            style={{
              width: "120px",
              height: "120px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              borderRadius: "16px",
              background: gazeZone === i ? "#2563eb" : "rgba(255, 255, 255, 0.1)",
              border: gazeZone === i ? "3px solid #60a5fa" : "2px solid rgba(255, 255, 255, 0.2)",
              fontSize: "3rem",
              transition: "all 0.15s ease-out",
            }}
          >
            {char}
          </div>
        ))}
      </div>
    </div>
  );
}

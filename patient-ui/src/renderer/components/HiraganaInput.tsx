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
      <div className="hiragana-input">
        <div className="hiragana-input__display">
          {inputText || "文字を入力"}
        </div>
        <div className="hiragana-input__grid">
          {HIRAGANA_GROUPS.map((group, i) => (
            <div
              key={i}
              className={`hiragana-input__key ${gazeZone === i ? 'hiragana-input__key--gazed' : ''}`}
              onClick={() => setSelectedGroup(i)}
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
    <div className="hiragana-input">
      <div className="hiragana-input__display">
        {inputText || "文字を入力"} | {group.label}
      </div>
      <div className="hiragana-input__char-row">
        {group.chars.map((char, i) => (
          <div
            key={i}
            className={`hiragana-input__char-key ${gazeZone === i ? 'hiragana-input__char-key--gazed' : ''}`}
            onClick={() => {
              setInputText((prev) => prev + char);
              setSelectedGroup(null);
            }}
          >
            {char}
          </div>
        ))}
      </div>
    </div>
  );
}

import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./styles/global.css";
import "./styles/bubble.css";
import "./styles/emergency.css";
import "./styles/calibration.css";
import "./styles/status-bar.css";
import "./styles/conversation-log.css";
import "./styles/hiragana-input.css";
import "./styles/gaze-debug.css";
import { App } from "./App";

const root = document.getElementById("root");
if (root) {
  createRoot(root).render(
    <StrictMode>
      <App />
    </StrictMode>
  );
}

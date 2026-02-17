# VoiceReach Research

VoiceReach実装に向けた体系的な技術調査。先行研究・OSS・商用製品・最新モデルを網羅的に調査し、技術選定の根拠を確立する。

## ディレクトリ構成

```
research/
├── RESEARCH_PLAN.md       ← 調査方針・方法論・スケジュール
├── REPORT_TEMPLATE.md     ← レポート標準テンプレート
├── phase_a/               ← 先行研究・既存手法
├── phase_b/               ← 最新モデル・デバイス
└── scripts/               ← ベンチマーク・データ収集スクリプト
```

## 調査エリア一覧

### Phase A: 先行研究・既存手法

| コード | テーマ | 優先度 | ステータス | 関連設計書 |
|--------|--------|--------|-----------|-----------|
| [A1](phase_a/a1_eye_gaze_tracking/report.md) | 視線推定 | HIGH | Not Started | `docs/02_EYE_TRACKING_AND_INPUT.md` |
| [A2](phase_a/a2_aac_communication_systems/report.md) | AAC意思伝達装置 | HIGH | Not Started | `docs/00_PROJECT_OVERVIEW.md` |
| [A3](phase_a/a3_llm_for_aac/report.md) | LLM × AAC | HIGH | Not Started | `docs/04_AI_CANDIDATE_GENERATION.md` |
| [A4](phase_a/a4_voice_preservation_synthesis/report.md) | 音声保存・合成 | CRITICAL | Not Started | `docs/08_VOICE_PRESERVATION.md` |
| [A5](phase_a/a5_emotion_detection/report.md) | 感情検出 | MEDIUM | Not Started | `docs/05_EMOTION_AND_CONTEXT.md` |
| [A6](phase_a/a6_finger_pressure_input/report.md) | 指・圧力入力 | MEDIUM | Not Started | `docs/02_EYE_TRACKING_AND_INPUT.md` |
| [A7](phase_a/a7_personal_voice_profile_nlp/report.md) | PVP / NLP | MEDIUM-HIGH | Not Started | `docs/03_PERSONAL_VOICE_PROFILE.md` |

### Phase B: 最新モデル・デバイス

| コード | テーマ | 優先度 | ステータス | 関連設計書 |
|--------|--------|--------|-----------|-----------|
| [B1](phase_b/b1_local_llms/report.md) | ローカルLLM | HIGH | Not Started | `docs/01_SYSTEM_ARCHITECTURE.md` |
| [B2](phase_b/b2_cloud_llms/report.md) | クラウドLLM | HIGH | Not Started | `docs/04_AI_CANDIDATE_GENERATION.md` |
| [B3](phase_b/b3_voice_synthesis_models/report.md) | 音声合成モデル | CRITICAL | Not Started | `docs/08_VOICE_PRESERVATION.md` |
| [B4](phase_b/b4_vision_gaze_models/report.md) | 視線推定モデル | HIGH | Not Started | `docs/02_EYE_TRACKING_AND_INPUT.md` |
| [B5](phase_b/b5_vlm_models/report.md) | VLM | MEDIUM | Not Started | `docs/05_EMOTION_AND_CONTEXT.md` |
| [B6](phase_b/b6_edge_devices/report.md) | エッジデバイス | MEDIUM | Not Started | `docs/01_SYSTEM_ARCHITECTURE.md` |
| [B7](phase_b/b7_input_devices/report.md) | 入力デバイス | LOW-MEDIUM | Not Started | `docs/02_EYE_TRACKING_AND_INPUT.md` |

## 調査実行順序

```
Tier 1 (即時):  A4 → B3 → A1 → B4 → A2    ← Phase 0・MVP設計をブロック
Tier 2 (早期):  A3 → B1 → B2 → A6          ← MVP実装に必要
Tier 3 (中期):  A7 → A5 → B5 → B6          ← Phase 2機能
Tier 4 (後期):  B7                           ← Phase 3+
```

## スクリプト

ベンチマーク・データ収集スクリプトは [`scripts/`](scripts/README.md) を参照。

```bash
cd research/scripts
pip install -r requirements.txt
```

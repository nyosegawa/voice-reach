# Research Scripts

VoiceReach調査用のベンチマーク・データ収集スクリプト。

## セットアップ

```bash
cd research/scripts
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## ディレクトリ構成

| ディレクトリ | 用途 |
|-------------|------|
| `gaze_estimation/` | MediaPipe・視線推定CNNの精度・レイテンシ計測 |
| `llm_benchmark/` | LLM候補生成の品質・レイテンシ評価 |
| `voice_synthesis/` | TTS品質評価・ボイスクローンテスト |
| `emotion_detection/` | rPPG精度・ランドマークドリフト分析 |
| `input_devices/` | ピエゾセンサ波形分析・USB HIDレイテンシ |
| `utils/` | 論文収集・GitHub OSS調査等の共通ユーティリティ |

## 命名規則

- スクリプト: `snake_case.py`（目的が明確にわかる名前）
- ベンチマーク結果: 各調査レポートの appendix に記載
- 生データ: `.gitignore` で除外（`**/output/` ディレクトリ）

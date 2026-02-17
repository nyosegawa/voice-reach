# 音声合成モデル -- 調査レポート

## Meta

- **エリア**: Phase B - B3
- **担当**:
- **日付**:
- **ステータス**: Not Started
- **関連設計書**: `docs/08_VOICE_PRESERVATION.md`

## 1. リサーチクエスチョン

- [ ] Q1: 2025-2026年のゼロショット声質クローニングのSoTA
- [ ] Q2: 日本語声質クローニング品質が最も高いモデルはどれか
- [ ] Q3: コンシューマHWでリアルタイム合成 + 感情/トーン制御が可能なモデルは
- [ ] Q4: 30-60分の録音から得られるクローン音声のMOSスコアの期待値
- [ ] Q5: 最新モデル比較: Fish Speech, CosyVoice, F5-TTS, ChatTTS, Parler-TTS, MeloTTS, GPT-SoVITS

## 2. 背景・動機

Phase 0の録音プロトコル設計には、ターゲットとするTTSモデルの要件（必要データ量、サンプリングレート、音素カバレッジ等）を事前に把握する必要がある。また、日本語の声質クローニング品質は英語に比べて情報が少なく、最新モデルの実測評価が重要。

## 3. 調査方法

- **検索キーワード（英語）**: zero-shot voice cloning 2025 2026, text-to-speech state of art, emotion controllable TTS, Japanese voice synthesis, voice cloning minimal data
- **検索キーワード（日本語）**: ゼロショット音声合成, 声質クローニング 最新, 日本語 TTS, 感情制御 音声合成
- **調査対象モデル**: Fish Speech, CosyVoice, F5-TTS, ChatTTS, Parler-TTS, MeloTTS, GPT-SoVITS, XTTS v2, StyleTTS 2, Bark, VITS, VoiceCraft
- **ベンチマーク**: `scripts/voice_synthesis/tts_quality_eval.py`, `scripts/voice_synthesis/clone_voice_test.py`

## 4. 学術文献レビュー

### 4.1 英語文献

| 論文 | 著者 | 年 | 会議/誌 | 要旨 | VoiceReachへの示唆 |
|------|------|---|---------|------|-------------------|

### 4.2 日本語文献

| 論文 | 著者 | 年 | 会議/誌 | 要旨 | VoiceReachへの示唆 |
|------|------|---|---------|------|-------------------|

### 4.3 主要知見サマリ

## 5. オープンソースソフトウェア調査

| 名前 | URL | Stars | License | 言語 | 主な特徴 | VoiceReach適合性 | 最終更新 |
|------|-----|-------|---------|------|---------|-----------------|---------|

## 6. 商用製品・サービス

| 名前 | 企業 | 価格帯 | 主な特徴 | ALS適合性 | 日本市場 |
|------|------|--------|---------|----------|---------|

## 7. 比較分析

## 8. VoiceReachへの推奨事項

## 9. 未解決の問題・今後の調査

## 10. 参考文献

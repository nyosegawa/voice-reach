# 音声保存・合成 -- 調査レポート

## Meta

- **エリア**: Phase A - A4
- **担当**:
- **日付**:
- **ステータス**: Not Started
- **関連設計書**: `docs/08_VOICE_PRESERVATION.md`

## 1. リサーチクエスチョン

- [ ] Q1: 1時間未満のデータでのゼロショット声質クローニングのSoTA品質
- [ ] Q2: XTTS v2, StyleTTS 2, VALL-E X, Coqui TTSの日本語品質比較
- [ ] Q3: 世界・日本における音声バンキングプログラムの実施状況と録音プロトコル
- [ ] Q4: クローン音声における感情・トーン制御の実現手法
- [ ] Q5: 最低限必要な録音品質（サンプリングレート、ビット深度、SNR）と量

## 2. 背景・動機

音声保存はVoiceReachで最も時間的制約が厳しい領域。ALS診断後、構音障害が進行する前に患者の声を記録する必要がある。Phase 0で即座に録音プロトコルを提供するため、どのTTSモデルをターゲットにすべきか、最低限何を録音すべきかの知見が急務。

## 3. 調査方法

- **検索キーワード（英語）**: zero-shot voice cloning, voice banking ALS, voice preservation neurodegenerative, TTS minimal data, emotion controllable TTS, Japanese voice cloning
- **検索キーワード（日本語）**: 声質クローニング, 音声バンキング, ALS 音声保存, 音声合成 少量データ, 感情制御 TTS
- **調査対象OSS**: Coqui TTS (XTTS v2), StyleTTS 2, Bark, Tortoise TTS, VITS, Fish Speech, GPT-SoVITS, F5-TTS, CosyVoice
- **調査対象プログラム**: ModelTalker, Speech Ark, VocaliD, Team Gleason Voice Banking, 国立障害者リハビリテーションセンター

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

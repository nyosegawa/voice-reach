# クラウドLLM -- 調査レポート

## Meta

- **エリア**: Phase B - B2
- **担当**:
- **日付**:
- **ステータス**: Not Started
- **関連設計書**: `docs/04_AI_CANDIDATE_GENERATION.md`, `docs/01_SYSTEM_ARCHITECTURE.md`

## 1. リサーチクエスチョン

- [ ] Q1: Claude, GPT-4o, GeminiのAAC候補生成品質比較（PVP + context付き）
- [ ] Q2: 各プロバイダのEnd-to-endレイテンシ（API + ネットワーク）
- [ ] Q3: Intent-axis diversity指示への各モデルの追従性
- [ ] Q4: 1日あたりのコスト推計（推定50-100 API calls/day）
- [ ] Q5: ストリーミング出力による段階的表示のサポート状況

## 2. 背景・動機

VoiceReachの2段階推論のStage 2として、クラウドLLMが1-2秒で高品質候補を生成する。MVP段階ではクラウドLLMが主要な候補生成エンジンとなるため、プロバイダ選定とプロンプト最適化が重要。

## 3. 調査方法

- **調査対象**: Claude (Anthropic), GPT-4o/4o-mini (OpenAI), Gemini Pro/Flash (Google), Command R+ (Cohere)
- **評価軸**: 日本語品質, レイテンシ, コスト, intent diversity追従性, ストリーミングサポート
- **ベンチマーク**: `scripts/llm_benchmark/aac_generation_eval.py`, `scripts/llm_benchmark/prompt_comparison.py`

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

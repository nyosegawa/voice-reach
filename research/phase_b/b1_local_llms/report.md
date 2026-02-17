# ローカルLLM -- 調査レポート

## Meta

- **エリア**: Phase B - B1
- **担当**:
- **日付**:
- **ステータス**: Not Started
- **関連設計書**: `docs/01_SYSTEM_ARCHITECTURE.md`, `docs/07_SAFETY_AND_EMERGENCY.md`

## 1. リサーチクエスチョン

- [ ] Q1: コンシューマHW（Apple Silicon M1-M4, Intel 12世代+）で4候補応答を200ms以内に生成可能なモデルは
- [ ] Q2: Phi-3/4, Llama 3/3.1/3.2, Gemma 2/3, Qwen 2.5の日本語品質比較
- [ ] Q3: 量子化レベル（GGUF Q4/Q5/Q8）で日本語品質はどの程度維持されるか
- [ ] Q4: 1B-3Bモデルは複雑なシステムプロンプト（PVP + context + intent axis）に追従できるか
- [ ] Q5: 推論FW（llama.cpp, MLX, ONNX Runtime, MLC-LLM）のプラットフォーム別最適解

## 2. 背景・動機

VoiceReachの2段階推論アーキテクチャでは、Stage 1としてローカルLLMが~200msで4候補を生成する。オフライン動作（70%機能維持）の要件もあり、ローカル推論の実現可能性検証が不可欠。

## 3. 調査方法

- **検索キーワード（英語）**: small language model, on-device LLM, edge inference, Japanese LLM benchmark, quantized LLM quality
- **検索キーワード（日本語）**: 軽量LLM, オンデバイス推論, 日本語LLM ベンチマーク, 量子化 品質
- **ベンチマーク**: `scripts/llm_benchmark/local_llm_latency.py`, `scripts/llm_benchmark/aac_generation_eval.py`

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

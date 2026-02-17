# 視線推定（Eye/Gaze Tracking） -- 調査レポート

## Meta

- **エリア**: Phase A - A1
- **担当**:
- **日付**:
- **ステータス**: Not Started
- **関連設計書**: `docs/02_EYE_TRACKING_AND_INPUT.md`, `docs/01_SYSTEM_ARCHITECTURE.md`

## 1. リサーチクエスチョン

- [ ] Q1: Webcamベース視線推定でMediaPipe + 軽量CNNはどの程度の角度精度を達成可能か（Tobii IR方式との比較）
- [ ] Q2: Zone-based入力（2-5度精度で十分）に最適なappearance-based CNN構造はどれか
- [ ] Q3: OSS視線推定（L2CS-Net, RT-GENE, ETH-XGaze, GazeML, OpenFace 2.0）の精度・レイテンシ比較
- [ ] Q4: ALS患者（頭部動作制限あり・ベッド上）向けキャリブレーション手法の先行研究
- [ ] Q5: 低照度環境での性能と対策（近赤外LED補助等）

## 2. 背景・動機

VoiceReachはTobii等の高額IRアイトラッカーに依存せず、標準Webcam（~$50）のみで視線推定を実現する。MediaPipe Face Meshで468点ランドマークを取得し、64x64目領域パッチからappearance-based CNN（~500Kパラメータ、~5ms推論）で画面座標を推定する設計。Zone-based（4-16分割）のため、ピクセル精度は不要だが2-5度精度は必要。

## 3. 調査方法

- **検索キーワード（英語）**: webcam gaze estimation, appearance-based gaze CNN, eye tracking calibration ALS, zone-based gaze input, low-light gaze estimation, L2CS-Net, RT-GENE, ETH-XGaze
- **検索キーワード（日本語）**: 視線推定, ウェブカメラ 視線, 外観ベース視線推定, 視線入力 ALS, ゾーンベース視線
- **調査対象OSS**: MediaPipe Face Mesh, L2CS-Net, RT-GENE, GazeML, OpenFace 2.0, Pupil Labs, EyeTrackKit
- **調査対象製品**: Tobii Eye Tracker 5, Tobii Pro Spark, EyeTech TM5, Irisbond Duo
- **ベンチマーク**: `scripts/gaze_estimation/`

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

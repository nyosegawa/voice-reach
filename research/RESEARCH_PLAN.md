# VoiceReach 調査方針

## 目的

VoiceReach実装の技術選定を裏付けるため、先行研究・OSS・商用製品・最新モデルを体系的に調査する。各調査レポートは `REPORT_TEMPLATE.md` に従い、具体的な推奨事項と根拠を提示する。

---

## Phase A: 先行研究・既存手法

### A1: 視線推定（Eye/Gaze Tracking）

**優先度**: HIGH（MVP直結）
**関連設計書**: `docs/02_EYE_TRACKING_AND_INPUT.md`, `docs/01_SYSTEM_ARCHITECTURE.md`

**リサーチクエスチョン**:
1. Webcamベース視線推定でMediaPipe + 軽量CNNはどの程度の角度精度を達成可能か（Tobii IR方式との比較）
2. Zone-based入力（2-5度精度で十分）に最適なappearance-based CNN構造はどれか
3. OSS視線推定（L2CS-Net, RT-GENE, ETH-XGaze, GazeML, OpenFace 2.0）の精度・レイテンシ比較
4. ALS患者（頭部動作制限あり・ベッド上）向けキャリブレーション手法の先行研究
5. 低照度環境での性能と対策（近赤外LED補助等）

**検索キーワード**:
- EN: webcam gaze estimation, appearance-based gaze CNN, eye tracking calibration ALS, zone-based gaze input, low-light gaze estimation
- JP: 視線推定, ウェブカメラ 視線, 外観ベース視線推定, 視線入力 ALS, ゾーンベース視線

**調査対象OSS**: MediaPipe Face Mesh, L2CS-Net, RT-GENE, GazeML, OpenFace 2.0, Pupil Labs, EyeTrackKit
**調査対象製品**: Tobii Eye Tracker 5, Tobii Pro Spark, EyeTech TM5, Irisbond Duo
**ベンチマーク**: `scripts/gaze_estimation/`

---

### A2: AAC意思伝達装置

**優先度**: HIGH（競合理解）
**関連設計書**: `docs/00_PROJECT_OVERVIEW.md`, `docs/10_PROGRESSIVE_ADAPTATION.md`

**リサーチクエスチョン**:
1. ALS患者向け既存AAC機器の現状と具体的な課題（通信速度WPM、疲労、コスト）
2. 視線追跡型AAC（Tobii Dynavox I-Series, Grid 3, Smartbox）のdwell-click疲労問題への対処法
3. Dwell-click代替手法（smooth pursuit, gaze gesture, 2段階確認）の学術的検証状況
4. 日本市場のAAC機器（伝の心, レッツチャット, ミヤスク, OriHime eye）の機能・価格・普及状況
5. 既存AAC利用者のコミュニケーション速度と満足度データ

**検索キーワード**:
- EN: AAC ALS, eye tracking communication, augmentative alternative communication, dwell click alternative, gaze gesture input
- JP: 意思伝達装置, ALS コミュニケーション, 視線入力, 代替コミュニケーション, 重度障害者 AAC

**調査対象製品**: Tobii Dynavox (PCEye 5, I-Series), Grid 3, Snap + Core First, 伝の心, レッツチャット, OriHime eye, ミヤスクEZ
**調査対象団体**: ALS Association, 日本ALS協会, Communication Matters, RESNA

---

### A3: LLM × AAC（候補生成）

**優先度**: HIGH（コア機能）
**関連設計書**: `docs/04_AI_CANDIDATE_GENERATION.md`, `docs/03_PERSONAL_VOICE_PROFILE.md`

**リサーチクエスチョン**:
1. LLMをAAC候補テキスト生成に適用した先行研究の存在と結果
2. In-Context Learning（ICL）による個人文体再現の有効性と限界
3. Intent-diverse generation（意図軸多様性）を実現するプロンプト戦略
4. 会話コンテキストからの応答予測（conversational response prediction）のSoTA
5. Few-shot例がパーソナライゼーション品質に与える影響の定量的知見

**検索キーワード**:
- EN: LLM text prediction AAC, conversational response generation, intent diverse generation, personalized language model, persona-based dialogue
- JP: LLM 予測入力, AAC テキスト予測, 意図多様性生成, ペルソナ対話

**調査対象学会**: ACL, CHI, ASSETS, EMNLP
**ベンチマーク**: `scripts/llm_benchmark/`

---

### A4: 音声保存・合成

**優先度**: CRITICAL（Phase 0直結、時間的制約あり）
**関連設計書**: `docs/08_VOICE_PRESERVATION.md`

**リサーチクエスチョン**:
1. 1時間未満のデータでのゼロショット声質クローニングのSoTA品質
2. XTTS v2, StyleTTS 2, VALL-E X, Coqui TTSの日本語品質比較
3. 世界・日本における音声バンキングプログラムの実施状況と録音プロトコル
4. クローン音声における感情・トーン制御の実現手法
5. 最低限必要な録音品質（サンプリングレート、ビット深度、SNR）と量

**検索キーワード**:
- EN: zero-shot voice cloning, voice banking ALS, voice preservation neurodegenerative, TTS minimal data, emotion controllable TTS
- JP: 声質クローニング, 音声バンキング, ALS 音声保存, 音声合成 少量データ, 感情制御 TTS

**調査対象OSS**: Coqui TTS (XTTS v2), StyleTTS 2, Bark, Tortoise TTS, VITS, Fish Speech, GPT-SoVITS
**調査対象プログラム**: ModelTalker, Speech Ark, VocaliD, Team Gleason Voice Banking, 国立障害者リハビリテーションセンター
**ベンチマーク**: `scripts/voice_synthesis/`

---

### A5: 感情検出

**優先度**: MEDIUM（Phase 2だが新規性高く早期検証が望ましい）
**関連設計書**: `docs/05_EMOTION_AND_CONTEXT.md`, `docs/10_PROGRESSIVE_ADAPTATION.md`

**リサーチクエスチョン**:
1. 標準FERモデルはALS患者（顔面筋制限）でも有用なシグナルを検出できるか
2. Webcamによるrpg（遠隔光電容積脈波）の心拍推定精度と感情覚醒検出への応用可能性
3. ALS/麻痺患者の感情検出に特化した研究の有無
4. ベースライン相対アプローチ（個人偏差）vs絶対FER分類の有効性
5. 眼球シグナル（瞳孔径、瞬目パターン、注視安定性）の感情指標としての検証状況

**検索キーワード**:
- EN: facial expression recognition disabled, rPPG emotion detection, pupil dilation emotion, ALS emotion, eye movement affect
- JP: 表情認識 障害者, rPPG 感情, 瞳孔 感情検出, ALS 感情, 自律神経 カメラ計測

**調査対象OSS**: pyVHR, HeartCV, rPPG-Toolbox, HSEmotion, POSTER, DAN
**ベンチマーク**: `scripts/emotion_detection/`

---

### A6: 指・圧力入力

**優先度**: MEDIUM（MVPに必要だが技術的リスクは低い）
**関連設計書**: `docs/02_EYE_TRACKING_AND_INPUT.md`

**リサーチクエスチョン**:
1. ALS患者向けピエゾセンサの市販構成と実績
2. 運動障害者向け微小動作入力デバイスのSoTA
3. 不随意運動（線維束攣縮）と意図的操作を区別するフィルタリング手法
4. カスタム圧力センサのUSB HID実装事例
5. 既存ALSスイッチデバイスのVoiceReachへの転用可能性

**検索キーワード**:
- EN: pressure sensor switch access AAC, piezoelectric input ALS, involuntary movement filter, minimal movement input device
- JP: ピエゾスイッチ 入力, ALS 入力デバイス, 不随意運動 フィルタリング, 福祉スイッチ

**調査対象製品**: AbleNet (Specs Switch, Micro Light), Origin Instruments (Sip/Puff), Tecla, パシフィックサプライ, テクノツール
**調査対象HW**: Arduino/RPi ピエゾ入力、QMK firmware

---

### A7: パーソナルボイスプロファイル（NLP）

**優先度**: MEDIUM-HIGH（Phase 2機能だが、データ収集戦略に影響）
**関連設計書**: `docs/03_PERSONAL_VOICE_PROFILE.md`

**リサーチクエスチョン**:
1. テキストコーパスから文体・語彙傾向・コミュニケーションパターンを抽出するNLP技術
2. Author profiling / stylometryの精度と個人の「声」捕捉能力
3. LLMによる非構造化テキストからの構造化パーソナリティプロファイル抽出の実現可能性
4. 信頼性あるプロファイル構築に必要な最低テキスト量
5. 日本語特有の言語特徴（終助詞、敬語、方言）のスタイル分析への影響

**検索キーワード**:
- EN: author profiling, computational stylometry, writing style extraction, personality detection text, persona extraction dialogue
- JP: 著者推定, 文体解析, 言語指紋, パーソナライズ対話, 日本語スタイル変換

**調査対象ツール**: Stylo (R), LIWC, spaCy + GiNZA, PAN shared tasks (CLEF)
**調査対象研究**: PersonaChat, LIGHT, StyleTransfer in NLP

---

## Phase B: 最新モデル・デバイス

### B1: ローカルLLM

**優先度**: HIGH（200msレイテンシ目標の実現可能性検証）
**関連設計書**: `docs/01_SYSTEM_ARCHITECTURE.md`

**リサーチクエスチョン**:
1. コンシューマHW（Apple Silicon M1-M4, Intel 12世代+）で4候補応答を200ms以内に生成可能なモデルは
2. Phi-3/4, Llama 3/3.1/3.2, Gemma 2/3, Qwen 2.5のJapanese品質比較
3. 量子化レベル（GGUF Q4/Q5/Q8）でJapanese品質はどの程度維持されるか
4. 1B-3Bモデルは複雑なシステムプロンプト（PVP + context + intent axis）に追従できるか
5. 推論FW（llama.cpp, MLX, ONNX Runtime, MLC-LLM）のプラットフォーム別最適解

**ベンチマーク**: `scripts/llm_benchmark/local_llm_latency.py`, `scripts/llm_benchmark/aac_generation_eval.py`

---

### B2: クラウドLLM

**優先度**: HIGH（MVP直結）
**関連設計書**: `docs/04_AI_CANDIDATE_GENERATION.md`

**リサーチクエスチョン**:
1. Claude, GPT-4o, GeminiのAAC候補生成品質比較（PVP + context付き）
2. 各プロバイダのEnd-to-endレイテンシ（API + ネットワーク）
3. Intent-axis diversity指示への各モデルの追従性
4. 1日あたりのコスト推計（推定50-100 API calls/day）
5. ストリーミング出力による段階的表示のサポート状況

**ベンチマーク**: `scripts/llm_benchmark/aac_generation_eval.py`, `scripts/llm_benchmark/prompt_comparison.py`

---

### B3: 音声合成モデル

**優先度**: CRITICAL（Phase 0録音プロトコル設計に直結）
**関連設計書**: `docs/08_VOICE_PRESERVATION.md`

**リサーチクエスチョン**:
1. 2025-2026年のゼロショット声質クローニングのSoTA
2. 日本語声質クローニング品質が最も高いモデルはどれか
3. コンシューマHWでリアルタイム合成+感情/トーン制御が可能なモデルは
4. 30-60分の録音から得られるクローン音声のMOSスコアの期待値
5. 最新モデル比較: Fish Speech, CosyVoice, F5-TTS, ChatTTS, Parler-TTS, MeloTTS, GPT-SoVITS

**ベンチマーク**: `scripts/voice_synthesis/tts_quality_eval.py`, `scripts/voice_synthesis/clone_voice_test.py`

---

### B4: 視線推定モデル

**優先度**: HIGH（MVP直結）
**関連設計書**: `docs/02_EYE_TRACKING_AND_INPUT.md`

**リサーチクエスチョン**:
1. L2CS-Net, GazeTR, GazeOnce以降の最新webcam視線推定モデル
2. Transformer系視線推定モデルはCNNアプローチを上回るか
3. MediaPipe代替のface mesh / landmark検出手段
4. Webcamのみでsub-2度精度を達成可能なモデルはあるか

**ベンチマーク**: `scripts/gaze_estimation/`

---

### B5: VLM（Vision-Language Model）

**優先度**: MEDIUM（Phase 2機能）
**関連設計書**: `docs/05_EMOTION_AND_CONTEXT.md`

**リサーチクエスチョン**:
1. GPT-4V, Claude Vision, Gemini Vision, LLaVA等のベッドサイドカメラ画像からの場面記述能力
2. プライバシー保護のためのローカルVLMの実用性
3. VoiceReach設計書に記載されたシナリオ（人物認識、物体検出、イベント検出）での性能
4. クラウドVLMのコスト・レイテンシ推計（イベント駆動10fps処理想定）

---

### B6: エッジデバイス

**優先度**: MEDIUM（デプロイ計画に重要）
**関連設計書**: `docs/01_SYSTEM_ARCHITECTURE.md`, `docs/07_SAFETY_AND_EMERGENCY.md`

**リサーチクエスチョン**:
1. Apple Silicon Mac (M1-M4)でVoiceReach全スタック（視線推定 + ローカルLLM + TTS）の同時実行は可能か
2. NVIDIA Jetson (Orin Nano/NX)の性能エンベロープ
3. CPU-onlyでMVPは動作可能か、専用NPU/GPUは必須か
4. 各構成の消費電力・バッテリー寿命推計
5. Qualcomm Snapdragon X Elite / Intel Core Ultra NPU搭載PCの可能性

---

### B7: 入力デバイス

**優先度**: LOW-MEDIUM（Phase 3+）
**関連設計書**: `docs/02_EYE_TRACKING_AND_INPUT.md`, `docs/10_PROGRESSIVE_ADAPTATION.md`

**リサーチクエスチョン**:
1. ALS患者がアクセス可能な最新BCI（Brain-Computer Interface）技術
2. 2024-2026年に登場した新しい微小動作入力デバイス
3. 消費者向けEMGベース入力デバイスの現状
4. 革新的なSip-and-Puff / 呼気ベース入力システム

---

## 文献検索戦略

### データベース

| データベース | 用途 | URL |
|-------------|------|-----|
| arXiv | CS/EE プレプリント | arxiv.org |
| Google Scholar | 横断検索 | scholar.google.com |
| ACM DL | HCI (CHI, ASSETS, UIST) | dl.acm.org |
| IEEE Xplore | 信号処理・ロボティクス | ieeexplore.ieee.org |
| PubMed | ALS臨床研究 | pubmed.ncbi.nlm.nih.gov |
| Semantic Scholar | 引用グラフ探索 | semanticscholar.org |
| CiNii Research | 日本語学術論文 | cir.nii.ac.jp |
| J-STAGE | 日本語学会誌 | jstage.jst.go.jp |

### GitHub OSS調査基準

1. トピック別キーワードでGitHub検索
2. フィルタ: stars > 50, 2年以内に更新, ライセンスあり
3. 上位3-5候補をクローンして基本テスト実行
4. `scripts/utils/github_oss_scanner.py` で体系的に実施

### 商用製品調査

展示会カタログ（ATIA, CSUN, 国際福祉機器展/H.C.R.）、ALS協会ガイド、メーカーサイトから情報収集。可能であればデモ動画・トライアル利用。

---

## 横断的考慮事項

### 日本語対応

全調査エリアで以下を確認:
- 日本語サポート品質
- 日本語学習データの可用性
- 日本語固有の課題（形態素解析、敬語、かな漢字入力）
- 日本市場での入手性

### プライバシー

`docs/09_PRIVACY_AND_ETHICS.md` と照合し、各技術のプライバシー影響を評価。ローカル処理 vs クラウド処理の分類を明記。

### 4層アーキテクチャとの対応

各レポートで、調査技術がVoiceReachの4層アーキテクチャ（Sensing → Context → Intelligence → Presentation）のどこに位置するかを明記。

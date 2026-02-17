# B6 -- エッジデバイス調査レポート

**調査日**: 2026-02-17
**対象**: VoiceReachの全パイプライン（視線推定+LLM+TTS+VLM）を動作させるエッジデバイスの選定
**ステータス**: Draft

---

## 1. エグゼクティブサマリー

VoiceReachはローカルファースト設計で、70%以上の機能がオフライン動作する必要がある。主要パイプラインとして、視線推定（25fps+）、ローカルLLM推論（200ms以内で4候補生成）、TTS合成、VLM環境認識を同一デバイスで同時実行する。

**結論**: VoiceReachの推奨プラットフォームは**Apple Silicon Mac（Mac mini M4 Pro / M4）**である。MLXフレームワークの成熟度、ユニファイドメモリアーキテクチャ、静音性、macOSエコシステム、日本市場での入手性を総合的に評価した結果、他プラットフォームに対して明確な優位性がある。コスト帯別に3構成を提案し、NVIDIA Jetsonは将来的なポータブル版・量産版の選択肢として位置づける。

---

## 2. リサーチクエスチョンへの回答

### Q1: Apple Silicon上でのLLM・TTS・視線推定モデルの推論性能

#### Apple Silicon各世代の性能比較

| チップ | メモリ帯域幅 | GPU コア数 | Neural Engine | 統合メモリ | LLM推論 (Qwen3-1.7B Q4, MLX) | TDP |
|---|---|---|---|---|---|---|
| **M1** | 68.25 GB/s | 8 | 16コア | 8/16GB | ~120 tok/s | 15-39W |
| **M1 Pro** | 200 GB/s | 16 | 16コア | 16/32GB | ~180 tok/s | 30-58W |
| **M2** | 100 GB/s | 10 | 16コア | 8/16/24GB | ~150 tok/s | 15-39W |
| **M2 Pro** | 200 GB/s | 19 | 16コア | 16/32GB | ~200 tok/s | 30-58W |
| **M3** | 100 GB/s | 10 | 16コア | 8/16/24GB | ~160 tok/s | 15-36W |
| **M3 Pro** | 150 GB/s | 18 | 16コア | 18/36GB | ~210 tok/s | 30-55W |
| **M4** | 120 GB/s | 10 | 16コア | 16/24/32GB | ~200 tok/s | 15-40W |
| **M4 Pro** | 273 GB/s | 20 | 16コア | 24/48GB | ~320 tok/s | 40-80W |
| **M4 Max** | 546 GB/s | 40 | 16コア | 36/48/64/128GB | ~525 tok/s | 60-100W |
| **M5** (参考) | 153 GB/s (ベース) | - | 改良版 | - | M4比19-27%向上 | - |

**注記**: LLM推論速度はメモリ帯域幅にほぼ比例する（メモリバウンド処理）。上記はQwen3-1.7B Q4_K_Mでのトークン生成速度の概算値。

#### VoiceReach全パイプラインの同時実行性能 (M4 Pro, 24GB推定)

| タスク | 使用メモリ | GPU使用率 | 推論速度 | 要件との比較 |
|---|---|---|---|---|
| 視線推定 (MediaPipe + CNN) | ~0.5GB | ~10% (常時) | 30fps | 要件25fps: **合格** |
| ローカルLLM (Qwen3-1.7B Q4) | ~1.2GB | ~15% (バースト) | ~320 tok/s → 150tok/0.2秒 | 要件200ms: **合格** |
| TTS (VOICEVOX等) | ~0.5-1GB | ~10% (バースト) | リアルタイム以上 | **合格** |
| VLM (MiniCPM-V 4.0 Q4) | ~2.5GB | ~10-15% (断続) | ~45 tok/s | 5-10秒間隔: **合格** |
| OS + アプリ | ~4-6GB | - | - | - |
| **合計** | **~9-11GB** | **ピーク ~50%** | - | **24GBで余裕** |

#### MLXフレームワークの成熟度

MLXは2023年12月にAppleが公開し、2025年末時点で本番グレードの成熟度に到達している:

- **推論性能**: llama.cppと比較して同等以上のスループット。特にM4チップ以降で最適化が進み最速。
- **VLM対応**: MLX-VLMパッケージにより、LLaVA、Qwen-VL、MiniCPM-V等の主要VLMをネイティブサポート。
- **量子化**: Q4_K_M等のGGUF量子化に対応。精度と速度のバランスが良い。
- **サーバー機能**: vllm-mlxにより、OpenAI/Anthropic互換のAPIサーバーを提供。連続バッチングで21-87%高スループット。
- **ファインチューニング**: LoRA/QLoRAによるオンデバイスファインチューニングをサポート。
- **WWDC25**: Appleが公式セッション「Explore large language models on Apple silicon with MLX」を開催。エコシステムの拡大が加速中。
- **M5チップ最適化**: TTFT（Time-to-First-Token）が全モデルサイズで3倍以上高速化。14Bモデルで10秒未満、30B MoEで3秒未満。

**評価: MLXは本番利用に十分成熟。VoiceReachのメインフレームワークとして推奨。**

### Q2: NVIDIA Jetson Orin Nano/NXの性能とコスト

#### Jetson Orin Nano Super

| 項目 | 仕様 |
|---|---|
| AI性能 | 67 TOPS (Super Mode) |
| GPU | 1024 CUDA + 32 Tensor コア |
| CPU | 6コア Arm Cortex-A78AE (1.7GHz) |
| メモリ | 8GB LPDDR5 (102 GB/s) |
| ストレージ | NVMe SSD (別売) |
| 消費電力 | 7-25W (設定可能) |
| 価格 | $249 (開発キット) |
| フレームワーク | TensorRT-LLM, llama.cpp, Ollama, vLLM, MLC |

**LLM推論性能 (Jetson Orin Nano Super 8GB)**:
- Qwen2.5 7B (INT4): ~21.75 tok/s
- 1B-3Bモデル (INT4): ~28-55 tok/s
- **VoiceReachの200ms要件**: 3Bモデルで40 tok/sの場合、0.2秒で8トークン。4候補×3-5語 = 60-100トークンの生成には1.5-2.5秒。**200ms要件は満たせない。**

**VLM推論性能**:
- Qwen2.5-VL-3B: 動作可能（メモリ制約内）
- VILA 1.5-3B: 動作可能
- 8B以上のモデル: メモリ不足で動作不可

**結論**: Jetson Orin Nano SuperはVoiceReachの全パイプラインを1台で動かすには**メモリとLLM推論速度が不十分**。ただし、VLM専用ノード、またはTTS専用ノードとしての活用は検討可能。

#### Jetson Orin NX

| 項目 | 仕様 (Super Mode) |
|---|---|
| AI性能 | 最大157 TOPS (NX 16GB Super) |
| メモリ | 8GB / 16GB LPDDR5 |
| 消費電力 | 10-40W |
| 価格 | ~$400-600 (モジュール+キャリアボード) |

**VoiceReachへの適用性**:
- 16GBモデルであればQwen3-1.7B (Q4) + MiniCPM-V 4.0 (Q4) の同時ロードが可能（合計~3.7GB）
- ただしメモリ帯域幅(102 GB/s)がApple M4 Pro(273 GB/s)の約1/3であり、LLM推論速度で大きく劣る
- **価格対性能比でApple Silicon Macに劣る**

#### Jetson AGX Orin

| 項目 | 仕様 |
|---|---|
| AI性能 | 275 TOPS |
| メモリ | 32GB / 64GB LPDDR5 (204.8 GB/s) |
| 消費電力 | 15-60W |
| 価格 | $999-1999 |

AGX Orinは性能的にVoiceReach全パイプラインを動作可能だが、価格がMac mini M4 Pro（約20万円）と同等以上であり、macOSエコシステムの利便性を考慮するとApple Siliconを推奨。

### Q3: Intel/AMD NPU搭載PCのAI推論性能

#### Intel Core Ultra シリーズ

| チップ | NPU性能 | GPU (統合) | 対応フレームワーク | 備考 |
|---|---|---|---|---|
| Meteor Lake (Core Ultra 1xx) | 11 TOPS | Intel Arc (統合) | OpenVINO | NPUはLLM推論に不向き |
| Arrow Lake (Core Ultra 2xx) | ~13 TOPS | Intel Arc (統合) | OpenVINO | NPU性能微増 |
| Lunar Lake (Core Ultra 2xx V) | 40+ TOPS | Intel Arc (統合) | OpenVINO | 大幅改善。Meteor Lake比80%高速 |

**VoiceReachへの適用性**:
- OpenVINOでLLM推論をサポートするが、MLX/Apple Siliconと比較してエコシステムの成熟度が低い
- NPUは主に軽量推論タスク（背景除去、物体検出等）に最適化されており、LLMのトークン生成には不向き
- Intel Arc GPUでの推論はNVIDIA GPUに劣る
- **LLM中心のVoiceReachにはオーバーキル or アンダーパワー**: NPUだけではLLM推論に不十分、GPU性能もApple Silicon/NVIDIAに劣る

#### AMD Ryzen AI 300 シリーズ (Strix Point)

| チップ | NPU性能 (XDNA 2) | 特徴 | 備考 |
|---|---|---|---|
| Ryzen AI 9 HX 370 | 50 TOPS | 12コア Zen 5 + RDNA 3.5 | ノートPC向け最高峰 |
| Ryzen AI 9 365 | 50 TOPS | 10コア Zen 5 | コスト効率良好 |

- NPU性能はIntelを大きく上回る（50 TOPS vs 11-40 TOPS）
- XDNA 2は35x CPUより電力効率が高い
- ただし、NPU向けLLMフレームワークの成熟度がMLXに大きく劣る
- AMD ROCm (GPU向け) のLinuxサポートは改善しているが、WindowsでのLLM推論はまだ発展途上
- **結論: 将来的に有望だが、2026年現在ではApple Siliconの方が実用的**

### Q4: Raspberry Pi 5 + AI HAT等の低コストプラットフォーム

#### Raspberry Pi 5 + AI HAT+ 2 (Hailo-10H)

| 項目 | 仕様 |
|---|---|
| AI性能 | 40 TOPS (AI HAT+ 2, Hailo-10H) |
| CPU | Broadcom BCM2712 (Arm Cortex-A76 2.4GHz, 4コア) |
| メモリ | 4/8GB LPDDR4X |
| NPU専用メモリ | 8GB (AI HAT+ 2のオンボードRAM) |
| 消費電力 | Pi5本体 ~5-12W + AI HAT ~5-10W |
| 価格 | Pi5 8GB: ~$80 + AI HAT+ 2: $130 = **合計 ~$210** |
| LLM推論速度 | ~6.5 tok/s (AI HAT+ 2) |

**VoiceReachへの適用性**:
- LLM推論速度が致命的に遅い（6.5 tok/s → 4候補生成に10秒以上）
- **VoiceReachの200ms要件を満たすことは不可能**
- VLMの推論もメモリ制約で限定的
- **結論: VoiceReachのメインデバイスとしては不適。ただし、補助デバイス（カメラノード、センサーハブ）としての活用は検討可能**

#### Google Coral Edge TPU

| 項目 | 仕様 |
|---|---|
| AI性能 | 4 TOPS |
| 推論対象 | TensorFlow Lite モデル |
| 消費電力 | ~2W |
| 価格 | ~$60 (USB Accelerator) |

- 4 TOPSはVLM/LLM推論には全く不十分
- MobileNet V2で~400 FPS等、画像分類特化
- **VoiceReachには不適**（視線推定の前処理等、非常に限定的な用途のみ可能）

### Q5: ALS患者のベッドサイド設置条件

ALS患者のベッドサイドに設置するデバイスには、以下の要件がある:

#### 必須要件

| 要件 | 基準 | 理由 |
|---|---|---|
| **静音性** | 30dB以下 (ささやき声レベル) | 患者の睡眠妨害防止。人工呼吸器の音を超えない |
| **低発熱** | 表面温度45度C以下 | 患者の手が触れる可能性。火傷防止 |
| **コンパクトさ** | 30cm x 30cm x 10cm以下 | ベッドサイドのスペース制約 |
| **安定性** | 24/7連続稼働、年間99.5%以上 | 緊急通報機能の信頼性 |
| **停電対策** | UPS接続またはバッテリー内蔵 | 最低30分のバッテリー持続 |
| **清掃性** | 拭き取り消毒可能 | 医療環境の衛生要件 |

#### 各デバイスの適合性評価

| デバイス | 消費電力 | ファン騒音 | サイズ | 発熱 | ベッドサイド適合性 |
|---|---|---|---|---|---|
| **Mac mini M4** | 5-65W | ~20dB (ほぼ無音) | 12.7 x 12.7 x 5cm | 低 (表面温度低い) | **最適** |
| **Mac mini M4 Pro** | 10-80W | ~25-30dB (低負荷時ほぼ無音) | 12.7 x 12.7 x 5cm | 低-中 | **良好** |
| MacBook Air M4 | 5-30W | **ファンレス** | ノートPC | 低 | 良好 (バッテリー内蔵) |
| Jetson Orin Nano Super | 7-25W | 要外付けファン or ヒートシンク | 小型 (モジュール) | **高** (90度C到達例あり) | 要冷却対策 |
| Raspberry Pi 5 + AI HAT | 10-22W | 要ファン | 小型 | 中-高 | 要ケース設計 |
| Intel NUC (Core Ultra) | 15-65W | ~25-35dB | 小型PC | 中 | 要モデル選定 |

**Mac mini M4の特筆すべき点**:
- Jeff Geerlingの実測で「効率が驚異的」と評価。M3比32%の電力効率改善。
- 低負荷時(アイドル)の消費電力は5-8W程度。AIタスク実行中でも25-40W。
- ファン音は通常負荷でほぼ無音。高負荷時でも20-25dB（図書館レベル以下）。
- サイズ12.7cm角は手のひらサイズ。ベッドサイドの棚やモニターアームに設置可能。

### Q6: VoiceReach推奨ハードウェア構成（コスト帯別）

#### 構成A: エントリー構成（約5万円）

| コンポーネント | 製品 | 価格（税込参考） | 備考 |
|---|---|---|---|
| メインデバイス | **Mac mini M4 (16GB/256GB)** | ¥94,800 | M4チップ、16GB統合メモリ |
| 内向きカメラ | Webカメラ (1080p) | ~¥3,000 | Logicool C920等 |
| 外向きカメラ | Webカメラ (720p, 広角) | ~¥3,000 | 広角90度以上 |
| モニター | 既存モニター利用 | ¥0 | HDMI接続 |
| **合計** | | **~¥100,800** | |

**注**: 5万円台では新品Macの購入が困難。中古M1/M2 Mac mini（3-5万円）を活用すれば5万円台で構成可能だが、性能は制限される。最低実用構成として10万円を推奨。

**性能見積もり**:
- LLM (Qwen3-1.7B Q4): ~200 tok/s → 200ms要件を満たす
- VLM (Moondream 2B): 動作可能だが、MiniCPM-V 4.0は16GBでも可能（他タスクとの並行に注意）
- TTS: リアルタイム可能
- 視線推定: 30fps以上

**制約**: 16GBメモリは全パイプライン同時実行時にやや逼迫する可能性。VLMは軽量モデル（Moondream 2B）推奨。

#### 構成B: 推奨構成（約15万円）

| コンポーネント | 製品 | 価格（税込参考） | 備考 |
|---|---|---|---|
| メインデバイス | **Mac mini M4 (24GB/512GB)** | ¥124,800 | M4チップ、24GB統合メモリ |
| 内向きカメラ | Webカメラ (1080p, IR対応) | ~¥5,000 | 暗所でもIR視線追跡可能 |
| 外向きカメラ | 広角Webカメラ (720p) | ~¥3,000 | 90度以上の画角 |
| モニター | 15-17インチモニター | ~¥15,000 | 患者が見やすいサイズ |
| UPS | 小型UPS | ~¥8,000 | 30分以上のバッテリーバックアップ |
| **合計** | | **~¥155,800** | |

**性能見積もり**:
- LLM (Qwen3-1.7B Q4): ~200 tok/s → 200ms要件を余裕で満たす
- VLM (MiniCPM-V 4.0 Q4): ~45 tok/s → 5-10秒間隔のシーン記述に十分
- TTS: リアルタイム
- 視線推定: 30fps以上
- **全パイプライン同時実行で~11GBメモリ使用。24GBで十分な余裕**

#### 構成C: プレミアム構成（約25万円）

| コンポーネント | 製品 | 価格（税込参考） | 備考 |
|---|---|---|---|
| メインデバイス | **Mac mini M4 Pro (24GB/512GB)** | ¥218,800 | M4 Pro、24GB統合メモリ、273 GB/s帯域幅 |
| 内向きカメラ | 高品質Webカメラ (4K/1080p, IR) | ~¥8,000 | 瞳孔検出精度向上 |
| 外向きカメラ | 広角カメラ (1080p) | ~¥5,000 | 高解像度環境認識 |
| モニター | 21インチタッチモニター | ~¥25,000 | 介護者操作にも対応 |
| UPS | 中型UPS (1時間+) | ~¥15,000 | 長時間バックアップ |
| スピーカー | 高品質スピーカー | ~¥5,000 | TTS音声品質向上 |
| **合計** | | **~¥276,800** | |

**性能見積もり**:
- LLM (Qwen3-1.7B Q4): ~320 tok/s → 200ms要件を大幅に上回る
- VLM (MiniCPM-V 4.5 Q4 8B): ~25 tok/s → 高精度シーン理解
- TTS: リアルタイム（高品質モデルも可）
- 視線推定: 30fps以上
- **将来的に4B以上のLLMやより大きなVLMへの移行も可能**
- **M4 Proの高メモリ帯域幅(273 GB/s)により、全タスクのレイテンシが大幅改善**

#### 構成D: ポータブル/量産構成（参考）

| コンポーネント | 製品 | 価格（参考） | 備考 |
|---|---|---|---|
| メインデバイス | **NVIDIA Jetson Orin NX 16GB** | ~¥60,000-80,000 | 組込み向け。Linux |
| 筐体 | カスタム筐体 (ヒートシンク付き) | ~¥10,000 | ファンレス設計推奨 |
| カメラ | MIPI CSI-2カメラモジュール x2 | ~¥5,000 | 組込み向け小型カメラ |
| ディスプレイ | 組込みタッチディスプレイ | ~¥15,000 | 7-10インチ |
| バッテリー | リチウムイオンバッテリー | ~¥10,000 | 2-4時間駆動 |
| **合計** | | **~¥100,000-120,000** | |

**用途**: 外出用ポータブルデバイス、量産時の原価削減。ただし、LLM推論性能はApple Siliconに劣るため、クラウドフォールバックの利用頻度が高くなる。

---

## 3. 文献レビュー / 技術情報

### 3.1 主要論文・技術報告

| 論文/報告 | 著者/組織 | 年 | 要旨 | VoiceReachへの示唆 |
|---|---|---|---|---|
| Production-Grade Local LLM Inference on Apple Silicon | arXiv:2511.05502 | 2025 | MLX, llama.cpp, Ollama等の体系比較。MLXが最高スループット | VoiceReachのApple Silicon + MLX採用を支持 |
| Benchmarking On-Device ML on Apple Silicon with MLX | arXiv:2510.18921 | 2025 | M4 Maxで525 tok/s。Apple Silicon ML推論の定量評価 | M4 Proでも十分な性能が見込めることを確認 |
| Exploring LLMs with MLX and the Neural Accelerators in the M5 GPU | Apple ML Research | 2025 | M5でTTFT 3x改善。MLXの継続進化 | Apple Siliconの性能向上トレンドは今後も続く |
| Native LLM and MLLM Inference at Scale on Apple Silicon | arXiv:2601.19139 | 2026 | Apple Silicon上でのLLM/MLLM大規模推論の実現性 | VoiceReachの全パイプライン同時実行の理論的裏付け |
| NITRO: LLM Inference on Intel Laptop NPUs | arXiv:2412.11053 | 2024 | Intel NPU上でのLLM推論手法。性能はGPU推論に劣る | Intel NPUはVoiceReachのメイン推論には不十分 |
| Vision-Language Models for Edge Networks Survey | arXiv:2502.07855 | 2025 | エッジVLMの包括的サーベイ。圧縮技術の体系化 | エッジデバイスでのVLM最適化の指針 |

### 3.2 ベンダー技術ドキュメント

| ドキュメント | ベンダー | 内容 | VoiceReachへの示唆 |
|---|---|---|---|
| JetPack 6.2 Super Mode | NVIDIA | Orin Nano/NXの最大2x性能向上 | ソフトウェアアップデートで既存HWの性能改善 |
| OpenVINO 2025.0 | Intel | DeepSeek対応、NPU最適化 | Intel NPUの改善は継続中だがMLXに追いつかず |
| Mac mini Technical Specifications | Apple | M4/M4 Pro仕様。最大65-80W | ベッドサイド設置に適した小型・省電力設計 |
| Raspberry Pi AI HAT+ 2 | Raspberry Pi | Hailo-10H、40 TOPS、8GB RAM | LLM推論は低速(6.5 tok/s)。主デバイスには不適 |

---

## 4. 製品・プラットフォーム比較表

### 4.1 総合比較

| プラットフォーム | AI性能 (TOPS) | メモリ | メモリ帯域幅 | 消費電力 | 価格帯 | LLM推論 (1.7B Q4) | VLM同時実行 | 静音性 | 開発エコシステム | VoiceReach適合度 |
|---|---|---|---|---|---|---|---|---|---|---|
| **Mac mini M4** | ~38 TOPS (Neural Engine) | 16/24/32GB | 120 GB/s | 5-65W | ¥95K-155K | ~200 tok/s | 可能 | **最高** | **最高** (MLX) | **A** |
| **Mac mini M4 Pro** | ~38 TOPS (NE) + GPU | 24/48GB | 273 GB/s | 10-80W | ¥219K-289K | ~320 tok/s | 可能 | 高 | **最高** (MLX) | **S** |
| MacBook Air M4 | ~38 TOPS | 16/24/32GB | 120 GB/s | 5-30W | ¥165K-225K | ~200 tok/s | 可能 | **最高** (ファンレス) | **最高** | B+ (コスト高) |
| Jetson Orin Nano Super | 67 TOPS | 8GB | 102 GB/s | 7-25W | ~¥35K | ~40-55 tok/s (3B) | 限定的 | 低 (要冷却) | 中-高 | C+ |
| Jetson Orin NX 16GB | 100-157 TOPS | 16GB | 102 GB/s | 10-40W | ~¥60-80K | ~60-80 tok/s (3B) | 可能 | 低 (要冷却) | 中-高 | B- |
| Jetson AGX Orin 64GB | 275 TOPS | 64GB | 204.8 GB/s | 15-60W | ~¥150-300K | ~100+ tok/s | 十分可能 | 低 (要冷却) | 中-高 | B (高価) |
| Raspberry Pi 5 + AI HAT+ 2 | 40 TOPS (Hailo) | 8GB (+8GB NPU) | 低 | 10-22W | ~¥30K | ~6.5 tok/s | 不可 | 中 | 高 (Linux) | D |
| Intel NUC (Core Ultra) | 11-40 TOPS (NPU) | 16-32GB | 様々 | 15-65W | ¥80K-150K | GPU依存 | 可能 | 中-高 | 中 (OpenVINO) | C |
| AMD Ryzen AI PC | 50 TOPS (XDNA 2) | 16-64GB | 様々 | TDP 15-54W | ¥100K-200K | GPU/NPU依存 | 可能 | 中 | 低-中 (発展途上) | C+ |
| Qualcomm Snapdragon X Elite | 45-80 TOPS (NPU) | 16-64GB | ~136 GB/s | ~8W (NPU) | ¥100K-200K | NPU/CPU依存 | 可能 | 高 | 低 (Windows) | C |

### 4.2 Apple Silicon世代別の推奨度

| チップ | VoiceReach推奨度 | 理由 |
|---|---|---|
| M1 (8/16GB) | C | メモリ8GBでは不足。16GBならMVP動作可能だがVLM併用困難 |
| M1 Pro/Max | B | 十分なメモリ帯域幅。中古市場で安価 |
| M2 (8/16/24GB) | B- | 24GBモデルならVLM併用可能 |
| M2 Pro | B+ | 200 GB/sの帯域幅。安定性高い |
| M3 (24GB) | B+ | M4に近い性能。コスト効率良好 |
| **M4 (24GB)** | **A** | **推奨最小構成。24GBで全パイプライン同時実行可能** |
| **M4 Pro (24GB)** | **S** | **推奨構成。273 GB/sの帯域幅でLLM推論最速クラス** |
| M4 Max | A+ | オーバースペック気味だが将来の拡張性は最高 |

---

## 5. VoiceReach向け推奨事項

### 5.1 メインプラットフォーム: Apple Silicon Mac

**第一推奨: Mac mini M4 Pro (24GB)**

推奨理由:
1. **性能**: 273 GB/sメモリ帯域幅により、Qwen3-1.7B Q4で~320 tok/s。200ms要件を大幅に上回る
2. **メモリ**: 24GBでVoiceReach全パイプライン（LLM 1.2GB + VLM 2.5GB + TTS 1GB + 視線推定 0.5GB + OS 6GB = ~11GB）に十分な余裕
3. **静音性**: 低負荷時ほぼ無音(~20dB)。ALS患者のベッドサイドに最適
4. **サイズ**: 12.7cm角の手のひらサイズ。モニターアームやベッドサイドの棚に設置可能
5. **安定性**: macOSの高い安定性。クラッシュ頻度が極めて低い
6. **エコシステム**: MLXフレームワーク(Apple公式)が本番グレードに成熟。WWDC25で更に強化
7. **価格**: ¥218,800（税込）。医療・福祉機器として妥当な価格帯
8. **将来性**: M5チップ以降でさらなる性能向上が見込める。ソフトウェア互換性が維持される

**コスト制約がある場合: Mac mini M4 (24GB)**

推奨理由:
1. **価格**: ¥124,800（税込）。構成Bの中心
2. **性能**: 120 GB/sメモリ帯域幅でも200ms要件は満たせる（~200 tok/s）
3. **静音性**: M4 Proよりさらに静か（低消費電力）

### 5.2 将来の量産・ポータブル版: NVIDIA Jetson

将来的にVoiceReachを専用デバイスとして量産する場合、NVIDIA Jetsonプラットフォームが候補となる:

- **Jetson Orin NX 16GB**: 量産価格で$399（モジュール単体）。組込みLinuxで動作。
- **課題**: LLM推論速度がApple Siliconに劣る。クラウドLLMとのハイブリッド運用が必要。
- **利点**: カスタム筐体設計、バッテリー駆動、MIPI CSIカメラ直接接続。

### 5.3 推奨しないプラットフォーム

| プラットフォーム | 不推奨理由 |
|---|---|
| Raspberry Pi 5 + AI HAT | LLM推論速度が致命的に遅い(6.5 tok/s)。メモリも不足 |
| Google Coral Edge TPU | 4 TOPSではVLM/LLM推論不可 |
| Intel Core Ultra (Meteor Lake) | NPU 11 TOPSはLLM推論に不十分。エコシステム未成熟 |
| 汎用Windows PC (dGPU無し) | CPU推論では要件を満たせない |

### 5.4 統合時の考慮点

1. **電源管理**: Mac miniはUPSとの接続を推奨。緊急通報機能の継続動作に必須。
2. **冷却**: Mac mini M4/M4 Proは内蔵ファンで十分だが、設置場所の通気を確保する（壁に密着させない等）。
3. **ネットワーク**: macOSのファイアウォール設定で、VLM/LLMプロセスのインターネットアクセスをデフォルト遮断（プライバシー保護）。
4. **自動起動**: macOSの「ログイン項目」でVoiceReachアプリを自動起動設定。電源復帰時も自動起動するように設定。
5. **監視**: ヘルスチェックプロセスを常駐させ、メインアプリのクラッシュを検出して自動再起動。
6. **更新**: MLXフレームワークとモデルの更新はネットワーク接続時に自動チェック。適用は介護者の承認後。

### 5.5 期待される性能（推奨構成B: Mac mini M4, 24GB）

| 指標 | 要件 | 予測値 |
|---|---|---|
| 視線推定フレームレート | 25fps以上 | 30fps以上 |
| LLM候補生成レイテンシ | 200ms以内 | ~150ms (Qwen3-1.7B Q4) |
| TTS合成レイテンシ | リアルタイム | リアルタイム |
| VLMシーン記述更新 | 10秒以内 | 5-8秒間隔 |
| メモリ使用量（全パイプライン） | 16GB以下 | ~11GB |
| 消費電力（通常動作時） | 50W以下 | ~25-40W |
| ファン騒音 | 30dB以下 | ~20dB |
| 24/7稼働安定性 | 99.5%以上 | 99.9%（macOSの安定性） |

### 5.6 リスクと軽減策

| リスク | 影響度 | 軽減策 |
|---|---|---|
| Apple Silicon搭載Mac miniの供給停止 | 低 | Appleは年次更新を継続。最低5年のサポート。中古市場も活発 |
| MLXフレームワークの開発停止 | 低 | Apple公式プロジェクト。WWDC25でも推進。llama.cppへのフォールバック可能 |
| macOSの互換性破壊的アップデート | 低-中 | 特定macOSバージョンで固定運用する選択肢。セキュリティパッチのみ適用 |
| Mac miniの故障時の代替 | 中 | 同型機をバックアップとして確保。設定のエクスポート/インポート自動化 |
| 将来モデルのメモリ要件増大 | 中 | 24GBで当面十分。M4 Pro 48GB版も選択可能。量子化技術の進歩に期待 |
| Jetson版への移植コスト | 中 | MLX → NVIDIA (TensorRT/llama.cpp) の移植は、モデルフォーマット変換のみで比較的容易 |
| 医療機器認証の要件 | 高 | VoiceReachは「医療機器」ではなく「日常生活用具」としての位置づけを推奨。認証要件を確認 |

---

## 6. 未解決の問題・今後の調査

1. **実機ベンチマーク**: Mac mini M4/M4 ProでのVoiceReach全パイプライン同時実行の実測値取得
2. **長時間稼働テスト**: 24/7連続稼働での安定性、メモリリーク、温度推移の検証
3. **UPS連携**: Mac miniの自動電源オン/オフとUPSの連携方法
4. **外部カメラの接続安定性**: USB Webカメラの長時間使用での接続断の頻度と自動復旧
5. **M5チップ搭載Mac miniのベンチマーク**: 2026年後半に予想されるM5 Mac miniでの性能向上の確認
6. **Jetsonポータブル版のプロトタイプ**: 外出用デバイスとしてのJetson Orin NX版の試作と評価
7. **医療・福祉機器としての認証・補助金**: 日本における日常生活用具給付制度の対象となるための要件調査
8. **Qualcomm Snapdragon X2 Elite (80 TOPS)**: 2026年後半の登場予定。Windows + NPU推論の成熟度を再評価

---

## 7. 参考文献

1. arXiv:2511.05502. "Production-Grade Local LLM Inference on Apple Silicon: A Comparative Study of MLX, MLC-LLM, Ollama, llama.cpp, and PyTorch MPS." 2025. https://arxiv.org/abs/2511.05502
2. arXiv:2510.18921. "Benchmarking On-Device Machine Learning on Apple Silicon with MLX." 2025. https://arxiv.org/abs/2510.18921
3. Apple ML Research. "Exploring LLMs with MLX and the Neural Accelerators in the M5 GPU." 2025. https://machinelearning.apple.com/research/exploring-llms-mlx-m5
4. arXiv:2601.19139. "Native LLM and MLLM Inference at Scale on Apple Silicon." 2026. https://arxiv.org/html/2601.19139v1
5. Apple Developer. "Explore large language models on Apple silicon with MLX." WWDC25. https://developer.apple.com/videos/play/wwdc2025/298/
6. Jeff Geerling. "M4 Mac mini's efficiency is incredible." 2024. https://www.jeffgeerling.com/blog/2024/m4-mac-minis-efficiency-incredible
7. Apple Support. "Mac mini power consumption and thermal output." https://support.apple.com/en-us/103253
8. NVIDIA. "Jetson Orin Nano Super Developer Kit." https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-orin/nano-super-developer-kit/
9. NVIDIA Developer Blog. "Jetson Orin Nano Developer Kit Gets a Super Boost." 2025. https://developer.nvidia.com/blog/nvidia-jetson-orin-nano-developer-kit-gets-a-super-boost/
10. NVIDIA Developer Blog. "JetPack 6.2 Brings Super Mode." 2025. https://developer.nvidia.com/blog/nvidia-jetpack-6-2-brings-super-mode-to-nvidia-jetson-orin-nano-and-jetson-orin-nx-modules/
11. NVIDIA Developer Blog. "Getting Started with Edge AI on NVIDIA Jetson." https://developer.nvidia.com/blog/getting-started-with-edge-ai-on-nvidia-jetson-llms-vlms-and-foundation-models-for-robotics/
12. Raspberry Pi. "Introducing the Raspberry Pi AI HAT+ 2." 2026. https://www.raspberrypi.com/news/introducing-the-raspberry-pi-ai-hat-plus-2-generative-ai-on-raspberry-pi-5/
13. CNX Software. "Raspberry Pi AI HAT+ 2 review." 2026. https://www.cnx-software.com/2026/01/20/raspberry-pi-ai-hat-2-review-a-40-tops-ai-accelerator-tested-with-computer-vision-llm-and-vlm-workloads/
14. Coral. "Edge TPU performance benchmarks." https://www.coral.ai/docs/edgetpu/benchmarks/
15. Intel. "NPU Device - OpenVINO documentation." https://docs.openvino.ai/2025/openvino-workflow/running-inference/inference-devices-and-modes/npu-device.html
16. Intel. "Most Efficient LLMs for AI PC - OpenVINO." https://docs.openvino.ai/2025/about-openvino/performance-benchmarks/generative-ai-performance.html
17. arXiv:2412.11053. "NITRO: LLM Inference on Intel Laptop NPUs." 2024. https://arxiv.org/html/2412.11053v1
18. Tom's Hardware. "AMD Ryzen AI 300 series Strix Point processors." https://www.tomshardware.com/pc-components/cpus/amd-unwraps-ryzen-ai-300-series-strix-point-processors
19. HotHardware. "Qualcomm Snapdragon X Elite Benchmarks." https://hothardware.com/reviews/qualcomm-snapdragon-x-elite-benchmarks
20. Futurum Group. "Snapdragon X2 Elite Pushes AI-PC Performance." https://futurumgroup.com/insights/snapdragon-x2-elite-pushes-ai-pc-performance-to-new-heights/
21. GitHub. "Performance of llama.cpp on Apple Silicon M-series." https://github.com/ggml-org/llama.cpp/discussions/4167
22. Andreas Kunar. "Benchmarking Apple's MLX vs. llama.cpp." Medium. https://medium.com/@andreask_75652/benchmarking-apples-mlx-vs-llama-cpp-bbbebdc18416
23. MLX Framework. https://mlx-framework.org/
24. Blaizzy/mlx-vlm. GitHub. https://github.com/Blaizzy/mlx-vlm
25. waybarrios/vllm-mlx. GitHub. https://github.com/waybarrios/vllm-mlx
26. NVIDIA. "Jetson Benchmarks." https://developer.nvidia.com/embedded/jetson-benchmarks
27. Cytron. "Deploy F5-TTS on NVIDIA Jetson Orin Nano." https://www.cytron.io/tutorial/nvidia-jetson-orin-nanotext-to-speech-synthesis-with-f5-tts
28. GenAI Protos. "On-Device LLM Inference on NVIDIA Jetson Orin Nano." Medium. https://genaiprotos.medium.com/on-device-llm-inference-on-nvidia-jetson-orin-nano-0e7c7066d062
29. LearnOpenCV. "VLM on Edge: Worth the Hype or Just a Novelty?" 2025. https://learnopencv.com/vlm-on-edge-devices/
30. Sound on Sound Forum. "Is the Mac mini M4 silent?" https://www.soundonsound.com/forum/viewtopic.php?t=93280

# B5 -- VLM（Vision-Language Models）調査レポート

**調査日**: 2026-02-17
**対象**: VoiceReachの外向きカメラによる環境認識・状況理解に最適なVLMの選定
**ステータス**: Draft

---

## 1. エグゼクティブサマリー

VoiceReachの外向きカメラ（10fps, 720p）は、VLMを用いてベッドサイドの環境（来客、食事の到着、医療機器、テレビ画面等）を認識し、文脈に応じた発話候補生成のトリガーとする。本調査では、クラウドVLMとローカルVLMの性能・コスト・プライバシートレードオフを包括的に評価した。

**結論**: VoiceReachには**ハイブリッドアーキテクチャ**を推奨する。通常時はローカルVLM（**MiniCPM-V 4.5** または **Moondream 2B**）による定期スナップショット分析（5-10秒間隔）を行い、重要イベント検出時のみクラウドVLM（**Gemini 2.5 Flash**、コスト効率最優先）にフォールバックする。プライバシー保護の観点から、カメラ映像は原則ローカル処理とし、クラウド送信時は患者の明示的同意に基づく。

---

## 2. リサーチクエスチョンへの回答

### Q1: クラウドVLMの画像理解能力の比較

主要クラウドVLMのベンチマーク比較（2025-2026年時点）:

| モデル | MMMU | MMBench-EN | OCRBench | シーン理解 | 表情読み取り | テキスト読み取り | 1Mトークンあたりコスト（入力） |
|---|---|---|---|---|---|---|---|
| **Gemini 2.5 Pro** | 81.7-84.0% | 非公開 | 高 | 最高レベル | 高 | 最高レベル | ~$1.25 |
| **Gemini 2.5 Flash** | ~75-78% | 非公開 | 高 | 高レベル | 中-高 | 高レベル | ~$0.15 |
| **GPT-4o** | ~69-72% | ~83% | 高 | 高レベル | 高 | 高レベル | ~$2.50 |
| **GPT-5** | ~84.2% | 非公開 | 非公開 | 最高レベル | 最高レベル | 最高レベル | ~$10 |
| **Claude Sonnet 4.5** | 77.8% | 非公開 | 中-高 | 高レベル | 中-高 | 高レベル | ~$3.00 |

**VoiceReach向け評価**:

- **シーン理解（人物認識、物体検出）**: Gemini 2.5 Proが空間推論能力で最も優れ、チャート相関・UI解析・手書き文書解析に強い。GPT-4oも実用十分。
- **表情読み取り**: GPT-4o/GPT-5シリーズが最も信頼性が高いが、ALS患者の微細表情は専用モデル（設計書05で規定）に任せるべき。VLMは介護者の表情読み取りに限定使用。
- **テキスト読み取り（テレビ画面、医療機器ディスプレイ）**: Gemini 2.5 Pro/FlashのOCR能力が突出。Claude Sonnet 4.5もコードスクリーンショットの読み取りに強いが、汎用テキスト読み取りではGeminiが優位。
- **コスト効率**: Gemini 2.5 Flashが圧倒的に安価（GPT-4oの約1/17、Claude Sonnet 4.5の約1/20）。VoiceReachのイベント駆動処理（1日あたり数十〜数百回の画像分析）では月額数百円レベルで運用可能。

### Q2: ローカルVLMの性能とリソース要件

#### 主要ローカルVLM比較

| モデル | パラメータ数 | MMMU | OpenCompass | メモリ要件 (Q4) | Apple Silicon推論速度 | 特徴 |
|---|---|---|---|---|---|---|
| **MiniCPM-V 4.5** | 8B | 高 | 77.0 | ~5GB | ~20-30 tok/s (M4) | GPT-4o超えと主張。動画対応。OCR最強クラス |
| **MiniCPM-V 4.0** | 4.1B | 中+ | 69.0 | ~2.5GB | ~40-50 tok/s (M4) | GPT-4.1-mini超え。軽量で高性能 |
| **Qwen2.5-VL-7B** | 7B | 70.2 (72B) | 高 | ~4.5GB | ~25-35 tok/s (M4) | 日本語品質が高い。動的解像度対応 |
| **Qwen2.5-VL-3B** | 3B | 中 | 中 | ~2.0GB | ~50-65 tok/s (M4) | Jetson Orin Nanoでも動作可能 |
| **InternVL3-8B** | 8B | ~68% | 高 | ~5GB | ~20-30 tok/s (M4) | 英中バイリンガル。マルチモーダル知覚が強い |
| **InternVL3-2B** | 2B | ~55% | 中 | ~1.5GB | ~55-70 tok/s (M4) | 超軽量。MMBench 81.1 |
| **Moondream 2B** | 1.8B | 中-低 | 中-低 | ~1.3GB (Q8) | ~60-80 tok/s (M4) | 極小。Raspberry Pi動作可能 |
| **Moondream 0.5B** | 0.5B | 低 | 低 | ~0.8GB (Q8) | ~100+ tok/s (M4) | 世界最小VLM。エッジ特化 |
| **Moondream 3.0 (MoE)** | 9B (2B活性) | 高 | 高 | ~6GB | ~30-40 tok/s (M4) | GPT-5/Claude 4超えと主張 |
| **Apple FastVLM-7B** | 7B | 中+ | 中+ | ~4.5GB | TTFT 85x高速化 | Apple公式。CVPR 2025。TTFT最速 |
| **Apple FastVLM-0.5B** | 0.5B | 低-中 | 低-中 | ~0.5GB | TTFT最速クラス | 3.4x小さいエンコーダ。リアルタイム可能 |
| **LLaVA-NeXT-34B** | 34B | Gemini Pro超え | 高 | ~20GB | ~8-12 tok/s (M4 Max) | 高性能だが重い |

#### Apple Silicon上での推論の実用性

**結論: 十分に実用的。**

- **MLX-VLM**: Apple公式MLXフレームワーク上でVLMを推論・ファインチューニングするパッケージ。Qwen-VL、LLaVA等をサポート。ユニファイドメモリアーキテクチャにより、CPU-GPU間メモリ転送のボトルネックがない。
- **vllm-mlx**: MLXバックエンドで400+ tok/s達成。OpenAI互換API。連続バッチング対応。llama.cppより21-87%高スループット。
- **M4 Pro (24GB)**: 7-8Bモデルを余裕を持って動作可能。VoiceReachの視線推定+ローカルLLM+TTSと並行して、VLMの定期推論も十分可能。
- **M4 Max (48-128GB)**: 30B超のモデルも動作可能。30-45 tok/s（量子化70Bモデル）。

### Q3: VLMを使った「状況理解」の精度と実用性

VoiceReachの設計書（01_SYSTEM_ARCHITECTURE.md）に記載された4つのタスクについて:

#### 1. 人物認識（顔認識 + 服装/体格推定）

- **精度**: クラウドVLM（GPT-4o, Gemini 2.5 Pro）は「白衣を着た女性が入ってきました」レベルの記述は高精度に可能。
- **ローカルVLM**: MiniCPM-V 4.5/Qwen2.5-VL-7Bでも「部屋に人が入ってきた」「女性が2人いる」程度の認識は実用的。ただし個人識別（「山田さん」等）はVLMの範疇外であり、別途顔認識モデルとの組み合わせが必要。
- **VoiceReach向け**: 「誰か来た」→ VLMで服装・体格記述 → 顔認識DBで照合 → 「山田看護師さんですね」の候補生成パイプラインが現実的。

#### 2. 物体認識（食事トレイ、リモコン、医療機器等）

- **精度**: 日常物体の検出はクラウド・ローカル共に高精度。「テーブルの上に食事トレイがある」「ベッド横にリモコンがある」レベルの記述はMoondream 2Bでも可能。
- **課題**: 医療機器の細かい表示（点滴の残量、モニターの数値等）の読み取りにはOCR能力の高いモデル（MiniCPM-V 4.5, Gemini 2.5 Flash）が必要。
- **VoiceReach向け**: 「お昼ご飯が来ましたね」「リモコンがテーブルの上にありますよ」等の候補生成に十分実用的。

#### 3. イベント検出（入室、退室、物の移動等）

- **精度**: 単一フレームからのイベント推定は限界がある。前フレームとの差分を用いた変化検出が必要。
- **実装戦略**: (a) 従来型の動体検出（OpenCV背景差分）でイベントトリガー → (b) VLMで詳細記述、のハイブリッドが最も効率的。
- **VoiceReach向け**: 定期スナップショット（10秒間隔）の差分比較 + 動体検出トリガーによるオンデマンドVLM推論が実用的。

#### 4. シーン記述テキスト生成

- **精度**: クラウドVLMは自然な日本語でのシーン記述が可能。ローカルVLMはQwen2.5-VL-7Bが日本語記述品質で最も優秀。
- **VoiceReach向け**: 生成された記述テキストをLLM候補生成のコンテキスト入力として使用。「今の状況: 部屋に看護師が2人。食事トレイがテーブル上。テレビがついている」→ この文脈で発話候補を生成。

### Q4: リアルタイム推論 vs 定期スナップショット分析

| 方式 | レイテンシ | 消費リソース | 適用場面 | VoiceReach推奨 |
|---|---|---|---|---|
| **リアルタイムストリーミング (30fps)** | <100ms | GPU 90%+ 占有 | 自動運転、ロボット | 不要（過剰） |
| **高頻度スナップショット (1fps)** | 0.5-2秒 | GPU 30-50% | 監視カメラ | 特殊ケースのみ |
| **定期スナップショット (0.1-0.2fps)** | 5-10秒間隔 | GPU 5-15% | 環境モニタリング | **通常時（推奨）** |
| **イベント駆動** | トリガー後1-3秒 | GPU <5%（待機時） | スマートホーム | **推奨（メイン）** |

**VoiceReach向け推奨アーキテクチャ**:

```
外向きカメラ (10fps, 720p)
  ├→ 軽量動体検出 (OpenCV, 常時, CPU ~5%) → 変化検出
  ├→ 定期スナップショット (5-10秒間隔)
  │    └→ ローカルVLM (MiniCPM-V 4.0 or Moondream 2B)
  │         └→ シーン記述テキスト → コンテキスト統合層へ
  └→ イベントトリガー (入室、大きな変化等)
       └→ 高精度分析 (ローカルVLM or クラウドVLM)
            └→ 詳細記述 → 候補生成エンジンへ
```

**レイテンシの現実性**:
- **ローカルVLM (MiniCPM-V 4.0, 4B)**: 画像エンコーディング + テキスト生成で約1-3秒（M4 Pro）。定期スナップショットには十分。
- **Apple FastVLM-0.5B**: TTFT 85x高速化により、サブ秒でのレスポンスが可能。リアルタイム性が必要な場面に適する。
- **クラウドVLM (Gemini 2.5 Flash)**: API呼び出し含め1-3秒。ネットワーク遅延が主要因。

### Q5: プライバシー考慮とローカル処理の必要性

#### 倫理的問題の整理

| 懸念事項 | 深刻度 | 対策 |
|---|---|---|
| 常時カメラ映像のクラウド送信 | **極めて高い** | ローカル処理を原則とする |
| 患者の生体情報（表情、視線）の外部送信 | **極めて高い** | 生体データは一切クラウドに送信しない |
| 介護者・面会者の映り込み | **高い** | 人物情報のクラウド送信前に匿名化 |
| 医療情報（モニター数値等）の漏洩 | **高い** | OCR結果のみをローカルに保持 |
| VLMモデル提供者によるデータ利用 | **中-高** | API利用規約の精査。ゼロリテンションポリシー確認 |
| 映像データの保存期間 | **中** | ローカルで短期間（数分）のみ保持。分析後は即削除 |

#### ローカル処理の必要性: 必須

ALS患者のベッドサイドという極めてプライバシーが高い環境において、映像データのクラウド送信は以下の理由から原則避けるべき:

1. **日本の個人情報保護法・医療情報ガイドライン**: 常時カメラ映像は要配慮個人情報に該当する可能性が高い
2. **患者の尊厳**: 身体介助中の映像がクラウドに送信されることは患者の尊厳を著しく損なう
3. **面会者のプライバシー**: 来訪者の同意なくクラウドに送信することは問題
4. **ネットワーク障害時の継続動作**: ローカルファースト設計の要件（設計書で70%以上オフライン動作を規定）

#### プライバシー保護技術

- **Federated LoRA (FedVLM)**: デバイス上でVLMを個人データでファインチューニングし、モデル更新のみを共有。生データは送信しない。VoiceReach向けに有望（患者の環境に適応したVLMを構築できる）。
- **差分プライバシー**: モデル更新時にノイズを注入し、個人情報の逆推定を防止。
- **オンデバイスVLM**: MiniCPM-V 4.0 (4.1B) / Moondream 2B (1.8B) はApple Silicon M4上で十分実用的な速度で動作し、映像データを一切外部に送信せずに処理可能。

### Q6: VLMのAAC支援への応用可能性

VLMによる「今見えているもの」を話題にした発話候補生成は、AAC（拡大代替コミュニケーション）の革新的な拡張となる:

#### 具体的な応用シナリオ

| シナリオ | VLMの出力 | 生成される発話候補 |
|---|---|---|
| 食事トレイが置かれた | 「テーブルに食事トレイ。味噌汁、ご飯、焼き魚」 | 「今日のお昼はおいしそうだね」「味噌汁から先に食べたい」 |
| テレビでニュースが流れている | 「テレビに天気予報。明日は晴れ」 | 「明日は天気いいんだね」「散歩日和だね」 |
| 面会者が来た | 「白いシャツの男性が入室。花束を持っている」 | 「来てくれてありがとう」「きれいな花だね」 |
| 窓の外の景色 | 「窓の外は桜が咲いている」 | 「桜がきれいだね」「もう春だなぁ」 |
| 医療スタッフが機器を操作 | 「看護師が点滴を調整中」 | 「よろしくお願いします」「痛くないですよ」 |

#### 従来AAC vs VLM拡張AAC

- **従来AAC**: 事前に用意されたフレーズ、またはキーボード入力。「文脈のない」コミュニケーション。
- **VLM拡張AAC**: 「今この瞬間」の文脈に即した候補を自動生成。会話の自然さが飛躍的に向上。視線入力の負担を大幅に軽減（選ぶだけで済む）。

#### 最新の学術研究動向

Frontiers in Communication (2025) にて "Future Technologies in Alternative and Augmented Communication: A Scoping Review of Innovations" が発表され、AIとモバイルデバイスのAAC統合が急速に進展していることが報告されている。VLMを活用したコンテキストアウェアAAC はこの研究トレンドの最先端に位置する。

---

## 3. 文献レビュー / 技術情報

### 3.1 主要論文・技術報告

| 論文/報告 | 著者/組織 | 年 | 要旨 | VoiceReachへの示唆 |
|---|---|---|---|---|
| FastVLM: Efficient Vision Encoding for VLMs | Apple ML Research | 2025 (CVPR) | ハイブリッドビジョンエンコーダ(FastViTHD)で85x高速TTFT。0.5B-7Bモデル提供 | リアルタイムオンデバイスVLM処理の実現可能性を実証。VoiceReachの低レイテンシ要件に最適 |
| MiniCPM-V 4.5 | OpenBMB | 2025 | 8Bパラメータで GPT-4o-latest超え。ビデオ対応。OCRBenchでSOTA | 軽量ながら高性能。エッジデバイスでの実用的なシーン理解に適する |
| Vision-Language Models for Edge Networks: A Comprehensive Survey | arXiv 2502.07855 | 2025 | エッジVLMの圧縮技術（プルーニング、量子化、知識蒸留）を体系的にレビュー | VoiceReachのローカルVLM最適化の指針 |
| LiteVLM: Low-Latency VLM Inference Pipeline | arXiv 2506.07416 | 2025 | パッチ選択+トークン選択+投機的デコーディングで2.5xレイテンシ削減 | エッジデバイスでのVLM高速化に直接応用可能 |
| FedVLM: Scalable Personalized VLMs through Federated Learning | arXiv 2507.17088 | 2025 | Federated LoRAでVLMを分散適応。pLoRAでクライアント固有データに最適化 | 患者環境に適応したVLMを、プライバシーを保持して構築可能 |
| InternVL3 | OpenGVLab | 2025 | MMMU 72.2%。オープンソースMLLMの最高水準 | 高性能ローカルVLMの選択肢 |
| Qwen2.5-VL | Alibaba | 2025 | 3B/7B/32B/72B。MMMU 70.2%(72B)。日本語品質が高い | 日本語シーン記述品質で最も有望 |
| Moondream 3.0 (Preview) | Moondream | 2025 | MoEアーキテクチャ。9Bパラメータ、2B活性。GPT-5/Claude 4超えと主張 | 超軽量でありながら高性能。Raspberry Pi動作実績あり |
| Production-Grade Local LLM Inference on Apple Silicon | arXiv 2511.05502 | 2025 | MLX, llama.cpp, Ollama等をApple Silicon上で体系的に比較。MLXが最高スループット | VoiceReachのフレームワーク選定に直接参考 |
| Benchmarking On-Device ML on Apple Silicon with MLX | arXiv 2510.18921 | 2025 | Apple SiliconでのML推論ベンチマーク。M4 Maxで525 tok/s達成 | Apple Siliconの実力を定量的に評価 |

### 3.2 フレームワーク比較

| フレームワーク | 対応モデル | 対応HW | VLMサポート | API互換 | 備考 |
|---|---|---|---|---|---|
| **MLX-VLM** | LLaVA, Qwen-VL, 多数 | Apple Silicon | 完全対応（画像/動画/複数画像） | Python API | LoRA/QLoRAファインチューニング対応 |
| **vllm-mlx** | LLaVA, Qwen-VL等 | Apple Silicon | 対応 | OpenAI/Anthropic互換 | 連続バッチング。400+ tok/s |
| **vLLM** | 多数 | NVIDIA GPU | 完全対応（画像/音声/動画） | OpenAI互換 | 高スループット。マルチユーザーサービング |
| **llama.cpp** | GGUF形式全般 | CPU/GPU/Metal | 一部対応 | OpenAI互換 | 移植性最高。量子化に強い |
| **Ollama** | GGUF形式全般 | CPU/GPU/Metal | LLaVA対応 | REST API | セットアップ容易。初心者向け |

---

## 4. 製品・プラットフォーム比較表

### 4.1 クラウドVLM比較

| サービス | モデル | コンテキスト窓 | 画像入力 | 動画入力 | 入力コスト($/1M tok) | 出力コスト($/1M tok) | レイテンシ | 日本語品質 |
|---|---|---|---|---|---|---|---|---|
| Google | Gemini 2.5 Pro | 1M tokens | 対応 | 対応 | ~$1.25 | ~$10 | 1-3秒 | 高 |
| Google | Gemini 2.5 Flash | 1M tokens | 対応 | 対応 | ~$0.15 | ~$0.60 | 0.5-2秒 | 中-高 |
| OpenAI | GPT-4o | 128K tokens | 対応 | 非対応 | ~$2.50 | ~$10 | 1-3秒 | 高 |
| OpenAI | GPT-5 | 400K tokens | 対応 | 対応 | ~$10 | ~$30 | 2-5秒 | 最高 |
| Anthropic | Claude Sonnet 4.5 | 200K tokens | 対応 | 非対応 | ~$3.00 | ~$15 | 1-3秒 | 高 |

### 4.2 ローカルVLM比較（VoiceReach向け）

| モデル | パラメータ | 量子化後メモリ (Q4) | M4 Pro推論速度 | Jetson Orin Nano | 日本語品質 | シーン理解 | OCR能力 | ライセンス |
|---|---|---|---|---|---|---|---|---|
| **MiniCPM-V 4.5** | 8B | ~5GB | ~25 tok/s | 不可（メモリ不足） | 中 | 最高 | 最高 | Apache 2.0 |
| **MiniCPM-V 4.0** | 4.1B | ~2.5GB | ~45 tok/s | ~15 tok/s (Q4) | 中 | 高 | 高 | Apache 2.0 |
| **Qwen2.5-VL-7B** | 7B | ~4.5GB | ~30 tok/s | 不可 | **最高** | 高 | 高 | Apache 2.0 |
| **Qwen2.5-VL-3B** | 3B | ~2.0GB | ~55 tok/s | ~20 tok/s (Q4) | 高 | 中-高 | 中-高 | Apache 2.0 |
| **InternVL3-2B** | 2B | ~1.5GB | ~60 tok/s | ~25 tok/s (Q4) | 中 | 中-高 | 中 | MIT |
| **Moondream 2B** | 1.8B | ~1.3GB | ~70 tok/s | ~30 tok/s (Q4) | 低-中 | 中 | 中 | Apache 2.0 |
| **Moondream 0.5B** | 0.5B | ~0.4GB | ~100+ tok/s | ~50 tok/s (Q4) | 低 | 低-中 | 低 | Apache 2.0 |
| **FastVLM-7B** | 7B | ~4.5GB | TTFT最速 | 不可 | 中 | 高 | 中-高 | Apple License |
| **FastVLM-0.5B** | 0.5B | ~0.5GB | TTFT最速 | 可能 | 低 | 中 | 低-中 | Apple License |

### 4.3 ベンチマーク比較（主要VLMベンチマーク）

| モデル | MMMU | MMBench-EN | OCRBench | ChartQA | VideoMME | SEEDBench |
|---|---|---|---|---|---|---|
| Gemini 2.5 Pro | 81.7-84.0 | - | 高 | 高 | - | - |
| GPT-4o | ~69-72 | ~83 | 高 | 高 | - | - |
| Claude Sonnet 4.5 | 77.8 | - | 中-高 | - | - | - |
| InternVL3-78B | 72.2 | 88+ | - | - | - | - |
| Qwen2.5-VL-72B | 70.2 | 88.6 | 88.8 | - | - | - |
| Qwen2.5-VL-32B | 70.0 | - | 57.2 (v2) | - | - | - |
| MiniCPM-V 4.5 (8B) | 高 | 高 | GPT-4o超 | - | SOTA (<30B) | - |
| Moondream 2B | 中-低 | - | - | 77.5 | - | - |

---

## 5. VoiceReach向け推奨事項

### 5.1 推奨アーキテクチャ: ハイブリッド3層構成

```
Layer 1: 常時監視（CPU, <5%負荷）
  └ OpenCV動体検出 + フレーム差分
  └ 変化なし → 何もしない（省電力）
  └ 変化あり → Layer 2をトリガー

Layer 2: ローカルVLM分析（GPU, ~10-20%負荷、断続的）
  ├ 定期実行: 5-10秒間隔でシーン記述更新
  ├ イベント駆動: Layer 1のトリガーで即時実行
  └ 使用モデル:
     ├ Apple Silicon → MiniCPM-V 4.0 (4.1B) 推奨
     ├ Jetson Orin Nano → Qwen2.5-VL-3B 推奨
     └ 低スペック → Moondream 2B

Layer 3: クラウドVLM（オプション、患者同意時のみ）
  ├ 使用条件: ローカルVLMで判断困難な場面
  ├ 推奨: Gemini 2.5 Flash（コスト最安）
  └ 月額コスト目安: 数百円（1日100画像分析の場合）
```

### 5.2 採用推奨モデル

#### ローカルVLM（第一推奨）

| 優先順位 | モデル | 理由 |
|---|---|---|
| 1 | **MiniCPM-V 4.0 (4.1B)** | 4Bクラスで最高性能。GPT-4.1-mini超え。メモリ2.5GBで他タスクとの共存が容易 |
| 2 | **Qwen2.5-VL-3B** | 日本語品質が最も高い3Bクラスモデル。Jetsonでも動作可能 |
| 3 | **Moondream 2B** | 超軽量。メモリ1.3GBで動作。Raspberry Pi実績あり |

#### クラウドVLM（フォールバック）

| 優先順位 | モデル | 理由 |
|---|---|---|
| 1 | **Gemini 2.5 Flash** | 圧倒的コスト効率。1M tokens入力で$0.15。VoiceReachの利用パターンでは月額数百円 |
| 2 | **GPT-4o** | 安定した性能。日本語品質が高い |
| 3 | **Claude Sonnet 4.5** | 指示追従能力が高い。コード/文書解析に強い |

### 5.3 統合時の考慮点

1. **メモリ管理**: ローカルVLM（4B, ~2.5GB）とローカルLLM（Qwen3-1.7B, ~1.2GB）とTTS（~0.5-1GB）の合計は約4-5GB。M4 Pro (24GB) なら余裕。16GBでも実用的。
2. **GPU時分割**: VLMは断続的使用（5-10秒に1回、推論時間1-3秒）のため、LLMやTTSとのGPU競合は限定的。MLXの効率的なメモリ管理により問題ない。
3. **遅延の許容**: 環境認識は即時性を要さない（数秒の遅延は許容）。ただしイベント駆動時は1-3秒以内の応答が望ましい。
4. **フォールバック戦略**: クラウドVLM利用時は、(a) 患者同意確認 (b) 画像の匿名化処理（可能であれば）(c) APIのゼロリテンションポリシー確認 を行う。

### 5.4 期待される性能

| 指標 | 目標 | 予測値 (M4 Pro + MiniCPM-V 4.0) |
|---|---|---|
| シーン記述更新間隔 | 10秒以内 | 5-8秒（5秒間隔 + 推論1-3秒） |
| イベント検出→候補生成 | 5秒以内 | 2-4秒（動体検出→VLM→LLM候補生成） |
| メモリ使用量（VLM分） | 4GB以下 | ~2.5GB (Q4量子化) |
| GPU使用率（VLM分） | 20%以下 | ~10-15%（断続使用） |
| 電力消費増（VLM分） | 5W以下 | ~3-5W（断続使用） |

### 5.5 リスクと軽減策

| リスク | 影響度 | 軽減策 |
|---|---|---|
| ローカルVLMの日本語記述品質が不十分 | 中 | Qwen2.5-VL-3Bを代替として検討。LoRAファインチューニングで改善 |
| VLMが医療情報を誤認識 | 高 | VLMの出力を「参考情報」として扱い、重要な医療判断には使用しない |
| プライバシー事故（意図しないクラウド送信） | 高 | ネットワーク制御をOS/FW レベルで実装。VLMプロセスのネットワークアクセスをデフォルト遮断 |
| モデルの幻覚（存在しない物体の報告） | 中 | 時系列の整合性チェック。複数フレームでの確認。信頼度スコアの閾値設定 |
| Apple FastVLMのライセンス制約 | 低-中 | Apache 2.0のMiniCPM-VまたはQwen2.5-VLを主軸とし、FastVLMはオプション |

---

## 6. 未解決の問題・今後の調査

1. **ALS患者のベッドサイド環境に特化したVLMファインチューニング**: 医療機器、介護用品、ベッドサイド家具等の認識精度向上のためのドメイン特化LoRA
2. **VLM出力の日本語品質の定量評価**: VoiceReachのシナリオ（食事、面会、医療行為等）に特化した評価データセットの構築
3. **マルチモーダル統合**: VLMのシーン記述 + 音声認識（誰が何を言ったか）+ 視線データ（患者が何を見ているか）の統合方法の設計
4. **長期運用時の適応学習**: Federated LoRAを用いた患者環境への適応と、モデルドリフトの監視
5. **倫理審査**: ALS患者のベッドサイドカメラ設置に関する倫理審査プロセスの確立。IRB承認取得の要件整理

---

## 7. 参考文献

1. Apple ML Research. "FastVLM: Efficient Vision Encoding for Vision Language Models." CVPR 2025. https://machinelearning.apple.com/research/fast-vision-language-models
2. OpenBMB. "MiniCPM-V 4.5: Cooking Efficient MLLMs via Architecture, Data, and Training Recipe." arXiv:2509.18154, 2025. https://arxiv.org/abs/2509.18154
3. Qwen Team. "Qwen2.5-VL Technical Report." 2025. https://huggingface.co/Qwen/Qwen2.5-VL-72B-Instruct
4. OpenGVLab. "InternVL3: Exploring Advanced Training and Test-Time Recipes." arXiv:2504.10479, 2025. https://arxiv.org/pdf/2504.10479
5. Moondream. "Introducing Moondream 0.5B: The World's Smallest Vision-Language Model." 2025. https://moondream.ai/blog/introducing-moondream-0-5b
6. Moondream. "Moondream 3 Preview: Frontier-level reasoning at a blazing speed." 2025. https://moondream.ai/blog/moondream-3-preview
7. arXiv:2502.07855. "Vision-Language Models for Edge Networks: A Comprehensive Survey." 2025. https://arxiv.org/abs/2502.07855
8. arXiv:2506.07416. "LiteVLM: A Low-Latency Vision-Language Model Inference Pipeline for Resource-Constrained Environments." 2025. https://arxiv.org/abs/2506.07416
9. arXiv:2507.17088. "FedVLM: Scalable Personalized Vision-Language Models through Federated Learning." 2025. https://arxiv.org/html/2507.17088
10. arXiv:2511.05502. "Production-Grade Local LLM Inference on Apple Silicon." 2025. https://arxiv.org/abs/2511.05502
11. arXiv:2510.18921. "Benchmarking On-Device Machine Learning on Apple Silicon with MLX." 2025. https://arxiv.org/abs/2510.18921
12. Blaizzy/mlx-vlm. "MLX-VLM: Vision Language Models on Apple Silicon." GitHub. https://github.com/Blaizzy/mlx-vlm
13. waybarrios/vllm-mlx. "vllm-mlx: OpenAI compatible server for Apple Silicon." GitHub. https://github.com/waybarrios/vllm-mlx
14. LearnOpenCV. "VLM on Edge: Worth the Hype or Just a Novelty?" 2025. https://learnopencv.com/vlm-on-edge-devices/
15. Clarifai. "Benchmarking Best Open-Source Vision Language Models: Gemma 3 vs. MiniCPM vs. Qwen 2.5 VL." 2025. https://www.clarifai.com/blog/benchmarking-best-open-source-vision-language-models
16. HuggingFace. "Vision Language Models (Better, faster, stronger)." 2025. https://huggingface.co/blog/vlms-2025
17. Frontiers in Communication. "Future Technologies in Alternative and Augmented Communication: A Scoping Review." 2025. https://www.frontiersin.org/journals/communication/articles/10.3389/fcomm.2025.1607531/abstract
18. MMMU Benchmark. https://mmmu-benchmark.github.io/
19. Dextralabs. "Top 10 Vision Language Models in 2026." https://dextralabs.com/blog/top-10-vision-language-models/
20. NVIDIA. "Benchmarking - NVIDIA NIM for Vision Language Models." https://docs.nvidia.com/nim/vision-language-models/latest/benchmarking.html

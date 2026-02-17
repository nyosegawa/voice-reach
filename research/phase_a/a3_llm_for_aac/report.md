# A3: LLM x AAC 候補生成 ― 調査報告書

> **調査日**: 2026-02-17
> **対象**: VoiceReach プロジェクト ― AI候補生成エンジンの設計根拠と先行研究
> **範囲**: LLM-based AAC prediction, ICL personalization, diverse response generation, persona-based dialogue, conversational response prediction

---

## 目次

1. [Academic Literature Review](#1-academic-literature-review)
2. [Existing AAC+AI Products](#2-existing-aacai-products)
3. [ICL Personalization Research](#3-icl-personalization-research)
4. [Diverse Generation Techniques](#4-diverse-generation-techniques)
5. [Conversational Response Prediction](#5-conversational-response-prediction)
6. [Comparative Analysis](#6-comparative-analysis)
7. [Prompt Engineering Insights](#7-prompt-engineering-insights)
8. [Recommendations](#8-recommendations)
9. [Open Questions](#9-open-questions)

---

## 1. Academic Literature Review

### 1.1 LLM for AAC ― Core Papers

#### 1.1.1 SpeakFaster (Google Research + Team Gleason, 2024)

- **論文**: "Using large language models to accelerate communication for eye gaze typing users with ALS"
- **著者**: Shanqing Cai, Subhashini Venugopalan, Katrin Tomanek, et al.
- **掲載**: Nature Communications, 2024 (arXiv: 2312.01532)
- **URL**: https://www.nature.com/articles/s41467-024-53873-3

**概要**: ALS患者の視線タイピングにおけるLLM活用の最も重要な実証研究。高度に省略されたテキスト（単語イニシャル+補足文字）をLLMで完全なフレーズに展開するシステム。2つのfine-tuned LLM（KeywordAE: 略語展開、FillMask: 文脈に基づく単語補完）を使用。

**主要結果**:
- オフラインシミュレーションで従来の予測キーボードより57%多くのモーターアクションを削減
- 2名のALS患者（視線タイピングユーザー）での実地テストで、ベースラインより29-60%高いテキスト入力速度を達成
- ベースラインの視線タイピング速度: 8.1 +/- 3.9 WPM（words per minute）
- 約180万のユニークなトリプレット {context, abbreviation, full phrase} でfine-tuned

**VoiceReachへの示唆**: SpeakFasterは文字入力の加速に焦点を当てるが、VoiceReachは「文字入力そのものを不要にする」（意図レベルでの候補生成）というより上位の抽象化を目指している。両者は補完的であり、VoiceReachのLevel 3（2ストローク文字入力）にSpeakFaster的な略語展開技術を統合することは有望。

---

#### 1.1.2 Foundation Models in AAC: AMBRA (2024)

- **論文**: "Foundation Models in Augmentative and Alternative Communication: Opportunities and Challenges"
- **著者**: Ambra Di Paola, Serena Muraro, Roberto Marinelli, Christian Pilato
- **掲載**: arXiv:2401.08866, January 2024
- **URL**: https://arxiv.org/abs/2401.08866

**概要**: AAC領域におけるfoundation modelの機会と課題をマッピングした概観論文。AMBRAプラットフォーム（クラウド+エッジデバイスの連携基盤）を提案。連合学習とgenerative AIを組み合わせたパーソナライズドAAC基盤。

**主要貢献**:
- AAC教材の自動生成（text-to-text生成モデル）
- シンボルコンテンツのトークン化と生成
- 教育者間の知識共有基盤
- パーソナライゼーションのためのfederated learning

**VoiceReachへの示唆**: AMBRAはシンボルベースAAC（主に発達障害向け）に焦点。VoiceReachのテキストベース候補生成とは異なるアプローチだが、federated learningによるプライバシー保護型パーソナライゼーションの設計は参考になる。

---

#### 1.1.3 Adapting LLMs for Character-based AAC (2025)

- **論文**: "Adapting Large Language Models for Character-based Augmentative and Alternative Communication"
- **著者**: Dylan Gaines, Keith Vertanen
- **掲載**: Findings of EMNLP 2025 (arXiv:2501.10582)
- **URL**: https://arxiv.org/abs/2501.10582

**概要**: サブワードトークン予測を行うLLMを、文字単位AAC入力に適応させるアルゴリズム。サブワードLLMから文字確率を抽出する手法を開発し、分類層追加、バイトレベルLLM、n-gramモデルよりも高精度な文字予測を実現。

**主要結果**:
- AAC会話・平易テキストに特化したドメイン適応データセットを構築
- ドメイン適応により会話的・簡潔なテキストでの性能が顕著に向上
- subword LLMからの文字確率抽出アルゴリズムが全比較手法を上回る

**VoiceReachへの示唆**: Level 3（文字入力）フォールバック時のLLM予測精度向上に直接適用可能。特に日本語2ストローク入力後の単語/文予測に、この文字レベル適応手法は有用。

---

#### 1.1.4 SpeakEase (2025)

- **論文**: "Your voice is your voice: Supporting Self-expression through Speech Generation and LLMs in Augmented and Alternative Communication"
- **著者**: Yiwen Xu, Monideep Chakraborti, Tianyi Zhang, Katelyn Eng, Aanchan Mohan, Mirjana Prpa
- **掲載**: arXiv:2503.17479, March 2025
- **URL**: https://arxiv.org/abs/2503.17479

**概要**: マルチモーダル入力（テキスト、音声、コンテキスト手がかり）とLLMを統合したAACシステム。ASR + コンテキスト認識LLM出力 + パーソナライズドTTSを組み合わせ。会話相手と感情トーンをコンテキストとして使用。

**主要結果**:
- SLPs（言語聴覚士）による評価で、パーソナライズされた文脈適合的コミュニケーション支援の可能性を確認
- マルチモーダル入力とLLM統合によるexpressivity（表現力）の向上

**VoiceReachへの示唆**: VoiceReachのリスニングモード（ASR + LLM候補生成）と非常に近い設計。感情トーンをコンテキストに組み込む点はVoiceReachの感情検出統合と類似。SpeakEaseは「1つの最適応答」を目指すのに対し、VoiceReachは「4つの多様な候補」を生成する点が差別化。

---

#### 1.1.5 SocializeChat (UbiComp 2023, updated 2025)

- **論文**: "SocializeChat: a GPT-based AAC Tool for Social Communication Through Eye Gazing"
- **著者**: Liye et al.
- **掲載**: ACM UbiComp/ISWC 2023 Adjunct; updated version arXiv:2510.19017 (2025)
- **URL**: https://dl.acm.org/doi/10.1145/3594739.3610705

**概要**: GPT-4を用いた視線入力AAC。ユーザーの記憶記録とペルソナデータベースを活用し、社会的関係性・生活状況・個人的習慣に合わせた文候補を生成。

**主要結果**:
- 16名の参加者中、7名がPerfectly Matched、4名がMostly Matched
- 話題嗜好と対人親密度に基づくパーソナライゼーション
- 社会的コンテキストと会話相手に応じた文体の調整

**VoiceReachへの示唆**: VoiceReachのPVP（relational_styles）と極めて類似した設計思想。SocializeChatは「社会的親密度」でスタイルを変えるが、VoiceReachはより詳細な相手別プロファイル（妻/医師/孫/看護師等）と7意図軸の組み合わせで候補を生成する点でより包括的。

---

#### 1.1.6 "The less I type, the better" (CHI 2023)

- **論文**: "The less I type, the better: How AI Language Models can Enhance or Impede Communication for AAC Users"
- **著者**: Shanqing Cai et al. (Google Research)
- **掲載**: CHI 2023 (ACM Conference on Human Factors in Computing Systems)
- **URL**: https://dl.acm.org/doi/10.1145/3544548.3581560

**概要**: 12名のAACユーザーとのユーザースタディ。AI言語モデル（LLM）が生成するフレーズ候補を、3つのシナリオ（短い返答の拡張、伝記的質問への回答、支援要請）でテスト。

**主要知見**:
- 参加者はAI生成フレーズが時間・身体的・認知的労力を削減できると評価
- **しかし**、生成されるフレーズが「自分のコミュニケーションスタイルと好みを反映すること」が極めて重要と回答
- 文脈適合性、個人スタイルの一致、カスタマイズ・編集・削除の機能を要求
- AI提案への移行は「タイピングからプロンプティング+選択へ」のパラダイムシフト

**VoiceReachへの示唆**: この知見はVoiceReachのPVP設計の根拠を直接裏付ける。「スタイル一致なき高速化は無意味」というユーザーの声は、PVP + ICLアプローチの必然性を示す。

---

#### 1.1.7 Card Prediction with Colourful Semantics (2024)

- **論文**: "Enhancing Augmentative and Alternative Communication with Card Prediction and Colourful Semantics"
- **著者**: Jayr Pereira, Francisco Rodrigues, Jaylton Pereira, Cleber Zanchettin, Robson Fidalgo
- **掲載**: arXiv:2405.15896, May 2024
- **URL**: https://arxiv.org/abs/2405.15896

**概要**: Colourful Semantics（品詞を色分けするフレームワーク）とBERTを統合したシンボルベースAAC予測モデル。ブラジルポルトガル語向け。

**主要結果**:
- BERTptCS（CS統合版）がBERTptAAC（非統合版）をtop-k accuracy、MRR、Entropy@Kで有意に上回る
- 構文的構造の明示的導入がシンボル予測精度を向上

---

#### 1.1.8 Aphasia Rehabilitation with LLM (2024)

- **論文**: "Integration of a large language model with augmentative and alternative communication tool for oncological aphasia rehabilitation"
- **掲載**: Asia-Pacific Journal of Oncology Nursing / PMC 2024
- **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC10821375/

**概要**: がん性失語症リハビリテーションにGPT-4をAACツールと統合する提案。LLMが社会的文脈に応じたコンテンツを生成し、従来の静的・定型的AAC内容の限界を超える。

---

### 1.2 ICL Personalization ― Core Papers

#### 1.2.1 Personalization of LLMs: A Survey (TMLR 2025)

- **論文**: "Personalization of Large Language Models: A Survey"
- **著者**: Zhehao Zhang, Ryan A. Rossi, Branislav Kveton, Yijia Shao, Diyi Yang, Hamed Zamani, et al. (21名)
- **掲載**: Transactions on Machine Learning Research (TMLR), accepted 2025 (arXiv:2411.00027)
- **URL**: https://arxiv.org/abs/2411.00027

**概要**: LLMパーソナライゼーションの包括的サーベイ。2つの主要方向性を統合:
1. **パーソナライズドテキスト生成**: ユーザー固有コンテキストに合わせた生成
2. **下流タスクパーソナライゼーション**: 推薦システム等への応用

**技術的分類** (3レベル):
- **入力レベル**: プロンプティングによるパーソナライズドコンテキスト（ICL含む）
- **モデルレベル**: パーソナライズドアダプター（fine-tuning）
- **目的関数レベル**: パーソナライズド嗜好へのアラインメント

**VoiceReachへの示唆**: VoiceReachは主に「入力レベル」（PVP in system prompt = ICL）を採用。サーベイの分類に照らすと、これはfine-tuningに比べ更新容易性・モデル非依存性で優位だが、パーソナライゼーション精度ではfine-tuningに劣る可能性がある。

---

#### 1.2.2 LaMP: When LLMs Meet Personalization (ACL 2024)

- **論文**: "LaMP: When Large Language Models Meet Personalization"
- **著者**: Alireza Salemi, Sheshera Mysore, Michael Bendersky, Hamed Zamani
- **掲載**: ACL 2024 Long Paper (arXiv:2304.11406)
- **URL**: https://arxiv.org/abs/2304.11406

**概要**: LLMパーソナライゼーションの標準ベンチマーク。7つのパーソナライズドタスク（3分類 + 4生成）。Retrieval Augmentation（用語一致、セマンティック一致、時間考慮型）でユーザープロファイルからパーソナライズドプロンプトを構築。

**主要結果**:
- Retrieval augmentationが7タスク中6タスクで統計的に有意な改善
- ゼロショット vs. few-shot vs. fine-tuned の比較
- ユーザーベース/時間ベースの2つの評価設定

**VoiceReachへの示唆**: PVPの構成要素の中から状況に応じて関連部分を「検索」してプロンプトに含めるRetrieval Augmented Personalizationのアプローチが有効。PVP全体（~2000トークン）を常に含めるよりも、状況に応じた関連部分の選択的組み込みの方が効果的かもしれない。

---

#### 1.2.3 PersonalLLM: Tailoring LLMs to Individual Preferences (ICLR 2025)

- **論文**: "PersonalLLM: Tailoring LLMs to Individual Preferences"
- **掲載**: ICLR 2025 Conference Paper (arXiv:2409.20296)
- **URL**: https://arxiv.org/abs/2409.20296

**概要**: 個人の嗜好多様性を前提としたパーソナライゼーションベンチマーク。従来のアラインメントベンチマークが暗黙に「均一な嗜好」を仮定していたのに対し、異質な潜在的嗜好を持つ多様なユーザーをモデル化。

---

#### 1.2.4 Few-shot Personalization of LLMs with Mis-aligned Responses (2024)

- **論文**: "Few-shot Personalization of LLMs with Mis-aligned Responses"
- **掲載**: arXiv:2406.18678
- **URL**: https://arxiv.org/abs/2406.18678

**概要**: Fermiフレームワーク。少数のユーザー事例と人口統計情報からパーソナライズドプロンプトを漸進的に改善。LLMが自律的にプロンプトを最適化。

---

#### 1.2.5 "Catch Me If You Can?" ― LLMs and Writing Style Imitation (EMNLP 2025 Findings)

- **論文**: "Catch Me If You Can? Not Yet: LLMs Still Struggle to Imitate the Implicit Writing Styles of Everyday Authors"
- **著者**: Zhengxiang Wang et al.
- **掲載**: EMNLP 2025 Findings (arXiv:2509.14543)
- **URL**: https://arxiv.org/abs/2509.14543

**概要**: LLMの暗黙的文体模倣能力を大規模評価。400人以上の実世界著者、モデルあたり40,000以上の生成文を評価。

**主要結果**:
- ニュース・メールなど構造化されたフォーマットではスタイル近似が可能
- ブログ・フォーラムなどカジュアルで多様な文体では困難
- 最適なexemplar（事例）選択戦略は一貫しない ― コンテンツ最適化・長さ最適化がスタイル模倣向上に必ずしも寄与しない
- 評価指標のアンサンブル（著者帰属、著者検証、スタイル一致、AI検出）が単一指標より有効

**VoiceReachへの示唆**: **極めて重要な知見**。ICLのみでは個人の文体完全模倣は困難であることを示す。VoiceReachのPVPアプローチは、暗黙的な文体コピーではなく、明示的なスタイル記述（語彙・語尾・思考パターン等の構造化プロファイル）を提供する点で、この論文の示す課題を回避する設計になっている。明示的PVP > 暗黙的few-shot例示、という仮説を支持。

---

### 1.3 Diverse Response Generation

#### 1.3.1 Exploring and Controlling Diversity in LLM-Agent Conversation (EMNLP 2025)

- **論文**: "Exploring and Controlling Diversity in LLM-Agent Conversation"
- **著者**: KuanChao Chu, Yi-Pei Chen, Hideki Nakayama
- **掲載**: EMNLP 2025 Findings (arXiv:2412.21102)
- **URL**: https://arxiv.org/abs/2412.21102

**概要**: LLMエージェント対話における多様性の探索と制御。長期シミュレーションで対話多様性が劣化する現象を発見。

**主要結果**:
- **全てのプロンプト構成要素が多様性を制約する**が、Memoryが最も影響力が大きい
- **高attention内容が一貫して多様性を抑制** ― 顕著な情報がかえって変動性を低下させるパラドックス
- **Adaptive Prompt Pruning (APP)**: lambdaパラメータ1つで多様性を制御。attention scoreに基づきプロンプトセグメントを動的に削除
- APPは出力の流暢性を完全に維持し、coherence・全体スコアではベースラインを上回る

**VoiceReachへの示唆**: **直接的に適用可能**。VoiceReachの候補生成で、会話履歴（Memory）を増やすほど候補の多様性が低下するリスクがある。APPの知見を応用し、多様性が必要な場合はコンテキストの一部を意図的に省略することで、意図軸の分散を維持できる可能性。

---

#### 1.3.2 Diverse Beam Search (2018)

- **論文**: "Diverse Beam Search: Decoding Diverse Solutions from Neural Sequence Models"
- **著者**: Ashwin K. Vijayakumar, Michael Cogswell, Ramprasaath R. Selvaraju, et al.
- **掲載**: AAAI 2018 (arXiv:1610.02424)
- **URL**: https://arxiv.org/abs/1610.02424

**概要**: 標準beam searchの多様性不足問題を解決。ビームを複数のサブグループに分割し、各タイムステップでグループ間多様性を最大化する内部反復を追加。

**VoiceReachへの示唆**: デコーディング時の多様性制御技術として、候補生成パイプラインに組み込み可能。ただし、VoiceReachの「意図軸による多様性」はデコーディング多様性とは異なるレベルの多様性であり、セマンティックレベルの多様性制御が別途必要。

---

#### 1.3.3 Nucleus Sampling (ICLR 2020)

- **論文**: "The Curious Case of Neural Text Degeneration"
- **著者**: Ari Holtzman, Jan Buys, Li Du, Maxwell Forbes, Yejin Choi
- **掲載**: ICLR 2020
- **URL**: https://openreview.net/forum?id=rygGQyrFvH

**概要**: Top-p (nucleus) samplingの提案。確率質量のp%を含む動的なトークン核から次トークンをサンプリング。

**VoiceReachへの示唆**: 4候補を異なるtemperature/top-p設定で生成し、表面的な多様性を確保する戦略の基盤。ただし、意図レベルの多様性はサンプリングだけでは不十分で、明示的なプロンプト制御が必要。

---

### 1.4 Persona-based Dialogue

#### 1.4.1 Recent Trends in Personalized Dialogue Generation (LREC-COLING 2024)

- **論文**: "Recent Trends in Personalized Dialogue Generation: A Review of Datasets, Methodologies, and Evaluations"
- **掲載**: LREC-COLING 2024 (arXiv:2405.17974)
- **URL**: https://aclanthology.org/2024.lrec-main.1192.pdf

**概要**: パーソナライズド対話生成の包括的サーベイ。22データセット（ベンチマーク+拡張データセット）をカバー。

**主要知見**:
- PersonaChatが依然として標準ベンチマーク（個人的事実に基づくペルソナ記述 + 対話）
- LLMのゼロショット/few-shot ICL能力により、事例提供のみで流暢なカスタマイズ対話生成が可能
- GPT-3等を使ったペルソナ拡張パイプラインの提案

---

#### 1.4.2 PersonalityChat (2024)

- **論文**: "PersonalityChat: Conversation Distillation for Personalized Dialog Modeling with Facts and Traits"
- **掲載**: arXiv:2401.07363
- **URL**: https://arxiv.org/abs/2401.07363

**概要**: PersonaChatを拡張し、ペルソナ事実と性格特性（personality traits）の両方で条件付けした合成対話データセット。性格特性ラベルを用いた生成モデルのパーソナライゼーション。

---

#### 1.4.3 UniMS-RAG: Multi-source RAG for Personalized Dialogue (2024)

- **論文**: "UniMS-RAG: A Unified Multi-source Retrieval-Augmented Generation for Personalized Dialogue Systems"
- **掲載**: arXiv:2401.13256
- **URL**: https://arxiv.org/abs/2401.13256

**概要**: 知識ベース、ウェブページ、ユーザープロファイルなど複数情報源を統合するRAGフレームワーク。パーソナライゼーションモジュールがユーザー固有情報（嗜好、履歴）を組み込み。

**VoiceReachへの示唆**: PVPデータ + 会話履歴 + 環境コンテキスト + 時間帯情報 を統合するVoiceReachのコンテキスト統合エンジンは、UniMS-RAGの multi-source approach と方向性が一致。

---

### 1.5 日本語関連研究

日本語AAC領域におけるLLM活用の学術論文は、英語圏に比べ極めて限定的。CiNii、J-STAGE検索では、LLMと意思伝達装置を直接組み合わせた研究は確認できなかった。

- **意思伝達装置（伝の心、miyasuku等）**: 依然として文字スキャン方式が主流。AI予測入力の統合は公開文献では確認されていない
- **日本語LLM開発**: リコーの130億パラメータモデル（2024年）、NII LLM研究開発センター等が日本語LLM開発を推進しているが、AAC応用は未報告
- **日本語IMEへのLLM統合**: Zenn等の技術ブログでは「LLMは予測変換が得意なのにIMEに搭載されない理由」が議論されているが、推論レイテンシとリソース要求が主要障壁として指摘されている

**VoiceReachへの示唆**: 日本語AAC + LLMは先行研究がほぼ存在せず、VoiceReachは当該領域のフロントランナーとなりうる。英語圏のSpeakFaster、SpeakEase等の知見を日本語に適応する際、日本語固有の課題（文字種の多さ、語順の自由度、敬語体系）への対応が差別化要素。

---

## 2. Existing AAC+AI Products

### 2.1 Commercial Products

| 製品 | 開発元 | AI機能 | 入力方式 | 対象 |
|---|---|---|---|---|
| **Grid 3** | Smartbox | SwiftKey予測、AI Fix（スペル補正・略語展開）、Mind's Eye（AI画像生成） | タッチ/スイッチ/視線 | MND/ALS等 |
| **TD Snap** | Tobii Dynavox | シンボル予測、Google Assistant統合 | タッチ/視線/スイッチ | 幅広い障害 |
| **Proloquo4Text** | AssistiveWare | PolyPredix単語予測エンジン（学習型）、文予測 | タッチ（iOS） | テキストベースAAC |
| **Proloquo2Go** | AssistiveWare | PolyPredix予測、QWERTY + 単語予測 | タッチ（iOS） | シンボル+テキスト |
| **伝の心** | 日立ケーイーシステムズ | 基本的な文字予測（統計的） | スイッチスキャン | ALS等 |
| **miyasuku EyeConSW** | ユニコーン | 基本的な文字予測 | スイッチ/視線 | ALS等 |

### 2.2 Research Prototypes

| システム | 開発元 | 技術 | 状態 |
|---|---|---|---|
| **SpeakFaster** | Google Research + Team Gleason | Fine-tuned LLM x2、略語展開、コンテキスト利用 | フィールドテスト済 |
| **SpeakEase** | Yiwen Xu et al. | Custom GPT、マルチモーダル入力、パーソナライズドTTS | 探索的可行性研究 |
| **SocializeChat** | Liye et al. | GPT-4、ペルソナDB、社会的コンテキスト | プロトタイプ |
| **AMBRA** | Di Paola et al. | Foundation models、連合学習 | プラットフォーム提案段階 |

### 2.3 Key Gap Analysis

現存する製品・研究プロトタイプと比較したVoiceReachの独自性:

1. **意図軸による多様性制御**: 既存システムは全て「最も確からしい1候補」を上位に表示する設計。「意図の異なる4候補を同時提示」というアプローチは見当たらない
2. **PVPの構造的深さ**: SocializeChatのペルソナDBは比較的浅い（話題嗜好+対人親密度）。VoiceReachのPVPは語彙・語尾・思考パターン・対人スタイル・避ける表現を構造化しており、はるかに詳細
3. **視線滞留フィードバックの統合**: 「選ばなかった」ことを次の候補生成に反映する明示的フィードバックループは既存システムにない
4. **感情シグナルの統合**: 候補選択プロセスに感情検出を組み込むシステムは確認されていない
5. **日本語対応**: 日本語LLMベースのAAC候補生成は実質的に未開拓

---

## 3. ICL Personalization Research

### 3.1 ICLパーソナライゼーションの効果

LaMP benchmark（ACL 2024）の結果に基づく知見:

- **Retrieval-augmented ICL**（ユーザープロファイルから関連アイテムを検索しプロンプトに含める方式）が7タスク中6タスクで有意な改善
- **セマンティック検索 > 用語一致検索**: ユーザープロファイルから関連情報を選ぶ際、意味的類似性に基づく検索がキーワード一致より効果的
- **時間考慮型検索**: 最新のユーザー活動を重視する時間ベースの検索もパーソナライゼーションに寄与

### 3.2 ICLの限界

"Catch Me If You Can?" (EMNLP 2025) の知見:

- **構造化テキスト（ニュース・メール）**: ICLでのスタイル模倣はある程度成功
- **非構造化テキスト（ブログ・フォーラム）**: 暗黙的スタイル模倣は依然困難
- **カジュアル会話**: 最も模倣が難しいドメイン ― AAC候補生成の主要ユースケースと重なる

### 3.3 ICL vs Fine-tuning vs RAG

| アプローチ | パーソナライゼーション精度 | 更新容易性 | モデル非依存 | データ効率 | コスト |
|---|---|---|---|---|---|
| ICL（PVP in prompt） | 中~中高 | 極めて容易 | はい | 高い | 推論コストのみ |
| Fine-tuning | 高 | 困難（再訓練要） | いいえ | 低い | 訓練+推論 |
| RAG + ICL | 中高~高 | 容易 | はい | 中 | 検索+推論 |
| LoRA/Adapter | 高 | やや容易 | 部分的 | 中 | 軽量訓練+推論 |

### 3.4 VoiceReachのICL戦略の妥当性

**肯定的側面**:
- PVPは暗黙的スタイルコピーではなく明示的スタイル記述を採用 → "Catch Me If You Can?"の指摘する暗黙的模倣の困難を回避
- モデル非依存性によりClaude/GPT-4o等の切り替えが容易
- 更新がテキスト修正のみで可能（患者の状態変化に適応しやすい）
- ~2000トークンはコンテキストウィンドウの効率的利用

**リスク**:
- カジュアル会話のスタイル模倣はICLの弱点領域
- PVP + 会話履歴 + 状況コンテキストの合計トークン数がコンテキストウィンドウを圧迫する可能性
- 個人差が大きく、PVPの品質がシステム全体の品質を規定

---

## 4. Diverse Generation Techniques

### 4.1 デコーディング多様性 vs 意図的多様性

VoiceReachの候補生成における「多様性」は2つの異なるレベルで必要:

**Level A: 表面的多様性（デコーディング）**
- Temperature、top-p、top-k等のサンプリングパラメータ
- Diverse Beam Search
- 同じ意図内での表現バリエーション

**Level B: 意味的多様性（意図軸）**
- 異なる発話意図のカバー
- VoiceReachの7意図軸フレームワーク
- プロンプトによる明示的制御

既存研究はLevel Aに集中しており、Level Bを体系的に扱う研究は少ない。

### 4.2 意図的多様性の実現手法

#### 4.2.1 明示的指示による分散

最もシンプルかつ効果的な手法。プロンプトで各候補に異なる意図タグを割り当てることを要求。

```
各候補は異なる発話意図を持つこと:
- 候補1: [感情応答]
- 候補2: [質問]
- 候補3: [自分語り]
- 候補4: [行動要求]
```

#### 4.2.2 逐次生成 + 差別化制約

候補を1つずつ生成し、前の候補との差分を明示的に指示:

```
候補2を生成してください。ただし候補1の[感情応答]とは異なる意図軸を使用すること。
```

#### 4.2.3 並列独立生成 + 後処理選択

4つの独立したLLM呼び出しで候補を生成し、最も多様な組み合わせを後処理で選択。Multi-armed bandit的なアプローチ。

#### 4.2.4 Adaptive Prompt Pruning の応用

Chu et al. (EMNLP 2025) のAPPを応用し、多様性を高めたい場合はコンテキスト情報を意図的に間引く。

### 4.3 多様性の評価指標

| 指標 | 説明 | 適用レベル |
|---|---|---|
| **Self-BLEU** | 候補間の相互BLEU（低いほど多様） | 表面的多様性 |
| **Distinct-n** | ユニークなn-gramの割合 | 表面的多様性 |
| **Embedding distance** | 候補間のembedding距離 | 意味的多様性 |
| **Intent axis coverage** | 7意図軸のカバー率 | 意図的多様性 (VoiceReach固有) |
| **Entropy@K** | top-K候補の予測エントロピー | 候補分布の多様性 |

---

## 5. Conversational Response Prediction

### 5.1 State of the Art

#### 5.1.1 Response Selection (Retrieval-based)

- **DCM (Deep Context Modeling)**: BERTをcontext encoderとして使用し、multi-turn対話のcontext continuityをモデル化
- **IoI**: 複数のインタラクション層で発話-応答ペアの意味的関係をself-attentionでモデル化
- **2段階パイプライン**: bi-encoderによる高速recall + cross-encoderによる精密reranking

#### 5.1.2 Response Generation (Generative-based)

- **Next Segment Prediction**: エージェントの応答をターン全体として予測
- **Voice Activity Projection (VAP)**: ストリーミング応答生成。ターン交替予測に基づきLLMが応答生成を開始
- **LLM-based Multi-turn**: 大規模言語モデルを直接multi-turn対話に適用する手法が主流化

#### 5.1.3 Hit Rate の実績値

AAC文脈での予測精度:
- **Word prediction (従来型)**: トップ1候補の命中率 ~30%、トップ5で ~50-60%（Trnka et al.）
- **SpeakFaster (LLM)**: 略語展開の精度は高いが、完全な「意図予測」とは異なる
- **一般的な対話応答予測**: next utterance prediction のRecall@1は研究ベンチマークで30-50%程度

### 5.2 VoiceReachの予測精度目標の妥当性

VoiceReachの目標:
- Level 0（ゼロ操作）: 40-60%命中率
- Level 1（リスニングモード）: 70-80%命中率

**Level 0 (40-60%) の妥当性**:
- 状況コンテキスト（時刻、対話相手、環境）のみからの予測
- 定型的状況（朝の挨拶、介護者入室）では60%以上も十分可能
- 非定型的会話場面では40%でも高い目標
- **先行研究との比較**: 純粋なcontext-based予測としては妥当だが、やや楽観的。初期段階では30-40%を現実的な目標とし、PVPの改善・学習データの蓄積で50-60%を目指す方が安全

**Level 1 (70-80%) の妥当性**:
- 相手の質問に対する回答候補は選択肢が限定的
- 「おかゆ vs うどん」のような二択質問 → 自然に90%+
- オープンエンドな会話 → 50-60%がより現実的
- **加重平均として70-80%は合理的**（質問回答が多い介護場面に限定すれば達成可能）

---

## 6. Comparative Analysis

### 6.1 VoiceReachの位置づけ

```
抽象度: 低 ←────────────────────────────────→ 高

文字予測    単語予測    フレーズ予測   意図予測
  ↑           ↑             ↑            ↑
Gaines     Proloquo    SpeakFaster   VoiceReach
(2025)     4Text       (2024)
                       SpeakEase
                       (2025)
```

VoiceReachは「意図レベル」での候補生成を目指す点で、既存AAC研究の最も抽象度の高いポジションに位置する。

### 6.2 機能比較表

| 機能 | SpeakFaster | SpeakEase | SocializeChat | VoiceReach |
|---|---|---|---|---|
| LLM活用 | Fine-tuned (x2) | Custom GPT | GPT-4 | ICL (PVP) |
| パーソナライゼーション | なし | コンテキスト | ペルソナDB | PVP (~2000t) |
| 候補の多様性制御 | なし | なし | なし | 7意図軸フレームワーク |
| コンテキスト利用 | 会話文脈 | 相手+感情 | 社会的関係 | 時刻+相手+環境+感情+履歴 |
| 入力方式 | 視線タイピング | マルチモーダル | 視線 | 視線+指+まばたき |
| 非選択フィードバック | なし | なし | なし | 視線滞留+感情 |
| 対象言語 | 英語 | 英語 | 英語 | 日本語 (主) |
| 進行度適応 | なし | なし | なし | 4段階適応 |
| TTS統合 | なし | パーソナライズド | なし | パーソナライズド |

### 6.3 VoiceReachの新規性

1. **7意図軸による構造的多様性**: 候補間の「意図の違い」を明示的にフレームワーク化。これは対話システム研究でもAAC研究でも見られないアプローチ
2. **PVPの構造的詳細さ**: 語彙・語尾・思考パターン・対人スタイル・避ける表現を統合した ~2000トークンの構造化プロファイルは、既存のペルソナ記述（通常5-10文の事実記述）よりはるかに豊か
3. **暗黙的フィードバック（視線+感情）の候補生成統合**: 「選ばなかったこと」自体が情報になるという設計は、対話システムにおける暗黙的フィードバック研究（主にrecent-based reranking）とは異質
4. **進行度適応**: ALS進行に伴う入力チャネル・候補数・多様性-命中率バランスの段階的調整は完全に新規
5. **多巡ナビゲーション**: 前巡の視線データ+感情データから次巡の意図軸・抽象度・温度感を自動調整するメカニズム

---

## 7. Prompt Engineering Insights

### 7.1 PVP + 候補生成プロンプトの設計原則

先行研究から抽出される設計原則:

#### 原則1: 明示的スタイル記述 > 暗黙的事例コピー

"Catch Me If You Can?" の知見に基づき、PVPは暗黙的なfew-shot事例よりも明示的なスタイルルール記述を優先すべき。

```
非推奨（暗黙的）:
  以下は{患者名}さんの過去の発言例です:
  - "ありがとね"
  - "まあまあだよ"
  - ...

推奨（明示的）:
  {患者名}さんのスタイル:
  - 感謝表現: 「ありがとね」（家族向け）、「ありがとうございます」（フォーマル）
  - 体調報告: 深刻でも軽めに「まあまあ」「ぼちぼち」と答える傾向
  - 語尾: 疑問形が多い。断定を避ける
  - 避ける表現: 過度に弱気な表現、敬語過剰
```

VoiceReachのPVP設計はすでにこの原則に沿っている。

#### 原則2: コンテキストと多様性のトレードオフを意識的に管理

Chu et al. (EMNLP 2025) の知見:
- 会話履歴を詳細に含めるほど候補の多様性は低下する
- 初回候補生成（多様性重視）ではコンテキストを適度に間引く
- 2巡目以降（命中率重視）ではコンテキストを詳細に含める

```
1巡目プロンプト（多様性重視）:
  コンテキスト: {最小限の状況 + 直前の1発話}
  指示: 4つの異なる意図軸から候補を生成

2巡目プロンプト（命中率重視）:
  コンテキスト: {詳細な状況 + 直近5発話 + 1巡目の視線データ}
  指示: 関心のある意図軸を深掘り
```

#### 原則3: Role Prompting + Persona Conditioning

先行研究が示すシステムプロンプトのベストプラクティス:
- ペルソナの社会人口統計属性、文化的知識、伝記的詳細、文脈依存の態度、行動例を含む "deeply contextualised persona prompting" が最も効果的
- VoiceReachのPVPはすでにこのレベルの詳細さを持つ

#### 原則4: 構造化出力フォーマットの強制

候補の意図軸ラベルを明示的に要求し、後処理での多様性検証を可能にする:

```json
{
  "candidates": [
    {"text": "すごいじゃん！", "intent_axis": "emotional_response", "confidence": 0.8},
    {"text": "何で表彰されたの？", "intent_axis": "question", "confidence": 0.7},
    {"text": "俺も小学校の時なぁ", "intent_axis": "self_reference", "confidence": 0.5},
    {"text": "太郎に電話したいな", "intent_axis": "action_request", "confidence": 0.4}
  ]
}
```

#### 原則5: Retrieval-Augmented PVP

LaMP (ACL 2024) の知見に基づき、PVP全体を毎回含めるのではなく、状況に応じて関連部分を選択的に検索・挿入:

```
対話相手が妻 → PVPのrelational_styles[wife]を優先的に含める
体調に関する会話 → PVPのfrequent_topics[daily_care]を含める
未知の人との会話 → PVPのrelational_styles[unknown]とavoidancesを含める
```

### 7.2 Temperature戦略

4候補に対して異なるsampling設定を使い分けることで、表面レベルの多様性を確保:

| 候補 | Temperature | 意図 |
|---|---|---|
| 候補1 (安全策) | 0.3-0.5 | 最も確からしい応答 |
| 候補2 (準安全策) | 0.5-0.7 | 別の意図軸で確からしい応答 |
| 候補3 (探索的) | 0.7-0.9 | 予想外だが文脈に合った応答 |
| 候補4 (冒険的) | 0.9-1.2 | 意外性のある応答（ユーモア等） |

### 7.3 意図軸選択のためのメタプロンプト

候補生成の前段として、状況コンテキストから「この場面で最も関連する意図軸」を選択するメタプロンプトを挟む:

```
Step 1 (メタプロンプト):
  状況: {context}
  7つの意図軸から、この場面で最も関連する4つを選び、
  各軸の推定使用確率を出力してください。

Step 2 (候補生成プロンプト):
  選択された4意図軸に沿って、それぞれ1つずつ候補を生成してください。
```

この2段階アプローチにより、意図軸選択の合理性を検証可能にする。

---

## 8. Recommendations

### 8.1 プロンプトアーキテクチャ

**推奨構成**:

```
[System Prompt]
├── Role定義: ALS患者の代弁者（VoiceReachアシスタント）
├── PVP（関連部分を検索・選択的に挿入、800-1200トークン）
├── 意図軸フレームワーク定義（7軸の説明、100トークン）
├── 出力フォーマット指示（JSON構造、50トークン）
└── 制約条件（avoidances、スタイルルール、50トークン）

[User Prompt]
├── 状況コンテキスト（時刻、環境、患者状態、200トークン）
├── 対話相手情報（名前、関係、50トークン）
├── 会話履歴（直近3-5発話、200-400トークン）
├── 前巡フィードバック（視線+感情データ、あれば100トークン）
└── 生成指示（巡数・意図軸指定、50トークン）

合計: 1500-2100トークン（入力側）
```

### 8.2 期待命中率の現実的評価

| レベル | VoiceReach目標 | 現実的初期値 | 成熟期の目標 | 根拠 |
|---|---|---|---|---|
| Level 0 (ゼロ操作) | 40-60% | 25-35% | 45-55% | 定型場面のみで60%可能、混合平均は低い |
| Level 1 (リスニング) | 70-80% | 55-65% | 70-80% | 質問応答中心なら達成可能 |
| Level 2 (カテゴリ) | N/A (確実) | 90%+ | 95%+ | 階層メニューのため高精度 |
| Level 3 (文字入力) | N/A (確実) | 80-90% | 90%+ | LLM予測＋文字入力で高精度 |

**注**: 「命中率」の定義を明確化する必要がある。「4候補中1つ以上が許容範囲内」であればTop-4 accuracy、「4候補中1つが完全一致」であれば別の基準が必要。前者の定義であれば上記目標は達成可能性が高い。

### 8.3 評価方法論

#### オフライン評価

1. **過去の会話データからの予測テスト**: 実際の患者の会話ログから{context, actual_response}ペアを抽出し、contextからの候補生成がactual_responseをどの程度カバーするかを評価
2. **意図軸カバレッジ**: 4候補が何種類の意図軸をカバーしているかの平均値
3. **表面多様性**: Self-BLEU、Distinct-1/2/3
4. **意味的多様性**: BERTScore間の候補ペア距離
5. **スタイル一致**: PVPに記載されたスタイル特性との一致率（human evaluation）

#### オンライン評価

1. **Top-4 Hit Rate**: 4候補中1つ以上を患者が選択した割合
2. **巡数分布**: 何巡目で意図に到達したかの分布
3. **操作到達時間**: 意図の発話完了までの時間
4. **Keystroke Saving Rate (KSR)**: 従来の文字入力と比較した操作削減率
5. **患者満足度**: 定期的なアンケート（5段階、視線入力対応）
6. **介護者評価**: 「患者らしい」と感じる割合

#### PVP品質評価

1. **A/Bテスト**: PVPあり vs. PVPなしの候補を家族が評価
2. **ブラインドテスト**: 生成文が「本人の言葉」か「AI生成」かを家族が判定
3. **PVP更新後のスコア変化**: 日次/週次の更新による命中率トレンド

### 8.4 技術的推奨事項

1. **モデル選択**: Claude (Anthropic) または GPT-4o (OpenAI) をクラウド候補として推奨。レイテンシ要件（< 1秒）を満たすstreaming応答が必要
2. **オンデバイスフォールバック**: Llama 3 / Phi-3 等の7-8Bモデルでオフライン時の候補生成を確保
3. **キャッシュ戦略**: 定型場面（朝の挨拶、食事時等）の候補をプリキャッシュし、レイテンシをゼロに近づける
4. **A/Bテスト基盤**: プロンプト構成の比較評価を継続的に行う基盤を初期段階で構築
5. **PVP検索モジュール**: PVP全体のベタ挿入ではなく、状況に応じた関連部分の選択的挿入（Retrieval-augmented PVP）を実装

### 8.5 段階的実装ロードマップへの提言

| フェーズ | 焦点 | 技術 |
|---|---|---|
| Phase 1 | 基本候補生成 | LLM API + 固定プロンプト + 意図軸フレームワーク |
| Phase 2 | PVP統合 | PVP抽出パイプライン + ICL統合 + Retrieval-augmented PVP |
| Phase 3 | フィードバック統合 | 視線滞留 + 感情データ → 2巡目生成の最適化 |
| Phase 4 | 個人適応 | 使用ログからのPVP自動更新 + 意図軸確率の個人化 |
| Phase 5 | 進行度適応 | Stage別候補数/多様性/命中率の動的バランス調整 |

---

## 9. Open Questions

### 9.1 技術的課題

1. **日本語でのICL personalization精度**: 英語での研究結果が日本語に転移するか。日本語の敬語体系、語尾変化の豊かさ、主語省略等の特性がICLパーソナライゼーションに与える影響は不明
2. **7意図軸の最適性**: 7軸は設計者の仮説。実際のALS患者の会話データから、より妥当な軸の数・種類を検証する必要がある。コーパス分析による検証が推奨される
3. **レイテンシ制約下での多様性**: 4候補を十分に多様にするためのLLM呼び出し戦略（1回 vs 複数回）とレイテンシのトレードオフ。1回の呼び出しで4候補を出すか、4回の並列呼び出しで1候補ずつ出すか
4. **PVPのトークン予算**: ~2000トークンのPVPが常に最適とは限らない。Retrieval-augmented PVPにおける関連部分の選択精度
5. **感情信号の信頼性**: 微弱な感情シグナル（ALS患者の表情筋低下環境下）が候補生成フィードバックとして十分な信号強度を持つか

### 9.2 評価に関する課題

6. **「命中」の定義**: 「言いたいことに近い」「方向は合っている」「完全に一致」のどのレベルを命中とするか。段階的命中率（0: 全く違う / 0.5: 方向は合っている / 1.0: ほぼ一致）の導入
7. **長期的適応効果の測定**: PVPの更新による命中率改善がプラトーに達するまでの時間
8. **個人差**: 患者間でPVP+ICLの有効性が大きく異なる可能性。個人差要因（言語使用の豊かさ、発症前データの量・質）の特定

### 9.3 倫理的課題

9. **代弁の限界**: AIが生成した候補が「患者の本当に言いたかったこと」でない場合の検知方法。特に、PVPに基づく「その人らしさ」の再現が実際の現在の意図と乖離する可能性
10. **自律性の保持**: 予測精度が高まるほど、患者がシステムの提案に「従わされる」リスク。多様性を維持するコストと命中率向上のトレードオフは、本質的に患者の自律性の問題

### 9.4 未探索の研究方向

11. **マルチモーダル候補生成**: 画像・ジェスチャーをコンテキストとしてLLMに入力する候補生成（外向きカメラのVLM活用）
12. **協調生成**: 介護者と患者のペア特有のコミュニケーションパターンをモデル化し、双方向の候補生成を行う
13. **感情表出としての候補**: テキスト候補だけでなく、非言語的表現（嘆息、うなずき、笑い）の候補も含める

---

## 参考文献一覧

### LLM for AAC

1. Cai, S., Venugopalan, S., Tomanek, K., et al. (2024). "Using large language models to accelerate communication for eye gaze typing users with ALS." *Nature Communications*. https://www.nature.com/articles/s41467-024-53873-3
2. Di Paola, A., Muraro, S., Marinelli, R., Pilato, C. (2024). "Foundation Models in Augmentative and Alternative Communication: Opportunities and Challenges." *arXiv:2401.08866*. https://arxiv.org/abs/2401.08866
3. Gaines, D., Vertanen, K. (2025). "Adapting Large Language Models for Character-based Augmentative and Alternative Communication." *Findings of EMNLP 2025*. https://arxiv.org/abs/2501.10582
4. Xu, Y., Chakraborti, M., Zhang, T., Eng, K., Mohan, A., Prpa, M. (2025). "Your voice is your voice: Supporting Self-expression through Speech Generation and LLMs in Augmented and Alternative Communication." *arXiv:2503.17479*. https://arxiv.org/abs/2503.17479
5. Cai, S., et al. (2023). "The less I type, the better: How AI Language Models can Enhance or Impede Communication for AAC Users." *CHI 2023*. https://dl.acm.org/doi/10.1145/3544548.3581560
6. Liye et al. (2023/2025). "SocializeChat: a GPT-based AAC Tool for Social Communication Through Eye Gazing." *UbiComp 2023*. https://dl.acm.org/doi/10.1145/3594739.3610705; Updated: https://arxiv.org/abs/2510.19017
7. Pereira, J., Rodrigues, F., Pereira, J., Zanchettin, C., Fidalgo, R. (2024). "Enhancing Augmentative and Alternative Communication with Card Prediction and Colourful Semantics." *arXiv:2405.15896*. https://arxiv.org/abs/2405.15896

### ICL Personalization

8. Zhang, Z., Rossi, R.A., Kveton, B., et al. (2025). "Personalization of Large Language Models: A Survey." *TMLR*. https://arxiv.org/abs/2411.00027
9. Salemi, A., Mysore, S., Bendersky, M., Zamani, H. (2024). "LaMP: When Large Language Models Meet Personalization." *ACL 2024*. https://arxiv.org/abs/2304.11406
10. PersonalLLM (2025). "Tailoring LLMs to Individual Preferences." *ICLR 2025*. https://arxiv.org/abs/2409.20296
11. Wang, Z., et al. (2025). "Catch Me If You Can? Not Yet: LLMs Still Struggle to Imitate the Implicit Writing Styles of Everyday Authors." *EMNLP 2025 Findings*. https://arxiv.org/abs/2509.14543

### Diverse Generation

12. Chu, K., Chen, Y.-P., Nakayama, H. (2025). "Exploring and Controlling Diversity in LLM-Agent Conversation." *EMNLP 2025 Findings*. https://arxiv.org/abs/2412.21102
13. Vijayakumar, A.K., et al. (2018). "Diverse Beam Search: Decoding Diverse Solutions from Neural Sequence Models." *AAAI 2018*. https://arxiv.org/abs/1610.02424
14. Holtzman, A., Buys, J., Du, L., Forbes, M., Choi, Y. (2020). "The Curious Case of Neural Text Degeneration." *ICLR 2020*.

### Persona-based Dialogue

15. "Recent Trends in Personalized Dialogue Generation." *LREC-COLING 2024*. https://aclanthology.org/2024.lrec-main.1192.pdf
16. "PersonalityChat: Conversation Distillation for Personalized Dialog Modeling." *arXiv:2401.07363*. https://arxiv.org/abs/2401.07363
17. "UniMS-RAG: A Unified Multi-source Retrieval-Augmented Generation for Personalized Dialogue Systems." *arXiv:2401.13256*. https://arxiv.org/abs/2401.13256

### AAC Communication Rate

18. Trnka, K., McCaw, J. (2008). "Word prediction and communication rate in AAC." *Proc. IASTED Telehealth/AT*. https://www.eecis.udel.edu/~mccoy/publications/2008/trnka08at.pdf

### RAG Personalization

19. "Improving RAG for Personalization with Author Features and Contrastive Examples." *arXiv:2504.08745*. https://arxiv.org/abs/2504.08745
20. "Crafting Personalized Agents through Retrieval-Augmented Generation." *EMNLP 2024*. https://aclanthology.org/2024.emnlp-main.281.pdf

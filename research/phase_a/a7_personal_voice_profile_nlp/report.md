# A7 -- Personal Voice Profile / NLP 調査レポート

## メタ情報

| 項目 | 内容 |
|------|------|
| エリア | Phase A - A7 |
| 調査日 | 2026-02-17 |
| 調査者 | Claude Opus 4.6（AI Research Assistant） |
| ステータス | 初版完了 |
| 関連設計書 | `docs/03_PERSONAL_VOICE_PROFILE.md` |

---

## 1. リサーチクエスチョンへの回答

### RQ1: 著者推定（authorship attribution）の手法で、個人の文体・語彙特徴をどの程度抽出できるか？

#### 概要

著者推定（Authorship Attribution）とスタイロメトリ（Stylometry / 計量文献学）は、テキストの文体的特徴から著者を特定する手法の総称であり、VoiceReachのPVP（Personal Voice Profile）構築に直接応用可能な技術基盤を提供する。

#### 手法の分類と精度

**1. 古典的スタイロメトリ特徴量:**

- 語彙的特徴: 語彙豊富度、語長分布、特定語の使用頻度
- 統語的特徴: 品詞nグラム、文長分布、句構造パターン
- 文字レベル特徴: 文字nグラム、句読点使用パターン
- 内容非依存特徴: 機能語（助詞・助動詞）の使用頻度

**2. 深層学習アプローチ（2024-2025の主流）:**

- CNN、RNN、Transformerアーキテクチャが語彙・統語・文字レベルの特徴ベクトルをスタイロメトリクスとして抽出する
- これらのモデルは従来手法が見落としがちな複雑な言語パターンやニュアンスを捉える能力を持つ
- Twitter、ブログ、レビュー、小説、エッセイなど様々なデータセットで評価されている

**3. 最新動向（LLMとの関係）:**

- スタイロメトリは人間が書いたテキストとLLM生成テキストを短いサンプルでも区別できることが実証されている（arXiv, 2025）
- PAN 2025では文レベルの著者変更検出タスクが新たに導入され、スタイル分析の粒度が段落レベルから文レベルに細分化されている
- Google DeepMindがテキスト透かし技術を2024年にNatureで発表するなど、著者特定とAI検出が融合する傾向にある

#### 日本語著者推定の研究

日本語の計量文献学（計量文体学）は以下の特徴量を用いる:

- 語または文の長さ
- 特定の単語や品詞の使用率
- 同義語の使い分け
- 句読点パターン
- 592名の日本語著者による592小説（950万文字）のコーパスを用いた研究が存在する

**VoiceReach向け結論**: 著者推定の手法は個人の文体・語彙特徴の抽出に十分な精度を持ち、PVP構築のパターン抽出層（Round 1: 語彙・表現の癖、Round 2: 思考パターン・論理構造）に直接活用できる。特に機能語（助詞・助動詞）の使用パターンは言語横断的に個人識別力が高く、日本語でも有効である。

---

### RQ2: 日本語の文体特徴（文末表現、助詞使用、敬語レベル、方言的特徴）を自動分析する手法・ツールは？

#### 形態素解析による文体特徴抽出

日本語のスタイル分析には形態素解析が基盤となる。以下のツールが文体分析に活用可能である。

**1. MeCab + IPAdic / NEologd:**

- 最も広く使われる形態素解析器
- 品詞タグ付け: 名詞、動詞、形容詞、副詞、助詞等の分類
- 文末表現（終助詞「ね」「よ」「な」等）の検出が可能
- ただし7年以上更新されておらず、新語対応が弱い

**2. Sudachi / SudachiPy:**

- Works Applications開発のビジネス向けトークナイザ
- 3段階の分割粒度（A: 最短、B: 中間、C: 固有表現）を提供
- 表記揺れの正規化機能（「お母さん」「おかあさん」「お母様」の統一等）
- 辞書定義に忠実なトークン分割
- 処理速度はMeCabより遅いが、品質は高い

**3. GiNZA v5（spaCyベース）:**

- Universal Dependenciesに基づく日本語NLPライブラリ
- 形態素解析 + 依存構造解析 + 固有表現認識を一体提供
- v5.2.0（2024年3月）で日本語節認識API（実験的）を追加
- Transformersモデル（ja_ginza_electra）により高精度な構文解析を実現
- 文体分析に必要な品詞情報、依存関係、名詞句境界をすべて提供

#### 敬語レベルの自動判定

- Feely et al.（2019）が日本語の文をinformal / polite / formalの3レベルに分類する手法を提案
- 2022年にACL DCLRLワークショップで日本語敬語コーパス（10,007文）が公開された
- ルールベース、ロジスティック回帰、SVM、Transformerベースの各モデルが評価されている
- ただし、敬語のランク付けと言い換えに関する研究は依然として限定的で、(1) コーパスの不足と (2) 既存NLPモデルの敬語処理の未成熟が課題

#### 文体特徴の抽出パイプライン提案

```
入力テキスト
    |
    v
[形態素解析 (GiNZA/Sudachi)]
    |
    +-- 品詞分布 → 機能語使用パターン
    +-- 終助詞抽出 → 文末表現パターン（「ね」「よ」「な」等）
    +-- 活用形分析 → 敬語レベル推定
    +-- 依存構造 → 文の複雑度・構造パターン
    |
    v
[統計的特徴量算出]
    |
    +-- 語彙豊富度（TTR, Yule's K等）
    +-- 文長分布（平均、分散）
    +-- 品詞nグラム頻度
    +-- 敬語使用率（尊敬語/謙譲語/丁寧語の比率）
    +-- 文末表現分布
    |
    v
[LLMによるパターン解釈]
    |
    +-- 統計的特徴量を自然言語で要約
    +-- PVPの各セクションにマッピング
```

**VoiceReach向け推奨**: GiNZA v5を主軸とし、Sudachiの表記揺れ正規化機能を併用する。敬語レベルの判定はGiNZAの品詞情報 + ルールベースの敬語パターンマッチングで実装し、対人スタイル（relational_styles）の自動推定に活用する。

---

### RQ3: LLMのペルソナ対話（persona-based dialogue）の最新手法と、少数サンプル（50-100文程度）から個人のスタイルを学習する方法は？

#### ペルソナ対話の最新研究動向

2024-2025年にLLMペルソナの研究が急速に発展している。

**1. 主要サーベイ論文:**

- "Two Tales of Persona in LLMs: A Survey of Role-Playing and Personalization"（EMNLP 2024 Findings）: ロールプレイとパーソナライゼーションの2軸でLLMペルソナ研究を体系化
- "A Survey of Personalized Large Language Models"（arXiv, 2025）: プロンプティング、ファインチューニング、アラインメントの3アプローチを整理

**2. ペルソナ手法の分類:**

| 手法 | 概要 | 少数サンプル適用性 |
|------|------|-------------------|
| Role Prompting | "You are X..."形式でペルソナを指定 | 高（プロンプトのみ） |
| Deeply Contextualized Persona Prompting | 経歴・社会的文脈・信念・経験を含む構造化プロンプト | 高（VoiceReachのPVPに近い） |
| RAG + Persona | ユーザー履歴からキーワード抽出 → 関連パッセージ検索 → ペルソナブロック生成 | 中（データベース構築が必要） |
| Test-time Persona Alignment | ペルソナプロンプトを反復的に書き換えてテキスト損失を最小化 | 高（ファインチューニング不要） |
| Soft Prompt Tuning | ペルソナを学習可能な連続埋め込みとしてエンコード | 低（学習データが必要） |
| PersonaAgent with GraphRAG | ユーザーインタラクショングラフからペルソナを抽出、統計サマリに圧縮 | 中 |

**3. 少数サンプル（50-100文）からのスタイル学習:**

**課題**: 最新の研究（"Catch Me If You Can? Not Yet: LLMs Still Struggle to Imitate the Implicit Writing Styles of Everyday Authors", arXiv, 2025）では、LLMは著名人やフィクションキャラクターのスタイル模倣には優れるが、**一般ユーザーの暗黙的な文体の模倣は依然として困難**であることが示されている。

**有効なアプローチ:**

1. **構造化プロファイル + Few-shot例文**: VoiceReachのPVP設計（構造化YAMLプロファイル + example_utterances）はこの課題に対する有効なアプローチ。プロファイルで「何を」言うかを規定し、例文で「どう」言うかを示す。

2. **TinyStyler（2024-2025）**: 効率的な少数ショットテキストスタイル変換手法。パラメータ効率的なファインチューニングが有効。

3. **パラメータ効率的ファインチューニング（PEFT）**: LoRAなどのアダプタを少数サンプルで学習する手法が、ゼロショットやfew-shotプロンプティングよりも大幅にスタイル再現精度を向上させる。

4. **段階的プロファイル構築**: VoiceReachの5ラウンド逐次抽出（語彙 → 思考パターン → 対人スタイル → 話題傾向 → 回避パターン）は、少数データからの段階的な特徴抽出として合理的な設計である。

**VoiceReach向け結論**: 50-100文程度からのスタイル学習は、(1) 構造化PVP + (2) example_utterances（5-10文/相手別）+ (3) In-Context Learningの組み合わせで実現可能。ただし、一般ユーザーの暗黙的文体の完全な再現は現在のLLMでは限界があるため、PVPの精度をユーザーフィードバックで漸進的に改善する仕組みが重要である。

---

### RQ4: VoiceReachのPVP（約2000トークンの構造化プロファイル）をLLMシステムプロンプトに埋め込む際のベストプラクティスは？

#### 構造化ペルソナプロンプトのベストプラクティス

**1. プロンプト構造の設計原則:**

- **"You are X..." 形式の直接ロールプレイ**: モデルが一人称でペルソナとして動作する形式が最も効果的
- **ペルソナテンプレートの構造化**: 経歴、社会的文脈、信念、経験を含む多段落の構造化プロンプトが有効
- **最小限の効果的スキャフォールディングから始める**: TOP-2（上位2属性）や粗い属性で十分な場合も多い。過度に詳細なプロファイルが必ずしも精度向上につながるわけではない
- **大規模モデルが必ずしもペルソナ忠実度を保証しない**: プロンプト設計とインストラクションチューニングが重要

**2. VoiceReachのPVP埋め込みに関する具体的推奨:**

```
[System Prompt 構造]

Part 1: ロール定義（~100トークン）
  "あなたは{患者名}さんの発話を代弁するアシスタントです。"
  + 基本的な行動指針

Part 2: PVP本体（~1500トークン）
  YAML形式の構造化プロファイル
  - vocabulary（語彙・表現の癖）
  - thinking_patterns（思考パターン）
  - relational_styles（対人スタイル）-- 現在の対話相手のみ
  - frequent_topics（頻出トピック）-- 上位5件のみ
  - avoidances（避ける表現）

Part 3: 制約ルール（~200トークン）
  - 語彙・語尾の忠実再現
  - 対話相手に応じたスタイル切替
  - avoidancesの厳守
  - 候補の意図軸分散

Part 4: Few-shot例文（~200トークン）
  - 現在の対話相手向けの例文3-5件
```

**3. 動的プロファイル選択（トークン節約）:**

2000トークン全体をシステムプロンプトに含めるのではなく、現在のコンテキストに応じて関連部分のみを選択的に埋め込むアプローチが推奨される。

- 対話相手に応じて該当するrelational_stylesのみを含める
- 時間帯・状況に応じて関連するfrequent_topicsを優先する
- RAGパイプラインでタスク入力からキーワード抽出 → 関連PVPセクションを検索する手法も有効

**4. 評価と反復改善:**

- ペルソナ忠実度を人口レベルの調査データやファセットリッチなデータセットで根拠づける
- ペルソナ特徴量が説明する分散の限界効果を定量化してから大規模展開する
- VoiceReachでは「家族が"らしい"と評価した割合 80%以上」というKPIが設定されており、これを評価指標とする

---

### RQ5: プロファイルの自動更新（会話ログからの学習・更新）の技術的アプローチは？

#### 最新の研究動向

LLMのパーソナライゼーションにおけるプロファイル自動更新は2024-2025年の活発な研究領域である。

**1. Apple MLR - "On the Way to LLM Personalization: Learning to Remember User Conversations"（ICLR L2M2 2025）**

- PLUM（Personalized Language Understanding and Memory）フレームワーク
- 会話データを質問-回答ペアにデータ拡張でアップサンプリング
- 重み付きクロスエントロピー損失でLoRAアダプタをファインチューニング
- ユーザーの会話履歴から嗜好を「記憶」するモデルを実現

**2. PersonalLLM ベンチマーク（ICLR 2025）**

- パーソナライズされたモデルは個々のユーザーの嗜好とニーズに適応すべき
- 類似ユーザーの履歴データから新しいユーザーのフィードバックを効率的に学習する方法を提案
- インタラクションの蓄積に伴い最大限の利益を提供する設計

**3. Persistent Memory and User Profiles（arXiv, 2025）**

- LLMエージェントの持続的メモリとユーザープロファイルによる長期パーソナライゼーション
- ユーザープロファイルはLLMにより暗黙的に生成され、継続的に洗練される
- 人口統計、嗜好、興味、性格特性、会話特性（トーン、コミュニケーション嗜好）を含む
- インタラクション中にエージェントが会話コンテキストを受け取り、プロファイルカテゴリを新情報で更新

**4. Personalized LLMs Survey（arXiv, 2025）**

技術的アプローチの3分類:
- **Prompting for Personalized Context**: プロンプトにパーソナライズされたコンテキストを組み込む
- **Finetuning for Personalized Adapters**: パーソナライズされたアダプタのファインチューニング
- **Alignment for Personalized Preferences**: パーソナライズされた嗜好へのアラインメント

#### VoiceReach向けの自動更新設計

```
[日次更新プロセス]

1. 会話ログの収集
   - その日の全発話（選択された候補テキスト）
   - 不採用候補（選ばれなかった候補）
   - 文字入力で直接入力されたテキスト

2. パターン検出（LLMバッチ処理）
   入力: 当日の会話ログ + 現在のPVP
   処理:
   - 新しい語彙・表現パターンの検出
   - PVPに記載のない新しい表現が使われたか？
   - 既存の表現パターンと矛盾する使用はあったか？
   - 新しい話題・関心事の検出

3. 差分レポートの生成
   出力:
   - 追加候補: "「だるい」を「しんどい」の同義語として追加"
   - 修正候補: "文末「〜だよね」の使用頻度が増加"
   - 削除候補: "「〜じゃん」の使用が減少傾向"

[週次統合]

4. 差分の統合判定
   - 3回以上出現したパターンのみ候補とする（ノイズ排除）
   - confidenceスコアを算出
   - PVPの該当セクションに反映

[月次レビュー]

5. 家族/本人による確認
   - 自動更新の提案をリスト表示
   - 承認/拒否/修正のフィードバック
   - 拒否されたパターンをネガティブ例として記録

[随時更新]

6. 明示的フィードバック
   - "こうは言わない" → avoidancesに追加
   - "これは自分らしい" → example_utterancesに追加
   - 候補選択時の「修正して選択」からの学習
```

**技術的注意点:**

- メモリ保持と更新メカニズムにより、関連情報の効率的な検索を可能にする
- 継続学習による動的メモリが時間経過に伴い適応する
- ただし、入力制約下（ALS進行後）のデータは表現の簡略化を伴うため、重み付けを低くする必要がある（PVP設計の `weight: 0.5` に一致）

---

### RQ6: 日本語の自然言語処理ツール（MeCab, Sudachi, GiNZA等）の比較と、VoiceReachでの活用方法は？

#### ツール比較

| 特徴 | MeCab | Sudachi / SudachiPy | GiNZA v5 |
|------|-------|---------------------|----------|
| **開発元** | 京都大学（奈良先端大） | Works Applications | Megagon Labs |
| **ライセンス** | BSD/LGPL/GPL | Apache 2.0 | MIT |
| **最終更新** | 2013年頃（本体） | 継続的更新 | 2024年3月（v5.2.0） |
| **形態素解析** | 高速・高精度 | 高精度・3段階粒度 | spaCyベース |
| **依存構造解析** | なし | なし | UD準拠。Transformer対応 |
| **固有表現認識** | なし | C分割モードで対応 | GSK2014-Aベースのモデル |
| **表記揺れ正規化** | なし | あり（強力） | なし |
| **新語対応** | NEologd辞書で対応 | 継続更新辞書 | BCCWJ準拠 |
| **処理速度** | 最速 | 低速（MeCab比） | 中速 |
| **Python統合** | fugashi経由 | SudachiPy | spaCy API |
| **節認識** | なし | なし | v5.2.0で実験的対応 |

**2024年12月の比較研究（arXiv: 2412.17361）の結論:**

- Sudachiは辞書定義に最も忠実なトークンを生成する
- MeCabとSentencePieceは処理速度で優れる
- 感情分析タスクではSentencePiece + TF-IDF + Logistic Regressionが最高性能

#### VoiceReachでの活用方法

**1. PVP抽出パイプラインでの活用:**

```
[データソース] → [正規化層] → [形態素解析] → [特徴量抽出] → [LLM解釈]

形態素解析ステージ:
  GiNZA v5 を使用:
    - 品詞タグ付け → 助詞・助動詞の使用パターン分析
    - 依存構造解析 → 文の複雑度・構造パターン
    - 固有表現認識 → 話題・人物の抽出

  Sudachi を補助的に使用:
    - 表記揺れ正規化 → 同一表現の統合
    - 3段階分割 → 語彙分析の粒度調整
```

**2. リアルタイム候補評価での活用:**

```
LLM生成候補 → GiNZA形態素解析 → PVPとの整合性チェック

チェック項目:
  - 文末表現がPVPのsentence_endingsに合致するか
  - 敬語レベルが対話相手のrelational_stylesに合致するか
  - avoidancesに記載された表現が含まれていないか
  - 語彙選択がword_choicesに合致するか
```

**3. 会話ログ分析での活用:**

```
選択された候補テキスト → GiNZA解析 → パターン検出

検出パターン:
  - 新しい語彙・表現の出現
  - 文末表現パターンの変化
  - 敬語レベルの変化
  - 話題キーワードの抽出
```

**VoiceReach向け推奨**: GiNZA v5を主軸として採用する。理由は (1) 依存構造解析まで一体で提供、(2) spaCy APIによる統合の容易さ、(3) Transformerモデル（ja_ginza_electra）による高精度、(4) 2024年も継続的にメンテナンスされている点である。Sudachiは表記揺れ正規化が必要な場面で補助的に使用する。MeCabは処理速度が重要なリアルタイム処理でのフォールバックとして位置づける。

---

## 2. 文献レビュー

### 2.1 著者推定・スタイロメトリ

| # | 論文タイトル | 出版 | 年 | 主な知見 |
|---|---|---|---|---|
| 1 | Deep Learning for Stylometry and Authorship Attribution: a Review | IJRASET | 2024 | CNN, RNN, Transformerによるスタイロメトリの包括的レビュー |
| 2 | Authorship Attribution Methods, Challenges, and Future Directions: A Comprehensive Survey | Information (MDPI) | 2024 | 著者推定手法の体系的分類。課題と将来方向を整理 |
| 3 | Stylometry recognizes human and LLM-generated texts in short samples | arXiv | 2025 | スタイロメトリによる人間/LLMテキストの短サンプル識別 |
| 4 | Stylometry Analysis of Multi-authored Documents for Author Style Change Detection | arXiv | 2024 | 多著者文書のスタイル変更検出手法 |
| 5 | Overview of PAN 2024: Multi-author Writing Style Analysis | CEUR-WS | 2024 | 段落レベルの著者変更検出タスク |
| 6 | Overview of PAN 2025: Multi-author Writing Style Analysis | Springer | 2025 | 文レベルの著者変更検出に進化。Easy/Medium/Hardの3データセット |

### 2.2 ペルソナ対話・LLMパーソナライゼーション

| # | 論文タイトル | 出版 | 年 | 主な知見 |
|---|---|---|---|---|
| 7 | Two Tales of Persona in LLMs: A Survey of Role-Playing and Personalization | EMNLP 2024 Findings | 2024 | ロールプレイとパーソナライゼーションの2軸で体系化 |
| 8 | PersonalLLM | ICLR 2025 | 2025 | パーソナライゼーションベンチマーク。ユーザー嗜好への適応を評価 |
| 9 | A Persona-Aware LLM-Enhanced Framework for Multi-Session Dialogue | ACL 2025 Findings | 2025 | マルチセッション対話でのペルソナ一貫性維持 |
| 10 | On the Way to LLM Personalization: Learning to Remember User Conversations | ICLR L2M2 2025 / Apple MLR | 2025 | PLUMフレームワーク。会話記憶のためのLoRA学習 |
| 11 | Enabling Personalized Long-term Interactions through Persistent Memory and User Profiles | arXiv | 2025 | 持続的メモリとユーザープロファイルによる長期パーソナライゼーション |
| 12 | A Survey of Personalized Large Language Models | arXiv | 2025 | プロンプティング・ファインチューニング・アラインメントの3軸整理 |
| 13 | OpenCharacter: Training Customizable Role-Playing LLMs with Large-Scale Synthetic Personas | arXiv | 2025 | 20Kの合成キャラクター + 306K対話ペアによるロールプレイLLM訓練 |
| 14 | PersoDPO: Scalable Preference Optimization for Persona-Grounded Dialogue | arXiv | 2025 | Multi-LLM評価によるペルソナ対話の嗜好最適化 |
| 15 | Recent Trends in Personalized Dialogue Generation | LREC-COLING 2024 | 2024 | パーソナライズ対話生成のデータセット・手法・評価の動向 |

### 2.3 テキストスタイル転送

| # | 論文タイトル | 出版 | 年 | 主な知見 |
|---|---|---|---|---|
| 16 | Catch Me If You Can? LLMs Still Struggle to Imitate Implicit Writing Styles of Everyday Authors | arXiv | 2025 | LLMは一般ユーザーの暗黙的文体模倣が困難 |
| 17 | TinyStyler: Efficient Few-Shot Text Style Transfer | UPenn | 2024-2025 | 少数ショットでの効率的テキストスタイル変換 |
| 18 | Controlling Arbitrary Style in Text with LLMs | LREC-COLING 2024 | 2024 | LLMによる任意テキストスタイルの制御 |
| 19 | LLM one-shot style transfer for Authorship Attribution and Verification | arXiv | 2025 | ワンショットスタイル転送による著者推定 |
| 20 | Text Style Transfer with Parameter-efficient LLM Finetuning | arXiv | 2025 | PEFTによるスタイル変換。LoRAの有効性を実証 |

### 2.4 日本語NLP・文体分析

| # | 論文タイトル | 出版 | 年 | 主な知見 |
|---|---|---|---|---|
| 21 | Construction and Validation of a Japanese Honorific Corpus | ACL DCLRL 2022 | 2022 | 10,007文の日本語敬語コーパス構築 |
| 22 | Automatic Classification of Japanese Formality | ANLP 2023 | 2023 | 日本語の形式度自動分類。ルールベース〜Transformerまで比較 |
| 23 | Computational Politeness in NLP: A Survey | ACM Computing Surveys | 2024 | 計算的丁寧さの包括的サーベイ |
| 24 | An Experimental Evaluation of Japanese Tokenizers for Sentiment-Based Text Classification | arXiv | 2024 | Sudachi, MeCab, SentencePieceの感情分析タスクでの比較。SentencePiece+TF-IDF+LRが最高性能 |
| 25 | Sudachi: a Japanese Tokenizer for Business | LREC 2018 | 2018 | Sudachiの設計と多段階分割・正規化機能 |

### 2.5 ペルソナ対話データセット

| # | 論文タイトル / データセット | 出版 | 年 | 主な知見 |
|---|---|---|---|---|
| 26 | PersonaChat | arXiv | 2018 | 10.9K対話。ペルソナ記述文5文ずつ付与 |
| 27 | Multi-Session Chat (MSC) | Facebook AI | 2022 | PersonaChatのセッション2-5。5Kの継続対話 |
| 28 | Synthetic-Persona-Chat | Google Research | 2023 | PersonaChatの合成拡張版 |
| 29 | Post Persona Alignment for Multi-Session Dialogue | arXiv | 2025 | 応答後のペルソナ検索による一貫性向上 |
| 30 | LMSYS-Chat-1M | ICLR 2024 | 2024 | 25 LLMとの100万対話。210K IPアドレスから収集 |

---

## 3. OSSプロジェクト調査

### 3.1 日本語形態素解析・NLPツール

| 名称 | GitHub URL | Stars | ライセンス | VoiceReach適用性 |
|------|-----------|-------|-----------|-----------------|
| **GiNZA v5** | github.com/megagonlabs/ginza | ~800+ | MIT | **高**。spaCyベース。形態素解析+依存構造+固有表現。Transformer対応。VoiceReachの主軸NLPツールとして推奨 |
| **SudachiPy** | github.com/WorksApplications/SudachiPy | ~400+ | Apache 2.0 | **高**。3段階粒度分割、表記揺れ正規化。PVP抽出の前処理に有用 |
| **MeCab (fugashi)** | github.com/polm/fugashi | ~300+ | BSD | **中**。最高速。リアルタイム処理のフォールバックとして有用 |
| **spaCy** | github.com/explosion/spaCy | ~30K+ | MIT | **高**。GiNZAの基盤。多言語対応、パイプライン管理 |
| **awesome-japanese-nlp-resources** | github.com/taishi-i/awesome-japanese-nlp-resources | ~2K+ | CC0 | **参考**。日本語NLPリソースの包括的リスト |

### 3.2 著者推定・スタイル分析

| 名称 | GitHub URL | Stars | ライセンス | VoiceReach適用性 |
|------|-----------|-------|-----------|-----------------|
| **Stylo (R)** | github.com/computationalstylistics/stylo | ~300+ | GPL | **中**。R言語の計量文献学ライブラリ。分析には有用だが本番統合は困難 |
| **PAN shared tasks** | pan.webis.de | -- | 研究用 | **高**。著者推定の最新ベンチマーク・手法の参照 |
| **PersonaLLM-Survey** | github.com/MiuLab/PersonaLLM-Survey | ~100+ | 不明 | **参考**。LLMペルソナ研究のキュレーションリスト |
| **awesome-llm-role-playing-with-persona** | github.com/Neph0s/awesome-llm-role-playing-with-persona | ~200+ | 不明 | **参考**。LLMロールプレイ研究のリソースリスト |

### 3.3 ペルソナ対話データセット

| 名称 | 規模 | ライセンス | VoiceReach適用性 |
|------|------|-----------|-----------------|
| **PersonaChat** | 10.9K対話 | 研究用 | **中**。英語のみ。ペルソナ対話の基礎データセット |
| **Multi-Session Chat (MSC)** | 5K対話（4-5セッション） | 研究用 | **中**。長期対話でのペルソナ一貫性研究に参考 |
| **Synthetic-Persona-Chat** | PersonaChat拡張 | 研究用 | **中**。合成データによるペルソナ対話の拡張 |
| **LMSYS-Chat-1M** | 100万対話 | 研究用 | **低**。大規模LLM対話データだがパーソナライゼーション特化ではない |

### 3.4 日本語感情・テキストデータセット

| 名称 | 規模 | ライセンス | VoiceReach適用性 |
|------|------|-----------|-----------------|
| **WRIME** | 35,000投稿 | 研究用 | **高**。日本語感情強度推定。PVPの感情表現パターン分析に利用可能 |
| **Japanese Honorific Corpus** | 10,007文 | 研究用 | **高**。敬語レベル分類。relational_stylesの自動推定に有用 |

---

## 4. 商用製品・サービス

| 製品名 | 提供元 | 主な機能 | VoiceReach適用性 |
|--------|--------|---------|-----------------|
| **Claude API** | Anthropic | LLM API。System prompt対応。構造化出力 | **高**。PVP埋め込みのシステムプロンプトとして直接利用。VoiceReachの候補生成エンジンに既に選定 |
| **GPT-4o API** | OpenAI | LLM API。System/User/Assistant形式 | **高**。Claude APIの代替候補 |
| **LIWC** | Pennebaker Lab | 言語的特徴量分析（英語中心） | **低**。日本語対応が限定的 |
| **Character.ai** | Character Technologies | ペルソナベース対話 | **低**。エンターテインメント用途。医療・福祉適用には不向き |

---

## 5. VoiceReach向け推奨事項

### 5.1 技術選定の推奨

1. **日本語NLPスタック**: GiNZA v5（主軸）+ SudachiPy（表記揺れ正規化）+ fugashi/MeCab（高速フォールバック）

2. **PVP抽出パイプライン**: 設計ドキュメントの5ラウンド逐次抽出を維持しつつ、以下を追加:
   - Round 0（前処理）: GiNZAによる形態素解析 + Sudachiによる正規化
   - 各Roundに統計的特徴量（品詞分布、文末表現分布、語彙豊富度）を補助入力として追加

3. **LLMペルソナ制御**: 構造化YAMLプロファイル + 対話相手別のfew-shot例文 + 動的プロファイル選択（コンテキスト依存の部分埋め込み）

4. **プロファイル自動更新**: 日次差分検出 → 週次統合（3回以上出現パターンのみ） → 月次レビュー（家族承認）の3層構成

### 5.2 実装優先順位

```
Phase 2（9-15ヶ月）:
  1. データソースコネクタ（Gmail API, LINEエクスポート）
  2. GiNZA + Sudachi による前処理パイプライン
  3. LLMバッチ処理による5ラウンド逐次抽出
  4. PVP管理UI（確認・編集）
  5. PVP埋め込みのシステムプロンプト設計
  6. 基本的な対話相手別スタイル切替

Phase 3（15-24ヶ月）:
  7. 日次/週次の自動更新パイプライン
  8. 動的プロファイル選択（コンテキスト依存の部分埋め込み）
  9. PVP精度のA/B テスト（PVPあり vs なし）
  10. 家族フィードバックによる反復改善
```

### 5.3 研究課題

1. **少数サンプルからの日本語スタイル学習の精度評価**: 50-100文の日本語テキストからPVPを構築した場合の「らしさ」再現度を定量評価する必要がある。

2. **敬語レベルの自動推定精度**: 対話相手別の敬語切替の精度を評価。既存コーパス（10,007文）でのベンチマークを実施する。

3. **プロファイル更新の安定性**: 自動更新が元の人格を壊さないことの検証。特に入力制約下（ALS進行後）のデータによる不適切な更新の防止策。

4. **LLMモデル依存性の低減**: PVPはモデル非依存を設計原則としているが、実際のペルソナ忠実度はモデルにより差がある。複数モデルでの評価が必要。

5. **プライバシーとデータ最小化**: メール・LINE・SNSデータの取り扱いにおけるプライバシー保護。ローカル処理を基本とし、クラウドへの送信を最小化する設計。

### 5.4 KPI目標との整合

設計ドキュメントの「PVP抽出精度: 家族が"らしい"と評価した割合 80%以上」を達成するために:

- データソース: 最低200件以上のテキストデータ（メール+LINE+SNS）を推奨
- 対話相手: 最低3名以上の対話相手別データを確保
- 評価方法: ブラインド評価（PVPあり候補 vs PVPなし候補を家族が比較）
- 反復改善: 月次レビューで家族のフィードバックを反映し、段階的に精度を向上

---

## 6. 参考文献リスト

1. Deep Learning for Stylometry and Authorship Attribution. *IJRASET*, 2024. https://www.ijraset.com/best-journal/deep-learning-for-stylometry-and-authorship-attribution-a-review-of-literature
2. Authorship Attribution Methods, Challenges, and Future Directions. *Information (MDPI)*, 2024. https://www.mdpi.com/2078-2489/15/3/131
3. Stylometry recognizes human and LLM-generated texts in short samples. *arXiv*, 2025. https://arxiv.org/pdf/2507.00838
4. Stylometry Analysis of Multi-authored Documents. *arXiv*, 2024. https://arxiv.org/html/2401.06752v1
5. Overview of PAN 2024: Multi-author Writing Style Analysis. *CEUR-WS*, 2024. https://ceur-ws.org/Vol-3740/paper-222.pdf
6. PAN at CLEF 2025 - Multi-Author Writing Style Analysis. https://pan.webis.de/clef25/pan25-web/style-change-detection.html
7. Two Tales of Persona in LLMs: A Survey of Role-Playing and Personalization. *EMNLP 2024 Findings*. https://aclanthology.org/2024.findings-emnlp.969/
8. PersonalLLM. *ICLR 2025*. https://proceedings.iclr.cc/paper_files/paper/2025/file/a730abbcd6cf4a371ca9545db5922442-Paper-Conference.pdf
9. A Persona-Aware LLM-Enhanced Framework for Multi-Session Dialogue. *ACL 2025 Findings*. https://aclanthology.org/2025.findings-acl.5.pdf
10. On the Way to LLM Personalization: Learning to Remember User Conversations. *Apple MLR / ICLR L2M2 2025*. https://machinelearning.apple.com/research/on-the-way
11. Enabling Personalized Long-term Interactions through Persistent Memory and User Profiles. *arXiv*, 2025. https://arxiv.org/abs/2510.07925
12. A Survey of Personalized Large Language Models. *arXiv*, 2025. https://arxiv.org/abs/2502.11528
13. OpenCharacter: Training Customizable Role-Playing LLMs. *arXiv*, 2025. https://arxiv.org/html/2501.15427v1
14. PersoDPO: Scalable Preference Optimization for Persona-Grounded Dialogue. *arXiv*, 2025. https://arxiv.org/html/2602.04493v1
15. Recent Trends in Personalized Dialogue Generation. *LREC-COLING 2024*. https://aclanthology.org/2024.lrec-main.1192.pdf
16. Catch Me If You Can? LLMs Still Struggle to Imitate Implicit Writing Styles. *arXiv*, 2025. https://arxiv.org/html/2509.14543v1
17. TinyStyler: Efficient Few-Shot Text Style Transfer. *UPenn*, 2024-2025. https://www.cis.upenn.edu/~ccb/publications/tinystyler.pdf
18. Controlling Arbitrary Style in Text with LLMs. *LREC-COLING 2024*. https://aclanthology.org/2024.lrec-main.1328.pdf
19. LLM one-shot style transfer for Authorship Attribution. *arXiv*, 2025. https://arxiv.org/html/2510.13302v1
20. Text Style Transfer with Parameter-efficient LLM Finetuning. *arXiv*, 2025. https://arxiv.org/html/2602.15013
21. Construction and Validation of a Japanese Honorific Corpus. *ACL DCLRL 2022*. https://aclanthology.org/2022.dclrl-1.3.pdf
22. Automatic Classification of Japanese Formality. *ANLP 2023*. https://www.anlp.jp/proceedings/annual_meeting/2023/pdf_dir/D2-5.pdf
23. Computational Politeness in NLP: A Survey. *ACM Computing Surveys*, 2024. https://dl.acm.org/doi/10.1145/3654660
24. An Experimental Evaluation of Japanese Tokenizers for Sentiment-Based Text Classification. *arXiv*, 2024. https://arxiv.org/abs/2412.17361
25. Sudachi: a Japanese Tokenizer for Business. *LREC 2018*. https://aclanthology.org/L18-1355.pdf
26. PersonaChat: Personalizing Dialogue Agents. *arXiv*, 2018. https://arxiv.org/pdf/1801.07243
27. Synthetic-Persona-Chat. *Google Research*. https://github.com/google-research-datasets/Synthetic-Persona-Chat
28. Post Persona Alignment for Multi-Session Dialogue. *arXiv*, 2025. https://arxiv.org/html/2506.11857v1
29. LMSYS-Chat-1M. *ICLR 2024*. https://arxiv.org/abs/2309.11998
30. GiNZA v5. *Megagon Labs*. https://github.com/megagonlabs/ginza
31. SudachiPy. *Works Applications*. https://github.com/WorksApplications/SudachiPy
32. fugashi: a Tool for Tokenizing Japanese in Python. https://ar5iv.labs.arxiv.org/html/2010.06858
33. awesome-japanese-nlp-resources. https://github.com/taishi-i/awesome-japanese-nlp-resources
34. WRIME Dataset. *NAACL 2021*. https://github.com/ids-cv/wrime
35. PersonaLLM-Survey. https://github.com/MiuLab/PersonaLLM-Survey
36. Persona-L: Leveraging LLMs for Personas of People with Complex Needs. *CHI 2025*. https://dl.acm.org/doi/10.1145/3706598.3713445
37. Comparing Styles across Languages: Cross-Cultural Exploration of Politeness. *arXiv*, 2023. https://arxiv.org/html/2310.07135v3
38. TYDIP: A Dataset for Politeness Classification in Nine Languages. *EMNLP 2022 Findings*. https://aclanthology.org/2022.findings-emnlp.420.pdf
39. 計量文献学. *Wikipedia*. https://ja.wikipedia.org/wiki/%E8%A8%88%E9%87%8F%E6%96%87%E7%8C%AE%E5%AD%A6
40. Deeply Contextualised Persona Prompting. *Emergent Mind*. https://www.emergentmind.com/topics/deeply-contextualised-persona-prompting

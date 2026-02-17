# 03 — Personal Voice Profile（PVP）の設計と運用

## 1. PVPの目的と位置づけ

Personal Voice Profile（PVP）は、患者の文体・語彙・思考パターン・対人スタイルを構造化した個人プロファイルである。システムアーキテクチャ（01章）のLayer 3（インテリジェンス層）において、三段ハイブリッドLLM推論のシステムプロンプトに埋め込まれ、In-Context Learning（ICL）により「その人らしさ」を再現する。

PVPは以下の3つの役割を担う。

1. **スタイル規定**: 語彙・語尾・思考パターン等の明示的な記述により、LLMが生成する候補文のスタイルを制御する
2. **対人適応**: 対話相手ごとの文体切替（妻/医師/孫/看護師等）を可能にする
3. **進行度追従**: ALS進行に伴う文体変化を段階的に反映し、プロファイルを生きた文書として維持する

### 1.1 なぜファインチューニングではなくICLか

調査レポートA3（LLM x AAC）が示すとおり、LLMパーソナライゼーションには入力レベル（ICL）、モデルレベル（ファインチューニング）、目的関数レベル（アラインメント）の3アプローチが存在する [A3: TMLR 2025 Survey]。VoiceReachがICLを主軸とする根拠を以下に整理する。

| 観点 | ファインチューニング | PVP + ICL |
|---|---|---|
| 更新容易性 | モデル再訓練が必要 | YAML編集のみ |
| モデル依存 | 特定モデルに固定 | 任意のLLM（Qwen3/Gemini/Claude）で利用可能 |
| データ量 | 大量のペアデータが必要 | 数百件の文例で十分 |
| 可搬性 | モデルごと移動が必要 | YAMLファイル1つで移動可能 |
| 透明性 | ブラックボックス | プロファイルを人間が確認・編集可能 |
| コスト | GPU時間が必要 | 追加コスト不要 |
| 三段ハイブリッド対応 | 各モデルに個別訓練が必要 | 同一PVPを全段で共有 |

**ICLの限界と対策**: 調査レポートA3が引用する "Catch Me If You Can?"（EMNLP 2025 Findings）は、LLMが一般ユーザーの暗黙的文体模倣に困難を抱えることを示した [A3: 1.2.5]。特にカジュアル会話はICLの弱点領域である。VoiceReachのPVPはこの課題を、暗黙的なfew-shot事例コピーではなく**明示的なスタイルルール記述**で回避する設計となっている [A3: 7.1 原則1]。

**Retrieval-Augmented PVP**: LaMP（ACL 2024）の知見に基づき、PVP全体（~2000トークン）を毎回含めるのではなく、状況に応じて関連セクションを選択的に検索・挿入するRetrieval-Augmented Personalizationを採用する [A3: 1.2.2]。これによりトークン予算を効率化しつつ、パーソナライゼーション精度を向上させる。

### 1.2 ICL vs ファインチューニング vs RAG: 精度比較

| アプローチ | パーソナライゼーション精度 | 更新容易性 | モデル非依存 | データ効率 |
|---|---|---|---|---|
| ICL（PVP in prompt） | 中~中高 | 極めて容易 | はい | 高い |
| Fine-tuning | 高 | 困難（再訓練要） | いいえ | 低い |
| **RAG + ICL（VoiceReach採用）** | **中高~高** | **容易** | **はい** | **中** |
| LoRA/Adapter | 高 | やや容易 | 部分的 | 中 |

出典: [A3: 3.3 ICL vs Fine-tuning vs RAG]

---

## 2. PVPのデータ構造

PVPは~2000トークンのYAML構造として定義する。この上限は、三段ハイブリッド推論（01章 5.2）のプロンプトキャッシュ設計における `layer_1_static`（~2300トークン = PVP + 基本タスク指示）との整合に基づく。

### 2.1 構造概要

```yaml
personal_voice_profile:
  version: "2.0"
  patient_id: "xxx-xxx"
  last_updated: "2026-02-17T14:00:00+09:00"

  data_sources:
    - type: "gmail"
      records: 1250
      date_range: "2018-01 ~ 2025-06"
    - type: "line"
      records: 8400
      date_range: "2020-03 ~ 2025-08"
    - type: "voice_recording"
      hours: 12.5
      date_range: "2024-01 ~ 2025-03"

  # ===== Section 1: スタイロメトリ特徴量 =====
  # GiNZA v5 + SudachiPy による自動抽出 [A7: RQ2]
  stylometry:
    lexical_diversity:
      ttr: 0.72                    # Type-Token Ratio
      yules_k: 105.3               # Yule's K（低いほど語彙豊富）
      note: "同世代男性の平均（TTR 0.65）より語彙豊富"
    sentence_length:
      mean: 18.5                   # 平均文長（形態素数）
      std: 8.2                     # 標準偏差
      distribution: "右裾が長い（短文が多く、時々長い説明文）"
    particle_usage:                # 助詞使用パターン [A7: RQ1]
      frequent: ["は", "が", "も", "で"]
      characteristic: "「も」の使用頻度が高い（他者への配慮・含意の表現）"
      avoids: "「のに」（不満表現を避ける傾向と一致）"
    formality_level:               # 敬語レベル自動判定 [A7: RQ2]
      default: "casual"
      distribution:
        informal: 0.55
        polite: 0.35
        formal: 0.10

  # ===== Section 2: 語彙と表現の癖 =====
  vocabulary:
    preferred_expressions:
      - pattern: "感謝"
        typical: "ありがとね"
        context: "家族に対して。フォーマルな場では「ありがとうございます」"
      - pattern: "謝罪"
        typical: "ごめんね" / "悪いね"
        avoids: "すみません"（ほとんど使わない）
      - pattern: "同意"
        typical: "そうだよね" / "だよなぁ"
      - pattern: "体調報告"
        typical: "まあまあ" / "ぼちぼち"
        note: "深刻でも軽めに答える傾向"

    sentence_endings:
      casual: ["〜だよね", "〜かな", "〜だなぁ", "〜じゃん"]
      neutral: ["〜ですね", "〜だと思います"]
      emphasis: ["〜だよ！", "〜でしょ！"]
      frequency_note: "疑問形の語尾が多い。断定を避ける傾向。"
      # GiNZA終助詞抽出による自動更新対象 [A7: RQ2]

    fillers_and_openers:
      - "そうだなぁ"（考え始め）
      - "あ、そういえば"（話題転換時）
      - "ちょっと"（依頼の前置き）
      - "なんかさ"（カジュアルな話題導入）

    word_choices:
      - domain: "食事"
        preferences: "ごはん（「食事」とは言わない）、うまい（「美味しい」より多用）"
      - domain: "体調"
        preferences: "しんどい（「辛い」より多用）、だるい、きつい"

  # ===== Section 3: 思考パターン =====
  thinking_patterns:
    structure:
      - "結論を先に言わず、背景や経緯から話し始める"
      - "「〜だけど、でも〜」のように一度譲歩してから本題に入る"
      - "相手の気持ちへの言及を必ず含める"
    reasoning_style:
      - "具体例をよく使う（「たとえば〜」が多い）"
      - "数字や事実を根拠にする傾向（エンジニア出身）"
    humor:
      - "自虐的なユーモアが多い"
      - "ダジャレは言わない"
      - "相手を笑わせようとする場面：緊張をほぐしたいとき"

  # ===== Section 4: 対人スタイル =====
  relational_styles:
    - relation: "wife"
      name: "花子"
      tone: "casual, warm, slightly playful"
      formality: "informal"          # GiNZA敬語レベル推定と連動 [A7: RQ2]
      characteristics:
        - "遠慮なく要望を伝える"
        - "感謝は短くても必ず添える"
        - "体調が悪くても心配させないよう明るく振る舞う"
      example_utterances:
        - "花子さん、ありがとね。無理しないでね"
        - "あ、ちょっとトイレお願い"
        - "今日も一日おつかれさま"

    - relation: "doctor"
      name: "田中先生"
      tone: "polite but direct, informative"
      formality: "polite"
      characteristics:
        - "症状を正確に伝えようとする"
        - "質問は具体的"
        - "余計な世間話はしない"
      example_utterances:
        - "先生、左足の痺れが3日前から強くなっています"
        - "薬を飲んだ後、2時間くらいで効果が薄れる感じがします"

    - relation: "children"
      name: "太郎（孫）、美咲（娘）"
      tone: "playful, encouraging, proud"
      formality: "informal"
      characteristics:
        - "褒めることが多い"
        - "冗談を言いたがる"
        - "成長を喜ぶ表現が多い"
      example_utterances:
        - "太郎すごいじゃん！"
        - "美咲に似て頭いいなぁ"

    - relation: "nurse"
      tone: "polite, appreciative, concise"
      formality: "polite"
      characteristics:
        - "短く要件を伝える"
        - "必ずお礼を言う"
      example_utterances:
        - "吸引お願いします"
        - "ありがとうございます、助かります"

    - relation: "unknown"
      tone: "polite, neutral"
      formality: "polite"
      default_style: "ですます調、丁寧だが堅すぎない"

  # ===== Section 5: 頻出トピックと定型表現 =====
  frequent_topics:
    daily_care:
      - category: "体位"
        expressions: ["体勢を少し右に", "背中がかゆい", "足を上げてほしい"]
      - category: "排泄"
        expressions: ["トイレお願い", "尿器お願い"]
      - category: "環境"
        expressions: ["エアコン下げて", "テレビ消して", "カーテン閉めて"]
      - category: "食事"
        expressions: ["水が欲しい", "もう少し食べたい", "もういい"]
      - category: "医療"
        expressions: ["吸引お願い", "薬の時間", "痛い"]
    emotional:
      - "ありがとう、助かるよ"
      - "大丈夫、心配しないで"
      - "今日は調子いいよ"
    interests:
      - topic: "野球"
        detail: "阪神タイガースファン。試合結果を気にする"
      - topic: "孫"
        detail: "太郎の学校の話を聞きたがる"
      - topic: "技術"
        detail: "元エンジニア。新しいガジェットに興味"

  # ===== Section 6: 避ける表現 =====
  avoidances:
    - "過度に弱気な表現（「もう無理」「死にたい」等は本人の意思に反する）"
    - "敬語過剰（家族に対して「〜していただけますか」等は不自然）"
    - "子供扱いされるような表現"
    - "直接的な不満表現（「嫌だ」より「ちょっと困るなぁ」を好む）"

  # ===== Section 7: 音声特性メモ（TTS連携用） =====
  voice_characteristics:
    pace: "ややゆっくり。考えながら話す"
    pitch: "中低音。落ち着いた声"
    laugh: "控えめだが頻繁。鼻で笑うことが多い"
    emotional_expression: "声のトーンよりも言葉選びで感情を表す"

  # ===== Section 8: Progressive Decay 設定 =====
  # ALS進行に伴う文体変化への追従 [A7: RQ5]
  progressive_decay:
    current_stage: "early"           # early / moderate / advanced / locked-in
    data_weights:
      pre_onset: 1.0                 # 発症前データ（語彙・表現パターンの基盤）
      post_onset_mobile: 0.8         # 発症後・入力制約前（話題や関心事の更新）
      post_onset_constrained: 0.5    # 発症後・入力制約後（意図は参考、表現は割引）
      current_usage_log: 0.3         # 現在の使用ログ（最新の好み反映、システム依存表現を除外）
    decay_policy: "weighted_merge"   # 新しいパターンは重み付きで既存に統合
```

### 2.2 動的・選択的エンベディング

PVP全体（~2000トークン）を常にシステムプロンプトに含めるのではなく、対話状況に応じて関連セクションを選択的に埋め込む [A7: RQ4, A3: 7.1 原則5]。

```
推論時のPVPプロンプト構成:

Part 1: 常時埋め込み（~500トークン）
  - stylometry（スタイロメトリ特徴量の要約）
  - vocabulary（語彙・表現の癖）
  - avoidances（避ける表現）

Part 2: 対話相手に応じて選択（~300トークン）
  - relational_styles[{current_relation}] のみを含める
  - 例: 妻との会話 → relational_styles[wife]
  - 未知の人 → relational_styles[unknown]

Part 3: 状況に応じて選択（~200トークン）
  - 関連するfrequent_topicsの上位カテゴリのみ
  - 例: 食事時 → frequent_topics[daily_care][食事]
  - 例: 孫の来訪 → frequent_topics[interests][孫]

Part 4: Few-shot例文（~200トークン）
  - 現在の対話相手向けのexample_utterances 3-5件
  - 会話ログRAGで取得した類似状況での過去発話 [A7: RQ5]

合計: 800-1200トークン（フルPVPの40-60%）
```

この動的選択はRetrieval-Augmented PVPパイプライン（後述 3.5節）により実現する。

---

## 3. 抽出パイプライン

### 3.1 全体フロー

```
[データソース群]
  ├→ Gmail API → 送信メール本文
  ├→ LINE トーク履歴エクスポート → テキスト
  ├→ SNS アーカイブ（X, Facebook）→ 投稿テキスト
  ├→ 音声録音 → ASR → テキスト + パラ言語特徴
  ├→ ブログ / 文書 → テキスト
  └→ 手紙（スキャン）→ OCR → テキスト

      ↓

[正規化層]
  各ソースのデータを統一フォーマットに変換（3.3節）
      ↓

[Round 0: NLP前処理層] ★ 新設 [A7: 5.1推奨]
  GiNZA v5 + SudachiPy による形態素解析・正規化
  MeCab (fugashi) による高速フォールバック
      ↓

[サンプリング層]
  相手別 x 時期別 x チャネル別にクラスタリング
  各クラスタから代表サンプルを抽出
      ↓

[パターン抽出層]（LLMバッチ処理 + 統計的特徴量）
  段階的に抽出:
    Round 1: 語彙・表現の癖 + スタイロメトリ特徴量
    Round 2: 思考パターン・論理構造
    Round 3: 対人スタイル（相手別）+ 敬語レベル推定
    Round 4: トピック傾向・定型表現
    Round 5: 避ける表現・NGパターン
      ↓

[統合・圧縮層]
  各Roundの結果をマージし、重複排除・矛盾解消
  最終PVPを生成（~2000トークン以内）
      ↓

[検証層]
  家族/本人にPVPを提示して確認
  修正フィードバックを反映
```

### 3.2 日本語NLP解析スタック

調査レポートA7（RQ6）の比較評価に基づき、以下の3層構成を採用する。

| 優先度 | ツール | 役割 | 選定理由 |
|--------|--------|------|----------|
| 1（主軸） | **GiNZA v5**（spaCyベース） | 形態素解析 + 依存構造解析 + 固有表現認識 | UD準拠、Transformerモデル（ja_ginza_electra）、品詞/依存関係/節認識を一体提供 [A7: RQ2] |
| 2（補助） | **SudachiPy** | 表記揺れ正規化 + 3段階粒度分割 | 「お母さん」「おかあさん」「お母様」等の統一。辞書定義に忠実なトークン分割 [A7: RQ6] |
| 3（高速FB） | **MeCab**（fugashi経由） | リアルタイム処理のフォールバック | 最高速の形態素解析。リアルタイム候補評価での使用 [A7: RQ6] |

**スタック構成図**:

```
入力テキスト
    │
    ├→ [SudachiPy] 表記揺れ正規化（前処理）
    │     └→ 3段階分割: A（最短）/ B（中間）/ C（固有表現）
    │
    ▼
[GiNZA v5 + ja_ginza_electra]
    │
    ├→ 品詞タグ付け → 助詞・助動詞の使用パターン分析
    ├→ 終助詞検出 → 文末表現パターン（「ね」「よ」「な」等）
    ├→ 活用形分析 → 敬語レベル推定（informal / polite / formal）
    ├→ 依存構造解析 → 文の複雑度・構造パターン
    └→ 固有表現認識 → 人名・地名・組織名の抽出
    │
    ▼
[統計的特徴量算出]
    │
    ├→ 語彙豊富度（TTR, Yule's K）
    ├→ 文長分布（平均、標準偏差）
    ├→ 品詞nグラム頻度
    ├→ 敬語使用率（尊敬語/謙譲語/丁寧語の比率）
    └→ 文末表現分布
    │
    ▼
[LLMによるパターン解釈]
    │
    ├→ 統計的特徴量を自然言語で要約
    └→ PVPの各セクションにマッピング
```

出典: [A7: RQ2 文体特徴の抽出パイプライン提案]

### 3.3 データソース別コネクタ仕様

#### Gmail

```
取得方法: Gmail API（OAuth2認証）
対象: 送信メールのみ（受信メールは相手のデータ）
フィルタ:
  - 自動返信・不在通知を除外
  - テンプレート文面を除外
  - 一定文字数以下（10文字以下）を除外
抽出情報:
  - 本文テキスト
  - 宛先（相手の推定関係性）
  - 送信日時
  - 件名（話題の手がかり）
```

#### LINE

```
取得方法: トーク履歴エクスポート機能（テキストファイル）
対象: 患者本人の発言のみ抽出
フィルタ:
  - スタンプ/画像/動画の通知行を除外
  - URL共有のみの行を除外
抽出情報:
  - 発言テキスト
  - 相手名（トークルーム名から推定）
  - 日時
  - 前後の文脈（相手の発言も参考用に保持）
```

#### 音声録音

```
取得方法: 音声ファイル（WAV/MP3/M4A）を直接入力
処理:
  1. 話者分離（Speaker Diarization）→ 患者の発話区間を特定
  2. 音声認識（ASR）→ テキスト化
  3. パラ言語特徴量抽出:
     - 発話速度（WPM）
     - ピッチパターン（平均、分散、文末の上下）
     - ポーズの長さと頻度
     - 笑い声の頻度と種類
     - 声の大きさの変動
抽出情報:
  - テキスト + タイムスタンプ
  - パラ言語特徴メタデータ
  - 相手情報（手動アノテーション or 話者認識）
```

### 3.4 正規化フォーマット

```json
{
  "id": "msg_001",
  "source": "line",
  "timestamp": "2024-06-15T18:30:00+09:00",
  "patient_text": "今日は暑かったね。ビール飲みたいな",
  "patient_text_normalized": "今日は暑かったね。ビール飲みたいな",
  "recipient_relation": "wife",
  "recipient_name": "花子",
  "context": {
    "prior_messages": [
      {"speaker": "花子", "text": "ただいま〜、暑かった〜"}
    ]
  },
  "nlp_features": {
    "ginza_analysis": {
      "pos_tags": ["名詞", "助詞", "形容詞", ...],
      "sentence_endings": ["ね", "な"],
      "dependency_depth": 3,
      "formality": "informal"
    },
    "sudachi_normalized": "今日は暑かったね。ビール飲みたいな"
  },
  "metadata": {
    "channel": "chat",
    "estimated_tone": "casual",
    "topic_tags": ["weather", "food_drink", "desire"],
    "data_weight": 1.0
  }
}
```

### 3.5 Retrieval-Augmented PVP パイプライン

会話ログをベクトル化して保持し、推論時に類似状況の過去発話を動的に取得してPVPを補強する [A3: 1.2.2 LaMP, A7: RQ5]。

```
[会話ログDB]
  各発話を以下のメタデータとともにベクトルDB（Qdrant / ChromaDB）に格納:
    - テキスト埋め込みベクトル
    - 対話相手
    - 時間帯
    - 話題カテゴリ
    - 感情状態

[推論時の動的取得]
  1. 現在のコンテキスト（相手、話題、時間帯）をクエリとして検索
  2. 類似度上位3-5件の過去発話を取得
  3. PVPのPart 4（Few-shot例文）として挿入
  4. 時間考慮型検索: 最新の発話を優先的に重み付け

[取得例]
  状況: 妻が食事を持ってきた場面
  取得される過去発話:
    - "おぉ、うまそう。ありがとね"（2025-03-15）
    - "今日はおかゆ？ちょっと味噌汁も欲しいな"（2025-02-28）
    - "ごちそうさま。美味しかったよ"（2025-04-10）
```

### 3.6 スタイロメトリ特徴量の抽出

調査レポートA7（RQ1）が示す著者推定（Authorship Attribution）の手法をPVP構築に応用する。

#### 抽出する特徴量

| カテゴリ | 特徴量 | 抽出ツール | PVPでの用途 |
|---------|--------|-----------|-------------|
| 語彙的特徴 | TTR、Yule's K、語長分布 | GiNZA + Python統計 | `stylometry.lexical_diversity` |
| 統語的特徴 | 品詞nグラム、文長分布 | GiNZA | `stylometry.sentence_length` |
| 機能語パターン | 助詞・助動詞の使用頻度 | GiNZA | `stylometry.particle_usage` |
| 文末表現 | 終助詞の分布 | GiNZA終助詞検出 | `vocabulary.sentence_endings` |
| 敬語レベル | informal/polite/formal比率 | GiNZA活用形分析 + ルールベース | `stylometry.formality_level` |
| 文字レベル | 句読点パターン、絵文字使用 | 正規表現 | `vocabulary`への補足 |

出典: [A7: RQ1] 日本語の計量文献学（計量文体学）研究に基づく

#### 敬語レベルの自動推定

Feely et al.（2019）の3段階分類（informal / polite / formal）を基盤とし、GiNZAの品詞情報 + ルールベースの敬語パターンマッチングで実装する [A7: RQ2]。

```
推定ルール:
  informal: 常体（「だ」「だよ」「じゃん」等）
  polite: 丁寧語（「です」「ます」等）
  formal: 尊敬語 + 謙譲語（「いらっしゃる」「申し上げる」等）

対人スタイルへの適用:
  各relational_styleのformalityフィールドに自動設定
  → LLM候補生成時の敬語レベル制御に使用
```

### 3.7 パターン抽出プロンプト（Round 1 例）

```
以下は{患者名}さんが{相手}に送ったメッセージ群です。
（{ソース名}、{期間}、{件数}件）

## 統計的特徴量（GiNZA v5 + SudachiPy解析結果）
- 語彙豊富度: TTR={ttr}, Yule's K={yules_k}
- 平均文長: {mean_len}形態素（標準偏差 {std_len}）
- 文末表現分布: {ending_distribution}
- 助詞使用パターン: {particle_pattern}
- 敬語レベル: informal {inf_ratio}% / polite {pol_ratio}% / formal {form_ratio}%

## 指示
上記の統計的特徴量を参考に、メッセージ群から{患者名}さんの語彙と表現の癖を抽出してください。

具体的には：
1. よく使う言い回し・フレーズ（5つ以上）
   - どういう場面で使うかも記述
2. 特徴的な語尾パターン（3つ以上）
3. 口癖・フィラー表現
4. 特定の単語の選好（例：「美味しい」vs「うまい」）
5. 避けている表現があれば

必ず原文からの引用例を添えてください。
引用は「」で囲み、どのメッセージからの引用か番号で示してください。

[メッセージデータ: 200件分]
```

---

## 4. PVPの運用

### 4.1 推論時のプロンプト構成

01章（5.1, 5.4）の三段ハイブリッド推論およびプロンプトキャッシュ設計と整合させた構成。

```
[System] ← layer_1_static（キャッシュ対象、~2300トークン）
あなたは{患者名}さんの発話を代弁するアシスタントです。

{患者名}さんのPersonal Voice Profile:
---
{PVP 動的選択済み部分（800-1200トークン）}
---

以下のルールを厳守してください:
- {患者名}さんの語彙・語尾・表現の癖を忠実に再現する
- 対話相手に応じたスタイルを使い分ける（formalityレベルを厳守）
- avoidancesに記載された表現は絶対に使わない
- 候補はそれぞれ異なる「発話意図」を持つこと

[User] ← layer_3_dynamic（キャッシュしない）
現在の状況:
- 時刻: {timestamp}
- 対話相手: {recipient_name}（{relation}）
- 相手の直前の発話: "{last_speech}"
- 環境: {scene_description}
- 患者の状態: {patient_state}
- 直近の会話: {conversation_history}

参考: 類似状況での過去の発話（RAG取得）:
{retrieved_past_utterances}

{患者名}さんが返しそうな応答を4つ生成してください。
各候補に[意図タグ]を付けてください。
短い候補から順に並べてください。
```

### 4.2 リアルタイム候補評価

LLMが生成した候補が PVP に準拠しているかを、MeCab（高速フォールバック）で即時チェックする [A7: RQ6]。

```
LLM生成候補 → MeCab形態素解析（<5ms）→ PVP整合性チェック

チェック項目:
  - 文末表現がPVPのsentence_endingsに合致するか
  - 敬語レベルが対話相手のrelational_styles.formalityに合致するか
  - avoidancesに記載された表現が含まれていないか
  - 語彙選択がword_choicesに合致するか

不合致の場合:
  - 軽微（語尾の不一致等）→ 自動修正して出力
  - 重大（avoidances違反等）→ 候補を破棄して再生成
```

### 4.3 自動更新メカニズム

調査レポートA7（RQ5）の最新研究（Apple MLR PLUMフレームワーク、Persistent Memory and User Profiles等）に基づく3層更新構成。

```
[日次: パターン検出]

  1. 会話ログの収集
     - その日の全発話（選択された候補テキスト）
     - 不採用候補（選ばれなかった候補）
     - 文字入力で直接入力されたテキスト

  2. GiNZA + SudachiPy によるNLP解析
     - 新しい語彙・終助詞パターンの検出
     - 文長分布の変動
     - 敬語レベルの変化

  3. LLMバッチ処理によるパターン検出
     入力: 当日の会話ログ + 現在のPVP + NLP解析結果
     処理:
     - PVPに記載のない新しい表現が使われたか？
     - 既存の表現パターンと矛盾する使用はあったか？
     - 新しい話題・関心事の検出

  4. 差分レポートの生成
     出力:
     - 追加候補: "「だるい」を「しんどい」の同義語として追加"
     - 修正候補: "文末「〜だよね」の使用頻度が増加"
     - 削除候補: "「〜じゃん」の使用が減少傾向"

[週次: 統合判定]

  5. 差分の統合判定
     - 3回以上出現したパターンのみ候補とする（ノイズ排除）
     - confidenceスコアを算出
     - PVPの該当セクションに反映
     - スタイロメトリ特徴量（TTR, 文長分布等）の更新

[月次: 家族レビュー]

  6. 家族/本人による確認
     - 自動更新の提案をリスト表示
     - 承認/拒否/修正のフィードバック
     - 拒否されたパターンをネガティブ例として記録

[随時: 明示的フィードバック]

  7. 本人/家族による直接修正
     - "こうは言わない" → avoidancesに追加
     - "これは自分らしい" → example_utterancesに追加
     - 候補選択時の「修正して選択」からの学習
```

### 4.4 Progressive Decay: ALS進行への対応

ALS進行に伴い、患者の入力能力が段階的に低下する。これに伴う文体データの質の変化にPVPが適切に追従する仕組み。

```
Phase 1: 発症前（data_weight: 1.0）
  → 語彙・表現パターンの基盤。最も「その人らしい」データ

Phase 2: 発症後・入力制約前（data_weight: 0.8）
  → 話題や関心事の更新は重要。新しい価値観の反映
  → 表現パターンは発症前データで十分カバーされている場合、補足的位置づけ

Phase 3: 発症後・入力制約後（data_weight: 0.5）
  → 意図は参考にするが、表現は入力手段の制約を受けている
  → 短縮化された表現をそのまま採用しない

Phase 4: VoiceReach使用中（data_weight: 0.3）
  → 最新の好みを反映
  → ただしシステム依存の表現（候補選択由来のバイアス）は除外
  → 直接文字入力された表現は高い重みで採用
```

**decay_policyの詳細**:

```
weighted_merge の動作:
  新パターンが検出された場合:
    1. 既存PVPの該当セクションとの矛盾を検出
    2. data_weightに基づいて統合判定
       例: Phase 4 (0.3) のパターンがPhase 1 (1.0) と矛盾
       → Phase 1を優先し、Phase 4のパターンは注記として保持
    3. 3回以上の再現が確認された場合のみ本採用を候補とする
    4. 月次レビューで家族が最終判断
```

### 4.5 発症前データの重要性

PVP構築において発症前のデータを優先的に使う理由:

- 発症後は入力手段の制約で表現が簡略化されている可能性が高い
- 「本来のその人の声」は発症前の豊かな表現の中にある
- ただし、発症後の変化（新しい関心事、価値観の変化）も反映すべき

推奨データ量（調査レポートA7 5.4に基づく）:
- **最低**: 200件以上のテキストデータ（メール + LINE + SNS）
- **推奨**: 500件以上（3名以上の対話相手別データを含む）
- **50-100文からでもPVP構築は可能**だが、スタイロメトリ特徴量の安定性には200件以上が望ましい [A7: RQ3]

---

## 5. 評価基準

### 5.1 PVP品質KPI

| 指標 | 目標値 | 評価方法 |
|------|--------|---------|
| 家族「らしい」評価率 | 80%以上 | ブラインドA/Bテスト（PVPあり vs なし） |
| avoidances違反率 | 0% | 自動チェック + 家族報告 |
| 敬語レベル一致率 | 90%以上 | GiNZAによる自動検証 |
| スタイル一貫性 | 85%以上 | 候補間での語彙・語尾の一貫性スコア |

出典: [A7: 5.4 KPI目標との整合], [A3: 8.3 PVP品質評価]

### 5.2 評価方法

**A/Bテスト**: 同一状況で PVP適用候補と PVP非適用候補を生成し、家族が「どちらがより本人らしいか」をブラインド判定。

**ブラインドテスト**: 生成文が「本人の言葉」か「AI生成」かを家族が判定。PVP適用時にAI生成文が本人の言葉と誤認される割合を測定。

**長期適応効果**: 日次/週次の自動更新によるKPIトレンドを追跡。PVPの改善がプラトーに達するまでの時間を測定。

---

## 6. 研究課題と既知の限界

### 6.1 未解決の技術課題

1. **少数サンプルからの日本語スタイル学習**: 50-100文からPVPを構築した場合の精度は、構造化PVP + example_utterances + ICLの組み合わせで「許容範囲内」と推定されるが、定量的な評価データは不足 [A7: RQ3]

2. **カジュアル会話の模倣困難性**: ICLの弱点領域であるカジュアル会話での文体模倣は、明示的PVPである程度回避できるが、完全な再現は現在のLLMでは限界がある [A3: 1.2.5]

3. **敬語レベル自動推定の精度**: 既存コーパス（10,007文）でのベンチマークが必要。特に日本語敬語のランク付けと言い換えに関する研究は限定的 [A7: RQ2]

4. **LLMモデル依存性**: PVPはモデル非依存を設計原則としているが、実際のペルソナ忠実度はモデルにより差がある。三段ハイブリッド（Qwen3/Gemini/Claude）の各段での一貫性検証が必要 [A7: 5.3]

5. **Progressive Decayの最適パラメータ**: data_weightsの値（1.0/0.8/0.5/0.3）は仮説段階。実際のALS患者データによる検証が必要

### 6.2 プライバシー考慮事項

PVPの構築にはメール・LINE・SNS等の個人データを扱うため:

- データ処理は原則ローカル（Mac mini M4 Pro上）で完結
- クラウドLLM（Gemini/Claude）へ送信する場合は匿名化済みPVP + コンテキストのみ
- 原文データはクラウドに送信しない
- 詳細は09章（プライバシーと倫理）を参照

---

## 参考文献・調査レポート

本章の設計は以下の調査レポートに基づく。

- **[A7]** Phase A - A7: Personal Voice Profile / NLP 調査レポート（`research/phase_a/a7_personal_voice_profile_nlp/report.md`）
  - RQ1: 著者推定・スタイロメトリ手法 [文献1-6]
  - RQ2: 日本語文体特徴の自動分析（GiNZA v5, SudachiPy, MeCab）[文献21-25]
  - RQ3: ペルソナ対話・少数サンプルからのスタイル学習 [文献7-20]
  - RQ4: PVPのLLMプロンプト埋め込みベストプラクティス [文献7, 12, 40]
  - RQ5: プロファイル自動更新の技術的アプローチ [文献10-12]
  - RQ6: 日本語NLPツール比較と推奨 [文献24-25, 30-33]

- **[A3]** Phase A - A3: LLM x AAC 候補生成 調査報告書（`research/phase_a/a3_llm_for_aac/report.md`）
  - 1.2.2: LaMP - Retrieval-Augmented Personalization [ACL 2024]
  - 1.2.5: "Catch Me If You Can?" - ICLによる文体模倣の限界 [EMNLP 2025 Findings]
  - 3.3: ICL vs Fine-tuning vs RAG 比較表
  - 7.1: PVP + 候補生成プロンプトの設計原則
  - 8.3: PVP品質評価方法論

主要な学術文献:
- Feely et al. (2019): 日本語文の形式度3段階分類
- LaMP: When LLMs Meet Personalization (ACL 2024)
- "Catch Me If You Can?" - LLMs Still Struggle to Imitate Implicit Writing Styles (EMNLP 2025 Findings)
- Personalization of LLMs: A Survey (TMLR 2025)
- On the Way to LLM Personalization: Learning to Remember User Conversations (Apple MLR / ICLR L2M2 2025)
- Enabling Personalized Long-term Interactions through Persistent Memory and User Profiles (arXiv 2025)
- An Experimental Evaluation of Japanese Tokenizers (arXiv 2024)
- Construction and Validation of a Japanese Honorific Corpus (ACL DCLRL 2022)

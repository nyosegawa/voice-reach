# A5 -- 感情検出（Emotion Detection）調査レポート

## メタ情報

| 項目 | 内容 |
|------|------|
| エリア | Phase A - A5 |
| 調査日 | 2026-02-17 |
| 調査者 | Claude Opus 4.6（AI Research Assistant） |
| ステータス | 初版完了 |
| 関連設計書 | `docs/05_EMOTION_AND_CONTEXT.md`, `docs/10_PROGRESSIVE_ADAPTATION.md` |

---

## 1. リサーチクエスチョンへの回答

### RQ1: ALS患者など運動機能制限のある人の感情をどのようなセンサーモダリティで推定できるか？

ALS患者の感情推定には、運動機能の段階的喪失を考慮した複数のセンサーモダリティが利用可能である。以下に有効性の高い順に整理する。

#### (A) 自律神経系信号（最も長期間利用可能）

ALS患者においても自律神経系の機能は比較的保存されることが知られている。特に**瞳孔の自律神経制御はALSで特徴的に温存される**ことが報告されている（Sensory Involvement in ALS, Int. J. Mol. Sci., 2022）。これは瞳孔径による感情推定がALS患者に対して特に有望であることを示す。

- **rPPG（遠隔光電容積脈波）**: Webカメラから顔面皮膚の微細な色変化を検出し、心拍数・心拍変動（HRV）を推定。2024年の研究では、ALS患者のパルスデータとNLP感情分析を組み合わせて感情状態を定量化する試みが報告された（Improving Care for ALS with AI and Affective Computing, Journal of the Neurological Sciences, 2024）。
- **皮膚電気活動（EDA）**: ウェアラブルセンサーで計測可能だが、ALS患者では四肢の運動制限により装着が困難な場合がある。
- **顔面血流変化**: rPPGの副次的情報として取得可能。紅潮や蒼白化は感情的覚醒の指標となる。

#### (B) 眼球周辺信号（長期間利用可能）

ALSでは眼筋が最後まで保存されるため、最も信頼性の高い長期的モダリティである。

- **瞳孔径変化**: 覚醒度（arousal）の信頼性の高い指標。ALS患者でも瞳孔反応が保存されていることが確認されている。
- **まばたきパターン**: 頻度・持続時間の変化は緊張・疲労・動揺を反映する。
- **視線パターン**: 安定度、滞留時間、往復パターンが関心度や不安を示す。

#### (C) 顔面微細信号（中期まで利用可能）

- **微表情（Micro-expression）**: ALS進行に伴い有効性が低下するため、初期〜中期のみ利用可能。
- **顔面ランドマーク微変化**: MediaPipe 468点の精密追跡による眉間・眉・口角の微細な動きの検出。

#### (D) マルチモーダル統合

2024-2025年の研究トレンドとして、ウェアラブルバイオセンシングとアイトラッキングの組み合わせが急増しており、2023-2025年の論文の10%以上がこれらを含む。2022年以降の研究の40%以上が3モーダル以上の構成またはTransformerベースのクロスモーダル融合アーキテクチャを採用している（Comprehensive Review of Multimodal Emotion Recognition, Biomimetics, 2025）。

**VoiceReach向け推奨**: 瞳孔径 + rPPG + 視線パターン + まばたきパターンの4チャネル構成を基本とし、進行度に応じてチャネルの重み付けを動的に変更する。

---

### RQ2: rPPG（remote photoplethysmography）による心拍変動推定の最新精度と、Webカメラのみで実用可能か？

#### 最新精度

rPPGの精度は近年大きく向上しており、Webカメラのみでの実用が現実的になりつつある。

**心拍数（HR）推定精度:**

- VitalLens 2.0（2025）: MAE 1.57 bpm（HR）、1.08 bpm（RR）
- 231名のオンラインWebカメラ録画を用いた研究（2024）: パルスオキシメータとの相関 r > 0.75、有意差なし（Behavior Research Methods, 2024）
- rPPG-Toolbox ベンチマーク: 深層学習手法が従来手法を大幅に上回る精度を達成

**心拍変動（HRV）推定精度:**

- VitalLens 2.0: HRV-SDNN MAE 10.18 ms、HRV-RMSSD MAE 16.45 ms
- PRV（Pulse Rate Variability）信号はrPPGから得られるが、接触型PPGに比べてノイズが多く時間分解能が低いため、HRV推定はHR推定より困難
- 2025年の研究では、Adaptive Sparse AttentionやGated Temporal Poolingなどの新しい深層学習手法がrPPGからの感情認識精度を向上させている

**制限事項:**

- 低照度環境: rPPGの精度が著しく低下する（npj Digital Medicine, 2025）
- 高心拍数: 現在のアルゴリズムの多くが高心拍数時に精度が低下する
- 動きアーティファクト: 頭部の動きが精度に影響する
- ROI選択: 額・頬領域（24.5%・21.7%）が全顔（36.8%）より高精度だが、ALS患者の場合は頭部固定が多いため有利な条件

**結論**: Webカメラのみでの心拍数推定は実用可能。ただしHRV推定はまだ精度的に限界がある。VoiceReachでは心拍数の変化トレンド（上昇・安定・下降）を主に利用し、精密なHRV値への依存は避けるべきである。ALS患者は比較的静止しているため、動きアーティファクトの問題は軽減される。

---

### RQ3: 瞳孔径変化から感情価（valence）・覚醒度（arousal）をどの程度推定できるか？MediaPipe虹彩ランドマークで瞳孔径計測は実用的か？

#### 瞳孔径と感情の関係

瞳孔径は**覚醒度（arousal）の信頼性の高い指標**であることが文献上のコンセンサスとなっている。一方、**感情価（valence）との関係はより論争的**である（Emotion Detection Based on Pupil Variation, Healthcare, 2023）。

- **覚醒度との関係**: 瞳孔散大は交感神経活動の増加を反映し、感情的覚醒度と正の相関を示す。
- **感情価との関係**: 一部の研究ではネガティブ刺激で瞳孔が拡大すると報告されているが、ポジティブ刺激でも拡大する場合があり、覚醒度との交絡が問題となる。
- **先行研究の精度**: 機械学習を用いた研究では、arousal予測85%、valence予測91%の効率が報告されている（Quantifying Emotional Arousal through Pupillary Response, arXiv, 2025）。ただし光量変化の影響を分離する必要がある。

**ALS患者における特別な利点**: 瞳孔の自律神経制御はALSで温存されることが確認されており、交感神経・副交感神経の随意的制御の非侵襲的検出にも利用可能である（Int. J. Human-Computer Studies, 2019）。これはVoiceReachにとって非常に重要な知見である。

#### MediaPipe虹彩ランドマークの実用性

**MediaPipe Iris の能力:**

- 虹彩の水平径は人口全体でほぼ一定（11.7 +/- 0.5 mm）
- 距離推定: 平均相対誤差4.3%、標準偏差2.4%（2mまで）
- 5つの瞳孔キーポイントと71の眼球キーポイントをリアルタイムで出力
- RGB単眼カメラのみで動作

**課題:**

- MediaPipe Irisは「虹彩」のランドマークであり、「瞳孔径」の直接測定には追加処理が必要
- 光量変化による瞳孔反射（PLR）と感情による変化の分離が必要

**PupilSense / EyeDentify（2024-2025）の登場:**

- EyeDentify: Webcam画像からの瞳孔径推定専用データセット（51名、212,073画像）
- Tobii Eye Trackerの真値との比較でResNet-18がMAE 0.1340を達成
- PupilSense: Streamlitベースのアプリケーションとして2025 ETRA Symposiumで発表
- 画像アップスケーリングにより予測精度が向上することが確認されている

**VoiceReach向け推奨**: MediaPipe Irisを虹彩・眼球のランドマーク取得に利用しつつ、PupilSense/EyeDentifyのアプローチ（ResNetベースの回帰モデル）を参考に瞳孔径推定の精度を向上させる。光量補正にはMediaPipeで取得した虹彩サイズとの比率を利用し、環境光の影響を正規化する。

---

### RQ4: ALS患者の表情筋が衰えた状態で、微表情（micro-expression）解析は有効か？代替アプローチは？

#### 微表情解析のALS患者への適用可能性

**結論: ALS進行後の患者に対して従来の微表情解析は有効ではない。**

理由:

1. 微表情は不随意的に生じる短時間（1/25〜1/5秒）の表情で、FACS（Facial Action Coding System）のAction Unit（AU）として定義される
2. ALS患者は顔面筋力の低下により、微表情の振幅が健常者と比較して著しく小さくなる
3. 2024-2025年のメタ分析では、ALS・脳卒中における深層学習FERモデルの精度は73.2%にとどまり、他の神経疾患（認知症、ベル麻痺等）と比較して低い（Facial expression deep learning algorithms in the detection of neurological disorders, BioMedical Engineering OnLine, 2025）

#### 代替アプローチ

**1. パーソナルベースライン相対検出（VoiceReachの設計方針に一致）**

- 個人の安静時からの微小な偏差を検出する
- 絶対的な表情カテゴリではなく、valence/arousalの連続値変化として扱う
- チャネル信頼性スコアにより、利用可能な信号を動的に重み付けする

**2. Motion Magnification（動き拡大）技術**

- GAM-MM-MER（Graph Attention Mechanism-based Motion Magnification）により、微細な筋肉運動を増幅して解析する
- Swin Transformerベースのネットワークで微細な動きを強調する
- ALS患者の残存する微小な筋活動を検出可能にする潜在性がある

**3. 自律神経系信号への移行**

- rPPG、瞳孔径、顔面血流変化は表情筋の衰退に影響されない
- ALS進行に伴い、これらの信号への依存度を自動的に増加させる

**4. 行動パターンベースの感情推定**

- 視線パターン（候補を見る順番、滞留時間、回避行動）
- 入力パターン（選択速度、キャンセル頻度、候補巡回回数）
- これらの間接的指標は運動機能に依存しない

**5. MER-MFVA（Multi-modal Facial Video Analysis）アプローチ**

- 顔面表情特徴とrPPG信号を統合するフレームワーク
- Dual-path TransformerネットワークによるrPPG情報の強化
- 眼球運動情報を顔面Action Unitと同列に扱う設計

**VoiceReach向け推奨**: 微表情解析に依存せず、瞳孔径 + rPPG + 視線パターン + 入力パターンのマルチモーダル統合を基本とする。初期〜中期は顔面ランドマークの微変化も補助的に利用し、Motion Magnification技術で残存する微小な筋活動を増幅する。

---

### RQ5: ベースライン相対アプローチ（個人の平静時からの変化量で判定）の有効性と実装方法は？

#### 有効性

ベースライン相対アプローチは感情コンピューティングにおいて確立された手法であり、特にALS患者のような個人差が大きい対象に対して有効である。

**文献的根拠:**

- 研究者は現在、ビルトインキャリブレーションまたは手動キャリブレーションと、EMGプロトコルに倣った刺激前ベースライン手順を使用している（Frontiers in Psychology, 2026）
- キャリブレーションは中立的な表情を捉え、その後のデータを調整することで個人の顔貌の交絡効果を軽減する
- 刺激前ベースラインにより、刺激開始前の顔面筋活動と進行中の感情関連変動を考慮できる
- パーソナライズされた感情認識モデルは汎化モデルよりも特定のコンテキストで優れた性能を示す（JMIR AI, 2024）

**VoiceReachの設計との整合:**

VoiceReachの設計ドキュメント（`05_EMOTION_AND_CONTEXT.md`）では既にパーソナルベースライン + 差分検出のアプローチを採用しており、これは文献的に強く支持される方針である。

#### 実装方法

```
1. 初期キャリブレーション（既存設計の精緻化）

  セッション構成（30分、分割可能）:

  Phase 1: 安静時ベースライン（5分）
    - 全チャネル（瞳孔径、rPPG HR、まばたき頻度、
      視線安定度、顔面ランドマーク）のニュートラル値を記録
    - 30秒ウィンドウで平均・標準偏差を算出

  Phase 2: 快刺激（5分）
    - 各チャネルのポジティブ方向変化を記録
    - ベースラインからの差分ベクトルを算出

  Phase 3: 不快刺激（5分）
    - 各チャネルのネガティブ方向変化を記録

  Phase 4: 興味刺激（5分）
    - 覚醒度の上昇パターンを記録

  Phase 5: 退屈刺激（5分）
    - 覚醒度の低下パターンを記録

2. リアルタイム推定

  入力信号 → 1秒ウィンドウ平均化
           → ベースラインとの差分算出
           → 各チャネルの偏差スコア（z-score）
           → チャネル信頼性重みで加重平均
           → valence / arousal / confidence 出力

3. 動的再キャリブレーション

  - 日次: 1日の使用データから移動平均ベースラインを更新
  - 週次: チャネルごとの振幅変化を評価
  - 月次: チャネル信頼性スコアの再計算と重み再配分
  - 振幅縮小検出 → 閾値の自動下方修正
  - チャネル消失検出 → 残存チャネルへの重み再配分
```

**技術的注意点:**

- 1秒の刺激前ベースラインインターバルを使用した感情反応のベースライン補正が実証されている
- すべての研究がベースラインとキャリブレーションの両方を実施しているわけではなく、データ収集アプローチのバリエーションが結果の一般化を複雑にしている
- VoiceReachでは、ベースライン + キャリブレーション + 動的更新の3層構成を推奨する

---

### RQ6: マルチモーダル感情推定（瞳孔+rPPG+視線パターン+入力パターン）の統合フレームワークの先行研究は？

#### 主要な先行研究とフレームワーク

**1. MER-MFVA（Multimodal Emotion Recognition through Multimodal Facial Video Analysis）**

- 顔面映像から表情特徴とrPPG信号を同時に抽出
- 顔面Action Unit、眼球運動情報を統合
- Dual-path TransformerネットワークによるrPPG情報の強化
- VoiceReachへの適用性: 高。同一カメラから複数モダリティを抽出する設計と一致する

**2. EEG + Eye Movement Feature Fusion Network（Frontiers in Neuroscience, 2023）**

- EEGと眼球運動信号（瞳孔径、視線データ、まばたき）のマルチモーダル融合
- 新しい特徴融合ネットワークを提案
- VoiceReachへの適用性: 融合アーキテクチャの設計は参考になるが、EEGはVoiceReachでは使用しない

**3. PPG + Video Feature Fusion（Applied Sciences, 2024）**

- 光電容積脈波とビデオ信号の特徴融合による感情認識
- 学習ベースの融合モデル
- VoiceReachへの適用性: rPPGと他のビデオ特徴の融合手法として参考になる

**4. Multi-head Cross Attention with Representation Learning（Frontiers in Psychiatry, 2025）**

- マルチモーダル生理信号の感情認識
- クロスアテンション機構による異なるモダリティ間の関係性学習
- 2025年の最新手法

**5. Multimodal Knowledge Distillation（2025）**

- 感情認識のための知識蒸留
- 大規模マルチモーダルモデルから軽量モデルへの知識転移
- VoiceReachへの適用性: エッジデバイスでのリアルタイム推論に有用

#### VoiceReach向けの統合フレームワーク提案

```
         VoiceReach マルチモーダル感情推定

[カメラ入力]
     |
     +------------------------------+
     |                              |
 +-----------+              +-------------+
 | MediaPipe |              | rPPG        |
 | Face Mesh |              | エンジン    |
 | + Iris    |              | (VitalLens  |
 |           |              |  /open-rppg)|
 +-----+-----+              +------+------+
       |                           |
  +----+-------+             +-----+-----+
  |瞳孔径変化  |             |HR / HRV   |
  |まばたき    |             |顔面血流   |
  |視線パターン|             |           |
  |ランドマーク|             |           |
  |微変化      |             |           |
  +----+-------+             +-----+-----+
       |                           |
  +----+---------------------------+--------+
  |  パーソナルベースライン差分算出          |
  |  各チャネルのz-score計算                |
  +-----------------+----------------------+
                    |
  +-----------------+----------------------+
  |  チャネル信頼性重み付き融合             |
  |  (Late Fusion + Attention)             |
  +-----------------+----------------------+
                    |
  +-----------------+----------------------+
  |  入力パターン信号との統合               |
  |  (選択速度、キャンセル頻度等)           |
  +-----------------+----------------------+
                    |
    出力: valence / arousal / confidence /
          frustration
```

---

## 2. 文献レビュー

### 2.1 rPPG関連

| # | 論文タイトル | 出版 | 年 | 主な知見 |
|---|---|---|---|---|
| 1 | Remote photoplethysmography (rPPG) in the wild: Remote heart rate imaging via online webcams | Behavior Research Methods | 2024 | 231名のWebカメラ録画でrPPGとパルスオキシメータの相関 r > 0.75を確認 |
| 2 | The reliability of rPPG under low illumination and elevated heart rates | npj Digital Medicine | 2025 | 低照度・高心拍数環境でのrPPG信頼性を体系的に検証。現行アルゴリズムの限界を明確化 |
| 3 | A comprehensive review of heart rate measurement using rPPG and deep learning | PMC | 2025 | 深層学習手法が従来手法を大幅に上回る精度を示すサーベイ |
| 4 | VitalLens 2.0: High-Fidelity rPPG for HRV Estimation from Face Video | arXiv | 2025 | HR MAE 1.57 bpm、HRV-SDNN MAE 10.18 msを達成 |
| 5 | Enhancing Stress Detection through rPPG Analysis and Deep Learning | Sensors (PMC) | 2024 | rPPGと深層学習を組み合わせたストレス検出の包括的アプローチ |
| 6 | Emotion Recognition from rPPG via Physiologically Inspired Temporal Encoding | PMC | 2025 | Adaptive Sparse Attention、Gated Temporal PoolingによるrPPG感情認識 |
| 7 | The role of face regions in rPPG for contactless HR monitoring | npj Digital Medicine | 2025 | 額・頬領域が全顔より高精度。ROI選択の重要性を示す |
| 8 | Remote photoplethysmography for health assessment (IntelliProve review) | Frontiers in Digital Health | 2025 | rPPGの健康評価応用に関する包括的レビュー |

### 2.2 瞳孔径・感情検出関連

| # | 論文タイトル | 出版 | 年 | 主な知見 |
|---|---|---|---|---|
| 9 | Quantifying Emotional Arousal through Pupillary Response | arXiv | 2025 | 光量効果を分離した瞳孔反応による感情覚醒度の定量化手法 |
| 10 | PupilSense: Webcam-Based Pupil Diameter Estimation | ETRA 2025 / arXiv | 2024-2025 | EyeDentifyデータセット（51名、212K画像）。ResNet-18でMAE 0.1340 |
| 11 | Webcam-based Pupil Diameter Prediction Benefits from Upscaling | VISAPP 2025 | 2025 | 画像アップスケーリングにより瞳孔径予測精度が向上 |
| 12 | Emotion Detection Based on Pupil Variation | Healthcare (MDPI) | 2023 | 瞳孔径はarousalの信頼性の高い指標。valenceとの関係は論争的 |
| 13 | Non-intrusive Affective Assessment from Pupil Diameter and Facial Expression | Springer | 2018 | Russell円環モデルに基づくマルチモーダル感情評価システム |

### 2.3 ALS・神経疾患関連

| # | 論文タイトル | 出版 | 年 | 主な知見 |
|---|---|---|---|---|
| 14 | Improving care for ALS with AI and affective computing | J. Neurological Sciences | 2024 | ALS患者14名のパルスとNLP感情分析を統合。経済的懸念が最も強い感情反応を誘発 |
| 15 | Facial expression DL algorithms in neurological disorders: meta-analysis | BioMedical Engineering OnLine | 2025 | ALS・脳卒中でのFER精度73.2%。他の神経疾患より低い |
| 16 | Sensory Involvement in ALS | Int. J. Mol. Sci. (MDPI) | 2022 | ALS患者において瞳孔の自律神経制御は温存される |
| 17 | A HCI based on the "voluntary" pupil accommodative response | Int. J. Human-Computer Studies | 2019 | 瞳孔反応HCIの可能性を実証。ALS患者への応用を示唆 |
| 18 | Affective BCIs: Psychophysiological markers of emotion in ALS | ResearchGate | 2011 | ALS患者の感情の心理生理学的マーカーに関する先駆的研究 |

### 2.4 マルチモーダル感情認識

| # | 論文タイトル | 出版 | 年 | 主な知見 |
|---|---|---|---|---|
| 19 | Comprehensive Review of Multimodal Emotion Recognition | Biomimetics (MDPI) | 2025 | ウェアラブル+アイトラッキング組み合わせが急増。40%以上が3モーダル+ |
| 20 | Multimodal emotion recognition: review, trends, challenges | WIREs Data Mining | 2024 | 生理信号の客観性による利点を強調する包括的レビュー |
| 21 | Feature fusion for multimodal emotion recognition from EEG and eye movement | Frontiers in Neuroscience | 2023 | EEGと眼球運動の融合アーキテクチャの設計指針 |
| 22 | Emotion Recognition from PPG and Video Signal Feature Fusion | Applied Sciences (MDPI) | 2024 | PPGとビデオ信号の特徴融合モデル |
| 23 | Driver multi-task emotion recognition via multi-modal facial video analysis | Pattern Recognition | 2025 | MER-MFVA: rPPG + Action Unit + 眼球運動の統合 |

### 2.5 ベースライン・パーソナライゼーション関連

| # | 論文タイトル | 出版 | 年 | 主な知見 |
|---|---|---|---|---|
| 24 | Facial obstructions and baseline correction in affective computing | Frontiers in Psychology | 2026 | 1秒の刺激前ベースラインによる感情反応の補正の重要性 |
| 25 | Personalized vs Generalized Emotion Recognition with Consumer Wearables | JMIR AI | 2024 | パーソナライズモデルが汎化モデルを上回る |
| 26 | Affective computing has changed: the foundation model disruption | npj Artificial Intelligence | 2025 | 基盤モデルの登場による感情コンピューティングの変革 |

### 2.6 微表情関連

| # | 論文タイトル | 出版 | 年 | 主な知見 |
|---|---|---|---|---|
| 27 | Advances in Facial Micro-Expression Detection and Recognition | Information (MDPI) | 2025 | 微表情認識の包括的レビュー |
| 28 | Facial micro-expression recognition based on motion magnification and graph attention | ScienceDirect | 2024 | GAM-MM-MER: 動き拡大とグラフアテンションの統合 |
| 29 | Leveraging vision transformers and entropy-based attention for micro-expression | Scientific Reports | 2025 | ViTベースのエントロピー注意による微表情認識 |
| 30 | HRV-Based Recognition of Complex Emotions | Healthcare (MDPI) | 2025 | HRVによる複合感情（ポジティブ驚き、ネガティブ悲しみ等）の識別 |

---

## 3. OSSプロジェクト調査

### 3.1 rPPGライブラリ

| 名称 | GitHub URL | Stars | ライセンス | 最終更新 | VoiceReach適用性 |
|------|-----------|-------|-----------|---------|-----------------|
| **rPPG-Toolbox** | github.com/ubicomplab/rPPG-Toolbox | ~500+ | MIT (NeurIPS 2023) | 2024 | **高**。深層学習ベンチマーク・トレーニングに最適。7データセット対応 |
| **pyVHR** | github.com/phuselab/pyVHR | ~300+ | GPL-3.0 | 2022 | **中**。9つの古典手法 + MTTS-CAN。11データセット対応。更新が古い |
| **open-rppg** | github.com/KegangWangCCNU/open-rppg | ~100+ | 不明 | 2024 | **高**。リアルタイムWebカメラ推論特化。JAXベース低遅延。最新モデル7種対応（iBVPNet, PhysMamba, RhythmFormer等） |
| **VitalLens Python** | github.com/Rouast-Labs/vitallens-python | ~50+ | 商用 | 2025 | **高**。最高精度（HR MAE 1.57 bpm）。Python/JS SDK。HRV対応 |
| **Awesome-rPPG** | github.com/zx-pan/Awesome-rPPG | ~100+ | MIT | 2024 | **参考**。rPPGリソースのキュレーションリスト |

### 3.2 瞳孔径推定

| 名称 | GitHub URL | Stars | ライセンス | VoiceReach適用性 |
|------|-----------|-------|-----------|-----------------|
| **MediaPipe Iris** | (MediaPipeの一部) | -- | Apache 2.0 | **高**。虹彩・瞳孔ランドマークのリアルタイム検出 |
| **EyeDentify / PupilSense** | github.com/vijulshah/eyedentify | ~50+ | MIT | **高**。Webcam瞳孔径推定専用。212K画像データセット付き |
| **MediaPipe Face Mesh** | (MediaPipeの一部) | -- | Apache 2.0 | **高**。468点ランドマーク。VoiceReachの基盤技術 |

### 3.3 感情認識データセット

| 名称 | 規模 | 言語 | VoiceReach適用性 |
|------|------|------|-----------------|
| **AffectNet** | 100万枚以上 | -- | **低**。健常者対象。転移学習のベースとして利用可能 |
| **FER2013** | 35,887画像 | -- | **低**。同上 |
| **ABAW Challenge** | 毎年更新 | -- | **中**。最新ベンチマーク結果の参照用 |
| **WRIME** | 35,000投稿 | 日本語 | **高**。Plutchikの8基本感情 + 強度。主観・客観アノテーション |
| **MOE Speech** | 394Kファイル/622時間 | 日本語 | **中**。感情音声コーパス（2024版） |
| **Keio-ESD** | 47感情 | 日本語 | **中**。日本語男性話者の感情音声 |

---

## 4. 商用製品・サービス

| 製品名 | 提供元 | 主な機能 | 価格帯 | VoiceReach適用性 |
|--------|--------|---------|--------|-----------------|
| **VitalLens API** | Rouast Labs | HR, HRV, RR推定。Python/JS SDK | APIベース（従量制） | **高**。リアルタイム対応。最高精度 |
| **Binah.ai SDK** | Binah.ai | HR, HRV, RR, SpO2, BP。35-60秒の顔動画で測定 | SDK（要問合せ） | **高**。包括的バイタル測定。モバイル対応 |
| **VitalSignAI** | VitalSign.ai | リアルタイム姿勢・感情・バイタルサイン | 要問合せ | **中**。感情検出機能あり。ALS特化ではない |
| **IntelliProve** | IntelliProve | rPPGベース健康評価 | 要問合せ | **中**。高精度だが統合柔軟性は不明 |
| **Philips Biosensing (rPPG)** | Philips | rPPG特許ポートフォリオ・ライセンス | ライセンス | **低**。ライセンス利用のため、OSS代替が望ましい |

---

## 5. 日本語感情関連リソース

| リソース | 種別 | URL | VoiceReach適用性 |
|----------|------|-----|-----------------|
| **WRIME** | テキスト感情データセット | github.com/ids-cv/wrime | **高**。日本語テキストの感情強度推定 |
| **luke-japanese-large-sentiment-analysis-wrime** | 事前学習モデル | HuggingFace | **高**。WRIMEで学習済みの日本語感情分析モデル |
| **wav2vec2-xlsr-japanese-speech-emotion-recognition** | 音声感情認識 | HuggingFace | **中**。リスニングモードでの活用 |
| **MOE Speech Dataset** | 感情音声コーパス | HuggingFace | **中**。対話感情音声研究開発用 |

---

## 6. VoiceReach向け推奨事項

### 6.1 技術選定の推奨

1. **rPPGエンジン**: open-rppgを第一候補とする。リアルタイムWebカメラ推論に最適化されており、最新モデル（RhythmFormer 2024等）に対応している。精度要件が高い場合はVitalLens APIをフォールバックとして併用する。

2. **瞳孔径推定**: MediaPipe Irisの虹彩ランドマークをベースとし、PupilSense/EyeDentifyのアプローチ（ResNetベースの回帰モデル）を統合する。光量変化の補正には虹彩サイズとの比率正規化を使用する。

3. **感情推定アーキテクチャ**: Late Fusion + Attention機構による重み付き統合。各チャネルの信頼性スコアをattention weightとして使用する。

4. **データセット**: 初期開発にはWRIME（日本語テキスト感情）を使用する。瞳孔径推定にはEyeDentifyデータセットで転移学習を行う。

### 6.2 実装優先順位

```
Phase 2（9-15ヶ月）:
  1. パーソナルベースラインのキャリブレーション実装
  2. Layer 1（瞳孔径、まばたき、視線パターン）の感情推定
  3. rPPGエンジンの統合（HR推定のみ）
  4. フラストレーション検出 + エスケープUI

Phase 3（15-24ヶ月）:
  5. HRV推定の追加
  6. マルチモーダル融合の最適化
  7. 動的再キャリブレーション
  8. Motion Magnification技術の実験的導入
```

### 6.3 研究課題

1. **ALS患者特化のマルチモーダル感情データセットの構築**: 既存データセットはALS患者を含まないため、少数の協力患者からのデータ収集が必要である。
2. **低照度環境でのrPPG精度向上**: 夜間利用を考慮し、近赤外LED補助を検討する（Phase 3の夜間モードと連携）。
3. **長期的なベースライン変動の追跡**: ALS進行に伴うチャネル消失の自動検出と対応。
4. **感情推定の倫理的配慮**: 誤った感情推定が患者の尊厳を傷つけないよう、confidence閾値の適切な設定と「不確実な場合は推定しない」方針を徹底する。

### 6.4 KPI目標との整合

設計ドキュメントの感情検出精度KPI「valence方向の正答率（快/不快/中立の3分類）70%以上」は、以下の条件下で達成可能と考えられる:

- パーソナルベースライン相対アプローチの採用
- 4チャネル以上のマルチモーダル統合
- 3ヶ月以上の個人データ蓄積後

---

## 7. 参考文献リスト

1. Remote photoplethysmography (rPPG) in the wild. *Behavior Research Methods*, 2024. https://pubmed.ncbi.nlm.nih.gov/38632165/
2. A comprehensive review of heart rate measurement using rPPG and deep learning. *PMC*, 2025. https://pmc.ncbi.nlm.nih.gov/articles/PMC12181896/
3. The reliability of rPPG under low illumination and elevated heart rates. *npj Digital Medicine*, 2025. https://www.nature.com/articles/s41746-025-02192-y
4. VitalLens 2.0: High-Fidelity rPPG for HRV Estimation. *arXiv*, 2025. https://arxiv.org/abs/2510.27028
5. The role of face regions in rPPG for contactless HR monitoring. *npj Digital Medicine*, 2025. https://www.nature.com/articles/s41746-025-01814-9
6. Remote photoplethysmography for health assessment (IntelliProve). *Frontiers in Digital Health*, 2025. https://www.frontiersin.org/journals/digital-health/articles/10.3389/fdgth.2025.1667423/full
7. Quantifying Emotional Arousal through Pupillary Response. *arXiv*, 2025. https://arxiv.org/html/2504.13886
8. PupilSense: Webcam-Based Pupil Diameter Estimation. *ETRA 2025*. https://dl.acm.org/doi/10.1145/3715669.3723125
9. EyeDentify: A Dataset for Pupil Diameter Estimation. *arXiv*, 2024. https://arxiv.org/html/2407.11204v1
10. Webcam-based Pupil Diameter Prediction Benefits from Upscaling. *VISAPP 2025*. https://www.scitepress.org/Papers/2025/131628/131628.pdf
11. Emotion Detection Based on Pupil Variation. *Healthcare (MDPI)*, 2023. https://pmc.ncbi.nlm.nih.gov/articles/PMC9914860/
12. Improving care for ALS with AI and affective computing. *J. Neurological Sciences*, 2024. https://www.jns-journal.com/article/S0022-510X(24)00464-7/fulltext
13. Facial expression DL algorithms in neurological disorders. *BioMedical Engineering OnLine*, 2025. https://pmc.ncbi.nlm.nih.gov/articles/PMC12096636/
14. Sensory Involvement in ALS. *Int. J. Mol. Sci.*, 2022. https://pmc.ncbi.nlm.nih.gov/articles/PMC9779879/
15. A HCI based on the "voluntary" pupil accommodative response. *IJHCS*, 2019. https://www.sciencedirect.com/science/article/abs/pii/S1071581918301101
16. Comprehensive Review of Multimodal Emotion Recognition. *Biomimetics*, 2025. https://www.mdpi.com/2313-7673/10/7/418
17. Multimodal emotion recognition: review, trends, challenges. *WIREs Data Mining*, 2024. https://wires.onlinelibrary.wiley.com/doi/abs/10.1002/widm.1563
18. Feature fusion for multimodal emotion recognition (EEG + eye movement). *Frontiers in Neuroscience*, 2023. https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2023.1234162/full
19. Multimodal physiological signal emotion recognition (cross attention). *Frontiers in Psychiatry*, 2025. https://www.frontiersin.org/journals/psychiatry/articles/10.3389/fpsyt.2025.1713559/full
20. Emotion Recognition from PPG and Video Signal Feature Fusion. *Applied Sciences*, 2024. https://www.mdpi.com/2076-3417/14/24/11594
21. Facial obstructions and baseline correction in affective computing. *Frontiers in Psychology*, 2026. https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2026.1713462/full
22. Personalized vs Generalized Emotion Recognition. *JMIR AI*, 2024. https://ai.jmir.org/2024/1/e52171
23. Affective computing: the foundation model disruption. *npj AI*, 2025. https://www.nature.com/articles/s44387-025-00061-3
24. Enhancing Stress Detection through rPPG and Deep Learning. *Sensors*, 2024. https://pmc.ncbi.nlm.nih.gov/articles/PMC10892284/
25. Emotion Recognition from rPPG via Temporal Encoding and Curriculum Learning. *PMC*, 2025. https://pmc.ncbi.nlm.nih.gov/articles/PMC12251639/
26. HRV-Based Recognition of Complex Emotions. *Healthcare*, 2025. https://www.mdpi.com/2227-9032/13/23/3036
27. Driver emotion recognition via multi-modal facial video analysis. *Pattern Recognition*, 2025. https://ui.adsabs.harvard.edu/abs/2025PatRe.16111241X/abstract
28. Advances in Facial Micro-Expression Detection and Recognition. *Information*, 2025. https://www.mdpi.com/2078-2489/16/10/876
29. Micro-expression recognition based on motion magnification and graph attention. *ScienceDirect*, 2024. https://www.sciencedirect.com/science/article/pii/S2405844024119950
30. pyVHR: a Python framework for remote photoplethysmography. *PeerJ CS*, 2022. https://pmc.ncbi.nlm.nih.gov/articles/PMC9044207/
31. rPPG-Toolbox: Deep Remote PPG Toolbox. *NeurIPS 2023*. https://github.com/ubicomplab/rPPG-Toolbox
32. open-rppg: rPPG inference toolbox. https://github.com/KegangWangCCNU/open-rppg
33. VitalLens Python SDK. https://github.com/Rouast-Labs/vitallens-python
34. WRIME Dataset. *NAACL 2021*. https://github.com/ids-cv/wrime
35. Binah.ai SDK. https://www.binah.ai/sdk/
36. MediaPipe Iris. https://research.google/blog/mediapipe-iris-real-time-iris-tracking-depth-estimation/
37. EyeDentify GitHub. https://github.com/vijulshah/eyedentify
38. A Robust Remote Photoplethysmography Method. *arXiv*, 2025. https://arxiv.org/html/2502.02229v1

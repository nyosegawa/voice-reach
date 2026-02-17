# B7 -- 最新入力デバイス（BCI, EMG, ALS向け最新技術）

## 1. メタ情報

| 項目 | 内容 |
|---|---|
| 調査ID | B7 |
| 調査テーマ | 最新入力デバイス（BCI, EMG, ALS向け最新技術） |
| 調査日 | 2026-02-17 |
| 調査者 | Claude Opus 4.6（AI Research Assistant） |
| ステータス | 完了 |
| VoiceReach関連ドキュメント | `docs/02_EYE_TRACKING_AND_INPUT.md`, `docs/10_PROGRESSIVE_ADAPTATION.md` |

---

## 2. リサーチクエスチョンへの回答

### RQ1: BCI（Brain-Computer Interface）の最新動向

#### 非侵襲型BCI（EEG）の実用性・精度・コスト

2025-2026年において、非侵襲型EEG-BCIは以下の3つのパラダイムが主流である。

| パラダイム | 精度 | 入力速度（ITR） | 特徴 |
|---|---|---|---|
| **P300** | 74.0% +/- 8.9%（ALS患者） | 0.29 bps / 約5文字/分 | 注意の集中で誘発。疲労しやすい |
| **SSVEP** | 99.2%（高頻度刺激時） | 1.44 bps / 67.1 bits/min | 視覚刺激への応答。速度面で優位 |
| **Motor Imagery（MI）** | 81.68%（メタ分析） | 低い | 運動想起。視覚不要だが精度課題あり |
| **P300-SSVEP ハイブリッド** | 92.72%（LDAモデル） | 28 bits/min | 両方の長所を組み合わせ。最有望 |

**2025年の重要なブレークスルー: ChatBCI**
P300スペラーに大規模言語モデル（LLM）を組み合わせた「ChatBCI」が2025年に発表された（Nature Scientific Reports）。LLMによる文脈予測を活用することで、キーストローク数を53.22%削減し、情報伝達速度を229.48%向上させた。これはVoiceReachのLLM先読み設計思想と極めて近い。

**2026年のEEG-ALS研究**
2026年1月のmedRxiv論文（"From Thought to Speech"）では、低コストEEGデバイスとCNNを組み合わせ、ALS患者の内語（subvocalized words）をデコードする実証が報告されている。まだ研究段階だが、非侵襲BCIによるALS向けコミュニケーションの実現可能性を示す重要な成果である。

**コスト帯**

| デバイス | チャンネル数 | 価格帯 | 用途 |
|---|---|---|---|
| NeuroSky MindWave Mobile 2 | 1ch | ~$100 | 入門・教育用 |
| Muse 2 | 4ch (EEG) + 参照3ch | ~$250 | 瞑想・ウェルネス |
| Emotiv Insight | 5ch | ~$499 | 研究・BCI開発 |
| Emotiv EPOC X | 14ch | ~$999 | 本格研究 |
| g.tec Unicorn Hybrid Black | 8ch | ~EUR 1,089 | 研究・BCI開発 |
| OpenBCI Cyton | 8ch | ~$1,000-2,000（周辺機器込） | 研究・カスタム |
| OpenBCI Cyton+Daisy | 16ch | ~$1,500-2,500 | 高精度研究 |
| OpenBCI Galea | 8ch EEG + EMG/EDA/PPG/EOG | 要見積もり | マルチモーダル研究 |

#### ALS患者向けBCIの現状

**非侵襲型の課題:**
- ALS進行に伴い脳波パターンが変化し、BCIの精度が経時的に低下する「BCI illiteracy」問題
- 完全閉じ込め状態（CLIS）ではP300やSSVEPが利用できない可能性（視覚刺激への注意が困難）
- 個人適応・自己再較正が必要

**侵襲型・低侵襲型の進展:**
- **Neuralink N1**: 2024年1月に初の被験者（Noland Arbaugh、四肢麻痺）に埋め込み。1,024電極。2025年時点でMario Kart操作やPC制御を実現。2026年1月時点で21名の被験者に拡大。5時間ごとの充電が必要
- **Synchron Stentrode**: 血管内留置型BCI。開頭手術不要。2025年8月にALS患者がiPadのSwitch Controlを思考だけで操作に成功。10名の患者で安全性を確認。$200M Series D調達

**日本国内の動向:**
- **産総研ニューロコミュニケーター**: 2010年開発。脳波からP300信号を読み取り、アバターと音声合成で意思伝達。好条件で90%精度、2-3秒に1選択
- **JiMED社（大阪大学発ベンチャー）**: 埋め込み型BCI装置を開発中。頭蓋骨に窓を開け脳表面に電極シートを留置。運動イメージの脳波でカーソル操作。2028年実用化目標で国内初の治験申請準備中（ALS患者10名、約半年間）

**fNIRS-BCI:**
- Kernel Flow: 重量2.05kg、52モジュール。TD-fNIRS技術。ピコ秒パルスで脳血流変化を計測
- fNIRS-BCIのALS患者での精度は81.3% +/- 5.7%で、P300-BCIの74.0% +/- 8.9%を上回る
- EEG+fNIRSのマルチモーダル統合が進展中。分類精度90.11%を達成した報告あり

---

### RQ2: EMG（筋電位）ベースの入力デバイス

#### 表面EMGの技術概要

表面EMGの信号特性:
- 帯域幅: 0-500 Hz
- 振幅: 0-1.5 mV（増幅前はマイクロボルトレベル）
- 増幅率: 通常1,000-1,500倍が必要
- ノイズ源: 電源ライン干渉、筋間クロストーク、モーションアーティファクト

**最新の柔軟電極技術:**
- ナノ材料ベースの柔軟電極（導電性ポリマーフォーム、カーボンナノチューブ、銀ナノワイヤ）
- 皮膚密着型のドライ電極により、ジェル不要での長時間計測が可能に
- アクティブ電極によるノイズ低減と、DRL（Driven Right Leg）回路による電源ライン干渉除去

#### 主要デバイス

| デバイス | チャンネル | サンプリングレート | 価格 | 状態 |
|---|---|---|---|---|
| Myo Armband (Thalmic Labs) | 8ch | 200Hz | - | **販売終了**（IP: CTRL-Labs -> Meta） |
| OYMotion gForcePro+ | 8ch | 500Hz (12bit) / 1kHz (8bit) | $90-150 | 販売中 |
| OYMotion gForce 200 | 8ch（医療グレード） | - | 要見積もり | 販売中 |
| Meta Neural Band | 16ch (sEMG) | - | $799（AR眼鏡込） | 2025年9月発売 |

#### Meta Neural Band（旧CTRL-labs）

2025年9月に発表されたMeta Neural Bandは、EMG入力デバイスとして最も注目すべき製品である。

- Facebookが2019年にCTRL-labsを$500M-$1Bで買収して以降、約200,000人の研究参加者でデータを蓄積
- **個人キャリブレーション不要**で動作する「ユニバーサルデコード」を実現（重要なブレークスルー）
- タップ、スワイプ、ピンチなどのジェスチャーを認識
- Nature誌に研究成果を発表
- 2025年9月30日にMeta Ray-Ban Displayとセットで$799で発売

#### ALS患者の残存筋力での実用性

**課題:**
- ALS進行に伴い、運動ニューロン変性により筋線維が脱落し、EMG信号振幅が徐々に減少
- 初期段階（Stage 1-2）では十分な信号が得られるが、進行段階（Stage 3以降）では信号対雑音比が急速に低下
- ファシキュレーション（筋線維束攣縮）がノイズ源となる

**実用性の評価:**
- **初期〜中期（発症後1-3年）**: 表面EMGは有効。残存筋力で十分な信号振幅（>50uV）が得られる
- **中期〜後期（3-5年）**: 信号振幅が著しく低下（<10uV）。高感度アンプと適応フィルタが必要
- **後期（5年以上）**: 表面EMGでは検出困難。BCIまたは他の入力に移行が必要

**VoiceReachのピエゾ素子との比較:**
VoiceReachの指タップ入力は、EMGよりもはるかにシンプルな機械的アプローチであり、信号処理の複雑さを回避している。しかし、指が動かなくなった場合のフォールバックとして、EMGは残存する微弱な筋活動（指を動かす「意図」だけで発生するMU発火）を検出できる可能性がある。

---

### RQ3: まばたき検出・EOG（眼電図）ベースの入力

#### カメラベース vs センサーベースの比較

| 項目 | カメラベース（MediaPipe EAR） | センサーベース（EOG） |
|---|---|---|
| **精度** | 98.03%（Eyeblink 8データセット） | 95-99%（電極品質依存） |
| **追加ハードウェア** | 不要（Webカメラのみ） | 眼周囲に電極貼付が必要 |
| **装着負担** | なし | 電極の貼付・交換が必要 |
| **頭部傾斜対応** | 2D EARは頭部傾斜で問題（3D方式で改善） | 頭部位置に非依存 |
| **照明条件** | 暗所で性能低下 | 照明条件に非依存 |
| **長時間使用** | 適している | 電極の長時間貼付は不快 |
| **リアルタイム性** | 30fps程度 | ミリ秒レベル |
| **コスト** | Webカメラのみ（~$50） | 専用電極+アンプ（~$200-500） |
| **OSS実装** | 豊富（MediaPipe, OpenCV, dlib） | 限定的 |

**カメラベースのEAR（Eye Aspect Ratio）検出:**
- Soukupova & Cech (2016) が提唱した方式
- MediaPipe Face Meshの468点ランドマークから目の縦横比を計算
- まばたき時にEAR値が急激に低下することで検出
- 3Dランドマーク方式により頭部傾斜への耐性が向上

**まばたきモールス通信:**
- 複数のオープンソースプロジェクトが存在（後述）
- 2025年の研究で平均デコード精度62%、応答時間18-20秒
- 低コストだが入力速度が極めて遅い（緊急時のフォールバック向け）

**VoiceReachとの親和性:**
VoiceReachは既にMediaPipe Face Meshを使用しているため、カメラベースのまばたき検出は追加ハードウェアなしで統合可能。Stage 4（指が動かない）のフォールバック入力として最も自然な選択肢。

---

### RQ4: 舌制御デバイス（TDS: Tongue Drive System等）

#### Georgia Tech TDS

- 2005年からGhovanloo教授（当時NC State、後にGeorgia Tech）が開発
- 舌に小型磁石を固定（接着剤で短期、バーベルピアスで長期）
- 頭部ヘッドセットの磁気センサーで舌の動きを6方向で検出
- Sip-and-Puffと比較して**3倍速**でタスクを完了（Science Translational Medicine, 2013）
- 精度はSip-and-Puffと同等

#### Intra-oral TDS（iTDS）

- 口腔内に完全に収まるリテーナー型デバイス
- 90%以上の被験者がiTDSを好むと報告
- 外見上の目立たなさが大きなアドバンテージ

#### ALS患者の舌機能保持期間

**重要な制約:**
- **球麻痺型発症（Bulbar onset）**: 舌圧低下は**3ヶ月以内**に始まる。Stage 3で舌の動きが著しく制限され、Stage 4で舌萎縮が顕著
- **四肢型発症（Spinal onset）**: 舌圧低下は**6ヶ月以内**。球麻痺型より緩やかだが最終的に同様の経過
- 発話速度が100-120語/分に低下した時点が、コミュニケーション支援介入の臨床指標

**VoiceReachへの適用性:**
- 舌機能が保持されている期間は限定的であり、特に球麻痺型ALS患者では早期に使用不能になる
- VoiceReachのフォールバックとしては**中優先度**（使える期間が限られるため）
- 磁石の装着負担と口腔ケアの複雑化も課題

---

### RQ5: 呼気入力（Sip/Puff）スイッチ

#### Origin Instruments Sip/Puff Switch

- 吸引（sip）と吹き出し（puff）を独立したスイッチクローズに変換
- 2つの3.5mmポート搭載
- 堅牢な電気機械式設計（外部電源不要）
- マルチユーザーヘッドセット版あり（使い捨てマウスピース対応）

#### QuadJoy 4（2025年リニューアル）

- 30年以上の歴史を持つ口腔操作ジョイスティックがメジャーアップデート
- 口やあごで操作するジョイスティック + 内蔵Sip/Puff
- **48種類のエッジジェスチャーコマンド**に対応
- 調整可能なSip/Puff閾値、LEDインジケーター
- 価格: $1,368.50（本体）/ $1,636.00（フルキット）
- 30日間リスクフリートライアルあり

#### QuadStick

- ゲーミング向け口腔操作コントローラー
- Sip/Puff + ジョイスティック + リップポジションセンサー
- AbleGamersとの連携

#### 技術的限界

- ALS進行に伴い呼吸筋が弱化し、Sip/Puff操作に必要な圧力を生成できなくなる
- 人工呼吸器使用時はSip/Puff操作が不可能または大幅に制限される
- 衛生管理（マウスピースの清掃・交換）が必要

---

### RQ6: 皮膚表面電位・GSR/EDA による受動的意図検出

#### 技術概要

- GSR（Galvanic Skin Response）/ EDA（Electrodermal Activity）は、自律神経系の交感神経活動による発汗を皮膚電気伝導率の変化として計測
- 意識的な制御が困難な**無意識レベル**の生理反応
- 感情的覚醒、ストレス、認知負荷を反映

#### 意図検出の可能性

**二値通信（Yes/No）への応用:**
- 興奮状態と安静状態の分類精度: 84.7%（6名の健常被験者）
- メンタルエクササイズや呼吸法による**双方向制御**が可能
- 「The ALS Locked-In Communicator（TALCOR）」プロジェクトがGSRを含む通信手段を開発

**重要な制約:**
- 応答速度が遅い（数秒〜数十秒のラグ）
- 信号対雑音比が低い
- 環境温度・湿度・薬物の影響を強く受ける
- 自律神経系自体がALSの影響を受ける場合がある
- 二値（Yes/No）以上の複雑な入力は現時点では困難

**VoiceReachへの適用性:**
- 「完全閉じ込め状態（CLIS）」における最後の手段としての可能性
- 単独での実用的コミュニケーションは困難
- BCIや他の入力との**併用**（信頼度スコアの補助信号として）が最も現実的
- Shimmer3R GSR+センサー等の低コストデバイスで研究レベルの計測は可能

---

### RQ7: VoiceReachの将来的フォールバックとしての推奨優先順位

VoiceReachの現行設計「視線+指タップ」からのフォールバック経路を、以下の評価軸で優先順位付けする。

**評価軸:**
1. ALS全期間でのカバー範囲
2. VoiceReach既存アーキテクチャとの統合容易性
3. 追加ハードウェアコスト
4. 学習コスト（患者の認知負荷）
5. 入力速度・精度

#### 推奨フォールバック階層

```
Stage 1-2（筋力あり）:
  [主入力] 視線 + 指タップ（現行VoiceReach設計）
    |
Stage 2-3（筋力低下）:
  [第1フォールバック] 視線 + EMG微弱信号検出
  理由: 指が動かせなくても「動かそうとする意図」のEMG信号は残る
  統合: ピエゾ素子の代替/補完として追加可能
    |
Stage 3-4（四肢の動きなし、眼球運動あり）:
  [第2フォールバック] 視線のみ + まばたきパターン入力
  理由: 追加ハードウェア不要（MediaPipeで実現可能）
  統合: 既存カメラパイプラインの拡張のみ
    |
Stage 4（眼球運動の低下）:
  [第3フォールバック] 非侵襲BCI（EEG-SSVEP/P300 + LLM）
  理由: 眼球運動が困難になった場合の次の選択肢
  統合: ChatBCIのLLM統合アプローチはVoiceReachと親和性が高い
    |
Stage 5（完全閉じ込め状態）:
  [第4フォールバック] fNIRS-BCI or 侵襲型BCI
  理由: 現時点では研究段階だが、CLISでの唯一の選択肢
  統合: 専門医療機関との連携が必要
```

**補助的オプション（特定条件下で有効）:**
- **舌制御（TDS）**: 球麻痺型でなく舌機能が保持されている場合。期間限定的
- **Sip/Puff**: 人工呼吸器未使用で呼吸筋力が残っている場合
- **EDA/GSR**: 二値確認の補助信号として他の入力と併用

---

## 3. 文献レビュー

### 3.1 BCI関連

| # | タイトル | 著者/出版元 | 年 | 主な知見 |
|---|---|---|---|---|
| 1 | Advances in brain computer interface for ALS communication | Wang et al., Brain-X (Wiley) | 2025 | ALS向けBCIの包括的レビュー。高精度ECoG音声合成（90-99%）、EEGとアイトラッキングのハイブリッド統合の進展を報告 |
| 2 | Brain-computer interfaces in 2023-2024 | Chen et al., Brain-X (Wiley) | 2025 | BCI全般の年次レビュー。非侵襲型の時間・空間分解能の限界と侵襲型の進歩を整理 |
| 3 | Advancements in the application of BCI based on different paradigms in ALS | Frontiers in Neuroscience | 2025 | P300、SSVEP、MI各パラダイムのALS応用を比較。ハイブリッドBCIの優位性を主張 |
| 4 | Non-Invasive Brain-Computer Interfaces: State of the Art and Trends | PMC | 2025 | 非侵襲BCIの現状と展望。個人適応、自己較正の重要性を強調 |
| 5 | From Thought to Speech: Integrating Low-Cost EEG with AI for ALS | medRxiv | 2026 | 低コストEEG+CNNでALS患者の内語デコード。非侵襲BCIの通信モダリティとしての実現可能性を実証 |
| 6 | AI powered P300 and SSVEP based BCI in Neurorehabilitation (meta-analysis) | Neurology | 2025 | メタ分析。SSVEP-P300ハイブリッドLDAモデルで最高精度92.72%。MI+P300は81.68%で最低 |
| 7 | ChatBCI: P300 speller BCI with LLM word prediction | Nature Scientific Reports | 2025 | P300スペラーにLLM統合。キーストローク53.22%削減、ITR 229.48%向上 |
| 8 | Connecting a P300 speller to a large language model | bioRxiv | 2025 | P300-LLM統合の技術的詳細。BCI+LLMの相乗効果を実証 |
| 9 | High-speed spelling with a noninvasive BCI | PNAS | 2015 | SSVEPスペラーの高速入力。ITR 67.1 bits/min、精度99.2%を達成 |
| 10 | A hybrid P300-SSVEP BCI speller with FERC paradigm | Frontiers in Neuroscience | 2023 | ハイブリッドスペラー。精度94.29%、ITR 28 bits/min |

### 3.2 EMG関連

| # | タイトル | 著者/出版元 | 年 | 主な知見 |
|---|---|---|---|---|
| 11 | New design of EMG sensor for movement detection in HMI | Phan et al., SAGE Journals | 2025 | 低コスト多チャンネルEMGセンサーの設計。EMG信号のノイズ耐性向上 |
| 12 | Recent advances in flexible noninvasive electrodes for sEMG | npj Flexible Electronics | 2023 | ナノ材料ベース柔軟電極の進展。ドライ電極での長時間計測の実現可能性 |
| 13 | Ultra-Low Power Surface EMG Sensor for Wearable Applications | PMC | 2021 | 超低消費電力sEMGセンサー。ウェアラブルバイオメトリクス応用 |
| 14 | Advances in EMG armbands for gesture recognition and multimodal fusion | PMC | 2025 | EMGアームバンドの進化とマルチモーダル融合の包括的レビュー |
| 15 | Meta sEMG research published in Nature | Meta Reality Labs / Nature | 2025 | 200,000人のデータでユニバーサルEMGデコード実現。個人較正不要 |

### 3.3 まばたき・EOG関連

| # | タイトル | 著者/出版元 | 年 | 主な知見 |
|---|---|---|---|---|
| 16 | Camera-based Blink Detection using 3D-Landmarks | ACM | 2022 | 3Dランドマークでのまばたき検出。2D EARの頭部傾斜問題を解決 |
| 17 | Blink-to-Code: Real-Time Morse Code via Eye Blink Detection | arXiv | 2025 | まばたきモールス通信。平均デコード精度62%、応答時間18-20秒 |
| 18 | Proposal for Eye Blink Detection Using MediaPipe, EAR and Peak Identification | Springer | 2024 | MediaPipe+EAR+ピーク検出の統合手法。Eyeblink 8データセットで98.03%精度 |

### 3.4 舌制御・Sip-Puff関連

| # | タイトル | 著者/出版元 | 年 | 主な知見 |
|---|---|---|---|---|
| 19 | Evaluation of TDS by Individuals with High-Level SCI | PMC | 2015 | TDSの臨床評価。Sip-and-Puffの3倍速でタスク完了。Science Translational Medicine掲載 |
| 20 | Qualitative assessment of TDS by people with high-level SCI | VA Rehabilitation R&D | 2014 | TDSの定性評価。使いやすさと学習容易性を確認 |
| 21 | Automated Tongue Tracker for Quantifying Bulbar Function in ALS | PMC/Frontiers in Neurology | 2022 | 舌運動の自動追跡。球麻痺機能の定量化ツール |
| 22 | Prognostic value of decreased tongue strength on survival in ALS | J. Neurology (Springer) | 2012 | 舌圧低下の予後価値。球麻痺型は3ヶ月、四肢型は6ヶ月で低下開始 |

### 3.5 EDA/GSR関連

| # | タイトル | 著者/出版元 | 年 | 主な知見 |
|---|---|---|---|---|
| 23 | A galvanic skin response interface for people with severe motor disabilities | ACM SIGACCESS | 2004 | 重度運動障害者向けGSRインターフェース。二値制御で84.7%精度 |
| 24 | Assessing the potential of EDA as an alternative access pathway | ScienceDirect | 2007 | EDAの代替アクセス経路としての評価。双方向制御の実現可能性 |

### 3.6 fNIRS・マルチモーダル関連

| # | タイトル | 著者/出版元 | 年 | 主な知見 |
|---|---|---|---|---|
| 25 | fNIRS-based brain-computer interfaces: a review | PMC | 2015 | fNIRS-BCIの基盤レビュー。ポータビリティとBCI illiteracy耐性を強調 |
| 26 | E-FNet: EEG-fNIRS dual-stream model for BCI | ScienceDirect | 2024 | EEG+fNIRSデュアルストリームモデル。マルチモーダル統合の精度向上 |
| 27 | Improved performance of fNIRS-BCI by deep learning frequency domain features | PLOS ONE | 2025 | 深層学習による周波数特徴抽出。fNIRS-BCI精度を90.11%に向上 |

### 3.7 Synchron・侵襲型BCI関連

| # | タイトル | 著者/出版元 | 年 | 主な知見 |
|---|---|---|---|---|
| 28 | Advances in endovascular brain computer interface: Systematic review | ScienceDirect | 2025 | 血管内BCI（Stentrode等）の系統的レビュー。長期安定信号と低侵襲性を確認 |
| 29 | Stentrode System by Synchron: Architectural Design and Clinical Translation | Auctores | 2025 | Stentrodeのアーキテクチャと臨床展開。4患者で12ヶ月安全性確認 |

---

## 4. 商用製品・デバイス比較表

### 4.1 BCI/EEGデバイス

| 製品名 | メーカー | チャンネル数 | サンプリングレート | 電極タイプ | 通信方式 | 価格（USD） | ALS適用性 | 備考 |
|---|---|---|---|---|---|---|---|---|
| MindWave Mobile 2 | NeuroSky | 1ch | 512Hz | ドライ | Bluetooth | ~$100 | 低（1chでは限界） | 注意/瞑想検出のみ。認識精度47.5% |
| Muse 2 | InteraXon | 4ch EEG + 3ref | 256Hz | ドライ | Bluetooth | ~$250 | 低〜中 | 瞑想/ウェルネス向け。研究グレード |
| Insight | Emotiv | 5ch | 128Hz | セミドライポリマー | Bluetooth | ~$499 | 中 | セットアップ数分。SDK充実 |
| EPOC X | Emotiv | 14ch | 128/256Hz | サリン湿式 | Bluetooth/USB | ~$999 | 中〜高 | 認証精度99%。EmotivPro（有料）で生データ |
| Unicorn Hybrid Black | g.tec | 8ch | 250Hz (24bit) | ハイブリッド（乾/湿） | Bluetooth | ~$1,200 | 高 | 56g軽量。8.16g耐衝撃。2時間バッテリー |
| Cyton Board | OpenBCI | 8ch | 250Hz (24bit) | 任意（ADS1299） | Bluetooth/WiFi | ~$1,000+ | 高 | 完全オープンソース。カスタマイズ自由 |
| Cyton+Daisy | OpenBCI | 16ch | 125Hz (24bit) | 任意（ADS1299） | Bluetooth/WiFi | ~$1,500+ | 高 | 高チャンネル研究向け |
| Galea | OpenBCI + Pupil Labs | 8ch EEG + EMG/EDA/PPG/EOG + Eye Tracking | 250Hz | ドライアクティブ | 有線/無線 | 要見積もり | 非常に高 | マルチモーダル。VR/AR統合。2024年出荷開始 |
| Kernel Flow | Kernel | 52モジュール | - | fNIRS (TD) | 有線 | 要見積もり（研究機関向け） | 中（fNIRS） | 2.05kg。脳血流計測。BCI illiteracy耐性 |

### 4.2 EMGデバイス

| 製品名 | メーカー | チャンネル数 | サンプリングレート | 価格（USD） | ALS適用性 | 備考 |
|---|---|---|---|---|---|---|
| gForcePro+ | OYMotion | 8ch | 500Hz/1kHz | $90-150 | 中（初期〜中期） | クラウドAIジェスチャー学習。BLE 4.0 |
| gForce 200 | OYMotion | 8ch（医療グレード） | - | 要見積もり | 中〜高 | Arduino対応。9軸IMU搭載 |
| Meta Neural Band | Meta | 16ch sEMG | - | $799（眼鏡込） | 中（初期〜中期） | キャリブレーション不要。2025年9月発売 |

### 4.3 舌制御・Sip-Puff デバイス

| 製品名 | メーカー | 入力方式 | 価格（USD） | ALS適用性 | 備考 |
|---|---|---|---|---|---|
| TDS / iTDS | Georgia Tech / Zynet | 磁石+磁気センサー | 研究段階 | 低〜中（舌機能依存） | S&Pの3倍速。iTDSは口腔内完結 |
| Sip/Puff Switch | Origin Instruments | 呼気圧 | ~$200-400 | 低（呼吸筋依存） | 堅牢設計。外部電源不要 |
| QuadJoy 4 | QuadLIFE | ジョイスティック+S&P | $1,368-1,636 | 低〜中 | 48コマンド。30日トライアルあり |
| QuadStick | QuadStick | ジョイスティック+S&P+唇 | ~$500-800 | 低〜中 | ゲーミング向け。AbleGamers連携 |

### 4.4 視線入力デバイス（参考比較）

| 製品名 | メーカー | 技術 | 価格（USD） | ALS適用性 | 備考 |
|---|---|---|---|---|---|
| TD I-13 / I-16 | Tobii Dynavox | 赤外線アイトラッキング | $10,000-20,000 | 非常に高 | 業界標準。屋外対応。92%の改善報告 |
| VoiceReach（設計中） | - | Webカメラ+MediaPipe | ~$50（カメラのみ） | 高（独自設計） | ゾーンベース。Dwell Click排除 |

---

## 5. OSSプロジェクト

### 5.1 BCI / EEG処理

| プロジェクト名 | 言語 | GitHub Stars | 最終更新 | 概要 | VoiceReach関連度 |
|---|---|---|---|---|---|
| [MNE-Python](https://github.com/mne-tools/mne-python) | Python | 2,500+ | 活発 | EEG/MEG解析の標準ライブラリ。フィルタリング、アーティファクト除去、接続性推定 | 高（BCI統合時の前処理） |
| [OpenViBE](http://openvibe.inria.fr/) | C++ | - | 活発 | BCI設計・テスト・利用プラットフォーム。GUIベース | 中（プロトタイピング） |
| [BCI2000](https://www.bci2000.org/) | C++ | - | 更新中 | 信号取得・刺激提示・モニタリング。Windows専用 | 低（機能拡張停滞） |
| [MetaBCI](https://github.com/TBC-TJU/MetaBCI) | Python | 300+ | 2024 | BCI全チェーンカバー。SSVEP/P300/MI対応 | 高（統合BCI開発） |
| [PyNoetic](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0327791) | Python | - | 2025 | ノーコードBCI開発フレームワーク。全パイプライン対応 | 中（プロトタイピング） |
| [BioPyC](https://www.mdpi.com/1424-8220/21/17/5740) | Python | - | 2021 | オフラインEEG/生体信号分類。プログラミング不要 | 中（評価） |
| [pyriemann](https://github.com/pyRiemann/pyRiemann) | Python | 600+ | 活発 | リーマン幾何ベースのBCI分類。全OS対応 | 中（分類精度向上） |
| [MOABB](https://github.com/NeuroTechX/moabb) | Python | 400+ | 活発 | BCI評価ベンチマーク。複数データセット・パイプライン比較 | 高（評価） |
| [awesome-bci](https://github.com/NeuroTechX/awesome-bci) | - | 1,000+ | 活発 | BCI関連リソースのキュレーションリスト | 高（リファレンス） |

### 5.2 まばたき・視線関連

| プロジェクト名 | 言語 | 概要 | VoiceReach関連度 |
|---|---|---|---|
| [Eye-Blink-Detection-using-MediaPipe](https://github.com/Pushtogithub23/Eye-Blink-Detection-using-MediaPipe-and-OpenCV) | Python | MediaPipe + EAR + ピーク検出。リアルタイムまばたき検出 | 非常に高 |
| [WinkCode](https://github.com/YohanV1/WinkCode) | Python | まばたき -> モールス -> テキスト変換パイプライン | 高 |
| [blink-morse](https://github.com/robmcelhinney/blink-morse) | Python | まばたきモールス入力。OpenCV+dlib | 中 |
| [Hello-Morse-OpenCV](https://github.com/raghavpatnecha/Hello-Morse-OpenCV) | Python | Webカメラでまばたき検出 -> モールス -> 英語変換 | 中 |
| [MorseCode_Converter_DeepLearning](https://github.com/acl21/MorseCode_Converter_DeepLearning) | Python | 深層学習。4入力方式（フラッシュ、まばたき、手、マウス） | 中 |
| [awesome-assistivetech](https://github.com/openassistive/awesome-assistivetech) | - | 支援技術フレームワーク・リソース集 | 高 |

### 5.3 EMG関連

| プロジェクト名 | 言語 | 概要 | VoiceReach関連度 |
|---|---|---|---|
| [OYMotion SDK](https://oymotion.github.io/en/) | C/Python | gForce EMGアームバンドのSDK。ジェスチャー認識 | 中 |
| [Unicorn Suite Hybrid Black](https://github.com/unicorn-bi/Unicorn-Suite-Hybrid-Black) | C#/Python/C++ | g.tec Unicornの公式ソフト。EEG+EMG対応 | 中 |

---

## 6. VoiceReach向け推奨事項

### 6.1 フォールバック入力の優先順位

以下は、VoiceReachの「視線+指タップ」設計を基盤として、ALS進行に伴う入力能力の段階的低下に対応するフォールバック戦略の推奨である。

#### Tier 1（最優先 -- 短期的に実装すべき）

**1. カメラベースまばたき入力**
- **根拠**: VoiceReachは既にMediaPipe Face Meshを使用しており、EAR計算のための追加コードは最小限。追加ハードウェア不要
- **実装コスト**: 低（既存パイプラインの拡張）
- **対象Stage**: Stage 4（指が動かない、眼球運動あり）
- **推奨アクション**:
  - MediaPipeのランドマーク#33,#133等からEARを計算するモジュールを実装
  - 意図的まばたき（長め・強め）vs 自然まばたきの分類器を学習
  - まばたきパターン入力（シングル=確定、ダブル=キャンセル、ロング=メニュー）
  - モールス入力は学習コストが高いため、VoiceReachのLLM候補選択と組み合わせた「まばたき選択」方式を推奨

**2. 視線ジェスチャー入力の強化**
- **根拠**: 指タップなしでも、視線の滞留パターンだけで入力を完結させる
- **実装コスト**: 低〜中（UIロジックの変更）
- **対象Stage**: Stage 3-4
- **推奨アクション**:
  - 滞留時間の閾値を動的調整（Dwell Click回避のため、0.5秒滞留+まばたき確認の組み合わせ）
  - 視線の「うなずき」パターン（上 -> 下の視線移動）を確定操作に割り当て

#### Tier 2（中優先 -- 中期的に検討すべき）

**3. 表面EMGによる微弱筋活動検出**
- **根拠**: 指が物理的に動かなくても、「動かそうとする意図」に伴う微弱なEMG信号は残存する場合がある。VoiceReachの既存ピエゾ入力の代替として自然に統合可能
- **実装コスト**: 中（EMGセンサー+信号処理モジュール追加）
- **追加ハードウェア**: OYMotion gForcePro+（$90-150）または低コストsEMGモジュール
- **対象Stage**: Stage 2-3
- **推奨アクション**:
  - 前腕または手の甲に装着する2-4chの小型EMGセンサーモジュールの調査
  - 閾値ベースの二値入力（筋活動あり/なし）から開始
  - パーソナルベースラインの概念をEMG信号にも適用

**4. ChatBCI型のLLM統合EEG入力**
- **根拠**: ChatBCIの研究成果は、VoiceReachのLLM先読み設計と極めて親和性が高い。P300/SSVEP単体の低速入力をLLMで大幅に補完できる
- **実装コスト**: 高（EEGデバイス+信号処理パイプライン）
- **追加ハードウェア**: Emotiv Insight（$499）またはg.tec Unicorn（~$1,200）
- **対象Stage**: Stage 4-5
- **推奨アクション**:
  - ChatBCIの論文と実装を詳細調査
  - VoiceReachのLLM候補生成エンジンとBCI入力の統合アーキテクチャを設計
  - OpenBCI Galea（EEG+EMG+アイトラッキング統合）の評価

#### Tier 3（低優先 -- 長期的に監視すべき）

**5. 舌制御デバイス（TDS）**
- **根拠**: 使える期間が限定的（特に球麻痺型）であり、フォールバックとしての信頼性に欠ける
- **推奨アクション**: 技術動向の監視のみ。iTDS商用化時に再評価

**6. Sip/Puff**
- **根拠**: ALS後期の呼吸筋力低下と人工呼吸器使用により使用不能になる
- **推奨アクション**: 既存QuadJoy/QuadStickとの連携可能性の調査のみ

**7. EDA/GSR受動的意図検出**
- **根拠**: 二値通信精度80-85%は実用的だが、応答速度が遅く単独使用は困難
- **推奨アクション**: CLISにおけるYes/No確認の補助信号としての研究動向を監視

**8. 侵襲型/低侵襲型BCI（Neuralink, Synchron）**
- **根拠**: ALS患者向けの治験が進行中で将来的に最も有望だが、手術が必要であり、VoiceReachの「カメラオンリー」哲学とは方向性が異なる
- **推奨アクション**: 商用化された際のAPI連携可能性を検討。Synchron Stentrodeは低侵襲であり注目すべき

### 6.2 アーキテクチャへの提言

#### 入力抽象化レイヤーの設計

VoiceReachに「入力抽象化レイヤー（Input Abstraction Layer）」を設計することを強く推奨する。

```
+---------------------------------------------+
|           入力抽象化レイヤー (IAL)             |
|                                             |
|  入力イベント統一インターフェース:             |
|    - SELECT(target_id, confidence)          |
|    - CONFIRM()                              |
|    - CANCEL()                               |
|    - EMERGENCY()                            |
|    - SCROLL(direction)                      |
|                                             |
|  各入力ソースのアダプター:                    |
|    +------+ +------+ +--------+ +-----+    |
|    | 視線 | |ピエゾ| |まばたき| | EMG |    |
|    |      | |タップ| |        | |     |    |
|    +--+---+ +--+---+ +---+----+ +--+--+    |
|       +--------+--------+---------+         |
|                    |                        |
|            設定による切替/併用               |
|    +------+ +------+ +------+              |
|    | BCI  | |舌TDS | | S&P  |              |
|    |(EEG) | |      | |      |              |
|    +------+ +------+ +------+              |
+---------------------------------------------+
```

**設計原則:**
1. **統一イベント**: すべての入力ソースは同じイベント型（SELECT, CONFIRM等）に変換される
2. **ホットスワップ**: 入力ソースの切替は再起動不要で行える
3. **併用モード**: 複数の入力ソースを同時に使用し、信頼度スコアの重み付け合成が可能
4. **進行度連動**: パーソナルベースラインの変化に応じて自動的に入力ソースの重み付けを調整
5. **プラグイン方式**: 新しい入力デバイスはアダプターの追加のみで統合可能

#### 日本国内リソースの活用

- **産総研ニューロコミュニケーター**: P300ベースのBCI。VoiceReachのLLM統合と組み合わせることで効率向上の可能性。長谷川良平研究グループとの連携を検討
- **JiMED社**: 2028年の商用化後、APIレベルでの連携を検討。国内ALS患者への治験情報提供も価値がある
- **国立障害者リハビリテーションセンター（国リハ）**: 視線入力機器の知見が蓄積されており、VoiceReachの臨床評価パートナーとして有望

### 6.3 短期アクションアイテム

| # | アクション | 優先度 | 工数見積もり | 期待効果 |
|---|---|---|---|---|
| 1 | MediaPipe EARまばたき検出モジュールの実装 | 高 | 1-2週間 | Stage 4フォールバック確保 |
| 2 | 入力抽象化レイヤー（IAL）の設計・実装 | 高 | 2-3週間 | 将来の入力拡張基盤 |
| 3 | 視線のみ入力モードの実装（滞留+まばたき） | 高 | 1-2週間 | 指タップ不要のフォールバック |
| 4 | OYMotion gForcePro+ の評価 | 中 | 1週間 | EMGフォールバック可能性検証 |
| 5 | ChatBCI論文の詳細分析とPoC設計 | 中 | 2週間 | BCI+LLM統合の技術検証 |
| 6 | OpenBCI Galea の評価（マルチモーダル） | 低 | 2-3週間 | 統合デバイスの可能性検証 |

---

## 7. 参考文献リスト

### 学術論文

1. Wang et al. (2025). "Advances in brain computer interface for amyotrophic lateral sclerosis communication." *Brain-X (Wiley)*. https://onlinelibrary.wiley.com/doi/full/10.1002/brx2.70023
2. Chen et al. (2025). "Brain-computer interfaces in 2023-2024." *Brain-X (Wiley)*. https://onlinelibrary.wiley.com/doi/full/10.1002/brx2.70024
3. (2025). "Advancements in the application of brain-computer interfaces based on different paradigms in amyotrophic lateral sclerosis." *Frontiers in Neuroscience*. https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2025.1658315/full
4. (2025). "Non-Invasive Brain-Computer Interfaces: State of the Art and Trends." *PMC*. https://pmc.ncbi.nlm.nih.gov/articles/PMC11861396/
5. (2026). "From Thought to Speech: Integrating a Low-Cost Electroencephalography Device with AI to Decode Neural Language Signals in Amyotrophic Lateral Sclerosis Patients." *medRxiv*. https://www.medrxiv.org/content/10.64898/2026.01.18.26344355v1
6. (2025). "Recent applications of EEG-based brain-computer-interface in the medical field." *Military Medical Research*. https://mmrjournal.biomedcentral.com/articles/10.1186/s40779-025-00598-z
7. (2025). "Artificial Intelligence (AI) powered P300 and SSVEP based Brain Computer Interfaces (BCI) used in Neurorehabilitation -- A Systematic Review and Meta-Analysis." *Neurology*. https://www.neurology.org/doi/10.1212/WNL.0000000000212241
8. (2025). "ChatBCI, a P300 speller BCI with context-driven word prediction leveraging large language models, from concept to evaluation." *Nature Scientific Reports*. https://www.nature.com/articles/s41598-025-25660-7
9. (2025). "Connecting a P300 speller to a large language model." *bioRxiv*. https://www.biorxiv.org/content/10.1101/2025.11.06.686984v1.full
10. Chen et al. (2023). "A hybrid P300-SSVEP brain-computer interface speller with a frequency enhanced row and column paradigm." *Frontiers in Neuroscience*. https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2023.1133933/full
11. (2015). "High-speed spelling with a noninvasive brain-computer interface." *PNAS*. https://www.pnas.org/doi/10.1073/pnas.1508080112
12. Phan et al. (2025). "A new design of an electromyography sensor for movement detection in human-machine interaction systems." *SAGE Journals*. https://journals.sagepub.com/doi/10.1177/16878132251338446
13. (2025). "Electromyography Signal Acquisition, Filtering, and Data Analysis for Exoskeleton Development." *PMC*. https://pmc.ncbi.nlm.nih.gov/articles/PMC12251896/
14. (2023). "Recent advances in flexible noninvasive electrodes for surface electromyography acquisition." *npj Flexible Electronics*. https://www.nature.com/articles/s41528-023-00273-0
15. (2025). "Advances in electromyography armbands for gesture recognition and multimodal fusion." *PMC*. https://pmc.ncbi.nlm.nih.gov/articles/PMC12818089/
16. (2022). "Camera-based Blink Detection using 3D-Landmarks." *ACM*. https://dl.acm.org/doi/fullHtml/10.1145/3558884.3558890
17. (2025). "Blink-to-Code: Real-Time Morse Code Communication via Eye Blink Detection and Classification." *arXiv*. https://arxiv.org/html/2508.09344v2
18. (2024). "Proposal for a Eye Blink Detection Using Mediapipe, Eye Aspect Ratio and Peak Identification." *Springer*. https://link.springer.com/chapter/10.1007/978-3-031-77584-0_67
19. (2015). "Evaluation of the Tongue Drive System by Individuals with High-Level Spinal Cord Injury." *PMC*. https://pmc.ncbi.nlm.nih.gov/articles/PMC4467691/
20. (2022). "An Automated Tongue Tracker for Quantifying Bulbar Function in ALS." *Frontiers in Neurology*. https://www.frontiersin.org/journals/neurology/articles/10.3389/fneur.2022.838191/full
21. (2012). "Prognostic value of decreased tongue strength on survival time in patients with amyotrophic lateral sclerosis." *Journal of Neurology (Springer)*. https://link.springer.com/article/10.1007/s00415-012-6503-9
22. (2004). "A galvanic skin response interface for people with severe motor disabilities." *ACM SIGACCESS*. https://dl.acm.org/doi/10.1145/1029014.1028640
23. (2007). "Assessing the potential of electrodermal activity as an alternative access pathway." *ScienceDirect*. https://www.sciencedirect.com/science/article/abs/pii/S1350453307001026
24. (2025). "Advances in endovascular brain computer interface: Systematic review and future implications." *ScienceDirect*. https://www.sciencedirect.com/science/article/pii/S0165027025001128
25. (2025). "Improved performance of fNIRS-BCI by stacking of deep learning-derived frequency domain features." *PLOS ONE*. https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0314447
26. (2025). "A Review of Brain-Computer Interface Technologies: Signal Acquisition Methods and Interaction Paradigms." *arXiv*. https://arxiv.org/html/2503.16471v1
27. (2025). "PyNoetic: A modular python framework for no-code development of EEG brain-computer interfaces." *PLOS ONE*. https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0327791
28. Soukupova, T. & Cech, J. (2016). "Real-Time Eye Blink Detection using Facial Landmarks." *CVWW*.

### 商用製品・企業サイト

29. Emotiv EEG Headset Products. https://www.emotiv.com/
30. OpenBCI Documentation and Shop. https://docs.openbci.com/ / https://shop.openbci.com/
31. g.tec Unicorn Hybrid Black. https://www.gtec.at/product/unicorn-hybrid-black/
32. NeuroSky MindWave. https://neurosky.com/neurosky-products/mindwave-headset/
33. InteraXon Muse 2. https://choosemuse.com/products/muse-2
34. OYMotion gForcePro+. https://www.oymotion.com/en/product32/149
35. Kernel Flow. https://spie.org/news/kernel-flow-a-wearable-device-for-noninvasive-optical-brain-imaging
36. Meta Neural Band / EMG Technology. https://www.meta.com/emerging-tech/emg-wearable-technology/
37. Synchron Stentrode. https://synchron.com/
38. Origin Instruments Sip/Puff Switch. https://www.orin.com/access/sip_puff/
39. QuadJoy 4 / QuadLIFE. https://quadjoy.io/ / https://quad.life/
40. QuadStick. https://www.quadstick.com/
41. Tobii Dynavox TD I-Series. https://us.tobiidynavox.com/pages/td-i-series
42. Georgia Tech TDS. http://ghovanloo.ece.gatech.edu/index_files/TongueDrive.htm
43. Neuralink. https://neuralink.com/

### 日本語リソース

44. 産業技術総合研究所 (2010). "脳波計測による意思伝達装置「ニューロコミュニケーター」を開発." https://www.aist.go.jp/aist_j/press_release/pr2010/pr20100329/pr20100329.html
45. 産総研ニューロコミュニケーター解説. https://www.aist.go.jp/aist_j/aistinfo/story/no4.html
46. JiMED社 埋め込み型BCI装置開発 (2025). https://news.yahoo.co.jp/articles/cf64abfd0662436950e9bcccf85ddefd84a6b33e
47. 国立障害者リハビリテーションセンター研究所. https://www.rehab.go.jp/ri/
48. ALS ACTION "視線入力機器体験レポート." https://als-station.jp/alsaction/communication/
49. ICR Newsletter (2023). "AIで飛躍する脳インターフェース BMI/BCIの動向." https://www.icr.co.jp/newsletter/wtr407-20230227-harada.html
50. SOMPOインスティチュート・プラス (2024). "ブレイン・マシン・インターフェースの進化と社会実装に向けた課題." https://www.sompo-ri.co.jp/2024/03/29/11774/

### OSSリポジトリ

51. MNE-Python: https://github.com/mne-tools/mne-python
52. NeuroTechX awesome-bci: https://github.com/NeuroTechX/awesome-bci
53. MetaBCI: https://www.sciencedirect.com/science/article/pii/S0010482523012714
54. Unicorn Suite Hybrid Black: https://github.com/unicorn-bi/Unicorn-Suite-Hybrid-Black
55. OYMotion SDK: https://oymotion.github.io/en/
56. Eye-Blink-Detection-using-MediaPipe: https://github.com/Pushtogithub23/Eye-Blink-Detection-using-MediaPipe-and-OpenCV
57. WinkCode: https://github.com/YohanV1/WinkCode
58. blink-morse: https://github.com/robmcelhinney/blink-morse
59. MorseCode_Converter_DeepLearning: https://github.com/acl21/MorseCode_Converter_DeepLearning
60. awesome-assistivetech: https://github.com/openassistive/awesome-assistivetech

---

*本レポートは2026年2月17日時点のWeb検索に基づく調査結果である。BCI分野は急速に進展しているため、特にNeuralink、Synchron、Meta Neural Bandの動向は定期的な再調査を推奨する。*

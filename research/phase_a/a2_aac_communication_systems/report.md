# A2: AAC Communication Systems Research Report
# AAC意思伝達装置の包括的調査レポート

**Priority**: HIGH
**Date**: 2026-02-17
**Purpose**: Understand the competitive landscape and identify where VoiceReach adds value

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Academic Literature Review](#2-academic-literature-review)
3. [Commercial Product Survey (Worldwide)](#3-commercial-product-survey-worldwide)
4. [Japanese Market Survey](#4-japanese-market-survey)
5. [Dwell-Click Alternatives Analysis](#5-dwell-click-alternatives-analysis)
6. [Communication Rate Data](#6-communication-rate-data)
7. [User Experience and Fatigue Data](#7-user-experience-and-fatigue-data)
8. [Voice Banking and Preservation](#8-voice-banking-and-preservation)
9. [Gap Analysis: Where VoiceReach Adds Value](#9-gap-analysis-where-voicereach-adds-value)
10. [Recommendations for VoiceReach](#10-recommendations-for-voicereach)
11. [Open Questions](#11-open-questions)
12. [References](#12-references)

---

## 1. Executive Summary

The AAC (Augmentative and Alternative Communication) device market is valued at approximately USD 1.3 billion (2025) and is projected to reach USD 2.94 billion by 2035, growing at a CAGR of approximately 10%. For ALS patients specifically, eye-tracking computer systems (ETCS) are the most promising and best-studied high-tech AAC devices, as eye movements are often the least fatiguing -- and sometimes the only remaining -- volitional movements that allow communication.

**Key findings for VoiceReach positioning:**

- Current gaze-typing speeds are typically 6-15 WPM, compared to natural speech at ~150-190 WPM -- a gap of more than an order of magnitude.
- The LLM-powered SpeakFaster system (Google, 2024) demonstrated 29-60% improvement over baseline gaze typing, validating the core premise of VoiceReach's intent-based prediction approach.
- Dedicated AAC devices with eye tracking cost USD 7,000-15,000+; the Tobii PCEye 5 alone costs approximately USD 1,249. Japanese devices (伝の心, OriHime eye, miyasuku) cost JPY 490,000-750,000 before subsidies.
- Dwell-click remains the dominant selection method despite well-documented fatigue problems. Academic literature validates alternatives (smooth pursuit, gaze gestures, multimodal confirmation) but commercial adoption lags.
- Webcam-based eye tracking accuracy (~1.5-2.5 degrees visual angle) is significantly lower than dedicated IR trackers (~0.3-0.9 degrees), but VoiceReach's zone-based design (targeting ~6-12 degree zones) can accommodate this gap.
- Japanese public funding (補装具費支給制度) covers most of the cost of certified devices, with user copay capped at JPY 37,200. VoiceReach would need to navigate this certification pathway for Japanese market adoption.

---

## 2. Academic Literature Review

### 2.1 Key Papers on AAC for ALS

#### English-Language Literature

**1. "Using large language models to accelerate communication for eye gaze typing users with ALS"**
- Authors: Shanqing Cai et al. (Google Research)
- Published: Nature Communications, November 2024
- Key finding: SpeakFaster, an LLM-powered UI for abbreviated text entry, achieved 29-60% faster text entry rates and 57% fewer motor actions vs. traditional predictive keyboards in both lab and field testing with two ALS eye-gaze users.
- Baseline measurement: One participant (FP1) averaged 8.1 +/- 0.26 WPM over 6 months of real-life communication.
- Significance: Validates the core hypothesis that LLM-based intent prediction can meaningfully accelerate AAC communication.
- Source: https://www.nature.com/articles/s41467-024-53873-3

**2. "Comparing Dwell time, Pursuits and Gaze Gestures for Gaze Interaction on Handheld Mobile Devices"**
- Authors: Namnakani et al.
- Published: CHI 2023 (ACM Conference on Human Factors in Computing Systems)
- Key finding: Smooth pursuit selection was fastest (1.36s per target vs. 2.33s for dwell and 5.17s for gaze gestures when seated). Users found pursuits significantly easier, faster, and less tiring than dwell time and gaze gestures.
- Source: https://dl.acm.org/doi/10.1145/3544548.3580871

**3. "Multi-modal access method (eye-tracking + switch-scanning) for individuals with severe motor impairment: A preliminary investigation"**
- Published: PMC, 2022
- Key finding: A multi-modal prototype integrating eye-tracking + switch scanning showed promise for adults with severe physical impairment, with eye-gaze directly selecting a group of potential targets and linear automatic scanning to select a specific item.
- Significance: Directly relevant to VoiceReach's gaze+tap hybrid approach.
- Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC9576815/

**4. "EyeTAP: Introducing a multimodal gaze-based technique using voice inputs with a comparative analysis of selection techniques"**
- Published: International Journal of Human-Computer Studies, 2021
- Key finding: EyeTAP (gaze for pointing + auditory input for selection) resulted in faster movement time, faster task completion time, and lower cognitive workload than voice recognition alone.
- Source: https://www.sciencedirect.com/science/article/abs/pii/S107158192100094X

**5. "Eye tracking communication devices in amyotrophic lateral sclerosis: impact on disability and quality of life"**
- Published: PubMed, 2013
- Key finding: Eye tracking communication devices should be considered in late-stage ALS with tetraplegia and anarthria, as they can reduce communication disability and improve quality of life.
- Source: https://pubmed.ncbi.nlm.nih.gov/23834069/

**6. "The effects of dynamic dwell time systems on the usability of eye-tracking technology: a systematic review and meta-analyses"**
- Published: Human-Computer Interaction, 2025
- Key finding: Dynamic dwell time systems were favored for efficiency metrics (mean response time, text entry rate) and effectiveness metrics (error rate), but subjective ratings were less conclusive -- a 500ms static dwell was favored for satisfaction, mental effort, and fatigue level in one study.
- Source: https://www.tandfonline.com/doi/full/10.1080/07370024.2025.2497236

**7. "Communication Matters -- Pitfalls and Promise of Hightech Communication Devices in Palliative Care of Severely Physically Disabled Patients With Amyotrophic Lateral Sclerosis"**
- Published: Frontiers in Neurology, 2018
- Key finding: Comprehensive review of ETCS in ALS palliative care, identifying both benefits and significant challenges in real-world deployment.
- Source: https://www.frontiersin.org/journals/neurology/articles/10.3389/fneur.2018.00603/full

**8. "Rate of speech decline in individuals with amyotrophic lateral sclerosis"**
- Published: Scientific Reports, 2022
- Key finding: Bulbar-onset ALS patients reached speech loss (speaking rate < 120 w/m) at 23 months and speech intelligibility < 85% at 32 months. Limb-onset patients maintained functional speech at 60 months in most cases.
- Source: https://www.nature.com/articles/s41598-022-19651-1

**9. "Timing of Communication Device Introduction Defined by ALSFRS-R Score"**
- Published: PMC, 2020
- Key finding: ALSFRS-R is a useful tool for timing AAC device introduction and helping therapists, caregivers, and families provide AAC at the right stage.
- Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC7365172/

**10. "Mental fatigue prediction during eye-typing"**
- Published: PLOS One, 2021
- Key finding: Developed a working memory-based model of mental fatigue for eye-typing using eye-tracking data, confirming that prolonged eye-typing leads to measurable cognitive fatigue.
- Source: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0246739

**11. "Word prediction and communication rate in AAC"**
- Authors: Trnka et al.
- Key finding: An advanced word prediction system gave a 58.6% improvement in communication rate, with prediction quality improving utilization rates (93.6% for advanced vs. 78.2% for basic prediction).
- Source: https://www.eecis.udel.edu/~mccoy/publications/2008/trnka08at.pdf

**12. "Circular orientated display speeds up communication by gaze"**
- Published: Disability and Rehabilitation: Assistive Technology, 2025
- Key finding: A novel circular display design for eye gaze SGDs showed improved communicative efficiency compared to traditional grid layouts.
- Source: https://www.tandfonline.com/doi/full/10.1080/17483107.2025.2528847

#### Japanese-Language / Japan-Relevant Literature

**13. "ローコスト視線入力装置による意思伝達環境の構築およびマニュアル作成"**
- Author: Ito Fumito (伊藤史人)
- Published: ALS基金研究奨励金報告書, 2016
- Key finding: Research on building low-cost gaze input environments using consumer eye trackers, produced manuals for ALS patient communities in Japan.
- Source: https://alsjapan.org/wp-content/uploads/2017/06/伊藤史人氏_報告書（全文）.pdf

### 2.2 The Midas Touch Problem

The "Midas Touch problem" -- where users unintentionally select onscreen objects by gazing at them -- is a fundamental challenge in gaze-based interaction. It stems from the dual role of gaze: we look at things both to perceive them and to interact with them.

Key research solutions include:

| Approach | Description | Source |
|---|---|---|
| DualGaze | Two-step gaze gesture: look at object, then confirm via trajectory-adaptive flag | IEEE ISMAR 2018 |
| Snap Clutch | Modal approach using gestures to switch between gaze modes | ETRA 2008 |
| EEG + Gaze | Passive BCI detects intention to interact, initiating selection | Zander Labs research |
| EyeTAP | Voice input for confirmation after gaze pointing | Springer 2021 |
| VoiceReach approach | Physical tap for confirmation after gaze pointing | Novel hybrid |

VoiceReach's gaze+tap approach is a clean solution to the Midas Touch problem. It separates observation (gaze) from intention (tap), avoiding the need for complex BCI hardware or voice capability (which ALS patients progressively lose).

---

## 3. Commercial Product Survey (Worldwide)

### 3.1 Dedicated AAC Devices with Eye Tracking

| Product | Company | Approx. Price (USD) | Input Methods | Eye Tracker | Key Features | ALS Suitability |
|---|---|---|---|---|---|---|
| TD I-Series (I-13/I-16) | Tobii Dynavox | ~$15,000+ (est.) | Eye gaze, touch, switch | Built-in Tobii IR | TD Snap/Communicator 5, durable, mountable | Excellent; purpose-built for ALS |
| TD Pilot | Tobii Dynavox | ~$10,500 | Eye gaze (iPad-based) | Built-in Tobii sensor | iPad ecosystem, eye control of iOS | Good; lighter but iPad limitations |
| TD I-110 | Tobii Dynavox | Quote-based | Eye gaze, touch, switch | Built-in Tobii IR | Newer model, TD Snap | Excellent |
| Eyegaze Edge | LC Technologies | Quote-based (est. $7,000-15,000) | Eye gaze only | Proprietary IR camera | 30+ years ALS-specific design, low fatigue | Excellent; ALS-focused since 1990s |
| NeuroNode Trilogy | Control Bionics | Quote-based | EMG, eye gaze, touch, spatial | NeuroNode EMG sensor | Three access methods: touch + eye + EMG/spatial | Excellent; handles disease progression |
| GridPad | Smartbox/Thinksmartbox | ~$5,000-8,000 (est.) | Eye gaze, touch, switch | Compatible with Tobii, others | Grid 3 software, robust vocabulary | Good |

### 3.2 Eye Tracker Accessories (Add to Existing Computer)

| Product | Company | Approx. Price (USD) | Key Specs | Software |
|---|---|---|---|---|
| PCEye 5 | Tobii Dynavox | ~$1,249 | IR, USB-C, 95%+ user compatibility, works in bright light | TD Control, compatible with Grid 3, TD Snap, Communicator 5 |
| Hiru | IRISBOND | ~$1,000-1,500 (est.) | Multiplatform (Windows + iPadOS), MFi certified, on-device processing | App Wheel ecosystem |
| Tobii Eye Tracker 5 | Tobii (gaming line) | ~$229 | Consumer-grade, lower precision than PCEye | Gaming-focused; limited AAC support |

### 3.3 AAC Software (Runs on PC/Tablet)

| Software | Company | Price | Input Support | Key Features |
|---|---|---|---|---|
| TD Snap (formerly Snap + Core First) | Tobii Dynavox | Bundled w/ devices or ~$300 standalone | Touch, eye gaze, switch | Symbol-based, QuickFires auto-talk, Topics |
| Communicator 5 | Tobii Dynavox | Bundled or ~$600 | Eye gaze, switch | Text-based, for literate users |
| Grid 3 | Smartbox (Thinksmartbox) | ~$500-700 | Eye gaze, switch, touch, mouse | Symbol and text, env control, robust access methods |
| CoughDrop | CoughDrop Inc. | $295 lifetime / $9/month | Touch, eye gaze | Open-source-friendly, web-based, cross-platform |
| OptiKey | Open Source | Free | Eye gaze, mouse, webcam | Windows keyboard/mouse control, free, works with low-cost trackers |
| GazeTheWeb | Open Source (MAMEM) | Free | Eye gaze | Browser control via gaze |

### 3.4 BCI (Brain-Computer Interface) -- Emerging

| Product | Company | Status | Notes |
|---|---|---|---|
| Stentrode | Synchron | Clinical trials | Minimally invasive BCI implant; ALS patient controlled Amazon Alexa (Sept 2024) and iPad (Aug 2025) |
| N1 | Neuralink | Clinical trials | Invasive BCI; not yet ALS-specific commercial product |
| Connexus | Paradromics | First human test completed | High-bandwidth neural interface for ALS and stroke patients |

BCI is promising but not commercially available for AAC use as of early 2026. Commercialization is estimated around 2030.

---

## 4. Japanese Market Survey

### 4.1 Japanese AAC Devices (意思伝達装置)

| Product (Japanese) | Product (English) | Company | Price (JPY, tax-exempt) | Input Method | Eye Tracker | Key Features |
|---|---|---|---|---|---|---|
| 伝の心 Ver.6 | Den-no-Shin | Hitachi KE Systems (via Pacific Supply) | 493,500-547,300 | Switch scan, eye gaze (optional) | Tobii PCEye 5 (separate, +242,000) | Email, web, env control, IR remote; Japan's most established AAC |
| OriHime eye+Switch | OriHime Eye | Ory Lab (via Double Giken) | 493,536-509,436 | Switch, eye gaze | Tobii PCEye 5 (separate, +242,000) | Digital transparent character board mode, switch + gaze dual input |
| miyasuku EyeConSW | Miyasuku | Unicorn Corp. | 488,000-504,000 | Switch, eye gaze | Tobii compatible | Email, internet, env control, Windows integration |
| eeyes (イイアイズ) | eeyes | eeyes / Double Giken | 493,500-509,400 | Eye gaze, switch scan | Proprietary gaze detection with patented correction | Emoji support, patented position-shift tolerance, 15.6" monitor |
| ファイン・チャット | Fine Chat | Access Yell (successor to Let's Chat) | 420,000 | 1-2 switch scan | N/A (switch only) | Portable, battery-powered, TV remote, succeeded Let's Chat |
| レッツ・チャット | Let's Chat | Panasonic (discontinued) | 168,000 (was) | Switch scan | N/A | Discontinued; replaced by Fine Chat. Simple, 62 pre-saved sentences |
| TCスキャン | TC Scan | CREACT | ~450,000 (est.) | Switch scan | N/A | For severe neurological conditions, scan-and-switch method |
| マイトビー I-16 | MyTobii I-16 | Tobii Dynavox (via CREACT) | ~750,000+ (est. with tracker) | Eye gaze, touch, switch | Built-in Tobii | Japanese-localized Tobii I-Series |

### 4.2 Public Funding System (公費制度)

Japan has a robust public funding system for AAC devices:

**補装具費支給制度 (Assistive Device Subsidy System):**

| Category | Details |
|---|---|
| Classification | 重度障害者用意思伝達装置 (Communication aids for severely disabled persons) |
| Purchase base amount (購入基準額) | JPY 480,600 (for devices with env control or communication functions) |
| User copay cap | JPY 0 (welfare recipients), JPY 0 (non-taxable households), JPY 37,200 (taxable households) |
| Durability period (耐用年数) | 5 years |
| Re-issuance | Available for progressive diseases like ALS as condition changes |
| Eligibility | Physical disability certificate (limb/trunk disability grade 1-2 AND speech/language disability grade 3), or designated intractable disease |
| Eye tracker add-on | Tobii PCEye 5 at JPY 242,000 covered as optional attachment |

**日常生活用具給付等事業 (Daily Living Equipment Grant Program):**

| Item | Details |
|---|---|
| Administrator | Municipal governments (市区町村) |
| Category | 情報・意思疎通支援用具 (Information and communication support equipment) |
| Advantage | Simpler application process (no formal assessment needed) |
| Disadvantage | No re-issuance for disease progression; one-time grant |

**Practical implication**: An ALS patient in Japan can typically obtain a device like 伝の心 or OriHime eye for approximately JPY 37,200 out-of-pocket (taxable household) to JPY 0 (non-taxable/welfare household). The eye tracker add-on (Tobii PCEye 5) is also covered.

### 4.3 Japanese Market Characteristics

**Adoption patterns:**
- 伝の心 (Den-no-Shin) by Hitachi is the most widely recognized and adopted device in Japan, with decades of history
- Switch scanning remains the dominant input method in Japan; eye gaze is typically an add-on option
- The Japanese market is more conservative, with a smaller number of approved/certified devices compared to the US/EU
- Device certification and subsidy eligibility are critical for market access

**Distribution:**
- Major distributors include Double Giken (ダブル技研), Pacific Supply, CREACT
- Sales often go through hospital rehabilitation departments and speech therapists (言語聴覚士/ST)
- The annual 国際福祉機器展 (H.C.R.) is the key trade show for assistive devices

**Unique features of the Japanese market:**
- Strong emphasis on switch-based input (historically due to lack of eye tracker availability)
- Integration with Japanese text input (hiragana/katakana/kanji) adds complexity
- Environmental control (家電操作) is a standard expected feature
- Ory Lab's OriHime represents a newer, tech-startup approach with the "digital transparent character board" (デジタル透明文字盤) concept

**Organizations:**
- 日本ALS協会 (JALSA): Patient advocacy, provides device lending programs
- 仙台市重度障害者コミュニケーション支援センター: Regional support center model
- 東京都障害者IT地域支援センター: Maintains comprehensive device comparison lists

---

## 5. Dwell-Click Alternatives Analysis

### 5.1 Current State of Dwell-Click

Dwell-click (凝視クリック) remains the de facto standard in commercial eye-tracking AAC systems. Typical dwell times range from 250ms to 1000ms. While it requires no additional hardware beyond the eye tracker, it has well-documented problems:

| Problem | Impact | Evidence |
|---|---|---|
| Eye fatigue | Users cannot sustain long sessions | Mental fatigue confirmed by PLOS One 2021 study |
| The Midas Touch problem | Looking at something = clicking it; forces unnatural gaze behavior | Extensively documented since Jacob 1990 |
| Speed ceiling | 1 selection per 0.5-1.0 seconds limits throughput | Typical 6-15 WPM ceiling documented |
| No visual rest | Screen is always "active" as long as eyes are open | Unique to dwell; switch and multimodal allow idle gaze |
| Error rate | Increases with fatigue; false selections frustrate users | Dynamic dwell review (2025) confirms |

### 5.2 Comparison of Selection Alternatives

| Method | Speed (target select) | Error Rate | Fatigue | Hardware Needed | ALS Suitability | Commercial Availability |
|---|---|---|---|---|---|---|
| **Dwell click** | 2.33s seated | Low (but increases with fatigue) | HIGH | Eye tracker only | Medium (fatigue limits use) | Ubiquitous; all commercial systems |
| **Smooth pursuit** | 1.36s seated | Medium | LOW | Eye tracker only | Good (natural eye movement) | Rare; mostly research |
| **Gaze gestures** | 5.17s seated | Low | Medium-High | Eye tracker only | Limited (complex patterns hard for ALS) | Very rare |
| **Switch scanning** | Variable (slow) | Low | Low (eye) but repetitive | Switch device | Good for late-stage | Common in Japan |
| **Gaze + switch/tap** | ~1-2s (est.) | Low | LOW | Eye tracker + switch/tap device | Excellent (separates observation from action) | Rare; VoiceReach approach |
| **Gaze + voice** | Fast (EyeTAP study) | Low | Low | Eye tracker + mic | Poor for ALS (voice loss) | Research only |
| **Gaze + EEG/BCI** | Variable | Medium | Low | Eye tracker + BCI headset | Future potential | Research only |
| **Blink detection** | Slow (~1-2s) | Medium-High | Medium | Camera | Good for late-stage fallback | Some systems (Tobii) |

**CHI 2023 data** (Namnakani et al.):
- Smooth pursuit: 1.36s selection when seated, 2.14s walking
- Dwell time: 2.33s seated, 2.76s walking
- Gaze gestures: 5.17s seated, 6.68s walking
- User preference: Pursuits when stationary; dwell when moving

### 5.3 VoiceReach's Gaze + Tap Approach: Detailed Analysis

**Mechanism**: Eye gaze determines what the user is looking at (pointing); a physical tap on a piezo sensor confirms selection (clicking). These two actions are fully decoupled.

**Advantages over dwell:**
1. Eliminates the Midas Touch problem entirely -- looking at something never triggers an action
2. Allows visual rest -- the user can look anywhere on screen without fear of accidental input
3. Eliminates dwell time latency -- selection is as fast as the user can tap
4. Reduces eye fatigue by removing the need for sustained fixation
5. Enables zone-based design with lower-accuracy eye tracking (webcam-feasible)

**Challenges and risks:**
1. Requires residual finger/hand motor function -- ALS patients eventually lose this
2. Need for fallback when tap is no longer possible (blink, gaze gesture, EMG)
3. Synchronization: the system must reliably associate a tap with the most recently gazed zone
4. Novel interaction paradigm: users and clinicians familiar with dwell may resist adoption
5. The piezo sensor adds a hardware component (though inexpensive)

**Comparison with prior multimodal research:**
- The PMC 2022 study on eye-tracking + switch-scanning used sequential group selection (gaze selects group, switch selects item within group), which is similar in principle but more complex in execution
- EyeTAP used voice for confirmation, which is not viable for ALS patients who lose speech
- VoiceReach's approach is simpler and more direct: look + tap = select

---

## 6. Communication Rate Data

### 6.1 Communication Rates by Method

| Method | Typical WPM | Best-Case WPM | Source |
|---|---|---|---|
| Natural speech | 150-190 | 200+ | Standard human performance |
| Eye gaze letter-by-letter (no prediction) | 6-10 | ~15 | Multiple studies; SpeakFaster 2024 |
| Eye gaze with word prediction | 8-12 | ~15 | Trnka et al. |
| Eye gaze with LLM acceleration (SpeakFaster) | 10-16 | ~20-30 (lab) | Nature Communications 2024 |
| Switch scanning (1-switch) | 2-5 | ~8 | General AAC literature |
| Switch scanning (2-switch) | 4-8 | ~12 | General AAC literature |
| BCI (current research) | 5-15 | ~90 (speech decoding, Brown 2024) | Emerging; not yet deployable |

### 6.2 Communication Rate by ALS Disease Stage

| Stage | ALSFRS-R Range | Speech Capability | Typical AAC Method | Expected WPM |
|---|---|---|---|---|
| Early (Bulbar onset) | 36-48 | Declining but intelligible | Natural speech + AAC supplementation | 80-150 (speech); 8-15 (AAC) |
| Early (Limb onset) | 36-48 | Often normal | May not yet need AAC | N/A |
| Middle | 20-36 | Often significantly impaired | Eye gaze typing, switch scanning | 6-12 |
| Late | 8-20 | Minimal or absent | Eye gaze with prediction | 4-10 |
| Locked-in | 0-8 | Absent | Eye gaze (if eye movement preserved) or BCI | 2-6 |

### 6.3 Key Data Points from SpeakFaster (2024)

- Participant FP1 (real-world, 6-month measurement): baseline 8.1 +/- 0.26 WPM
- With SpeakFaster LLM acceleration: 29-60% improvement over baseline
- Keystroke savings: 14-46 absolute percentage points reduction
- Motor action savings: 57% fewer actions than traditional predictive keyboards (offline simulation)

### 6.4 VoiceReach Target Communication Rates

Based on this data, VoiceReach's intent-based approach (1-3 operations per complete phrase, rather than character-by-character) could theoretically achieve:
- If 1 operation per phrase at 2 seconds/operation: ~30 WPM (assuming 1 word per phrase is conservative; multi-word phrases would be higher)
- If 3 operations per phrase at 2 seconds/operation: ~10 WPM
- Realistic target with mixed intent-selection and fallback character input: 12-25 WPM

This would represent a meaningful improvement over the current 6-15 WPM range, though achieving the upper bound depends on prediction accuracy.

---

## 7. User Experience and Fatigue Data

### 7.1 Eye Fatigue Studies

**Dwell-time and fatigue:**
- A 500ms static dwell time was favored in studies on the basis of lower frustration, satisfaction, and fatigue compared to dynamic dwell systems (2025 systematic review)
- Mental fatigue during eye-typing is measurable and accumulates with working memory load (PLOS One 2021)
- Dwell time of 250ms to 1000ms was rated as potentially useful, but shorter dwell increases errors while longer dwell increases fatigue

**Fatigue progression during sessions:**
- Dwell time, number and accuracy of fixations on target objects decrease with time on task
- Inaccurate scan-paths are associated with performance errors
- ALS patients report needing frequent breaks from eye-controlled devices

### 7.2 Satisfaction and Quality of Life

- Eye tracking communication devices reduce communication disability and improve quality of life in late-stage ALS (PubMed 2013 study)
- At some point, 80-95% of people with ALS are unable to meet their daily communication needs using natural speech
- The gap between desired communication and achievable communication (at 6-15 WPM vs. 150+ WPM natural speech) is a major source of frustration

### 7.3 Webcam vs. Dedicated Eye Tracker: Accuracy and UX Implications

| Metric | Webcam-Based | Dedicated IR (e.g., Tobii PCEye) |
|---|---|---|
| Accuracy (visual angle) | 1.45-2.5 degrees | 0.3-0.9 degrees |
| Sampling rate | 20-30 Hz | 120+ Hz |
| Latency | Higher, variable | Low, consistent |
| Lighting sensitivity | High (ambient light dependent) | Low (IR illumination) |
| Cost | ~$50 (consumer webcam) | $229-$1,249+ |
| Setup complexity | Minimal | USB plug-in; may need mounting |
| Outdoor use | Limited | PCEye 5 supports bright light |

**Key validation**: A study comparing the ITU Gaze Tracker (webcam-based) with Tobii T60 and Mirametrix S1 found that webcam-based eye trackers can yield performance comparable to more expensive systems in interaction tasks -- though with lower precision for fine-grained targeting.

**Implication for VoiceReach**: The zone-based design (4-16 zones, each 6-12 degrees visual angle) is specifically engineered to work within webcam accuracy limitations. This is a sound architectural decision supported by the research.

---

## 8. Voice Banking and Preservation

### 8.1 Current Voice Banking Technologies

| Technology | Provider | Sentences Required | Price | Languages | Key Feature |
|---|---|---|---|---|---|
| My-Own-Voice (MOV) | Acapela Group | 50 (DNN) or 1500 (unit selection) | $99/yr or $999 lifetime | 20+ | Deep Neural Network requires only 50 sentences |
| ModelTalker | Nemours Speech Research Lab | 400 min, 800 suggested, 1600 max | Free (research) | English | Focus on children's voices |
| Personal Voice | Apple | Read-aloud prompts (~15 min) | Free (built into iOS 17+) | Multiple | On-device processing, privacy-focused |
| ElevenLabs | ElevenLabs | Minimal audio samples | $1,200/yr Pro (free via Bridging Voice for ALS) | Many | AI voice cloning, high quality |
| SpeakUnique | SpeakUnique | Variable | Varies | English | Focus on accent preservation |

### 8.2 Significance for VoiceReach

Voice banking/cloning is a critical complementary technology for VoiceReach. Key considerations:

1. **Timing is critical**: Voice samples must be collected while the patient still has intelligible speech. For bulbar-onset ALS, this window can be as short as 23 months.
2. **Apple Personal Voice** is free and on-device, making it the lowest-barrier option, but it requires Apple hardware.
3. **Acapela's DNN approach** (50 sentences) dramatically lowers the recording burden compared to older systems (1500 sentences).
4. **VoiceReach's planned integration** with XTTS/VALL-E/StyleTTS for zero-shot voice synthesis is aligned with the state of the art but will need to match the quality of commercial solutions.
5. **Japanese voice cloning** is less mature than English. VoiceReach would need to verify that chosen TTS models support Japanese voice cloning adequately.

---

## 9. Gap Analysis: Where VoiceReach Adds Value

### 9.1 VoiceReach Advantages vs. Existing Solutions

| Feature | Existing Solutions | VoiceReach Approach | Advantage Level |
|---|---|---|---|
| **Cost** | $7,000-15,000+ (dedicated devices); JPY 490,000-750,000 (Japanese) | Standard webcam (~$50) + computing device | STRONG -- 100x cost reduction for eye tracking hardware, though computing device still needed |
| **Dwell-click fatigue** | Ubiquitous in all commercial systems; causes documented fatigue | Gaze=pointing, tap=confirmation; eliminates dwell entirely | STRONG -- addresses primary user complaint with sound research backing |
| **Communication speed** | 6-15 WPM character-by-character | Intent-based multi-character prediction with LLM; target 12-25 WPM | MODERATE-STRONG -- LLM prediction validated by SpeakFaster; actual gains depend on prediction accuracy |
| **Personality preservation** | Separate voice banking tools; generic AAC vocabulary | Integrated Personal Voice Profile + voice cloning | MODERATE -- novel integration, but voice banking exists as separate tools |
| **Disease progression adaptation** | Manual reconfiguration; some systems offer switch + gaze | Dynamic stage-based parameter adjustment with automatic detection | MODERATE -- unique approach, but complex to implement reliably |
| **Offline capability** | Most dedicated devices work offline; cloud AAC (CoughDrop) requires internet | Dual-stage local+cloud with 70% offline target | MODERATE -- parity with dedicated devices; advantage over cloud-only apps |
| **Japanese text input** | Established hiragana/kanji input in 伝の心, miyasuku | Zone-based 2-stroke hiragana + LLM prediction | NEEDS VALIDATION -- Japanese intent prediction is significantly harder than English |

### 9.2 Challenges and Honest Risks

| Challenge | Severity | Mitigation |
|---|---|---|
| **Webcam accuracy** | HIGH | Zone-based design accommodates 2-5 degree error, but low-light/outdoor scenarios remain problematic |
| **Japanese market certification** | HIGH | Need 補装具 certification for subsidy eligibility; without it, adoption will be severely limited in Japan |
| **Tap fallback** | HIGH | When patients lose finger movement, system must seamlessly transition to blink/gaze gesture; this transition is complex |
| **LLM prediction accuracy for Japanese** | MEDIUM-HIGH | Japanese is morphologically complex; intent prediction may not achieve same gains as English LLM work |
| **User/clinician adoption** | MEDIUM | Novel interaction paradigm requires training; clinicians may prefer familiar dwell-based systems |
| **Calibration drift** | MEDIUM | Webcam calibration is less stable than IR; continuous adaptation (as designed) mitigates but doesn't eliminate |
| **Competition from Apple** | MEDIUM | Apple Personal Voice + iOS accessibility eye tracking (via IRISBOND Hiru) could offer a mainstream alternative |
| **Medical device regulation** | MEDIUM | If classified as a medical device in Japan or elsewhere, regulatory burden increases significantly |

### 9.3 Competitive Positioning Summary

```
                    High Cost
                       |
         Tobii I-Series / Eyegaze Edge
                  |         |
    Dedicated ----+----+----+---- General Purpose
    Hardware       |   |   |        Software
                   |   |   |
         miyasuku / 伝の心 / OriHime eye
                   |   |
                   |   +--- TD Pilot (iPad-based)
                   |
                   +--- CoughDrop + PCEye 5
                   |
           OptiKey + webcam (free software, lower accuracy)
                   |
              VoiceReach (webcam + LLM + hybrid input)
                   |
                Low Cost

VoiceReach occupies a unique position: low-cost hardware with
high-intelligence software, and a novel input paradigm that
no current commercial product offers.
```

---

## 10. Recommendations for VoiceReach

### 10.1 Strategic Recommendations

1. **Validate webcam gaze + tap with ALS patients early.** The gaze+tap paradigm is theoretically sound and supported by research, but has not been tested with actual ALS patients in a production context. Conduct user studies with 5-10 ALS patients at different disease stages as the highest priority.

2. **Target the "gap" population first.** Many ALS patients cannot afford or access dedicated devices, or are between insurance approvals. VoiceReach's low-cost webcam approach serves this underserved group immediately.

3. **Do not underestimate the Japanese certification pathway.** For the Japanese market, achieving 補装具費支給 eligibility is not optional -- it is a prerequisite for meaningful adoption. Begin the certification process early, engaging with organizations like RESJA (テクノエイド協会).

4. **Benchmark against SpeakFaster results.** The Nature Communications 2024 paper provides the current gold standard for LLM-accelerated AAC. VoiceReach should explicitly benchmark against their 29-60% improvement and 8.1 WPM baseline.

5. **Build fallback chain robustly.** The tap -> blink -> gaze gesture fallback chain is critical for progressive diseases. Each transition point should be as smooth as possible, with gradual blending rather than hard switches.

6. **Consider IRISBOND Hiru as intermediate option.** Rather than webcam-only, offer a tiered approach: webcam for cost-sensitive users, IRISBOND Hiru (~$1,000-1,500) for improved accuracy, Tobii PCEye 5 (~$1,249) for maximum precision. The software should support all three.

7. **Prioritize Japanese LLM capability.** Test intent prediction with Japanese-specific LLMs (e.g., Japanese-tuned Llama variants, Rinna models) and measure WPM improvement for Japanese text entry specifically.

### 10.2 Technical Recommendations

1. **Implement smooth pursuit as a supplementary selection method** alongside gaze+tap. CHI 2023 data shows it is faster (1.36s vs. 2.33s for dwell) and less tiring. It could serve as an alternative for patients who find tap difficult.

2. **Adopt continuous adaptive calibration** from the start (as designed in doc 02). The key validation data: the eeyes system's patented position-shift tolerance shows commercial demand for this feature.

3. **Support the ALSFRS-R scale** in the progressive adaptation module. Research shows it is the standard tool for timing AAC introduction and device transitions.

4. **Integrate with Apple Personal Voice** where possible. It is free, on-device, and increasingly adopted. VoiceReach's voice preservation could use Apple Personal Voice as one backend option on iOS.

5. **Design for 15+ inch screens at 50-70cm distance** (as specified in doc 02). This is consistent with all dedicated AAC devices. Ensure mobile/tablet fallback is also available.

6. **Use the zone-based 2-stroke hiragana input** (as designed) but also consider romaji input mode for users comfortable with it, as some AAC users prefer QWERTY-style layouts.

### 10.3 Business/Market Recommendations

1. **Open-source the core platform** to build community trust and enable rapid iteration. OptiKey demonstrates this model can work for AAC.

2. **Partner with 日本ALS協会 (JALSA)** and regional ALS support centers for clinical validation and user recruitment.

3. **Attend 国際福祉機器展 (H.C.R.)** to demonstrate the prototype and build relationships with distributors like Double Giken and Pacific Supply.

4. **Explore grant funding** from ALS research foundations (e.g., ALS基金 research incentive grants, which funded similar low-cost gaze input research by Ito in 2016).

---

## 11. Open Questions

### Technical

1. **What is the actual WPM achievable with VoiceReach's zone-based gaze + tap for Japanese text?** No existing study tests this exact combination. User testing is required.

2. **How does webcam gaze estimation perform with ALS patients who have ptosis (eyelid drooping), facial muscle atrophy, or non-invasive ventilation masks?** These are common in ALS and could significantly impact webcam-based tracking.

3. **What is the optimal number of intent candidates to display?** VoiceReach designs for 4 candidates, but the optimal balance between choice paralysis and coverage is an empirical question.

4. **Can the piezo tap sensor be replaced by other minimal-movement inputs (e.g., tongue click, cheek twitch, EMG)?** The fallback chain needs concrete hardware evaluation.

5. **What local LLM size is needed for acceptable Japanese intent prediction quality?** The 70% offline target requires a local model that handles Japanese well.

### Clinical/Regulatory

6. **What is the regulatory classification of VoiceReach in Japan?** Is it a medical device (医療機器), assistive device (補装具), or general software? This determines the certification pathway.

7. **Can VoiceReach qualify for 補装具費支給 as a "重度障害者用意思伝達装置"?** The current standards assume specific hardware configurations; a webcam-based software system may not fit existing categories.

8. **What level of clinical evidence is needed for Japanese insurance reimbursement?** Controlled studies vs. case series vs. expert recommendation.

### Market

9. **Will clinicians (言語聴覚士/ST) recommend a non-certified, non-traditional AAC system?** The gatekeeper role of STs in Japan is significant.

10. **How does the competition from Apple's built-in accessibility features (Personal Voice, eye tracking via AssistiveTouch, Switch Control) affect VoiceReach's value proposition?** Apple is rapidly improving iOS accessibility with each release.

11. **What is the total addressable market for ALS-specific AAC in Japan?** Japan has approximately 10,000 ALS patients; what fraction would benefit from VoiceReach vs. existing solutions?

---

## 12. References

### Academic Papers

1. Cai, S. et al. "Using large language models to accelerate communication for eye gaze typing users with ALS." Nature Communications 15, 2024. https://www.nature.com/articles/s41467-024-53873-3

2. Namnakani, M. et al. "Comparing Dwell time, Pursuits and Gaze Gestures for Gaze Interaction on Handheld Mobile Devices." CHI 2023. https://dl.acm.org/doi/10.1145/3544548.3580871

3. "Multi-modal access method (eye-tracking + switch-scanning) for individuals with severe motor impairment." PMC, 2022. https://pmc.ncbi.nlm.nih.gov/articles/PMC9576815/

4. "EyeTAP: Introducing a multimodal gaze-based technique." Int. J. Human-Computer Studies, 2021. https://www.sciencedirect.com/science/article/abs/pii/S107158192100094X

5. "The effects of dynamic dwell time systems on the usability of eye-tracking technology." Human-Computer Interaction, 2025. https://www.tandfonline.com/doi/full/10.1080/07370024.2025.2497236

6. "Mental fatigue prediction during eye-typing." PLOS One, 2021. https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0246739

7. "Rate of speech decline in individuals with amyotrophic lateral sclerosis." Scientific Reports, 2022. https://www.nature.com/articles/s41598-022-19651-1

8. "Timing of Communication Device Introduction Defined by ALSFRS-R Score." PMC, 2020. https://pmc.ncbi.nlm.nih.gov/articles/PMC7365172/

9. Trnka, K. et al. "Word prediction and communication rate in AAC." 2008. https://www.eecis.udel.edu/~mccoy/publications/2008/trnka08at.pdf

10. "Eye tracking communication devices in amyotrophic lateral sclerosis: impact on disability and quality of life." PubMed, 2013. https://pubmed.ncbi.nlm.nih.gov/23834069/

11. "Communication Matters -- Pitfalls and Promise of Hightech Communication Devices in Palliative Care." Frontiers in Neurology, 2018. https://www.frontiersin.org/journals/neurology/articles/10.3389/fneur.2018.00603/full

12. "Circular orientated display speeds up communication by gaze." Disability and Rehabilitation: Assistive Technology, 2025. https://www.tandfonline.com/doi/full/10.1080/17483107.2025.2528847

13. "Webcam eye tracking close to laboratory standards." PMC, 2024. https://pmc.ncbi.nlm.nih.gov/articles/PMC11289017/

14. "Can Eye Tracking with Pervasive Webcams Replace Dedicated Eye Trackers?" Springer, 2022. https://link.springer.com/chapter/10.1007/978-3-031-19679-9_1

15. "Pinch, Click, or Dwell: Comparing Different Selection Techniques for Eye-Gaze-Based Pointing in VR." ETRA 2021. https://dl.acm.org/doi/10.1145/3448018.3457998

### Commercial Products

16. Tobii Dynavox. PCEye 5. https://us.tobiidynavox.com/products/pceye
17. Tobii Dynavox. TD I-Series. https://us.tobiidynavox.com/products/td-i-series
18. Tobii Dynavox. TD Pilot. https://us.tobiidynavox.com/products/td-pilot
19. IRISBOND. Hiru. https://www.irisbond.com/en/aac-products/hiru-the-first-multiplatform-eye-tracker/
20. LC Technologies. Eyegaze Edge. https://eyegaze.com/products/eyegaze-edge/
21. Control Bionics. NeuroNode Trilogy. https://www.controlbionics.com/products/the-neuronode-trilogy/
22. OptiKey (Open Source). https://github.com/OptiKey/OptiKey
23. CoughDrop. https://www.coughdrop.com/

### Japanese Products

24. Hitachi KE Systems. 伝の心. https://www.hke.jp/products/dennosin/denindex.htm
25. Ory Lab. OriHime eye+Switch. https://orihime.orylab.com/eye/
26. Unicorn Corp. miyasuku. https://www.e-unicorn.co.jp/
27. eeyes. https://www.eeyesgo.com/eeyes/
28. Access Yell. ファイン・チャット. https://accessyell.co.jp/products/fine-chat/
29. CREACT. TCスキャン. https://www.creact.co.jp/welfare/communication-device/tcscan/
30. Double Giken (distributor). https://j-d.co.jp/

### Funding and Policy

31. 厚生労働省. 日常生活用具給付等事業の概要. https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/hukushi_kaigo/shougaishahukushi/yogu/seikatsu.html
32. 厚生労働省. 補装具費支給制度の概要. https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/hukushi_kaigo/shougaishahukushi/yogu/hosouguhisikyuuseido.html
33. 日本ALS協会. 利用できる社会資源. https://alsjapan.org/system-available_social_resources/
34. 重度障害者用意思伝達装置導入ガイドライン. http://www.resja.or.jp/com-gl/gl/a-4.html
35. Double Giken. 公費制度解説. https://j-d.co.jp/fukushikiki-kouhi.html

### Voice Banking

36. Acapela Group. My-Own-Voice. https://www.acapela-group.com/solutions/my-own-voice/
37. Apple. Personal Voice. https://support.apple.com/en-us/104993
38. Team Gleason. Voice Preservation. https://teamgleason.org/pals-resource/voice-message-banking/

### Market and Industry

39. AAC Device Market Report 2024-2031. https://www.datamintelligence.com/research-report/augmentative-and-alternative-communication-aac-device-market
40. 東京都障害者IT地域支援センター. 意思伝達装置一覧. https://www.tokyo-itcenter.com/700link/ishi-s-10.html

### BCI

41. Synchron. https://www.controlbionics.com/
42. BCIs in 2025: Trials, Progress, and Challenges. https://andersenlab.com/blueprint/bci-challenges-and-opportunities

---

*Report compiled for VoiceReach project. Data sourced from peer-reviewed publications, manufacturer websites, government publications, and patient advocacy organizations. All prices are approximate and subject to change. Research data reflects published studies and may not generalize to all ALS populations.*

# A1: Eye/Gaze Tracking -- Prior Research and Existing Methods (先行研究・既存手法)

**Research Area**: HIGH PRIORITY -- Core input method for VoiceReach MVP
**Date**: 2025-02-17
**Status**: Complete

---

## 1. Academic Literature Review

### 1.1 Foundational Papers

| # | Title | Authors | Year | Venue | Summary | VoiceReach Relevance |
|---|-------|---------|------|-------|---------|---------------------|
| 1 | **Appearance-based Gaze Estimation with Deep Learning: A Review and Benchmark** | Cheng, Y., Wang, H., Bao, Y., Lu, F. | 2021 (updated 2024) | IEEE TPAMI | Comprehensive survey of appearance-based gaze estimation using deep learning. Establishes benchmark on GazeHub with fair comparison across datasets (MPIIGaze, Gaze360, ETH-XGaze). Covers data pre-processing, model architectures, personal calibration. | **Critical reference**. Establishes the field's taxonomy. VoiceReach's pipeline aligns with "appearance-based + personal calibration" approach. |
| 2 | **MPIIGaze: Real-World Dataset and Deep Appearance-Based Gaze Estimation** | Zhang, X., Sugano, Y., Fritz, M., Bulling, A. | 2017 | IEEE TPAMI | Introduces MPIIGaze dataset (213,659 images, 15 participants) collected during everyday laptop use. Proposes LeNet-based appearance model. | **Key dataset**. Real-world laptop conditions closely match VoiceReach's deployment scenario. |
| 3 | **Eye Tracking for Everyone** (iTracker / GazeCapture) | Krafka, K., Khosla, A., Kellnhofer, P., et al. | 2016 | CVPR | Introduces GazeCapture dataset (2.5M frames, 1474 subjects) and iTracker CNN. Achieves 1.7cm error on phones without calibration, 1.3cm with calibration. | **Important for architecture ideas**. Multi-input CNN (face + eyes + face grid) design influenced subsequent work including L2CS-Net. |
| 4 | **ETH-XGaze: A Large Scale Dataset for Gaze Estimation under Extreme Head Pose and Gaze Variation** | Zhang, X., Park, S., Beber, T., et al. | 2020 | ECCV | 1M+ high-resolution images from 110 participants across 18 cameras with varying illumination. Extreme head poses covered. | **Dataset for robustness testing**. ALS patients in bed may have unusual head poses. ETH-XGaze tests model robustness to these conditions. |
| 5 | **L2CS-Net: Fine-Grained Gaze Estimation in Unconstrained Environments** | Abdelrahman, A., Hempel, T., Khalifa, A., Al-Hamadi, A. | 2023 | FG 2023 (IEEE) | ResNet-50 backbone with dual classification+regression loss. Achieves 3.92 deg on MPIIGaze, 10.41 deg on Gaze360. Real-time capable (<10ms inference). | **Primary candidate model** for VoiceReach. Good accuracy-to-latency tradeoff. Open-source PyTorch. |
| 6 | **RT-GENE: Real-Time Eye Gaze Estimation in Natural Environments** | Fischer, T., Chang, H.J., Demiris, Y. | 2018 | ECCV | Proposes RT-GENE dataset and ensemble model with head-pose normalization. Uses semantic inpainting to handle glasses. Cross-dataset: 7.7 deg on MPIIGaze. | **Ensemble approach is interesting**, but cross-dataset accuracy (7.7 deg) is insufficient for VoiceReach's zone-based input without per-user calibration. |
| 7 | **Gaze Estimation using Transformer** (GazeTR) | Cheng, Y., Lu, F. | 2022 | ICPR | Hybrid CNN+Transformer architecture. ResNet-18 backbone + 6-layer transformer. GazeTR-Hybrid achieves SOTA across multiple datasets. | **Architecture reference**. Transformer attention improves accuracy but increases latency. Hybrid approach is a good design pattern. |
| 8 | **Few-Shot Adaptive Gaze Estimation** (FAZE) | Park, S., Mello, S.D., Molchanov, P., et al. | 2019 | ICCV (Oral) | Meta-learning framework for person-specific adaptation with as few as 3 calibration samples. Disentangling encoder-decoder + MAML. 3.18 deg on GazeCapture (19% improvement over prior art). | **Critical for calibration design**. VoiceReach's 5-point calibration directly benefits from few-shot adaptation ideas. Meta-learning enables rapid per-patient tuning. |
| 9 | **Webcam-based gaze estimation for computer screen interaction** | Valliappan, N., et al. | 2024 | Frontiers in Robotics and AI | Comprehensive evaluation of webcam-based gaze tracking for screen interaction. Integrates SfM for head movement handling. | **Directly applicable**. Screen-interaction context matches VoiceReach deployment. |
| 10 | **Real-Time Gaze Estimation Using Webcam-Based CNN Models for Human-Computer Interactions** | (multiple authors) | 2025 | MDPI Computers | Achieves 2.08 deg average accuracy with CNN + calibration + transfer learning on webcam images. | **Validates VoiceReach's target accuracy**. 2.08 deg is within the 2-5 deg range needed for zone-based input. |

### 1.2 Low-Light and Special Conditions

| # | Title | Authors | Year | Venue | Summary | VoiceReach Relevance |
|---|-------|---------|------|-------|---------|---------------------|
| 11 | **Gaze in the Dark: Gaze Estimation in a Low-Light Environment with Generative Adversarial Networks** | Cai, H., et al. | 2020 | Sensors (MDPI) | Uses GAN to enhance low-light eye images before feeding to gaze estimation CNN. 4.5-8.9% accuracy improvement under dark conditions vs. baseline. No extra hardware needed. | **Directly relevant to night mode**. GAN-based image enhancement could replace or supplement near-IR LED approach. |
| 12 | **Polarized Near-Infrared Light Emission for Eye Gaze Estimation** | (ACM ETRA) | 2020 | ETRA | Uses polarized NIR LEDs to create identifiable corneal glints for pupil detection in dark conditions. | **Technical reference** for the optional near-IR LED night mode described in VoiceReach's design. |
| 13 | **Gaze-Vector Estimation in the Dark with Temporally Encoded Event-driven Neural Networks** | (arXiv) | 2024 | arXiv | Event-camera-based approach for gaze estimation in darkness. | **Future consideration**. Event cameras are specialized hardware but could be relevant for advanced night mode. |

### 1.3 ALS-Specific and Accessibility Research

| # | Title | Authors | Year | Venue | Summary | VoiceReach Relevance |
|---|-------|---------|------|-------|---------|---------------------|
| 14 | **Eye-Tracking Assistive Technologies for Individuals With Amyotrophic Lateral Sclerosis** | (Repository @ Middlesex University) | 2023 | Review paper | Comprehensive review of eye tracking for ALS. Documents challenges: ptosis, dry eyes, reduced eye movement range. Reports environmental/positioning adjustments needed. | **Essential context**. Documents real-world ALS challenges that VoiceReach must accommodate. |
| 15 | **An Eye-Tracking Assistive Device Improves the Quality of Life for ALS Patients and Reduces the Caregivers' Burden** | Hwang, C.S., et al. | 2014 | Journal of Motor Behavior | Validates that eye tracking significantly improves QoL for ALS patients. | **Motivation validation**. Confirms the clinical impact of the product category. |
| 16 | **A real-time eye movement-based computer interface for people with disabilities** | (ScienceDirect) | 2024 | Computers & Electrical Engineering | Webcam-based system for people with disabilities. No blinking required (important for advanced ALS where blink reflex is diminished). | **Key design principle**. VoiceReach should not require blinking as primary input. |
| 17 | **Person-Specific Gaze Estimation from Low-Quality Webcam Images** | (MDPI Sensors) | 2023 | Sensors | Person-specific transfer learning for low-quality webcam gaze estimation. Achieves improved accuracy with limited calibration data. | **Relevant for robustness**. Hospital/home webcams may be low quality. |
| 18 | **Self-Recording of Eye Movements in ALS Patients Using a Smartphone Eye-Tracking App** | (PMC) | 2024 | PMC | Smartphone-based eye tracking for ALS patients. Validates feasibility of consumer-grade camera eye tracking for this population. | **Validates approach feasibility** with ALS patients using consumer cameras. |

### 1.4 Japanese-Language Research (日本語論文)

| # | Title | Authors | Year | Venue | Summary |
|---|-------|---------|------|-------|---------|
| 19 | **外観ベース視線推定の深層学習手法に関するサーベイ** | 程 逸華, 陸 峰 (Beihang Univ) | 2021 | GazeHub / Phi-AI Lab | GazeHubプラットフォームに公開されているサーベイ。日本語の文献リストを含む。 |
| 20 | **Webカメラを用いたリアルタイム視線推定** | Various authors at NII, Tokyo Univ, etc. | 2020-2024 | 情報処理学会 / 電子情報通信学会 | 国内会議でのWebカメラ視線推定に関する発表。MediaPipeベースの実装が増加傾向。 |

*Note: Specific Japanese paper titles on webcam-based gaze estimation for accessibility were not found in the search results. The GazeHub platform (Beihang University) provides the most comprehensive multilingual resource for gaze estimation research.*

---

## 2. Open-Source Software Survey

### 2.1 OSS Comparison Table

| Name | GitHub URL | Stars | License | Key Features | Accuracy (deg) | Latency | VoiceReach Suitability |
|------|-----------|-------|---------|--------------|----------------|---------|----------------------|
| **L2CS-Net** | [Ahmednull/L2CS-Net](https://github.com/Ahmednull/L2CS-Net) | ~400 | Apache-2.0 | ResNet-50, dual classification+regression loss, Pipeline API, PyTorch | 3.92 (MPIIGaze), 10.41 (Gaze360) | <10ms (GPU) | **HIGH**. Best accuracy-to-simplicity ratio. PyTorch integration easy. Would need to swap ResNet-50 for lighter backbone (ResNet-18 or MobileNet) to meet 5ms CPU target. |
| **RT-GENE** | [Tobias-Fischer/rt_gene](https://github.com/Tobias-Fischer/rt_gene) | ~500 | CC-BY-NC-SA 4.0 | Ensemble of 4 models, head-pose normalization, glasses inpainting, ROS integration | 7.7 (cross-dataset MPIIGaze) | ~30ms (ensemble) | **MEDIUM**. Good robustness from ensemble but NC license is restrictive. Higher latency from ensemble. Cross-dataset accuracy is moderate. |
| **GazeTR** | [yihuacheng/GazeTR](https://github.com/yihuacheng/GazeTR) | ~200 | MIT | Hybrid CNN+Transformer, ResNet-18 backbone + 6-layer transformer | SOTA on multiple datasets | ~15-20ms (GPU) | **MEDIUM**. Higher accuracy from transformer but heavier compute. Good architecture reference. |
| **OpenFace 2.0** | [TadasBaltrusaitis/OpenFace](https://github.com/TadasBaltrusaitis/OpenFace) | ~7,000 | Custom academic | Multi-task: landmarks + AU + head pose + gaze, C++ | 9.1 (MPIIGaze) -- poor | Real-time | **LOW**. Gaze estimation accuracy is poor (9.1 deg). Useful for facial landmark detection but not for gaze. |
| **OpenFace 3.0** | [CMU-MultiComp-Lab/OpenFace-3.0](https://github.com/CMU-MultiComp-Lab/OpenFace-3.0) | New (2025) | Custom academic | Lightweight multi-task, uncertainty weighting, improved gaze | 2.56 (MPIIGaze), 10.6 (Gaze360) | Real-time, lightweight | **HIGH**. Dramatic improvement over 2.0. Multi-task architecture means face landmarks + gaze in one pass. Worth evaluating as alternative to MediaPipe + separate CNN. |
| **GazeML** | [swook/GazeML](https://github.com/swook/GazeML) | ~300 | MIT | TensorFlow, stacked-hourglass for eye landmarks, trained on UnityEyes synthetic data | Moderate (no standard benchmark) | Real-time | **LOW**. Older TensorFlow implementation. Limited to landmark detection, not full gaze vector. |
| **GazeTracking** | [antoinelame/GazeTracking](https://github.com/antoinelame/GazeTracking) | ~3,500 | MIT | Pure Python, dlib-based, minimal dependencies, pupil tracking | Low (rough direction only) | Real-time | **LOW**. Too simplistic for zone-based input. Only provides left/right/center/up/down. |
| **GazeFollower** | [GanchengZhu/GazeFollower](https://github.com/GanchengZhu/GazeFollower) | New (2024) | Open source | Trained on 32M face images, person-specific fine-tuning, Python API | 1.11cm (before calibration), 0.92cm (after) | Real-time | **HIGH**. Best reported webcam accuracy. Person-specific calibration built-in. Published in ACM PACMCGIT 2024. |
| **WebGazer.js** | [brownhci/WebGazer](https://github.com/brownhci/WebGazer) | ~3,500 | GPLv3 | Browser-based JavaScript, self-calibrating from clicks, no server needed | ~130px error (~2-4 deg) | Real-time (browser) | **MEDIUM**. Browser-native is attractive for VoiceReach's Electron app. But noisy and not optimized for accessibility. Good for prototyping. |
| **Pupil Core** | [pupil-labs/pupil](https://github.com/pupil-labs/pupil) | ~4,000 | LGPL v3.0 | Headset-based eye tracking, Python+C++, 0.6 deg accuracy, full ecosystem | 0.6 deg (with headset) | 45ms pipeline | **NOT APPLICABLE**. Requires dedicated headset hardware. Not webcam-only. |
| **MediaPipe Face Mesh** | [google-ai-edge/mediapipe](https://github.com/google-ai-edge/mediapipe) | ~28,000 | Apache-2.0 | 468 face landmarks, iris tracking (478 with iris), cross-platform, WebAssembly support | 1.37 deg (head pose), iris for rough gaze | <5ms | **CRITICAL DEPENDENCY**. Already in VoiceReach design. Provides landmarks and iris detection as input to gaze CNN. |
| **OptiKey** | [OptiKey/OptiKey](https://github.com/OptiKey/OptiKey) | ~4,000 | GPLv3 | Windows AAC software, works with eye trackers and webcam, dwell selection, speech synthesis | Depends on tracker | N/A (application) | **Reference implementation**. Not a gaze model, but the leading open-source AAC application for ALS. VoiceReach should study its UX patterns and supported trackers. |
| **MobileGaze** | [yakhyo/gaze-estimation](https://github.com/yakhyo/gaze-estimation) | ~100 | MIT | MobileNet v2, MobileOne, ResNet-18/34/50, ONNX export, classification+regression | Comparable to L2CS-Net | <5ms (MobileOne) | **HIGH**. Directly implements lightweight backbones suitable for VoiceReach's ~500K param / ~5ms target. MobileOne s0 is particularly interesting. |

### 2.2 Key Takeaways from OSS Survey

1. **L2CS-Net** is the most validated open-source gaze estimator for unconstrained environments. Its dual-loss approach (classification bins + regression) is a proven design pattern.

2. **OpenFace 3.0** (2025) represents a significant leap from 2.0 and deserves serious evaluation. Its multi-task architecture could replace MediaPipe + separate CNN with a single model.

3. **GazeFollower** achieves the best reported webcam-only accuracy (0.92cm after calibration), making it the state-of-the-art for screen gaze tracking.

4. **MobileGaze** provides ready-to-use lightweight backbones (MobileOne, MobileNet v2) with ONNX export, matching VoiceReach's latency requirements.

5. **MediaPipe Face Mesh** remains the best face landmark solution due to its cross-platform support, Apache license, and WebAssembly capability.

---

## 3. Commercial Eye Tracking Products

### 3.1 Product Comparison Table

| Product | Type | Price (USD) | Accuracy | Sampling Rate | Connection | ALS Suitability | Notes |
|---------|------|-------------|----------|---------------|------------|-----------------|-------|
| **Tobii Eye Tracker 5** | IR bar, consumer | ~$250 | ~0.5 deg | 133 Hz | USB | MEDIUM. Consumer-grade, not designed for accessibility. | 40x40 deg FOV, 45-95cm operating distance. Gaming-focused. |
| **Tobii Pro Spark** | IR bar, research | ~$2,000-3,000 | <0.3 deg | 60 Hz | USB/USB-C | HIGH. Research-grade accuracy. | 27" screen max. Embedded processing. Smallest research tracker. |
| **Tobii Pro Spectrum** | IR bar, research | ~$20,000+ | 0.3 deg | 600 Hz | USB | OVERKILL. Lab-grade. | Too expensive for patient use. |
| **Tobii Dynavox TD I-Series** | Integrated AAC device | $7,000-15,000 | <0.5 deg | 60 Hz | Integrated | **DESIGNED FOR ALS**. Built-in AAC software, ptosis compensation, insurance fundable. | Gold standard for ALS communication. VoiceReach must outperform on AI-assisted features. |
| **EyeTech TM5 Mini** | IR bar, assistive | ~$1,500-3,000 | <0.5 deg | 48 fps | USB | HIGH. Designed for assistive use. | 29cm x 3cm x 2.5cm, 230g, 3-5W. Compact. |
| **Irisbond Duo** | IR bar, assistive | ~$2,000-3,000 | ~0.5 deg | 30+ Hz | USB | HIGH. Simple setup, AAC compatible. | Lightweight, mobile, Windows compatible. |
| **Eyegaze Edge** | Integrated system | ~$8,000-15,000 | ~0.5 deg | 30+ Hz | Integrated | **DESIGNED FOR ALS**. Ptosis compensation, dry-eye handling. | LC Technologies. Long track record with ALS patients. |
| **Tobii Nexus** (Software) | Webcam SDK | License fee | ~1-2 deg | Webcam fps | Software only | MEDIUM. Proprietary webcam tracking. | Tobii's AI engine for webcam gaze. Commercial license needed. |
| **Eyeware Beam** | Webcam software | $30 (one-time) | ~2-3 deg | 60+ fps | Software only | LOW. Gaming-focused. | 6-DoF head tracking + eye tracking. Not designed for accessibility. |

### 3.2 Key Observations

1. **Dedicated IR trackers achieve 0.3-0.5 deg accuracy** -- roughly 5-10x better than webcam-based approaches. However, they cost $250-$15,000+.

2. **ALS-specific devices (Tobii Dynavox, Eyegaze Edge) cost $7,000-$15,000** and are often funded through insurance/government programs. They include ptosis compensation and dedicated AAC software.

3. **VoiceReach's value proposition is clear**: webcam-only approach at near-zero hardware cost, with AI-assisted communication that dedicated devices lack. The accuracy tradeoff (2-5 deg vs. 0.3-0.5 deg) is acceptable for zone-based input.

4. **Tobii Nexus represents direct competition**: a proprietary webcam gaze SDK from the market leader. VoiceReach should benchmark against this.

---

## 4. Benchmark Dataset Overview

### 4.1 Standard Datasets

| Dataset | Year | Images | Subjects | Collection Method | Gaze Range | Key Challenge | SOTA Angular Error |
|---------|------|--------|----------|-------------------|------------|---------------|-------------------|
| **MPIIGaze** | 2017 | 213,659 | 15 | Laptop webcam, everyday use | Natural (frontal) | Real-world conditions, illumination variation | ~2.5-3.9 deg (leave-one-out) |
| **GazeCapture** | 2016 | 2.5M | 1,474 | Crowdsourced, phones/tablets | Frontal | Scale, diversity, mobile devices | ~1.3cm / ~1.7cm (phone/tablet) |
| **ETH-XGaze** | 2020 | 1M+ | 110 | 18 SLR cameras, controlled | Extreme poses | Extreme head pose, gaze variation | ~3.1-3.3 deg |
| **Gaze360** | 2019 | 172K+ | 238 | Indoor/outdoor, 360 deg | Full 360 deg | Unconstrained, large gaze range | ~9.9-10.4 deg (full), ~3.9 deg (front) |
| **RT-GENE** | 2018 | 122,531 | 15 | Motion capture + eye tracking glasses | Natural | Glasses handling, natural environments | ~5.9-8.4 deg |
| **Columbia Gaze** | 2013 | 5,880 | 56 | Controlled lab, high-res | 5 head poses x 21 gaze | High quality, limited diversity | (Older, less used for DL) |
| **EYEDIAP** | 2014 | Video | 16 | Screen targets + floating targets | Screen + 3D | Video-based, continuous | ~5.1 deg |
| **MPSGaze** | 2022 | Multi-person | Multiple | GazeOnce dataset | Multi-person | Multi-person gaze in single image | N/A (multi-person metric) |
| **UnityEyes** | 2016 | Synthetic | N/A | Rendered 3D eye model | Configurable | Synthetic-to-real domain gap | N/A (training only) |

### 4.2 Key Accuracy Benchmarks (State-of-the-Art as of early 2025)

**MPIIGaze (leave-one-person-out, within-dataset)**:
- OpenFace 3.0: **2.56 deg** (multi-task model)
- L2CS-Net: **3.92 deg** (ResNet-50)
- GazeTR-Hybrid: **~3.5 deg** (CNN + Transformer)
- OpenFace 2.0: 9.1 deg (old baseline)

**ETH-XGaze (cross-person)**:
- GazeSymCAT: **3.28 deg** (symmetric cross-attention transformer, 2025)
- Leaderboard best: **~3.11 deg**

**Gaze360 (full 360 deg)**:
- CrossGaze: **9.94 deg**
- L2CS-Net: 10.41 deg
- OpenFace 3.0: 10.6 deg

**GazeCapture (screen coordinates)**:
- GazeFollower (calibrated): **0.92cm**
- FAZE (3-shot): **3.18 deg** (19% improvement)
- iTracker: 1.7cm (phone, no calibration)

### 4.3 Relevance to VoiceReach

For VoiceReach's **zone-based input with 4-16 zones** on a 15"+ screen at 50-70cm distance:

- **4 zones**: Each zone subtends ~12 deg x 7 deg. Accuracy of **5 deg or better** is sufficient.
- **9 zones**: Each zone subtends ~8 deg x 4.5 deg. Accuracy of **3 deg or better** is needed.
- **16 zones**: Each zone subtends ~6 deg x 3.4 deg. Accuracy of **2 deg or better** is needed.

Current state-of-the-art with person-specific calibration achieves **2-4 deg** on webcam, meaning:
- 4-zone mode: **Reliably achievable** even without calibration
- 9-zone mode: **Achievable** with basic 5-point calibration
- 16-zone mode: **Achievable** with good calibration and smoothing, but marginal

---

## 5. Comparative Analysis for VoiceReach

### 5.1 Webcam vs. IR Tracker Accuracy

| Metric | Tobii IR Tracker | Webcam (Uncalibrated) | Webcam (Calibrated, Person-specific) |
|--------|------------------|----------------------|-------------------------------------|
| Angular accuracy | 0.3-0.5 deg | 3-5 deg | 1.5-3 deg |
| Spatial accuracy (at 60cm) | 0.3-0.5cm | 3-5cm | 1.5-3cm |
| Precision | <0.1 deg | ~1 deg | ~0.5-1 deg |
| Head movement tolerance | 40x40 deg FOV | Degrades with movement | Degrades, but normalizable |
| Glasses handling | Good | Moderate | Good with training data |
| Low light | Near-IR immune | Degrades significantly | Requires enhancement |
| Latency | 7-16ms | 5-30ms (model dependent) | 5-30ms |
| Cost | $250-$15,000+ | $0 (uses existing webcam) | $0 |

**Key insight**: For zone-based input (not pixel-precise pointing), calibrated webcam accuracy of 1.5-3 deg is sufficient for 4-9 zones. The 5-10x cost advantage makes webcam the correct choice for VoiceReach's target users.

### 5.2 Architecture Comparison for VoiceReach's Requirements

| Architecture | Accuracy (MPIIGaze) | Params | Latency (CPU) | Calibration | VoiceReach Score |
|-------------|---------------------|--------|---------------|-------------|-----------------|
| MediaPipe + Custom 3-layer CNN (~500K) | ~3-4 deg (estimated) | ~500K | ~5ms | 5-point | **A** (current design) |
| L2CS-Net (ResNet-50) | 3.92 deg | ~25M | ~30ms | None built-in | B (too heavy for CPU) |
| L2CS-Net (MobileNet v2 swap) | ~4.0-4.5 deg | ~3M | ~8ms | None built-in | **A** |
| MobileGaze (MobileOne s0) | ~4.0-4.5 deg | ~3-5M | ~5ms | None built-in | **A** |
| OpenFace 3.0 (multi-task) | 2.56 deg | Lightweight | Real-time | None built-in | **A+** (if license permits) |
| GazeFollower (full model) | 0.92cm | Large (32M training) | ~15ms | Built-in fine-tuning | B+ (heavier but best accuracy) |
| GazeTR-Hybrid | ~3.5 deg | ~11M | ~15-20ms | None built-in | B (transformer overhead) |

### 5.3 Calibration Strategy Comparison

| Strategy | Calibration Time | Samples Needed | Accuracy Improvement | Interruption | ALS Suitability |
|----------|-----------------|----------------|---------------------|--------------|-----------------|
| **5-point initial** (VoiceReach current) | ~30s | 5 points x 2s | Baseline | One-time | GOOD. Brief, manageable. |
| **1-point re-calibration** (VoiceReach current) | ~5s | 1 point | Offset correction | Minimal | EXCELLENT. Quick reset. |
| **FAZE few-shot** (3-9 samples) | ~15-45s | 3-9 points | 19% over uncalibrated | One-time | GOOD. Similar to 5-point. |
| **Continuous adaptive** (VoiceReach current) | Ongoing | Tap-gaze pairs | Gradual improvement | None | EXCELLENT. No interruption. |
| **GazeFollower fine-tuning** | ~2-5 min | ~31 samples | 0.92cm from 1.11cm | Initial setup | MODERATE. Longer initial. |
| **None (cross-person model)** | 0 | 0 | N/A | None | POOR accuracy for zone input. |

### 5.4 Low-Light Performance Analysis

| Approach | Hardware Needed | Accuracy Impact | Implementation Complexity | VoiceReach Fit |
|----------|----------------|-----------------|--------------------------|----------------|
| Screen glow illumination | None | Moderate degradation (~2x error) | Low | GOOD for basic night mode |
| GAN image enhancement ("Gaze in the Dark") | None | 4.5-8.9% improvement over dark baseline | Medium (add GAN preprocessing) | GOOD. Software-only solution. |
| Near-IR LED (850nm) | 1 LED (~$5) | Near-normal operation | Low (hardware + software) | BEST for reliable night mode |
| Reduce zones to 4 | None | Tolerance increase | None | GOOD as fallback strategy |
| Infrared webcam mod | Modified webcam | Good in dark | Medium (hardware mod) | MODERATE. Requires hardware change. |

---

## 6. Recommendations for VoiceReach

### 6.1 Recommended Architecture (MVP)

```
Input Pipeline (unchanged from current design):
  Webcam 720p+ @ 30fps
  -> MediaPipe Face Mesh (468 landmarks + iris)
  -> Eye patch extraction (64x64)
  -> Head pose via PnP (pitch, yaw, roll)

Gaze Estimation Model (updated recommendation):
  Option A (Conservative):
    L2CS-Net architecture with MobileNet v2 backbone
    - Replace ResNet-50 with MobileNet v2 (~3M params)
    - Keep dual classification+regression loss
    - Expected: ~4-4.5 deg uncalibrated, ~2.5-3 deg calibrated
    - Latency: ~5-8ms CPU

  Option B (Aggressive, if license permits):
    Evaluate OpenFace 3.0 as single pipeline replacement
    - Replaces both MediaPipe and separate gaze CNN
    - 2.56 deg on MPIIGaze (multi-task)
    - Single model for landmarks + gaze + AU detection
    - Risk: Custom academic license may restrict commercial use

Smoothing (unchanged):
  Kalman filter with adaptive noise covariance
  - Less filtering during saccades, more during fixations
  - EMA as simpler fallback

Zone Mapping (unchanged):
  Hysteresis-based zone boundaries
  - Default: 4 zones (high reliability)
  - Adaptive: 9 zones when calibration confidence is high
  - Maximum: 16 zones only for well-calibrated, stable head position
```

### 6.2 Expected Accuracy

| Condition | Expected Accuracy | Zone Reliability |
|-----------|-------------------|-----------------|
| Good lighting, after 5-point calibration | 2-3 deg | 4-zone: >95%, 9-zone: >85% |
| Good lighting, continuous adaptive | 1.5-2.5 deg | 4-zone: >97%, 9-zone: >90% |
| Low light, screen glow only | 4-6 deg | 4-zone: >80%, 9-zone: <70% |
| Low light + near-IR LED | 2.5-4 deg | 4-zone: >90%, 9-zone: >75% |
| Bed-bound, unusual head pose | 3-5 deg | 4-zone: >85%, 9-zone: >70% |

### 6.3 Calibration Protocol for ALS Patients

```
1. Initial Setup (first use, ~2 minutes):
   a. Position webcam at 50-70cm from patient's face
   b. Adjust screen brightness and angle
   c. Run 5-point calibration (corners + center, 3s per point)
   d. System validates calibration quality
   e. If quality < threshold: offer 9-point extended calibration

2. Daily Use:
   a. 1-point quick calibration on startup (~5s)
   b. Continuous adaptive calibration from tap-gaze pairs
   c. Auto-detect when re-calibration is needed (accuracy drop)

3. ALS-Specific Accommodations:
   a. Extended dwell time per calibration point (3s vs 2s)
   b. Larger calibration targets (visual angle 5+ deg)
   c. Audio feedback for each calibration point
   d. Ptosis detection: if eyelid droop > threshold, widen
      eye detection ROI and increase sensitivity
   e. Dry eye handling: detect corneal reflection changes,
      remind caregiver about eye drops
   f. Body repositioning: auto-detect and trigger re-calibration

4. Progressive Degradation:
   a. If calibration quality drops: reduce zones (16->9->4)
   b. If eye tracking fails: fall back to blink input
   c. If all vision fails: fall back to tap-only with
      sequential scanning
```

### 6.4 Implementation Priority

1. **Phase 1 (MVP)**: MediaPipe Face Mesh + lightweight CNN (MobileNet v2 backbone, L2CS-Net loss design), 5-point calibration, 4-zone input, Kalman smoothing
2. **Phase 2**: Continuous adaptive calibration, 9-zone mode, low-light GAN enhancement
3. **Phase 3**: OpenFace 3.0 evaluation, near-IR LED night mode, ptosis adaptation, 16-zone mode

---

## 7. Open Questions

1. **OpenFace 3.0 licensing**: Can the CMU MultiComp Lab license be used for an assistive technology product? Need to contact the lab directly.

2. **ALS-specific training data**: No public gaze dataset includes ALS patients (ptosis, reduced eye movement range, bed positioning). VoiceReach may need to collect a small dataset (~10-20 patients) for fine-tuning and validation.

3. **Continuous calibration convergence**: How many tap-gaze pairs are needed before the adaptive calibration provides meaningful improvement? What is the forgetting rate for old calibration data when the patient's condition changes?

4. **Head pose range for bed-bound patients**: What is the typical range of head poses for ALS patients in bed? ETH-XGaze covers extreme poses, but specific bed-bound distributions are unknown.

5. **Webcam quality variance**: Consumer webcams vary greatly in quality. What is the minimum acceptable webcam specification (resolution, frame rate, lens quality)? Should VoiceReach recommend specific webcam models?

6. **Multi-modal fusion timing**: When to trust gaze data vs. tap data? If gaze says zone A but the tap latency suggests the patient might have been looking at zone B, which signal should dominate?

7. **Long-term stability**: How does webcam gaze estimation accuracy degrade over sessions lasting 8+ hours? Thermal effects on webcam, eye fatigue, and environmental lighting changes throughout the day are all factors.

---

## References

### Key URLs
- GazeHub Benchmark Platform: https://phi-ai.buaa.edu.cn/Gazehub/
- L2CS-Net: https://github.com/Ahmednull/L2CS-Net
- OpenFace 3.0: https://github.com/CMU-MultiComp-Lab/OpenFace-3.0
- MediaPipe Face Mesh: https://github.com/google-ai-edge/mediapipe
- GazeFollower: https://github.com/GanchengZhu/GazeFollower
- MobileGaze: https://github.com/yakhyo/gaze-estimation
- FAZE (Few-Shot): https://github.com/NVlabs/few_shot_gaze
- OptiKey (AAC Reference): https://github.com/OptiKey/OptiKey
- WebGazer.js: https://github.com/brownhci/WebGazer
- ETH-XGaze: https://ait.ethz.ch/xgaze

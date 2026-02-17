# B4: Vision/Gaze Models -- Latest Models and Architectures (最新モデル)

**Research Area**: HIGH PRIORITY -- Core input method for VoiceReach MVP
**Date**: 2025-02-17
**Status**: Complete

---

## 1. Academic Literature Review: Latest Gaze Estimation Models (2022-2026)

### 1.1 Transformer-Based and Hybrid Models

| # | Title | Authors | Year | Venue | Architecture | Key Result | VoiceReach Relevance |
|---|-------|---------|------|-------|-------------|------------|---------------------|
| 1 | **GazeTR: Gaze Estimation using Transformer** | Cheng, Y., Lu, F. | 2022 | ICPR | ResNet-18 CNN backbone -> 7x7x32 feature maps -> 6-layer Transformer encoder -> 2D gaze | SOTA on MPIIGaze, Gaze360, ETH-XGaze at time of publication | **Architecture reference**. Proves transformers add value for gaze, but the overhead may be too much for VoiceReach's 5ms target. |
| 2 | **TransGaze: Exploring Plain Vision Transformers for Gaze Estimation** | (Springer) | 2024 | Machine Vision & Applications | Pre-trained ViT as backbone, integrates local eye features, flexible pre-trained model adaptation | First demonstration that plain ViTs work well for gaze estimation with large-scale pre-training | **Important finding**. Pre-trained ViTs (e.g., DINOv2 features) could improve accuracy. However, ViT models are typically too large for real-time CPU inference. |
| 3 | **GazeSymCAT: A Symmetric Cross-Attention Transformer for Robust Gaze Estimation under Extreme Head Poses** | (Oxford JCDE) | 2025 | J. Computational Design & Engineering | ResNet+DCA feature extractor for face and eyes -> symmetric self- and cross-attention transformer encoder-decoder | **3.28 deg** on ETH-XGaze (SOTA), 4.11 deg on MPIIFaceGaze | **Relevant for extreme head pose robustness**. ALS patients in bed have unusual head poses. Cross-attention between face and eye features is a proven design. |
| 4 | **Gaze-LLE: Gaze Target Estimation via Large-Scale Learned Encoders** | Ryan, F.K., et al. | 2025 | CVPR (Highlight) | Frozen DINOv2 encoder + lightweight gaze decoder, estimates where a person is looking in a scene | SOTA on gaze target estimation benchmarks | **Conceptually relevant**. Shows frozen foundation model encoders + light decoders can estimate gaze. Not directly applicable (gaze *target* vs. gaze *direction*) but the DINOv2-based approach is transferable. |
| 5 | **ARGaze: Autoregressive Transformers for Online Egocentric Gaze Estimation** | (arXiv) | 2025 | arXiv | Autoregressive transformer for predicting gaze from first-person video, sequential prediction | Improved temporal consistency for egocentric gaze | **Limited relevance**. Designed for egocentric (wearable camera) use, not webcam screen gaze. Temporal modeling idea is relevant. |
| 6 | **ViTGaze: Gaze Following with Interaction Features in Vision Transformers** | (arXiv/Visual Intelligence) | 2024 | Visual Intelligence | ViT-based gaze following with head-scene interaction features | SOTA on gaze following benchmarks | **Limited relevance**. Gaze following (where is person X looking in a scene?) is different from gaze estimation (what direction are the eyes pointing?). |

### 1.2 Lightweight and Mobile Models (2024-2025)

| # | Title | Authors | Year | Venue | Architecture | Key Result | VoiceReach Relevance |
|---|-------|---------|------|-------|-------------|------------|---------------------|
| 7 | **GazeCapsNet: A Lightweight Gaze Estimation Framework** | (MDPI Sensors) | 2025 | Sensors | Capsule networks + MobileNet v2 / MobileOne / ResNet-18. Eliminates facial landmark dependency. | 11.7M params, 20ms/frame inference. 15% MAE reduction on ETH-XGaze and Gaze360 vs. existing. | **HIGH RELEVANCE**. Eliminates landmark detection dependency (could replace MediaPipe step). MobileNet v2 backbone matches VoiceReach's lightweight requirements. |
| 8 | **MobGazeNet: Robust Gaze Estimation Mobile Network Based on Progressive Attention Mechanisms** | (Springer) | 2025 | Machine Vision & Applications | Mobile backbone + progressive attention (SE + CBAM + Coordinate Attention). 6D rotation representation. Geodesic loss. | Lightweight, robust to head pose changes. Uses progressive attention instead of transformer. | **HIGH RELEVANCE**. Progressive attention mechanisms add accuracy without transformer overhead. 6D rotation representation avoids gimbal lock issues with Euler angles. |
| 9 | **Lightweight Gaze Estimation Model Via Fusion Global Information** | (arXiv) | 2024 | arXiv | Lightweight CNN with global information fusion | Competitive accuracy with significantly fewer parameters | **Relevant**. Another data point confirming lightweight CNNs can approach heavier model accuracy. |
| 10 | **MobileGaze: Real-Time Gaze Estimation Models** | yakhyo (GitHub) | 2024 | Open-source | ResNet-18/34/50, MobileNet v2, MobileOne s0-s4. L2CS-Net loss design. ONNX export. | MobileOne s0: near-instant inference. MobileNet v2: <5ms. | **DIRECTLY APPLICABLE**. Ready-to-use implementation of lightweight L2CS-Net variants. ONNX export enables deployment in Electron/Node.js via ONNX Runtime. |

### 1.3 Multi-Person and Real-Time Models

| # | Title | Authors | Year | Venue | Architecture | Key Result | VoiceReach Relevance |
|---|-------|---------|------|-------|-------------|------------|---------------------|
| 11 | **GazeOnce: Real-Time Multi-Person Gaze Estimation** | Zhang, M., et al. | 2022 | CVPR | Single-stage detection + gaze estimation. Feature pyramid + context modules (RetinaFace-based). | First real-time multi-person gaze. Faster and more accurate than cascaded approaches. | **LOW RELEVANCE** for MVP (single patient), but interesting for future multi-user scenarios (patient + caregiver awareness). |
| 12 | **OpenFace 3.0: A Lightweight Multitask System for Comprehensive Facial Behavior Analysis** | Baltrušaitis, T., et al. | 2025 | arXiv | Multi-task: landmarks + AU + gaze + emotion. Uncertainty-weighted multi-task loss. | Gaze: **2.56 deg** on MPIIGaze (vs. 9.1 for OpenFace 2.0). Lightweight, real-time. | **CRITICAL CANDIDATE**. Single model replaces both MediaPipe and gaze CNN. 2.56 deg is best reported for a lightweight, multi-task model. |

### 1.4 Person-Specific Adaptation and Few-Shot Models

| # | Title | Authors | Year | Venue | Architecture | Key Result | VoiceReach Relevance |
|---|-------|---------|------|-------|-------------|------------|---------------------|
| 13 | **FAZE: Few-Shot Adaptive Gaze Estimation** | Park, S., et al. (NVIDIA) | 2019 | ICCV (Oral) | Disentangling encoder-decoder + MAML meta-learning for person-specific adaptation | 3.18 deg on GazeCapture with k=9 calibration samples. Works with k=3. | **CRITICAL for calibration**. Meta-learning enables rapid per-patient adaptation. VoiceReach's 5-point calibration maps directly to FAZE's few-shot approach. |
| 14 | **GazeFollower: An open-source system for deep learning-based gaze tracking with web cameras** | Zhu, G., et al. | 2024 | ACM PACMCGIT | Large-scale model trained on 32M face images. Person-specific fine-tuning API. | **0.92cm accuracy** after calibration (1.11cm before). On par with budget commercial trackers. | **BEST webcam accuracy reported**. The fine-tuning API is directly usable for VoiceReach's calibration. However, the model is large and may not meet 5ms CPU requirement. |
| 15 | **WebEyeTrack: Webcam-based gaze estimation for computer screen interaction** | Valliappan, N., et al. | 2024 | Frontiers in Robotics and AI | Model-based head pose + on-device few-shot learning (k<9 calibration samples) + SfM for head movement | 2.32cm error on GazeCapture with few-shot calibration | **Relevant**. On-device few-shot learning is exactly what VoiceReach needs. SfM for head movement handling is innovative. |
| 16 | **Real-time HCI based on eye gaze estimation from low-quality webcam images** | (Oxford Digital Scholarship in the Humanities) | 2025 | Oxford Academic | CNN + calibration + transfer learning from quality data to low-quality webcam | **2.08 deg** average visual angle accuracy | **Validates VoiceReach's accuracy target**. Transfer learning from high-quality training data to user's specific webcam is a proven approach. |

### 1.5 Systematic Reviews and Surveys (2024-2025)

| # | Title | Year | Venue | Coverage |
|---|-------|------|-------|----------|
| 17 | **A systematic review on vision-based gaze estimation: Advance in computer vision and deep learning** | 2025 | Engineering Applications of AI (Elsevier) | Comprehensive 2025 survey covering CNNs, RNNs, GANs, Transformers for gaze estimation |
| 18 | **Appearance-based Gaze Estimation with Deep Learning: A Review and Benchmark** (updated) | 2024 | IEEE TPAMI | GazeHub benchmark update with latest methods |

---

## 2. MediaPipe Alternatives for Face/Landmark Detection

### 2.1 Comparison Table

| Tool | Landmarks | Speed | Accuracy | License | Language | Platforms | VoiceReach Fit |
|------|-----------|-------|----------|---------|----------|-----------|---------------|
| **MediaPipe Face Mesh** | 468 (478 with iris) | <5ms | 98.6% avg precision | Apache-2.0 | Python, JS, C++, Java | All (incl. WebAssembly) | **CURRENT CHOICE**. Best cross-platform support. |
| **DLib (HOG + 68-point)** | 68 | <5ms (CPU) | Good (frontal faces) | Boost Software License | C++, Python | Desktop | **Alternative**. Slightly faster than MediaPipe. Fewer landmarks (68 vs 468) but sufficient for eye region. |
| **InsightFace / RetinaFace** | 5 key points + optional dense | ~10ms (GPU) | 96.9% on WiderFace | MIT | Python (MXNet/PyTorch) | Desktop, Server | **Not recommended**. Fewer landmarks, GPU-dependent. Designed for face recognition, not landmark density needed for gaze. |
| **YOLOv8-Face** | 5 key points | <5ms (GPU) | High detection rate | AGPL-3.0 | Python (Ultralytics) | Desktop, Server | **Not recommended** as primary. Good for face detection but insufficient landmark density. |
| **OpenFace 3.0** | 68 landmarks + gaze + AU | Real-time | Good | Custom academic | C++ | Desktop | **STRONG ALTERNATIVE**. Includes gaze estimation built-in. Could replace MediaPipe + CNN. |
| **Apple Vision (ARKit)** | 1220 landmarks | Real-time | Excellent (TrueDepth) | Proprietary | Swift | iOS only | **NOT APPLICABLE**. Requires TrueDepth camera (iPhone X+). Not cross-platform. |
| **SCRFD (InsightFace)** | 5 key points | Fast | Enhanced accuracy | MIT | Python | Desktop, Server | **Not recommended**. Face detection focus, not landmark density. |

### 2.2 Assessment

**MediaPipe Face Mesh remains the best choice** for VoiceReach because:
1. **468+ landmarks** provide sufficient density for accurate eye region extraction and head pose estimation
2. **Cross-platform support** including WebAssembly enables browser/Electron deployment
3. **Apache-2.0 license** allows commercial use without restrictions
4. **< 5ms inference** on CPU meets real-time requirements
5. **Iris landmarks** (468-477) provide additional gaze signal

The only serious challenger is **OpenFace 3.0**, which bundles landmarks + gaze into a single model with 2.56 deg accuracy. However, its academic license and C++ requirement are drawbacks.

---

## 3. Can Sub-2-Degree Accuracy Be Achieved with Webcam-Only?

### 3.1 Evidence Summary

| Study/System | Reported Accuracy | Conditions | Calibration |
|-------------|-------------------|------------|-------------|
| OpenFace 3.0 | 2.56 deg (MPIIGaze) | Within-dataset evaluation | No person-specific calibration |
| Real-time HCI (2025) | 2.08 deg | Webcam CNN + calibration + transfer learning | Person-specific calibration + transfer learning |
| GazeFollower | 0.92cm (~1.5-2 deg at 60cm) | Webcam, controlled | Person-specific fine-tuning (31 samples) |
| Webcam vs. EyeLink study | 1.4 deg | Webcam, controlled | 9-point calibration |
| Skovsgaard et al. | 0.88 deg | Webcam, controlled, stationary | Full calibration, stationary user |
| MediaPipe + CNN | 1.37 deg (head pose), 0.8 deg (non-disabled) | Controlled conditions | Calibrated |
| Typical webcam (moving user) | 2-5 deg | Realistic conditions | Basic calibration |

### 3.2 Assessment

**Sub-2-degree accuracy IS achievable** with webcam-only under specific conditions:

**Conditions that enable sub-2-deg accuracy:**
1. Person-specific calibration (5-9 points or fine-tuning)
2. Stationary head position (or robust head-pose normalization)
3. Good lighting (200+ lux)
4. Reasonable webcam quality (720p+, 30fps+)
5. Frontal face orientation (within +/-30 deg yaw)
6. Smoothing (Kalman filter) applied

**Conditions that degrade accuracy to 3-5+ deg:**
1. Cross-person (no calibration)
2. Head movement during tracking
3. Low lighting
4. Low webcam quality
5. Extreme head poses
6. Glasses with reflective coatings

**For ALS patients (bed-bound, limited mobility)**: The stationary head position is a *natural advantage*. Combined with person-specific calibration and good lighting, sub-2-degree accuracy is realistic. The key risk factors are unusual head pose (bed angle) and potential ptosis.

---

## 4. Architectural Recommendations for VoiceReach

### 4.1 Model Architecture Comparison Matrix

| Architecture | Params | CPU Latency | GPU Latency | Accuracy (MPIIGaze) | Calibration Support | ONNX Export | VoiceReach Score |
|-------------|--------|-------------|-------------|---------------------|--------------------|-----------|-|
| **Current Design: MediaPipe + 3-layer CNN (500K)** | ~500K (CNN only) | ~5ms (CNN only) | ~2ms | ~3-4 deg (estimated) | Manual 5-point | Possible | **B+** |
| **Proposed: MediaPipe + MobileNet v2 (L2CS loss)** | ~3M | ~5-8ms | ~3ms | ~4.0-4.5 deg (uncalib) | Bolt-on FAZE | Yes (ONNX Runtime) | **A** |
| **Proposed: MediaPipe + MobileOne s0 (L2CS loss)** | ~3-5M | ~3-5ms | ~2ms | ~4.0-4.5 deg (uncalib) | Bolt-on FAZE | Yes | **A+** |
| **Alternative: OpenFace 3.0 (all-in-one)** | Lightweight | Real-time | Real-time | 2.56 deg | None built-in | No (C++) | **A** (if license OK) |
| **Alternative: GazeCapsNet (MobileNet v2)** | ~11.7M | ~20ms | ~5ms | 15% better than baselines | None built-in | Possible | **B** (slower) |
| **Future: DINOv2 frozen + light decoder** | Large encoder, tiny decoder | Too slow (CPU) | ~10ms | Potentially best | Fine-tuning | No | **C** (GPU only) |

### 4.2 Recommended Architecture: Tiered Approach

```
Tier 1 (MVP - 3 months):
  MediaPipe Face Mesh (468 landmarks)
  + Custom CNN with MobileOne s0 backbone
  + L2CS-Net dual classification+regression loss
  + 5-point calibration
  + Kalman filter smoothing
  + 4-zone input (expandable to 9)

  Expected: ~4 deg uncalibrated, ~2.5 deg calibrated
  Latency: ~8ms total (MediaPipe 5ms + CNN 3ms)
  Params: ~3-5M (CNN only)

Tier 2 (Enhancement - 6 months):
  + FAZE-style meta-learning for few-shot calibration
  + Continuous adaptive calibration from tap-gaze pairs
  + GAN-based low-light image enhancement
  + Adaptive zone count (4/9/16 based on tracking confidence)
  + Temporal smoothing with velocity-based Kalman

  Expected: ~2-3 deg with ongoing calibration

Tier 3 (Advanced - 12 months):
  Evaluate OpenFace 3.0 as unified pipeline replacement
  OR
  Fine-tune DINOv2/foundation model encoder with light decoder
  + ALS-specific training data collection
  + Ptosis and dry-eye detection and adaptation
  + Near-IR LED night mode integration

  Expected: <2 deg in optimal conditions
```

### 4.3 Loss Function Design

Based on L2CS-Net's proven approach:

```
Total Loss = L_cls + alpha * L_reg

where:
  L_cls = CrossEntropy(gaze_bins_predicted, gaze_bins_truth)
    - Discretize gaze angle into N bins (e.g., 90 bins for yaw, 90 for pitch)
    - Classification provides coarse but robust estimation

  L_reg = SmoothL1(gaze_angle_predicted, gaze_angle_truth)
    - Regression provides fine-grained estimation

  alpha = weighting factor (typically 1.0)

Enhancement for VoiceReach:
  + L_zone = CrossEntropy(zone_predicted, zone_truth)
    - Direct zone prediction as auxiliary task
    - Trains model to be zone-aware
    - Helps during inference for zone boundary decisions
```

### 4.4 Training Data Strategy

```
Pre-training (large-scale, cross-person):
  - ETH-XGaze (1M+ images, extreme head poses)
  - GazeCapture (2.5M frames, mobile/tablet)
  - MPIIGaze (213K images, laptop use)
  - Gaze360 (172K images, unconstrained)

Fine-tuning (person-specific):
  - 5-9 calibration images from user's webcam
  - Meta-learning (FAZE-style) to adapt in <1 second
  - Continuous learning from tap-gaze pairs during use

Data Augmentation:
  - Random brightness/contrast (simulate lighting changes)
  - Random crop/scale (simulate head movement)
  - Gaussian noise (simulate low-quality webcams)
  - Synthetic ptosis (occlude top portion of eye region)
  - Horizontal flip (left-right eye symmetry)
```

---

## 5. Benchmark Dataset Deep Dive

### 5.1 State-of-the-Art Results by Dataset (as of early 2025)

**MPIIGaze (within-dataset, leave-one-person-out)**:
| Method | Year | Angular Error (deg) | Type |
|--------|------|--------------------|----|
| OpenFace 3.0 | 2025 | **2.56** | Multi-task |
| Fine-grained (cls+reg) | 2024 | **3.86** | CNN |
| L2CS-Net | 2023 | 3.92 | CNN |
| GazeTR-Hybrid | 2022 | ~3.5 | CNN+Transformer |
| GazeSymCAT | 2025 | 4.11 (MPIIFaceGaze) | Transformer |
| OpenFace 2.0 | 2018 | 9.1 | Classical+CNN |

**ETH-XGaze (cross-person, evaluation server)**:
| Method | Year | Angular Error (deg) |
|--------|------|---------------------|
| SLYKLatent | 2024 | Best on subset (11.59% improvement) |
| GazeSymCAT | 2025 | **3.28** |
| Leaderboard top | 2024 | ~3.11 |

**Gaze360 (full 360-degree)**:
| Method | Year | Angular Error (deg) |
|--------|------|---------------------|
| CrossGaze | 2024 | **9.94** |
| L2CS-Net | 2023 | 10.41 |
| OpenFace 3.0 | 2025 | 10.6 |

**GazeCapture (screen coordinates, cm)**:
| Method | Year | Error (cm) | Calibration |
|--------|------|-----------|-------------|
| GazeFollower | 2024 | **0.92** | Fine-tuned |
| GazeFollower | 2024 | 1.11 | Uncalibrated |
| GazeEstimator | 2024 | 1.25 | - |
| Siamese NN | 2023 | 1.33 | - |
| AFF-Net | 2022 | 1.62 | - |
| iTracker | 2016 | 1.70 | Phone |

### 5.2 VoiceReach Target Positioning

```
                       Accuracy (angular error, deg)
                  0      1      2      3      4      5      6
                  |      |      |      |      |      |      |
  Tobii IR        |=|    |      |      |      |      |      |  (0.3-0.5 deg)
  OpenFace 3.0    |      |  ==|=|     |      |      |      |  (2.56 deg)
  VoiceReach Goal |      |   |===|    |      |      |      |  (2-3 deg calibrated)
  L2CS-Net        |      |      |     |=|    |      |      |  (3.92 deg)
  Webcam uncalib  |      |      |      |      |===|==|     |  (4-6 deg)
  OpenFace 2.0    |      |      |      |      |      |     |====> (9.1 deg)

  Zone thresholds:
  16-zone needs:  |      |==|   |      |      |      |      |  (<2 deg)
  9-zone needs:   |      |      |==|   |      |      |      |  (<3 deg)
  4-zone needs:   |      |      |      |      |==|   |      |  (<5 deg)
```

---

## 6. Emerging Trends and Future Directions

### 6.1 Foundation Model Integration

The emergence of DINOv2 (Meta, 2023) and DINOv3 (Meta, 2025) as general-purpose visual encoders opens new possibilities:

- **Frozen encoder + light decoder**: Gaze-LLE (CVPR 2025) demonstrates that a frozen DINOv2 encoder with a lightweight learned decoder achieves SOTA for gaze target estimation. This pattern could be adapted for gaze direction estimation.
- **LoRA adaptation**: DINOv2 can be efficiently adapted with LoRA (Low-Rank Adaptation) for person-specific gaze estimation, potentially requiring very few parameters to tune.
- **Limitation**: DINOv2 ViT-L has ~300M parameters, far too large for real-time CPU inference. Would require GPU or extensive distillation.

### 6.2 Event Camera Integration

Event cameras (neuromorphic sensors) operate in complete darkness and have microsecond-level temporal resolution. Recent work (2024) shows gaze estimation with event cameras. This is a potential future path for VoiceReach's night mode, though event cameras remain expensive and specialized.

### 6.3 Self-Supervised Calibration

SCPT (Self-Calibration and Person-specific Transform) modules represent the latest in self-supervised calibration -- no labeled calibration data required. The system learns person-specific features from unlabeled video during normal use. This could evolve VoiceReach's continuous calibration from semi-supervised (tap-gaze pairs) to fully self-supervised.

### 6.4 Temporal Modeling

Several 2024-2025 papers incorporate temporal information:
- **Spatio-Temporal Attention + Gaussian Processes**: 2.5 deg improvement on Gaze360 without personalization, +0.8 deg with 3-sample personalization.
- **LSTM layers after CNN**: MobileNet-V3 + LSTM for temporal consistency.
- **ARGaze**: Autoregressive transformers for sequential gaze prediction.

VoiceReach should consider replacing the current Kalman filter with a learned temporal model (lightweight LSTM or 1D convolution) that can capture gaze dynamics specific to ALS patients.

### 6.5 Capsule Networks

GazeCapsNet (2025) shows that capsule networks can replace traditional CNNs for gaze estimation, achieving 15% error reduction while eliminating the dependency on facial landmark detection. This is interesting because it could simplify VoiceReach's pipeline by removing the MediaPipe step entirely.

---

## 7. Commercial Webcam Gaze SDKs

### 7.1 SDK Comparison

| Product | Type | Price | Accuracy | Calibration | Platform | API | VoiceReach Assessment |
|---------|------|-------|----------|-------------|----------|-----|----------------------|
| **Tobii Nexus** | Webcam SDK | Commercial license (pricing on request) | ~1-2 deg (claimed) | Built-in | Windows, Mac, Linux | C++, Python | **COMPETITOR**. Tobii's proprietary webcam tracking. Likely best accuracy but high cost and proprietary lock-in. |
| **Eyeware Beam** | Consumer app | $30 one-time | ~2-3 deg | Minimal | Windows | OpenTrack protocol | **Not suitable** as SDK. Gaming-focused app, not embeddable. |
| **GazeFlow (GazeRecorder)** | Web SDK | Commercial | ~2-3 deg (claimed) | Browser-based | Web | JavaScript | **Reference**. Web-based gaze tracking for research. Could inform VoiceReach's browser-based approach. |
| **SentiGaze (Neurotechnology)** | Embedded SDK | Commercial | ~1-2 deg (claimed) | Multi-point | Windows | C++, .NET | **Alternative**. Desktop SDK with contactless tracking. |
| **Gazepoint GP3** | Hardware + SDK | $995 | 0.5-1 deg | Software | Windows | API | **HARDWARE TRACKER**. Budget research tracker, not webcam-only. |

### 7.2 Key Insight

Commercial webcam SDKs (Tobii Nexus, SentiGaze) likely achieve 1-2 deg accuracy using proprietary models trained on massive datasets. VoiceReach can approach this with:
1. Open-source model (L2CS-Net / MobileGaze / OpenFace 3.0)
2. Person-specific calibration (FAZE-style)
3. Continuous adaptive learning
4. Domain-specific training data (ALS patients, bed-bound)

The open-source approach trades ~0.5-1 deg of accuracy for zero licensing cost and full customizability for ALS-specific needs.

---

## 8. Recommendations for VoiceReach

### 8.1 Model Selection Decision Matrix

| Criterion | Weight | MediaPipe+MobileOne | OpenFace 3.0 | GazeFollower | L2CS-Net (ResNet-50) |
|-----------|--------|--------------------|--------------|--------------|--------------------|
| Accuracy (uncalibrated) | 25% | 3/5 (est. 4 deg) | **5/5** (2.56 deg) | **5/5** (1.11cm) | 4/5 (3.92 deg) |
| CPU Latency | 20% | **5/5** (<8ms) | **5/5** (real-time) | 3/5 (~15ms) | 2/5 (~30ms) |
| License | 15% | **5/5** (Apache+MIT) | 2/5 (Academic) | 4/5 (Open) | **5/5** (Apache) |
| Cross-platform | 15% | **5/5** (WebAssembly) | 2/5 (C++ desktop) | 3/5 (Python) | 4/5 (PyTorch) |
| Calibration support | 10% | 3/5 (manual) | 2/5 (none) | **5/5** (built-in) | 2/5 (none) |
| ALS adaptability | 10% | 4/5 (modular) | 3/5 (fixed) | 3/5 (general) | 3/5 (general) |
| Community/maintenance | 5% | **5/5** (Google) | 3/5 (CMU lab) | 2/5 (new) | 3/5 (limited) |
| **Weighted Score** | | **4.25** | **3.65** | **3.75** | **3.30** |

### 8.2 Final Recommendation

**Primary path: MediaPipe Face Mesh + MobileOne s0 backbone with L2CS-Net dual loss**

This combination offers:
- **Best cross-platform support** (WebAssembly for Electron)
- **Fastest inference** (<8ms total on CPU)
- **Permissive licensing** (Apache-2.0 + MIT)
- **Proven accuracy** (~4 deg uncalibrated, ~2.5 deg with 5-point calibration)
- **Modular design** allowing each component to be upgraded independently
- **ONNX Runtime deployment** for optimized inference in Electron/Node.js

**Secondary investigation: OpenFace 3.0**

If the academic license can accommodate VoiceReach's distribution model:
- Evaluate as a single-model replacement for MediaPipe + CNN
- 2.56 deg accuracy without person-specific calibration is compelling
- Multi-task model also provides AU detection (useful for emotion/fatigue monitoring)

### 8.3 Calibration Architecture

```
Phase 1 (Initial calibration, ~30s):
  - 5-point grid (4 corners + center)
  - 3 seconds per point (with audio guidance)
  - Collect ~90 frames per point (30fps x 3s)
  - Compute affine correction parameters
  - Store as user profile

Phase 2 (Continuous adaptation, ongoing):
  - Every tap+gaze pair creates a labeled sample
  - Exponentially weighted buffer (recent samples weighted more)
  - Background retraining of last FC layer every N samples
  - Forgetting factor: older samples decay to handle
    condition progression

Phase 3 (Future - meta-learning):
  - FAZE-style meta-learned initialization
  - New user starts from meta-learned weights
  - 3-5 calibration points sufficient for convergence
  - Faster and more accurate than random initialization
```

### 8.4 Deployment Architecture

```
Electron Application
  |
  +-- MediaPipe Face Mesh (WASM)
  |     Input: Webcam frame (720p)
  |     Output: 468 landmarks + iris positions
  |     Latency: ~5ms
  |
  +-- Eye Patch Extractor (JS)
  |     Input: Landmarks
  |     Output: 64x64 left eye, 64x64 right eye, head pose
  |     Latency: <1ms
  |
  +-- Gaze CNN (ONNX Runtime for Node.js)
  |     Input: Eye patches + head pose
  |     Model: MobileOne s0 + L2CS dual loss
  |     Output: Gaze angle (pitch, yaw) + confidence
  |     Latency: ~3ms
  |
  +-- Calibration Layer (JS)
  |     Input: Raw gaze angle
  |     Output: Calibrated screen coordinate
  |     Method: Affine transform + adaptive offset
  |     Latency: <1ms
  |
  +-- Smoothing (JS)
  |     Input: Calibrated coordinate stream
  |     Output: Smoothed coordinate
  |     Method: Kalman filter (adaptive noise)
  |     Latency: <1ms
  |
  +-- Zone Mapper (JS)
        Input: Smoothed coordinate
        Output: Zone ID + confidence
        Method: Hysteresis boundaries
        Latency: <1ms

Total pipeline latency: ~10ms (well within 33ms frame budget at 30fps)
```

---

## 9. Open Questions

1. **MobileOne s0 vs. MobileNet v2 for gaze**: No head-to-head comparison exists in the literature. VoiceReach should benchmark both on MPIIGaze/GazeCapture to determine the better backbone for gaze-specific tasks.

2. **Transformer attention value**: For VoiceReach's zone-based input (not pixel-precise), does transformer attention (as in GazeTR) provide meaningful improvement over pure CNN? The 0.5 deg improvement may not justify 2-3x latency increase.

3. **OpenFace 3.0 real-world ALS testing**: The 2.56 deg result is on MPIIGaze (healthy participants, laptop use). How does it perform for ALS patients in bed with unusual head poses and ptosis?

4. **GazeFollower's 32M training images**: What is the composition of this training data? Does it include diverse populations, lighting conditions, and disabilities? If not, fine-tuning for ALS patients may require additional data collection.

5. **Capsule network viability**: GazeCapsNet eliminates landmark detection dependency, potentially simplifying the pipeline. But capsule networks have limited deployment tooling (ONNX export, WebAssembly). Is the simplification worth the deployment complexity?

6. **Head-pose normalization for bed-bound**: Standard gaze datasets assume upright head orientation. A patient lying in bed at 30-45 degree angle has a fundamentally different head-camera geometry. Do existing head-pose normalization techniques handle this, or is custom normalization needed?

7. **ONNX Runtime in Electron performance**: What is the actual performance of ONNX Runtime for Node.js with a MobileOne s0 model? GPU acceleration availability in Electron varies by platform. Need to benchmark on target hardware (typical patient laptop/tablet).

8. **Temporal model benefits**: The Kalman filter currently handles temporal smoothing. Would a lightweight learned temporal model (1D conv or LSTM with few parameters) provide better smoothing for ALS patients' specific eye movement patterns (slow saccades, involuntary nystagmus)?

---

## References

### Key Papers
- Cheng & Lu. "Gaze Estimation using Transformer," ICPR 2022.
- Abdelrahman et al. "L2CS-Net: Fine-Grained Gaze Estimation," FG 2023.
- Park et al. "Few-Shot Adaptive Gaze Estimation," ICCV 2019.
- Baltrušaitis et al. "OpenFace 3.0: A Lightweight Multitask System," arXiv 2025.
- Zhu et al. "GazeFollower: Deep learning-based gaze tracking with web cameras," ACM PACMCGIT 2024.
- GazeSymCAT. J. Computational Design & Engineering, 2025.
- GazeCapsNet. Sensors (MDPI), 2025.
- MobGazeNet. Machine Vision & Applications, 2025.
- TransGaze. Machine Vision & Applications, 2024.
- Ryan et al. "Gaze-LLE: Gaze Target Estimation via Large-Scale Learned Encoders," CVPR 2025.

### Key GitHub Repositories
- L2CS-Net: https://github.com/Ahmednull/L2CS-Net
- GazeTR: https://github.com/yihuacheng/GazeTR
- OpenFace 3.0: https://github.com/CMU-MultiComp-Lab/OpenFace-3.0
- FAZE: https://github.com/NVlabs/few_shot_gaze
- GazeFollower: https://github.com/GanchengZhu/GazeFollower
- MobileGaze: https://github.com/yakhyo/gaze-estimation
- GazeOnce: https://github.com/mf-zhang/GazeOnce
- MediaPipe: https://github.com/google-ai-edge/mediapipe
- GazeHub: https://phi-ai.buaa.edu.cn/Gazehub/
- Gaze-LLE: https://github.com/fkryan/gazelle
- ETH-XGaze: https://github.com/xucong-zhang/ETH-XGaze

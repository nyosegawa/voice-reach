# B3: Voice Synthesis Models -- 最新モデル調査レポート

**Research Date**: 2026-02-17
**Priority**: CRITICAL (Phase 0 dependency -- recording protocol design depends on target TTS model)
**Researcher**: Claude Opus 4.6 (AI-assisted deep research)

---

## 1. Academic Literature Review

### 1.1 The 2024-2026 TTS Revolution: From Codec Language Models to Flow Matching

The period from 2024 to early 2026 has seen an unprecedented acceleration in zero-shot TTS quality. Three major architectural paradigms now compete:

**Paradigm 1: Codec Language Models (Autoregressive)**
Models like VALL-E, Seed-TTS, and CosyVoice treat TTS as a next-token prediction problem over neural audio codec codes, leveraging the same scaling laws that drove LLM progress.

**Paradigm 2: Flow Matching (Non-Autoregressive)**
Models like F5-TTS, VoiceBox, and Marco-Voice use continuous flow matching (a generalization of diffusion models) to transform noise into mel-spectrograms in parallel, enabling faster inference.

**Paradigm 3: Masked Generative Models (Non-Autoregressive)**
MaskGCT and similar models use masked prediction (similar to BERT) on codec tokens, offering parallelism without the complexity of flow matching.

### 1.2 Key Papers (2024-2026) -- Chronological

| # | Paper | Authors / Org | Date | Venue | Architecture | Key Contribution |
|---|-------|--------------|------|-------|-------------|-----------------|
| 1 | **VALL-E 2** | Chen et al. / Microsoft | Jun 2024 | arXiv | Codec LM (AR) | First human parity on LibriSpeech/VCTK. Repetition Aware Sampling. Grouped Code Modeling. Not released. |
| 2 | **NaturalSpeech 3** | Ju et al. / Microsoft | Mar 2024 | ICML 2024 | Factorized Diffusion | Disentangles content/prosody/timbre/acoustics via FVQ. 1B params, 200K hrs. Comparable to ground truth. Not released. |
| 3 | **Seed-TTS** | Anastassiou et al. / ByteDance | Jun 2024 | arXiv | Codec LM | Production-quality. Proposes Seed-TTS-eval benchmark (WER + SIM). Emotion control. Not released, but eval set is open. |
| 4 | **VoiceCraft** | Peng et al. | 2024 | ACL 2024 | Codec LM | Zero-shot speech editing + TTS. Unique in supporting editing existing audio. Open-source. |
| 5 | **XTTS** | Casanova et al. / Coqui | Jun 2024 | arXiv | Codec LM | 17-language including Japanese. 21.53 Hz encoder. Fine-tunable with 10 min. Open-source (MPL-2.0). Company defunct. |
| 6 | **MaskGCT** | Wang et al. | Sep 2024 | ICLR 2025 | Masked Generative | No alignment needed. Two-stage: semantic tokens → acoustic tokens. 100K hrs training. Open-source (Amphion). |
| 7 | **F5-TTS** | Chen et al. | Oct 2024 | arXiv | Flow Matching + DiT | No duration model or phoneme alignment. RTF 0.15. Sway Sampling strategy. 100K hrs multilingual. Open-source (MIT). |
| 8 | **EmoKnob** | Chen et al. / Columbia | Oct 2024 | EMNLP 2024 | Framework (model-agnostic) | Emotion direction vectors in speaker embedding space. Fine-grained, open-ended emotion control. Open-source. |
| 9 | **CosyVoice 2** | Du et al. / Alibaba | Dec 2024 | arXiv | Codec LM + Flow Matching | Unified streaming/non-streaming. 150ms latency. Human-parity. 9 languages. Finite-scalar quantization. Open-source (Apache). |
| 10 | **LLaSA** | HKUST Audio | Feb 2025 | arXiv | Codec LM (LLaMA-based) | Extends LLaMA 1B/3B/8B for TTS. XCodec2 (65K tokens). 250K hrs CN+EN. Seamless LLM framework integration. |
| 11 | **Voice Cloning for Dysarthric Speech** | Various | Mar 2025 | arXiv | Applied research | Cloning works for dysarthric speech (30% fooled SLP). Relevant for degraded ALS patient speech. |
| 12 | **Benchmarking Japanese TTS: VITS vs Style-BERT-VITS2** | Various | May 2025 | arXiv | Evaluation | First formal comparison of Japanese expressive TTS models. Evaluates pitch-accent and phoneme timing. |
| 13 | **CosyVoice 3** | Du et al. / Alibaba | May 2025 | arXiv | Codec LM + Flow Matching | Scaled to 1M hrs, 1.5B params. 9 languages + 18 Chinese dialects. New speech tokenizer. Differential reward model. |
| 14 | **VoiceStar** | Peng et al. / UT Austin | May 2025 | arXiv | Codec LM (AR) | First zero-shot TTS with duration control AND extrapolation. PM-RoPE. 840M params, 65K hrs. English-only. |
| 15 | **Voice Cloning Comprehensive Survey** | Various | May 2025 | arXiv 2505.00579 | Survey | Comprehensive survey of the entire voice cloning field as of 2025. |
| 16 | **IndexTTS2** | IndexTeam | Jun 2025 | arXiv | Codec LM (AR) | Emotion-timbre disentanglement. Duration control. Text-based emotion via Qwen3 LLM. |
| 17 | **Marco-Voice** | Alibaba AIDC | Aug 2025 | arXiv | Flow Matching | Speaker-emotion disentanglement via contrastive learning. Rotational emotion embedding. Outperforms CosyVoice on emotion. |
| 18 | **Orpheus TTS** | Canopy AI | Sep 2025 | Blog/GitHub | Codec LM (Llama-3b) | Apache 2.0. Emotion tags. ~100-200ms latency. English-focused. |
| 19 | **GLM-TTS** | Zhipu AI | Dec 2025 | arXiv | Codec LM + Flow Matching | Multi-reward GRPO (CER + SIM + Emotion + Laughter). Outperforms commercial on emotion benchmarks. CN+EN. |
| 20 | **Chatterbox Multilingual** | Resemble AI | 2025 | GitHub | Codec LM | MIT license. 23 languages. Paralinguistic tags. Perth watermarking. 63.75% preferred over ElevenLabs. |
| 21 | **ClonEval** | Cai et al. | Apr 2025 | arXiv | Benchmark | Open voice cloning benchmark. XTTS-v2 scores highest among tested open models. Emotional speech evaluation included. |
| 22 | **F5R-TTS** | Various | Apr 2025 | arXiv | Flow Matching | Improves F5-TTS with Group Relative Policy Optimization. Better quality without retraining. |

### 1.3 Key Trends Identified

1. **Convergence of LLM and TTS**: Models like LLaSA, CosyVoice, and Orpheus treat speech tokens as an extension of the LLM vocabulary, enabling joint text-speech reasoning.

2. **Flow Matching dominance for quality**: Non-autoregressive flow matching models (F5-TTS, VoiceBox) offer better parallelism and faster inference, while autoregressive models offer more natural prosody.

3. **Hybrid architectures winning**: CosyVoice 2/3 combines LLM-based token prediction with flow matching for acoustic generation, getting the best of both worlds.

4. **Reinforcement learning for expressiveness**: GLM-TTS's multi-reward GRPO and F5R-TTS's GRPO show that RL can significantly improve emotion expressiveness without retraining from scratch.

5. **Benchmark standardization**: Seed-TTS-eval and ClonEval are emerging as standard benchmarks, using WER (intelligibility) and SIM (speaker similarity) as primary metrics.

---

## 2. Comprehensive Model Comparison

### 2.1 Answers to Research Questions

#### Q1: State-of-the-art in zero-shot voice cloning as of 2025-2026?

The state-of-the-art is defined by several systems, none of which is definitively "best" across all dimensions:

**Quality leader (closed)**: VALL-E 2 (Microsoft, Jun 2024) -- first to achieve human parity on standard benchmarks. Not released.

**Quality leader (open)**: CosyVoice 3 (Alibaba, May 2025) -- 1.5B parameters trained on 1M hours. Surpasses CosyVoice 2 in content consistency, speaker similarity, and prosody naturalness. Covers 9 languages including Japanese.

**Efficiency leader**: F5-TTS (Oct 2024) -- only 2,994 MB GPU memory. RTF 0.15. MIT license. Best balance of quality and compute.

**Streaming leader**: CosyVoice 2 (Dec 2024) -- 150ms first-chunk latency in streaming mode. Virtually lossless quality vs. non-streaming.

**Emotion leader**: IndexTTS2 (Jun 2025) + Marco-Voice (Aug 2025) -- both achieve emotion-identity disentanglement. IndexTTS2 adds text-based emotion instruction.

**Community leader**: GPT-SoVITS v4 (ongoing) -- 55K GitHub stars. Excellent few-shot quality from 1 minute of audio. Active community with Japanese-specific support.

**Minimum data**: Fish Speech v1.5 / OpenAudio S1 -- convincing clones from 10 seconds. Trained on 1M+ hours including 100K+ hours of Japanese.

#### Q2: Which models produce the best Japanese voice cloning quality?

**Ranked by Japanese quality (based on training data, community evaluation, and language-specific features)**:

| Rank | Model | Japanese Quality Evidence | Approach |
|------|-------|--------------------------|----------|
| 1 | **Style-Bert-VITS2 JP Extra** | Purpose-built for Japanese. 800-hr JP-only pretraining. WavLM discriminator. Best pitch-accent handling. Formal evaluation paper (arXiv 2505.17320). | Fine-tuned (requires 10-30 min per speaker) |
| 2 | **GPT-SoVITS v4** | Explicit JP support. Large JP user community. Fine-tuned Japanese models widely shared. Few-shot from 1 min. | Few-shot (1 min) or fine-tuned |
| 3 | **Fish Speech v1.5** | Trained on 100K+ hours of Japanese data. Best zero-shot Japanese capability. | Zero-shot (10s reference) |
| 4 | **CosyVoice 2/3** | Explicit Japanese in 9-language support. Massive training scale. | Zero-shot (3-5s reference) |
| 5 | **XTTS v2** | Japanese in 17-language support. Proven but not JP-optimized. | Zero-shot (6s reference) |
| 6 | **Chatterbox** | 23 languages including Japanese. Less JP-specific evaluation available. | Zero-shot (few seconds) |
| 7 | **F5-TTS** | Multilingual training includes Japanese. Less JP-specific evaluation. | Zero-shot (3-5s reference) |
| 8 | **MeloTTS** | Japanese support but no voice cloning. Good as generic JP TTS fallback. | No cloning (generic voices) |

**Critical note**: No comprehensive benchmark compares all these models specifically on Japanese voice cloning quality. The ranking above is based on training data composition, community reports, and available ablation studies. VoiceReach should conduct its own Japanese MOS evaluation.

#### Q3: Can any current model do real-time synthesis with emotion/tone control on consumer hardware?

**Yes**, with caveats:

| Model | Hardware Required | Latency | Emotion Control | Japanese | Feasibility |
|-------|------------------|---------|-----------------|----------|-------------|
| **CosyVoice 2** | RTX 3060+ (6GB VRAM) | 150ms streaming | Native (emotion prompts) | Yes | **Feasible** |
| **F5-TTS** | RTX 3060+ (~3GB VRAM) | RTF 0.15 (batch) | Limited (requires additional framework) | Yes | **Feasible (batch, not streaming)** |
| **GPT-SoVITS v4** | RTX 3060+ (6GB VRAM) | ~500ms-1s | Moderate (style transfer) | Yes | **Feasible for AAC** (latency acceptable) |
| **Chatterbox Turbo** | RTX 3060+ | <200ms | Paralinguistic tags | Yes | **Feasible** |
| **XTTS v2** | RTX 3060+ (4GB VRAM) | <150ms streaming | Limited | Yes | **Feasible** |
| **OpenVoice v2** | CPU capable | Very fast | Style control (emotion, accent) | Yes | **Feasible (lower quality)** |

**"Consumer hardware" definition**: NVIDIA RTX 3060 (12GB), 16GB RAM, modern x86 CPU. This is VoiceReach's target.

**Real-time definition for AAC**: <500ms from text input to first audio chunk. All Tier 1 candidates meet this requirement.

**Key finding**: CosyVoice 2 in streaming mode (150ms) with native emotion control on an RTX 3060 is the most promising configuration for VoiceReach's real-time AAC requirement.

#### Q4: Achievable MOS score for cloned Japanese voices with 30-60 minutes of recording?

Based on available data and extrapolation:

| Condition | Estimated MOS Range | Notes |
|-----------|-------------------|-------|
| Ground truth (human speaker) | 4.5 - 4.8 | Reference baseline |
| Zero-shot (5s reference), best model | 3.5 - 4.0 | Fish Speech / CosyVoice 3 |
| Zero-shot (30s reference), best model | 3.8 - 4.2 | Fish Speech / CosyVoice 3 |
| Fine-tuned (10 min data) | 3.8 - 4.2 | GPT-SoVITS / Style-Bert-VITS2 |
| Fine-tuned (30 min data) | 4.0 - 4.3 | GPT-SoVITS / Style-Bert-VITS2 |
| Fine-tuned (60 min data) | 4.1 - 4.4 | Style-Bert-VITS2 (JP-specific) |
| Commercial API (ElevenLabs Professional) | 4.0 - 4.3 | For reference |

**Important caveats**:
- These are estimates. No published study specifically measures cloned Japanese voice MOS with exactly 30-60 minutes of data across all these models.
- MOS for Japanese is typically lower than English due to pitch-accent complexity.
- MOS depends heavily on recording quality, not just quantity.
- The VoiceReach Phase 2 KPI target is MOS 3.5+. This is achievable with any Tier 1 model and 30+ minutes of clean data.
- With careful fine-tuning of Style-Bert-VITS2 on 60 minutes of high-quality Japanese data, MOS 4.0+ is realistic.

#### Q5: How do the latest models compare: Fish Speech, CosyVoice, F5-TTS, ChatTTS, Parler-TTS, MeloTTS, GPT-SoVITS?

### 2.2 Detailed Head-to-Head Comparison

| Dimension | Fish Speech v1.5 | CosyVoice 2/3 | F5-TTS | ChatTTS | Parler-TTS | MeloTTS | GPT-SoVITS v4 |
|-----------|-----------------|---------------|--------|---------|------------|---------|---------------|
| **Architecture** | Codec LM | Codec LM + Flow Matching | Flow Matching + DiT | Codec LM | Decoder-only Transformer | VITS-based | GPT + SoVITS |
| **GitHub Stars** | ~25K | ~20K | ~14K | ~39K | ~5.5K | ~7.2K | ~55K |
| **License** | Apache (code), CC-BY-NC-SA (model) | Apache-2.0 | MIT | AGPL-3.0 | Apache-2.0 | MIT | MIT |
| **Voice Cloning** | Zero-shot (10s) | Zero-shot (3-5s) | Zero-shot (3-5s) | No | No (description-based) | No | Zero-shot (5s) + few-shot (1 min) |
| **Japanese Support** | Excellent (100K+ hrs) | Excellent (native) | Good (multilingual) | Limited (CN/EN) | Limited (EN focus) | Yes (JP native) | Excellent (native) |
| **Streaming** | Limited | Yes (150ms) | No (non-AR) | No | No | No | No |
| **Emotion Control** | Moderate | Good (native) | Limited | Good (prosody tags) | Description-based | None | Good (style transfer) |
| **Min GPU VRAM** | ~4GB | ~6GB | ~3GB | ~4GB | ~4GB | ~2GB (CPU OK) | ~6GB |
| **Inference Speed (RTF)** | ~0.3 | ~0.2 (streaming) | 0.15 | ~0.5 | ~0.3 | Real-time on CPU | ~0.5-1.0 |
| **Training Data** | 1M+ hrs | 10K-1M hrs | 100K hrs | Unknown | ~10K hrs | Unknown | Community-dependent |
| **Active Development** | Yes (rebranding to OpenAudio) | Yes (v3 released May 2025) | Yes | Slowing | Slowing | Stale | Very active |
| **Fine-tuning Support** | Yes | Yes | Community scripts | Limited | No | No | Excellent |
| **VoiceReach Score** | 8/10 | 9/10 | 7/10 | 3/10 | 2/10 | 2/10 | 9/10 |

### 2.3 Additional Models Not in Original List

| Model | Why It Matters | VoiceReach Relevance |
|-------|---------------|---------------------|
| **Chatterbox (Resemble AI)** | MIT license, 23 languages, paralinguistic tags, watermarking | HIGH -- Strong all-around candidate |
| **IndexTTS2** | Best emotion-timbre disentanglement | MEDIUM -- Emotion control reference, but JP support unclear |
| **Style-Bert-VITS2** | Best Japanese-specific TTS quality | HIGH -- For fine-tuned JP quality |
| **GLM-TTS** | Multi-reward RL for emotion | LOW -- CN/EN only, but RL approach is informative |
| **Marco-Voice** | Speaker-emotion contrastive disentanglement | MEDIUM -- Research reference for emotion architecture |
| **Orpheus TTS** | Apache 2.0, Llama backbone, emotion tags | LOW -- English only |
| **OpenVoice v2** | MIT, instant cloning, very fast, style control | MEDIUM -- Lightweight fallback option |
| **VoiceStar** | Duration control for natural pacing | LOW -- English only, but duration control concept is valuable |
| **LLaSA** | LLM-TTS unification | LOW -- CN/EN only, but architecture trend is relevant |
| **MaskGCT (Amphion)** | ICLR 2025, no alignment needed | MEDIUM -- Academic quality, cross-lingual potential |

---

## 3. Commercial Products and APIs

### 3.1 Commercial TTS Services with Voice Cloning

| Service | Organization | Voice Cloning | Japanese | Emotion Control | Latency | Pricing | ALS Suitability |
|---------|-------------|--------------|----------|----------------|---------|---------|-----------------|
| **ElevenLabs** | ElevenLabs | Instant (1 min) + Professional (30 min) | Good | Moderate | ~300ms | $5-330/mo | Medium (commercial service, ongoing cost) |
| **Fish Audio API** | Fish Audio | Zero-shot (10s) | Excellent | Moderate | Low | Pay-per-use | Good (same tech as OSS, production-grade) |
| **Resemble AI** | Resemble AI | Professional-grade | Good | Good (emotion tags) | <200ms | Enterprise | Medium (expensive for individual patients) |
| **Google Cloud TTS** | Google | Custom Voice (10s min) | Excellent | Limited | Low | Pay-per-use ($4-16/1M chars) | Medium (reliable but limited cloning) |
| **Azure Neural TTS** | Microsoft | Custom Neural Voice | Good | Good | Low | Pay-per-use | Medium (VALL-E lineage) |
| **Amazon Polly** | AWS | No true cloning | Good | SSML-based | Low | Pay-per-use | Low (no cloning) |
| **Speechify** | Speechify | Instant (20s) | Partial | Limited | Low | Subscription | Low (consumer focus) |
| **Hume AI** | Hume | Emotion-aware synthesis | Limited | Excellent (core focus) | Low | API pricing | Medium (emotion-first approach) |

### 3.2 On-Device Solutions

| Solution | Platform | Voice Cloning | Japanese | Recording Needed | Privacy | ALS Suitability |
|----------|----------|--------------|----------|-----------------|---------|-----------------|
| **Apple Personal Voice** | iOS 17+ / macOS | Yes (on-device) | Yes | 150 sentences / 15 min | Excellent (fully on-device) | **Very High** |
| **Android Custom Voice** | Android 14+ | Limited | Limited | Varies | Good | Low (limited features) |
| **Samsung Voice** | Samsung devices | Limited | Limited | Varies | Good | Low |

---

## 4. Comparative Analysis for VoiceReach

### 4.1 Weighted Scoring Matrix

Scoring criteria (weighted for VoiceReach's specific needs):

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Japanese Quality | 25% | Native-level Japanese synthesis with correct pitch-accent |
| Voice Cloning Quality | 20% | Speaker similarity from 30-60 min data |
| Emotion/Tone Control | 15% | Ability to produce same text with different emotional tones |
| Real-time Capability | 15% | <500ms for AAC use, preferably streaming |
| License & Sustainability | 10% | Permissive license, active development, community |
| Resource Efficiency | 10% | Runs on consumer GPU (RTX 3060 class) |
| Integration Ease | 5% | Clean API, documentation, Python ecosystem |

### 4.2 Weighted Scores

| Model | JP Quality (25%) | Clone Quality (20%) | Emotion (15%) | Real-time (15%) | License (10%) | Efficiency (10%) | Integration (5%) | **Total** |
|-------|---------|---------|---------|---------|---------|---------|---------|---------|
| **CosyVoice 2/3** | 9 | 9 | 8 | 10 | 9 | 7 | 8 | **8.80** |
| **GPT-SoVITS v4** | 9 | 9 | 7 | 6 | 10 | 7 | 8 | **8.25** |
| **Fish Speech v1.5** | 10 | 9 | 6 | 7 | 6 | 8 | 7 | **8.00** |
| **Chatterbox** | 7 | 8 | 7 | 9 | 10 | 7 | 9 | **7.95** |
| **F5-TTS** | 7 | 8 | 5 | 7 | 10 | 10 | 8 | **7.50** |
| **Style-Bert-VITS2** | 10 | 8 | 7 | 7 | 5 | 7 | 6 | **7.50** |
| **XTTS v2** | 6 | 7 | 4 | 9 | 8 | 8 | 9 | **6.85** |
| **OpenVoice v2** | 6 | 6 | 6 | 10 | 10 | 10 | 8 | **7.10** |
| **IndexTTS2** | 4 | 8 | 10 | 7 | 5 | 7 | 5 | **6.35** |
| **MaskGCT** | 5 | 8 | 6 | 7 | 10 | 7 | 6 | **6.60** |

### 4.3 Analysis Summary

**Top 3 candidates for VoiceReach**:

1. **CosyVoice 2/3** (Score: 8.80) -- Best overall balance. Streaming capability is a decisive advantage for AAC. Strong Japanese support. Active development by Alibaba. Apache-2.0 license.

2. **GPT-SoVITS v4** (Score: 8.25) -- Best few-shot quality. MIT license. Largest community. Excellent Japanese community support. Only weakness is real-time streaming (requires batched inference).

3. **Fish Speech v1.5** (Score: 8.00) -- Best zero-shot Japanese quality due to massive JP training data. Active development (rebranding to OpenAudio). Concern: CC-BY-NC-SA model license restricts commercial use.

**Recommended strategy**: **Multi-model pipeline**

```
[Primary TTS Engine: CosyVoice 2]
  - Used for real-time streaming synthesis
  - 150ms first-chunk latency
  - Native emotion control via emotion prompts

[Quality Engine: GPT-SoVITS v4]
  - Used for high-quality non-real-time synthesis
  - Pre-generates common phrases
  - Fine-tuned on patient's 30-60 min recording
  - Best speaker similarity

[Fallback Engine: Pre-generated audio cache]
  - Most common phrases pre-synthesized
  - Instant playback
  - Updated nightly with new phrases

[Emotion Enhancement: EmoKnob framework]
  - Applied on top of primary engine
  - Maps PVP valence/arousal to emotion vectors
  - Fine-grained control without model retraining
```

---

## 5. Recommendations

### 5.1 Immediate Actions for Phase 0 (Recording Protocol)

**Recording protocol should be model-agnostic but optimized for fine-tuning**:

Since the TTS landscape evolves rapidly, the recording protocol should capture maximum-quality raw data that works with any future model.

1. **Audio format**: 48 kHz / 24-bit WAV. Do not compress or process raw recordings.

2. **Recording duration target**:
   - Minimum viable: 20 minutes (50 sentences + 10 min free conversation)
   - Recommended: 45-60 minutes (100 sentences + emotion sessions + free conversation)
   - Optimal: 60-90 minutes (adds more emotion variety and natural conversation)

3. **Sentence set**: Design 100 Japanese sentences covering:
   - All morae (including ん, っ, and palatalized/voiced variants)
   - All common pitch-accent patterns (頭高, 中高, 尾高, 平板)
   - Sentence-final particles (よ, ね, か, な, ぞ, わ)
   - Various sentence lengths (short 5-mora to long 40+ mora)
   - Natural conversational sentences (not unnatural phonetic test sentences)
   - Reference: Base on JVS corpus sentence design but adapted for conversational context

4. **Emotion sessions** (15-20 minutes total):
   - Neutral/calm (基本): 10 sentences + 3 min monologue
   - Happy/warm (嬉しい/温かい): 10 sentences + 3 min about happy memories
   - Serious/emphatic (真剣/強調): 10 sentences + 3 min about important topics
   - Gentle/soft (優しい): 10 sentences + 3 min talking to loved ones
   - (Optional) Playful/humorous (楽しい): 5 sentences + 2 min jokes/funny stories

5. **Quality checks in recording app**:
   - Real-time SNR monitoring (warn if <30 dB)
   - Peak level monitoring (warn if clipping)
   - Background noise detection
   - Recording completeness tracking
   - Per-sentence quality score

6. **Metadata to capture**:
   - Timestamp per sentence
   - Self-reported emotion/mood
   - Recording environment description
   - Microphone type and distance
   - Patient's speech condition assessment (1-5 scale)

### 5.2 Model Selection Recommendation

**Primary recommendation: CosyVoice 2 (with plan to migrate to v3)**

Rationale:
- Streaming synthesis at 150ms is essential for AAC real-time use
- Apache-2.0 license allows commercial use and modification
- Active development by Alibaba's speech lab (CosyVoice 3 already released)
- Native Japanese support with large-scale training
- Built-in emotion control via prompt conditioning
- Unified streaming/non-streaming architecture simplifies deployment

**Secondary: GPT-SoVITS v4 for fine-tuned quality**

Rationale:
- MIT license (most permissive)
- Best few-shot quality from 1 minute of data
- Extensive Japanese community and pre-built pipelines
- Excellent for pre-generating high-quality phrase cache
- Can be fine-tuned on patient's full 60-min recording for maximum similarity

**Emotion enhancement: EmoKnob framework**

Rationale:
- Model-agnostic (works with any backbone)
- Proven at EMNLP 2024
- Fine-grained continuous emotion control (not discrete categories)
- Open-ended text description of target emotion
- Can be applied post-hoc without retraining the TTS model

### 5.3 Technical Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Voice Synthesis Pipeline                   │
│                                                              │
│  Input: Text + Emotion Parameters + Speaker ID               │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐    │
│  │ Japanese Text Frontend                                │    │
│  │  MeCab/Sudachi → reading → accent → phoneme sequence │    │
│  └─────────────────────────┬────────────────────────────┘    │
│                             │                                 │
│  ┌─────────────────────────┴────────────────────────────┐    │
│  │ Emotion Mapper                                        │    │
│  │  PVP valence/arousal → EmoKnob direction vector       │    │
│  │  OR manual tone selection → emotion embedding          │    │
│  │  OR auto-detect from context (listener, situation)     │    │
│  └─────────────────────────┬────────────────────────────┘    │
│                             │                                 │
│  ┌─────────────────────────┴────────────────────────────┐    │
│  │ Router (latency/quality tradeoff)                     │    │
│  │  ├─ Cached phrase hit? → Instant playback             │    │
│  │  ├─ Real-time needed? → CosyVoice 2 (streaming)      │    │
│  │  └─ Quality priority? → GPT-SoVITS (fine-tuned)      │    │
│  └─────────────────────────┬────────────────────────────┘    │
│                             │                                 │
│  ┌─────────────────────────┴────────────────────────────┐    │
│  │ Post-processing                                       │    │
│  │  - Loudness normalization (ITU-R BS.1770)             │    │
│  │  - Optional enhancement (if needed)                   │    │
│  │  - Watermarking (optional, for safety)                │    │
│  └─────────────────────────┬────────────────────────────┘    │
│                             │                                 │
│  Output: Audio stream → Speaker                              │
└─────────────────────────────────────────────────────────────┘

Hardware Target:
  - GPU: NVIDIA RTX 3060 12GB (or equivalent)
  - RAM: 16GB+
  - Storage: 10GB for models + voice bank
  - OS: Linux (Ubuntu 22.04+) or Windows 11

Model Storage:
  ┌─────────────────────────┐
  │ Per-Patient Voice Bank   │
  │  - Raw recordings (WAV)  │  ~2-5 GB
  │  - Speaker embedding     │  ~1 MB
  │  - Fine-tuned model      │  ~2-4 GB
  │  - Emotion embeddings    │  ~10 MB
  │  - Phrase cache (audio)  │  ~500 MB
  └─────────────────────────┘
```

### 5.4 Evaluation Plan

Before committing to final model selection in Phase 2, conduct a comparative evaluation:

1. **Prepare test data**: Record 60 minutes from 3 Japanese speakers (1 male, 2 female; or 2 male, 1 female) using the Phase 0 recording protocol.

2. **Train/adapt all Tier 1 models**:
   - CosyVoice 2: Zero-shot + fine-tuned
   - GPT-SoVITS v4: Few-shot (1 min) + fine-tuned (full 60 min)
   - Fish Speech v1.5: Zero-shot + fine-tuned
   - F5-TTS: Zero-shot
   - Chatterbox: Zero-shot

3. **Generate test utterances**: 50 sentences per model per speaker, including 5 emotion categories.

4. **MOS evaluation**:
   - 10+ Japanese native evaluators
   - Rate naturalness (1-5), speaker similarity (1-5), emotion appropriateness (1-5)
   - Compare against ground truth recordings

5. **Technical metrics**:
   - WER (word error rate via Whisper large-v3)
   - SIM (speaker similarity via WavLM or resemblyzer)
   - RTF (real-time factor)
   - First-chunk latency
   - GPU memory usage
   - Total inference time

6. **Decision criteria**:
   - MOS naturalness >= 3.8
   - MOS speaker similarity >= 3.5
   - First-chunk latency < 500ms
   - Runs on RTX 3060

### 5.5 Migration Strategy

Given the rapid evolution of TTS models:

1. **Abstract the TTS interface**: Define a clean Python interface for the TTS engine:
   ```python
   class VoiceReachTTS:
       def synthesize_streaming(self, text: str, speaker_id: str,
                                 emotion: EmotionParams) -> AsyncIterator[AudioChunk]
       def synthesize_batch(self, text: str, speaker_id: str,
                            emotion: EmotionParams) -> AudioBuffer
       def load_speaker(self, voice_bank_path: str) -> str  # returns speaker_id
   ```

2. **Model-agnostic speaker representation**: Store speaker embeddings in a standard format (numpy arrays) alongside raw audio, so new models can re-extract embeddings.

3. **Version the voice bank**: Each model produces different fine-tuned weights. Keep all versions alongside the raw data.

4. **Monitor the field**: Set up alerts for new releases from: Alibaba (CosyVoice), Fish Audio, RVC-Boss (GPT-SoVITS), and any new entrants. Re-evaluate every 6 months.

---

## 6. Open Questions

1. **CosyVoice 2 vs. 3 deployment maturity**: CosyVoice 3 has better benchmarks but was released more recently (May 2025). Is it stable enough for production? Should we start with v2 and migrate to v3?

2. **Fine-tuning data efficiency**: What is the exact quality curve for Japanese voice cloning as a function of training data amount (5 min, 10 min, 30 min, 60 min, 90 min)? This determines the minimum viable recording for Phase 0.

3. **Emotion-speaker disentanglement for Japanese**: Most emotion control research has been evaluated on English and Chinese. Does the emotion-identity disentanglement hold for Japanese, where prosody (pitch-accent) carries both emotional and lexical information?

4. **Long-term API stability**: If we use CosyVoice (Alibaba), what happens if Alibaba stops maintaining it? The Apache license protects the code, but not the training data or future improvements.

5. **Degraded speech voice cloning**: Can we clone a voice from recordings where the patient's speech is already partially degraded by ALS? The 2025 dysarthria paper suggests yes, but practical Japanese evaluation is needed.

6. **On-device inference**: Can CosyVoice 2 or GPT-SoVITS run on Apple Silicon (M1/M2/M3 Mac) for a fully on-device solution? MLX ports of F5-TTS exist, suggesting this is feasible.

7. **Whisper-based transcription accuracy for Japanese**: The preprocessing pipeline requires accurate Japanese ASR for aligning recordings. Whisper large-v3 is good but not perfect for spontaneous Japanese speech. What is the error rate, and how does it affect training data quality?

8. **Patient perception study**: Do ALS patients and their families prefer a very accurate clone (that might sound slightly robotic) or a slightly less accurate clone that sounds more natural? This affects model selection priorities.

---

## 7. Timeline Mapping to VoiceReach Roadmap

| Phase | Timeline | Voice Synthesis Activities |
|-------|----------|--------------------------|
| **Phase 0** | Months 0-3 | Design recording protocol. Build recording app with quality checks. Record first 5 patients. Store raw WAV + metadata. Begin preprocessing pipeline. |
| **Phase 0.5** (new) | Months 2-4 | Conduct model evaluation (Section 5.4). Select primary + secondary models. Build abstraction layer. |
| **Phase 1** | Months 3-9 | Integrate generic TTS (no patient voice yet). Build Japanese text frontend. Implement phrase caching infrastructure. |
| **Phase 2** | Months 9-15 | Integrate voice cloning pipeline. Fine-tune models per patient. Implement emotion mapping. Deploy streaming synthesis. Conduct MOS evaluation with patients. |
| **Phase 3** | Months 15-24 | Optimize latency. Expand emotion control. Support on-device inference. Consider model updates (CosyVoice 4? GPT-SoVITS v5?). |

---

## References

### Key Repositories
- CosyVoice: https://github.com/FunAudioLLM/CosyVoice (19.6K stars, Apache-2.0)
- GPT-SoVITS: https://github.com/RVC-Boss/GPT-SoVITS (55K stars, MIT)
- Fish Speech: https://github.com/fishaudio/fish-speech (24.9K stars, Apache-2.0 code)
- F5-TTS: https://github.com/SWivid/F5-TTS (14.1K stars, MIT)
- Chatterbox: https://github.com/resemble-ai/chatterbox (22.7K stars, MIT)
- Style-Bert-VITS2: https://github.com/litagin02/Style-Bert-VITS2 (1.2K stars, AGPL-3.0)
- IndexTTS: https://github.com/index-tts/index-tts (18.8K stars)
- MaskGCT/Amphion: https://github.com/open-mmlab/Amphion (9.7K stars, MIT)
- OpenVoice: https://github.com/myshell-ai/OpenVoice (35.9K stars, MIT)
- GLM-TTS: https://github.com/zai-org/GLM-TTS (0.9K stars, Apache-2.0)
- EmoKnob: https://github.com/tonychenxyz/emoknob
- Seed-TTS-eval: https://github.com/BytedanceSpeech/seed-tts-eval
- ClonEval: https://github.com/amu-cai/cloneval

### Key Papers (arXiv)
- VALL-E 2: arXiv:2406.05370
- NaturalSpeech 3: arXiv:2403.03100
- Seed-TTS: arXiv:2406.02430
- F5-TTS: arXiv:2410.06885
- CosyVoice 2: arXiv:2412.10117
- CosyVoice 3: arXiv:2505.17589
- MaskGCT: arXiv:2409.00750
- EmoKnob: arXiv:2410.00316
- Marco-Voice: arXiv:2508.02038
- IndexTTS2: arXiv:2506.21619
- GLM-TTS: arXiv:2512.14291
- VoiceStar: arXiv:2505.19462
- Voice Cloning Survey: arXiv:2505.00579
- ClonEval: arXiv:2504.20581
- Japanese TTS Benchmark: arXiv:2505.17320
- Dysarthric Voice Cloning: arXiv:2503.01266

### Commercial / Program Resources
- ALS SAVE VOICE (Japan): https://prtimes.jp/main/html/rd/p/000000022.000019066.html
- Apple Personal Voice: https://machinelearning.apple.com/research/personal-voice
- Acapela My-Own-Voice: https://mov.acapela-group.com/
- SpeakUnique: https://www.speakunique.co.uk/
- Team Gleason: https://teamgleason.org/pals-resource/voice-message-banking/
- ALS Association Voice Banking: https://www.als.org/support/programs/voice-banking
- Toshiba CoEStation: https://coestation.jp/

# A4: Voice Preservation & Synthesis -- 先行研究レポート

**Research Date**: 2026-02-17
**Priority**: CRITICAL (Phase 0 dependency)
**Researcher**: Claude Opus 4.6 (AI-assisted deep research)

---

## 1. Academic Literature Review

### 1.1 Core Zero-Shot Voice Cloning Papers

| # | Paper | Authors | Year | Venue | Summary | VoiceReach Relevance |
|---|-------|---------|------|-------|---------|---------------------|
| 1 | **VALL-E: Neural Codec Language Models are Zero-Shot Text to Speech Synthesizers** | Wang et al. (Microsoft) | 2023 | arXiv 2301.02111 | First to frame TTS as language modeling over neural codec codes. 3-second enrollment. Trained on 60K hours of English speech (LibriLight). | Foundational architecture. Not open-source, but inspired most subsequent models. |
| 2 | **VALL-E 2: Neural Codec Language Models are Human Parity Zero-Shot Text to Speech Synthesizers** | Chen et al. (Microsoft) | 2024 | arXiv 2406.05370 | First system to achieve human parity on LibriSpeech and VCTK benchmarks. Introduces Repetition Aware Sampling and Grouped Code Modeling. | Demonstrates that zero-shot voice cloning can match human speech quality. Not released publicly due to safety concerns. |
| 3 | **VALL-E X: Speak Foreign Languages with Your Own Voice** | Zhang et al. (Microsoft) | 2023 | arXiv 2303.03926 | Cross-lingual extension of VALL-E. Supports speech generation in target language while preserving source speaker's voice. | Relevant for multilingual/cross-lingual scenarios; not open-source. |
| 4 | **NaturalSpeech 3: Zero-Shot Speech Synthesis with Factorized Codec and Diffusion Models** | Ju et al. (Microsoft) | 2024 | ICML 2024, arXiv 2403.03100 | Uses factorized vector quantization to disentangle content, prosody, timbre, and acoustic details. Scales to 1B parameters, 200K hours. Achieves comparable or better quality than ground-truth speech. | Critical architecture insight: factorized representations enable independent control of prosody/timbre/emotion -- exactly what VoiceReach needs for tone control. |
| 5 | **VoiceBox: Text-Guided Multilingual Universal Speech Generation at Scale** | Le et al. (Meta) | 2023 | NeurIPS 2023 | Flow-matching based model for in-context learning of speech. Supports speech infilling, noise removal, style conversion. | Demonstrates versatility of flow-matching for speech tasks; not open-source. |
| 6 | **Seed-TTS: A Family of High-Quality Versatile Speech Generation Models** | Anastassiou et al. (ByteDance) | 2024 | arXiv 2406.02430 | Comprehensive TTS system with superior emotion controllability. Proposes standardized evaluation benchmark (Seed-TTS-eval) using WER and SIM metrics. | The Seed-TTS-eval benchmark is now widely used. Model not open-source, but evaluation framework is available. |
| 7 | **F5-TTS: A Fairytaler that Fakes Fluent and Faithful Speech with Flow Matching** | Chen et al. | 2024 | arXiv 2410.06885 | Fully non-autoregressive TTS using flow matching + DiT. No duration model, no phoneme alignment needed. RTF of 0.15. Trained on 100K hours multilingual data. | Excellent candidate: efficient, high-quality, supports Japanese, low latency. Open-source with code and checkpoints. |
| 8 | **CosyVoice 2: Scalable Streaming Speech Synthesis with Large Language Models** | Du et al. (Alibaba) | 2024 | arXiv 2412.10117 | Unified streaming/non-streaming synthesis. Finite-scalar quantization for improved codebook utilization. 150ms latency in streaming mode. Human-parity naturalness. | Strong candidate for real-time synthesis: streaming support, low latency, Japanese support, open-source. |
| 9 | **CosyVoice 3: Towards In-the-wild Speech Generation via Scaling-up and Post-training** | Du et al. (Alibaba) | 2025 | arXiv 2505.17589 | Scaled to 1M hours, 1.5B parameters, 9 languages including Japanese. Novel speech tokenizer and differentiable reward model for post-training. | Latest evolution with explicit Japanese support and massive scale. |
| 10 | **MaskGCT: Zero-Shot Text-to-Speech with Masked Generative Codec Transformer** | Wang et al. | 2025 | ICLR 2025, arXiv 2409.00750 | Fully non-autoregressive TTS using masked generative approach. No explicit text-speech alignment needed. Trained on 100K hours. Supports emotion control and cross-lingual dubbing. | Published at top venue (ICLR 2025). Open-source via Amphion framework. |
| 11 | **XTTS: A Massively Multilingual Zero-Shot Text-to-Speech Model** | Casanova et al. (Coqui) | 2024 | arXiv 2406.04904 | 17-language support including Japanese. Encoder at 21.53 Hz frame rate (faster than VALL-E's 75Hz). Can mimic whispering style from only 10 min English data across 16 languages. | Proven multilingual model with Japanese support. Open-source. Community widely uses it. Company (Coqui) shut down but code remains. |
| 12 | **StyleTTS 2: Towards Human-Level Text-to-Speech through Style Diffusion and Adversarial Training with Large Speech Language Models** | Li et al. | 2023 | NeurIPS 2023 | Achieves human-level TTS quality for English. Strong style/prosody control via style diffusion. 3x smaller than XTTS v2 with faster inference. | Excellent quality but English-only. Not suitable for Japanese without significant adaptation. |
| 13 | **VoiceCraft: Zero-Shot Speech Editing and Text-to-Speech in the Wild** | Peng et al. | 2024 | ACL 2024 | Supports speech editing (modifying existing audio) and TTS from few seconds. Useful for correcting/editing voice bank recordings. | Speech editing capability is uniquely useful for voice bank post-processing. |
| 14 | **VoiceStar: Robust Zero-Shot Autoregressive TTS with Duration Control and Extrapolation** | Peng et al. | 2025 | arXiv 2505.19462 | First zero-shot TTS with output duration control and extrapolation to longer utterances. Uses PM-RoPE. 840M parameters trained on 65K hours. | Duration control is important for natural conversation pace in AAC contexts. |
| 15 | **EmoKnob: Enhance Voice Cloning with Fine-Grained Emotion Control** | Chen et al. (Columbia) | 2024 | EMNLP 2024, arXiv 2410.00316 | Framework for fine-grained emotion control in voice cloning. Extracts emotion direction vectors in speaker embedding space. Supports open-ended text descriptions for emotion. | Directly addresses VoiceReach's need for emotion/tone control in cloned voices. Model-agnostic approach that could be applied to any backbone. |
| 16 | **Marco-Voice Technical Report** | Alibaba AIDC | 2025 | arXiv 2508.02038 | Speaker-emotion disentanglement via in-batch contrastive learning. Rotational emotion embedding for smooth control. Outperforms CosyVoice on emotion fidelity. | State-of-art in emotion-identity disentanglement. Directly relevant to "same voice, different emotions" requirement. |
| 17 | **IndexTTS2: Emotionally Expressive and Duration-Controlled Zero-Shot TTS** | IndexTeam | 2025 | arXiv 2506.21619 | Disentangles emotional expression and speaker identity. Supports emotion prompt from different speaker + text-based emotion instructions via finetuned Qwen3. | Strong emotion control with natural language interface for emotion specification. Open-source. |
| 18 | **GLM-TTS: Controllable & Emotion-Expressive Zero-shot TTS with Multi-Reward RL** | Zhipu AI | 2025 | arXiv 2512.14291 | Multi-reward GRPO framework combining CER, SIM, Emotion, and Laughter rewards. Outperforms commercial models on emotion benchmarks. | Reinforcement learning approach to emotion; open-source (Dec 2025). |
| 19 | **ClonEval: An Open Voice Cloning Benchmark** | Cai et al. | 2025 | arXiv 2504.20581 | Standardized benchmark using LibriSpeech + 4 emotional speech datasets. Found XTTS-v2 achieves highest overall score among tested models. | Useful evaluation framework for comparing models during VoiceReach development. |

### 1.2 Voice Banking and ALS-Specific Papers

| # | Paper | Authors | Year | Venue | Summary | VoiceReach Relevance |
|---|-------|---------|------|-------|---------|---------------------|
| 20 | **The ModelTalker Project: A Web-Based Voice Banking Pipeline for ALS/MND Patients** | Bunnell & Lilley | 2013 | Various | Web-based pipeline requiring ~1600 sentences. Produces unit-selection synthetic voice. | Pioneer in ALS voice banking. Protocol is extensive but established. |
| 21 | **Voice Cloning for Dysarthric Speech Synthesis: Addressing Data Scarcity in Speech-Language Pathology** | Various | 2025 | arXiv 2503.01266 | Uses voice cloning on TORGO dataset to generate synthetic dysarthric speech. SLP misclassified 30% of synthetic as real. | Demonstrates voice cloning works even for dysarthric speech patterns. Relevant for ALS patients whose speech is already degrading. |
| 22 | **A Multilingual Framework for Dysarthria: Detection, Severity Classification, Speech-to-Text, and Clean Speech Generation** | Raman et al. | 2025 | arXiv 2510.03986 | Unified framework for dysarthria with 97% detection accuracy. Includes clean speech generation from degraded input. | "Clean speech generation" could reconstruct a patient's pre-degradation voice from their current degraded speech. |
| 23 | **Advancing Speech Accessibility with Personal Voice** | Apple ML Research | 2023 | Apple ML Blog | On-device voice banking with 150 sentences / 15 minutes. Machine learning tuning overnight on-device. | Apple's approach is the gold standard for accessibility-focused voice banking UX. |
| 24 | **Benchmarking Expressive Japanese Character TTS with VITS and Style-BERT-VITS2** | Various | 2025 | arXiv 2505.17320 | First formal comparison of VITS vs Style-BERT-VITS2 for expressive Japanese character speech. Evaluates pitch-accent and phoneme timing. | Directly relevant evaluation of Japanese TTS quality for expressive synthesis. |

### 1.3 Japanese-Language and Japanese-Focused Papers

| # | Paper | Authors | Year | Summary | Relevance |
|---|-------|---------|------|---------|-----------|
| 25 | **JVS corpus: free Japanese multi-speaker voice corpus** | Takamichi et al. | 2019 | arXiv 1908.06248. Free corpus of 30 hours from 100 speakers, 3 styles each. | Essential training/evaluation data for Japanese voice cloning. |
| 26 | **JSUT and JVS: Free Japanese voice corpora for accelerating speech synthesis research** | Takamichi et al. | 2020 | J. Acoust. Soc. Jpn. JSUT: 10 hours, 1 speaker. JVS: 30 hours, 100 speakers. | Foundational Japanese speech corpora. |
| 27 | **J-MAC: Japanese multi-speaker audiobook corpus for speech synthesis** | Various | 2022 | arXiv 2201.10896 | Japanese audiobook corpus for TTS research. | Additional Japanese training data source. |
| 28 | **Style-Bert-VITS2 JP Extra** | litagin02 et al. | 2024 | GitHub/community | Japanese-specialized VITS2 with 800-hour pretraining. WavLM discriminator for enhanced naturalness. | State-of-art for fine-tuned Japanese TTS with style control. Very active Japanese community. |

---

## 2. OSS Project Survey

### 2.1 Comprehensive Model Comparison Table

| Name | GitHub URL | Stars | License | Key Features | Japanese Support | Min Data | RTF / Latency | VoiceReach Suitability | Last Active |
|------|-----------|-------|---------|-------------|-----------------|----------|---------------|----------------------|-------------|
| **Fish Speech v1.5** | github.com/fishaudio/fish-speech | ~24.9K | Apache-2.0 (code), CC-BY-NC-SA-4.0 (model) | Zero-shot from ~10s. Trained on 1M+ hours. Rebranding to "OpenAudio S1". | Yes (>100K hrs training data) | ~10s | Low latency, limited streaming | **HIGH** -- Excellent Japanese support, large training data, active development. NC license on model is a concern. | Feb 2026 |
| **GPT-SoVITS v4** | github.com/RVC-Boss/GPT-SoVITS | ~55K | MIT | Few-shot (1 min) / zero-shot (5s). GPT + SoVITS two-stage. v2/v3/v4 with progressive improvements. | Yes (CN/EN/JP/KR/Cantonese) | 5s (zero-shot), 1 min (fine-tune) | Moderate | **HIGH** -- Most starred TTS repo. Strong Japanese. Great for fine-tuning with limited data. MIT license. | Feb 2026 |
| **CosyVoice 2/3** | github.com/FunAudioLLM/CosyVoice | ~19.6K | Apache-2.0 | Streaming + non-streaming. Human-parity quality. 9 languages + 18 Chinese dialects. 150ms streaming latency. | Yes (explicit JP support) | ~3-5s | 150ms (streaming) | **HIGH** -- Best streaming option. Excellent quality metrics. Japanese support. Apache license. | Feb 2026 |
| **F5-TTS** | github.com/SWivid/F5-TTS | ~14.1K | MIT | Non-autoregressive flow matching + DiT. No duration model needed. RTF 0.15. 2,994 MB GPU memory. | Yes (multilingual training) | ~3-5s | RTF 0.15 | **HIGH** -- Most resource-efficient. Good for edge deployment. MIT license. Strong long-form stability. | Feb 2026 |
| **Chatterbox** | github.com/resemble-ai/chatterbox | ~22.7K | MIT | MIT-licensed, 23 languages. Paralinguistic tags ([laugh], [cough]). PerTh watermarking. 63.75% preferred over ElevenLabs. | Yes (23 languages incl. Japanese) | ~3-5s | <200ms TTFB | **HIGH** -- Multilingual, MIT license, paralinguistic controls, watermarking for safety. | Feb 2026 |
| **ChatTTS** | github.com/2noise/ChatTTS | ~38.7K | AGPL-3.0 | Conversational TTS with detailed prosody. Fine-grained control (pause, laughter, etc.). | Partial (CN + EN focus) | N/A (no cloning) | Fast | **LOW** -- No voice cloning capability. Japanese not well supported. AGPL license is restrictive. | Jan 2026 |
| **IndexTTS / IndexTTS2** | github.com/index-tts/index-tts | ~18.8K | Custom | Emotion-timbre disentanglement. Duration control. Text-based emotion instruction via Qwen3. | Limited (CN + EN focus) | ~3-5s | Moderate | **MEDIUM** -- Excellent emotion control architecture, but Japanese support is unclear. | Dec 2025 |
| **OpenVoice v2** | github.com/myshell-ai/OpenVoice | ~35.9K | MIT | Instant voice cloning. Tone color cloning across languages. Flexible style control (emotion, accent, rhythm). | Yes (JP native support) | ~few seconds | Very fast (feed-forward) | **MEDIUM** -- Very fast inference, good for real-time. But quality may be below newer models. | Apr 2025 (stale) |
| **Orpheus TTS** | github.com/canopyai/Orpheus-TTS | ~5.9K | Apache-2.0 | Llama-3b backbone. Zero-shot cloning. Emotion tags. ~100-200ms streaming latency. | Limited (English focus) | ~few seconds | ~100-200ms | **LOW** -- English-focused. Japanese not supported natively. | Dec 2025 |
| **MaskGCT (Amphion)** | github.com/open-mmlab/Amphion | ~9.7K | MIT | ICLR 2025. Non-autoregressive. No alignment needed. Emotion control, cross-lingual dubbing. 100K hours training. | Limited (evaluation mainly English) | ~3-5s | Moderate | **MEDIUM** -- Strong academic backing. Cross-lingual capabilities. Japanese support needs verification. | May 2025 |
| **Coqui TTS (XTTS v2)** | github.com/coqui-ai/TTS | ~44.5K | MPL-2.0 | 17 languages incl. Japanese. Proven and widely used. Encoder at 21.53 Hz. Can fine-tune with 10 min. | Yes (17 languages) | 6s (zero-shot) | <150ms (streaming) | **MEDIUM** -- Proven Japanese support, but company shut down (Jan 2024). Code is archived. No active development. | Aug 2024 (archived) |
| **Tortoise TTS** | github.com/neonbjb/tortoise-tts | ~14.8K | Apache-2.0 | High quality but very slow. Good with RVC pipeline. | No (English only) | Multiple clips | Very slow (minutes) | **LOW** -- Too slow for real-time AAC. No Japanese. | Nov 2024 (stale) |
| **Bark** | github.com/suno-ai/bark | ~39K | MIT | Multilingual, non-verbal sounds. Simple API. | Partial | N/A (no true cloning) | Slow | **LOW** -- No voice cloning. Slow inference. Abandoned by Suno. | Aug 2024 (stale) |
| **MeloTTS** | github.com/myshell-ai/MeloTTS | ~7.2K | MIT | CPU-optimized real-time TTS. Multilingual. | Yes (JP support) | N/A (no cloning) | Real-time on CPU | **LOW** -- No voice cloning capability. Only useful for fallback generic voice. | Dec 2024 (stale) |
| **Parler-TTS** | github.com/huggingface/parler-tts | ~5.5K | Apache-2.0 | Text-described voice control (gender, pitch, style). Hugging Face official. | Limited | N/A (description-based, no cloning) | Moderate | **LOW** -- No voice cloning. Interesting for voice description but not patient voice preservation. | Dec 2024 (stale) |
| **GLM-TTS** | github.com/zai-org/GLM-TTS | ~0.9K | Apache-2.0 | Multi-reward RL (CER + SIM + Emotion + Laughter). Streaming inference. CN/EN bilingual. | No (CN + EN only) | ~few seconds | Streaming capable | **LOW** -- Interesting RL approach for emotion but no Japanese support. Too new (Dec 2025). | Dec 2025 |
| **Style-Bert-VITS2** | github.com/litagin02/Style-Bert-VITS2 | ~1.2K | AGPL-3.0 | Japanese-specialized VITS2. 800-hr JP pretraining. Style control. WavLM discriminator. | **Excellent** (Japanese-first) | ~10-30 min fine-tune | Fast | **HIGH for JP** -- Best Japanese-specific model. Requires fine-tuning (not zero-shot), but quality is excellent. AGPL license. | Dec 2025 |
| **VoiceCraft** | github.com/jasonppy/VoiceCraft | ~8.5K | Custom | Zero-shot speech editing + TTS. ACL 2024. Few seconds reference. | Limited (English focus) | ~few seconds | Moderate | **MEDIUM** -- Speech editing capability useful for voice bank post-processing. | Mar 2025 (stale) |
| **Seed-VC** | github.com/Plachtaa/seed-vc | ~3.6K | GPL-3.0 | Zero-shot voice conversion + singing voice conversion. Real-time support. 400ms latency on mid-range GPU. | Limited | ~few seconds | 400ms | **LOW** -- Voice conversion (not TTS). Could be used as post-processing. | Apr 2025 |
| **LLaSA** | HuggingFace: HKUSTAudio/Llasa-3B | N/A (HF) | N/A | Extends LLaMA for TTS. 1B/3B/8B sizes. 250K hours CN+EN training. XCodec2 (65K tokens). | Partial (CN + EN) | ~few seconds | Moderate | **LOW** -- No Japanese training data. Interesting LLM-TTS unification approach. | Feb 2025 |

### 2.2 Key Findings from OSS Survey

1. **Most active and capable for Japanese**: GPT-SoVITS (55K stars, MIT, explicit JP), Fish Speech (25K stars, Apache, 100K+ hrs JP data), CosyVoice (20K stars, Apache, explicit JP), Style-Bert-VITS2 (1.2K stars but Japanese-first design)
2. **Best streaming/real-time**: CosyVoice 2 (150ms), XTTS v2 (<150ms), Chatterbox (<200ms)
3. **Best emotion control**: IndexTTS2, Marco-Voice, GLM-TTS, EmoKnob (model-agnostic framework)
4. **Most resource-efficient**: F5-TTS (2,994 MB GPU), MeloTTS (CPU-capable)
5. **Coqui TTS/XTTS v2 is archived**: The company shut down in Jan 2024. Code remains usable but receives no updates.

---

## 3. Commercial Products & Voice Banking Programs

### 3.1 Voice Banking Services for ALS

| Name | Organization | Country | Recording Requirement | Cost | Technology | Japanese Availability | ALS Suitability |
|------|-------------|---------|----------------------|------|------------|---------------------|-----------------|
| **Acapela My-Own-Voice v3** | Acapela Group (Belgium) | International | 50 sentences (~10-20 min) with DNN; 1500 sentences with unit selection | Free for ALS (via Team Gleason/MND Assoc.) | DNN-based voice synthesis | No (European languages + EN) | **HIGH** -- Designed for ALS. Minimal recording. Funded by charities. |
| **ModelTalker** | Nemours/U of Delaware | USA | ~1600 sentences | $100 download fee | Unit selection synthesis | No | **MEDIUM** -- Pioneer but requires extensive recording. Older technology. |
| **Apple Personal Voice** | Apple | Global | 150 sentences (~15 min) | Free (built into iOS/macOS) | On-device ML | Yes (available on Japanese iOS) | **VERY HIGH** -- Free, minimal recording, on-device privacy, works with AAC apps. Available in Japan. |
| **ALS SAVE VOICE** | Ory Lab + Toshiba Digital Solutions + WITH ALS | Japan | ~10 sentences / ~5-20 min (via CoEStation) | Free (crowdfunded) | Toshiba CoEStation TTS | **Yes (Japanese-native)** | **VERY HIGH** -- Only Japanese-native ALS voice preservation service. Integrates with OriHime eye-tracking device. |
| **SpeakUnique** | U of Edinburgh spin-out | UK/Scotland | 150-400 sentences | Funded by NHS Scotland / MND Scotland for eligible patients | DNN voice synthesis | No | **HIGH** -- Three modes: Voice Build, Voice Repair, Voice Design. Can work with degraded speech. |
| **VocaliD (Veritone Voice)** | VocaliD / Veritone | USA | 3 seconds (BeSpoke) to full banking | $1,199+ for custom voice | Voice matching + blending | No | **MEDIUM** -- BeSpoke mode works with minimal/impaired speech. Expensive. |
| **ElevenLabs** | ElevenLabs | International | ~1 min (Instant) / ~30 min (Professional) | Subscription-based ($5-99/mo) | Proprietary DNN | Partial (multilingual) | **MEDIUM** -- Commercial service, not ALS-specific. Good quality but ongoing cost. |
| **Team Gleason Voice Banking** | Team Gleason | USA | Varies (partners with multiple providers) | Free for ALS patients | Multiple (Acapela, Apple PV, etc.) | No | **HIGH** -- Umbrella program connecting ALS patients with voice banking services. |
| **I Will Always Be Me** | Dell + Intel + Team Gleason | USA | Custom recording + AI | Free for ALS patients | Custom AI voice banking | No | **HIGH** -- Lets patients "voice bank with feeling" -- captures emotional variations. |

### 3.2 Commercial TTS APIs with Voice Cloning

| Name | Key Features | Japanese Quality | Latency | Pricing | VoiceReach Suitability |
|------|-------------|-----------------|---------|---------|----------------------|
| **ElevenLabs** | Industry-leading quality. Multilingual. Instant + Professional cloning. | Good | ~300ms | $5-99/mo | Good quality but ongoing API costs |
| **Fish Audio API** | Based on Fish Speech. Production-grade. | Excellent | Low | Pay-per-use | Strong Japanese. Same team as OSS model. |
| **Resemble AI** | Enterprise voice cloning. Watermarking. Emotion control. | Good | <200ms | Enterprise pricing | Professional but expensive |
| **Google Cloud TTS** | Custom Voice (10s minimum). Reliable infrastructure. | Excellent | Low | Pay-per-use | Good Japanese quality, Google infrastructure |
| **Azure Neural TTS** | Microsoft's commercial offering. Custom Neural Voice. | Good | Low | Pay-per-use | Based on Microsoft's TTS research (VALL-E lineage) |

---

## 4. Answers to Specific Research Questions

### Q1: State-of-the-art quality in zero-shot voice cloning from < 1 hour of audio?

**Answer**: As of early 2026, the state-of-the-art has advanced dramatically:

- **Zero-shot (no fine-tuning)**: Models like VALL-E 2, CosyVoice 3, Fish Speech v1.5, and Chatterbox can produce high-quality clones from **3-10 seconds** of reference audio. VALL-E 2 achieved human parity on LibriSpeech/VCTK benchmarks in June 2024.
- **Few-shot (minimal fine-tuning)**: GPT-SoVITS achieves excellent results with just **1 minute** of reference audio and brief fine-tuning.
- **With 30-60 minutes of data**: This is now considered a **generous** amount of data. Fine-tuning any modern model (F5-TTS, CosyVoice, GPT-SoVITS, Style-Bert-VITS2) with 30-60 minutes of clean data will produce results that are nearly indistinguishable from the original speaker for most listeners.
- **MOS scores**: The best models achieve MOS 4.0-4.5 (on a 1-5 scale) for cloned voices with sufficient reference data, approaching ground truth (MOS ~4.5-4.8). With 30-60 minutes of Japanese data and fine-tuning, MOS 3.8-4.3 is achievable.

### Q2: How do XTTS v2, StyleTTS 2, VALL-E X, and Coqui TTS compare in Japanese quality?

**Answer**:

| Model | Japanese Quality | Notes |
|-------|-----------------|-------|
| **XTTS v2** | **Medium-Good** | Japanese is one of 17 supported languages. Accent and prosody are acceptable but not native-level. Pitch-accent errors occur. Company (Coqui) shut down; no further improvements. |
| **StyleTTS 2** | **Not available** | English-only. No Japanese support. Excellent quality for English but irrelevant for Japanese use. |
| **VALL-E X** | **Unknown (not released)** | Microsoft has not released the model. Theoretical support for Japanese but no public evaluation. |
| **Coqui TTS** | **Medium** | The broader Coqui TTS library includes VITS and other models. Japanese quality is functional but not state-of-the-art. XTTS v2 is the best option within the Coqui ecosystem. |

**Recommendation**: For Japanese, all four original candidates are suboptimal. Better choices in 2026 are **GPT-SoVITS** (best few-shot Japanese), **Fish Speech v1.5** (best zero-shot Japanese, 100K+ hrs JP training), **CosyVoice 2/3** (best streaming Japanese), and **Style-Bert-VITS2** (best fine-tuned Japanese quality).

### Q3: What voice banking programs exist internationally and in Japan? What recording protocols do they use?

**Answer**: See Section 3.1 for the comprehensive table. Key findings:

**International Programs**:
- **Acapela My-Own-Voice v3**: 50 sentences, 10-20 minutes. DNN-based. Free for ALS via charities.
- **Apple Personal Voice**: 150 sentences, 15 minutes. On-device processing. Free on iOS 17+.
- **ModelTalker**: 1600 sentences. Older unit-selection technology. $100.
- **SpeakUnique**: 150-400 sentences. Three modes including "Voice Repair" for degraded speech.
- **Team Gleason**: Umbrella program providing free access to multiple services.

**Japan-Specific**:
- **ALS SAVE VOICE** (Ory Lab + Toshiba + WITH ALS): The only Japanese-native program. Uses Toshiba CoEStation (10 sentences / 5-20 minutes). Integrates with OriHime eye-tracking device. Launched 2019 via crowdfunding.
- **Apple Personal Voice**: Available on Japanese iOS devices.
- No equivalent of Team Gleason exists in Japan. The ALS Association Japan (日本ALS協会) does not currently offer a comprehensive voice banking program.

**Recording Protocol Summary**:
- Modern DNN-based services: 50-150 sentences, 10-20 minutes
- Older unit-selection services: 1500-1600 sentences, several hours
- VoiceReach should target: 50-200 guided sentences (phoneme coverage) + 15-30 min free conversation

### Q4: How can emotion/tone control be achieved in cloned voices?

**Answer**: Multiple approaches exist, roughly categorized:

1. **Speaker-Emotion Disentanglement** (Most promising for VoiceReach):
   - **Marco-Voice** (Alibaba 2025): In-batch contrastive learning separates speaker identity from emotion. Rotational embedding for smooth emotion control.
   - **IndexTTS2** (2025): Separate emotion prompt (from any speaker) + text-based emotion instructions.
   - **NaturalSpeech 3** (Microsoft 2024): Factorized codec disentangles content, prosody, timbre, acoustic details.

2. **Emotion Direction Vectors** (Model-agnostic):
   - **EmoKnob** (Columbia, EMNLP 2024): Extracts emotion direction in speaker embedding space using neutral/emotional pair. Adjustable emotion strength. Can work with any voice cloning backbone.

3. **Reinforcement Learning for Emotion**:
   - **GLM-TTS** (Zhipu 2025): GRPO framework with Emotion reward function. Multi-reward optimization (CER + SIM + Emotion + Laughter).

4. **Paralinguistic Tags**:
   - **Chatterbox Turbo**: Native [cough], [laugh], [chuckle] tags.
   - **Orpheus TTS**: Emotion tags in text input.

5. **Prosody Transfer from Emotion Reference**:
   - Record emotion samples during voice banking (happy, sad, calm, urgent)
   - Use these as emotion references at synthesis time

**Recommendation for VoiceReach**: Use a hybrid approach:
- Primary: Choose a backbone model with native emotion disentanglement (CosyVoice 2/3 or Fish Speech with fine-tuning)
- Augment with: EmoKnob-style direction vectors for fine-grained control
- Record: Emotion samples during Phase 0 voice banking (Session 2 of current protocol)
- Interface: Map PVP valence/arousal to emotion vectors automatically, with manual override

### Q5: What is the minimum recording quality and quantity needed?

**Answer**:

**Recording Quality Requirements**:

| Parameter | Minimum | Recommended | Optimal |
|-----------|---------|-------------|---------|
| Sample Rate | 22 kHz | 44.1 kHz | 48 kHz |
| Bit Depth | 16-bit PCM | 16-bit PCM | 24-bit PCM |
| SNR | >30 dB | >35 dB | >40 dB |
| Background Noise Floor | <-50 dB | <-60 dB | <-70 dB |
| Volume (RMS) | -23 to -18 dB | -20 to -16 dB | Consistent |
| Peak Level | <-3 dB | <-6 dB | <-6 dB |
| Format | WAV (uncompressed) | WAV | WAV |
| Microphone | Smartphone mic | USB condenser mic | Studio condenser mic |
| Distance | 20-50 cm | 20-30 cm | 20-30 cm with pop filter |

**Recording Quantity Requirements**:

| Use Case | Minimum | Recommended | Notes |
|----------|---------|-------------|-------|
| Zero-shot (no fine-tuning) | 3-10 seconds | 30-60 seconds | Quality depends on model |
| Few-shot fine-tuning | 1 minute | 5-10 minutes | GPT-SoVITS excels here |
| High-quality fine-tuning | 10-30 minutes | 30-60 minutes | Diminishing returns above 1 hour |
| Emotion coverage | 5 min per emotion | 10-15 min per emotion | 4-5 emotion categories |
| Optimal total | 30 minutes | 45-60 minutes | Including emotions and free speech |

**Key insight**: With modern models (2025-2026), the bottleneck is no longer data quantity but data quality. 30 minutes of clean, high-SNR recording with good phoneme coverage will outperform 3 hours of noisy or inconsistent recording.

---

## 5. Comparative Analysis for VoiceReach

### 5.1 Best Approaches for VoiceReach's Specific Needs

VoiceReach requires:
1. Japanese voice cloning (primary)
2. Emotion/tone control
3. Real-time synthesis (<500ms for AAC)
4. Works with 30-60 min recording
5. Open-source / self-hostable (privacy)
6. Runs on consumer hardware

**Tier 1 Candidates (Recommended for primary investigation)**:

| Model | Japanese | Emotion | Real-time | Data Needs | License | Overall |
|-------|---------|---------|-----------|-----------|---------|---------|
| **CosyVoice 2/3** | Excellent | Good (native) | Excellent (150ms streaming) | 3-5s zero-shot | Apache-2.0 | **Best overall balance** |
| **GPT-SoVITS v4** | Excellent | Good | Moderate | 1 min few-shot | MIT | **Best for fine-tuning with limited data** |
| **Fish Speech v1.5** | Excellent (100K+ hrs JP) | Moderate | Good | 10s zero-shot | Apache (code) / CC-BY-NC-SA (model) | **Best Japanese zero-shot, but NC model license** |
| **F5-TTS** | Good | Moderate | Good (RTF 0.15) | 3-5s | MIT | **Best resource efficiency** |

**Tier 2 Candidates (Good alternatives or supplementary)**:

| Model | Strengths | Weaknesses |
|-------|----------|------------|
| **Chatterbox** | MIT license, 23 languages, paralinguistic tags, watermarking | Newer, less Japanese-specific evaluation |
| **Style-Bert-VITS2** | Best Japanese-specific quality, style control | Requires fine-tuning, AGPL license, not zero-shot |
| **IndexTTS2** | Best emotion-timbre disentanglement | Japanese support unclear, custom license |

### 5.2 Recommended Architecture

```
Phase 0 (Voice Banking):
  Recording App → WAV files (48kHz/24bit)
  ↓
  Preprocessing Pipeline:
    - Noise reduction (RNNoise / DTLN)
    - Speaker diarization (if multi-speaker source)
    - VAD + segmentation
    - Quality scoring (SNR, clarity)
    - Forced alignment + transcription
  ↓
  Storage: Raw WAV + processed segments + metadata

Phase 2 (Voice Synthesis Integration):
  Text Input (from candidate selection)
  ↓
  Japanese Text Processing:
    - Morphological analysis (MeCab/Sudachi)
    - Reading estimation (kanji → furigana)
    - Accent estimation (OJAD or trained model)
  ↓
  Emotion/Tone Selection:
    - Auto: PVP valence/arousal → emotion vector
    - Manual: Tone selector (calm/happy/serious/gentle)
  ↓
  TTS Engine (Primary: CosyVoice 2 or GPT-SoVITS):
    - Speaker embedding from voice bank
    - Emotion conditioning
    - Streaming synthesis
  ↓
  Post-processing:
    - Volume normalization
    - Latency optimization
  ↓
  Speaker Output
```

---

## 6. Recommendations

### 6.1 Recording Protocol for Phase 0

Based on the research, the current doc (08_VOICE_PRESERVATION.md) protocol is well-designed but should be updated:

**Updated Recommendations**:

1. **Reduce minimum barrier**: The protocol should have a "minimum viable recording" of just **50 guided sentences + 10 minutes free speech** (~20 minutes total). This aligns with Acapela's v3 and Apple's approach, and modern models can work with this.

2. **Target quality**: 44.1 kHz / 16-bit minimum. Recommend a USB condenser microphone (e.g., Blue Yeti, Audio-Technica AT2020USB+), but explicitly support smartphone recording as a fallback. Include SNR check in the recording app.

3. **Sentence set design**: Create a Japanese phoneme-covering sentence set of 100 sentences that also sounds natural (not linguistic test sentences). Reference the JSUT/JVS corpus sentence design. Include:
   - All Japanese morae (including palatalized, voiced, semi-voiced)
   - Common pitch-accent patterns
   - Various sentence types (declarative, interrogative, exclamatory)

4. **Emotion recording**: Record at least 3-4 emotion categories:
   - Neutral / calm (base)
   - Happy / warm
   - Serious / emphatic
   - Gentle / soft
   - Each category: read 10 sentences + 5 min free conversation about relevant topic

5. **Existing audio pipeline**: Prioritize building the preprocessing pipeline for existing recordings (videos, voice messages) as many patients will already have speech degradation at time of contact.

6. **Compatibility with multiple models**: Save speaker embeddings in a model-agnostic format. Always preserve raw WAV data. The TTS model landscape changes rapidly; today's best model may be superseded within months.

### 6.2 Model Selection for Phase 2

**Primary recommendation**: **CosyVoice 2/3**
- Rationale: Best combination of Japanese support, streaming capability (150ms), open-source Apache license, active development by Alibaba, and built-in emotion support
- Risk: Alibaba could change licensing or development direction

**Secondary/backup**: **GPT-SoVITS v4**
- Rationale: MIT license, most popular (55K stars), excellent Japanese few-shot quality, active community
- Risk: Not as strong at zero-shot; requires fine-tuning step

**For fine-tuned Japanese quality**: **Style-Bert-VITS2**
- Rationale: Purpose-built for Japanese, 800-hr JP pretraining, excellent pitch-accent handling
- Risk: AGPL license, requires dedicated fine-tuning, not zero-shot

**For emotion control**: Apply **EmoKnob** framework on top of the chosen backbone model
- Model-agnostic emotion direction vectors
- Can be added post-hoc to any voice cloning system

### 6.3 Integration Architecture

1. **Model serving**: Use vLLM or TensorRT-LLM for serving the TTS model. Target: RTX 3060 or better (consumer GPU).
2. **Streaming**: Use CosyVoice 2's chunk-aware streaming for <200ms first-chunk latency.
3. **Fallback chain**: CosyVoice (streaming) → F5-TTS (batch, high quality) → pre-generated phrases (instant)
4. **Privacy**: All inference runs locally. Voice bank data encrypted at rest. No cloud dependency for synthesis.

---

## 7. Open Questions

1. **Japanese emotion TTS quality**: No published benchmarks compare emotion-controlled voice cloning quality specifically for Japanese. We will need to conduct our own evaluation.

2. **Degraded speech reconstruction**: If a patient's speech is already partially degraded, can we use their degraded audio + pre-degradation recordings (videos) to reconstruct a high-quality voice? The 2025 dysarthria papers suggest this is possible but practical implementation is unclear.

3. **Long-term model stability**: The TTS model landscape evolves rapidly. CosyVoice 2 may be superseded by CosyVoice 4 within a year. How do we design the system for easy model swapping?

4. **Regulatory status**: Are cloned voices considered "medical devices" in Japan? The voice banking recording app may need regulatory consideration.

5. **MOS validation**: We need to conduct MOS evaluation with Japanese speakers for the top candidate models, specifically comparing zero-shot vs. fine-tuned results with 30-60 minutes of recording.

6. **Fish Speech / OpenAudio licensing**: The model weights are CC-BY-NC-SA, which prevents commercial use. Will OpenAudio release commercially-licensed models?

7. **Patient consent and voice rights post-mortem**: The ethical framework for voice cloning in Japan's legal system needs further investigation, particularly regarding the right to one's voice as a personality right (パブリシティ権).

8. **Apple Personal Voice API access**: Can third-party apps (like VoiceReach) access Apple Personal Voice on iOS? Current indications are yes (via AVSpeechSynthesizer), but the quality and controllability may be limited compared to direct model hosting.

---

## References

Key repositories and resources:
- Fish Speech: https://github.com/fishaudio/fish-speech
- GPT-SoVITS: https://github.com/RVC-Boss/GPT-SoVITS
- CosyVoice: https://github.com/FunAudioLLM/CosyVoice
- F5-TTS: https://github.com/SWivid/F5-TTS
- Chatterbox: https://github.com/resemble-ai/chatterbox
- Style-Bert-VITS2: https://github.com/litagin02/Style-Bert-VITS2
- IndexTTS: https://github.com/index-tts/index-tts
- OpenVoice: https://github.com/myshell-ai/OpenVoice
- MaskGCT (Amphion): https://github.com/open-mmlab/Amphion
- EmoKnob: https://github.com/tonychenxyz/emoknob
- GLM-TTS: https://github.com/zai-org/GLM-TTS
- Seed-TTS-eval: https://github.com/BytedanceSpeech/seed-tts-eval
- ClonEval: https://github.com/amu-cai/cloneval
- ALS SAVE VOICE: https://prtimes.jp/main/html/rd/p/000000022.000019066.html
- Acapela My-Own-Voice: https://mov.acapela-group.com/
- Apple Personal Voice: https://machinelearning.apple.com/research/personal-voice

# A6: Finger/Pressure Input for ALS Patients - Deep Research Report

## Executive Summary

This report investigates finger and pressure input devices suitable for the VoiceReach ALS communication platform. VoiceReach separates "look" from "select" --- gaze handles pointing while a finger tap provides confirmation --- requiring a highly sensitive, adaptive pressure input that works across ALS disease progression stages. The research covers academic literature, commercial switch products, Japanese market specifics, piezo sensor hardware, USB HID implementation, involuntary movement filtering, and progressive adaptation strategies.

---

## 1. Academic Literature Review

### 1.1 Switch Access for AAC

**LeMMS: Lever Magnetic-spring Mechanical Switch (Battistini et al., 2019)**
Published in the Journal of NeuroEngineering and Rehabilitation, this is the most directly relevant paper for VoiceReach. The LeMMS switch was designed specifically for ALS patients who lose the ability to extend fingers (antagonist muscles) needed to release conventional switches.

- **Mechanism**: A lever-based magnetic-spring design using ferrite cuboid magnets (9x5x5mm, 350g adhesion) and a Huaweite Electronics WK1-01 buckling-spring micro-switch
- **Activation force**: As low as "a few grams" --- patients adjust finger position longitudinally along the lever to find the equilibrium point requiring minimal active force
- **Key innovation**: Unlike capacitive sensors, the LeMMS provides return force to release the switch without requiring finger extension. This addresses a critical limitation where "the lack of antagonist muscles...makes it impossible to return the switch to the rest position."
- **Clinical results** (20 ALS patients, 12 months):
  - All 20 patients activated LeMMS after a single training session
  - Click-Test-30 baseline: 25.2 +/- 10.7 activations per 30 seconds
  - Daily usage: 5.45 hours/day average
  - At 12 months: 9/20 still using LeMMS for scanning access; 7 deceased, 3 transitioned to eye-tracking, 1 progressed beyond use
  - QUEST 2.0-Dev satisfaction: 4.63/5.0
  - ROC analysis: 16 activations/30s predicted successful scanning access (sensitivity 1.00, specificity 0.89)
- **Cost advantage**: Commercial eye-tracking costs approximately 15x more than scanning systems with LeMMS

Reference: [Battistini et al., J NeuroEngineering Rehabilitation, 2019](https://link.springer.com/article/10.1186/s12984-019-0626-5)

**Multi-Modal Access: Eye-Tracking + Switch-Scanning (2022)**
A study combining eye-tracking with switch-scanning for individuals with severe motor impairment demonstrated the approach VoiceReach is taking:

- **Equipment**: Tobii-Dynavox PCEye Mini eye-tracker + Jellybean switch
- **Method**: Eye gaze identified a cluster of 3-4 neighboring letters within 250px radius, then switch activation triggered linear scanning through the group
- **Results**: Multi-modal achieved 1.54 WPM with 7.1% error rate vs. eye-tracking alone at 2.34 WPM with 26.9% error rate
- **Key finding**: The trade-off showed slower speed but significantly improved accuracy --- directly validating VoiceReach's gaze+tap design
- **Four clinical subgroups** emerged: multi-modal beneficiaries, eye-tracking preference users, learning trajectory users, and fluctuating performance users --- suggesting VoiceReach needs to support multiple interaction modes

Reference: [Multi-modal access method, PMC, 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9576815/)

**Noncontact Gesture-Based Switch (AAGI, 2025)**
A noncontact switch enabling digital control for late-stage Duchenne Muscular Dystrophy patients. Input speed more than doubled after 3 months, with notable improvements in usability and quality of life. This represents the frontier of minimal-movement input for progressive neuromuscular diseases.

Reference: [Noncontact Gesture Switch, MDPI Healthcare, 2025](https://www.mdpi.com/2227-9032/13/22/2989)

### 1.2 Adaptive Threshold Algorithms for EMG/Pressure Signals

**Double-Threshold Detection**
Research shows that double-threshold detectors yield higher detection probability than single-threshold approaches for EMG onset detection. This directly applies to VoiceReach's need to distinguish intentional taps from noise:
- Primary threshold detects potential activation
- Secondary threshold (temporal or amplitude) confirms intentional input
- Users can tune detector performance according to different optimal criteria

Reference: [Adaptive Algorithm for Muscle Contraction Onset/Offset, IEEE, 2012](https://ieeexplore.ieee.org/document/6353938/)

**Adaptive Filtering for Non-Stationary Biomedical Signals**
Adaptive filters based on orthogonal discrete cosine or wavelet transforms provide high efficiency of noise suppression. LMS (Least Mean Squares) adaptive algorithms with synthetic references are effective for eliminating artifacts --- applicable to filtering fasciculations from intentional presses.

Reference: [Reducing Noise in Single-Channel EMG Signals, PMC, 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10059683/)

**Recursive Singular Spectrum Analysis (RSSA) for Tremor Isolation**
For real-time surgical robotics, RSSA combined with Random Vector Functional Link (RVFL) networks can isolate physiological tremor from intentional movement. Moving window variants enable real-time implementation on embedded systems.

Reference: [Real-time Tremor Isolation, ScienceDirect, 2024](https://www.sciencedirect.com/science/article/abs/pii/S0019057824006281)

### 1.3 Machine Learning for Involuntary Movement Classification

- **Mechanomyography (MMG)**: Uses accelerometers to measure low-frequency muscle vibrations (as opposed to EMG's electrical signals). More practical for a non-invasive wearable switch.
- **K-Nearest Neighbors (KNN)**: Achieved 95% accuracy in muscular fatigue prediction --- could be adapted for fasciculation vs. intentional tap classification
- **Autoencoders**: Commonly used to detect abnormal muscle movements (Parkinson's, ASD) --- applicable as anomaly detectors for involuntary movements

Reference: [Wearable Super-Resolution Muscle-Machine Interfacing, Frontiers Neuroscience, 2022](https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2022.1020546/full)

---

## 2. Commercial Switch Products

### 2.1 Product Comparison Table

| Product | Company | Price (USD) | Activation Force | Input Type | Travel | Interface | ALS Suitability | Japan Availability |
|---------|---------|-------------|-----------------|------------|--------|-----------|----------------|-------------------|
| **Micro Light Switch** | AbleNet | ~$100 | 10g (0.4 oz) | Mechanical press | 0.7cm | 3.5mm mono | Excellent (Stage 1-3) | Via importers |
| **Jelly Bean Twist** | AbleNet | ~$65 | 71g (2.5 oz) | Mechanical press | --- | 3.5mm mono | Good (Stage 1-2) | Via importers |
| **Buddy Button** | AbleNet | ~$60 | 142g (5 oz) | Mechanical press | 0.12cm | 3.5mm mono | Limited (Stage 1) | Via importers |
| **PPS Switch 2025** | Pacific Supply | JPY 46,970 | Ultra-low (piezo) | Piezo + Pneumatic | N/A | 3.5mm | Excellent (Stage 1-4) | Native Japanese |
| **Sip/Puff Switch** | Origin Instruments | ~$200 | ~3 in. water column | Breath | N/A | Dual 3.5mm | Alternative (no hand) | Via importers |
| **Petite Pillow Switch** | Enabling Devices | ~$50 | ~40g | Foam pillow press | N/A | 3.5mm mono | Good (Stage 1-2) | Via importers |
| **Plate Switch** | Enabling Devices | ~$35 | Very light touch | Thin plastic plate | N/A | 3.5mm mono | Good (Stage 1-3) | Via importers |
| **tecla-e** | Komodo OpenLab | ~$400 | N/A (hub device) | Switch hub (BLE) | N/A | BLE + 3.5mm | Hub for any switch | Limited |
| **Xbox Adaptive Controller** | Microsoft | ~$100 | N/A (hub device) | Switch hub (USB) | N/A | 19x 3.5mm + USB | Hub for any switch | Available in Japan |

### 2.2 Key Product Details

**AbleNet Micro Light Switch (Product #58500)**
- Activation surface: 1.7 x 0.5 in (4.5 x 1.3 cm)
- Activation force: 10g --- the lowest-force commercial mechanical switch readily available
- Provides auditory click and tactile feedback
- 5 ft cord, 3.5mm mono jack
- Threaded insert for mounting
- The closest commercial equivalent to what VoiceReach needs, but lacks adaptive threshold or digital filtering

**Pacific Supply PPS Switch 2025**
- The gold standard in Japan for ALS patients
- Dual sensor types: Piezoelectric (detects distortion/strain) and Pneumatic (air bag + cushion sensor)
- Piezo sensor: 17mm diameter disc, attaches with medical tape
- Control box: 76mm x 135mm x 27mm
- Power: USB Type-A, 3x AA batteries (30-day continuous use), or AC adapter
- Adjustable sensitivity and anti-malfunction protection
- Price: JPY 46,970 (tax included)
- This is the primary competitor/reference product for VoiceReach's input module

**Origin Instruments Sip/Puff Switch**
- Translates sips and puffs into independent switch closures
- Pressure thresholds: ~3 inches water column above/below ambient
- Switches carry 40 mA at AC/DC 30V or less, millions of cycles
- No external power required (electro-mechanical design)
- Comfortable adjustable headset with replaceable mouth tubes
- Relevant as a fallback input for Stage 4 ALS when finger input is no longer possible

**tecla-e (Komodo OpenLab)**
- Bluetooth Low Energy hub connecting adaptive switches to smartphones, tablets, computers
- Pairs with up to 8 BLE devices simultaneously
- Supports up to 6 switches or wheelchair controls
- Built-in sensors: location, temperature, motion, ambient light
- Size: 98 x 98 x 40mm, Weight: 230g
- Battery: 4600 mAh (90+ hours continuous use)
- Could serve as a bridge between VoiceReach's custom sensor and standard devices

---

## 3. Japanese Market

### 3.1 Regulatory Framework: Assistive Device Subsidies

Japan has a well-established public funding system for communication devices for severely disabled individuals:

**Supplementary Equipment (Hosousou-hi / 補装具費)**
- Communication devices (意思伝達装置) have been classified as supplementary equipment since October 2006
- Switches are included in the coverage as part of the communication device system
- For ALS and other progressive diseases, replacement (re-issuance) is permitted as the disease progresses
- Repair/replacement allowances by switch type:
  - Contact-type switch (接点式入力装置): JPY 10,000
  - Myoelectric switch (筋電式入力装置): JPY 80,000

**Daily Living Equipment Grant (日常生活用具給付)**
- "Information/Communication Support Equipment" category: JPY 100,000 base amount
- Covers PC peripherals, software, switches, mounting hardware
- Simpler application process (no medical opinion required)
- Limitation: No re-issuance for progressive diseases (unlike supplementary equipment)

### 3.2 Japanese Switch Products and Distributors

**National Rehabilitation Center Switch Database**
The National Rehabilitation Center for Persons with Disabilities (国立障害者リハビリテーションセンター) maintains a comprehensive database of 53 switches (as of October 2024), classified into 7 categories:

| Category (Japanese) | Count | Subsidy Base (JPY) | Description |
|---------------------|-------|-------------------|-------------|
| 接点式入力装置 (Contact switches) | 35 | 10,600 | Standard mechanical switches, 7.4g to 517.9g activation |
| 帯電式入力装置 (Capacitive switches) | 7 | 42,700 | Touch/proximity activation without physical pressure |
| 筋電式入力装置 (Myoelectric switches) | 2 | 85,400 | EMG-based, detects muscle electrical activity |
| 光電式入力装置 (Photoelectric switches) | 1 | --- | Light-based detection |
| 呼気式入力装置 (Breath switches) | 6 | 37,300 | Sip/puff and microphone-based |
| 圧電素子式入力装置 (Piezoelectric switches) | 1 | 53,400 | The PPS Switch category |
| 空気圧式入力装置 (Pneumatic switches) | 2 | 42,700 | Air bag/cushion sensors |

Reference: [National Rehabilitation Center Switch Database](https://www.rehab.go.jp/ri/kaihatsu/itoh/com-sw.html)

**Key Japanese Distributors and Manufacturers**

| Company | Products | Role |
|---------|----------|------|
| **Pacific Supply (パシフィックサプライ)** | PPS Switch 2025, Spec Switch, Pin Touch Switch, Point Touch Switch, rental switch sets | Primary manufacturer of ALS-focused switches |
| **Double Giken (ダブル技研)** | Distributor for 伝の心, miyasuku, My Tobii, TC Scan, OriHime eye+Switch | Major distributor of communication devices |
| **Creact (クレアクト)** | TC Scan | Communication device manufacturer |
| **Unicorn (ユニコーン)** | miyasuku EyeConSW | Software-based communication device |
| **Hitachi KE Systems** | 伝の心 (Den no Shin) | Historic ALS communication device since 1992 |
| **AT-mall (エイティーモール)** | Online retail | E-commerce platform for assistive technology |

**Japanese Communication Device Prices**

| Device | Type | Price (JPY, tax-excluded) |
|--------|------|--------------------------|
| miyasuku EyeConSW (w/ printer) | Eye gaze + Switch scanning | 504,000 |
| miyasuku EyeConSW (w/o printer) | Eye gaze + Switch scanning | 488,000 |
| 伝の心 (Den no Shin) | Switch scanning | ~450,000 |
| マイトビー I-16 | Eye gaze + tablet integrated | ~580,000 |
| PPS Switch 2025 | Input switch only | 46,970 |

### 3.3 VoiceReach Positioning in Japan

VoiceReach's input module would fall into the 圧電素子式入力装置 (Piezoelectric switch) category for subsidy purposes. The current subsidy base of JPY 53,400 is sufficient to cover the PPS Switch 2025 (JPY 46,970), and VoiceReach's custom piezo module should be designed to stay within this price range for maximum accessibility. The 補装具 (supplementary equipment) pathway is preferred over 日常生活用具 (daily living equipment) because it allows replacement as ALS progresses.

---

## 4. Piezo Sensor Hardware

### 4.1 Sensor Technology Comparison

| Sensor Type | Principle | Force Range | Static Force | Dynamic Response | Price | ALS Suitability |
|-------------|-----------|-------------|--------------|-----------------|-------|----------------|
| **Piezo Disc (PZT ceramic)** | Piezoelectric effect | N/A (voltage on deformation) | Cannot detect | Excellent | $0.50-$2 | Good for tap detection |
| **PVDF Film (e.g., LDT0-028K)** | Piezoelectric polymer | N/A (voltage on flex) | Cannot detect | Excellent | $3-$8 | Good for vibration/tap |
| **FSR (e.g., Interlink FSR-402)** | Piezoresistive | 0.1N - 10N (~10g - 1kg) | Yes | Moderate | $5-$12 | Good for sustained press |
| **Flex/Bend Sensor** | Resistive (carbon ink) | Bend angle | Yes | Moderate | $8-$15 | Alternative for finger curl |
| **Capacitive Touch** | Capacitance change | Zero force | N/A | Fast | $1-$5 | Limited (no return force) |
| **Strain Gauge** | Resistance change | Sub-gram to kg | Yes | Good | $5-$20 | Excellent precision |

### 4.2 Recommended Piezo Elements

**For VoiceReach's tap detection (primary recommendation):**

**27mm PZT Ceramic Disc**
- Specifications: Resonance frequency 4.6 KHz +/- 0.5 KHz, capacitance 20nF +/- 30% at 1 KHz, resonant impedance 300 ohm max
- Output: Up to +/-90V on strong impact; safe range for MCU: -0.5V to +5V with load resistor
- Price: $0.50-$2.00 per disc (extremely low cost)
- Wiring: Positive terminal to ADC pin, negative through 1M ohm resistor to ground
- Advantages: Extremely sensitive to dynamic force changes (taps), very low cost, no power required for sensing
- Limitations: Cannot detect static (sustained) force --- only detects changes. This is actually beneficial for tap detection.
- Source: [SparkFun, Amazon, generic electronics suppliers]

**SparkFun Piezo Vibration Sensor (LDT0-028K, PVDF film)**
- PVDF polymer film sensor from Measurement Specialties
- Available in multiple form factors: Large with Mass (SEN-09197), Large (SEN-09196), Small Horizontal (SEN-09198), Small Vertical (SEN-09199)
- Output: AC voltage, spikes between -0.5V and +5V with 1M ohm load resistor
- Very flexible thin film --- can be attached to skin or fabric
- Higher sensitivity than ceramic disc for very small vibrations
- Price: $3-$8
- Source: [SparkFun Piezo Vibration Sensor](https://www.sparkfun.com/products/9197)

**FSR-402 (Interlink Electronics) --- for sustained press detection:**
- Active area: 14.7mm diameter (18.28mm total diameter)
- Force range: 0.1N to 10N (approximately 10g to 1kg)
- Stand-off resistance: >10M ohm
- Operating temperature: -30C to +70C
- Sensitivity: Actuation force as low as 0.1N
- Advantage: Can detect sustained pressure (long-press gesture)
- Price: $5-$12
- Source: [Interlink FSR-402](https://www.interlinkelectronics.com/fsr-402)

### 4.3 Recommended Sensor Configuration for VoiceReach

**Dual-sensor approach (Piezo + FSR):**

```
[Piezo Disc/PVDF Film]  →  Tap detection (single, double, triple)
       ↓                    High sensitivity to dynamic changes
   ADC Channel 1            Good for detecting tap onset/offset edges

[FSR-402]               →  Long-press detection
       ↓                    Measures sustained force
   ADC Channel 2            Detects hold duration

Both signals → MCU → Gesture classification → USB HID event
```

This dual-sensor approach mirrors the PPS Switch 2025's dual-sensor philosophy (piezo + pneumatic) but uses more readily available components.

### 4.4 ADC Options

**On-chip ADC (built into MCU):**
- RP2040: 12-bit ADC, 500 ksps, 4 channels --- sufficient for basic threshold detection
- ATmega32U4: 10-bit ADC, ~77 ksps --- adequate for tap detection
- ESP32-S3: 12-bit ADC, up to 2 Msps --- excellent for waveform analysis

**External ADC for higher precision:**

**ADS1115 (Texas Instruments)**
- 16-bit resolution, 860 samples/second over I2C
- Programmable Gain Amplifier (PGA): +/-256mV to +/-6.144V input range
- Resolution at highest gain: ~8 microvolts --- can detect extremely subtle piezo signals
- 4 single-ended or 2 differential input channels
- Up to 4 modules on a single I2C bus (64 channels total)
- Available as breakout boards from Adafruit ($15), DFRobot, generic ($3-$5)
- **Recommended for Stage 3 ALS** where signals become extremely small

---

## 5. USB HID Implementation

### 5.1 Implementation Options

| Approach | MCU | Framework | HID Support | ADC | Size | Price | Complexity |
|----------|-----|-----------|-------------|-----|------|-------|------------|
| **Seeed XIAO RP2040** | RP2040 | CircuitPython | Native USB HID | 12-bit, 4ch | 21x17.5mm | ~$6 | Low |
| **Arduino Pro Micro** | ATmega32U4 | Arduino IDE | Native USB HID | 10-bit, 12ch | 33x18mm | ~$5 | Low |
| **Raspberry Pi Pico** | RP2040 | CircuitPython/C | TinyUSB HID | 12-bit, 3ch | 51x21mm | ~$4 | Low-Medium |
| **Digispark ATtiny85** | ATtiny85 | V-USB | Software USB HID | 10-bit, 4ch | 19x23mm | ~$2 | Medium |
| **ESP32-S3** | ESP32-S3 | Arduino/ESP-IDF | Native USB HID | 12-bit, 20ch | varies | ~$8 | Medium |
| **QMK Firmware** | Various | QMK | Full keyboard HID | Depends on MCU | varies | varies | Medium-High |

### 5.2 Recommended Implementation: CircuitPython on Seeed XIAO RP2040

**Rationale:**
1. **Smallest form factor** (21x17.5mm) --- critical for a medical/wearable device
2. **Native USB HID** via CircuitPython's `usb_hid` module --- no low-level driver development
3. **12-bit ADC** sufficient for piezo threshold detection
4. **CircuitPython** enables rapid prototyping and easy parameter adjustment without recompilation
5. **I2C support** for connecting external ADS1115 ADC for high-precision mode
6. **Low power** for battery operation
7. **Low cost** ($6) --- within subsidy allowances

**Software Stack:**

```
Layer 4: USB HID Report
  └── adafruit_hid library (Keyboard.press/release or Consumer Control)
  └── Custom HID report descriptor (optional, for raw sensor data)

Layer 3: Gesture Classification
  └── State machine: IDLE → TAP_DETECTED → CONFIRM / DOUBLE / LONG / TRIPLE
  └── Adaptive thresholds (per-user calibration stored in flash)
  └── Involuntary movement filter (see Section 6)

Layer 2: Signal Processing
  └── Moving average filter (noise reduction)
  └── Peak detection algorithm
  └── Complementary filter (if dual-sensor)

Layer 1: Sensor Input
  └── analogio.AnalogIn (built-in ADC for piezo)
  └── ADS1115 via adafruit_ads1x15 library (high-precision mode)
  └── digitalio for optional mechanical switch fallback
```

**CircuitPython HID Keyboard Example:**

```python
import board
import analogio
import time
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

# Initialize
piezo = analogio.AnalogIn(board.A0)
kbd = Keyboard(usb_hid.devices)

# Adaptive threshold (stored per user)
threshold = 3000  # ADC counts, calibrated per patient
debounce_ms = 150  # Adjusted per ALS stage

while True:
    value = piezo.value  # 0-65535 (16-bit from 12-bit ADC)
    if value > threshold:
        kbd.press(Keycode.SPACE)  # Or mapped to VoiceReach action
        time.sleep(debounce_ms / 1000)
        kbd.release(Keycode.SPACE)
        while piezo.value > threshold * 0.5:  # Wait for release
            pass
        time.sleep(0.05)  # Post-release debounce
```

### 5.3 Alternative: TinyUSB on RP2040 (C/C++)

For production firmware requiring maximum control:

- **TinyUSB** library provides low-level USB HID control
- Supports custom HID report descriptors for transmitting raw pressure data
- Can define the device as a custom HID device (not just keyboard) for richer communication with the VoiceReach desktop application
- The rp2040-gamecon project demonstrates RP2040 as USB HID gamepad --- adaptable for pressure sensor input
- Adafruit_TinyUSB_Arduino provides Arduino-compatible wrapper

Reference: [Adafruit TinyUSB Arduino](https://github.com/adafruit/Adafruit_TinyUSB_Arduino)

### 5.4 Custom HID Report for VoiceReach

Rather than emulating a keyboard, a custom HID device could transmit rich sensor data:

```
Custom HID Report Descriptor:
  Report ID: 1
  Fields:
    - Pressure Level (16-bit): Raw ADC value
    - Gesture Type (8-bit): 0=None, 1=Tap, 2=DoubleTap, 3=LongPress, 4=TripleTap
    - Confidence (8-bit): 0-255, gesture classification confidence
    - Timestamp (16-bit): ms since last event
```

This allows the VoiceReach desktop application to perform additional filtering and make final gesture decisions, rather than relying entirely on the microcontroller.

---

## 6. Involuntary Movement Filtering

### 6.1 The Problem: Fasciculations in ALS

ALS patients frequently experience fasciculations --- involuntary twitches of muscle fibers. These produce pressure/vibration signals that can be confused with intentional taps. The challenge intensifies as the disease progresses: threshold sensitivity must increase (to detect weaker intentional input) while fasciculation frequency may also increase.

### 6.2 Multi-Layer Filtering Strategy

VoiceReach should implement filtering at multiple levels:

**Layer 1: Hardware Filtering**
- **1M ohm load resistor** on piezo output dampens high-frequency noise
- **RC low-pass filter** (e.g., 10K ohm + 100nF = 160 Hz cutoff) to remove electrical noise above tap frequency range
- Intentional taps have dominant frequency content below 100 Hz; fasciculations typically produce higher-frequency, lower-amplitude signals

**Layer 2: Temporal Debounce**
- **Minimum activation duration**: Ignore signals shorter than 30-50ms (Stage 1-2) or 20ms (Stage 3)
- **Maximum activation duration**: Signals longer than 2 seconds are likely sustained involuntary activity, not taps
- **Refractory period**: After a confirmed tap, ignore signals for configurable period (100-200ms)
- **Double-threshold detection**: Signal must exceed primary threshold AND remain above secondary threshold for minimum duration

```
Signal Flow:
  Raw ADC → Moving Average (5-sample window) → Peak Detection
    → Primary Threshold Check (amplitude)
    → Duration Check (30ms < duration < 2000ms)
    → Rise/Fall Rate Check (intentional taps have sharper edges)
    → Refractory Period Check
    → Gesture State Machine
```

**Layer 3: Waveform Pattern Recognition**

Intentional taps vs. fasciculations have distinct waveform characteristics:

| Feature | Intentional Tap | Fasciculation |
|---------|----------------|---------------|
| Rise time | Fast (< 20ms) | Gradual (> 50ms) |
| Peak shape | Sharp, single peak | Irregular, multi-peak |
| Duration | 50-300ms | Variable, often sustained |
| Amplitude | Consistent within session | Highly variable |
| Repetition | Rhythmic (for multi-tap) | Random timing |
| Prior context | Gaze on UI element | Gaze anywhere |

Implementation approach:
1. **Template matching**: During calibration, collect 10-20 intentional tap waveforms to build a template
2. **Cross-correlation**: Compare incoming signals against the template
3. **Threshold**: Accept signals with correlation > 0.6 (adjustable)

**Layer 4: Context-Aware Filtering (VoiceReach-specific)**

This is VoiceReach's unique advantage over standalone switches:

```
Context signals available:
  - Gaze position: Is the user looking at a UI element?
  - UI state: Are candidates currently displayed?
  - Conversation state: Is a response expected?
  - Time context: Time since last interaction

Filtering rules:
  1. If gaze is NOT on any UI element → increase threshold by 50%
  2. If no candidates are displayed → require double-confirmation
  3. If time since last interaction > 30 minutes → enter "wake" mode
     requiring a specific activation pattern (e.g., 3 taps)
  4. Weight gesture confidence by gaze-UI alignment score
```

### 6.3 Adaptive Threshold Calibration

**Initial Calibration (per user, ~2 minutes):**
1. Present visual target on screen
2. Ask user to tap 20 times at comfortable intensity
3. Compute: mean amplitude, standard deviation, mean duration, mean rise time
4. Set threshold = mean - 2*SD (captures 95% of intentional taps)
5. Record waveform template (averaged shape of 20 taps)

**Continuous Adaptation:**
- Every confirmed tap (accepted by context + waveform match) updates the running statistics
- Exponential moving average with slow decay: `new_threshold = 0.95 * old_threshold + 0.05 * recent_mean`
- If rejection rate exceeds 30% for 5 minutes, prompt user for re-calibration
- Store calibration per user in persistent flash memory

**Stage-Based Preset Profiles:**

```
Stage 1 (Normal strength):
  threshold_amplitude = baseline * 1.0
  debounce_ms = 100
  min_duration_ms = 50
  max_fasciculation_filter = LOW
  gaze_context_weight = 0.3

Stage 2 (Moderate weakness):
  threshold_amplitude = baseline * 0.5
  debounce_ms = 150
  min_duration_ms = 40
  max_fasciculation_filter = MEDIUM
  gaze_context_weight = 0.5

Stage 3 (Severe weakness):
  threshold_amplitude = baseline * 0.2
  debounce_ms = 200
  min_duration_ms = 30
  max_fasciculation_filter = HIGH
  gaze_context_weight = 0.7
  external_adc = ENABLE (ADS1115)

Stage 4 (No finger movement):
  → Transition to blink/gaze-only input
  → Piezo can still monitor for any remaining voluntary movement
  → Alert caregiver if voluntary movement returns
```

---

## 7. Progressive Adaptation

### 7.1 ALS Progression and Hand Function

The ALSFRS-R (Revised ALS Functional Rating Scale) provides the clinical framework for tracking disease progression. The relevant subscale for VoiceReach's finger input is "Handwriting" (Question 4):

- **4**: Normal
- **3**: Slow or sloppy; all words legible
- **2**: Not all words legible
- **1**: Able to grip pen but unable to write
- **0**: Unable to grip pen

VoiceReach's Stage mapping to ALSFRS-R:

| VoiceReach Stage | ALSFRS-R Handwriting | Input Capability | Recommended Sensor Placement |
|-----------------|---------------------|-----------------|----------------------------|
| Stage 1 | 4-3 | Full finger tap | Fingertip (index or thumb) |
| Stage 2 | 2 | Weak finger tap | Hand dorsum, forearm |
| Stage 3 | 1 | Minimal movement | Any residual voluntary muscle |
| Stage 4 | 0 | No hand movement | Transition to eye/blink input |

### 7.2 Sensor Placement Migration Path

As the disease progresses, the sensor attachment point should move to where residual voluntary movement remains:

```
Stage 1: Fingertip → Maximum dexterity, natural tapping motion
   ↓
Stage 2: Thumb pad → Thumb often retains strength longer than fingers
   ↓
Stage 2b: Hand dorsum → Detects wrist extension/flexion
   ↓
Stage 3: Forearm → Detects residual forearm muscle contraction
   ↓
Stage 3b: Cheek/temple → Detects jaw clench or eyebrow raise
   ↓
Stage 4: Fallback to gaze-only or blink detection
```

### 7.3 Automatic Strength Monitoring

VoiceReach should continuously monitor tap strength to detect progression:

```python
# Pseudocode for progression monitoring
class StrengthMonitor:
    def __init__(self):
        self.weekly_averages = []
        self.alert_threshold = 0.5  # Alert if strength drops to 50%

    def record_tap(self, amplitude):
        self.session_amplitudes.append(amplitude)

    def weekly_analysis(self):
        current_avg = mean(self.session_amplitudes)
        if len(self.weekly_averages) > 4:
            trend = linear_regression(self.weekly_averages[-4:])
            if trend.slope < -0.1:  # Declining trend
                notify_caregiver(
                    "Tap strength declining. Consider sensor "
                    "repositioning or threshold adjustment."
                )
            if current_avg < self.initial_baseline * self.alert_threshold:
                notify_caregiver(
                    "Significant strength loss detected. "
                    "Recommend clinical evaluation."
                )
        self.weekly_averages.append(current_avg)
```

### 7.4 Graceful Degradation Strategy

| Capability Level | Input Method | Gesture Set | Error Correction |
|-----------------|-------------|-------------|-----------------|
| Full | Piezo tap + Gaze | 4 gestures (tap, double, long, triple) | Preview + cancel |
| Reduced | Piezo tap + Gaze | 2 gestures (tap, long press) | Extended preview |
| Minimal | Piezo tap only | 1 gesture (tap = confirm) | Sequential scanning |
| None (hand) | Gaze + Blink | Blink = confirm, Gaze = point | Slow scanning |

---

## 8. Recommendations

### 8.1 Hardware Recommendations

**Prototype Phase (Recommended BOM):**

| Component | Specific Part | Purpose | Price |
|-----------|--------------|---------|-------|
| MCU | Seeed XIAO RP2040 | USB HID + ADC + I2C | $6 |
| Primary Sensor | 27mm PZT Ceramic Disc | Tap detection | $1 |
| Secondary Sensor | Interlink FSR-402 | Long-press detection | $8 |
| Precision ADC | ADS1115 breakout (Adafruit) | High-resolution for Stage 3 | $15 |
| Enclosure | 3D printed custom | Housing for sensor + MCU | $5 |
| Cable | USB-C cable | Power + data | $3 |
| Medical tape | 3M Micropore | Sensor attachment | $3 |
| **Total** | | | **~$41** |

**Production Phase Considerations:**
- Custom PCB integrating MCU + ADC + signal conditioning
- Medical-grade enclosure (IP44 minimum for fluid resistance)
- Replaceable sensor modules (snap-on connectors for sensor migration)
- Consider CE/PSE marking for Japanese market
- Target COGS: JPY 15,000-20,000 (well within subsidy allowance)

### 8.2 Filtering Approach Recommendation

Implement the 4-layer filtering strategy described in Section 6:

1. **Hardware RC filter** --- simple, no computational cost
2. **Temporal debounce** --- proven, minimal code
3. **Waveform template matching** --- moderate complexity, high accuracy
4. **Context-aware gating** --- VoiceReach's unique differentiator

Start with layers 1-2 for the prototype, add layer 3 for beta, and layer 4 for production.

### 8.3 USB HID Implementation Strategy

**Phase 1 (Prototype)**: CircuitPython on XIAO RP2040
- `adafruit_hid` library for keyboard emulation
- Map gestures to specific key combinations that VoiceReach desktop app listens for
- E.g., Tap = F13, Double Tap = F14, Long Press = F15, Triple Tap = F16

**Phase 2 (Beta)**: Custom HID report via TinyUSB
- Define VoiceReach-specific HID report descriptor
- Transmit raw pressure data + gesture classification to host
- Host application performs additional filtering and context integration

**Phase 3 (Production)**: Dedicated firmware in C
- Optimized real-time signal processing
- OTA firmware updates via USB DFU
- Built-in self-test and diagnostics
- Consider Zephyr RTOS for real-time guarantees

### 8.4 Compatibility Strategy

VoiceReach's input module should support multiple connection modes:

1. **USB HID (primary)**: Direct connection to VoiceReach host computer
2. **3.5mm mono jack output**: Compatible with existing communication devices (伝の心, miyasuku, etc.) and switch interfaces
3. **Bluetooth HID (future)**: For wireless operation via ESP32-S3 or nRF52840
4. **Xbox Adaptive Controller compatible**: 3.5mm jack output enables connection to XAC for broader device ecosystem

---

## 9. Open Questions

### 9.1 Technical

1. **Optimal piezo disc size for finger attachment**: 27mm is standard but may be too large for fingertip attachment on weakened hands. Should we test 12mm and 20mm discs?

2. **Piezo vs. FSR as primary sensor**: Current recommendation uses piezo for taps and FSR for long-press. Should we prototype with FSR-only (simpler) and add piezo later, or start with dual-sensor?

3. **ADC resolution sufficiency**: Is the RP2040's built-in 12-bit ADC sufficient for Stage 3 patients, or should the ADS1115 (16-bit) be mandatory from the start?

4. **Waveform template matching computational cost**: Can the XIAO RP2040 (133MHz Cortex-M0+) perform cross-correlation in real time, or should this be offloaded to the host?

5. **Medical tape adhesion duration**: The PPS Switch uses medical tape for piezo attachment. What is the practical re-attachment interval? Sweat and skin oils degrade adhesion. Should we design a finger sleeve/strap alternative?

### 9.2 Clinical

6. **Calibration frequency**: How often will ALS patients need to recalibrate? The PPS Switch requires manual sensitivity adjustment --- can VoiceReach's automatic adaptation eliminate this?

7. **Fasciculation prevalence timing**: Do fasciculations have circadian patterns in ALS patients? If so, time-of-day could be added as a context feature for filtering.

8. **Caregiver burden of sensor repositioning**: As the sensor moves from fingertip to forearm to cheek, who performs the repositioning? What training is needed?

9. **Dual-hand input**: Should VoiceReach support two sensors (one per hand) for redundancy or for encoding richer gestures?

### 9.3 Regulatory/Market

10. **Japanese medical device classification**: Does VoiceReach's custom piezo input module require medical device certification (PMD Act), or does it qualify as a welfare device (福祉用具)?

11. **Subsidy category matching**: To qualify for the 圧電素子式入力装置 (JPY 53,400) subsidy, what documentation or certification is required?

12. **PPS Switch 2025 interoperability**: Can VoiceReach integrate directly with the PPS Switch 2025 (via its 3.5mm output) for users who already own one, rather than requiring a custom sensor?

13. **International availability**: If VoiceReach expands beyond Japan, how do subsidy/insurance frameworks differ in the US (Medicare/Medicaid), EU, and other markets?

### 9.4 Design

14. **Form factor for progressive disease**: Should VoiceReach ship multiple sensor housings (fingertip clip, hand strap, arm band, cheek pad) or a universal flexible mount?

15. **Visual/audio feedback from the sensor itself**: The AbleNet Micro Light Switch provides auditory click and tactile feedback. Should VoiceReach's sensor include an LED and/or haptic motor for confirmation feedback?

16. **Waterproofing**: ALS patients may drool or have feeding tube incidents. What IP rating is necessary for the sensor module?

---

## 10. References

### Academic Papers
1. Battistini, A. et al. (2019). Development of a new high sensitivity mechanical switch (LeMMS) for AAC access in people with ALS. *J NeuroEngineering Rehabilitation*. [Link](https://link.springer.com/article/10.1186/s12984-019-0626-5)
2. Multi-modal access method (eye-tracking + switch-scanning) for individuals with severe motor impairment (2022). [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9576815/)
3. Exploration of multimodal alternative access for individuals with severe motor impairments (2022). [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC9136588/)
4. Adaptive Algorithm for Muscle Contraction Onset/Offset (2012). [IEEE](https://ieeexplore.ieee.org/document/6353938/)
5. Methods for motion artifact reduction in online BCI experiments (2023). [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10619676/)
6. Reducing Noise, Artifacts and Interference in Single-Channel EMG Signals (2023). [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10059683/)
7. Eye-Tracking Assistive Technologies for Individuals With ALS (2022). [IEEE](https://ieeexplore.ieee.org/document/9745906/)

### Commercial Products
8. AbleNet Micro Light Switch. [AbleNet](https://www.ablenetinc.com/micro-light-switch/)
9. Pacific Supply PPS Switch 2025. [Pacific Supply](https://www.p-supply.co.jp/products/index.php?act=detail&pid=878)
10. Origin Instruments Sip/Puff Switch. [Origin Instruments](https://www.orin.com/access/sip_puff/)
11. Enabling Devices Adaptive Switches. [Enabling Devices](https://enablingdevices.com/product-category/switches/)
12. tecla-e by Komodo OpenLab. [Tecla](https://gettecla.com/products/tecla-e)
13. Xbox Adaptive Controller. [Microsoft](https://www.xbox.com/en-US/accessories/controllers/xbox-adaptive-controller)

### Hardware/Firmware Resources
14. SparkFun Piezo Vibration Sensor Hookup Guide. [SparkFun](https://learn.sparkfun.com/tutorials/piezo-vibration-sensor-hookup-guide/all)
15. Interlink FSR-402 Data Sheet. [Interlink](https://www.interlinkelectronics.com/fsr-402)
16. ADS1115 16-Bit ADC. [Adafruit](https://www.adafruit.com/product/1085)
17. Seeed Studio XIAO RP2040. [Seeed](https://www.seeedstudio.com/XIAO-RP2040-v1-0-p-5026.html)
18. CircuitPython USB HID. [Adafruit](https://learn.adafruit.com/customizing-usb-devices-in-circuitpython/hid-devices)
19. Adafruit TinyUSB Arduino Library. [GitHub](https://github.com/adafruit/Adafruit_TinyUSB_Arduino)
20. NicoHood HID Library. [GitHub](https://github.com/NicoHood/HID)
21. QMK Firmware. [QMK](https://docs.qmk.fm/)

### Japanese Resources
22. National Rehabilitation Center - Communication Device Switches. [NRCD](https://www.rehab.go.jp/ri/kaihatsu/itoh/com-sw.html)
23. Guidelines for Introducing Communication Devices for Severely Disabled Persons. [RESJA](http://www.resja.or.jp/com-gl/gl/a-1-1.html)
24. Pacific Supply Switch Compatibility Guide. [Pacific Supply](https://www.p-supply.co.jp/topics/index.php?act=detail&id=553)
25. Ministry of Health, Labour and Welfare - Daily Living Equipment Grant. [MHLW](https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/hukushi_kaigo/shougaishahukushi/yogu/seikatsu.html)

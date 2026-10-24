# samplerate — R3 Native Audio Driver & 3D Spatial Audio

> **Unfinished R3 audio driver—not a shipped DAW.** These are roadmap targets.
> R2 comprises [vexspoke](#file-vexspoke-md) CPU computation/synchronization and behavior and
> [relational-engine](#file-relational-engine-md) memory/storage/native C search. Migration is staged with
> retained Vexspoke ABI/default allocator. R1 owns lifetimes/residency; GPU DSP
> shaders/dispatch stay [graphvex](#file-graphvex-md). No engine integration, C/Rust atomic layout
> equivalence or automatic schema migration is implied.

> R3 Driver. The native audio device/DSP engine and spatial acoustics engine; the
> DAW application is [impedance](#file-impedance-md) (R5).
> Design target: Sub-millisecond latency, zero-drop realtime playback, zero steady-state heap allocations.
> Laws: Audio Thread Isolation (Lock-free RingBuffer, no locks, no malloc), Hot-Swappable DSP Modules, Native Driver Seams (CoreAudio/WASAPI direct).

---

## 🎯 Tier-0 Integration Proofs (Ground Truth)

*The live binary is the final judge. This table gates the repo headline — never the rows below, which keep their own independent truth. Statuses are re-verified, never copied from memory.*

| Proof Binary | End-to-End User Verification | Status | Evidence |
|---|---|:---:|---|
| `samplerate_boot` (no target) | Launch → realtime thread runs with zero drops while UI redraws | 🟥 | First `src/` slice compiles (format/buffer/stream + RE arena); no runnable binary, no hardware proof |

## The Samplerate Standard: The Zero-Drop Bare-Metal DAW

Samplerate rejects sluggish Electron wrappers, bloated C++ audio frameworks, and audio engines that glitch when the user interface redraws. It builds a high-performance C23 audio workstation with a dedicated lock-free realtime thread, hot-reloadable DSP plugins, and immersive 3D binaural audio:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                           THE SAMPLERATE STANDARD                                │
├─────────────────────────┬─────────────────────────┬──────────────────────────────┤
│ 1. Realtime Core Engine │ 2. Hot DSP Modules      │ 3. Darling Retained Mixer    │
│ • Lock-free RingBuffer  │ • Hot-reloadable voices │ • Retained hardware strips   │
│ • Zero-allocation loop  │ • Hot-reloadable effects│ • VU meters via HudBar       │
│ • Fixed 128/256 quantums│ • Saw/FM/Wavetable synth│ • Gain faders & pan dials    │
│ • Sample-accurate clock │ • Parametric EQ/Reverb  │ • Zero UI-thread audio drop  │
├─────────────────────────┴─────────────────────────┴──────────────────────────────┤
│ 4. Interactive Piano Roll + 3D Binaural HRTF Acoustics + MIDI Engine             │
│ • Piano roll note grid with velocity lanes and quantize snapping (1/4..1/32)     │
│ • Multi-lane parameter automation with bezier curve interpolation               │
│ • 3D spatial audio: listener orientation, point emitters, HRIR convolution,     │
│   inverse-square distance rolloff, and Doppler frequency shifting                │
│ • Direct hardware CoreAudio / WASAPI backends + USB MIDI device support          │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## Status Legend & Grading Standards

Every subsystem and mini-achievement is strictly graded based on the current reality of the codebase, test suites, and live runtime behavior:

| Emoji | Level | Definition |
|:---:|:---|:---|
| 💚 | **98% Done** | Basically 98% done: fully wired, compiles, runs, production-ready, actively polished |
| 🟩 | **95% Done** | Implemented & functional: wired, compiles and runs, minor polish remaining |
| 🟨 | **85% Done** | Substantially implemented: core works or has tests proving behavior, missing specific features/edge cases |
| 🟧 | **75% Done** | Partial implementation: core struct/concept exists, but major features missing or unwired |
| 🟥 | **Concept / Draft** | Still a concept or spec'd in docs/headers only, zero working source |
| ⬜ | **Vital Future Work** | Not implemented yet, but vital roadmap feature (+1 on the feature) |

---

## High-Level Subsystem Summary

| # | Subsystem | Scope Summary | Overall Status |
|:---:|:---|:---|:---:|
| 1 | `Realtime Audio Core` | Lock-free audio loop, fixed frame quantums, sample clock, zero malloc | 🟥 |
| 2 | `Hardware Driver Backends` | CoreAudio (`audio_cocoa.m`), ALSA, WASAPI, 60s sine proof | 🟧 |
| 3 | `Dynamic Voice Synthesis` | Hot-reloadable voice ABI (`voice_saw.dylib`), FM, Wavetable synthesis | 🟥 |
| 4 | `Dynamic DSP Effects` | Hot-reloadable effect ABI, 4-band EQ, Delay, Reverb, Compressor | 🟥 |
| 5 | `Multi-Track Mixer Console` | Channel strips, Master bus, Gain faders, Pan dials, Mute/Solo, VU meters | 🟥 |
| 6 | `Piano Roll & Sequencer` | Note grid, velocity lanes, quantize snapping (1/4..1/32), MIDI editing | 🟥 |
| 7 | `Parameter Automation Lanes` | Time-series automation curves, cubic bezier nodes, parameter read/write | 🟥 |
| 8 | `3D Spatial Audio & HRTF` | 3D listener, point emitters, HRIR convolution, Doppler shift, distance rolloff | ⬜ |
| 9 | `Audio File I/O & Streams` | Zero-alloc streaming WAV reader/writer, shell-out ffmpeg transcoding | ⬜ |
| 10 | `MIDI Hardware Integration` | USB MIDI device enumeration, packet decoding (Note On/Off/Velocity) | ⬜ |

---

## Detailed Mini-Achievements Breakdown

### 1. Realtime Audio Core & Render Quantum

The deterministic, zero-allocation audio execution loop.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 1.1 | Dedicated Realtime Audio Thread | High-priority thread isolated from UI and OS event queues | 🟥 |
| 1.2 | Lock-Free RingBuffer Communication | SPSC ring buffer transferring audio blocks between UI and audio threads | 🟨 |
| 1.3 | Fixed Render Quantum Processing | Processing audio in deterministic 128 / 256 / 512 frame blocks | 🟥 |
| 1.4 | Zero Steady-State Heap Allocations | Pre-allocated audio buffers and DSP scratch memory via `BitPool` | 🟥 |
| 1.5 | Monotonic Sample Clock | Sample-accurate timebase counter tracking global playback position | 🟥 |
| 1.6 | Transport Controls & Playback State | Play, Pause, Stop, Loop, Rewind, and Scrubbing transport API | 🟥 |

### 2. Hardware Audio Driver Backends

Direct hardware driver integration without intermediate translation overhead.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 2.1 | Native macOS CoreAudio Bridge | `platform/audio_stream_cocoa.m` binding a default-output `AudioUnit`; compiles, device output unproven | 🟧 |
| 2.2 | 60-Second Sine Wave Glitch Proof | Headless test suite playing continuous 440Hz sine without underruns | 🟥 |
| 2.3 | Buffer Underrun & Overrun Detect | Real-time drop detection counting missed hardware buffer deadlines | 🟥 |
| 2.4 | Linux ALSA / PulseAudio Backend | Native Linux audio driver implementation | ⬜ |
| 2.5 | Windows WASAPI Exclusive Backend | Native Windows WASAPI driver implementation | ⬜ |

### 3. Dynamic Voice Synthesis (`../hotcwap`)

Hot-reloadable synthesizer instruments.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 3.1 | Voice Module ABI Contract | `Voice_render(voice, buffer, frames)` exported by dynamic libraries | 🟥 |
| 3.2 | Band-Limited Sawtooth Oscillator | `voice_saw.dylib` generating anti-aliased sawtooth waves (PolyBLEP) | 🟥 |
| 3.3 | Multi-Waveform Basic Synth | Square, Triangle, Sine, and Noise generator modes with pulse-width control | 🟥 |
| 3.4 | ADSR Envelope Generator | Attack, Decay, Sustain, Release envelope generator with exponential curves | 🟥 |
| 3.5 | Resonant Lowpass / Highpass Filter | 12dB/24dB state-variable filter with cutoff and resonance controls | 🟥 |
| 3.6 | 2-Operator FM Synthesizer | Modulator-carrier frequency modulation synthesis engine | ⬜ |
| 3.7 | Wavetable Synthesis Engine | Scanning wavetable oscillator with custom waveform interpolation | ⬜ |

### 4. Dynamic DSP Effects & Audio Processing

Hot-reloadable effects processing pipeline.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 4.1 | Effect Module ABI Contract | `Effect_process(fx, buffer, frames)` exported by dynamic libraries | 🟥 |
| 4.2 | 4-Band Parametric Equalizer | Low shelf, two parametric peaking bands, and high shelf filter | 🟥 |
| 4.3 | Stereo Ping-Pong Delay | Tempo-synced delay line with feedback damping and stereo spread | 🟥 |
| 4.4 | Algorithmic Reverb Tank | Freeverb-style comb and all-pass filter tank with room size and decay | 🟥 |
| 4.5 | Dynamic Range Compressor / Limiter | Threshold, ratio, attack, release, and hard knee peak limiting | 🟥 |
| 4.6 | Tube Saturation & Overdrive | Soft-clipping hyperbolic tangent (`tanh`) distortion module | 🟥 |
| 4.7 | GPU Multi-Layer Audio Mix Compute | 8-layer stereo mix compute shader (`vulkan/audio_mix.comp`) | 🟧 |

### 5. Multi-Track Mixer Console

Retained mixer strips built directly on Darling widgets.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 5.1 | Track Channel Strip Layout | Vertical mixer strip layout hosting fader, pan, solo/mute, and FX slots | 🟥 |
| 5.2 | Volume Fader via Darling `Slider` | High-resolution logarithmic dB gain slider (-inf to +6dB) | 🟥 |
| 5.3 | Rotary Pan Control via `Knob` | Linear/equal-power stereo pan rotary dial | 🟥 |
| 5.4 | Mute & Solo Toggles via `Switch` | Exclusive solo and instant track muting logic | 🟥 |
| 5.5 | Fast Peak & RMS VU Meters | Responsive vertical meter bars with peak-hold tick indicators | 🟥 |
| 5.6 | Auxiliary Send & Return Busses | Routing track sends to shared reverb and delay aux buses | 🟥 |
| 5.7 | Master Bus Channel Strip | Final master output fader with brickwall limiter | 🟥 |

### 6. Interactive Piano Roll & Sequencer

Note event editing and musical sequencing.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 6.1 | Musical Pitch & Time Grid | Vertical semitone keys (C-1 to G9) × horizontal bar/beat timeline | 🟥 |
| 6.2 | Note Event Placement & Resizing | Clicking to spawn notes, dragging edges to adjust duration | 🟥 |
| 6.3 | Note Velocity Editor Lane | Bottom velocity bar drawer adjusting per-note velocity (0..127) | 🟥 |
| 6.4 | Grid Quantization Modes | Snapping note starts and lengths to 1/4, 1/8, 1/16, 1/32, and triplets | 🟥 |
| 6.5 | Multi-Note Selection & Transpose | Drag-selection box; arrow keys transposing notes up/down semitones | 🟥 |

### 7. Parameter Automation Lanes

Continuous parameter control curves.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 7.1 | Track Parameter Automation Drawer | Collapsible lanes underneath track for filter cutoff, volume, and pan | 🟥 |
| 7.2 | Cubic Bezier Curve Nodes | Placing automation points with adjustable curve tension handles | 🟥 |
| 7.3 | Real-Time Parameter Interpolation | Audio thread reading smoothed parameter values per frame block | 🟥 |
| 7.4 | Automation Modes (Read / Write) | Recording live knob adjustments into automation points during playback | 🟥 |

### 8. 3D Spatial Audio & Binaural HRTF

Immersive acoustic simulation for game audio and spatial mixing.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 8.1 | 3D Listener Orientation & Transform | Position, forward vector, and up vector representing player ears | ⬜ |
| 8.2 | 3D Point Sound Emitters | World-space 3D audio sources with spherical radiation patterns | ⬜ |
| 8.3 | Distance Inverse-Square Rolloff | Physically accurate volume falloff with minimum/maximum clamp ranges | ⬜ |
| 8.4 | Doppler Frequency Shift | Dynamic pitch modulation based on relative velocity between source and listener | ⬜ |
| 8.5 | Binaural HRIR Convolution Engine | Time-domain FIR convolution applying Head-Related Impulse Response tables | ⬜ |
| 8.6 | Acoustic Obstacle Occlusion | Lowpass filtering sound sources obstructed by geometry | ⬜ |

### 9. Audio File I/O & Streaming

Asset loading and recording pipelines.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 9.1 | Zero-Allocation WAV/PCM Reader | Streaming 16/24/32-bit WAV audio files directly from memory-mapped files | ⬜ |
| 9.2 | High-Speed Master Render Exporter | Rendering mixdown directly to disk at maximum CPU speed | ⬜ |
| 9.3 | Shell-Out ffmpeg Transcoding | Invoking `ffmpeg` via `ProcessSpawn` to export MP3, FLAC, and OGG formats | ⬜ |

### 10. MIDI Hardware & Device Integration

External keyboard and controller support.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 10.1 | macOS CoreMIDI Device Enumeration | Detecting connected USB MIDI keyboards and synthesizers | ⬜ |
| 10.2 | Raw MIDI Packet Parser | Decoding Note On, Note Off, Pitch Bend, and CC messages | ⬜ |
| 10.3 | Virtual On-Screen Keyboard | Typing on computer QWERTY keyboard to trigger musical notes | ⬜ |
| 10.4 | MIDI Learn Parameter Mapping | Right-clicking a Darling knob to bind it to a hardware MIDI CC knob | ⬜ |

---

## Strategic Implementation Priorities for Samplerate

1. **P0: CoreAudio Sine Wave Proof**
   - Finalize `audio_cocoa.m` CoreAudio bridge.
   - Run the 60-second headless sine wave test (`audio_test`) proving glitch-free playback without memory allocations.

2. **P1: The Voice Module Contract & Saw Synth**
   - Implement the `Voice_render` dynamic library interface.
   - Author `voice_saw.dylib` with PolyBLEP band-limited synthesis.

3. **P2: Darling Mixer Strip Integration**
   - Assemble a 4-channel mixer strip using Darling `Slider` (volume) and `Knob` (pan).
   - Wire mixer values to the realtime audio thread via lock-free rings.

4. **P3: Piano Roll & Note Sequencing**
   - Implement the interactive 2D note grid for triggering synthesizer voices.

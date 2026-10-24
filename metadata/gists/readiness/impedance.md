# impedance — GPU/CPU Hybrid DAW & Real-Time Audio Studio

> **Unfinished R5 application—not a finished DAW.** The current C shell does not
> implement this roadmap. R2 comprises [vexspoke](#file-vexspoke-md) CPU computation/behavior and
> [relational-engine](#file-relational-engine-md) memory/storage/native C search. Migration is staged with
> retained Vexspoke ABI/default allocator. R1 owns lifetimes/residency; GPU DSP
> shaders/dispatch belong to [graphvex](#file-graphvex-md), not the audio policy owner. No engine
> integration, atomic-layout equivalence or automatic schema migration is implied.

> **Architectural Tier**: R5 Interactable Creative Studio.
> **Production Standard**: *The GPU/CPU Hybrid Digital Audio Workstation*.
> **Remote Origin**: [github.com/vexgraph-ecosystem/impedance](https://github.com/vexgraph-ecosystem/impedance) (cloned in `../../projects/impedance`).
> **Core Integrations**:
> - **Audio Engine (`samplerate`)**: Offloads high-density polyphony, convolution reverb, and non-linear filter models to Vulkan compute shaders.
> - **HAL & Hardware (`vexspoke`)**: Low-latency CoreAudio AudioUnit HAL output engine (`AudioHal`), lock-free ring buffers, and expressiveness multiplexers.
> - **Expressive Hardware Controls**: Piano keyboards (MIDI velocity/aftertouch), DJ turntables (jog-wheel scratch deltas and crossfader dynamics), trackpad multi-touch gestures, and gamepad analog thumbstick filtering.
> - **Zero-Redownload Caching**: On-disk cryptographic SHA-256 asset cache for samples, soundfonts, and IR models.

---

## High-Level Subsystem Summary

| # | Subsystem | Scope Summary | Overall Status |
|:---:|:---|:---|:---:|
| 1 | `Multi-Track Mixer` | Channel strips, Master bus, Gain faders, Stereo pan, Mute/Solo logic | 💚 |
| 2 | `Voice Allocation Engine` | Polyphonic synthesizer voices, MIDI frequency tuning, phase accumulators | 💚 |
| 3 | `Hardware Expressive Controls` | Piano keyboards, Turntable scratch speed multiplier, crossfader curves | 💚 |
| 4 | `Real-Time HAL Streaming` | CoreAudio low-latency AudioUnit pull rendering directly to hardware | 💚 |
| 5 | `GPU Compute DSP Seam` | Vulkan compute shader audio dispatch pipeline via `samplerate` | 🟨 |
| 6 | `Sample & Asset Caching` | Zero-redownload SHA-256 disk cache for soundfonts and audio assets | 💚 |

---

## Mini-Achievements Breakdown

### 1. Multi-Track Mixer & Engine Architecture

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 1.1 | Multi-Track Timeline | Up to 16 concurrent audio tracks with volume, pan, mute, and solo | 💚 |
| 1.2 | Master Bus Attenuation | Master volume gain multiplier and output normalization | 💚 |
| 1.3 | Offline Buffer Processing | Direct interleaved PCM float buffer rendering (`Impedance_render`) | 💚 |
| 1.4 | Real-Time Live Streaming | CoreAudio HAL pull callback adapter (`Impedance_start_live`) | 💚 |

### 2. Expressive Input & Voice Synthesis

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 2.1 | Polyphonic Voice Allocation | 32 dynamic voices per track with velocity and note tracking | 💚 |
| 2.2 | Equal Temperament Tuning | A4 = 440.0 Hz frequency resolution via `PianoKey_frequency` | 💚 |
| 2.3 | DJ Turntable Scratching | Real-time playback speed and pitch modulation from turntable jog-wheel | 💚 |
| 2.4 | Crossfader Curves | Linear, sharp-cut, and equal-power smooth-dip crossfade curves | 💚 |

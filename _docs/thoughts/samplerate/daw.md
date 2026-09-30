# DAW (the bare-metal studio)

**Idea (in vexgraph's words):** a DAW built on the vex stack — tracks,
piano roll, mixer, and effects with the same retained-mode UI tree as
everything else. No JUCE, no Electron shell around a web view.

## Why the stack wants this
- **vexspoke audio seam exists** (`audio_stub.c` + `audio_cocoa.m`): the
  backend slot is cut, only silence lives there now. A real engine
  (sample clock, mixer graph, lock-free ring to the render thread) fills
  it without touching callers.
- **Knob/Slider/Switch shells exist** (darling `field/` + `button/`):
  mixer strips and plugin params are already data-defined — behavior
  (drag → value → callback) is the only missing half.
- **Sequencer/CurveEditor shells exist** (darling `../../tools` plan): piano
  roll and automation lanes are curve/sequence editing with a time axis.
- **hotcwap** = instruments and effects as reloadable modules: tweak a
  synth voice without stopping playback. The driver pattern from
  `/Users/vexgraph/CLionProjects/vexgraph/_docs/_thoughts/darkbase/database-switchboard.md`, reused a third time (`voice_saw.dylib`).
- **Legacy reference (thin):** `_legacy-java/src/audio/` holds exactly
  one file — `vulkan/audio_mix.comp`, an 8-layer stereo mix shader
  (per-layer gains, hard clip). No engine, no MIDI, and `src/daw/` is
  an empty placeholder. Useful as the GPU-mix target shape, not as
  a port source. No audio lessons exist in `_lessons/`.

## Constraints (sized honestly)
1. Audio engine first, UI second. Glitch-free playback needs a realtime
   thread with zero allocation (`RingBuffer` + `BitPool` already exist
   for exactly this). No UI work until a sine survives 60 seconds.
2. MIDI/file I/O rides the shell-out philosophy: import/export via
   terminal tools where possible, native decoders only for the hot path.
3. Latency budget decides the backend: CoreAudio/AAudio direct; never
   through a translation layer (the MoltenVK lesson, applied to audio).

## Sequencing
1. Real-time mixer core in vexspoke audio (sine → 60 s clean).
2. Instrument/effect module contract (`Voice_render/...`) + one synth.
3. Piano roll on Sequencer shell, mixer strips on Knob/Slider shells.
4. Arrangement timeline, then file formats.

## Status
Envisioned, not started. Seams in place (audio stub, knob/slider shells);
no mixer core, no voice contract.

## Next step
After the drawing app proves the darling input loop, spec the mixer
core: struct fields, render quantum, ring discipline.

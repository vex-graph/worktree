# Video viewer (VideoPanel + frame renderer)

**Idea:** a darling `Panel` node that plays video: `play/pause/seek`,
frame-accurate display, fit-not-stretch framing like `Picture`/`Object3D`.
The renderer turns decoded frames into GPU textures (`Texture_loadRaw`
today, IOSurface video path later) and stamps the current frame as a quad
each present. Audio is explicitly out of scope for v1 (mute motion first).

## Why this is the biggest of the four

- **No decoder exists in the tree.** Buffers, fonts, `Texture`, SDF, scenes
  exist — video decode (h264/vp9/av1, container parsing, seeking) does not.
  This thought is honest about that: the node design and the decoder are
  two separate projects, and the node must not wait for a native decoder.
- **Framing is solved, timing is not.** Display reuses the known fit law
  (uniform scale, center, letterbox — same as `Object3D`). The hard parts
  are frame clock vs vsync, seek latency, memory pressure (1080p RGBA is
  ~8 MB/frame — prefetch ring, not "load all frames"), and teardown
  (decoder thread joined before surfaces die, Rule 26/27 discipline).

## API sketch (not final)

```c
typedef struct VideoPanel {
    Panel base;            // viewport; frame stamps inside
    char path[...];        // inline media path (VFS uri); empty = blank panel
    double durationSec;    // total length (0 = unknown yet)
    double clockSec;       // current presentation time
    bool playing;          // transport state
    bool muted;            // v1: always true (no audio path yet)
    float frameRate;       // source fps (0 = unknown)
} VideoPanel;
// VideoPanel_0() / VideoPanel_1(parent)
// setSourcePath (VFS resolve + probe duration + dirty) / clearSource
// play() / pause() / toggle() / seekTo(sec) (clamped 0..duration)
// getDuration / getClock / isPlaying / getFrameRate
// No setFrame — frames arrive from the decoder, never from callers.
```

## Renderer shape

1. **v1 — shell-out frames (like drawing-app's PNG advice).** `ffmpeg`
   decodes/seeks to PNG/RGBA frames; darling uploads via `Texture_loadRaw`
   and stamps the current frame as a `texture_quad`. Proves transport
   (play/pause/seek), clock, fit framing, and teardown with zero decoder
   code in-tree.
2. **v2 — piped decoder.** `ffmpeg` stdout-piped raw frames into a bounded
   prefetch ring (3–5 frames); upload on present; drop-degrade on stall
   (keep old frame, Rule 27 spirit).
3. **v3 — native decode (only if v2 hurts).** Platform decoders
   (VideoToolbox/v4l2) or an in-tree codec. Not designed here — v2 decides
   whether v3 is ever needed.

## Constraints (sized honestly)

1. **Mute v1.** No audio routing, no A/V sync. Motion + transport first.
2. **Bounded everything.** Prefetch ring cap, 100ms-bounded waits, decoder
   thread joined before `Texture`/surface teardown. A hung decode must
   drop frames, never park the window.
3. **VFS sources.** Same as models/fonts: `anti://`, `project://` uris.
4. **License hygiene.** ffmpeg is a shell-out tool here, not linked code —
   no codec GPL surface inside the tree at v1/v2.

## Sequencing

1. `VideoPanel` shell: struct + transport state + fit framing over a
   *single* still frame (proves display without time).
2. Clock + play/pause/seek over an ffmpeg frame sequence (v1 renderer).
3. Prefetch ring + piped decode (v2), gallery section with 1 short clip.
4. Native decode evaluation — only on measured v2 pain.

## Status

Envisioned, not started. Do last of the four: it needs the least from
darling and the most from outside it.

## Next step

`VideoPanel` still-frame shell (one PNG via shell-out, fit-stamped).
If transport + framing feel right on a still, add time.

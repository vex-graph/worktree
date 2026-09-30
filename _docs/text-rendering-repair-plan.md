# Text rendering repair plan (approved)

## Background

The Vulkan text atlas now selects the correct glyph cell, but the visible
glyphs are inverted and soft. The demo seconds value is written by a worker;
the label pulls that value only during painting. Its demand probe polls on the
owner thread every loop step, rather than being woken by the worker.

## Proposed changes

### Graphvex: glyphs and scheduler

- Check the CoreText bitmap rows with an asymmetric glyph; correct the glyph-only
  row orientation in `src/objc/font_cocoa.m`, leaving image quads and the shared
  image shader unchanged. Add an orientation-specific test.
- Rasterize atlas cells at backing-scale native resolution while preserving
  24-point intended glyph size. Handle backing-scale changes and GPU texture
  cache ownership before replacing the atlas; do not destroy a texture that an
  in-flight frame still references. Consider cell gutters/inset UVs to prevent
  linear filtering across adjacent characters. Keep image sampling unchanged.
- In `src/graphics/graphics_loop.c` and its public contract, accept coalesced
  producer wake tickets without accessing the unsynchronized client registry
  from the worker. Consume existing dirty state before presentation and retain
  any concurrent new request; re-arm on failed/deferred present. Keep all
  registry updates, frame callbacks and GPU work on the owner thread, and all
  waits bounded with a cancel/termination predicate.

### Local demo

- In `main/test_suite.c`, publish a wake ticket after `Reactive_set`, leaving
  `Reactive_set` itself a leaf-level atomic operation. Owner-thread probe still
  compares values and marks its specific frame dirty. Bound the worker's sleep
  interval for responsive shutdown. Preserve present-on-demand (no constant
  animation or GPU presents while unchanged).

### Darling / vexspoke

- Follow-up finding: `presentsWithTransaction=YES` needs an enclosing
  Core Animation transaction for content-only updates. Wrap Frame's
  render/present hook with balanced platform Begin/End in `darling/frame.c`,
  `objc/frame_cocoa.m`, and `darling/frame_stub.c`. The reactive remains
  independent of graphics.

## Trade-offs / open questions

- A still screenshot cannot prove the counter never changes. Instrument elapsed
  values, probe calls, dirty consumption, and successful presents to separate
  an unwoken poll from a failing present or an actual lost request.
- Prefer 24 logical points rasterized at the current native scale (rather than
  shrinking text to 24 hardware pixels). Nearest filtering would hide blur but
  give visibly pixelated text; scale-aware rasterization keeps smooth edges.
- A scheduler wake needs a race-free timed-wait predicate and a safe shutdown
  path; a direct cross-thread `Frame_markDirty` is not safe with the current
  resizable client registry.

## Verification

- Build Graphvex and the demo with `-Wall -Wextra -Werror`; run text draw,
  graphics-loop, and frame/pipeline tests on the configured Vulkan backend.
- Assert an asymmetric glyph is upright, has stable coverage at 1x/2x, and
  does not sample an adjacent atlas cell. Verify a scale change still renders.
- Test worker notification during idle and during a present, shutdown with a
  sleeping worker, and zero additional presents while the value is unchanged.
- Manually inspect the live counter at 1x/Retina (upright, sharp, increments
  without interaction), recording any environment-dependent limitations.

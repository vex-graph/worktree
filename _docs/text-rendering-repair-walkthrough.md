# Text rendering repair walkthrough

- **Orientation:** CoreText's bitmap bytes were already top-down. Removed the
  extra row reversal in `graphvex/src/objc/font_cocoa.m`; tested the asymmetric
  `F` at 24 and 48 native pixels.
- **Sharpness:** `graphvex/src/vulkan/vk_graphics.c` now rasterizes a 24-point
  glyph at backing resolution, keeps transparent one-texel gutters, and rebuilds
  the atlas on a display-scale change only after the prior GPU submission has
  completed. Other image sampling and shader coordinates are unchanged.
- **Reactive demand:** `GraphicsLoop_notify` provides a coalesced, thread-safe
  wake ticket. The demo's worker sets the reactive and wakes the runner; the
  owner-thread probe marks the right frame dirty. The worker's sleep is bounded
  in 100 ms slices. Dirty demand is consumed before presentation so concurrent
  or callback-initiated marks are not lost; failed presents re-arm demand.
- **Visible repaint follow-up:** The demo's tick now posts an explicit repaint
  ticket, even if its value matches a previous one. Graphvex preserves a
  completed frame through same-size resize and retires a deferred present
  before recording into the same Vulkan source image again. Darling wraps the
  whole frame in a Core Animation transaction; its `presentsWithTransaction`
  seam otherwise leaves content-only changes off-screen.
- **Tests:** Built `graphvex` and `vk_test` with the configured
  `-Wall -Wextra -Werror`. All 14 Graphvex CTests passed, including glyph
  orientation/1x–2x atlas tests and worker-notify/reentrant-demand tests.
  `git diff --check` passed. A Retina `vk_test` run at 1600x1200, scale 2.0,
  logged `seconds: 0`, `1`, `2`, `3`, `4`, `5`, `6` in its paint callback;
  the extended frame trace reported a successful present for each value.
  Window-targeted captures visibly changed from `seconds: 0` to `seconds: 4`.
  The temporary demo process was terminated after observation.
- **Limit:** Window captures establish an actual displayed content change, but
  do not measure or guarantee exact one-second display latency. Label AUTO
  sizing still uses fixed-width metrics while Vulkan uses proportional glyph
  advances; longer text may wrap differently and deserves a separate change.

No commits or pushes were made. Pre-existing unrelated uncommitted changes
throughout the workspace were retained.

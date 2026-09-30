# Retained-Board Overhaul — Implementation Plan

## Background / Motivation

The demo window ("Darling UI Probe", dark root + Input + Button + Label) is
blank at first and never renders correctly, even after heavy resizing. Two
confirmed defects:

1. **First-present race (white launch).** The content board's CAMetalLayer is
   attached inside the first `GfxLoop_step` — after CoreAnimation already
   emitted the fresh window's first display pass. Present-on-demand then
   rests forever (tree clean, panes clean) — white until a resize creates
   demand.
2. **Frame-never-tracks-resize.** `Window_orderLayers` (the only layer framer)
   runs only when a board slot pointer *changes* (once at attach).
   `PanelCocoa_setSize` updates `drawableSize` + swapchain extent only —
   never the layer `frame`. The board content stays locked at 800x600 pts
   top-left while the window grows: "resize a lot, still partial/wrong".
3. **Idle seam.** The window-seam swapchain (the one Vulkan drawable that
   naturally tracks window size) is never presented (`present=0`); the app
   presents per-pane CAMetalLayers instead.

## User's approved model

- **One on-screen Metal layer**: the Frame's CAMetalLayer canvas (the seam
  swapchain). It resizes WITH the window (native CA autoresizing + explicit
  Native Pixel Law drawableSize), rebuilt by the existing Vk swapchain path.
- **scenePanel (bottom) and contentPanel (top)** stay bare panels but become
  the two CONCEPTUAL layers: retained offscreen rendering targets (VkLayer =
  dual-flight VkImage chains, FIXED physical px, never rebuilt during
  resize), composited by the seam pass in z-order — scene below, content
  above.
- GfxLoop remains the metadata/demand manager; the graphics loop (thread 0,
  `presentFrameLocked`) drives the Vulkan renderer.

## Mechanism reuse (zero new GPU machinery)

- `VkLayer` (graphvex vk_layer.c): retained offscreen target — register/
  resize/unregister, per-chain dual flight slots + semaphores + bounded 100ms
  fences, `VkLayer_visit` (render dirty layers, publish) and
  `VkLayer_composite` (sample last-published image into a render-pass-
  compatible BGRA8 pass). `VkLayer_visit` currently has ZERO call sites —
  this overhaul is its first driver.
- `Darling_layerRender` (:268) already has the board branch (backdrop fill +
  children with paintUI=true) and is already wired to `VkLayer_setRenderer`
  (:637); board pixel/point scale contract intact via `Darling_getPanelSize`.
- Seam pass `s_drawablePass` + `s_frameRenderer` (`Darling_renderFrame`) +
  `s_preFrameRenderer` (`Darling_preFrame`) already exist; `VkPane_count()==0`
  already routes presents to the seam chain (`Vk_clearPresent`).
- `Darling_attachLayers` already registers COMPOSITED scenes as VkLayers
  (unchanged); plain widgets never become panes (gate at panel_bridge.c:237).

## File changes by repo (upstream-first commit order)

### graphvex (1 commit)
- `feat(vk_layer): add VkLayer_hasDemand demand probe`
  - vk_layer.h/.c: `bool VkLayer_hasDemand(void)` — mirror of
    `VkPane_hasDemand` (vk_pane.c:212): true if any active chain is dirty
    (registration/resize arm it; tree dirt propagates via
    `VkLayer_markDirty`). Overview update same commit.

### darling-framework (4 commits)
1. `feat(panel_cocoa): boards become retained offscreen VkLayer targets`
   - `PanelCocoa_newBoard`: `VkLayer_register(pxW, pxH, panel)` instead of
     CAMetalLayer + `VkPane_register`. No CALayer is created or stored for
     boards; `isBoard` stays; `chain` field now stores the layer index
     (getter name keeps `PanelCocoa_chain` for the pane contract).
   - `PanelCocoa_setSize`: boards route to `VkLayer_resize` (no-op on
     unchanged extent — Pane-of-Glass Law); no drawableSize update.
   - `PanelCocoa_layer`: boards return nullptr (nothing to parent).
   - `PanelCocoa_free`: boards unregister via `VkLayer_unregister`.
   - PANES (`newMetal`) untouched: DIRECT scenes keep CAMetalLayer + VkPane.
2. `feat(panel_bridge): boards attach as retained VkLayers; no board layers`
   - `Darling_attachPanelBoards`: ensure/resize the board VkLayer per panel
     via the PanelCocoa path; DELETE the `Window_setTopLayer`/`setBottomLayer`
     parenting block (PanelCocoa_layer is null for boards; the seam layer is
     the Frame's contentView layer and lives in the tree natively).
3. `feat(compositor): seam pass composites retained boards; preFrame visits`
   - `Darling_preFrame`: after board ensure + pane/layer propagate, call
     `VkLayer_visit()` (thread 0, same cadence as present) so dirty boards
     render and publish BEFORE the seam pass samples them; clear-color
     refresh unchanged.
   - `Darling_renderFrame` (seam frame renderer): composite the scene board
     layer first (bottom), then the content board layer (top), each at full
     drawable extent via `VkLayer_composite(cb, drawW, drawH, idx,
     0,0,drawW,drawH, tint...)`; keep painting non-board root children for
     board-less frames. The board-backed early-return is retired.
   - Probe `darlingGfxFrameFn`: demand OR-chain gains `VkLayer_hasDemand()`.
   - `;;OVERVIEW` + `_docs/darling.md` compositor/board sections SAME commit
     (Living Darling Docs Law).
4. `fix(frame_cocoa): explicit Native Pixel Law on the seam layer`
   - At attach AND on `frameCocoaResizeHook`: `contentsScale` =
     backingScaleFactor; `drawableSize` = bounds*scale (physical px);
     `geometryFlipped = YES`; `presentsWithTransaction = YES`; keep
     autore sizingMask. Feeds `s_extent` to the seam swapchain rebuild —
     the resize tracking the old board layers lacked.

### vexspoke (docs, same cycle)
- preferences.md — amend the Window Compositing Layer Order Law (Tier 1) per
  the Conflict Triage Law managed exception: canonical stack = blur view +
  ONE window CAMetalLayer canvas + TWO retained offscreen board targets
  (VkLayer, fixed px) composited in Vulkan z-order (scene bottom, content
  top); DIRECT panes remain the managed exception; Present-On-Demand and
  Native Pixel Law unchanged. Commit in vexspoke repo.

## Behaviors preserved (law map)

- Present-On-Demand: seam presents only on demand (probe now sees tree dirt,
  live resize, pane demand, layer demand, caret).
- Pane-of-Glass: DIRECT scenes keep their own CAMetalLayer + swapchain.
- Continuous Real-Time Live Resize: boards are FIXED px (never rebuild
  mid-drag); seam layer re-frames natively by CA; preFrame layout re-runs
  every tick; pinned children track edges.
- Native Pixel Law: explicit drawableSize/contentsScale on the seam layer;
  board px fixed at register.
- Bounded Wait Law: all waits already 100ms bounded (layer fences).
- Teardown Order Law: Layer/Pane unregister before Vk_shutdown (existing
  Darling_shutdownCompositor / VkPane_shutdown / VkLayer_shutdown order).

## Verification

1. `cmake --build build --target gfx_loop_test button_test vk_test -j 8`
   (`-Wall -Wextra -Werror`).
2. Run vk_test: window must show dark 0xFF1E1E24 backdrop + Input/Button/
   Label IMMEDIATELY (no resize) — first seam present carries the content.
3. Resize: content must track the window edges live (no corner-locked
   content, no blank after drag).
4. Static content rests after first present (present-on-demand: log cadence
   drops to probe-only).
5. gfx_loop_test + button_test still PASS.
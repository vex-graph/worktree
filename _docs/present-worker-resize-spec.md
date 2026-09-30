# Present-Worker Split & The Absolute Resizing System — Implementation Spec

> Status: DRAFT (`;;DRAFT`). R1 hotcwap + R3 graphvex + R4 darling.
> Governs how a window geometry change becomes pixels, and how the render work
> is split across threads. Binds: the Window Decoupling Law, the Vertical
> Integration Law, the Bounded Wait Law, the Teardown Order Law, the
> Continuous Real-Time Live Resize & Presentation Law, the Present-On-Demand
> Law, the Native Pixel Law, the Single-Seam Canvas Law, the Immediate vs
> Retained Element Model (darling.md section 55), the Cold-Strict, Hot-Minimal
> Validation Law.

---

## 1. Background

The frame renders correctly only if three things hold at once, every geometry
step, without a swapchain rebuild:

1. the window publishes its NEW live size (and origin) the instant AppKit
   moves it,
2. the two board worlds re-render at that new size into FIXED monitor-pixel
   targets,
3. the seam composites those two targets and presents a top-left crop.

Today (a) and (b) are implemented; (c) runs entirely on thread 0, and the
seam is still a `VkSwapchainKHR` allocated once. The goal of this spec is to
(a) name the **absolute resizing system** end-to-end so `test_suite.c` proves
it semantically, and (b) introduce the **present worker (thread n)** so the
retained-worlds render moves off thread 0 — with a single-presenter handoff.

---

## 2. The Model (locked decisions)

- **Fixed-buffer, no swapchains.** The seam buffer and the two board images
  are allocated ONCE at the monitor's native backing-pixel size and NEVER
  resized. The window is a top-left crop (`kCAGravityTopLeft`,
  `anchorPoint (0,0)`, `geometryFlipped = YES`, `autoresizingMask =
  kCALayerNotSizable`). `Vk_seamSetMaxExtent` allocates; `Vk_seamSetExtent`
  sets the RENDER AREA (the window's live px), never the chain size. The seam
  buffer becomes an IOSurface (`Surface`), retiring `VkSwapchainKHR`.
- **One seam, two boards.** Exactly one on-screen `CAMetalLayer` (the seam);
  `scenePanel` (bottom) and `contentPanel` (top) are retained offscreen
  images composited into it in z-order. (The Single-Seam Canvas Law.)
- **Immediate vs Retained gate — KEEP AS IS.** A depth-1 child owns a retained
  offscreen target ONLY when its subtree contains retained output (a
  `COMPOSITED` scene) — `panelSubtreeNeedsRetained()` in
  `window/panel_bridge.c`. Every leaf and every all-immediate container paints
  INLINE. (No widening to "any panel with children".)
- **anchor / origin / pivot** = darling `Component`: `origin` = parent
  zero-point + axis direction (4 corners); `anchor` = 9-grid tracking point;
  `pivot` = the child's own placement reference (4 corners + center).

---

## 3. The Three Loops

| Loop | Role | Entry | Runs on |
|:--:|---|---|---|
| L1 | Present / plaster — composite the two boards into the seam, present the crop | `Darling_renderFrame` + `Vk_clearPresent` | thread 0 |
| L2 | Resize — window dimension is priority; force the boards to re-render at the new live points, present per drag step | `frameCocoaResizeHook` → `Frame_syncResize` → `GraphicsLoop_modalTickForced` | thread 0 |
| L3 | Retained worlds — each retained target renders its own world on its own timeline | `VkLayer_visit` → `Darling_layerRender` | thread 0 by default; **thread n (opt-in, per world)** |

**Thread n is opt-in per world, not a mandatory present worker.** Present
(L1) and resize (L2) always stay on thread 0. A retained world MAY be given
its own render thread so several worlds render in parallel (GPUs are
multi-core / multi-queue — the Dynamic Scalability & Anti-Hardcoding Law: no
artificial single-thread ceiling). The default (all worlds visited on thread
0, one `VkLayer_visit` walk) stays correct and is what ships first.

Key invariant (the Present-On-Demand Law): **composite != render.** L1 samples
published targets; it can never re-invoke a world's render. L3 is the only
path that renders a world.

---

## 4. The Absolute Resizing System (per-step pipeline)

Every geometry event (resize OR move) runs this exact order. "Live points" =
the fractional content size; "live px" = `convertRectToBacking(live points)`.

```
AppKit tracking tick (thread 0)
  WindowContentView.setFrameSize:            (window/window_cocoa.m)
    windowRefreshSize(handle)   -> mirror live points (cachedWidth/Height),
                                   bump sizeGeneration,
                                   WindowEvent_fireResized(w,h)          [R1]
    windowRefreshOrigin(handle) -> mirror origin (cachedX/Y),
                                   WindowEvent_fireMoved(x,y)            [R1]
  viewWillStartLiveResize / viewDidEndLiveResize -> liveResizing flag

WindowEvent.onResized  -> frameCocoaOnResized(frame,w,h)                 [R4]
WindowEvent.onMoved    -> frameCocoaOnMoved(frame,x,y)      (to wire)    [R4]
Window resize hook     -> frameCocoaResizeHook(frame)                    [R4]
        |
        v
Frame_syncResize(frame, w, h)                (darling/frame.c)           [R4]
  1. resolve live fractional bounds (the Single Rounding Currency Law)
  2. lock roots; forceSize the locked board roots to the live bounds
  3. relayout -> Component_recompute resolves anchor/pivot/origin/margin
                 against the NEW parent extents (eager abs rect)
  4. Frame_platformSyncLayer(frame, w, h)   (frame_cocoa.m)
       - seam layer frame/bounds = live points        [AppKit, thread 0]
       - drawableSize = live px (Native Pixel Law)    [AppKit, thread 0]
       - Vk_seamSetExtent(drawW, drawH)  -> RENDER AREA only, chain fixed
  5. render + synchronous present:
       Darling_preFrame(window, drawW, drawH)
         - mark BOTH boards dirty
         - VkLayer_visit()   -> L3: fixed monitor-px targets RE-RENDER at the
                                new live points (both worlds), same-queue
                                ahead of the seam composite
       Darling_renderFrame(cb, drawW, drawH)  -> L1 seam collage:
         scene board (bottom) then content board (top) at anchor rects
       Vk_clearPresentLive() -> acquire, clear, seam pass, present-with-
                                transaction (top-left crop)
```

At rest (no drag), L1/L3 are demand-gated: only dirty clients present, idle
rests. During a drag, the moving edge IS the ticket — every step re-renders
and presents.

---

## 5. Threading Model (thread 0 + opt-in thread n)

Today there is **no render worker at all**: `GraphicsLoop_run` is a
single-threaded loop and every call — present, resize, retained visits — runs
on thread 0. Target topology:

```
thread 0  (AppKit / main)         thread n  (opt-in, ONE PER RETAINED WORLD)
----------------------------      ----------------------------------------
Window_pollEvents                 VkLayer_visit(world)  -> render that
windowRefreshSize/Origin                                world into its own
Frame_syncResize / relayout                             offscreen target
VkLayer register/resize/unreg     (its own command buffer + fence)
Darling_preFrame + visit (default)
Darling_renderFrame  (L1 collage)
Vk_clearPresent      (L1 present)
frameCocoaResizeHook + modalTickForced (L2)
```

### Why thread n exists

So an application can render **different worlds in parallel** — e.g. a heavy
3D scene on its own thread while the UI board keeps a steady cadence on thread
0 — instead of every world serializing through one `VkLayer_visit` walk. It is
**not** "content board on one thread, scene board on another" as a fixed rule;
it is a per-world choice the app makes. The default (every world visited on
thread 0 in one walk) is correct and ships first; per-world threads are the
opt-in upgrade. GPUs are multi-core / multi-queue — the Dynamic Scalability &
Anti-Hardcoding Law forbids a single-thread ceiling.

### Synchronization (composite != render holds across threads)

- A world thread renders into its own offscreen flight target and publishes
  (bump `VkLayer_publishGeneration`), then signals its fence.
- The compositor (thread 0) samples ONLY published frames — never re-invokes
  a world render (the Present-On-Demand Law).
- A world that lags the window for a step: the seam samples its last
  published frame, pinned top-left, crisp — never stretched, never blank
  (the Continuous Real-Time Live Resize & Presentation Law).
- All cross-thread waits are 100ms bounded with a drop-degrade (the Bounded
  Wait Law).

### Hard rules

1. **AppKit stays thread 0.** NSWindow/NSView/layer frame/`CATransaction`
   commit never leave thread 0 (the Window Decoupling Law).
2. **register/resize/unregister stay thread 0** (the `vk_layer.h` contract).
3. **visit/composite may run on a world thread** (the `vk_layer.h` contract);
   a world thread owns only its own target's render.
4. **Single presenter.** Only thread 0 ever composites the seam or presents.
   No world thread ever presents. (No handoff needed — the presenter never
   leaves thread 0.)
5. **Bounded Wait Law**: fences/acquires 100ms bounded, drop-degrade, no
   `UINT64_MAX`.
6. **Teardown Order Law**: `Vk_shutdown` joins every world thread BEFORE
   device teardown; `Memory_freeAll` last.

---

## 6. File Changes by Repo (upstream-first)

### vexspoke (R2) — docs, same cycle
- Amend the Window Compositing Layer Order Law (Tier 1): canonical stack =
  blur view + ONE seam IOSurface canvas + TWO retained board targets
  (fixed monitor px) composited in z-order; `DIRECT` panes remain the managed
  exception; Present-On-Demand + Native Pixel unchanged. (The Conflict Triage
  Law.)

### graphvex (R3)
1. `feat(seam): make the seam an IOSurface (Surface), retire the swapchain`
   - Replace the `VkSwapchainKHR s_swapchain` seam with `Surface` +
     `VkIOSurface` (both already exist). `Vk_seamSetExtent` sets the render
     area; `Vk_seamSetMaxExtent` allocates once. Present binds the IOSurface
     as the layer's contents.
2. `feat(vk_layer): opt-in per-world render threads`
   - A retained world MAY be given its own render thread (own command buffer
     + fence) that owns `VkLayer_visit` for THAT world only; the default
     keeps the single thread-0 walk. The compositor samples published frames
     (never re-renders). Join all world threads in `Vk_shutdown` (the
     Teardown Order Law), 100ms bounded.
3. `fix(vk_layer): honor the thread contract`
   - Assert/clarify register/resize/unregister thread-0-only; visit/composite
     worker-only.

### darling-framework (R4)
1. `refactor(frame_cocoa): build the stack through VisualEffect + Surface`
   - Stop creating a raw `NSVisualEffectView`/`CAMetalLayer`; use the
     graphvex `VisualEffect` + `Surface` classes. R4 never reaches into R3
     internals (`Vk_seamSetMaxExtent` moves behind `Surface`).
2. `feat(frame_cocoa): consume onMoved`
   - `WindowEvent_setOnMoved(ev, frameCocoaOnMoved)` → `Frame_setLocation`
     reflection; keep the origin cache in step.
3. `refactor(surface): retire darling/render/surface.h`
   - Resolve the `Surface` name collision (graphvex `surface/surface.h` wins;
     darling's legacy stamp class goes).

### hotcwap (R1) — DONE this cycle
- `feat(window): add windowMoved lifecycle gateway` (onMoved slot +
  `windowDidMove:` + `windowRefreshOrigin` per-step).

### tests (umbrella, local)
- `feat(tests): prove the resize semantics in test_suite.c` (see section 7).

---

## 7. test_suite.c Semantics & Verification

### What it is supposed to do

`--self-test-anchor-live` boots the REAL Frame + bridge (Kernel + Application
+ Frame(window) + scene board bottom + content board top + a UI tree with
four corner panels and a center card), then drives a scripted drag and
asserts every registered panel's absolute rect against an INDEPENDENT anchor
contract (written from the `Component` contract, never from
`Component_recompute`, so a resolve regression cannot self-confirm).

### How it is run (visible — the user inspects)

The harness runs with a **VISIBLE window** so the drag can be watched and
screenshotted. Modes:

- `--self-test-anchor-live` — scripted drag, asserts, exits with a verdict.
- `--probe-resize-stay` — same drag but stays alive at a mid-drag geometry
  for visual inspection.

### What must be strengthened

1. **Drive the real geometry path.** `probeStep` must go through the real
   path (`Window_setSize` → AppKit → the resize hook), so the pipeline in
   section 4 is what's exercised — not a bare `Frame_resize` shortcut.
2. **Assert the present cadence.** Per step, both boards must have
   re-rendered (`VkLayer_presentCount` delta) and the seam must have
   presented (`Vk_presentCount` delta), for BOTH a grow drag and a shrink
   drag. A step that presents zero is a FAIL.
3. **Assert the crop, not a resize.** After the drag, the seam/board extents
   must equal the monitor-px allocation UNCHANGED (proving no rebuild), while
   the render area tracked the window.
4. **Assert per-step anchor tracking** (already present): grow 800->1040,
   shrink 1040->640, settle 800x600 — the dials re-resolve every step.
5. **`onMoved` probe.** Drive a window MOVE (not just resize) and assert the
   top-left `onMoved(x,y)` payload matches `Window_getLocation` per step.

### Acceptance

- `PASS anchor-live probe: all N assertions passed`
- new: `PASS resize cadence: <steps> steps, <steps> presents, boards
  re-rendered <2*steps>`
- new: `PASS move probe: <steps> onMoved steps, origin tracked`
- `window_event_test` (onMoved), `bridge_seam_test` 8/8 stay green.
- Build clean under `-Wall -Wextra -Werror` in every touched repo.

---

## 8. Resolved Decisions

1. **Seam -> `Surface`/IOSurface NOW.** Retire `VkSwapchainKHR`; the seam is a
   fixed monitor-px IOSurface, the window a top-left crop.
2. **Thread n = opt-in per-world render threads** (not a mandatory present
   worker, not "two boards on two threads"). Present + resize stay thread 0;
   a world may render on its own thread for parallelism. Default = single
   thread-0 visit walk.
3. **Verification is VISIBLE.** The user runs `vk_test` and watches the drag;
   the harness keeps a live window (`--probe-resize-stay`) for inspection.
4. **`onMoved` payload = window top-left only**, in absolute desktop points —
   the same space as `Window_getLocation` and `Window_setLocation` (pixel
   wise). `Window_getContentOrigin` stays a getter.

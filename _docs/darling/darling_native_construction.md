# Darling Native Construction — Anchoring Without Gap + Many-Panel Scale

> ;;DRAFT — PANE-ERA DOCUMENT (retirement banner). The per-child
> `IOSurface + CALayer` backing and the DIRECT `VkPane` swapchain model
> described across this file are RETIRED (the Single-Seam Canvas Law): the
> window owns ONE on-screen `CAMetalLayer` (the seam canvas), boards and
> depth-1 children are retained OFFSCREEN `VkLayer` targets composited into
> the seam pass, and `PanelCocoa_newMetal`/`PanelCocoa_setAnchors`/
> `anti_AttachPanelIOSurfaceChildren`/`Window_compositeIOSurfaceChildren` are
> deleted. The anchor/gravity math below remains mechanically valid for the
> retained-target model (TopLeft-pinned, `autoresizingMask` on the seam
> only); section 1 states the current contract.

> Construction contract for a darling API that is native by default.
> Goal: every `Panel` anchors natively (no catching gap on resize/scroll)
> and the tree holds 100+ panels without VRAM/layer exhaustion.
> Sources: `../../preferences.md` Rules 11-14, `projects/darling/darling/container.h`,
> `projects/darling/objc/panel_cocoa.m`, `projects/darling/window/panel_bridge.c`,
> `../../projects/hotcwap/objc/window_cocoa.m`, `projects/darling/darling/compositor.c`,
> `projects/darling/darling/panel/scroll_container.c`, `../../main/darling_gallery.c`.
> Governed by Rule 30: behavior change here without `;;OVERVIEW` + `_docs/darling.md`
> update in the same commit is a defect.

---

## 1. What "native" means (and what it does not)

1. `Panel` + `Container` is the `NSView` equivalent: layout, anchors, hit-test,
   events. It is never a pixel buffer.
2. The seam `CAMetalLayer` (`vexgraph.seam`) is the window's ONLY on-screen
   compositing node. AppKit/WindowServer composites it. Vulkan presents into
   it. No per-panel layer exists anywhere in the tree.
3. Boards (`PanelCocoa_newBoard`) are retained OFFSCREEN `VkLayer` flight
   targets — dumb GPU memory, never a CALayer, never in the window tree.
4. `Window` owns one `CAMetalLayer` (the seam swapchain). Scene/content
   boards render into retained offscreen `VkLayer` flight targets (graphvex)
   that the seam pass samples as textured quads — no per-scene Metal
   surface and no DIRECT mode (the pane-era `VkPane` swapchain is retired).
   Non-scenes never touch a swapchain
   (Rule 14, No Double-Render Law).

```
Panel/Container  ->  NSView  (layout + events + ScrollContainer offsets)
seam CAMetalLayer->  CAMetalLayer (the ONE on-screen layer, WindowServer-composited)
VkLayer board    ->  retained offscreen scene/content pixels (canvas-collaged)
VkLayer target   ->  depth-1 child pixels when subtree has retained output
```

---

## 2. Layer construction law (few layers, deep paint)

Only first-generation children of each board own a retained `VkLayer`
target — and only when their subtree contains retained-output (`RR`)
content (classification via `panelSubtreeNeedsRetained`). Everything deeper
paints **inside** the parent target/pass
via `Panel_setRenderHandler` (Vulkan `Vk_fillRect`, label/SDF quads).

```c
ScrollContainer *y = ScrollContainer_2(winW, winH);
Window_setContentPanel(w, (Panel*) y);      /* window IS y */

Panel *a = Panel_0();                        /* section S1 */
Panel_addContainer((Panel*) y, a);
Panel_setRenderHandler(a, section_render);   /* paints a1/a2/a3 inside */

Panel *a1 = Panel_0();                       /* interior widget, no target */
Panel_addContainer(a, a1);                   /* never PanelCocoa_newBoard(a1, ...) */
```

Rules:

* `panel_bridge.c`: `Darling_attachLayers` iterates direct children of each
  board only. Target alloc once (fixed pixel size), never realloc.
* `panel_cocoa.m`: `PanelCocoa_setSize` no-ops when the extent is unchanged
  (`w/maxW`, `h/maxH`). Resize = retained target resize, zero repaint unless
  drifted.
* Huge sizing panels (scroll `bounds`, `~900x16k` clamp) attach **after**
  surfacing and never call `PanelCocoa_newBoard`. They size the clamp only.
* No fixed cap: child targets register dynamically per the Dynamic
  Scalability & Anti-Hardcoding Law (the pane-era `IOSURFACE_CHILD_MAX 256`
  ceiling is retired). Gallery proves 100+ (S1-S12 curated + S13-S112
  stress twins).

---

## 3. Anchoring without the catching gap

The catching gap = layer frame visibly lags content during live resize or
scroll (tear, jump, doubled text). It has three causes and three fixes.
All three are required.

### 3.1 C-side resolve is the source of truth

```c
/* content scrolls, chrome stays — ScrollContainer_childFrame, not raw resolve */
void anti_GetChildLayout(Panel *child, float winW, float winH,
                         float *outX, float *outY, float *outW, float *outH)
{
    Panel *parent = Panel_getParent(child);
    if (parent && Memory_type(parent) == TYPE_SCROLL_PANEL_SINGLETON) {
        ScrollContainer_childFrame((ScrollContainer*) parent, child, winW, winH,
                               outX, outY, outW, outH);
        return;
    }
    Vec4 rect;
    Container_resolve(&(*child).base, 0.0f, 0.0f, winW, winH, &rect);
    (*outX) = rect.x;
    (*outY) = rect.y;
    (*outW) = rect.z;
    (*outH) = rect.w;
}
```

* `ScrollContainer_childFrame` (`scroll_container.c:668`): resolve child at
  `(0, 0, vw, vh)`, then `x -= offsetX; y -= offsetY` for content,
  bar untouched.
* `Window_compositeIOSurfaceChildren` (`window_cocoa.m:1102`) calls only this
  helper for `setFrame`. Never duplicate the math in ObjC.
* `Container_resolve` clears dirty; `hitTest` uses the same rect. Layout,
  paint offset, and hit-test can never disagree.

### 3.2 Native anchor pinning (Rule 13)

Set both anchors on every surfaced panel, in C **and** on the layer:

```c
Container_setParentAnchor(&(*a).base, CONTAINER_PARENT_ANCHOR_TOP_LEFT);
Container_setSelfAnchor(&(*a).base, CONTAINER_SELF_ANCHOR_TOP_LEFT);
PanelCocoa_setAnchors(pc, parentAnchor, selfAnchor);
```

`PanelCocoa_setAnchors` mapping (`panel_cocoa.m:251`):

| selfAnchor | `anchorPoint` | `contentsGravity` |
|---|---|---|
| 0 TL | (0,0) | `TopLeft` |
| 1 TC | (0.5,0) | `Top` |
| 2 TR | (1,0) | `TopRight` |
| 3 ML | (0,0.5) | `Left` |
| 4 C | (0.5,0.5) | `Center` |
| 5 MR | (1,0.5) | `Right` |
| 6 BL | (0,1) | `BottomLeft` |
| 7 BC | (0.5,1) | `Bottom` |
| 8 BR | (1,1) | `BottomRight` |

Parent anchor maps to `autoresizingMask` (same switch, `panel_cocoa.m:304`).
Without this, CoreAnimation stretches the old bitmap mid-drag and the panel
visibly catches up one frame later. With it, pixels stay pinned to the
correct corner before the next Vulkan repaint lands.

Required layer flags (set once in `PanelCocoa_new`):

* `geometryFlipped = YES` (Vulkan top-down onto CoreAnimation).
* `contentsGravity = TopLeft` initial, then per selfAnchor.
* `anchorPoint = (0,0)` initial, then per selfAnchor.
* `contentsScale = backingScaleFactor` (Rule 12, exact 1:1 Retina).
* `opaque = NO`, `drawsAsynchronously = NO`.
* Layer mutations on main thread only (`dispatch_async(main_queue)`),
  inside `[CATransaction setDisableActions:YES]`.

### 3.3 Pixel-exact backing (Rule 12)

```c
/* points -> pixels for surfaces; points for layer frames */
int pxW = (int)(rect.z * kx + 0.5f);
int pxH = (int)(rect.w * ky + 0.5f);
/* ... render into IOSurface at pxW/pxH ... */
[childLayer setFrame:CGRectMake(rx, ry, rw, rh)];   /* logical points */
childLayer.contentsScale = scale;                    /* backingScaleFactor */
```

Wrong scale = doubled/blurry text. Wrong frame space = permanent 2x offset
on Retina. `TextCore_backingScale()` is the single scale source.

---

## 4. Many-panel construction (how the gallery holds 112)

1. **Sections are flat.** S1-S112 are direct children of `y` at absolute
   frames (`TOP_LEFT/TOP_LEFT`). No nested `ScrollContainer`, no nested layers.
2. **Interiors are paint, not layers.** `section_render` fills bg blocks at
   resolved rects (flipped `y = surfH - yTop - h`) then invokes each child's
   `renderHandler` at its own rect. `ListContainer`/`GridContainer`/bubbles are layout
   math; glyphs arrive via `Label_renderFn`.
3. **Scrollbar is chrome.** Owned bar, last child (topmost), right-docked by
   `layoutBar`. `ScrollContainer_childFrame` exempts it from `-offset`.
   `scrollbar_render` draws track + value thumb; bar is pure view of `offsetY`.
4. **Surfaces are max-size once.** First `setSize` sets the ceiling
   (`base.maxW/H`); later resizes only shrink `contentsRect`. No per-frame
   `IOSurfaceCreate`.
5. **Present on demand.** `Vk_clearPresent` only on
   `firstFrame || resized || treeDirty || scrolling || overscrolled`.
   1 ms active / 16 ms idle sleep; vsync paces. Resize hook re-syncs
   `setViewportSize` + `syncToBar` + bar `markDirty` (thumb extent derives
   from view height, not value motion).
6. **No 50k surface, ever.** Document height lives as `ScrollContainer.offsetY`
   math. Viewport buffer (code/terminal) or cell recycling (chat bubbles)
   per the IOSurface ceiling (`16384 px` Metal limit, `~960 MB` for a
   `2400x100k @2x` buffer). Tiled `512x512` only for PDF/canvas.

Budget: 112 sections x `~900x~400 pt @2x` ~= small, fixed. One `900x16000`
surface is forbidden — that is what the surfaceless `bounds` panel exists
to prevent.

---

## 5. Scroll construction (offsets, feel, bar)

Single truth: `ScrollContainer.offsetX/Y`, end-clamped in `setOffset`
(`lo = -start`, `hi = content - view + end`, `hi = max(hi, lo)`).

* `scrollBy(dx, dy)` is the only raw-delta entry. `natural=true` default:
  `setOffset(ox + dx, oy - dy)`. Never hand-negate at call sites.
* `fling/tick/stop`: `tick(dt)` on Thread 0 while `isScrolling`;
  friction from `slippery`, rubber from `overscroll`, spring home past edge.
* `syncToBar` (offset -> bar) after every `setOffset/tick`; `syncFromBar`
  (bar -> offset) on drag input. Hiding/swapping the bar never breaks scroll.
* Trackpad: `onScroll -> ScrollContainer_scrollBy` via `Mouse_attachWindow`.

---

## 6. Verification checklist (run before calling it native)

* [ ] Every surfaced child sets parent + self anchor in C and the layer shows
  matching `anchorPoint`/`contentsGravity`/`autoresizingMask`.
* [ ] Live resize: no stretch/tear before repaint; `contentsRect` path taken,
  no `IOSurfaceCreate` in log.
* [ ] Retina: `contentsScale == backingScaleFactor`; 12 pt text measures
  12 pt on screen, glyphs sharp.
* [ ] Scroll: content shifts by `-offset`, bar stays; `natural` suite asserts
  `(0,500)+(0,100)->(0,400)` vs flipped `(0,600)`.
* [ ] Scale: gallery with S1-S112 presents; no `IOSURFACE_CHILD_MAX`
  warning; `bounds` panel has no `PanelCocoa` entry.
* [ ] Swapchain: non-scenes skipped when native (`No Double-Render Law`);
  COMPOSITED scenes sampled as `VkLayer` textured quads (zero per-scene Metal
  surfaces), DIRECT scenes hold their own pane chain; transparent scene +
  blur path intact.
* [ ] Teardown: `Window_destroy -> Darling_shutdownCompositor -> Vk_shutdown
  -> Thread_stopAll -> Memory_freeAll` (Rule 26); fence waits bounded
  at 100 ms (Rule 27).
* [ ] Docs: `;;OVERVIEW` + `_docs/darling.md` section updated in the same
  per-class commit (Rules 23, 30); commit message scoped to class, not repo
  (Rule 25); committed inside `../../projects/darling`, never umbrella root
  (Rules 6, 20).

---

## 7. Common violations (reject on sight)

* New `PanelCocoa_new` for an interior widget (`a1` inside `a`). Paint it.
* Tall content panel owning a tall surface. Keep it surfaceless; scroll math
  only.
* Raw `Container_resolve` for layer frames under a `ScrollContainer`. Use
  `anti_GetChildLayout`.
* `->` access, `(T *)` cast spacing, `dest`-first outs, second public struct
  in one file pair. See `../../preferences.md` Rules 1-5, 9, 16.
* Cross-repo blob commit or umbrella-root commit for a darling class.
  One class, one repo, upstream-first (Rules 6, 20, 25).

---

## 8. Minimal native window skeleton

```c
Window *w = Window_new(winW, winH, "native");
ScrollContainer *y = ScrollContainer_2((float) winW, (float) winH);
Window_setContentPanel(w, (Panel*) y);

Panel *hero = Panel_0();
Container_setParentAnchor(&(*hero).base, CONTAINER_PARENT_ANCHOR_TOP_LEFT);
Container_setSelfAnchor(&(*hero).base, CONTAINER_SELF_ANCHOR_TOP_LEFT);
Panel_addContainer((Panel*) y, hero);
Panel_setRenderHandler(hero, section_render);

/* after Window_show + attach: anchors reach the layers */
Window_compositeIOSurfaceChildren(w, (Panel*) y);
```

Proven by: `../../main/darling_gallery.c` (S1-S112, bounds, bar),
`../../main/darlingtest.c` (two-thread painter), `_docs/darling.md` #41-#49.

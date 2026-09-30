# Darling UI API — Complete Field / Compartment / Function Reference

> Retained-mode, off-heap UI for C23. For 2am-you: every struct field, every getter/setter,
> every compartment, why it is that way, and how pixels get to the WindowServer.
> Sources: `../../projects/darling` + `../../main/darling_gallery.c` + `../../main/darlingtest.c`.
> Governed by Rule 30 (Living Darling Docs): every darling bug fix, feature,
> or layout change must update the matching section in this file in the SAME
> commit as the code + `;;OVERVIEW` header. A section that disagrees with the
> source is a defect — fix the section, do not work around it.

## How to read this at 2am

- Every widget embeds `Panel base` as its first member, which embeds `Container base` first.
  Pass `&node->base` (or `&node->base.base`) to Container APIs. Never pierce structs manually;
  use the symmetric getters/setters (Rule 24).
- `add/insert` attach, `remove` detaches, never frees. The creator frees (Rule: detach-only).
- Colors are `uint32_t 0xAARRGGBB`. `0x00000000` = CLEAR/skip.
- Constructors: `_0` = detached defaults, `_1` = one arg, `_2` = two args.
- Compartments: `layout` (Container geometry), `visual` (color/shape/clip),
  `tree` (parent/children/source), `state` (widget value), `style` (swatches),
  `callback` (fn + ctx, never dirties), `owned` (we free), `borrowed` (we never free),
  `cache` (GPU/raster handles), `feel` (scroll physics), `bridge` (Vulkan/Metal/WindowServer).

## Table of Contents

- [1. Big picture](#1-big-picture--why-darling-exists)
- [2. Codebase laws](#2-codebase-laws-read-once)
- [3. Type registry](#3-type-registry-darling-typeh)
- [4. Container](#4-container-darlingcontainerhcontainercc)
- [5. Panel](#5-panel-darlingpanelpanelhpanelc)
- [6. Canvas](#6-canvas-darlingscenecanvashcanvsc)
- [7. ListContainer](#7-listcontainer)
- [8. GridContainer](#8-gridcontainer)
- [9. ScrollContainer](#9-scrollcontainer)
- [10. SectionContainer](#10-sectioncontainer)
- [11. LayeredContainer](#11-layeredcontainer)
- [12. MarkdownPanel](#12-markdownpanel)
- [13. RichTextPanel](#13-richtextpanel)
- [14. Button](#14-button)
- [15. Switch](#15-switch)
- [16. Checkbox](#16-checkbox)
- [17. RadioGroup](#17-radiogroup)
- [18. Slider](#18-slider)
- [19. Knob](#19-knob)
- [20. Input](#20-input-single-line--caret-subsystem)
- [21. Textarea](#21-textarea)
- [22. InputOTP](#22-inputotp)
- [23. Select](#23-select)
- [24. DatePicker](#24-datepicker)
- [25. ColorPicker](#25-colorpicker)
- [26. ColorSwatch](#26-colorswatch)
- [27. ScrollBar](#27-scrollbar)
- [28. Label](#28-label)
- [29. RichLabel](#29-richlabel)
- [30. Typography](#30-typography)
- [31. Kbd](#31-kbd)
- [32. Dialog](#32-dialog)
- [33. AlertDialog](#33-alertdialog)
- [34. FileDialog](#34-filedialog)
- [35. ColorDialog](#35-colordialog)
- [36. Picture](#36-picture)
- [37. Plot](#37-plot)
- [38. Scene / Scene2D / Scene3D](#38-scene--scene2d--scene3d)
- [39. RichText model](#39-richtext-textrich_texthc)
- [40. text_core bridge](#40-text_core-texttext_corehtext_core_stubcobjctext_corem)
- [41. Compositor](#41-compositor-darlingcompositorhc)
- [42. WindowServer / Metal / Vulkan end-to-end](#42-windowserver--metal--vulkan-end-to-end)
- [43. Vulkan shaders + SPV](#43-vulkan-shaders--spv)
- [44. Events + dispatch + bridge](#44-events--dispatch--bridge)
- [45. Anim](#45-anim-darlinganimanimhc)
- [46. Raster + Surface (CPU path)](#46-raster--surface-cpu-path-renderrasterhcsurfacehc)
- [47. IO / mmap / VFS / fontbake / .antifont](#47-io--mmap--vfs--fontbake--antifont)
- [48. ObjC bridges + panel_bridge](#48-objc-bridges--panel_bridge)
- [49. Gallery + darlingtest cookbook](#49-gallery--darlingtest-cookbook)
- [50. 2am cheat sheets](#50-2am-cheat-sheets)
- [51. Cursor](#51-cursor-darlingcursorcursorhc)
- [52. SplitContainer](#52-splitcontainer)
- [53. ExpandableListContainer](#53-expandablelistcontainer)
- [54. Frame (`darling/frame.h`, `frame.c`)](#54-frame-darlingframeh-framec)
- [55. Immediate vs Retained Element Model](#55-immediate-vs-retained-element-model-component-classification)
- [56. Component (new-architecture leaf)](#56-component-new-architecture-leaf-darlingcomponenthcomponentc)

---

## 1. Big picture — why darling exists

Darling sits at Layer 3: `vexspoke` (memory/math/types) -> `hotcwap` (windowing/input)
-> `darling` (UI tree + render) -> `api-haven` (telemetry). It is retained-mode:
you build a `Container/Panel` tree, mutate it via setters, and two render paths
present it:

1. **Metal path (current):** the window's single
   on-screen layer is the Frame **seam canvas** (`CAMetalLayer`); boards — scene
   (bottom) / content (top) — are retained OFFSCREEN `VkLayer` targets that paint
   their whole subtree; the seam pass composites the published board images in
   z-order at full extent (the Window Compositing Layer Order Law, managed
   exception per the Conflict Triage Law).
   Every scene child renders **COMPOSITED** (the Single-Seam Canvas Law) — the
   scene renders into a retained offscreen `VkLayer` flight target in graphvex
   (no per-scene Metal surface; the canvas samples the last-published frame as a
   textured quad in tree z-order). There is no DIRECT mode: the per-scene
   `CAMetalLayer` + `VkPane` swapchain path is retired, and the single
   on-screen canvas is the only Metal surface in the window.
   Apple WindowServer/CoreAnimation composites the layer tree.
   Retained
   layer-backed panels are *skipped* (never re-rendered) in every enclosing pass.
   Present is **on demand** (Rule 14): a canvas that is clean rests on its last
   composite; scenes render at their own FPS into their retained targets.
2. **CPU path (legacy/test):** `Raster` paints into `Buffer`s, `Surface` double-buffers
   per panel, Thread 0 composites fronts into a master `ColorBuffer`, `Window_present`.

The component-level classification — what is IMMEDIATE (one quad) vs RETAINED
(texture / offscreen target) per element, and how it decides delivery — lives
in [section 55](#55-immediate-vs-retained-element-model-component-classification).

Text has two paths: **sharp** (CoreText raster -> one cached texture quad) and
**SDF fallback** (GPU signed-distance-field per-glyph quads, JFA-baked atlas).
Images are borrowed off-heap pointers + UV crop + fit mode. Charts borrow `Buffer*`
data in place. Dialogs are borrowed-content + owned-title + modal focus capture.

---

## 2. Codebase laws (read once)

- **Rule 23 `;;OVERVIEW`:** every `.c` documents struct fields + 4-tier function index
  (constructors / core / setters / getters) in the first ~150 lines.
- **Rule 24 symmetric getters/setters:** every state field has `set/get` (or `is/`).
  Getters are `const*`, null-safe. Visual/state setters `markDirty`; wiring setters
  (`onChange/ctx/measurer`) do NOT dirty.
- **Rule 17 + uniform type rule:** darling IDs live in `darling-type.h`, numbered 1..N
  per project (no global windows). Each repo's registry starts at 1; the project byte
  in the 64-bit id disambiguates (`ID_PANEL` #1 of darling ≠ `ID_INT` #1 of vexspoke).
  Runtime dispatch uses full `TYPE_*_SINGLETON` ids only — bare `ID_*` numbers mean
  vexspoke's own class space. Parent chains are granted to vexspoke once via
  `Type_registerParents(PROJ_DARLING, ...)` in `c23/add.c`; vexspoke resolves by project
  byte and never includes `darling-type.h`.
- **Detach-only:** `Panel_addContainer` detaches from old parent first (reparent = move).
  `Panel_removeChild` unlinks + clears `parent`, never frees. `Panel_add` deep-copies
  structure but aliases payloads via `source`. Creator (or typed `*_free`) frees.
- **Dirty law:** layout setters call `layoutEdited` (dirty + invalidate `baseW/H`);
  pure state setters set `dirty=1` only so anchored panels do not jump mid-resize
  (the "subtle law"). `resolve`/`hitTest` clear dirty. `setEnabled` never dirties.
- **Null discipline:** every setter null-guards; every getter returns a type default
  (`false/0/0.0f/-1/nullptr`, colors `0u`, mode fallbacks).

---

## 3. Type registry (`darling-type.h`)

Ownership: vexspoke owns tag layout (`PROJ_*`, `FORM_*`, masks, the
`Type_registerParents` seam); darling owns its own class numbers, numbered 1..N
(uniform per-project rule). Included by `panel.h`, so the whole tree inherits it.

| ID | Value | What |
|----|-------|------|
| `ID_PANEL` | `1` | Panel |
| `ID_CONTAINER` | `2` | Container |
| `ID_CANVAS` | `3` | Canvas |
| `ID_PICTURE` | `4` | Picture |
| `ID_LABEL` | `5` | Label |
| `ID_RICH_LABEL` | `6` | RichLabel |
| `ID_SCENE` | `7` | Scene |
| `ID_SCENE2D` | `8` | Scene2D tag |
| `ID_SCENE3D` | `9` | Scene3D tag |
| `ID_LAYERED_CONTAINER` | `10` | LayeredContainer |
| `ID_SECTION_CONTAINER` | `11` | SectionContainer |
| `ID_LIST_PANEL` | `12` | ListContainer |
| `ID_SCROLL_PANEL` | `13` | ScrollContainer |
| `ID_GRID_PANEL` | `14` | GridContainer |
| `ID_MARKDOWN_PANEL` | `15` | MarkdownPanel |
| `ID_RICHTEXT_PANEL` | `16` | RichTextPanel |
| `ID_EXPANDABLE_LIST_CONTAINER` | `17` | ExpandableListContainer |
| `ID_BUTTON` | `18` | Button |
| `ID_SWITCH` | `19` | Switch |
| `ID_CHECKBOX` | `20` | Checkbox |
| `ID_RADIOGROUP` | `21` | RadioGroup |
| `ID_SLIDER` | `22` | Slider |
| `ID_KNOB` | `23` | Knob |
| `ID_SCROLLBAR` | `24` | ScrollBar |
| `ID_INPUT` | `25` | Input |
| `ID_TEXTAREA` | `26` | Textarea |
| `ID_INPUTOTP` | `27` | InputOTP |
| `ID_SELECT` | `28` | Select |
| `ID_DATEPICKER` | `29` | DatePicker |
| `ID_COLORPICKER` | `30` | ColorPicker |
| `ID_COLORSWATCH` | `31` | ColorSwatch |
| `ID_FILEDIALOG` | `32` | FileDialog |
| `ID_DIALOG` | `33` | Dialog |
| `ID_ALERTDIALOG` | `34` | AlertDialog |
| `ID_COLORDIALOG` | `35` | ColorDialog |
| `ID_KBD` | `36` | Kbd |
| `ID_PLOT` | `37` | Plot |
| `ID_TYPOGRAPHY` | `38` | Typography |
| `ID_RICHTEXT` | `39` | RichText |
| `ID_ANIM` | `40` | Anim |
| `ID_OBJECT3D` | `41` | Object3D |
| `ID_VIEWER3D` | `42` | Viewer3D |
| `ID_MATERIAL_PANEL` | `43` | MaterialPanel |
| `ID_VIDEO_PANEL` | `44` | VideoPanel |
| `ID_POINTER_EVENT` | `45` | PointerEvent (transient, no Panel base) |
| `ID_KEY_EVENT` | `46` | UIKeyEvent |
| `ID_FOCUS_EVENT` | `47` | FocusEvent |
| `ID_ACTION_EVENT` | `48` | ActionEvent |
| `ID_VALUE_EVENT` | `49` | ValueEvent |
| `ID_TREE_EVENT` | `50` | TreeEvent |
| `ID_GESTURE_EVENT` | `51` | GestureEvent |
| `ID_CURSOR` | `52` | Cursor |

Singleton tag pattern: `TYPE_X_SINGLETON = (PROJ_DARLING | FORM_SINGLETON | ID_X)`.
Every class above has a `TYPE_*_SINGLETON` in the registry; nothing is scattered into
widget-local headers (that scramble was a collision defect — the old `0x0069`/`0x006A`
window). Stamped by `Memory_alloc`, read back by `Memory_type`/`Type_class` for
Picture-vs-Container and Scene-vs-Panel dispatch without vtables. Events are transient
messages: no Panel base, no attach arms, but still `ARCH_DARLING` (and their parent
chain rows read as Panel, matching the legacy range table).

Parent chain (registered once in `c23/add.c` before the first `Darling_addAny`):
`container`/`canvas`/`richtext` are roots; `panel` descends from `container`;
`scene2d`/`scene3d` descend from `scene`; `alertdialog`/`colordialog` descend from
`dialog`; every other class descends from `panel` (events register as Panel, mirroring
legacy range resolution). `Darling_addAny` takes the full type id and masks it
(`Type_class`) for dispatch; `Type_isA(child, ID_PANEL)` walks the registered chain.
Anomaly to know: `Container_0` and `Canvas_0` both allocate with `TYPE_CONTAINER_SINGLETON`;
only `Panel_0` uses `TYPE_PANEL_SINGLETON`. `TYPE_CANVAS_SINGLETON` is defined but unused
at allocation today.

---

## 4. Container (`darling/container.h`, `container.c`)

Layout truth of every node. Ported contract-first from legacy `Container.java`.

### 4.1 Struct — every field

```c
typedef struct Container {
    float x, y, w, h;                 // layout
    float scaleX, scaleY;             // layout
    uint32_t anchors;                 // layout (packed two-anchor system)
    int32_t pivot;                    // layout
    float percentX, percentY;         // layout
    int32_t z;                        // layout (stored only, exterior sorter reads)
    uint8_t visible, enabled, dirty, clipping; // visual/state/dirty/clip
    float baseW, baseH;               // layout-cache (reserved today)
    float minW, minH, maxW, maxH;     // layout constraints
    float marginL, marginT, marginR, marginB;  // layout (additive margins)
    float radius; int radiusMode;     // visual shape
} Container;
```

| Field | Type | Default | Compartment | What it is / does |
|-------|------|---------|-------------|-------------------|
| `x` | `float` | `0` | layout | Position X in parent units. Input to `resolve`. Written by ctor, `setX`, `setLocation`. |
| `y` | `float` | `0` | layout | Position Y. Same as `x`. |
| `w` | `float` | `0` | layout | Logical width before `scaleX`/clamp. `resolve` uses `sw=w*scaleX`. |
| `h` | `float` | `0` | layout | Logical height before `scaleY`. |
| `scaleX` | `float` | `1` | layout | Axis scale applied at resolve only; stored `w` never rewritten. NULL read `1`. |
| `scaleY` | `float` | `1` | layout | Same on Y. |
| `anchors` | `uint32_t` | `TOP_LEFT` | layout | Packed: low byte parent anchor `0..8`, high byte self anchor `+1` biased (`0`=unset reads as `TOP_LEFT`). `setParentAnchor`/`setSelfAnchor` range-check; OOR write ignored, no dirty. |
| `pivot` | `int32_t` | `TOP_LEFT(0)` | layout | Source-of-truth point `0..4` (TL/TR/BL/BR/CENTER). Subtracted after percent in `resolve`. Setter rejects `<0`/`>4`. |
| `percentX` | `float` | `-1` (UNSET) | layout | If `>=0`, resolve replaces X with `parentX+percentX*parentW`. `0.5`=centered. `setCenter` writes `0.5` directly. |
| `percentY` | `float` | `-1` | layout | Same on Y. |
| `z` | `int32_t` | `0` | layout | Z-order within parent. Stored only; `container.c` never sorts (compositor iterates list order). |
| `visible` | `uint8_t` | `1` | visual | `hitTest` returns false when hidden. `setVisible` dirties. |
| `enabled` | `uint8_t` | `1` | state | Input flag for exterior dispatch only; never read in container/panel/canvas. Only setter that does NOT dirty. |
| `dirty` | `uint8_t` | `0` | dirty | `1`=needs re-resolve/re-render. Cleared by `resolve`/`clearDirty`. |
| `clipping` | `uint8_t` | `0` | visual | Clip-children directive; stored only, renderer honors. |
| `opacity` | `float` | `1` | visual | Per-node alpha multiplier over every paint of this node (bg, text, quads). Clamped `0..1`. `0`=fully transparent but still laid out and hit-tested (unlike `visible=0`). State edit: dirties, never recaptures base. |
| `baseW` | `float` | `0` | layout-cache | Parent width at last layout (legacy resize-delta ref). `layoutEdited` invalidates to `0`; current `resolve` never reads/writes it. Reserved. |
| `baseH` | `float` | `0` | layout-cache | Same on H. |
| `minW` | `float` | `0` (zeroed alloc) | layout | Min width. `0`=no floor. Enforced in `setSize/setMinSize/setMaxSize`. |
| `minH` | `float` | `0` | layout | Same on H. |
| `maxW` | `float` | `0`=unset | layout | Max width. Only clamps when `>0`. `setSize` first call sets ceiling `maxW=w` if unset. |
| `maxH` | `float` | `0`=unset | layout | Same on H. |
| `marginL` | `float` | `0` | layout | Additive: `resolve` does `screenX+=marginL`. Stored location never rewritten; zero margins resolve bit-identically. |
| `marginT` | `float` | `0` | layout | Same on Y. |
| `marginR` | `float` | `0` | layout (reserved) | Right edge for sibling layout. Written but unread in container/panel/canvas/compositor today. |
| `marginB` | `float` | `0` | layout (reserved) | Same on bottom. |
| `radius` | `float` | `0` | visual | Corner radius in parent units. `<0` clamps to `0`. Renderer interprets. |
| `radiusMode` | `int` | `CORNER_ARC(0)` | visual | `CORNER_ARC(0)` or `CORNER_SUPERELLIPSE(1)`. Others rejected. |

### 4.2 Functions — every signature

- `Container *Container_0(void)` — alloc `TYPE_CONTAINER_SINGLETON`, defaults above (`min/max` implicit zero). `nullptr` on OOM. No dirty.
- `float Container_getX/Y/Width/Height(const Container *c)` — raw, `0` on NULL.
- `void Container_setX(Container *c, float x)` / `setY` — write + `layoutEdited` (dirty + invalidate base).
- `void Container_setWidth/Height` — direct write + `layoutEdited`. No clamping (only `setSize/Min/Max` clamp).
- `void Container_setLocation(c,x,y)` — `setX`+`setY` (dirties twice, idempotent).
- `void Container_setSize(c,w,h)` — first-call ceiling (`maxW=w` if `<=0`), clamp to `[min,max]`, delegate to `setWidth/Height`.
- `void Container_setMinSize(c,w,h)` / `setMaxSize` — write limits, re-clamp current, delegate (dirty).
- `float Container_getScaleWidth/Height` — raw, `1.0` on NULL.
- `void Container_setScale(c,sx,sy)` — write both + `layoutEdited`.
- `int Container_getParentAnchor` — `anchors&0xFF`, `0` on NULL.
- `void Container_setParentAnchor(c,a)` — `0..8` else silent return; else pack + `layoutEdited`.
- `int Container_getSelfAnchor` — `(anchors>>8)&0xFF`, `0`=>`TOP_LEFT` else `raw-1`.
- `void Container_setSelfAnchor` — range-check, pack `(anchor+1)<<8`, `layoutEdited`.
- `int Container_getPivotReference` / `void Container_setPivotReference(c,p)` (`0..4`, else return).
- `void Container_setCenter(c)` — `setSelfAnchor(TOP_LEFT)` + `setPivotReference(CENTER)` then `percentX/Y=0.5`, `dirty=1` (percent write does not invalidate base).
- `float Container_getPercentX/Y` — raw, `UNSET(-1)` on NULL.
- `void Container_setPercentX/Y(c,pct)` — write + `dirty=1` only.
- `bool Container_hasPercentX/Y` — `getPercent>=0`.
- `int Container_getZ` / `void Container_setZ(c,z)` — write + `dirty=1`.
- `bool Container_isVisible/isEnabled/isClipChildren/isDirty` — `c && flag!=0`.
- `void Container_setVisible(c,v)` — `visible=v?1:0`, `dirty=1`.
- `void Container_setEnabled(c,e)` — flag only, no dirty.
- `void Container_setClipChildren(c,clip)` — write + `dirty=1`.
- `void Container_setOpacity(c,opacity)` — clamp `0..1`, write + `dirty=1` (no base invalidation). `float Container_getOpacity(c)` — raw, `1.0` on NULL.
- `void Container_markDirty(c)` — `dirty=1`. `void Container_clearDirty(c)` — `dirty=0`.
- `void Container_setMargin(c,l,t,r,b)` — write 4 + `dirty=1`.
- `void Container_getMargin(c,*l,*t,*r,*b)` — NULL container reads `0`; NULL out-ptrs skipped.
- `void Container_setRadius(c,r)` — `r<0?0:r`, `dirty=1`. `float Container_getRadius` (`0` NULL).
- `void Container_setRadiusMode(c,m)` — only `ARC/SUPERELLIPSE`, else return. `int Container_getRadiusMode` (`ARC` NULL).
- `void Container_resolve(c,parentX,parentY,parentW,parentH,Vec4 *outRect)` — dest-last. `sw=w*scaleX`, 9-grid parent anchor, 9-grid self anchor on scaled size, inward-margin sign flip for right/bottom-anchored, `screen=parent+p-s+margin+marginL/T`, percent override vs live parent, pivot shift, `Vec4_set(out,[x,y,sw,sh])`. Clears `dirty=0` unconditionally.
- `bool Container_hitTest(c,parentX,parentY,parentW,parentH,pointX,pointY)` — false if invisible/NULL. Calls `resolve` (clears dirty!), half-open `[x,x+w)` test. Note legacy `[x,y,w,h]` packed as `Vec4{x,y,z,w}`.

### 4.3 Why

First-member upcasting (`(Container*)panel == &panel->base`) gives Java-style inheritance
with zero-cost static binding, no vtable/RTTI on hot path. Two-tier dirty
(`layoutEdited` vs bare `dirty=1`) exists so color/hover/visibility/percent edits never
recapture `baseW/H` and anchored panels do not jump mid-resize.

---

## 5. Panel (`darling/panel/panel.h`, `panel.c`)

Visual + tree node. Base of Label/Picture/Scene and every widget.

```c
typedef void (*Panel_RenderFn)(struct Panel *panel, void *renderer, void *cmdBuffer,
                               float surfaceW, float surfaceH,
                               float x, float y, float w, float h);
typedef struct Panel {
    Container base;            // layout + dirty (inherited)
    uint32_t color;            // visual 0xAARRGGBB
    void *filters;             // bridge (future render-graph slot, @Draft)
    void *image;               // bridge (shared payload, aliased via source)
    Panel_RenderFn renderHandler; // visual+bridge (@Override slot)
    struct Panel *source;      // tree (view link, nullptr=owns data)
    struct Panel *parent;      // tree
    List *children;            // tree (owned List of Panel*, lazy, cap 4)
} Panel;
```

| Field | Default | Compartment | What / why |
|-------|---------|-------------|------------|
| `base` | `Container_0` copy | layout+dirty | Embedded layout. `Panel_add` copies x/y/w/h/scale/anchors/pivot/z/visible/enabled/clipping/percent (deliberately omits dirty/base/min/max/margin/radius). |
| `color` | `CLEAR(0)` | visual | Background fill. Compositor unpacks to float RGBA, skips draw if `0`. `PANEL_COLOR_WHITE/BLACK/CLEAR` constants. |
| `filters` | `nullptr` | bridge (future) | Render-graph placeholder, never dereferenced yet. Read/write-through canonical on views. |
| `image` | `nullptr` | bridge payload | Shared payload aliased by pointer through views, never freed by add/remove. View `set` writes through to canonical + fans dirty to holders; `get` reads through `source` chain. |
| `renderHandler` | `nullptr` | visual+bridge | Per-instance draw override (`@Override` in C). `nullptr`=solid quad default. Copied by `Panel_add` so views render like sources. Records into open pass (Vulkan cmd or software Raster) within clipped rect. |
| `source` | `nullptr` | tree | Canonical panel this view proxies. Set once by `Panel_add`. Drives read/write-through. |
| `parent` | `nullptr` | tree | Tree parent; `nullptr`=root/detached. Maintained by add/remove. |
| `children` | `nullptr` | tree | Lazily allocated `List(ID_LONG,4)` of `(uint64_t)(uintptr_t)child`. Never freed in panel.c (deferred to scene teardown). |

Functions:

- `Panel *Panel_0(void)` — alloc `TYPE_PANEL_SINGLETON`, temp `Container_0` struct-copy into prefix, shell freed. OOM-safe.
- `Panel *Panel_1(Panel *parent)` — `_0` + `Panel_addContainer(parent,p)` if both non-NULL.
- `uint32_t Panel_getBackgroundColor(const Panel *p)` (`CLEAR` NULL).
- `void Panel_setBackgroundColor(p,color)` — write + `markDirty` (no base invalidation).
- `void Panel_setBackgroundColorRGBA(p,r,g,b,a)` — pack `(a<<24|r<<16|g<<8|b)` + dirty.
- `void Panel_setBackgroundColorAndMark` — legacy-parity alias of set.
- `Panel_RenderFn Panel_getRenderHandler` / `void Panel_setRenderHandler(p,fn)` (`nullptr` restores default, dirties).
- Inline facades (null-guarded, one hop to `&base`): `Panel_setLocation/setSize/setMinSize/setMaxSize/setParentAnchor/setSelfAnchor/setVisible/isVisible/setZ/setMargin/getMargin/setRadius/getRadius/setRadiusMode/getRadiusMode`.
- `void *Panel_getImage` — recursive read-through `source`. `void Panel_setImage(p,image)` — view writes `src->image` + `markDirty(src)` + fan-out to every `src->children` entry; else write + dirty. Never frees old.
- `void *Panel_getFilters` / `void Panel_setFilters` — same pattern (view path recurses then marks view itself too).
- `const Panel *Panel_getSource` — raw `source`.
- `int Panel_refCount` — stub `;;INCOMPLETE`, returns `0` (parent-ref/damage-rect walker deferred).
- `Panel *Panel_getParent` / `bool Panel_hasParent` / `size_t Panel_childCount` (NULL-safe) / `Panel *Panel_getChild(p,i)` (bounds-checked) / `bool Panel_hasChildren` / `bool Panel_containsChild` (linear scan).
- `void Panel_addContainer(p,child)` — NULL/self guard; detach-from-old first; `child->parent=p`; lazy `List(ID_LONG,4)` (alloc fail restores `parent=nullptr`); append; dirty parent+child. Pure tree edit, no layout recapture.
- `bool Panel_removeChild(p,child)` — linear scan, `List_remove`, clear `child->parent` iff pointed at `p`, dirty both. Detach only, never frees.
- `Panel *Panel_add(parent,node)` — structural deep-copy + attach. Copies layout subset + `color` + `renderHandler`; `copy->source=node` (payloads alias); recursively copies children; attaches; dirties. Does NOT copy `image/filters` pointers (resolve via `source`), nor dirty/base/min/max/margin/radius.

Why: `color` = cheap solid-quad fast path; `renderHandler` = subclassing without vtables;
`image+source` = VIEW model (structure copied, payload aliased, dirty fans out to holders);
detach-only prevents dangling views. No `Panel_free` exists by design (needs pool-wide walker).

---

## 6. Canvas (`darling/scene/canvas.h`, `canvas.c`)

Flat 2D layout root: the coordinate space everyone resolves into. NOT a Panel/Container
subclass (no dirty flag, no tree pointers) — deviation from Java `volatile static`s is
intentional: C makes Canvas an explicit handle the compositor owns and passes.

```c
typedef struct Canvas { float virtualWidth, virtualHeight; int mode; float dpiScale; } Canvas;
// modes: CANVAS_MODE_STRETCH(0), FIT(1), PIXEL(2)
```

| Field | Default | Compartment | What |
|-------|---------|-------------|------|
| `virtualWidth` | `0`=follow fb | layout | Virtual-space width. `<=0` follows framebuffer on that axis. No validation. |
| `virtualHeight` | `0`=follow | layout | Same on Y. |
| `mode` | `PIXEL(2)` | visual policy | `STRETCH`=whole canvas->window asymmetric; `FIT`=uniform letterboxed+centered; `PIXEL`=1 unit=1px top-left pinned. Setter rejects outside `0..2`. NULL read `PIXEL`. |
| `dpiScale` | `1.0` | bridge | Backing-store factor. Only used in `PIXEL` mode. `<=0` clamps to `1`. NULL read `1`. |

Functions: `Canvas *Canvas_0(void)` (note: allocates with `TYPE_CONTAINER_SINGLETON`);
`void Canvas_setVirtualSize(c,w,h)` (no validation, no dirty — Canvas has no dirty);
`float Canvas_getVirtualWidth/Height` (`0` NULL); `void Canvas_setMode` (range-checked);
`int Canvas_getMode`; `void Canvas_setDpiScale` (`s>0?s:1`); `float Canvas_getDpiScale`;
`void Canvas_visibleRect(c,fbW,fbH,outRect)` (PIXEL `[0,0,fbW/dpi,fbH/dpi]`, else mapping);
`bool Canvas_buildProjection(c,fbW,fbH,Mat4 *dest)` (Y-down ortho->NDC, dest-last);
`void Canvas_resolveRoot(c,node,fbW,fbH,outRect)` (runtime-class dispatch: `ID_PICTURE`
resolves `&picture->base.panel.base` at `(0,0,cw,ch)`, else blind-cast to `Container*`;
clears target dirty via resolve);
`bool Canvas_windowToCanvas(c,winX,winY,fbW,fbH,Vec2 *outPoint)` (PIXEL path uses identity
scale — does not divide by dpi — asymmetric by construction; returns inside-test).

---

## 7. ListContainer

Indexed stack. Index IS the API. No second list exists; rows live in `base.children`.

```c
typedef struct ListContainer { Panel base; int32_t direction; float spacing; bool fillCross; } ListContainer;
// direction: LIST_PANEL_VERTICAL(0), HORIZONTAL(1)
```

| Field | Default | Compartment | What |
|-------|---------|-------------|------|
| `base` | `Panel_0` copy | inherited | Owns child list via `Panel_addContainer/getChild/removeChild/childCount`. |
| `direction` | `VERTICAL` | layout mode | `0`=vertical stack, `1`=horizontal. Others rejected (no-op). |
| `spacing` | `0` | layout mode | Gap between children, clamped `>=0`. Total subtracts one spacing at end. |
| `fillCross` | `false` | layout mode | `false`=cross wraps widest/tallest; `true`=stretch each child cross-size to self. |

Functions: `ListContainer *ListContainer_0(void)` (`TYPE_LIST_CONTAINER_SINGLETON`);
`ListContainer *ListContainer_1(direction)`; `setLocation/setSize` inline forwards;
`void ListContainer_add(lp,child)` (detach-old + attach + layout, never frees);
`void ListContainer_insert(lp,index,child)` (move-first if contained, clamp `index<0->0/>n->n`,
append then memmove `List_set/get` right, layout);
`Panel *ListContainer_get(lp,index)` (NULL/OOR=>`nullptr`);
`bool ListContainer_remove(lp,index)` (detach + layout, caller retains ownership);
`size_t ListContainer_count(lp)`; `void ListContainer_layout(lp)` (vertical: cursor on Y, track maxW,
optional stretch, `setLocation(kb,0,cursor)`, `cursor+=kh+spacing`, final wrap/stretch;
horizontal symmetric; skips nullptr kids; `n==0` leaves size untouched);
`void ListContainer_setSpacing` (clamp)/`setDirection` (reject invalid)/`setFillCross`
(all null-guard + layout + dirty);
`float ListContainer_getSpacing` (`0` NULL) / `int32_t ListContainer_getDirection`
(`VERTICAL` NULL) / `bool ListContainer_isFillCross` (`false` NULL).

---

## 8. GridContainer

Excel-core geometry. Cells are NEVER `base` children — `base` size is layout output.

```c
typedef struct GridContainer {
    Panel base; Panel **cells; float *rowHeights;
    int32_t rows, cols; float gapX, gapY; int32_t headerRows, headerCols;
} GridContainer;
```

| Field | Default | Compartment | What |
|-------|---------|-------------|------|
| `base` | `Panel_0` | inherited | Layout/tree/bg only. |
| `cells` | `nullptr` | slot array | Row-major `rows*cols`, `cells[r*cols+q]`. `nullptr` cell = empty hole, skipped. Detach-only overwrite. Grown by `ensureCapacity`. |
| `rowHeights` | `nullptr` | per-row override | `rows` entries; `-1`=auto (tallest child in row). New rows init `-1`. `setCell` cannot grow this; `setRowHeight` cannot grow grid. |
| `rows`/`cols` | `0` | extent | `>=0`; auto-grow on `setCell` past edge. |
| `gapX`/`gapY` | `0` | gaps | Uniform gaps, clamped `>=0`. Final total subtracts one gap. |
| `headerRows`/`headerCols` | `0` | metadata | Frozen-header counts. Stored + dirty only; no layout effect in v1 (future ScrollContainer honors). Clamped `>=0`. |

Functions: `GridContainer *GridContainer_0(void)`; `GridContainer *GridContainer_2(rows,cols)`
(negatives->0, `0x0` returns as-is, else `ensureCapacity(rows-1,cols-1)`, OOM=>free+`nullptr`);
`void GridContainer_setCell(g,row,col,cell)` (guard negatives, auto-grow, `nullptr` clears,
detach-only drop, layout; incoming child NOT `Panel_addContainer`ed — stays parentless);
`Panel *GridContainer_getCell` (NULL-safe/OOB=>`nullptr`);
`void GridContainer_layout(g)` (per-row `rh` = override or max child H; per-col `cw` = max child W
recomputed per cell; `setLocation(cb,x,y)` no stretch in v1; final `setWidth(totalW)`,
`setHeight(y-gy)`); `void GridContainer_setGap(g,gx,gy)` (clamp+layout);
`void GridContainer_setHeaderRows/Cols` (clamp, dirty only);
`void GridContainer_setRowHeight(g,row,h)` (`h<0?-1:h`, layout, cannot grow);
`setLocation/setSize` forwards; `void GridContainer_getGap(g,*gx,*gy)` (NULL-safe);
`int32_t GridContainer_getHeaderRows/Cols` / `float GridContainer_getRowHeight` (returns stored
`-1`=auto, not resolved) / `int32_t GridContainer_rowCount/colCount`.

---

## 9. ScrollContainer

Viewport + content + offsets. Single source of truth = `offsetX/Y`, end-clamped.
Compartments: viewport `base` + `content` child + ONE owned vertical `ScrollBar *bar`
(single bar only in this snapshot — no h/v pair yet) + insets + feel physics + direction flag.

```c
typedef struct ScrollContainer {
    Panel base; Panel *content; float offsetX, offsetY;
    float startInset, endInset; ScrollBar *bar; bool barVisible;
    float velX, velY, slippery, overscroll; bool natural;
} ScrollContainer;
```

| Field | Default | Compartment | What |
|-------|---------|-------------|------|
| `base` | `Panel_0`+size+clip | viewport | Viewport rect. `children` holds `content` + `bar`. `setClipChildren(true)`. |
| `content` | `nullptr` | viewport child | Oversized panel scrolled under viewport. `nullptr`=empty (bounds collapse to insets). Forwarders only, never `content->field` directly. |
| `offsetX/Y` | `0,0` | truth | Scroll offset into content. Everything (bar sync, scrollBy, tick) reads/writes this. Pinned by `setOffset`. |
| `startInset` | `0` | padding | Before first child; `lo=-start`. Unclamped (negative legal). |
| `endInset` | `0` | overscroll-past-end | `hi=content-view+end`. |
| `bar` | fresh `ScrollBar_0` | owned vertical bar (live view) | Child of viewport, right-docked 10px full-height via anchors. Replaceable view, never freed by ScrollContainer. Bar is pure view of `offsetY`. |
| `barVisible` | `true` | chrome visibility | Drives `Container_setVisible` on bar only; offsets keep working hidden. |
| `velX/velY` | `0` | feel (fling px/sec) | Set by `fling`, zeroed by `stop`, integrated+decayed by `tick`. |
| `slippery` | `0` | feel friction map | `0`=dead stop .. `1`=long glide. `friction=12+(0.8-12)*slippery`. Clamped `0..1`. |
| `overscroll` | `0` | feel rubber px | `0`=hard clamp. `>0` extends clamp `[lo-over,hi+over]` + spring-home in `tick`. Clamped `>=0`. |
| `natural` | `true` | direction | `true`: `scrollBy(dx,dy)->(ox+dx,oy-dy)` gesture-following; `false`: legacy flip. |

Functions:

- `ScrollContainer *ScrollContainer_2(viewW,viewH)` — only ctor. Alloc, base+size+clip, zero state, `ScrollBar_0` attach + `layoutBar`. OOM=>free+`nullptr`.
- `void ScrollContainer_setContent(sp,content)` — no-op if same; detach old (never free); attach new + store; `layoutBar` (re-dock + raise bar last) + `setOffset(cur)` re-clamp.
- `void ScrollContainer_setOffset(sp,x,y)` — THE clamp point. `over=overscroll>0?overscroll:0`, pin into `[lo-over,hi+over]`, dirty, `syncToBar`. Bounds: `lo=-start`, `hi=content-view+end`, `hi=max(hi,lo)` so undersized content collapses (no negative span).
- `void ScrollContainer_setViewportSize(sp,w,h)` — `setMaxSize` (lift first-size ceiling) + `setSize` self only, `layoutBar`, re-clamp.
- `void ScrollContainer_syncFromBar(sp)` — bar->offset (input): `t=clamp((value-min)/span)`, `offsetY=lo+t*(hi-lo)`, dirty. Span-zero guarded.
- `void ScrollContainer_syncToBar(sp)` — offset->bar (display) + `layoutBar`. Called by every setOffset/tick/setBar.
- `void ScrollContainer_setStartInset/setEndInset(sp,f)` — store + re-clamp.
- `void ScrollContainer_scrollbar_setVisible(sp,v)` — store + `setVisible(bar)` + dirty. Scrolling unaffected.
- `void ScrollContainer_scrollbar_setBar(sp,bar)` — detach-only swap + attach + visibility + layout + sync + dirty.
- `void ScrollContainer_setSlippery(sp,f)` — clamp `0..1`, no dirty. `void ScrollContainer_setOverscroll(sp,px)` — `px>0?px:0` + re-clamp.
- `void ScrollContainer_fling(sp,vx,vy)` / `void ScrollContainer_stop(sp)` (zero, no dirty).
- `void ScrollContainer_tick(sp,dt)` — no-op if `dt<=0`. Friction from slippery; per-axis: if moving integrate `off+=v*dt`, `v*=exp(-(friction+edge*6)*dt)`, `|v|<1->0`, hard-stop at rubber bounds; else if past edge spring `off+=(bound-off)*min(14*dt,1)`, snap `<0.5`. Write back, dirty if active, `syncToBar`. Run on Thread 0 per frame while `isScrolling`. Rest in-bounds = cheap no-op.
- `void ScrollContainer_setNatural(sp,b)` — flag only.
- `void ScrollContainer_scrollBy(sp,dx,dy)` — ONLY raw-delta entry. `natural?setOffset(ox+dx,oy-dy):setOffset(ox-dx,oy+dy)`. Callers never negate.
- `void ScrollContainer_panel_setSize(sp,w,h)` — `Container_setSize(content)` + re-clamp (no-op if empty).
- `void ScrollContainer_panel_setBackgroundColor(sp,c)` / `panel_setRadius` — forward to content (no-op if empty).
- `void ScrollContainer_childFrame(sp,child,winW,winH,*ox,*oy,*ow,*oh)` — `Container_resolve(child,0,0,vw,vh)`; if `child!=bar`: `x-=offsetX,y-=offsetY` (content scrolls, chrome stays). Outs null-tolerant. C-side resolve is source of truth (raw resolve would pin scrolled content).
- Getters: `getContent` / `getOffset(sp,*x,*y)` / `getStartInset/getEndInset` (`0` NULL) / `getBar` / `scrollbar_isVisible` (`sp&&barVisible`) / `getSlippery/getOverscroll` / `getVelocity` / `isScrolling` (`vx||vy`) / `isOverscrolled` (outside hard `[lo,hi]`) / `isNatural` / `panel_getSize` / `panel_getBackgroundColor` (`CLEAR` empty) / `panel_getRadius`.

Why end-clamped: every mutation funnels through `setOffset`, so shrinking content/viewport
can never maroon the viewport. Hiding/swapping the bar cannot break scrolling.

---

## 10. SectionContainer

Tabbed section container. The model holds N borrowed children; exactly one is live
in the base tree — hidden children are detached (zero layers, zero surfaces).
Switching is a hard cut (`TRANSITION_NONE`) or a bounded crossfade
(`TRANSITION_CROSSFADE`: old + new both live only inside `durationMs`, hard
timeout `durationMs+50ms`). Fade runs on the uniform helper clock
(`Anim_eval(ANIM_EASE_OUT, u)` over accumulated tick deltas; main tick, no thread).
A scene child is never nested — 3D promotes via R0 `Window_setScenePanel`.
`TabbedContainer` is banned: tabs are a mode of this class.

```c
typedef enum SectionContainerTabOverflow {
    SECTION_CONTAINER_TAB_OVERFLOW_SCROLL = 0, SECTION_CONTAINER_TAB_OVERFLOW_SHRINK
} SectionContainerTabOverflow;
typedef enum SectionContainerTransition {
    SECTION_CONTAINER_TRANSITION_NONE = 0, SECTION_CONTAINER_TRANSITION_CROSSFADE
} SectionContainerTransition;
typedef struct SectionContainer {
    Panel base; int32_t current; bool wrapAround;
    void (*onSectionChange)(void *ctx); void *ctx;
    SectionContainerTabOverflow tabOverflow; SectionContainerTransition transition;
    uint32_t transitionDurationMs; float tabMinWidthPx; int32_t selectedIndex;
    float tabScrollOffsetPx; Panel *headerView;
    Panel **children; uint32_t childCount; int32_t visibleIndex; Panel *previousChild;
    double fadeElapsedMs; float fadeFrom, fadeTo; bool fadeRunning;
} SectionContainer;
```

| Field | Default | Compartment | What |
|-------|---------|-------------|------|
| `base` | `Panel_0` | inherited | Live tree: visible child only (+ header on top). |
| `current` | `0` | state | Synced with `visibleIndex`/`selectedIndex` on every switch. |
| `wrapAround` | `false` | state | `false`=clamp ends; `true`=modulo wrap (negative-safe). |
| `onSectionChange` | `nullptr` | callback | Fired on every successful visible change (fade fires at start). |
| `ctx` | `nullptr` | callback ctx | Passed to `onSectionChange`. |
| `tabOverflow` | `SCROLL` | tab-strip part | `SCROLL`=IDE/Chrome strip, selected tab auto-scrolls into view (layout-deferred); `SHRINK`=compress to `tabMinWidthPx`, past floor falls back to scroll, never clips. |
| `transition` | `NONE` | tab-strip part | `NONE`=hard cut; `CROSSFADE`=bounded two-surface fade. Setting `CROSSFADE` with `durationMs==0` arms `180ms`. `SLIDE`/`WIPE` deferred. |
| `transitionDurationMs` | `0` | tab-strip part | Crossfade length; `0`=instant path. Animated default `180`. |
| `tabMinWidthPx` | `64.0f` | tab-strip part | Shrink floor, native px, clamped `>=0`. |
| `selectedIndex` | `0` | tab-strip part | Clamped selector; routes through `setVisibleChild`. |
| `tabScrollOffsetPx` | `0.0f` | tab-strip part (internal) | Derived strip offset; no setter. Auto-scroll lands with strip layout (`;;INCOMPLETE`). |
| `headerView` | `nullptr` | tab-strip part (borrowed view) | `null`=default strip. Replace detaches old, attaches new on top. Never freed here. |
| `children` | `nullptr` | content-slot part (model) | All N borrowed tabs, arena-owned, exact-size grown by `add`. |
| `childCount` | `0` | content-slot part | Model count. `getCount`/`getChildCount` report this (not the live tree). |
| `visibleIndex` | `-1` | content-slot part | Live index; `-1`=empty. New target during fades. |
| `previousChild` | `nullptr` | content-slot part (transient) | Outgoing child mid-fade only; `nullptr` otherwise. |
| `fadeElapsedMs` | `0.0` | fade clock (internal) | Accumulated `tick` deltas. `progress=clamp(elapsed/duration)`. |
| `fadeFrom/fadeTo` | `1.0/0.0` | fade clock (internal) | Outgoing opacity endpoints; incoming mirrors. |
| `fadeRunning` | `false` | fade clock (internal) | Read via `isFading`. |

Functions: `SectionContainer *SectionContainer_0(void)` (`TYPE_SECTION_CONTAINER_SINGLETON`);
`SectionContainer *SectionContainer_1(parent)` (attaches self);
`void SectionContainer_setVisibleChild(sc,index)` (invalid=no-op; same=no-op; `NONE`=detach+attach,
`CROSSFADE`=attach new at opacity 0 + start clock; fires `onSectionChange`);
`void SectionContainer_tick(sc,deltaMs)` (negative delta clamped 0; ease-out-cubic opacities;
done at `progress>=1` OR `elapsed>=duration+50`: detach old at opacity 1, `previousChild=null`);
`void SectionContainer_next/prev(sc)` (empty=no-op; clamp or wrap; route switch);
`void SectionContainer_setCurrent(sc,index)` (legacy clamp + route);
`void SectionContainer_setWrapAround`; `void SectionContainer_setTabOverflow/setTransition`
/`setTransitionDurationMs/setTabMinWidth` (negative floor `0`)/`setSelectedIndex` (clamp + route);
`void SectionContainer_header_setView(sc,view)` (detach-old + attach-new on top);
`void SectionContainer_add(sc,child)` (exact-size grow; first child becomes visible);
`void SectionContainer_setPane(sc,index,child)` (replace + live-swap if visible, detach-old);
`int32_t SectionContainer_getCurrent` (`0` NULL) / `getCount`+`getChildCount` (model count)
`bool SectionContainer_getWrapAround` / `getTabOverflow` (`SCROLL` NULL) / `getTransition`
(`NONE` NULL) / `uint32_t SectionContainer_getTransitionDurationMs` (`0` NULL)
`float SectionContainer_getTabMinWidth` (`64.0f` NULL) / `int32_t SectionContainer_getSelectedIndex`
`float SectionContainer_getTabScrollOffset` (`0.0f`; `;;INCOMPLETE` auto-scroll)
`Panel *SectionContainer_header_getView` / `getPane(sc,index)` (OOR=>`nullptr`)
`Panel *SectionContainer_getVisibleChild` (borrowed; `nullptr` when empty)
`bool SectionContainer_isFading` (`false` NULL).

---

## 11. LayeredContainer

Band-count shell. No z-stack array — bands are a count + 32-bit visibility mask.
Painting/hit-routing deferred (`(none — shell)`).

```c
typedef struct LayeredContainer { Panel base; int32_t bandCount; uint32_t bandVisibleMask; } LayeredContainer;
```

| Field | Default | What |
|-------|---------|------|
| `base` | `Panel_0` | Layout/tree/bg. |
| `bandCount` | `0` | Stacked band count `>=0` (clamped). Conceptual only. Does not touch mask. |
| `bandVisibleMask` | `0u` | Bit `i` = band `i` visible (`0..31`). All-hidden default. |

Functions: `LayeredContainer *LayeredContainer_0(void)`; `LayeredContainer_1(parent)`;
`void LayeredContainer_setBandCount(p,count)` (clamp, dirty);
`void LayeredContainer_setBandVisible(p,band,visible)` (guard `band<0||>=32`, bit set/clear, dirty);
`int32_t LayeredContainer_getBandCount` / `bool LayeredContainer_isBandVisible` (OOR=>false, no cross-check vs count).

---

## 12. MarkdownPanel

Document scanner: owned source string -> row Labels/RichLabels inside an owned ListContainer box.

```c
typedef struct MarkdownPanel {
    Panel base; uint8_t *textBlock; Font *font; uint32_t codeBackground;
    ListContainer *rows; float rowSpacing;
    struct MarkdownRowSlot *slots; size_t rowCount, rowCapacity;
    bool highlightable; TextSelect select; uint32_t highlightColor;
} MarkdownPanel;
struct MarkdownRowSlot { Panel *panel; RichText *model; uint8_t isRich;
                         float height; uint32_t cellStart, textLen; }; // file-local
// No source-offset fields on the slot: rows store display strings already, so
// copy slices/strips the rendered text directly (dead-structure rejected).
```

| Field | Default | Compartment | What |
|-------|---------|-------------|------|
| `base` | `Panel_0` | document root | Parent of `rows->base`. Own height NOT auto-wrapped; inner box carries cursor height. |
| `textBlock` | `nullptr` | owned source | vexspoke `string` block. `getText` returns borrowed `string_get`. Replaced wholesale on set. |
| `font` | `nullptr` | borrowed | RichText font. `nullptr`=>inline-markup lines fall back to plain Label, markers stripped. Triggers rebuild. Never freed. |
| `codeBackground` | `0xFF222222` | fenced-code fill | Behind fenced rows when `!=0`. |
| `rows` | fresh `ListContainer_0` spacing 4, attached | owned row box | Owns Y positions. `getRows` returns `&rows->base`. Shell freed in `free`; rows freed via slots. |
| `rowSpacing` | `4.0` | vertical gap | Mirrored into `ListContainer_setSpacing`; `cursor+=h+rowSpacing`, final `-rowSpacing`. Clamped `>=0`. |
| `slots` | `nullptr` | owned row records | Parallel to ListContainer children; drives typed teardown (`RichText_free`+`Memory_free` vs `Label_free`). Grown x2 from 8. |
| `rowCount/Capacity` | `0/0` | bookkeeping | Active vs alloc. |
| `highlightable` | `false` | selection gate | Enables document drag selection (no caret). Mirrored to every row's `setHighlightable`. Off clears the part (`TextSelect_reset`). |
| `select` | `TextSelect_default()` | selection part | Shared fixed-anchor part (Rule 29): `anchor/active` in the panel's rendered-text byte space + `hovered` flag. `begin`/`drag`/`end` mirror onto rows; `end` COMMITS a nonzero span (stays active/highlighted), collapses a plain click. |
| `highlightColor` | `0x662563EB` | selection fill | Packed `0xAARRGGBB`; propagated to every row via `setHighlightColor`. |

Sizes: `BASE 14, H1 28, H2 22, H3 17, CODE 12, LINE_FACTOR 1.35, TEXT 0xFFFFFFFF`.

Functions: `MarkdownPanel *MarkdownPanel_0(void)`; `MarkdownPanel_1(text)` (scan+layout now);
`void MarkdownPanel_free(s)` (detach-all + per-slot typed free + free slots + `string_free` +
free box shell + `Memory_free(s)`; does NOT detach `base` from its own parent);
`void MarkdownPanel_setText(s,text)` (free old, allocate new, rebuild; `nullptr`=>empty);
`void MarkdownPanel_setFont` (alias + rebuild); `void MarkdownPanel_setCodeBackground` (+rebuild);
`void MarkdownPanel_setRowSpacing` (clamp + mirror + rebuild);
`void MarkdownPanel_setLocation/setSize/setBackgroundColor` (forwards, no rebuild);
`void MarkdownPanel_setHighlightable(s,flag)` (mirror to rows; !flag resets the part);
`void MarkdownPanel_setSelection(s,start,end)` (part begin+drag + row mirror);
`void MarkdownPanel_setHighlightColor(s,color)` / `setHighlightColorRGBA(s,r,g,b,a)` (+row mirror);
`void MarkdownPanel_handlePointer(s,kind,localX,localY,window)` (document selection seam; the
`void *window` carries the OS window for the hover caret-cursor, `nullptr` headless);
`void MarkdownPanel_handleKey(s,ev)` (key seam: Cmd/Ctrl+C copies the committed span to the
board, Cmd/Ctrl+V pastes the board as the new document — cold rebuild; press-only, repeats
ignored, detection on keyCode + mods, never `ch`);
`char *MarkdownPanel_getSelectedText(s)` (arena copy, caller `Memory_free`; display-accurate:
label rows slice their stored visible string, rich rows tag-strip + unescape `\[`);
`const char *MarkdownPanel_getText` (borrowed) / `Font *MarkdownPanel_getFont` /
`uint32_t MarkdownPanel_getCodeBackground` / `Panel *MarkdownPanel_getRows` (live base) /
`float MarkdownPanel_getRowSpacing` / `size_t MarkdownPanel_getRowCount`
(== `ListContainer_count` on success) / `Panel *MarkdownPanel_getRow(s,index)` (slots panel) /
`bool MarkdownPanel_isHighlightable` / `void MarkdownPanel_getSelection(s,outStart,outEnd)`
(always ordered; null-safe on self AND out-params) / `uint32_t MarkdownPanel_getHighlightColor` /
`MarkdownPanel_getHighlightColorRGBA(s,outR,outG,outB,outA)`.

Selection: documents own their text (`dispatchPick` prefers a MarkdownPanel over its rows).
Down anchors (outside-down cancels), drag moves only the active edge, up COMMITS an ordered
nonzero range — the span persists highlighted and `getSelectedText` stays readable (legacy
behavior kept) — and a plain click collapses to none — same fixed-anchor browser semantics as
Label/RichLabel. First hover lifecycle, too: LEAVE/outside-MOVE flips `select.hovered` off and
applies the default cursor; inside MOVE/HOVER applies the I-beam when highlightable (markdown
previously had no caret-cursor). The selection index space aggregates each row's own text length
into one contiguous span (slot `cellStart` = sum of prior `textLen`); both row types'
`charIndexAt`/`setSelection` already speak that per-row space, so mapping is exact with no
tag/marker reverse-translation (managed exception, Tier 1 preserved). A selection spanning rows
covers the whole text of the rows it lands on; `getSelection` returns positions in this
rendered-text byte space, not raw source-byte offsets. Copy walks the committed span per-row by
`cellStart`/`textLen` and emits the bytes the user sees: Label rows slice the stored display
string (the `• ` bullet literal at `[0,4)` is included exactly when the selection touches it),
rich rows strip `[nn]`/style tags and unescape `\[` back to `[` via the rich glyph-span walk —
single two-pass count/fill alloc, no markdown re-parse.

Internals: `classifyLine` (blank/fence/headings/bullet/para), `hasInline` (backtick/`**`/`*`),
`measureTagged/fillTagged` (`[00]/[01 bold]/[02 italic]/[03 code]`, `[` escaped),
`fillStripped`, `addLabelRow` (bullet `• ` prefix, `Label_1`, `size*1.35` stack),
`addRichRow` (styles 0..3 on fresh RichText, `layout(0)`, `RichLabel_0`+`setTextModel`),
`markdownRowIndexAt` (row-local char hit-test), `markdownDocIndexAt` (y band scan over slot
heights + spacing, then row-local x), `applyRowSelection` (clamp + color + mirror per row;
rows whose span AND color already match are skipped, so a drag re-rasters only touched rows),
`refreshRowSelection` (ordered clamp + mirror all rows + dirty; skipped entirely when the
drag edge didn't move),
`rebuild` (zero-alloc line walk, `clearRows` cold path, skip blanks/fences, code Labels,
headings Labels, bullets/paras rich iff `font&&hasInline` else stripped, final box size +
authoritative `ListContainer_layout` + dirty).

---

## 13. RichTextPanel

Thin viewport over an ALIASED `RichText*` model. Height is output.

```c
typedef struct RichTextPanel { Panel base; RichText *source; float maxWidth; } RichTextPanel;
```

| Field | Default | What |
|-------|---------|------|
| `base` | `Panel_0` | Height output: `relayout` does `Panel_setSize(b,curW,src->layoutHeight)`. Width is input (preserved). |
| `source` | `nullptr` | Aliased, never owned/freed. `setSource` re-runs `RichText_layout` on caller model. |
| `maxWidth` | `0` | Wrap width for `RichText_layout`. Clamped `>=0`. |

Functions: `RichTextPanel *RichTextPanel_0(void)`; `RichTextPanel_2(rt,maxWidth)`;
`void RichTextPanel_free(s)` (null alias + free shell, model NOT freed);
`void RichTextPanel_setSource(s,rt)` (+relayout, nullable);
`void RichTextPanel_setMaxWidth` (+relayout);
`setLocation/setSize` (forward; height overwritten by next relayout) / `setBackgroundColor`;
`RichText *RichTextPanel_getSource` / `float RichTextPanel_getMaxWidth` /
`float RichTextPanel_contentHeight(s)` (`0` if no source, else `layoutHeight`; pair with ScrollContainer).

---

## 14. Button

Pressable shell. Label is `char*` copy (no owned label Panel in this snapshot).
State colors stored but no automatic selector yet; `press` is a documented-deferred no-op;
`onPress` never invoked yet (contrast `Switch_setOn` which fires).

```c
typedef struct Button {
    Panel base; char *label; Font *font; float fontSize; uint32_t textColor;
    uint32_t bg, bgHover, bgPressed, borderColor; float radius, borderWidth;
    bool disabled, hovered, pressed; void (*onPress)(void *ctx); void *ctx;
} Button;
```

| Field | Default | Compartment | What |
|-------|---------|-------------|------|
| `base` | `Panel_0` | inherited | |
| `label` | `nullptr` | owned copy | `TYPE_ARRAY(strlen+1)` + strcpy; `nullptr`=empty. Freed on replace/free. |
| `font` | `nullptr` | borrowed | `nullptr`=default. Never freed. |
| `fontSize` | `12` | style | Points. Unclamped. |
| `textColor` | `0xFFFFFFFF` | style | |
| `bg` | `0xFF3A3A3A` | style idle | Per-state fills exist but nothing selects among them yet. |
| `bgHover` | `0xFF4A4A4A` | style hover | |
| `bgPressed` | `0xFF2A2A2A` | style pressed | |
| `borderColor` | `0xFF888888` | style | |
| `radius` | `4` | style | Stored only; does NOT forward to `Panel_setRadius`. |
| `borderWidth` | `1` | style | Stored only. |
| `disabled` | `false` | state | Convention only; `press` stub enforces nothing. |
| `hovered`/`pressed` | `false` | state | Externally driven; no hit-test writes them. |
| `onPress`/`ctx` | `nullptr` | callback | Never invoked in current source. `setOnPress` does not dirty. |

Functions: `Button *Button_0(void)`; `Button_1(label)`; `Button_2(parent,label)`;
`void Button_press(b)` (`;;INCOMPLETE` no-op); `void Button_free(b)` (frees label, not parent/font/ctx);
setters `setLabel` (free old, `nullptr`=>empty, OOM=>`nullptr` label, dirty) +
`setFont/FontSize/TextColor/Background/Hover/Pressed/BorderColor/Radius/BorderWidth/Disabled/Hovered/Pressed`
(store + dirty, no validation) + `setOnPress(b,fn,ctx)` (store both, no dirty);
getters `getLabel` (`nullptr` empty) / `getFont` / `getFontSize` (`0` NULL) /
`getTextColor/Background/Hover/Pressed/BorderColor` (`0u`) / `getRadius/getBorderWidth` /
`isDisabled/isHovered/isPressed` / `getOnPress` / `getPressContext`.

---

## 15. Switch

Toggle. `setOn` fires `onChange` synchronously on actual flip only; `toggle` routes through it.

```c
typedef struct Switch { Panel base; bool on; uint32_t trackOn, trackOff, knob;
    void (*onChange)(void *ctx); void *ctx; } Switch;
```

| Field | Default | What |
|-------|---------|------|
| `base` | `Panel_0` | |
| `on` | `false` | Toggle state. |
| `trackOn` | `0xFF4CAF50` green | On-track fill. |
| `trackOff` | `0xFF777777` grey | Off-track fill. |
| `knob` | `0xFFFFFFFF` white | Knob fill. |
| `onChange/ctx` | `nullptr` | Fired inside `setOn` on flip only. Re-entrancy safe (recursive same-value absorbed). |

Functions: `Switch *Switch_0(void)`; `Switch_1(parent)`; `void Switch_toggle(s)`
(`setOn(s,!on)`); `void Switch_setOn(s,on)` (no-op if same: no callback, no dirty; else store+dirty+fire);
`setTrackOn/TrackOff/Knob` (store+dirty); `setOnChange(s,fn,ctx)` (store, no dirty/fire);
`bool Switch_isOn` / `getTrackOn/TrackOff/Knob` (`0u` NULL) / `getOnChange` / `getChangeContext`.

---

## 16. Checkbox

```c
typedef struct Checkbox { Panel base; bool checked, indeterminate;
    uint32_t box, check; void (*onChange)(void *ctx); void *ctx; } Checkbox;
```

| Field | Default | Compartment | What |
|-------|---------|-------------|------|
| `base` | `Panel_0` | layout | |
| `checked` | `false` | state | On/off. |
| `indeterminate` | `false` | state | Tri-state dash for mixed children; orthogonal to `checked`. `toggle` does not clear it. |
| `box` | `0xFF888888` | style | Box outline. |
| `check` | `0xFF222222` | style | Checkmark fill. |
| `onChange/ctx` | `nullptr` | callback | `toggle` does NOT invoke (pump will). `setOnChange/setCtx` assign only, no dirty. |

Functions: `Checkbox *Checkbox_0(void)`; `Checkbox_1(parent)`;
`void Checkbox_toggle(c)` (`setChecked(c,!isChecked)`); `void Checkbox_setChecked/setIndeterminate/setBox/setCheck`
(+dirty); `setOnChange/setCtx` (assign only);
`bool Checkbox_isChecked/isIndeterminate` / `uint32_t Checkbox_getBox/getCheck`
(`0` NULL) / `getOnChange` / `getCtx`. No `free` (via `Memory_free`).

---

## 17. RadioGroup

Exclusive choice. `options` list + `selected` + `onSelect`. Add/clear are `;;INCOMPLETE` stubs.

```c
typedef struct RadioGroup { Panel base; List *options; int32_t selected;
    int32_t orientation; void (*onSelect)(void *ctx); void *ctx; } RadioGroup;
// RADIOGROUP_VERTICAL(0), HORIZONTAL(1)
```

| Field | Default | What |
|-------|---------|------|
| `base` | `Panel_0` | |
| `options` | `nullptr` | Owned `char*` labels; `nullptr`=empty. |
| `selected` | `-1` | Active index; `-1`=none. `setSelected` raw-assigns (allows future index before list lands). |
| `orientation` | `VERTICAL` | Normalizing clamp: `HORIZONTAL?1:0`, anything else->vertical. |
| `onSelect/ctx` | `nullptr` | Assign only, no dirty. |

Functions: `RadioGroup *RadioGroup_0(void)`; `RadioGroup_1(parent)`;
`void RadioGroup_addOption(g,option)` (stub); `void RadioGroup_clear(g)` (stub);
`void RadioGroup_setSelected/setOrientation/setOnSelect/setCtx`;
`void RadioGroup_free(g)` (drains `List`: free each `char*` via `uintptr_t`, `List_free`, null, `Memory_free(g)`);
`int32_t RadioGroup_getSelected` (`-1` NULL) / `getOrientation` / `optionCount`
(`0` if null/empty) / `const char *RadioGroup_getOption(g,index)` (borrowed, OOB=>`nullptr`) /
`getOnSelect` / `getCtx`.

---

## 18. Slider

`0..1` (or ranged) drag. `value/value2` clamped with lo/hi swap tolerance.

```c
typedef struct Slider { Panel base; float min, max, value, step, value2;
    bool vertical, showValue, range; uint32_t fill, knob;
    void (*onChange)(void *ctx); void *ctx; } Slider;
```

| Field | Default | What |
|-------|---------|------|
| `min/max` | `0/1` | Track bounds. `setMin/Max` raw, no re-clamp of values. |
| `value` | `0` | Primary thumb, clamped. `9.0` on `[0,1]` -> `1.0`. |
| `step` | `0.01` | Keyboard nudge. No positivity check. |
| `value2` | `1` | Secondary range thumb, clamped. |
| `vertical` | `false` | Orientation. |
| `showValue` | `true` | Readout flag. |
| `range` | `false` | Dual-thumb enable. |
| `fill` | `0xFF3A86FF` | Track fill. |
| `knob` | `0xFFFFFFFF` | Thumb color. |
| `onChange/ctx` | `nullptr` | Assign only. |

Clamp helper swaps inverted lo/hi first, then pins — `min>max` never breaks.
Functions: `Slider *Slider_0(void)`; `Slider_1(parent)`; `void Slider_setRange(s,min,max)`
(`;;INCOMPLETE` drag-handler stub, no-op — use `setMin/setMax`);
`setMin/setMax/setStep` (raw+dirty) / `setValue/setValue2` (clamped+dirty) /
`setVertical/setShowValue/setRangeEnabled/setFill/setKnob` (+dirty) / `setOnChange/setCtx`;
getters `getMin/Max/Value/Step/Value2` (`0` NULL), `isVertical/isShowValue/isRange`,
`getFill/getKnob`, `getOnChange`, `getCtx`.

---

## 19. Knob

Rotary dial. Angle-mapped Slider sibling. Same clamp law.

```c
typedef struct Knob { Panel base; float min, max, value, startAngle, sweep, diameter;
    void (*onChange)(void *ctx); void *ctx; } Knob;
```

| Field | Default | What |
|-------|---------|------|
| `min/max/value` | `0/1/0` | `value` clamped. |
| `startAngle` | `135` | Sweep start degrees. |
| `sweep` | `270` | Sweep extent (classic missing-bottom-quadrant dial). Negative allowed at shell level. |
| `diameter` | `48` | Dial size in parent units. |
| `onChange/ctx` | `nullptr` | |

Functions: `Knob *Knob_0(void)`; `Knob_1(parent)`; `void Knob_setNormalized(k,t)`
(`;;INCOMPLETE` angular-map stub); `setMin/Max` (raw+dirty) / `setValue` (clamped+dirty) /
`setStartAngle/setSweep/setDiameter` (raw+dirty) / `setOnChange/setCtx`;
getters `getMin/Max/Value/StartAngle/Sweep/Diameter` (`0` NULL), `getOnChange`, `getCtx`.

---

## 20. Input (single-line + caret subsystem)

Owner core + view-only caret part + callbacks + pending measurer hook.

```c
typedef struct Input {
    Panel base; char *text; size_t cap; char *placeholder;
    bool password, readonly; int32_t cursor; Font *font;
    int caretMode; uint32_t caretColor; float caretBlinkPeriod;
    double caretClock; bool caretShown; float caretX, caretTargetX;
    Panel *caretView; float caretOpacity;
    Input_ChangeFn onChange; Input_SubmitFn onSubmit; void *ctx;
    Input_MeasureFn measurer; void *measureCtx;
} Input;
// caret modes: BLINK(0), SOLID(1), GLIDE(2); DEFAULT_PERIOD 0.53s; GLIDE_TIME 0.08s
```

| Field | Default | Compartment | What |
|-------|---------|-------------|------|
| `base` | `Panel_0` | layout | |
| `text` | `nullptr` | owned UTF-8 | Bounded by `cap`. `nullptr`=empty. |
| `cap` | `256` | bound | Max chars excl NUL. `Input_2(parent,cap)` makes it mandatory (non-standard arity). `setCap` shrinks via `setText` re-truncate. |
| `placeholder` | `nullptr` | owned hint | Unbounded (hint, not input). |
| `password` | `false` | state | Mask at render. |
| `readonly` | `false` | state | Reject edits, still selectable. |
| `cursor` | `0` | state | Caret offset. `setCursor`=>`goTo` (clamped, re-measured, blink restarted). |
| `font` | `nullptr` | borrowed SDF | Never freed. |
| `caretMode` | `BLINK` | caret view | Rejects outside `0..2`. Non-BLINK forces `shown=true`; SOLID snaps `x=target`. |
| `caretColor` | white | caret view | |
| `caretBlinkPeriod` | `0.53` | caret view | Half-cycle. Rejects `<=0`. |
| `caretClock` | `0` | caret view | Blink timer. |
| `caretShown` | `true` | caret view | Phase. |
| `caretX` | `0` | caret view | Painted x. |
| `caretTargetX` | `0` | caret view | Owner-measured x. `setTarget`: non-GLIDE blits `x=target`, GLIDE eases later. |
| `caretView` | `nullptr` | caret view (borrowed) | `nullptr`=thin rect. Detach-only, never freed/reparented. |
| `caretOpacity` | `1` | caret view | Clamped `0..1`. Effective = blink x user (`!shown->0`). |
| `onChange/onSubmit/ctx` | `nullptr` | callback | Assign only. |
| `measurer/measureCtx` | `nullptr` | callback (pending) | `index->x` hook; null until caret walker lands. |

Functions: `Input *Input_0(void)`; `Input *Input_2(parent,cap)`;
`void Input_insertChar/eraseChar` (`;;INCOMPLETE` walker stubs);
`void Input_goTo(inp,index)` (live: `clampCursor(len,index)`, `<0->0`, `>len->len`,
`INT32_MAX` cap; re-measure target; `clock=0,shown=true`; dirty);
`void Input_free` (frees text+placeholder, never font/caretView/ctx);
`void Input_setText` (free old, truncate to cap, alloc+copy+NUL, clamp cursor, re-measure,
restart blink, dirty; `nullptr` clears); `void Input_setCap` (assign; shrink=>`setText(cur)`);
`void Input_setPlaceholder` (free+copy+NUL, dirty); `setPassword/setReadonly/setCursor(setCursor=>goTo)/setFont`
(+dirty); `setFontSize/setTextColor/setPlaceholderColor/setTextAlign/setSpacingWidth/setLigatures`
(+dirty); `setSelection/setSelectionColor/setSelectedText` (+dirty, selection span);
`setOnChange/OnSubmit/Ctx/setMeasurer` (assign only);
caret `setMode/setColor/setBlinkPeriod/setTarget/setView/setOpacity`
(clamped/validated + dirty); `void Input_caret_placeView(inp,view,centerY)` (centers view,
mutates view, no Input dirty);
`void Input_caret_tick(inp,dt)` (`dt<=0` return; BLINK `phase=fmod(clock,period*2)`,
dirty only on flip; GLIDE `k=dt/0.08` capped, `Anim_eval(EASE_OUT,k)`, dirty only if moved;
SOLID no-op; depth-1 proving element — caret stays painted inside the Input child's own
retained target at local coords, no cross-loop geometry; blink flip marks ONLY the Input
child dirty (never the board/tree) so a blink re-renders a tiny target at ~2Hz and Loop1
re-collages; no path reaches `Panel_markTreeDirty`/board dirty — board demand arms one
hop via `Darling_propagatePaneDirty`);
getters `getText/Placeholder` / `getCap` / `isPassword/isReadonly` / `getCursor` / `getFont` /
`getFontSize/getTextColor/getPlaceholderColor/getTextAlign/getSpacingWidth/hasLigatures` /
`getSelection/getSelectionColor/getSelectedText` /
`getOnChange/getOnSubmit/getCtx/getMeasurer/getMeasureContext` +
caret `getMode/getColor/getBlinkPeriod/getTarget/getX/isShown/getView/getOpacity/getEffectiveOpacity`.

---

## 21. Textarea

Multi-line editor. UNBOUNDED buffer (unlike Input). Lives in ScrollContainer when long.

```c
typedef struct Textarea { Panel base; char *text; int32_t visibleLines, wrap;
    float scrollY; Font *font; } Textarea;
```

| Field | Default | What |
|-------|---------|------|
| `text` | `nullptr` | Owned UTF-8, unbounded. `setText` full copy. |
| `visibleLines` | `4` | Viewport height in lines. No validation yet. |
| `wrap` | `1` | `0`=off, `1`=word. Raw. |
| `scrollY` | `0` | Vertical offset pts. Unclamped (walker clamps later). |
| `font` | `nullptr` | Borrowed SDF. |

Functions: `Textarea *Textarea_0(void)`; `Textarea_2(parent,visibleLines)`;
`void Textarea_scrollTo(t,y)` (`;;INCOMPLETE`); `void Textarea_setText/setVisibleLines/setWrap/setScrollY/setFont`
(raw + dirty); `void Textarea_free` (frees text, never font);
`getText/getVisibleLines/getWrap/getScrollY/getFont`.

---

## 22. InputOTP

N-box code entry. Fixed `length+1` buffer allocated once, reused (no churn).

```c
typedef struct InputOTP { Panel base; char *digits; int32_t length;
    float boxSize; InputOTP_CompleteFn onComplete; void *ctx; } InputOTP;
```

| Field | Default | What |
|-------|---------|------|
| `digits` | `""` | Owned `length+1` NUL buffer. `setDigits` memcpys truncated, never reallocs. |
| `length` | param (`6` for `_1_parent`) | Fixed capacity. `allocOtp` floors `<0->0`. |
| `boxSize` | `40` | Per-digit edge pts. No positivity check. |
| `onComplete/ctx` | `nullptr` | Full-code hook (walker fires later). |

Functions: `InputOTP *InputOTP_1(length)` (detached); `InputOTP_1_parent(parent)` (length 6 +
attach — named disambiguation, no `_1(Panel*)` overload); `InputOTP_2(parent,length)`;
`void InputOTP_pushDigit` (`;;INCOMPLETE`); `void InputOTP_setDigits(otp,s)` (reuse buffer,
truncate to length, dirty; `nullptr` clears); `setBoxSize` (+dirty); `setOnComplete/setCtx`;
`void InputOTP_free` (frees digits); `getDigits/getLength/getBoxSize/getOnComplete/getCtx`.

---

## 23. Select

Dropdown. Owned item list + selected/open/filter/onSelect. Popup must escape clipping
via future OverlayRoot.

```c
typedef struct Select { Panel base; List *items; int32_t selected, open;
    char *filter; Select_SelectFn onSelect; void *ctx; } Select;
```

| Field | Default | What |
|-------|---------|------|
| `items` | `nullptr` | Owned `char*` list, `nullptr`=empty. Add/clear stubbed. |
| `selected` | `-1` | Index, `-1`=none. Raw, no bounds check. |
| `open` | `0` | Popup flag as int (allows animation phases), not bool. |
| `filter` | `nullptr` | Owned filter text (combo-box mode). Single `TYPE_ARRAY` string. |
| `onSelect/ctx` | `nullptr` | |

Functions: `Select *Select_0(void)`; `Select_1(parent)`; `void Select_addItem/clear`
(`;;INCOMPLETE`); `setSelected/setOpen` (raw+dirty); `setFilter` (free+copy, dirty;
`nullptr` clears); `setOnSelect/setCtx`; `void Select_free` (drain items + free filter);
`getSelected` (`-1`) / `getOpen` (`0`) / `getFilter` / `getOnSelect` / `getCtx` /
`size_t Select_itemCount` / `const char *Select_getItem(sel,i)` (borrowed, OOB=>`nullptr`).

---

## 24. DatePicker

Calendar popup + field. Epoch-millis keeps the node dependency-light (no datetime include).
No owned heap. No min/max in this shell (only value + view).

```c
typedef struct DatePicker { Panel base; int64_t epochMillis;
    int32_t viewYear, viewMonth; DatePicker_PickFn onPick; void *ctx; } DatePicker;
```

| Field | Default | What |
|-------|---------|------|
| `epochMillis` | `0` (1970-01-01T00:00Z) | Selected instant. |
| `viewYear` | `1970` | Visible year. |
| `viewMonth` | `1` | `1..12` unchecked. |
| `onPick/ctx` | `nullptr` | |

Functions: `DatePicker *DatePicker_0(void)`; `DatePicker_1(parent)`;
`void DatePicker_setToday` (`;;INCOMPLETE` clock stub);
`setEpochMillis/setViewYear/setViewMonth` (raw+dirty) / `setView(year,month)` (atomic pair,
single dirty) / `setOnPick/setCtx`; getters `getEpochMillis` (`0`) / `getViewYear` (`1970`) /
`getViewMonth` (`1`) / `getOnPick` / `getCtx`. No `free`.

---

## 25. ColorPicker

Inline hue/sat/val well + flags. Single well + HSV mirror; no alpha field, no recent row yet.

```c
typedef struct ColorPicker { Panel base; uint32_t color; float h, s, v;
    bool showAlpha, showHex; void (*onChange)(void *ctx); void *ctx; } ColorPicker;
```

| Field | Default | What |
|-------|---------|------|
| `color` | white | Packed `0xAARRGGBB`. |
| `h` | `0` | Hue mirror `0..360` unchecked. No color<->HSV sync yet. |
| `s` | `0` | Saturation `0..1`. |
| `v` | `1` | Value (white-consistent). |
| `showAlpha/showHex` | `true/true` | Readout flags. |
| `onChange/ctx` | `nullptr` | |

Functions: `ColorPicker *ColorPicker_0(void)`; `ColorPicker_1(parent)`;
`void ColorPicker_setHSV(h,s,v)` (`;;INCOMPLETE` pack stub — use `setH/S/V` for mirror);
`setColor/setH/setS/setV/setShowAlpha/setShowHex` (raw+dirty, no clamp/sync);
`setOnChange/setCtx`; getters `getColor` (`0`) / `getH/S/V` / `isShowAlpha/isShowHex` / `getOnChange/getCtx`.

---

## 26. ColorSwatch

Single-row chip palette. Inline fixed `palette[16]` => zero heap churn.

```c
#define COLORSWATCH_CAPACITY 16
typedef struct ColorSwatch { Panel base; uint32_t palette[16];
    int32_t count, selected; void (*onSelect)(void *ctx); void *ctx; } ColorSwatch;
```

| Field | Default | What |
|-------|---------|------|
| `palette[16]` | all `0` | Packed entries. |
| `count` | `0` | Active entries. NOT auto-maintained by `setColorAt` yet. |
| `selected` | `-1` | `-1`=none. Raw, no bounds check. |
| `onSelect/ctx` | `nullptr` | |

Functions: `ColorSwatch *ColorSwatch_0(void)`; `ColorSwatch_1(parent)`;
`bool ColorSwatch_addColor(s,color)` (`;;INCOMPLETE`, always false);
`void ColorSwatch_setSelected` (raw+dirty); `void ColorSwatch_setColorAt(s,i,c)`
(guard `i<0||>=16`, write+dirty, does NOT bump count); `setOnSelect/setCtx`;
`int32_t ColorSwatch_getCount` (`0`) / `getSelected` (`-1`) /
`uint32_t ColorSwatch_getColorAt(s,i)` (`0` if null/OOB) / `getOnSelect` / `getCtx`.

---

## 27. ScrollBar

Two modes, fully live math, no stubs. Smallest struct. No callbacks.

```c
#define SCROLL_BAR_GESTURE 0
#define SCROLL_BAR_POINT 1
typedef struct ScrollBar { Panel base; int mode; float min, max, value, thumbMin; } ScrollBar;
```

| Field | Default | What |
|-------|---------|------|
| `mode` | `GESTURE` | `0`=trackpad-style, `1`=precise thumb. Setter rejects others. Note `_1` takes `int mode`, not `Panel*` — unlike every other widget. No attach ctor. |
| `min/max` | `0/1` | Track bounds. `setRange` swaps if `min>max`, re-pins value. Only range mutator that auto-clamps. |
| `value` | `0` | Thumb, clamped. `setValue(9.0)` on `[0,1]` -> `1.0`. |
| `thumbMin` | `24` | Min thumb extent px. Floored at `0`. |

Math: `pinValue`/`pin01` (normalize lo/hi swap first), `gestureDelta=dPx/trackLen*span`
(`trackLen<=0->0`), `pointLerp=lo+pin01(f)*(hi-lo)`.
Functions: `ScrollBar *ScrollBar_0(void)`; `ScrollBar_1(mode)`;
`void ScrollBar_dragBy(sb,deltaPx,trackLen)` (GESTURE law: position-independent, eyes-free);
`void ScrollBar_clickAt(sb,fraction)` (POINT law: fraction clamped `0..1`, `9.0->hi`);
`void ScrollBar_setRange/setMode/setValue/setThumbMin` (+dirty);
`int ScrollBar_getMode` (`GESTURE` NULL) / `float getValue/getThumbMin` /
`void ScrollBar_getRange(s,*min,*max)` (NULL=>`0,1`, single-side query allowed).

---

## 28. Label

Single-style sharp text view. Tries CoreText cached quad, falls back to SDF. Supports rich typography: ligatures, letter tracking, line leading, underline decorations, mnemonic accelerators, and text selection highlights. Labels never show a caret — they are non-editable surfaces; editing carets belong to Input/Textarea/CodeField.

```c
typedef struct Label {
    Panel base; char *text; Font *font; char *fontFamily; float fontSize;
    uint32_t textColor; float smoothness; int32_t rasterTex;
    int rasterW, rasterH; float rasterBacking; bool rasterDirty;
    bool highlightable; bool mnemonic; char mnemonicChar; int mnemonicIndex;
    bool ligatures; float spacingWidth, spacingHeight;
    UnderlineStyle underline; uint32_t underlineColor;
    Cursor *cursor; TextSelect select;
    float highlightRadius; uint32_t highlightColor;
} Label;
```

| Field | Default | Compartment | What |
|-------|---------|-------------|------|
| `base` | `Panel_0`+`renderHandler=Label_renderFn` | layout | Base Panel hierarchy node. |
| `text` | `NULL` | owned UTF-8 | Full string incl `\n` sent to CoreText. `setText` frees+dups, marks raster+container dirty. |
| `font` | `NULL` | borrowed SDF | Atlas descriptor for fallback only. Never used on sharp path. |
| `fontFamily` | `"Helvetica"` | owned cache key | CoreText typeface selector. `setFontFamily` frees+dups (`NULL`=>`nullptr`). |
| `fontSize` | `12` | text | Points; `pxH=size*backing`. `<=0` disables render. |
| `textColor` | white | color | Passed as `argb` to raster; unpacked to floats on SDF path. |
| `smoothness` | `0.5` | SDF only | Edge AA `0..1`, clamped. Does NOT dirty raster (SDF param). |
| `rasterTex` | `-1` | CoreText cache | `Texture_loadRaw` handle. Invalidated on text/font/family/size/color/style change. `free` nulls but does NOT delete GL texture. |
| `rasterW/H` | `0` | cache | Native px dims from raster. |
| `rasterBacking` | `1` | cache | Retina scale at raster time; `qw/=backing` point correction. |
| `rasterDirty` | `true` | coherency | Set by `markRasterDirty`, cleared in `ensureRaster`. |
| `highlightable` | `false` | interaction | Enables text selection drag (sets `cursor` to `CURSOR_IBEAM`). No caret — labels are non-editable. |
| `mnemonic` | `false` | typography | Parses `&` accelerator prefix: strips `&`, underlines mnemonic char, populates `mnemonicChar`/`mnemonicIndex`. `&&` escapes. |
| `mnemonicChar` | `'\0'` | state | Extracted accelerator character. |
| `mnemonicIndex` | `-1` | state | Character offset of mnemonic in display string. |
| `ligatures` | `true` | typography | Enables standard typography ligatures via CoreText `kCTLigatureAttributeName`. |
| `spacingWidth` | `0.0` | typography | Letter tracking/kerning delta in points via CoreText `kCTKernAttributeName`. |
| `spacingHeight` | `0.0` | typography | Line leading delta in points (extra vertical distance between rows). |
| `underline` | `UNDERLINE_NONE` | decoration | `UNDERLINE_NONE` (0), `UNDERLINE_BASIC` (1), `UNDERLINE_STRIKETHROUGH` (2), `UNDERLINE_JAGGED` (3) wavy diagnostic squiggle. |
| `underlineColor` | `0` | decoration | Packed `0xAARRGGBB` stroke color. `0` inherits `textColor`. |
| `cursor` | `CURSOR_DEFAULT` | presentation | Mouse cursor style for window hover/focus integration. |
| `select` | `TextSelect_default` | interaction | Embedded shared selection part (`text/text_select.h`): `anchor` (fixed press edge), `active` (live drag edge), `hovered` flag (caret-cursor lifecycle). DOWN anchors, DRAG moves only the active edge, UP orders and COMMITS a nonzero range as the new fixed selection (or collapses a plain click/cancels), PTR_CANCEL clears. Committed spans persist — getSelectedText and the highlight survive pointer-up, matching the legacy `selectionStart/End` contract. |
| `highlightRadius` | `3.0` | styling | Corner radius in points for selection rounded rect highlight. |
| `highlightColor` | `0x662563EB` | styling | Packed `0xAARRGGBB` translucent fill for text selection highlight. |

Functions:
- Constructors: `Label *Label_0(void)`; `Label_1(text)`; `Label_2(parent,text)`; `Label_1_parent(parent)`.
- Setters: `setText`, `setFont`, `setFontFamily`, `setFontSize`, `setTextColor`, `setSmoothness`, `setLocation`, `setSize`, `setBackgroundColor`, `setHighlightable`, `setMnemonic`, `setLigatures`, `setSpacingWidth`, `setSpacingHeight`, `setSpacing(w,h)`, `setUnderline`, `setUnderlineColor`, `setUnderlineColorRGBA(r,g,b,a)`, `setCursor`, `setSelection(start,end)`, `setHighlightRadius`, `setHighlightColor`, `setHighlightColorRGBA(r,g,b,a)`, `setHovered`, `Label_free`.
- Pointer / Hit-test: `Label_charIndexAt(label,localX)`, `Label_handlePointer(label,kind,localX,localY,window)`, `Label_onPointer(label,event,window)`.
- Keys: `Label_handleKey(label,ev)` — Cmd/Ctrl+C copies the committed selection through the clipboard seam (consumes); Cmd/Ctrl+V is a no-op (labels are read-only). Detection by `keyCode` + modifier bits (cmd=8, ctrl=2 bridge bits), never the decoded character; press-only, repeats ignored.
- Getters: `getText`, `getFont`, `getFontFamily`, `getFontSize`, `getTextColor`, `getSmoothness`, `getRasterTexture`, `getRasterSize(outW,outH)`, `getRasterBacking`, `isRasterDirty`, `getGlyphOffsets`, `getGlyphOffsetCount`, `isHighlightable`, `isMnemonic`, `getMnemonicChar`, `getMnemonicIndex`, `hasLigatures`, `getSpacingWidth`, `getSpacingHeight`, `getSpacing(outW,outH)`, `getUnderline`, `getUnderlineColor`, `getUnderlineColorRGBA(outR,outG,outB,outA)`, `getCursor`, `getSelection(outStart,outEnd)`, `getHighlightRadius`, `getHighlightColor`, `getHighlightColorRGBA(outR,outG,outB,outA)`, `isHovered`.
- Internals: `ensureRaster` strips mnemonic `&` (recording a label→clean index map plus the consumed-marker byte), reads the ordered span from the `select` part, maps the span into clean coordinates, builds `TextStyleDescriptor` with selection and rounded highlight radius/color, invokes `TextCore_rasterStyled`, uploads raw texture. Selection coordinates are stated per glyph, not estimated: on a successful raster the label asks the same CoreText shaper that paints for one pen offset per UTF-8 byte (`TextCore_lineOffsets`, single line only, same font/ligature/tracking inputs) and caches the table in label space (`glyphX`, `glyphN = strlen+1`; consumed markers fold onto the previous glyph; cleared on every rebuild entry and on free, installed only beside successful pixels). `Label_charIndexAt` shares that table with the baked highlight — midpoint (hemisphere) boundaries between stated offsets, continuation bytes rewinding to the codepoint start — so proportional type maps 1:1; without a table (multiline, stub platform, raster failure) it keeps the uniform `roundf(ratio*len)` fallback. `Label_renderFn` passes quad to `Vk_drawTexture` and never draws a caret (labels are non-editable surfaces). Pointer events (`handlePointer` / `onPointer`) adapt the window cursor to `CURSOR_IBEAM` on enter/hover, restore `CURSOR_DEFAULT` on leave, and drive the shared `TextSelect` part — fixed-anchor drag so dragging left (backward) then right past the anchor selects exactly `[anchor, active]`, never a rolling union. `TextSelect_drag` reports movement (false when the edge didn't move), so unchanged drag events skip re-raster entirely. `getSelectedText` returns an arena-allocated slice of the committed span (label coordinates, unaffected by the clean mapping).

---

## 29. RichLabel

Multi-style SDF-only view hosting a `RichText` model. No CoreText attempt (per-run
fonts/colors/bold/shadow/decor cannot be one raster without losing effects).
Supports selectable text with a fixed drag anchor (browser-like): pointer-down is
the anchor, drag moves only the active edge, so dragging left (backward) then right
past the anchor selects exactly `[anchor, active]` — never a rolling union.
`localX/localY` map to a source byte index via each glyph quad's `charIndex`/`advance`;
highlights render as flat per-line spans behind the glyph quads. Selection state
lives in the shared `TextSelect` part (UP COMMITS a nonzero range; collapsed clicks
clear), so the highlight and copy persist after pointer-up. No caret — labels
are non-editable surfaces.

```c
typedef struct RichLabel {
    Panel base; RichText *textModel; WrapMode wrapMode;
    Cursor *cursor; bool highlightable;
    TextSelect select; uint32_t highlightColor;
} RichLabel;
```

| Field | Default | What |
|-------|---------|------|
| `base` | `Panel_0`+`RichLabel_renderFn` | |
| `textModel` | `NULL` | Styled layout model (`quads/quadCount` consumed). Raw pointer assign (no alloc/free) — treat as borrowed ref. |
| `wrapMode` | `WRAP_WORD` | Mirrored into model on set. |
| `cursor` | `CURSOR_DEFAULT` | Switches to `CURSOR_IBEAM` when `highlightable`. |
| `highlightable` | `false` | Enables drag selection (no caret). |
| `select` | `TextSelect_default` | Shared selection part (anchor/active edge + hovered flag). DOWN anchors, DRAG moves only the active edge, UP orders and COMMITS a nonzero range (collapsed clicks clear), outside-down cancels; committed spans persist. |
| `highlightColor` | `0x662563EB` | Packed `0xAARRGGBB` selection fill (flat spans — no rounded corners on the SDF path). |

Functions: `RichLabel *RichLabel_0(void)`; `RichLabel_1(parent)`; `RichLabel_free(l,)` (frees the struct, never the borrowed model);
`void RichLabel_setTextModel(l,model)` (assign + dirty);
`void RichLabel_setWrapMode(l,mode)` (store + `RichText_setWrapMode` if model + dirty);
selection: `setHighlightable`, `isHighlightable`, `setSelection(start,end)`,
`getSelection(outStart,outEnd)` (always ordered, null-safe), `setHighlightColor`,
`getHighlightColor`, `setHighlightColorRGBA(r,g,b,a)`, `getHighlightColorRGBA`,
`setHovered`, `isHovered`, `setCursor`, `getCursor` (null-safe defaults);
pointer: `int32_t RichLabel_charIndexAt(l,localX,localY)` (nearest glyph origin,
weighting vertical distance `×1.6` to stay on-line; `localX` past the last glyph
advance returns `len`, before the first origin returns `0`),
`RichLabel_handlePointer(l,kind,localX,localY,window)` (down=anchor, drag=active edge,
up=commit or collapse-to-clear, outside-down cancels), `RichLabel_onPointer(l,ev,window)`;
keys: `RichLabel_handleKey(l,ev)` — Cmd/Ctrl+C copies the committed selection (tag-stripped, consumes),
V no-op (read-only);
copy: `char *RichLabel_getSelectedText(l)` (arena-allocated tag-stripped plain slice; each
selected glyph quad emits its source bytes up to the next glyph minus `[..]` style tags,
escaped `\[` as literal, decor quads never leak; cold path).
Render (static): `RichLabel_renderFn(panel, rend, cmd, surfaceW, surfaceH, x, y, w, h)`: bg fill; if
`highlightable` selection present, `drawSelectionSpans` (per-line `Vk_fillRect`, lines
clustered by `|dy| > 0.5 * max glyph height`, span = min origin → max origin+advance);
then per `TextQuad q`: unpack color; `qx=x+q.x, qy=y+q.y`;
`decor!=NONE||textureId<0` => `Vk_fillRect` solid line; else `isColor` => `Vk_drawColorGlyph`;
else `Vk_drawSDFText(...,bold,0.5,...)` (smoothness hardcoded `0.5`, unlike `Label.smoothness`).

### TextQuad selection fields (text/rich_text.h)

`TextQuad` carries two selection-mapping fields written by `RichText_layout`:
`int32_t charIndex` = source byte index of the glyph (`-1` on decor/shadow quads);
`float advance` = pen advance in points (`>0` only on real glyph quads). Shadow and
decor quads get `charIndex=-1, advance=0` so pointer hit-testing and selection spans
consider only real glyphs.

---

## 30. Typography

Role-styled pure display node (no custom renderFn in this snapshot).

```c
typedef struct Typography { Panel base; char *text; int32_t role; Font *font; uint32_t color; } Typography;
// TYPOGRAPHY_H1(0), H2(1), H3(2), BODY(3), CAPTION(4)
```

| Field | Default | What |
|-------|---------|------|
| `text` | `nullptr` | Owned UTF-8 (free+strdup). |
| `role` | `BODY` | `0..4`. |
| `font` | `nullptr` | Borrowed optional descriptor. |
| `color` | white | |

Functions: `Typography *Typography_0(void)` (`TYPE_TYPOGRAPHY_SINGLETON`);
`Typography_1(text)`; `Typography_2(parent,text)`; `setText/setRole/setFont/setColor`
(+dirty); `void Typography_free` (frees text, never font);
`getText/getRole/getFont/getColor` (null-safe).

---

## 31. Kbd

Keyboard-shortcut chip (`Kbd_1("⌘K")`), pure display node.

```c
typedef struct Kbd { Panel base; char *keys; uint32_t bg, fg; } Kbd;
```

| Field | Default | What |
|-------|---------|------|
| `keys` | `nullptr` | Owned key string. strdup+free+dirty. |
| `bg` | `0xFFF2F2F2` | Chip bg. |
| `fg` | `0xFF1A1A1A` | Chip fg. |

Functions: `Kbd *Kbd_0(void)` (`TYPE_KBD_SINGLETON`); `Kbd_1(keys)`; `Kbd_2(parent,keys)`;
`setKeys/setBg/setFg` (+dirty); `void Kbd_free` (frees keys); `getKeys/getBg/getFg`.

---

## 32. Dialog

Modal family root. Inherits Frame (own window + handler link); base for
OptionDialog, InputDialog, FileDialog, ColorDialog.

```c
typedef struct Dialog { Frame frame; Frame *handler; char *title; Panel *content;
    bool modal; bool clinging; bool open;
    void (*onClose)(void *ctx); void *ctx; } Dialog;
```

| Field | What |
|-------|------|
| `frame` | Inherited Frame (own R1 window, R3 graphics, child-dialog registry). |
| `handler` | Owner/parent frame (nullable). Set by `Dialog_show(dialog, frame)` / `Dialog_setHandler`. |
| `title` | Owned title (dialog copies caller string; caller may stack-allocate). |
| `content` | Body node attached on open. BORROWED — dialog never dups/frees; caller retains lifetime. |
| `modal` | `true` captures focus exactly like clinging until closed — even when clinging was never set. Blocks handler close via `Frame_canClose`. |
| `clinging` | Locks focus to dialog and prevents handler frame from closing. |
| `open` | True while open/visible. |
| `onClose/ctx` | Borrowed close slot. |

Present with `Dialog_show(dialog, frame)` (binds the parent frame, ensures the
window, captures focus and stacks handler-below/dialog-on-top while modal or
clinging) or `Dialog_open(dialog)` (no parent). While modal/clinging the
dialog also retargets the global event bridge to its content — pointer and
key events drive the dialog, not the parent tree — and restores the prior
wiring on close (nested dialogs stack LIFO-clean). Enforcement is threefold:
(1) the handler OS key gate closes (`Window_setKeyEnabled` false — AppKit
refuses the parent key, so clicks on the parent are dead: no flash, no gap;
render + order unaffected, both scenes keep presenting); (2) the pair is
glued (`Window_attachChild` — handler below, dialog on top, one unit above
other apps); (3) the bridge retarget above. A held dialog is not minimizable
(yellow dimmed, restored on close). Close reverses all of the above and
restores key only when no other holder still governs the handler. The
dialog's own red button routes through `Dialog_requestClose` (full cleanup,
AppKit close cancelled — never a raw window close that would leave a zombie
holder claiming `open` with bridge, gate, and glue still held). Focus
re-asserts to the deepest open modal/clinging dialog as fallback; close
refocuses the handler. No `OverlayRoot` needed for this window-per-dialog path.

---

## 33. AlertDialog

Confirm/deny. Header only. IS-A Dialog via embedding (same pattern as Dialog embeds Panel).

```c
typedef struct AlertDialog { Dialog base; int32_t variant;
    char *message, *confirmLabel, *cancelLabel;
    void (*onConfirm)(void *ctx); void (*onCancel)(void *ctx); void *ctx; } AlertDialog;
// ALERT_INFO(0), WARN(1), DANGER(2)
```

All three strings owned; callbacks + ctx borrowed. `cancelLabel==nullptr` = no cancel.
Functions declared: `AlertDialog *AlertDialog_0(void)`; `AlertDialog_1(parent)`.

---

## 34. FileDialog

Modal browser. Fully implemented except IO scan (`refresh`/`choose` are `;;INCOMPLETE`).

```c
#define FILEDIALOG_PATH_MAX 512
#define FILEDIALOG_FILTER_MAX 64
typedef struct FileDialog { Panel base; char path[512]; char filter[64];
    bool showHidden; List *entries; int32_t selected;
    void (*onOpen)(void *ctx); void (*onCancel)(void *ctx); void *ctx; } FileDialog;
```

| Field | Default | What |
|-------|---------|------|
| `path[512]` | `""` | Inline current dir, truncated `511+NUL`. `nullptr`=>`""`. |
| `filter[64]` | `""` | Inline ext filter, `63+NUL`. |
| `showHidden` | `false` | Hidden-file predicate flag. |
| `entries` | `nullptr` | Entry names (`char*` via `List_get`/`uintptr_t`); null until IO pass. |
| `selected` | `-1` | Index into entries. |
| `onOpen/onCancel/ctx` | `nullptr` | Borrowed; set without dirty. |

Functions: `FileDialog *FileDialog_0(void)` (`TYPE_FILEDIALOG_SINGLETON`); `FileDialog_1(parent)`;
`void FileDialog_refresh(d)` (stub); `bool FileDialog_choose(d,index)` (stub, always false);
`setPath/setFilter` (truncated memcpy + dirty); `setShowHidden/setSelected` (+dirty);
`setOnOpen/setOnCancel/setCtx` (assign only);
`getPath/getFilter` (never null: `""` on null `d`) / `isShowHidden` / `getSelected` /
`entryCount` (`0` if null/empty) / `getEntryAt(d,i)` (bounds-checked) / `getOnOpen/getOnCancel/getCtx`.

---

## 35. ColorDialog

Picker in a modal. Header only. Twin distinction: inline widget twin is `field/colorpicker.h`;
this is the modal shell hosting picker-grade state.

```c
typedef struct ColorDialog { Dialog base; uint32_t color; float h, s, v;
    bool showAlpha; void (*onChange)(void *ctx); void *ctx; } ColorDialog;
```

`color+h,s,v` are value compartment (not pointers); `onChange/ctx` borrowed.
Functions declared: `ColorDialog *ColorDialog_0(void)`; `ColorDialog_1(parent)`.

---

## 36. Picture

Retained-mode off-heap image node. Generic `void *image` until `Image.h` is ported — BORROWED.

```c
#define PICTURE_AUTO -1.0f
typedef struct Picture { Panel base; void *image; float imageSizeW, imageSizeH;
    float cropX1, cropY1, cropX2, cropY2; bool hasImageSize, hasCrop; } Picture;
```

| Field | Default | What |
|-------|---------|------|
| `base` | `Panel_0` | No custom renderFn in this snapshot — leverages base render, overridden via `Panel_setRenderHandler`. Label sharp path already calls `Vk_drawTexture(...,PICTURE_MODE_FIT,...)` showing intended UV/fit vocabulary. |
| `image` | `nullptr` | Borrowed/off-heap asset. Never copied — avoids large memcpy/double-free. |
| `imageSizeW/H` | `0` | Explicit display size. Header documents `-1` auto-from-aspect, but `.c` zeroes + `hasImageSize` flag — caller must `setImageSize` or renderer derives aspect. |
| `cropX1/Y1/X2/Y2` | `0` | Normalized UV top-left/bottom-right. Selects sub-UV without duplicating texture. |
| `hasImageSize/hasCrop` | `false` | Override-active flags. |

Functions: `Picture *Picture_0(void)` (`TYPE_PICTURE_SINGLETON`); `Picture_1(image)`;
`getImage/setImage` (+dirty); `setImageSize(p,w,h)` (+dirty);
`getImageSize(p,*w,*h)` (null-tolerant outs); `hasImageSize`;
`setCrop(p,x1,y1,x2,y2)` (+dirty); `getCrop` (null-tolerant); `hasCrop`;
inline facades `Picture_setLocation/Size/ParentAnchor/SelfAnchor/BackgroundColor`.

---

## 37. Plot

Data-first chart (ggplot-inspired, single class). `xs/ys` BORROWED — never owned/copied/freed.
Kinds `LINE/BAR/SCATTER/HIST/AREA`. Proposed `DONUT/SPARK/HEAT` + tooltip picking later
(`hitPick` stub exists).

```c
typedef enum PlotKind { PLOT_LINE=0, PLOT_BAR, PLOT_SCATTER, PLOT_HIST, PLOT_AREA } PlotKind;
typedef struct Plot {
    Panel base; int32_t kind; Buffer *xs, *ys; size_t count; bool autoRange;
    float minX, maxX, minY, maxY;
    uint32_t lineColor, fillColor, gridColor, axisColor;
    char *title, *xlabel, *ylabel; bool showGrid, showAxes, showLegend;
    void (*onSelect)(void *ctx); void *ctx;
} Plot;
```

| Field | Default | What |
|-------|---------|------|
| `kind` | `LINE` | |
| `xs/ys` | `nullptr` | Borrowed float Buffers. Caller keeps alive while attached. Avoids per-frame copies. |
| `count` | `0` | Sample count over xs/ys. |
| `autoRange` | `true` | Recompute ranges from data on render (contract). |
| `minX/maxX/minY/maxY` | `0/1/0/1` | `setMin/Max/XRange/YRange` auto-swap if lo>hi. |
| `lineColor` | `0xFF3A86FF` | |
| `fillColor` | `0x663A86FF` | |
| `gridColor` | `0xFF3A3A3A` | |
| `axisColor` | `0xFFFFFFFF` | |
| `title/xlabel/ylabel` | `nullptr` | OWNED (free old, malloc+memcpy new, NULL clears). |
| `showGrid/showAxes/showLegend` | `true/true/false` | |
| `onSelect/ctx` | `nullptr` | Borrowed pick slot, no dirty. |

Functions: `Plot *Plot_0(void)` (`TYPE_PLOT_SINGLETON`); `Plot_1(parent)`;
`void Plot_autorange(p)` (`;;INCOMPLETE`); `int32_t Plot_hitPick(p,x,y)` (stub, `-1`);
`void Plot_free(p)` (frees titles, nulls borrowed xs/ys/callbacks);
`setKind/setData(xs,ys,count)` (borrowed assign, no copy) / `setAutoRange` /
`setMinX/MaxX/MinY/MaxY/setXRange/setYRange` (swap-aware) /
`setLineColor/setFillColor/setGridColor/setAxisColor` /
`setTitle/setXLabel/setYLabel` / `setShowGrid/setShowAxes/setShowLegend` (all +dirty) /
`setOnSelect/setCtx` (no dirty);
getters `getKind/getXs/getYs/getCount/isAutoRange/getMinX/getMaxX/getMinY/getMaxY/getLineColor/getFillColor/getGridColor/getAxisColor/getTitle/getXLabel/getYLabel/isShowGrid/isShowAxes/isShowLegend/getOnSelect/getCtx`.

---

## 38. Scene / Scene2D / Scene3D

Scene root. Minimal by design: `Panel+mode+presentMode`, virtual size =
`Container w/h`. No `Surface*` stamp slot — stamping lives in the present pass,
not the struct. Present scales the retained virtual scene per `mode` so resize
never re-renders. Where a scene's pixels land is `presentMode` (the
Single-Seam Canvas Law): COMPOSITED scenes own a retained offscreen `VkLayer` flight target in
graphvex that the canvas collages as a textured quad; INLINE scenes paint
straight into the enclosing board pass via their render handler. There is no
DIRECT mode: the per-scene `CAMetalLayer` + `VkPane` swapchain is retired
(single on-screen canvas only). The flight machinery (registry, dual flight
slots, acquire/render semaphores, bounded 100ms fences, dirty bit) serves the
compositable color image the canvas samples.

```c
#define SCENE_MODE_STRETCH 0
#define SCENE_MODE_FIT 1
#define SCENE_MODE_PIXEL 2
#define SCENE_PRESENT_COMPOSITED 0 // retained VkLayer target, sampled by the canvas
#define SCENE_PRESENT_INLINE 1     // paints into the enclosing board pass (render handler)
typedef struct Scene { Panel base; int32_t mode; int32_t presentMode; } Scene;
typedef struct Scene2D { Scene base; } Scene2D; // dispatch tag, no payload
typedef struct Scene3D { Scene base; } Scene3D;
```

| Field | Default | What |
|-------|---------|------|
| `base` | `Panel_0`, zero size | Hierarchy + `Container w/h` = virtual size. |
| `mode` | `PIXEL` | `STRETCH`=asymmetric fill; `FIT`=uniform letterbox; `PIXEL`=1:1 top-left (resize reveals more canvas). |
| `presentMode` | `COMPOSITED` | Destination of the scene's pixels (the Single-Seam Canvas Law). COMPOSITED = offscreen VkLayer sampled by the compositor, zero per-scene Metal surfaces. INLINE = paints into the board pass via handler. |

Functions: `Scene *Scene_0(void)` (PIXEL, COMPOSITED); `Scene_2(w,h)` (+`Container_setSize`);
`Scene_3(w,h,mode)` (+validated mode); `Scene2D_0(void)` / `Scene3D_0(void)`
(`allocScene(TYPE_SCENE2D/3D_SINGLETON)` casts); `int Scene_getMode` (`PIXEL` NULL);
`void Scene_setMode` (range-checked + dirty); `int Scene_getPresentMode` (`COMPOSITED` NULL)
`void Scene_setPresentMode` (range-checked + dirty; detach/attach of the
COMPOSITED layer happens on the next attach pass); `float Scene_getVirtualWidth/Height`
(`Container_getWidth/Height` via `sceneLayout` hoist `&s->base.base`);
inline facades `Scene_setLocation/Size/ParentAnchor/SelfAnchor/BackgroundColor`
(+ `Scene2D_*`/`Scene3D_*` twins).

---

## 39. RichText (`text/rich_text.h/.c`)

Styled layout model consumed by `RichLabel`/`RichTextPanel`/`MarkdownPanel`.

```c
typedef enum { WRAP_NONE, WRAP_WORD, WRAP_CHAR } WrapMode;
typedef enum { ALIGN_LEFT, ALIGN_CENTER, ALIGN_RIGHT, ALIGN_JUSTIFY } TextAlign;
typedef enum { DECOR_NONE, DECOR_LINE, DECOR_DASH, DECOR_SQUIGGLE } TextDecoration;
typedef struct TextStyle { uint32_t setFlags; Font *font; float size; uint32_t color;
    bool isBold; TextDecoration decor; uint32_t decorColor;
    float letterSpacing, lineSpacing; bool hasShadow;
    float shadowX, shadowY; uint32_t shadowColor; } TextStyle;
typedef struct TextRun { RunType type; int startChar, length;
    TextStyle computedStyle; TextAlign align; } TextRun;
typedef struct TextQuad { float x,y,w,h, u0,v0,u1,v1; uint32_t color;
    int32_t textureId; float bold; bool isColor; TextDecoration decor; } TextQuad;
typedef struct RichText { char *rawString; TextStyle *styles; size_t styleCapacity;
    TextRun *runs; size_t runCount, runCapacity; TextQuad *quads;
    size_t quadCount, quadCapacity; float layoutWidth, layoutHeight; WrapMode wrapMode; } RichText;
```

- `rawString` owned UTF-8 incl `[tag]` markup; `styles` dictionary (cap 16, grows `id+16`);
  `runs` shaped segments (byte offsets, CSS-cascade merged `computedStyle`, `align`);
  `quads` renderer-ready glyph rects + UV + `textureId` (per-page atlas, `-1`=solid decor),
  `bold` (`0` / `0.04` bold / `-0.5` blur-shadow signal), `isColor` (emoji color path);
  `layoutWidth/Height` last extents; `wrapMode` policy.
- `RichText *RichText_new(void)` (`TYPE_RICHTEXT_SINGLETON`, zeroed, `wrapMode=WORD`);
  `void RichText_free(rt)`; `void RichText_setStyle(rt,id,font,size,color,bold,decor)`
  (`setFlags=FONT|SIZE|COLOR|BOLD|DECOR`, `decorColor=color`);
  `void RichText_setShadow(rt,id,dx,dy,color)` (requires `id<cap`);
  `void RichText_setWrapMode`; `void RichText_setString(rt,str)` (free+strdup, reset runs,
  parse `[a|b|c]` tags: `\[` escaped, `n`=newline, `l/c/r/j`=align, numeric=style id merged);
  `void RichText_layout(rt,maxWidth)` (per run: vmetrics+scale, UTF-8 decode, kerning,
  wrap check `maxWidth>0 && cursorX+advance>maxWidth` with WORD-only-on-space / CHAR-always,
  shadow quad first then main quad, decor quad `y=cursorY+ascent+2`, alignment shift,
  finalize `layoutWidth/Height`).

---

## 40. text_core (`text/text_core.h`, `text_core_stub.c`, `objc/text_core.m`)

Native seam. `float TextCore_backingScale(void)` = `NSScreen backingScaleFactor` else 1
(Retina points->pixels; never hardcoded 2.0).

`bool TextCore_rasterLine(utf8,family,pxHeight,argb,&outRgba,&outW,&outH)` forwards to `TextCore_rasterStyled` with default typography settings.

`bool TextCore_rasterStyled(utf8,family,pxHeight,argb,style,&outRgba,&outW,&outH)`:
Takes `const TextStyleDescriptor *style` containing:
- `bool ligatures`: CoreText `kCTLigatureAttributeName` (`@(1)` / `@(0)`).
- `float spacingWidth`: Letter tracking/kerning delta in points (`kCTKernAttributeName`).
- `float spacingHeight`: Line leading delta in points between `\n` rows.
- `UnderlineStyle underline`: `UNDERLINE_NONE`, `UNDERLINE_BASIC` (straight baseline stroke), `UNDERLINE_STRIKETHROUGH` (middle stroke), `UNDERLINE_JAGGED` (sinusoidal/zigzag error wave).
- `uint32_t underlineColor`: Custom stroke color (defaults to `argb` text color if `0`).
- `int mnemonicIndex`: Character offset for native accelerator underline (`-1` = none).
- `int selectionStart`: Character start index of selection range (`-1` = none).
- `int selectionEnd`: Character end index of selection range (`-1` = none).
- `float highlightRadius`: Corner radius in points for selection rounded rect (default `3.0f`).
- `uint32_t highlightColor`: Packed `0xAARRGGBB` selection background fill (default `0x662563EB`).

macOS impl: `CTFontCreateWithName` -> Helvetica fallback; `a==e` glyph test -> Menlo fallback;
splits `\n` <=64 rows, one `CTLine` each, `w=ceil(maxAdv)+2, h=ceil(totalH)+2*nlines`
(clamp 8192x4096), RGBA bitmap (premultLast, antialias on, font-smoothing off,
subpixel positioning+quantization on), stack bottom-up, paints rounded selection highlight rectangle (`CGPathCreateWithRoundedRect`) under selected character ranges, draws glyphs cleanly over fill, strokes underlines directly in CGContext, returns malloc'd RGBA.
Non-Apple stub: `backingScale`=>`1.0`; `rasterLine`/`rasterStyled` validates, nulls outs, always false —
forces `Label.ensureRaster` failure => SDF fallback owns text.

`int32_t TextCore_lineOffsets(utf8,family,pxHeight,ligatures,kernPts,outPts,cap)`:
per-glyph pen offsets for single-line text in points — one entry per UTF-8 byte plus a trailing
total advance (`strlen+1` entries, fail-closed `-1` when multiline/empty/bad/cap-short, never
partial). Same font fallback chain, ligature flag, and tracking as the raster, so the table matches
paint exactly; the Label hit-test shares it with the baked highlight. Cold path only (label raster
rebuild). Stub always returns `-1` and the caller keeps its uniform fallback.

Clipboard seam: `TextCore_setTestClipboard(bool)` routes `copyToClipboard`/`pasteFromClipboard`
through an in-memory buffer (both the ObjC backend and the stub) so unit tests never write the
real NSPasteboard. Defaults to disabled; cold-test-only, never called from tick/render paths.

---

## 41. Compositor (`darling/compositor.h/.c`)

Header contract: `Darling_initCompositor(Window*)`, `Darling_shutdownCompositor()`,
 `Darling_preFrame(Window*,drawW,drawH,userdata)`, `Darling_renderFrame(cmdBuffer,drawW,drawH,userdata)`,
 `Darling_compositorSettled(void)` (true when no layer submit flies),
 `Darling_compositorIdleForResize(void)` (settled alias for layer/texture resize callers).
 STACK LAW (front->back): `seam canvas (single on-screen CAMetalLayer) -> blurred glass window` —
 Layer 1 = the Frame seam
 canvas — the window's ONLY on-screen Metal layer (the Window Compositing Layer Order Law,
 the Single-Seam Canvas Law): the seam pass composites the two retained
 board images (content top, scene bottom) composited at each board's OWN extent pinned
  top-left — never stretched to the drawable — and presents on demand.
  Layer 2 = scene/content full-window BOARDS as retained OFFSCREEN `VkLayer` targets
  (fixed pixel size, never a CALayer, never in the window tree, never rebuilt on resize —
  the Single-Seam Canvas Law), plus depth-1 `VkLayer` targets for EVERY first-generation
  child of each board (scenes and plain UI alike — Input included) sampled into the board
  pass. Loop1 depth-1 collage doctrine: retained presentables
  are EXACTLY the scene panel, the content panel, and their first-generation children;
  Loop1 collages published frames and paints nothing else; depth below 1 is each
  child's private affair. Every panel is a Vulkan rect painting into its retained
  target or the board pass; the seam pass collages the published board images. Resize: the seam
canvas frame tracks the window natively (autoresizingMask + the Native Pixel Law
  drawableSize contract); the resize hook drives the per-step render-then-present
  (`frameCocoaResizeHook`: chase drawableSize + `Frame_resize` + dirty re-arm +
  `GfxLoop_modalTick` — synchronous present at the NEW size within the step, with
  the swapchain rebuilt immediately on extent drift, no throttled drops; see
  section 55.2); boards resize on pixel drift (no-op when unchanged, the
  Single-Seam Canvas Law; idle-gated to the layer flight) and a board that lags a step
  composites pinned top-left at its own extent, never stretched.

 Private: `paintChildIntoPass(cmdBuffer,child,winW,winH,kx,ky,drawW,drawH,paintUI)` —
 one child into a board or retained-layer pass (shared by `Darling_renderFrame` with
 `paintUI=false` and `Darling_layerRender` subtrees with `paintUI=true`). Three
 destination branches, in order (Rule 14): retained layer-backed children are
 SAMPLED — `VkLayer_composite` draws the published frame as
 a textured quad at the anchor rect and returns (the child's render handler is never
 invoked here: composite != render); scenes and plain UI paint via handler or
 tri/`Vk_fillRect` fallback.
  - `Darling_preFrame`: `winW/H=Window_width/height`; boards FIRST:
    `Darling_attachPanelBoards(window,winW,winH)` attaches retained offscreen board
    targets (`PanelCocoa_newBoard`, one fixed-size `VkLayer` chain each) to scene/content
    panels (new board = register; existing = `VkLayer_resize`, no-op on unchanged extent);
    if contentPanel: `Container_setSize(content,winW,winH)` (compositor drives layout by
    writing Container size through embedded prefix); `Window_attachPanes` (inert stub)
    + `Darling_attachLayers(window,content,winW,winH)` AND
    `Darling_attachLayers(window,scene,winW,winH)` (EVERY first-generation child of
    each board — scenes and plain UI alike — as `VkLayer` targets at fixed pixel size,
    dirty=true on register per the Single-Seam Canvas Law; iterated via
    `Panel_childCount`, never hardcoded counts,
    per the Dynamic Scalability & Anti-Hardcoding Law; resize gated on
    `Darling_compositorIdleForResize` so a target never rebuilds under a submitted
    composite) + `Window_compositePanes` on change (inert stub; clears
    tree-dirty); `Darling_propagatePaneDirty` re-arms child/board layer
    demand (owner-subtree dirt re-arms the child's own target; a depth-1 child
    PUBLISH arms board demand one hop via a per-board `VkLayer_presentCount`
    snapshot — dirt dies on publish inside `VkLayer_visit`, so dirt is never
    the publish signal; content-child demand arms ONLY the content board,
    scene demand ONLY from the scene board's own children); then `VkLayer_visit()` renders
    every dirty retained target (boards + depth-1 children) into its offscreen flight
    image BEFORE the seam pass samples them — same-queue order makes visit-then-composite
    safe (registration demands the first render); if scenePanel: size to window,
    decode bg -> `Vk_setClearColor`; else if `root!=contentPanel` same from root bg.
  - `Darling_renderFrame` (Loop1 seam collage, the Present-On-Demand Law,
    composite != render): the seam pass. EVERY registered board is sampled on
    EVERY present — sampling is one draw call per board (cheap) and the
    fresh-cleared swapchain image would ERASE a skipped board, so demand gates
    board RE-RENDER (visit-side dirty), never sampling; unpublished boards
    no-op inside `VkLayer_composite`. A successful board composite clears that
    board's tree dirt (scene and content alike) so clean boards CLEAN-SKIP.
    Window-level `demanded` (any board demand via tree/target dirt or depth-1
    child present-count delta, never-presented,
    or live-resizing) presents exactly once per tick, else rests (idle rest). Scene board
    (bottom) then content board (top), each via `VkLayer_composite` at the board's OWN
    pixel extent pinned top-left in the drawable — NEVER stretched to fill it, so a board
    target that lags the window for a step pins its last publish crisply instead of
    gravity-resizing it (the Continuous Real-Time Live Resize Law; a converged board —
    extent equal to the drawable — samples identically to the old full-extent quad). Each
    board target already collaged its depth-1 children at preFrame's `VkLayer_visit`
    against the CURRENT panel size every tick, so a pinned composite still reflects the
    updating extents. Minimized windows suppress.
    When no board is registered, iterate ROOT children via shared
   `paintChildIntoPass(...,paintUI=false)`: resolve each, clip to draw extents, skip zero-area;
   COMPOSITED scenes SAMPLED as textured quads (sampling a published target is the
   composite, never a re-render — Rule 14);
   if nativeContent and type NOT a scene singleton => `return` (already composited by AppKit;
   stamping again would double-render); Scene with handler => handler in device px;
   Scene without => viewport/scissor to panel rect, tri draw, restore full; non-scene only when
   `!nativeContent`: handler or `Vk_fillRect`.
  - `Darling_layerRender(cb,w,h,owner=Panel*)`: retained-target render hook installed via
    `VkLayer_setRenderer` — runs inside each target's OWN begun
    render pass (never the shared batch CB, so steady rendering proceeds regardless of batch
    flight). Leaf target: resolves `Panel_getRenderHandler`; handler called with
    `(panel,nullptr,cb,w,h,0,0,w,h)`; scene with no handler falls back to the spinning tri
    (viewport/scissor = full target, push `uTime=(NanoTime_now()-animStart)/1e9`, bind tri
    pipeline, Draw(3)). Board target (scene/content panel WITH children): depth-1 collage —
    each first-generation child with a retained target is SAMPLED via `VkLayer_composite`
    at its anchor rect (unpublished children skip, keeping prior canvas content);
    children without a target fall back to
    `paintChildIntoPass(...,paintUI=true)` — children resolve against the board's own
    point size (`Darling_getPanelSize`) scaled to target pixels.
    Depth below 1 is each child's private affair:
    a child target paints its own subtree directly. Target owns its whole extent — NO window-absolute transform.
   Resize contract: handler-triggered resize-class work (dimension-changing
   `Texture_replaceRaw`) must consult `Darling_compositorIdleForResize()` first, else defer
   to same-size update or skip.
 - `darlingGfxFrameFn` demand probe (the Present-On-Demand Law): ticks the focused
   Input's caret; re-arms present demand on live resize, `VkLayer_hasDemand()` (retained
   boards + COMPOSITED re-arms) or a dirty panel
   tree — probe free (thread 0, struct reads only), present gated on demand.
   - `FrameCocoa_resizeRenderHook` (thread 0, per drag step — the effective seam):
     re-chases `drawableSize` in rounded native px from the live OS bounds
     (never the truncated cache — a Retina sub-point step is a whole pixel),
     runs ONE `Frame_resize` (render + present live inside it; the `onResized`
     bridge stands down while live so no step lays out twice), then re-arms
     the client dirty and calls `GfxLoop_modalTick()` — the dirty-gated modal
     tick presents ONLY the resizing window synchronously, best-effort with
dirty retained on drop: `Darling_preFrame` catch-up
      (layout + `VkLayer_visit` publishes boards at the fresh extent), then
      `Vk_clearPresent()` (seam swapchain rebuilt immediately
      on extent drift, no throttled drops — see section 55.2). `Darling_resizeRenderHook`
     (compositor fallback, overwritten by FrameCocoa) runs the same body directly
     for any frame that never attaches its cocoa shim.
  - `darlingWindowPresentFn` infancy rule (first-paint robustness): while the
    frame's `presentedFrames < 3` (`DARLING_INFANCY_PRESENTS`, file-local in
    `compositor.c`), demand-gating is off — every tick runs the shared
    `darlingPresentResizeSequence` body (ready/minimized/extent guards stay);
    each success bumps `presentedFrames`, each failure holds it for a retry,
    so the loop never settles into on-demand rest on an unconfirmed (phantom
    first-present) success. At 3 it emits one `GRAPHICS_VK_STATS`-gated settle
    line (`settled into on-demand rest after 3 infancy presents`) and takes the
    normal on-demand path thereafter; per-attempt lines (`infancy present N/3
    ok` / `infancy present failed`) prove delivery in the next trace instead of
    inferring it from QueuePresent traces. `hasPresented` latching is untouched
    (feeds Loop2 rest).
 - `Darling_initCompositor`:
    `VkView_refreshAll`, `VkSceneCanvas_initModule`,
    `Texture_initModule`, `SdfGpu_initModule`;
`Vk_setPreFrameRenderer(Darling_preFrame)`, `Vk_setFrameRenderer(Darling_renderFrame)`,
     `VkLayer_setRenderer(Darling_layerRender)` (boards + COMPOSITED targets) — after `Vk_init`,
     register always finds a live device, Rule 11.5.
  - `Darling_shutdownCompositor`: null renderers (layer chains are owned by `VkLayer_shutdown`);
    `Texture_shutdown`, `SdfGpu_shutdown`,
    `VkView_shutdown`, `VkSceneCanvas_shutdownModule` (Rule 26 order preserved).
    Teardown order Rule 26: Window -> compositor -> Vk -> threads -> arena.
    Proof: `_tests/darling/compositor_batch_test.c` (settled/idle + shutdown).

---

## 42. WindowServer / Metal / Vulkan end-to-end

Pixel journey (single-seam board path):

1. `Darling_preFrame` sizes content/scene panels to window, attaches Metal
   boards (`PanelCocoa_newBoard`, retained offscreen `VkLayer` targets) and
   depth-1 child targets (`Darling_attachLayers`), then
   `VkLayer_visit` publishes every dirty retained target (boards + children)
   into its offscreen flight image.
2. `Darling_renderFrame` (the seam pass) composites the two published board
   images — scene bottom, content top — into the window's SINGLE on-screen
   `CAMetalLayer` and presents on demand. `contentsScale =
   TextCore_backingScale()` gives exact 1:1 Retina mapping (Rule 12: points
   frame, pixel backing). `geometryFlipped=YES` matches Vulkan top-down;
   `contentsGravity=TopLeft`, `anchorPoint=(0,0)`, `presentsWithTransaction=YES`
   joins presents to the WindowServer transaction. No per-scene or per-child
   `CAMetalLayer` exists anywhere in the tree; the seam canvas is the only
   Metal surface.
3. `Window_attachPanes` / `Window_compositePanes` are inert `;;INTENTION`
   stubs retained as no-op seams (the old per-pane CALayer positioning is
   retired with the `VkPane` registry).
4. `Darling_layerRender` paints each retained target's own subtree (leaf
   handler or board subtree collage) inside that target's own begun pass;
   the seam pass then samples the published boards. WindowServer/CoreAnimation
   composites the single canvas layer onto the blur view. Each pixel written
   once by its owner.

Single-seam journey (the Single-Seam Canvas Law):

1. `FrameCocoa_attach` creates the seam `CAMetalLayer` (`vexgraph.seam`,
   BGRA8Unorm, `geometryFlipped=YES`, non-opaque, `contentsGravity=kCAGravityTopLeft`,
   `anchorPoint=(0,0)`, `presentsWithTransaction=YES` (WindowServer-synced
   presents), `contentsScale = TextCore_backingScale()`,
   `drawableSize = (w * scale) × (h * scale)` — Rule 12: physical pixels for the
   swapchain, logical points for the layer frame) and publishes the maximum
   drawable extent to `Vk_seamSetMaxExtent` (the fixed-buffer plaster: the
   monitor-sized chain is allocated once, the window is a top-left CROP of it —
   window resizes cost only a render area + layer frame, never a rebuild).
2. Boards: `PanelCocoa_newBoard` registers the scene/content panels as retained
   OFFSCREEN `VkLayer` targets (full-window, `Darling_attachPanelBoards` in
   `preFrame`); boards resize WITH the window
   (`VkLayer_resize` at settle — no-op when unchanged); mid-drag the frozen
   board stays pinned TopLeft (freeze-exact — the frozen drawable is never
   stretched or scaled; the seam past its extent is the layer's transparent
   `opaque=NO` remainder, blur shows through).
3. Every `Kernel_tick`: `darlingGfxFrameFn` probe re-arms demand; on demand the
   loop runs `Darling_preFrame` (layout + `VkLayer_visit` publishes), the seam
   pass composites, and one `Vk_clearPresent` paints the frame into the single
   canvas layer. Retained targets render on demand into their offscreen flight
   images (bounded 100ms fence wait + 25ms acquire, Rule 27; auto-rebuild on
   `OUT_OF_DATE` only for the seam chain), then `Darling_layerRender` records
   inside each target's own pass.
4. **Live resize = layer-motion on thread 0, rendering frozen mid-drag (Rule 11.6):**
   `AntiVulkanView` sets `Window.liveResizing` (atomic) in `viewWillStartLiveResize`/`viewDidEndLiveResize`.
   While set, thread 0 is inside AppKit's modal tracking loop — it runs the
   resize hook's synchronous present at the NEW size each step (chase
   drawableSize + `Frame_resize` + `GfxLoop_modalTick`: layout + freeze-exact
   direct paint of both boards through the shared painter into the seam image,
   one synchronous present) and nothing else
   (`Window_compositePanes` early-returns while the flag is set — inert).
   The drawable-to-layer mapping is WindowServer-accelerated: the seam's
   `autoresizingMask` + `anchorPoint (0,0)` make CoreAnimation lay it out
   INSIDE the window-resize transaction — edge-locked on the same vsync as
   the window edge, zero CPU math, zero catch-up (per-event explicit `setFrame:`
   would fight the accelerated pass and trail the live edge by a beat — the
   right/bottom "catching up" artifact; exact frames re-apply at settle).
   `Darling_preFrame` runs its live branch (layout + clear-color refresh only,
   zero layer mutation), so the work stays on thread 0 — no worker/thread-0
   layout race can tear the anchor math. The present worker
   (`kernel_present_job` / `app_present_job`) is gated out of requesting
   presents while live (the resize hook is the sole presenter):
   the board stays at its current extent — and its `contentsGravity` stays
   `kCAGravityTopLeft` from `viewWillStartLiveResize` through settle (freeze-exact).
   The gravity is state-gated —
   `applyLayerGravity` (TopLeft steady-state policy) and the render-gen rebuild both
   skip while the flag is set; the seam layer's
   `presentsWithTransaction` stays YES throughout the drag and settle.
   `Window_width/height` read atomic
   thread-0-written caches, never AppKit, so layout tracks the live
   size safely. On settle the flag clears before `resizeRenderFn` fires; the next pass
   runs exactly ONE board rebuild + ONE final re-render at the true final size.
   Per-drag-frame rebuilds/re-records are the size-proportional-lag defect.
5. `SdfGpu`/`Texture`/`VkView`/`VkSceneCanvas` modules initialized once in init; fence-bounded
   offscreen submit (100ms) keeps teardown alive.

Why this way: Vulkan does what it is best at (tri/SDF/texture quads, compute JFA bake),
CoreText does what it is best at (hinted native glyphs), CoreAnimation/WindowServer does
what it is best at (Retina-exact compositing, resize without repaint). Off-heap assets
(`mmap` `.anti`, `.antifont` atlases) fault in on demand, never heap-copied. UI is retained
(`Container/Panel` tree + per-panel surfaces + Thread-0 `Anim_tick` beside layout).
CPU `Raster/Surface` stays as headless/test fallback.

Gotchas: retained-offscreen targets are exact-size — painters clamp viewports/scissors to the
target extent. `contentsScale` must be backing scale or text blurs. Bounds panels must never
own a board target (gallery `~900x16k` CLEAR panel stays backing-free).
`renderNativeContent` skips `scenePanel` child; `renderFrame` skips non-scenes when native.

---

## 43. Vulkan shaders + SPV

Blobs in `vulkan/spv/`: `sdf_jfa.spv`, `sdf_combine.spv`, `text_sdf_vert/frag.spv`,
`texture_quad_vert/frag.spv`. Built by `vulkan/shaders/build_shaders.sh`
(`glslangValidator -V` x6). Only UI-owned shaders here (textured quads, SDF text, JFA bake);
core (`hello_triangle`, `solid_quad`) lives in vexspoke. Canonical home migrating to
`graphvex/shader/spv/` (`ANTI/VEX_SPV_DIR -> exe/spv -> Resources -> CWD`).

| Shader | Role |
|--------|------|
| `sdf_jfa.comp` (16x16) | Seed + jump-flood for baked SDF atlases. One dispatch covers 2048^2 page (16px gutters = 2x `SDF_PADDING`). Bindings: 0=`Cov` readonly (1M words coverage), 1=`Sdf`, 2/3=`SeedsA/B[4194304]`. Push: `mode(0 seed/1 flood), dstBuf, polarity, step(1024..1), dim(2048)`. `FAR=4094` loses every argmin where content exists. Storage buffers (not images) — MoltenVK argument-buffer path rejects images. |
| `sdf_combine.comp` | Nearest-seed -> stbtt-compatible bytes: `val=128+16*signed_dist` (inside +). Push: `inSel,outSel,dim,onedge=128,distScale=16`. `atomicOr` 4 bytes/word (host zeroes first). GPU/CPU pages interchangeable in one `.antifont`. |
| `text_sdf.vert/frag` | GPU label path. Vert: fullscreen 6-vertex quad from `gl_VertexIndex`, `v_uv=mix(uvBox)`, `pos=rectNdc`. Push: `rectNdc,color,textureId,bold,smoothness,uvBox`. Frag: bindless `sampler2D[]` + `nonuniformEXT`; `bold<-0.1`=shadow bloom `smoothstep(0.1,0.6,dist)`; `smoothness<0`=color glyph raw RGBA x alpha; else SDF `threshold=0.5-bold`, `smoothing=mix(0.02,fwidth*1.8,clamp)`, `alpha=smoothstep`, `dist==0->0`. Out `rgb=color.rgb, a=color.a*alpha`. |
| `texture_quad.vert/frag` | Panels/images. Vert: corner expansion, `v_uv=local`. Frag push: `color(tint),textureId,imgSize,quadSize,mode` (FIT, ZOOM_FILL, ZOOM_FIT, FILL_CENTER/TOP_LEFT/TOP_RIGHT/BOTTOM_LEFT/BOTTOM_RIGHT). FIT=stretch; FILL_*=1:1 map w/ alignment; ZOOM_FILL=cover (crop); ZOOM_FIT=contain (letter/pillarbox, OOR->transparent). Sample `(uv.x,1-uv.y)` x color (Y flip). |

---

## 44. Events / dispatch / bridge

All seven events are plain structs, NOT Panels — never attached, delivered by central wiring.
Every event carries `nanos + consumed`; `consume()` short-circuits the bubble walk.
Allocated `Memory_alloc(TYPE_*_SINGLETON)`, symmetric getters/setters, null-safe defaults.

- **PointerEvent** (10 fields): `Panel *target` (hit, null=none yet); `*related` (enter/leave pair);
  `float x,y` (target-local); `int32_t button` (0 none,1 primary,2 secondary,3 middle);
  `float pressure` (`0..1`, 0=unknown); `int32_t kind` (`PTR_DOWN/MOVE/UP/DRAG/HOVER/ENTER/LEAVE/CANCEL`);
  `uint64_t nanos`; `int32_t phase` (0 capture,1 target,2 bubble); `bool consumed`.
  Ctors `PointerEvent_0()` (DOWN, phase 1), `PointerEvent_4(kind,x,y,button)`.
- **UIKeyEvent** (8): `Panel *target` (focused); `int32_t keyCode` (platform); `int32_t ch`
  (codepoint, `-1`=none); `uint32_t mods` (bitmask); `bool pressed/repeat/consumed`; `uint64_t nanos`.
  Split is deliberate: vexspoke `KeyHandler` = hardware mechanism; this = GUI-domain data.
  Ctors `_0()` (ch -1, released), `_3(keyCode,pressed,repeat)`.
- **FocusEvent** (5): `*target` (gaining/losing); `*opposite`; `bool gained/consumed`; `nanos`.
  Ctors `_0()` (lost), `_2(target,gained)`.
- **ActionEvent** (5): `Panel *source`; `int32_t actionId`; `char *command` (OWNED, e.g.
  `"menu:file:open"`, dup-alloc `TYPE_ARRAY`); `bool consumed`; `nanos`. Ctors `_0()`,
  `_2(source,actionId)`. Extra `ActionEvent_free` (frees command, then event).
- **ValueEvent** (8): `Panel *source`; `int32_t tag`; `int64_t oldV/newV`; `double oldD/newD`;
  `bool consumed`; `nanos`. Ctors `_0()`, `_2(source,tag)`.
- **TreeEvent** (5): `Panel *parent, *child`; `bool added` (true=added); `bool consumed`; `nanos`.
  Ctors `_0()` (removed), `_3(parent,child,added)`.
- **GestureEvent** (9): `Panel *target`; `int32_t kind` (`TAP/DOUBLE/LONGPRESS/PINCH/SWIPE`);
  `float x,y` (centroid target-local); `float scale` (pinch, 1=identity); `float rotation` (radians);
  `int32_t touches`; `bool consumed`; `nanos`. Ctors `_0()` (tap, scale 1), `_2(kind,touches)`.
- **Dispatch** (`dispatch.h/.c`, no struct): `Darling_firePointer(root,ev)`, `fireKey(focused,ev)`,
  `fireFocus/Action/Value/Tree/Gesture`. Capture root->target phase 0, target phase 1, bubble
  target->root phase 2, `consumed` stops at once. `dispatchPick` prefers a `MarkdownPanel` over its
  text rows (documents own their text); `dispatchPointerTo` routes text leaves
  `ID_MARKDOWN_PANEL`/`ID_LABEL`/`ID_RICH_LABEL` to their 5-arg `Class_handlePointer(node,
  kind, lx, ly, window)` weak bindings (window = `dispatchWindow()` = `Darling_bridgeGetWindow()`;
  cursor handlers guard `if (window)`). `dispatchKeyTo` routes the three text kinds plus `Textarea`
  to `Class_handleKey(node, ev)` (pressed-only, repeat-ignored, `keyCode`+`mods` only; C=copy,
  markdown V=paste+consume; never `ch`). Most other routing bodies `;;INCOMPLETE` (null-guard only).
  Focus gate: `PTR_DOWN` sets `s_focusedPanel` only for focusable kinds — `ID_INPUT`,
  `ID_TEXTAREA`, or a highlightable `LABEL`/`RICH_LABEL`/`MARKDOWN_PANEL` (weak
  `Class_isHighlightable`), so plain labels never steal focus. `Darling_fireKey(focused, ev)` uses
  explicit `focused` or falls back to `s_focusedPanel`.
- **Bridge** (`bridge.h/.c`, struct-less MODULE): `s_root/s_focused/s_attached/s_window`,
  `s_keyListener/s_mouseListener`. `Darling_bridgeAttach(root)` idempotent listener install
  (`Key_addListener` onDown/Up/Repeat, `Mouse_addListener` onDown/Up/Move/Drag);
  `Darling_bridgeDetach`; `Darling_bridgeSetFocused/GetFocused/GetRoot` (explicit focus, no auto-focus);
  window seam `Darling_bridgeSetWindow(void*)`/`Darling_bridgeGetWindow(void)` (the hotcwap
  `Window*` bound by the host after window warm-up; read by dispatch's text-pointer arms and
  cursor handlers).
  Key: mods `SHIFT/CONTROL/OPTION/COMMAND->1/2/4/8` (down/up/repeat all map identically),
  code `keyEvent & KEY_MASK_CODE`, `ch=-1`, `nanos=exactNanos` (vexspoke freezes
  `slot.pressTime + epoch micros` at push — press moment registers).
  Mouse down/up: `Mouse_button/x/y`, `PointerEvent_4`, exact nanos; move/drag: `PTR_MOVE/DRAG`,
  `NanoTime_now` at delivery. Deferred: char composition, scroll/zoom/delta, touch.
  Chain: AppKit/NSEvent -> hotcwap `window_cocoa.m` + vexspoke `input/key.c/mouse.c` ring ->
  `bridgeKey*/bridgeMouse*` -> `UIKeyEvent/PointerEvent` -> `Darling_fire*`.
  Type identity: `Label`/`RichLabel` allocate `TYPE_LABEL_SINGLETON`/`TYPE_RICH_LABEL_SINGLETON`
  (their own darling classes — not bare `TYPE_PANEL`) so class-switch routing (`dispatch`,
  `Memory_type` consumers) matches the registry; parent chain `5 ID_LABEL -> 1 ID_PANEL`,
  `6 ID_RICH_LABEL -> 1 ID_PANEL` keeps `Darling_addAny` and `Type_isA(_, ID_PANEL)` green.

---

## 45. Anim (`darling/anim/anim.h/.c`)

- `AnimEase` (17): `ANIM_NORMAL`, `EASE_IN/OUT/IN_OUT`, `SINE_*`, `EXPONENTIAL_*`,
  `ELASTIC_*`, `BOUNCE_*`. IN=launch, OUT=landing, IN_OUT=hill (`IN` u<0.5 else `OUT`).
- `AnimSection`: LOCATION, SIZE, SCALE, FONT_SIZE, ALPHA, COUNT.
- `AnimKind`: CONTAINER (x/y/w/h/sx/sy), PANEL (+bg alpha), LABEL (+font size), BUTTON (+font size).
- Keys `{t; payload; ease}`: `AnimLocKey{t,x,y}`, `AnimSizeKey`, `AnimScaleKey`, `AnimFontKey`,
  `AnimAlphaKey{t,alpha 0..1}`.
- `Anim` fields: `*loc/size/scale/font/alpha` + `Count/Cap` each, `bool loop`,
  `Anim_DoneFn onDone + void *ctx`. `Anim_play` BORROWS (one preset animates N widgets);
  `Anim_free` retires preset; replay restarts binding.
- API: `Anim_0/free`, `Anim_addLocation/Size/Scale/FontSize/Alpha` (insertion-sorted by `t`;
  segment INTO a key uses that key's ease), `Anim_eval(ease,u)` (clamps u, elastic overshoot
  only inside; `EASE_IN=u^2`, `OUT=1-v^2`, `IN_OUT=2u^2/1-2v^2`; SINE cos/sin; EXPO `q=u^2;q*q`;
  ELASTIC `2^-10u*sin(...)+1`; BOUNCE `n1=7.5625,d1=2.75` 4-hump; IN variants `1-f(1-u)`),
  `Anim_duration` (max key t), `Anim_keyCount`, `setLoop/isLoop/setOnDone/getOnDone/getDoneContext`,
  `Anim_play(c,a,kind)`, `Anim_tick(dt)` (Thread 0 only, next to layout),
  `Anim_cancel/cancelAll/isPlaying/liveCount`, plus 30+ per-class facades
  (`Container_animate`, `Panel_animate`, `Label_animate`, ... `Scene_animate`, `Canvas_animate`).
- Player: private `AnimBinding{c,a,kind,elapsed,fromX/Y/W/H/SX/SY/Font/Alpha}`, array `s_bindings`
  (16->x2). `play` captures from-values (font default 12, label/button real size; alpha from
  `Panel.color>>24`); `dur<=0` applies instantly + swap-remove + onDone. `tick`: `elapsed+=dt`;
  `<dur` apply; loop+`dur>0` => `fmod` wrap; else final + swap-remove + onDone.
  `animApply` writes `(*c).x/y/w/h/scaleX/scaleY` + `dirty=1` DIRECTLY (never public setters —
  avoids `invalidateBase` jumping anchored panels mid-animation); Panel patches color high byte;
  Label sets `fontSize + rasterDirty=true`; Button clamps `>=0.5`. Samplers: first segment
  interpolates FROM captured value; later key-to-key with that key's ease; past end => last key.
  `Input_caret_tick` GLIDE path uses `Anim_eval(ANIM_EASE_OUT,k)` — one easing implementation.

---

## 46. Raster + Surface (CPU path) (`render/raster.h/.c`, `surface.h/.c`)

- **Raster** — stateless software rasterizer into any 4-channel `Buffer` (ColorBuffer RGBA).
  Zero-alloc, buffer-first args, clipped `putPixel` -> `ColorBuffer_setRGBA`.
  `Raster_rect` (fill); `Raster_roundedRect(buf,x,y,w,h,radius,mode)` (mode 0 circular
  `dx^2+dy^2<=1`, mode 1 superellipse, radius clamps `min(w,h)/2`, 0=rect, `+0.5` sampling,
  mid-band fast path); `Raster_gradientH` (lerp, `denom=w-1`); `Raster_line` (Bresenham
  `err=adx-ady`); `Raster_triangle` (edge functions, barycentric, winding-aware);
  `Raster_dumpPPM` (P6 RGB debug sink).
- **Surface** — CPU double-buffered stamp (mini-swapchain per panel):
  `typedef struct Surface { Buffer *canvas[2]; _Atomic int front; int x,y; }`.
  `Surface_new(w,h,x,y)` (2x ColorBuffer, `front=0`); `Surface_back` (`canvas[front^1]`,
  relaxed); `Surface_flip` (`fetch_xor` acq_rel publish); `Surface_front` (acquire);
  `setScissor/x/y`; `Surface_composite(panel,master)` stamps front at scissor via
  `Buffer_blit`, clipped to both rects incl negative-scissor skip; `Surface_free`.
  Producer paints back + flips; Thread 0 composites fronts. Per-panel resolution =>
  UI/scene stamp at different scales (v1 1:1, scaled via `Buffer_sample` later).
- CPU vs GPU: CPU `Raster->Buffer->(Surface flip/composite->master->Window_present)`
  (legacy demo) or `PanelCocoa_markDirty` CPU paint; GPU `Panel_setRenderHandler` painters
  (`Vk_fillRect`, label/SDF quads, scene tri) record into retained layer targets
  (boards + depth-1 children), the seam pass composites the published boards.
  Gallery sections use GPU
  `section_render`/`scrollbar_render`.

---

## 47. IO / mmap / VFS / fontbake / .antifont

- `io/bake.h/.c` — offline `.anti` bake. `ANTI_ASSET_MAGIC 0x49544E41 ("ANTI")`,
  `AntiAssetHeader{magic,version,type,payloadBytes}`. `Scene_bake(path)`: header
  (v1, type 1=MESH, 3 verts) + 3 interleaved `BakedVertex{x,y,z,r,g,b,a}` (RGB triangle).
  Zero-copy intent: file is `mmap`ed directly.
- `io/mmap.h/.c` — zero-copy read-only mmap. `MemoryMap{data;size;valid}`.
  `MemoryMap_open(path)`: `open(O_RDONLY)` -> `fstat` -> `mmap(PROT_READ,MAP_PRIVATE)` ->
  `close(fd)` immediately (POSIX retains inode ref). `MemoryMap_close`: `munmap` + zero.
  Address space without RAM; pages fault on demand.
- `font/fontbake.c` — headless baked-font installer CLI, pure-CPU (atlas+dictionary are
  CPU data; texture upload deferred). Bare = install missing+stale; `--force` rebake all;
  `--list` families+paths (`[x] baked [*] stale [ ] missing`); `--verify Fam`
  (`Font_openBaked` + `'A'@64pt` present + `U+0378` absent); `--emoji`
  (`Font_loadSystem("Helvetica")` + `U+1F33B` via Apple Color Emoji, `color==1`); `Fam...`
  = `FontBake_bakeOne` each. Reports `FontBakeInstallReport{bakedNew,rebaked,alreadyFresh,failed,total}`.
- VFS + `.antifont` + `~/vex/fonts`: `VexHome` (`~/anti/` transitioning to `~/vex`,
  Rule 22) with `projects/logs/fonts/placeholder`; `FontBake_storeDir()==VexHome_fonts()`.
  `.antifont v2` (graphvex `font/font_bake.h`): multi-page atlas + glyph dictionary,
  full-cmap packed across 2048^2 pages (~350 SDF glyphs/page, up to `FONT_PAGES_MAX`);
  header records source TTF mtime for staleness; `Font_open` = baked-fresh -> `createFromBaked`
  (file read + `Texture_loadRaw`, zero FontBook/stbtt) -> else heal-bake -> else `Font_loadSystem`;
  `Font_openBaked` = no heal/fallback. Uncovered codepoints resolve at runtime through
  platform color cascade (emoji without prebake). `Vfs`: snapshots `$HOME`, mkdirs
  `config/projects`; `Vfs_setProject` fail-closed on `../..`; `Vfs_resolve`: `anti://`,
  `project://`, `~`, else passthrough; `..` rejected.
  README: engine lives in graphvex, darling consumes via link.

---

## 48. ObjC bridges + panel_bridge

- `window/panel_bridge.c` (pure C, LEVEL L4): single-seam layer model + traffic law.
  Scene/content panels own retained offscreen `VkLayer` boards; EVERY first-generation
  child of each board owns a retained `VkLayer` flight target (scenes and plain UI
  alike — Input included); depth below 1
  is each child's private affair. The board pass collages each child's last-published
  frame (`VkLayer_composite`) and skips unpublished children (published<0 keeps prior
  canvas content); a depth-1 child publish arms board demand one hop via a
  per-board present-count snapshot (never dirt — dirt dies on publish).
  Layer-3 interiors paint inside the parent pass via
  `Panel_setRenderHandler` (not nested layers); scrollbar paints into the board pass,
  last child/topmost, right-docked by `layoutBar`;
  `ScrollContainer_childFrame` shifts content by `-offset`, chrome stays — C-side resolve is source
  of truth. Functions: `Darling_attachPanelBoards(window,scenePane,contentPane,
  width,height,drawW,drawH)` (scene/content get `PanelCocoa_newBoard` full-window
  offscreen chains; existing boards `PanelCocoa_setSize` — idle-gated via
  `Darling_compositorIdleForResize`, no-op on unchanged extent; new boards ungated);
  `Darling_attachLayers(window,boardPanel,width,height)` (EVERY first-generation child
  as a retained `VkLayer` target — iterated via `Panel_childCount`, never hardcoded
  counts, per the Dynamic Scalability & Anti-Hardcoding Law);
  `Darling_propagatePaneDirty(window,scenePane,contentPanel)` (owner-subtree dirt
  re-arms the child's own target; depth-1 child PUBLISH arms board demand one hop
  via per-board `VkLayer_presentCount` snapshot);
  `Darling_getPanelSize(p,outW,outH)` / `Darling_setPanelSize(p,w,h)` (dest-last,
  `Container_resolve`-style point size for board-pass children).
- `objc/panel_cocoa.h/.m` (LEVEL L4): retained board shim. Each backed panel owns
  a `PanelCocoa{panel; width,height (display px)}` registry entry — NOT a `CAMetalLayer`
  (boards are OFFSCREEN `VkLayer` targets, never a CALayer, never in the window tree;
  the seam canvas is the window's only on-screen Metal layer, the Single-Seam Canvas Law).
  Registry `PanelEntry{panel,pc}` (linear scan, free-slot reuse).
  `PanelCocoa_newBoard(panel,w,h)` registers the retained offscreen chain (fixed pixel
  size); `PanelCocoa_setSize` rebuilds on true drift, no-op when unchanged;
  `PanelCocoa_isBoard` / `PanelCocoa_chain` (VkLayer handle) / `PanelCocoa_width/height`
  accessors; `PanelCocoa_free` (unregister chain, detach-before-free Rule 26). The
  pane-era `CAMetalLayer` + `VkPane` swapchain shim is retired wholesale.
- `objc/text_core.m` (LEVEL L4): see #40.

---

## 49. Gallery + darlingtest cookbook

- `../../main/darlingtest.c` (345 lines) — two-thread decoupled demo.
  `DarlingDemo{window,master,masterW/H,scene,skyPanel,triPanel,uiPanel,skySurface,triSurface,uiSurface,drawWorker,running,drawFps/drawFrametimeUs/presentFps/presentFrametimeUs (atomics)}`.
  Worker (`Thread_new(TYPE_THREAD_DRAW_SINGLETON, tickWhenIdle)`): `paintSky` (horizon gradient +
  ground + line), `paintTriangle` (sin/cos bounce in 220^2, glow+fill+highlight), `paintUI`
  (frosted slate `30,41,59,210`, borders, header, pulsing dot `180+75*sin(6t)`, 2 bars) —
  each `Surface_back -> paint -> Surface_flip`; 500ms FPS report. Thread 0: poll events;
  resize-adapt master; clear `(10,10,15)`; `Container_resolve` each panel -> `Surface_setScissor` ->
  `Surface_composite` -> `Window_present`; 250ms title. Anchors: sky full-cover, tri `(40,40)`
  220^2 TOP_LEFT, UI `(30,30)` 220x120 BOTTOM_RIGHT-tracking. Exit Esc/close.
- `../../main/darling_gallery.c` (1216 lines) — widget gallery + suite.
  Model: `Window`~=JFrame; `ScrollContainer y`~=JPanel — **the window IS y**
  (`Window_setContentPanel(w,&scroll->base)`); sections a/b/c/d = direct children at absolute
  frames, `TOP_LEFT/TOP_LEFT`; a1/a2/a3 paint INSIDE section surface via Vulkan (no nested layers);
  scrollbar = owned bar, last child/topmost, right-docked, chrome via `ScrollContainer_childFrame`.
  S1 Labels (plain/tinted/on-tint); S2 Documents (MarkdownPanel rows); S3 Choice
  (Button/Switch/Checkbox); S4 Fields (Slider/Input/Textarea + caret); S5 Lists (ListContainer bubbles,
  radius+margin); S6 Grids (3x3, gap, diag tint);   S7 Scrollbars (gesture vs point `ScrollBar_0/_1`, captions naming each block,
  grid cells labeled `r,c`);
  S8-S107 stress (100 generated sections, palette cycle, mini-lists every 4th — proves 100+
  first-gen layers need `IOSURFACE_CHILD_MAX` headroom).
  Renderers: `fillVk` (`0xAARRGGBB` decode x Container opacity, skip CLEAR/alpha 0, bottom-up flip `y=surfH-yTop-h`);
  `paintKidsVk` (recursive, points->px `k=surfW/panelW`, invokes each child's `renderHandler` at its own rect
  flipped into bottom-up surface space `surfH-ky-kh` — the handler contract is bottom-up AppKit space,
  same space the bg fills land in; passing layout-space ky unflipped puts glyphs in a mirrored second world.
  THE 0,0 CONTRACT: `0,0` is always the SURFACE origin, never "the panel". A first-gen child owns its whole
  surface, so the compositor hands its handler `(0,0,W,H)` — there `0,0` coincides with the panel's own top-left,
  which is why it looks like "the panel references the panel". Inside a SHARED surface (a section), kids sit at
  OFFSETS (`ox + rect.x*k`); `Container_resolve`'s leading `(0,0,...)` is the PARENT's origin in layout space,
  composed by adding offsets per level);
  `section_render` (bg + subtree, own opacity folded); `caption(s,text,y)` (dim 12pt descriptor line);
  `scrollbar_render` (track + value thumb, viewport-proportioned `g_barViewH/g_barContentH`, thumbMin clamp, bar opacity folded).
  Compositor folds first-gen opacity into solid fills; `Label_renderFn`/`RichLabel_renderFn` fold their own
  node opacity into bg + glyph alpha (sharp-path tint + SDF); custom handlers own their opacity.
  Window: `O` key cycles whole-window `Window_setOpacity` `1.0 -> 0.85 -> 0.7 -> 1.0` (`NSWindow alphaValue`;
  `0.0` would vanish the window entirely — alive and presenting, just invisible — so the demo stops at `0.7`).
  Per-node fading is Container opacity instead; see-through backdrop holes are the separate
   `Window_setTransparentBackground` toggle (rebuilds swapchain non-opaque), not this.
   Full tree/handlers/layers/catalog: `_docs/darling_gallery.md` (#1 tree with
   every panel incl. `Panel` itself + scrollpanel-inside-scrollpanel `bounds`,
   #2 render handlers, #3 render order, #4 layers, #5 fidget completeness).
   Scroll: `onScroll -> ScrollContainer_scrollBy(dx,dy)` via `Mouse_attachWindow`;
  `natural=true` default (`ox+dx, oy-dy` — fingers-down pushes content down);
  `setNatural(false)` legacy inverted; suite asserts `natural: (0,500)+(0,100)->(0,400)` vs
  flipped `->(0,600)`. Never hand-negate — the flag owns the sign.
  Pump: `runSuite()` asserts (markdown/list/grid/slider/input/caret blink+glide+goto+view/
  scroll direction+viewport+scrollbar clamp+scroll clamp+feel fling/overscroll/panel-forward/margin/opacity clamp);
  `Vk_init`, `Window_setScenePanel(null)` (transparent scene -> blur path), `bgRoot` container
  (clear `0xFF0A0A0F`, childless), `Darling_initCompositor`, `Window_setResizeRenderHook`
  (per-border-step viewport track + `Vk_clearPresent` mid-drag), `Window_forceNativeContainerOnRoot(true)`,
  bounds panel attached AFTER surfacing (CLEAR, `~900x16k` — must never own VRAM surface;
  still sizes clamp + re-raises bar); warm-up <=60 `Vk_clearPresent` -> `Window_show`;
  resize hook (`onResizeRender`, per border step): refresh `g_barViewH`, `setViewportSize`, explicit
  `ScrollContainer_syncToBar` + bar `markDirty` (thumb EXTENT derives from fresh view height, not value motion —
  without this a resize with unmoved offsets repaints sections but keeps the old thumb), then present.
Surfaces re-render synchronously in the hook; the single seam canvas
   presents inside the same step (`Vk_clearPresent` via the resize hook —
   hotcwap main-thread present rule) — realtime paint, zero placement lag;
  present-on-demand (`firstFrame||resized||treeDirty||scrolling||overscrolled`), 1ms active /
  16ms idle sleep (vsync is pacer; gate on `now-lastActive<100ms` — feel alone idles mid-drag
  since direct manipulation sets no velocity); title `FPS||idle + scroll ox,oy`.

---

## 50. 2am cheat sheets

**Create + attach:** `Button_1("OK")` detached; `Button_2(parent,"OK")` attached.
`Panel_1(parent)`, `Switch_1(parent)`, `Checkbox_1(parent)`, `RadioGroup_1(parent)`,
`Slider_1(parent)`, `Knob_1(parent)`, `Select_1(parent)`, `DatePicker_1(parent)`,
`ColorPicker_1(parent)`, `ColorSwatch_1(parent)`, `Label_2(parent,text)`,
`Typography_2(parent,text)`, `Kbd_2(parent,keys)`, `Plot_1(parent)`,
`SectionContainer_1/LayeredContainer_1/FileDialog_1/Dialog_1/AlertDialog_1/ColorDialog_1(parent)`.
Special arities: `ScrollContainer_2(w,h)`, `GridContainer_2(rows,cols)`, `Input_2(parent,cap)`,
`Textarea_2(parent,lines)`, `InputOTP_1(len)/_1_parent(parent)/_2(parent,len)`,
`ScrollBar_1(mode)`, `Scene_2(w,h)/_3(w,h,mode)`, `MarkdownPanel_1(text)`,
`RichTextPanel_2(rt,maxWidth)`.

**Move/reparent:** `Panel_addContainer(newParent,&child->base)` — auto-detaches from old.
**Detach (never free):** `Panel_removeChild` / `ListContainer_remove` / `ScrollContainer_setContent(old->NULL)`.
**Free with typed knowledge:** `Button_free` (label), `MarkdownPanel_free` (rows+models),
`RichTextPanel_free` (shell only), `Input_free/Textarea_free/InputOTP_free` (buffers),
`Select_free/RadioGroup_free` (items), `Plot_free` (titles), `Label_free/Typography_free/Kbd_free`,
`RichText_free`, `ActionEvent_free`. Never free borrowed (`font/image/xs/ys/content/model/ctx/view`).

**Scroll:** offsets end-clamped; all resizes re-pin; `scrollBy` owns the sign via `natural`;
`tick(dt)` on Thread 0 while `isScrolling`; bar is pure view (hide/swap safe).

**Dirty:** visual/state setters dirty; wiring setters (`on*/ctx/measurer`) do not;
`setEnabled/setNatural/setSlippery` do not dirty; `resolve/hitTest` clear dirty;
anim writes `x/y/w/h` + dirty directly (never public setters).

**Corrections to folk knowledge:** ListContainer has NO row array (index = `base.children`
position). ScrollContainer has ONE vertical bar (no h/v pair yet). SectionContainer has NO
header/body (children ARE sections). LayeredContainer has NO z-stack array (count + mask).
Scene has NO Surface slot / percent flag (Panel+mode only). DatePicker has NO min/max
(value+view only). ColorPicker has NO alpha/recent (single well + mirror + flags).
Textarea is UNBOUNDED (Input is bounded). `Button_press` / `RadioGroup_addOption` /
`Slider_setRange` / `Knob_setNormalized` / `Input_insert/erase` / `Textarea_scrollTo` /
`InputOTP_pushDigit` / `Select_add/clear` / `DatePicker_setToday` / `ColorPicker_setHSV` /
`ColorSwatch_addColor` / `FileDialog_refresh/choose` / `Plot_autorange/hitPick` are stubs —
setters/getters + layout are live; pump/walker/popup behaviors land later.

**Pixel checklist:** `contentsScale=backingScale`; max-size surfaces, `setSize` never reallocs;
resize moves layers; swapchain stamps scenes only; Y-flip at every CPU->Layer bridge;
100ms fence bound; teardown Window->compositor->Vk->threads->arena.

---

## 51. Cursor (`darling/cursor/cursor.h/.c`)

Standard mouse cursor presentation bridge. Pairs with native OS window cursors (`Window_setCursorType`).

```c
typedef enum CursorType {
    CURSOR_DEFAULT       = 0,
    CURSOR_IBEAM         = 1,
    CURSOR_POINTING_HAND = 2,
    CURSOR_CROSSHAIR     = 3,
    CURSOR_RESIZE_EW     = 4,
    CURSOR_RESIZE_NS     = 5,
    CURSOR_NOT_ALLOWED   = 6,
    CURSOR_HIDDEN        = 7,
} CursorType;

typedef struct Cursor {
    int type;
    void *customData;
} Cursor;
```

Constructors:
- `Cursor *Cursor_0(void)`: returns new cursor with `CURSOR_DEFAULT`.
- `Cursor *Cursor_1(int type)`: returns new cursor with given type.
- `Cursor *Cursor_getPredefined(int type)`: returns cached singleton for types 0..7.

Core Functions:
- `void Cursor_apply(const Cursor *cursor, void *window)`: sets window cursor type via `Window_setCursorType`.
- `void Cursor_free(Cursor *cursor)`: frees dynamic cursor (no-op on predefined singletons).

Symmetric Setters / Getters:
- `void Cursor_setType(Cursor *cursor, int type)` / `int Cursor_getType(const Cursor *cursor)`
- `void Cursor_setCustomData(Cursor *cursor, void *customData)` / `void *Cursor_getCustomData(const Cursor *cursor)`


---

## 52. SplitContainer

Tiled splitter, sibling of the #7–11 containers. N borrowed children share the
box along one axis by fractions; all children are always live (tiling hides
nothing). Fractions stay normalized (sum 1); the last child absorbs rounding
remainder so tiles exactly fill the box. Layout uses the house lift-then-set
idiom (each child's max-size ceiling is lifted before sizing) so tiles track
container growth. Drag-resize dividers and min-size enforcement deferred.

```c
typedef enum SplitContainerDirection {
    SPLIT_CONTAINER_DIRECTION_HORIZONTAL = 0, SPLIT_CONTAINER_DIRECTION_VERTICAL
} SplitContainerDirection;
typedef struct SplitContainer {
    Panel base; SplitContainerDirection direction;
    Panel **children; float *fractions; uint32_t childCount;
} SplitContainer;
// ID: local `ID_SPLIT_CONTAINER` (`0x0069`) in `splitcontainer.h` (central
// registry adopts on landing); tag `TYPE_SPLIT_CONTAINER_SINGLETON`.
```

| Field | Default | Compartment | What |
|-------|---------|-------------|------|
| `base` | `Panel_0` | inherited | Live tree holds all tiled children. |
| `direction` | `HORIZONTAL` | state | `HORIZONTAL`=columns along X; `VERTICAL`=rows along Y. |
| `children` | `nullptr` | content-slot part (model) | All N borrowed tiles, arena-owned, exact-size grown. |
| `fractions` | `nullptr` | content-slot part | Parallel axis shares, kept normalized; `add` resets to equal split. |
| `childCount` | `0` | content-slot part | Tile count. |

Functions: `SplitContainer *SplitContainer_0(void)` / `SplitContainer_1(direction)`
(`TYPE_SPLIT_CONTAINER_SINGLETON`); `void SplitContainer_add(sc,child)` (grow +
attach + equalize + layout); `void SplitContainer_setPane(sc,index,child)`
(replace + live-swap, detach-old); `bool SplitContainer_removePane(sc,index)`
(detach + compact + renormalize; `false` OOR); `void SplitContainer_layout(sc)`
(normalize; cursor along axis; last child takes the remainder; lift-then-set);
`void SplitContainer_setDirection` (null-safe + layout)
`SplitContainerDirection SplitContainer_getDirection` (`HORIZONTAL` NULL);
`void SplitContainer_setFraction(sc,index,f)` (clamp `>=0` + renormalize + layout)
`float SplitContainer_getFraction` (`0.0f` OOR/NULL);
`Panel *SplitContainer_getPane` (borrowed; `nullptr` OOR/NULL)
`uint32_t SplitContainer_getChildCount` (`0` NULL).

---

## 53. ExpandableListContainer

Node-oriented tree list with data-oriented flat storage. Hierarchical/nested
lists (file trees, task checklists, outlines, mind maps, schema viewers) are
`ExpandableListContainer` instances with `checklistMode` enabled — never a
separate class. Children indent via `depthLevelValue` = `depth * indentSpacing`;
expand/collapse is a visibility toggle on the borrowed `childPanel` sibling.

**Slot record** (`ExpandableNode`, behaviorless, lives in the owning file pair
per Rule 3 SLOT RECORD):

```c
typedef struct ExpandableNode {
    uint32_t parentIndex;    // EXPANDABLE_LIST_ROOT (UINT32_MAX) = root
    uint32_t childStart;     // flat array index of first child (alignment pass)
    uint32_t childCount;     // aligned child count (alignment pass)
    uint32_t depth;          // 0 = root, 1 = direct child of root, …
    float depthLevelValue;   // depth * indentSpacing — drives horizontal offset
    bool expanded;           // true = childPanel visible
    bool checked;            // checklist only — checkbox state
    Panel *row;              // owned row: [chevron, (checkbox), label]
    Panel *childPanel;       // borrowed container; collapse hides, expand shows
} ExpandableNode;
```

**Main class**:

```c
typedef struct ExpandableListContainer {
    Panel base;                  // inherited
    ExpandableNode *nodes;       // flat pre-order array, MemoryArena-owned
    uint32_t nodeCount;
    uint32_t nodeCap;
    float indentSpacing;         // px per nesting level (default 20)
    float rowHeight;             // row strip height (default 22)
    bool checklistMode;          // adds checkbox at child slot 1 on all rows
    uint32_t chevronCollapsed;   // text glyph 0x003E ('>') until SVG seam lands
    uint32_t chevronExpanded;    // text glyph 0x005E ('^') until SVG seam lands
    uint32_t chevronColor;
    uint32_t textColor;
    uint32_t boxColor;
    uint32_t checkColor;
} ExpandableListContainer;
// ID: local `ID_EXPANDABLE_LIST_CONTAINER` (`0x006A`) in
// expandable_list_container.h (central registry adopts on landing);
// tag `TYPE_EXPANDABLE_LIST_CONTAINER_SINGLETON`.
// Parent resolves to `ID_PANEL` (0x0078) via Type_getParentClass
// range fallback in `vexspoke/src/oop/type.c` (0x0065–0x00FF).
```

| Field | Default | Compartment | What |
|-------|---------|-------------|------|
| `base` | `Panel_0` | inherited | Live tree owns all row + childPanel pairs. |
| `nodes` | `nullptr` | data-model (flat array) | Pre-order flat array; memory grown by `ensureCapacity`. |
| `nodeCount` | `0` | data-model | Number of live nodes. |
| `nodeCap` | `0` | data-model | Allocated capacity of `nodes` array. |
| `indentSpacing` | `20.0f` | style | Logical-pixel horizontal indent per nesting level. |
| `rowHeight` | `22.0f` | style | Row strip height in logical points. |
| `checklistMode` | `false` | mode | When `true`, every row gets a checkbox at child index 1. |
| `chevronCollapsed` | `0x003E` (`>`) | glyph slot | `;;INTENTION("text glyph until SVG/icon seam; becomes icon handle then.")` |
| `chevronExpanded` | `0x005E` (`^`) | glyph slot | Same deferred SVG intent. |
| `chevronColor` | `0x99FFFFFF` | style | Chevron text colour. |
| `textColor` | `0xFFEEEEEE` | style | Label text colour. |
| `boxColor` | `0xFF555555` | style | Checkbox box border colour. |
| `checkColor` | `0xFF4CD964` | style | Checkbox check-mark colour. |

**Row child order** (always the same, built at insert time):
`[0] chevron | [1] checkbox (checklistMode only) | [last] label`

Functions: `ExpandableListContainer *ExpandableListContainer_0(void)` /
`ExpandableListContainer_1(indentSpacing)` (`TYPE_…_SINGLETON`);
`uint32_t ExpandableListContainer_addNode(self, parentIndex, label)`
(pre-order insert at end of parent subtree, returns index; `EXPANDABLE_LIST_ROOT`
if parentIndex is `ROOT`); `void ExpandableListContainer_removeNode(self, idx)`
(detach subtree panels, shift, reindex); `void ExpandableListContainer_clear(self)`;
`void ExpandableListContainer_expand(self, idx)` / `_collapse` / `_toggle`
(set `expanded`, update chevron glyph, relayout); `void ExpandableListContainer_layout(self)`
(rebuild all row/childPanel positions from pre-order roots); `void
ExpandableListContainer_setChecked(self, idx, checked)` / `_isChecked` /
`_setChecklistMode` / `_isChecklistMode` (checklist API);
`void ExpandableListContainer_getChildren(self, idx, &start, &count)`
(dest-last flat range of direct children); `uint32_t
ExpandableListContainer_getParent` / `_getDepth` / `_getDepthLevelValue` /
`_isExpanded` / `_nodeCount`; part verbs (Rule 29): `Panel
*ExpandableListContainer_part_row(self, idx)`, `_part_childPanel`, `_part_chevron`,
`_part_label`, `_part_checkbox` (returns checkbox at child 1 when checklistMode;
`nullptr` when mode off or index OOR).

---

## 54. Frame (`darling/frame.h`, `frame.c`)

Host bridge gluing an R1 `Window` to an R3 graphics context: stacked FBO
layers on one `CAMetalLayer` (`presentsWithTransaction = YES`), the content /
scene board roots, the composable present-callback slots, and the
KeyMap-backed input bindings. `Dialog` embeds a `Frame` as its first member
(section 32). Frames are `calloc`'d via `Frame_0..3` and freed with
`Frame_destroy` + `Frame_free`; all grown sub-arrays (present slots,
KeyMap) live in the default master arena (lazy-init, reclaimed at
`Memory_freeAll` per the Teardown Order Law).

| field | type | default | compartment | role |
|---|---|---|---|---|
| `window` | `Window *` | null | state | R1 host window (borrowed) |
| `application` | `Application *` | null | state | R1 host app manifest (nullable) |
| `graphics` | `void *` | null | state | R3 graphics context (VkHotContext / Device) |
| `rootPanel` | `Panel *` | null | tree | Root UI component tree (borrowed, nullable) |
| `contentPane` | `Panel *` | null | tree | Upper board root — UI canvas (borrowed, nullable) |
| `scenePane` | `Panel *` | null | tree | Bottom board root — scene/backdrop (borrowed, nullable) |
| `title` | `char *` | null | state | Owned (`strdup` on set, `free` in `Frame_free`) |
| `chromeMode` | int | `FRAME_DECORATED` | chrome | Decorated / borderless / naked |
| `layers[8]`, `layerCount` | — | 0 | layers | Stacked FBO layers (SLOT RECORD `FrameLayer`) |
| `childDialogs[16]`, `childDialogCount` | — | 0 | dialogs | Managed child dialogs (max 16) |
| `ownerDialog` | `Dialog *` | null | dialogs | Owning Dialog if embedded in a Dialog |
| `parentFrame` | `struct Frame *` | null | dialogs | Parent frame if child dialog |
| `onQuitRequested`, `quitRequestedUserData` | — | null | policy | User-close policy hook |
 | `presentsWithTransaction` | bool | true | present | Atomic WindowServer present flag |
| `presentedFrames` | uint32 | 0 | present | Confirmed seam presents since attach (infancy gate: demand-gating off until 3) |
| `width`, `height` | int | 800/600 | geometry | Logical point dimensions |
| `inLiveResize` | bool | false | geometry | Active drag-resize |
| `isMinimized` | bool | false | geometry | Window miniaturized |
| `isZoomed` | bool | false | geometry | Window zoomed |
| `functions`, `functionCount`, `functionCapacity` | — | null/0/0 | frame-functions | Grown slot table (SLOT RECORD `FrameFunction`) — replaces the single `onRender` hook |
| `keyMap` | `KeyMap *` | null | input-bindings | Master-arena `KeyMap`; lazily created on first bind |
| `lastRenderNanos` | uint64 | 0 | frame-timing | `CLOCK_MONOTONIC` at last `Frame_render` (dt source) |
| `nativeView` | `void *` | null | platform | Native NSView / CAMetalLayer container |

**FrameFunction slot record** (per-slot):

| field | type | role |
|---|---|---|
| `fn` | `void (*)(Frame *frame, double dt, void *userData)` | Present callback |
| `userData` | `void *` | Callback context (opaque) |

Slots fire in registration order on every `Frame_render`. `dt` is seconds
since the previous render (0.0 on the first render), measured on
`CLOCK_MONOTONIC`.

Functions:

- `uint32_t Frame_addFrameFunction(Frame*, fn, userData)` — appends a present
  callback, returns the slot index. `UINT32_MAX` on failure (null fn or
  master arena unavailable). Replaces the removed `Frame_setOnRender` (which
  supported only one hook); migrate by calling `Frame_addFrameFunction` for
  each present callback, or use index 0 to replicate the old single-hook
  pattern.
- `bool Frame_removeFrameFunction(Frame*, uint32_t index)` — swap-remove
  (last slot fills the hole). `false` on null / out-of-range.
- `uint32_t Frame_getFrameFunctionCount(const Frame*)` — live slot count.
- `bool Frame_addKeyFunction(Frame*, int64_t combo, KeyBindingFn fn, userData)`
  — bind a keyboard combo (`KMOD_*/KMODE_*/KEY_*`); lazily creates the
  Frame's `KeyMap` on first bind.
- `bool Frame_addMouseFunction(Frame*, int64_t combo, KeyBindingFn fn, userData)`
  — identical table, mouse button combos (`MOUSE_*` code < 32). Split API
  so intent reads at the call site.
- `bool Frame_removeFunction(Frame*, int64_t combo, KeyBindingFn fn)` — unbind
  by combo + fn identity (`KeyMap_unbind`).
- `KeyMap *Frame_getKeyMap(const Frame*)` — the live `KeyMap` (null until first
  bind). Allow full KeyMap introspection (`KeyMap_count`, `KeyMap_match`).

**`Frame_render` order of operations** (per present):

1. `KeyMap_resolve` fires at most one binding — the source tap is consumed
   BEFORE the callback, so a re-entrant render cannot re-fire (the
   Present-On-Demand Law). Stale taps offered-but-declined on modifiers are
   expired automatically by the resolver. Recognition is windowed: taps are
   OFFERED while the per-key pending window (250ms, `tapWindowNanos` at push)
   is open and settle into SINGLE/DOUBLE/TRIPLE at close; TAP requires
   release, LONG_PRESS fires once per press (one-shot latch), and
   `KeyMap_setMultiTapEnabled(false)` picks rhythm mode (instant singles, no
   doubles/triples). See the vexspoke `KeyMap` section.
2. `dt` computed from `lastRenderNanos` via `clock_gettime(CLOCK_MONOTONIC)`.
3. Frame-function slots dispatched in registration order with `dt`.
4. Layer loop iterates visible layers (existing FBO stacking).

---

## 55. Immediate vs Retained Element Model (component classification)

Every darling element is a composition of **components** (paint parts), not a
single blob. Each component is one of exactly two classes, and the class
decides how far its pixels travel before the screen and how much memory they
hold:

- **IMMEDIATE** — a bounded number of filled quads computed directly from
  layout/state: background fill, border, divider, caret, line marker,
  scrollbar thumb, selection rect, plot grid/axes. Order matters, identity
  does not. Zero GPU memory, zero flight, zero allocation — `Vk_fillRect`
  straight into the currently-open render pass.
- **RETAINED** — resolution-bound pixel content: text rasters (CoreText /
  SDF glyph output), images, scene output. Owns GPU memory proportional to
  content and updates only when its content changes. Two sub-kinds:
  - **retained texture, sampled as one quad** — `Vk_drawTexture` inside the
    widget's own renderFn (Label/Button/Input text raster, Picture image).
    The quad is immediate; the texture is retained.
  - **retained output, re-rendered separately** — offscreen target
    (`VkLayer_composite`) whose pixels are
    produced by a render handler on its own timeline (scenes, boards,
    depth-1 collages).

The two classes are already mixed inside every widget's own renderFn
(`Panel_setRenderHandler` — no external render factories exist, and none are
needed: elements configure via setters such as `setBackground(r,g,b,a)`,
`setTextColor`, and the renderFn consumes them). What the classification adds
is the **delivery-path decision**: how many retained intermediaries a
component's pixels pass through.

### 55.1 The render primitives (the whole vocabulary)

| primitive | class | memory | notes |
|---|---|---|---|
| `Vk_fillRect(cb, sw, sh, x, y, w, h, r, g, b, a)` | immediate | zero | one filled quad; draw order = z-order |
| `Vk_drawTexture(cb, ..., PICTURE_MODE_FIT, texW, texH)` | retained sample | texture | one textured quad sampling an existing texture (text raster, image) |
| `VkLayer_composite(cb, sw, sh, idx, x, y, w, h, tint)` | retained sample | offscreen flight target | collages a published VkLayer image as one quad |
| `VkLayer_visit()` | retained render | offscreen targets | re-renders dirty retained targets (boards + COMPOSITED layers) and publishes fresh frames |
| scene render handler (`Panel_getRenderHandler`) | retained render | target | invoked into offscreen retained target (COMPOSITED) |
| `paintChildIntoPass(...)` | immediate fallback | zero | child without a layer: handler inline or background quad, then its whole I/R subtree recursively |

### 55.2 Delivery today (what the source does)

- The seam canvas (`CAMetalLayer`) is the window's SINGLE on-screen layer.
- scene board + content board = two retained `VkLayer` targets at full window
  pixel size; the seam pass composites them bottom/top (`Darling_renderFrame`).
- **Classification is LANDED** (`Darling_attachLayers`, panel_bridge.c):
  a depth-1 board child owns a retained `VkLayer` target ONLY when its
  subtree contains retained-output content — a COMPOSITED scene (classified
  by `panelSubtreeNeedsRetained`, an attach-time subtree walk). A rect-heavy
  child (Input included) therefore paints INLINE: `board target -> seam
  canvas` — one copy, same pass, zero child flight memory. A child
  reclassified to I/R unregisters its stale layer (idle-gated like the
  resize path).
- **The window opens already painted** ("run at least once"): the frame
  loop's first step lands only after `Frame_show`, so `Darling_initCompositor`
  ends with a synchronous warm-up present — the resize sequence runs
  pre-show (thread 0, zero concurrency): boards attach + render + publish,
  the seam composites, one clear-present paints the first frame before the
  window is visible. No blank first beat over the blur view; the loop's own
  first step re-presents only if demand says so (hasPresented latched).
- **Live resize references the UPDATING size, pinned top-left, never
  stretched** (the Continuous Real-Time Live Resize Law): layout runs against
  the fresh window size EVERY tick (`Darling_preFrame` `Container_setSize`
  plus the Window Board Root Lock Law `forceSize` inside `Frame_resize`), and
  the seam composites each board at its OWN pixel extent pinned top-left in
  the drawable (`Darling_renderFrame`), so a board target that lags a step
  pins its last publish crisply instead of gravity-resizing it — a converged
  board (extent == drawable) samples 1:1, identical to the old full-extent
  quad. Boards resize on pixel drift (no-op when unchanged, the Single-Seam
  Canvas Law; idle-gated to the layer flight). The pipeline test drives a programmatic
  resize (`Window_setSize` 480x320 -> 640x440, pumped until the new extent
  lands) and asserts a BOTTOM_RIGHT-anchored + BOTTOM_RIGHT-pivot probe
  resolves to the NEW corner — anchoring tracks the live size
  ("Bottom-right anchor tracks live resize ...: PASS").
- **Per-drag-step render-then-present** (resize hook is the live seam):
  AppKit's modal tracking loop owns thread 0 during a drag, so the GfxLoop's
  own steps are starved — the resize hook (`frameCocoaResizeHook`, the slot
  winner over the compositor's fallback) is the only live code per drag
  step. It re-chases `drawableSize` in rounded native px from the live OS
  bounds, runs ONE `Frame_resize`, re-arms
  the client dirty, then calls `GfxLoop_modalTick()` (dirty-gated, so idle
  windows rest per the Present-On-Demand Law; a drop keeps dirty armed for
  the next step) — the synchronous present
  renders at the NEW size and presents within the SAME step
  (`darlingWindowPresentFn` -> `Vk_clearPresent`, `Darling_preFrame` +
  board render + seam composite, GPU queue-ordered so the render completes
  before the swap). `Darling_preFrame` additionally consumes the live flag
  as a demand ticket (moving edge re-arms the client dirty every tick), and
  the R1 hook stays CPU-only publish — all GPU waits live in R3 behind the
  100ms fence / 25ms acquire bounds with try-lock drop.
- **Swapchain rebuilds immediately** (graphvex): the default
  `ANTI_RESIZE_HZ` is 0 — every extent drift rebuilds the chain so the
  drawable always matches the live window; a dragged step never drops.
  An opt-in throttle (`ANTI_RESIZE_HZ=N`) presents at the current chain
  extent (top-left pinned) instead of dropping the frame — no frozen
  frames on any path.
- The inline path is a **recursive subtree walk** (`paintChildIntoPass`,
  compositor.c): a handler-less plain container paints its backdrop, then
  its children, then theirs — each level resolved against its own parent's
  extents and offset by the parent's absolute origin, mirroring the
  depth-1 retained pass whose canvas was the child's own rect. Tree order
  is z-order; retained-output descendants keep their own targets.
- Inline children without a layer already painted via `paintChildIntoPass`
  inside the board pass (compositor.c); the recursion now covers whole
  I/R subtrees, not single leaves.
- Board-less frames paint root children directly into the seam pass
  (`Darling_renderFrame` fallback, `compositor.c`) — the all-immediate,
  zero-retained path.
- Each flight target is dual-slot (`VK_LAYER_FLIGHT = 2`, vk_layer.c): on a
  retina 2x window a full-window board target is `(winW*2 x winH*2 x 4B x 2)`
  — ~15MB per board at 800x600 logical. The memory bill is now boards
  (always) + COMPOSITED-scene subtrees (only when the tree has them);
  all-immediate trees hold exactly two targets. The pipeline test asserts
  `VkLayer_count() == 2` (boards only; 5 targets pre-classification).

### 55.3 The element matrix (components, not fields)

One row per element family. `I` = immediate, `R` = retained (texture quad),
`RR` = retained (re-rendered output). The renderFn column names the painter
registered via `Panel_setRenderHandler` today; `(base)` = no custom painter,
panel fallback (background quad).

| Element | components (class: primitive) | renderFn today |
|---|---|---|
| Container / Panel / Canvas | background fill (I: `Vk_fillRect`) | (base) |
| ListContainer / GridContainer / SectionContainer / LayeredContainer / SplitContainer / ExpandableListContainer | pure layout — no own paint; children only; own backdrop (I) | (base) |
| ScrollContainer | backdrop (I), scrollbar chrome (I: track + thumb rects), content (I or RR by child) | (base) + childFrame |
| Button | state fill (I), border (I: 4 rects), label text (R: `Vk_drawTexture` rasterTex) | `Button_renderFn` |
| Switch | track on/off (I), knob (I) | (base) |
| Checkbox | box outline (I), check fill (I) | (base) |
| RadioGroup | composes option children; no own paint | (base) |
| Slider | track (I), fill (I), thumb (I) | (base) |
| Knob | ring/arc (I), pointer/dot (I) | (base) |
| Input | background (I), border (I: 4 rects), text (R: raster `Vk_drawTexture`), caret (I), selection (I) | `Input_renderFn` |
| Textarea | same as Input: background (I), border (I), text (R), caret (I), selection (I) | `Textarea_renderFn` |
| CodeField | Indexed row composite: background, selection, text/caret, scrollbars, fixed gutter; all through Graphics. Variable heights and optional numbering. | `CodeField_paint` |
| InputOTP | boxes (I), box borders (I), digit text (R), caret (I) | `InputOTP_renderFn` |
| SearchField | border (I), icon (I: rects), badge (I), text (R) | `SearchField_renderFn` |
| Select / DatePicker / ColorPicker / ColorSwatch | chrome (I), swatch/thumb (I), text (R) | (base) |
| Label | text (R: sharp raster or SDF fallback, one textured quad) | `Label_renderFn` |
| RichLabel | text runs (R) | `RichLabel_renderFn` |
| Typography | metadata/scale class — no own paint | — |
| Kbd | shell (I), keycap text (R) | (base) |
| Dialog / AlertDialog / FileDialog / ColorDialog | scrim/backdrop (I), panel chrome (I), title/text (R), children | (base) |
| Picture | image (R: `Vk_drawTexture` of `textureId` quad, mode/crop/UV), missing-image placeholder (I: solid amber quad); Panel `setBackground` is an intended immediate first-op but the custom handler currently replaces the background pass | `Picture_renderFn` |
| Plot | grid/axes/lines/bars (I: quads), title/labels (R: text) | (base) |
| Scene / Scene2D / Scene3D | clear color (I), rendered output (RR: COMPOSITED VkLayer) | scene handler / tri fallback |
| RichText / MarkdownPanel / RichTextPanel | text runs (R), chrome (I) — the heavy retain case | `RichLabel_renderFn` / children |
| ScrollBar | track (I), thumb (I) | (base) |

The exemplars, stated plainly:

- **Picture** = two things: `background` (I — one quad) + `image` (R —
  texture, memory proportional to image resolution). Today the handler draws
  either the texture quad or an amber placeholder; the background-as-first-op
  is the intended immediate component for the classification-driven pass.
  Background never needs a target; image needs exactly one texture, sampled
  as one quad.
- **CodeField** = a panel with text: gutter bg, divider, line markers,
  scrollbar are mostly rectangles — order matters, not identity (I). The text
  itself is the only retained content (R: raster). None of it requires a
  full-window child layer.

### 55.4 The delivery rule (model-derived)

1. **The class never changes how the tree is walked.** Every element keeps
   its own renderFn (section 55.3 column 3); components configure via
   setters, never external render factories.
2. **All-immediate subtrees paint inline into the current pass.** They need
   no `VkLayer`, no board slot, no flight memory.
3. **Retained-texture components paint as ONE quad inside the widget's own
   renderFn** (`Vk_drawTexture`). They therefore do NOT require a subtree
   layer either — the texture is the retained part, the draw is immediate.
4. **Subtree layers remain only for `RR` content**: scenes (render
   handler output on its own timeline), boards (hosting `RR` children +
   collapsed depth-1 collages), and depth-1 children whose subtree is
   re-rendered separately.
5. **Boards become optional.** A content tree with only `I` + `R` components
   paints straight into the seam pass via the existing board-less fallback —
   one pass, zero intermediary targets.
6. **Landed** (per the Living Darling Docs Law): `Darling_attachLayers` is
   classification-driven — a retained target is registered only for
   children whose subtree contains `RR` content; `I`/`R`-only children take
   the inline `paintChildIntoPass` path (now recursive). Section 55.2 is
   the current state.

### 55.5 Aliveness heartbeat (future, managed exception)

A parked window currently rests per the Present-On-Demand Law (probe at
60Hz, zero presents). Option under consideration: a 1Hz liveness present
("alive window" assertion) to re-arm the composite after occlusion flips,
display profile changes, and wake edges where the last composite can go
stale. With an all-immediate tree this is a dozen fills into the same command
buffer — near-free, and `VkLayer_visit` clean-skips retained targets. It is a
Present-On-Demand Law managed exception per the Conflict Triage Law: requires
`;;INTENTION` + preferences.md wording in the same commit as the code. The
immediate classification is what makes it affordable.

### 55.6 Law map

- Present-On-Demand Law — sampling stays demand-gated; the classification
  only removes unnecessary retained *render*, never re-renders clean content.
- Single-Seam Canvas Law — the seam canvas is the window's only on-screen
  Metal layer; boards and depth-1 children are retained OFFSCREEN `VkLayer`
  targets (never a CALayer, never in the window tree) sampled into the seam
  pass; flight machinery is shared, only the destination differs.
- Native Pixel Law — retained target sizes stay fixed at register; inline
  quads resolve against the current pass extent (board or seam).
- Conflict Triage Law — the aliveness heartbeat is the
  documented managed exception; every waiver carries `;;INTENTION` + this
  section updated in the same commit (Living Darling Docs Law).
- Every code change that adds/removes a component or changes its class must
  update the matrix (section 55.3) and the current-state notes (section
  55.2) in the SAME commit — a stale row is a defect, exactly like a stale
  `;;OVERVIEW`.

---

## 56. Component (`darling/component.h`, `component.c`) — new-architecture leaf

The first concrete leaf of the immediate element model (section 55): a
from-scratch geometry+presentation leaf with **eager absolute resolution**
and **render hooks**, built so the immediate on-demand pass has zero
tree-walking and zero dirty flags. It intentionally does NOT embed
Container/Panel — it is the migration target Container geometry will clone
value-for-value, minus dirty/tree/percent/scale.

```
0x00 float x, y          .  placement + size; x/y = edge inset on right/bottom anchors
0x10 uint8_t anchor      .  COMPONENT_ANCHOR_* 0..8 (9-grid, mirrors CONTAINER_ANCHOR_*)
0x14 int32_t pivot       .  COMPONENT_PIVOT_* 0..4 (offset applied for TOP_LEFT anchors)
0x18 float minW/minH     .  size constraints (0 = unset)
0x20 float maxW/maxH     .  size constraints (0 = unset)
0x28 float marginL/T     .  additive placement offsets (final = resolved + margin)
0x30 float marginR/B     .  right/bottom edges stored for sibling layout
0x38 float paddingL/T    .  inward content insets (content box = abs + padding)
0x40 float paddingR/B    .
0x48 float borderWidth   . 0 = no border
0x50 uint32_t borderColor . 0xAARRGGBB
0x54 uint32_t backgroundColor . 0xAARRGGBB (consumed by render hooks)
0x58 float radius        .  corner radius (0 = square)
0x5C int radiusMode      .  COMPONENT_CORNER_ARC (0) / COMPONENT_CORNER_SUPERELLIPSE (1)
0x60 float opacity       .  0..1 alpha multiplier (1 = opaque)
0x68 int32_t z           .  z-order
0x6C uint8_t visible     .  visibility gate for render/hitTest
0x70 struct Component *parent . borrowed view, nullptr = root; NEVER owned
0x78 float absX/absY     .  EAGER: absolute left/top in the rendering space
0x80 float absW/absH     .  EAGER: absolute extent
0x88 float parentAbsX/Y  .  parent abs box at last recompute (the cascade entry)
0x90 float parentAbsW/H  .
0x98 Component_RenderFn backgroundRender . stage 0 hook
0xA0 Component_RenderFn foregroundRender . stage 1 hook
0xA8 void *renderUserdata . opaque arg handed to both hooks
```

Contract:

- **Eager abs cascade.** Every geometry setter (`setX/Y/Location/Size/Width/
  Height/Anchor/Pivot/Margin/MinSize/MaxSize`, the `setCenter` convenience)
  recomputes `absX/Y/W/H` immediately against the stored parent abs box.
  `Component_setParentAbs(self, px, py, pw, ph)` is the cascade entry: the
  parent (Container, board, window) reports its own abs box on every change
  and the child tracks in the same call — no layout pass, no dirty flag.
  A parentless component resolves against the identity box `(0,0,0,0)`.
  Setters never layout; the element is always already resolved.
- **Resolve parity with Container.** The placement math mirrors
  `Container_resolve` exactly: anchor 9-grid (`px + (anchorX/2)*(pw-w)`),
  location sign-flip for right/bottom anchors (edge-inset convention),
  additive `marginL/marginT` per the Panel Gravity Law mapping, pivot offset
  applied only for the TOP_LEFT anchor. A value-identical migration later
  means a Container child and a Component child sit in the same pixel.
- **clamp(min, size, max).** `setSize` and the re-clamp inside
  `setMinSize/setMaxSize` apply `w < minW → minW`, then
  `maxW > 0 && w > maxW → maxW` (min wins over a contradictory max,
  mirroring Container).
- **Render hooks, visible-gated.** `Component_render(self, graphics)` returns
  `false` (and does nothing) when invisible or when both hooks are null;
  otherwise it calls `backgroundRender` then `foregroundRender` with the
  component and the opaque userdata. Hooks are the immediate on-demand paint
  seam: the presenter calls render only when the element is dirty (the
  Present-On-Demand Law), and the hooks fill the current pass directly —
  no retained target required for plain UI.
- **hitTest** is a half-open point-in-abs-rect test (`x >= absX && x <
  absX+absW`), visible-gated.
- Memory: `Component_0()` allocates `TYPE_COMPONENT_SINGLETON` from the
  arena (root class, ID_COMPONENT = 56, parents row 56 → 0). Zero steady-state
  allocation; `parent` is borrowed, never freed, never reparented by the owner.

## Indexed CodeField: current migration

The old Textarea/Vulkan wrapper is replaced by the built indexed row implementation. The current field/API/ownership blueprint is [`ecosystem/darling-framework/_docs/darling.md`](../../ecosystem/darling-framework/_docs/darling.md). Number and text panels share vertical layout; horizontal scrolling affects text only. See the repository-local blueprint for verified status and limits.

# Layout Panels — List, Grid, Markdown, RichText, Scroll + Container Law

**Idea (in vexgraph's words):** new darling containers — `ListPanel`
(indexed panels, text bubbles), `GridPanel` (excel), `MarkdownPanel`
(markdown-fed), `RichTextPanel` (rich-string documents) — plus `ScrollBar`
(gesture vs point-accurate), `ScrollPanel` (viewport with offsets), and two
container-wide laws: additive **margin** and **corner radius** (superellipse
vs circular-arc, artifact first).

## 0. Naming & file layout (repo law)

New classes live beside their kin, one class per file pair (Rule 3):

| Class | Files | Base |
|---|---|---|
| `ListPanel` | `darling/panel/list_panel.h/.c` | `Panel` |
| `GridPanel` | `darling/panel/grid_panel.h/.c` | `Panel` |
| `MarkdownPanel` | `darling/panel/markdown_panel.h/.c` | `Panel` |
| `RichTextPanel` | `darling/panel/richtext_panel.h/.c` | `Panel` |
| `ScrollBar` | `darling/field/scrollbar.h/.c` | `Panel` |
| `ScrollPanel` | `darling/panel/scroll_panel.h/.c` | `Panel` |

`Panel_*` location/size/anchor shims already forward to `Container_*`
(`panel.h:73-90`); new widgets follow the same pattern: embed `Panel base`
first, expose `Widget_setLocation` → `Panel_setLocation` → `Container_*`.
Constructors are arity-overloaded (`ListPanel_0()`, `ListPanel_1(style)`)
via `CONSTRUCTOR_DISPATCH`; every state field gets symmetric
getter+setter (Symmetric Getter/Setter Completeness Law), dest-last on multi-out (Dest-Last Law),
two-layer cap (Two-Layer Access Cap Law), `;;OVERVIEW` per the Living `;;OVERVIEW` & `;;DEFINITION` Blueprint Law.

## 1. ListPanel — indexed panel list

A vertical (or horizontal) stack owning ordered children. Index *is* the
API: insert/remove/move by index, query by index. Text bubbles, chat logs,
file rows, settings groups.

```c
ListPanel *lp = ListPanel(LIST_PANEL_VERTICAL);
ListPanel_add(lp, &(*somePanel).base);          // append
ListPanel_insert(lp, 0, &(*other).base);        // by index
Panel *row = ListPanel_get(lp, 2);              // by index
ListPanel_remove(lp, 2);                        // detach only, never frees
ListPanel_setSpacing(lp, 8.0f);
ListPanel_setDirection(lp, LIST_PANEL_VERTICAL);
size_t n = ListPanel_count(lp);
```

- Layout: children stacked along the axis with `spacing`; cross-axis sized
  to the widest child (vertical) unless `fillCross` is set.
- Children stay ordinary `Panel`s — bubbles are just panels with radius +
  margin (see #7–8), so no bubble class is needed.
- `ListPanel` never frees children (detach-only, like `Panel` roots).

## 2. GridPanel — excel core

Fixed or auto rows×cols with per-cell min sizes, uniform gaps, optional
header row/col count frozen from scrolling when nested in a `ScrollPanel`.

```c
GridPanel *g = GridPanel(3, 4);                 // rows, cols
GridPanel_setCell(g, 1, 2, &(*cell).base);
Panel *cell = GridPanel_getCell(g, 1, 2);
GridPanel_setGap(g, 4.0f, 4.0f);                // dest-last: (gx, gy)
GridPanel_setHeaderRows(g, 1);
GridPanel_setHeaderCols(g, 1);
GridPanel_setRowHeight(g, 0, 28.0f);            // per-line override, -1 = auto
```

- Auto mode: `GridPanel_0()` grows rows/cols on `setCell` past the edge.
- Cells are `Panel*` slots; empty cell = `nullptr`, skipped in layout.
- Selection/édition lives above (a `GridView` controller later), not here.

## 3. MarkdownPanel — markdown-fed content

Takes a markdown string, builds an internal `ListPanel` of styled rows
(headings, paragraphs, code blocks, bullets). **No external md library**:
a zero-alloc line scanner over `primitive/string` (vexspoke), emitting
`Label`/`RichLabel` rows with style per block type.

```c
MarkdownPanel *md = MarkdownPanel("# Title\n\nHello *world*");
MarkdownPanel_setText(md, newSrc);              // re-scan + rebuild rows
MarkdownPanel_setCodeBackground(md, 0xFF1E1E1Eff);
Panel *rows = MarkdownPanel_getRows(md);        // the inner ListPanel
```

- v1 syntax: `#`/`##`/`###`, `*`/`-` bullets, `` `code` `` inline,
  fenced blocks, `**bold**`/`*italic*` via `RichText` styles.
- Rebuild is detach-all + re-layout (document panels are cold paths).

## 4. RichTextPanel — rich-string documents

Takes a styled rich-text string (the `RichText` span format in
`text/rich_text.h`: `RichText_setString` + `RichText_setStyle`), lays it
out to `maxWidth` (`RichText_layout`), and pages it as a document.

```c
RichTextPanel *doc = RichTextPanel(rt, 600.0f); // (RichText*, maxWidth)
RichTextPanel_setSource(doc, rt2);
RichTextPanel_setMaxWidth(doc, 600.0f);
float h = RichTextPanel_contentHeight(doc);     // for ScrollPanel pairing
```

- `MarkdownPanel` may build *on* this (scan → `RichText` → panel); keep
  both, different inputs.

## 5. ScrollBar — two interaction modes

Same track+thumb, two thumb laws (a mode flag, switchable live):

```c
ScrollBar *sb = ScrollBar(SCROLL_BAR_GESTURE);
ScrollBar_setMode(sb, SCROLL_BAR_POINT);        // live switch
ScrollBar_setRange(sb, 0.0f, 1.0f);             // dest-last min,max
ScrollBar_setValue(sb, 0.25f);
float v = ScrollBar_getValue(sb);
ScrollBar_setThumbMin(sb, 24.0f);               // px, gesture mode scaling
```

- `SCROLL_BAR_GESTURE` (iPhone volume): drag delta maps to value delta
  scaled by track length — position-independent, eyes-free.
- `SCROLL_BAR_POINT` (point-accurate): click jumps the value to the exact
  clicked fraction; drag tracks 1:1 under the finger.
- Value changes fire through the owner (`ScrollPanel` polls or a
  `valueChanged` hook — polling first, events if needed).

## 6. ScrollPanel — viewport with offsets

Owns a content `Panel` larger than itself; shows a window with
start/end offsets; clips children (`Container_setClipChildren` exists).

```c
ScrollPanel *sp = ScrollPanel(400.0f, 600.0f);  // viewport w,h
ScrollPanel_setContent(sp, &(*doc).base);
ScrollPanel_setOffset(sp, 0.0f, 120.0f);        // (x, y) into content
ScrollPanel_getOffset(sp, &ox, &oy);            // dest-last
ScrollPanel_setStartInset(sp, 8.0f);            // padding before first child
ScrollPanel_setEndInset(sp, 8.0f);              // overscroll past last child
ScrollBar *bar = ScrollPanel_getBar(sp);        // owned vertical bar
```

- Offsets clamp to `[−startInset, contentH − viewH + endInset]`.
- The owned `ScrollBar` writes offsets; direct `setOffset` writes back to
  the bar — single source of truth is the offset pair.

## 7. Container margin — additive, never absolute

All containers gain a 4-edge margin. Law: **final = location + margin**.
Margin is a plus-value applied at resolve time; it never rewrites stored
location, never participates in anchors, never persists into children.

```c
Container_setMargin(c, 8.0f, 8.0f, 8.0f, 8.0f); // dest-last: l,t,r,b
Container_getMargin(c, &l, &t, &r, &b);          // dest-last outs
```

- Resolve order: anchor → location → **+ margin** → min/max clamp.
- `Panel_*` shims forward both calls like every other `Container_*` pair.
- Zero default: every existing layout resolves bit-identically.

## 8. Corner radius — two curves, artifact first

All containers gain `radius` + `radiusMode`. Two raster laws:

- `CORNER_SUPERELLIPSE` (squircle-ish): `|x/a|^n + |y/b|^n <= 1`, n≈4 —
  Apple-continuous look, single formula, cheap in shader/SDF later.
- `CORNER_ARC` (classic): straight edges + circular quarter-arcs
  (`x²+y²=r²` pixel test) — exact CSS-style rounded rect.

```c
Container_setRadius(c, 12.0f);
Container_setRadiusMode(c, CORNER_SUPERELLIPSE);
```

**Artifact first:** before widgets consume it, a headless raster test
renders the same rounded rect both ways into `Buffer`s and diffs them:
same bounding box, symmetric quadrants, arc-mode pixel-exact against the
analytic circle, superellipse strictly inside the box. Proof lands as
`render/corner_test.c` (exit-nonzero on mismatch) *before* `ListPanel`
bubbles use it.

Raster surface: `Raster_roundedRect(buf, x, y, w, h, radius, mode, rgba)`
next to `Raster_rect` in `render/raster.c`; Vulkan SDF path can adopt the
superellipse formula later (it is already SDF-friendly).

## 9. Build & doc touch-ups with the work

- `darling/CMakeLists.txt`: append the six new sources (one line each).
- `../../preferences.md` Rule 17 darling owns-list: add the six widgets +
  margin/radius laws when they land (Rule 23 living-doc law).
- No new repos, no new deps: parser over vexspoke strings, raster over
  `Buffer`, text over `RichText`/`Label`.

## 10. Sequencing (agent split)

1. **Substrate**: margin + radius on `Container` (+`Panel` shims),
   `Raster_roundedRect` both modes, `render/corner_test.c` artifact.
2. **Lists**: `ListPanel`, `GridPanel` (parallel after 1).
3. **Documents**: `MarkdownPanel`, `RichTextPanel` (parallel after 1).
4. **Scroll**: `ScrollBar`, `ScrollPanel` (parallel after 1).
5. Wire CMake, full build, `corner_test` + `buffer_test` + harnesses.

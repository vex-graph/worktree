# How Labels Work: Selection, Positions, and Highlights

> Answers the fundamental question: **"When I drag over text, how does the pointer become a highlighted range — and why was the highlight landing in the wrong place?"**
> Covers `Label`, `RichLabel`, and `MarkdownPanel` document rows, the three coordinate spaces they juggle, and the per-glyph position table that keeps hit-testing and paint in agreement.

---

## 1. The Short Answer: Two Widgets, One Selection Part, Stated Positions

| Widget | Text model | Paint path | Position source |
|---|---|---|---|
| **`Label`** (`darling/label/label.c`) | Single style, one UTF-8 string | CoreText raster baked into one texture ("sharp path"); SDF per-glyph fallback | `glyphX` table from the same CoreText shaper that paints; uniform estimate only as fallback |
| **`RichLabel`** (`darling/label/rich_label.c`) | Multi-style `RichText` model (runs, tags, decor) | SDF glyph quads positioned on CPU | `TextQuad` `{x, advance, charIndex}` built by `RichText_layout` |
| **`MarkdownPanel`** (`darling/panel/markdown_panel.c`) | Document of rows (each row is a `Label` or `RichLabel`) | Delegates to its rows | Document byte space → per-row space |

All three share one selection primitive, the **`TextSelect` part** (`text/text_select.h`): `{anchor, active, hovered}`. The pointer protocol is identical everywhere:

- **DOWN** inside → `TextSelect_begin(idx)` — fixed anchor, collapsed span.
- **DRAG** → `TextSelect_drag(idx)` — moves only the active edge (dragging left then right past the anchor selects exactly `[anchor, active]`, never a rolling union).
- **UP** → `TextSelect_end(lo, hi)` — a nonzero range **commits** (stays readable, highlight persists); a collapsed range (plain click) **clears**.
- **DOWN outside** → `TextSelect_cancel()`.

Copy/paste lives on the key seam, not the pointer: `Class_handleKey` reacts to `keyCode` + modifier bits only (Cmd/Ctrl+C = 67 with mods `8|2`, never the decoded char), press-only, repeats ignored. `C` copies `Class_getSelectedText()` (arena-alloc, caller frees) through the `TextCore` clipboard seam and consumes; `V` on the MarkdownPanel pastes via `setText`. Labels are read-only — no caret, ever (carets belong to `Input`/`Textarea`).

---

## 2. The Three Coordinate Spaces

A `Label`'s text passes through three spaces. Confusing any two is the entire bug class this document exists to prevent:

```text
LABEL SPACE (what the user and TextSelect speak)
  bytes of (*label).text, e.g. "a&b" -> [a][&][b], indices 0..3
        │  mnemonic strip (& removed, && -> &)
        ▼
CLEAN SPACE (what CoreText paints)
  e.g. "ab" -> [a][b], indices 0..2
        │  rasterize at pxH = fontSize * backing
        ▼
RASTER SPACE (pixels in the texture, +1px left pad, backing scale)
```

The maps between them, built fresh on every raster rebuild in `ensureRaster`:

- `toClean[i]` — clean coordinate of original byte `i` (heap, cold path only, freed after install).
- `skipMark[i]` — flags the consumed `&` marker byte itself.
- `glyphX[i]` — the **stated position**: CoreText pen offset in points of original byte `i`, `strlen+1` entries. Consumed markers fold onto the previous glyph (`glyphX[i] = glyphX[i-1]`), so a zero-width phantom is never addressable. Continuation bytes share their codepoint's offset.

The selection span itself always stays in **label space** (`getSelectedText` slices the stored text). Only the raster call translates it: `selClean = toClean[clamp(sel)]` goes into `TextStyleDescriptor.selectionStart/End`. Before this mapping existed, any `&` before a selection shifted the painted highlight — same symptom family as the Gallery bug below.

---

## 3. Stated Positions vs Estimated Positions (the Core Idea)

There are exactly two ways to answer "which letter is at x?":

1. **Stated** — ask the shaper that paints. CoreText's `CTLineGetOffsetForStringIndex` returns the true pen x per index, accounting for proportional advances, kerning, tracking, and ligatures. This is what `TextCore_lineOffsets` does (single line only, same font fallback chain / ligature flag / tracking as the raster, fail-closed `-1` otherwise).
2. **Estimated** — assume every glyph is equally wide: `roundf(x / qw * len)`. One division, always available, wrong on proportional type by up to a full glyph.

The rule, enforced in code: **hit-testing and highlight paint must share one source of positions.** The table (`glyphX`, cached on the label, rebuilt whenever the raster rebuilds, installed only beside successful pixels, cleared on rebuild entry and on free) is that shared source:

```text
pointer x ──▶ Label_charIndexAt ──▶ TextSelect span ──▶ ensureRaster ──▶ CoreText highlight
                    │                                                    │
                    └────── same glyphX table ───────────────────────────┘
                              (offsets match paint by construction)
```

`Label_charIndexAt` with a table: clamp outside `[glyphX[0], glyphX[len]]` (plus the raster's 1px left pad in points), binary-search the midpoint boundaries between consecutive offsets (hemisphere: the `>=` split belongs to the right glyph), then rewind over equal neighbors so a span never opens mid-codepoint or on a marker. Without a table (multiline text, non-Apple stub with no shaper, raster failure, or a stale-length table) it keeps the old uniform path — deliberately, never silently.

`RichLabel` never had this bug class: its `TextQuad`s already carry `{x, advance, charIndex}`, and hit-test (`RichLabel_charIndexAt`, nearest glyph origin), highlight spans (`drawSelectionSpans`, min-origin → max-origin+advance per line cluster), and copy (`getSelectedText`, tag-stripped) all read the same quads. `MarkdownPanel` delegates per-row (`markdownRowIndexAt` → the row's own `charIndexAt`) inside one contiguous document byte space, so a cross-row drag is one monotonic index.

---

## 4. Worked Example: the "Gallery" Mis-Highlight

The gallery's S2 section builds `MarkdownPanel_setText(mdoc, "# Gallery\n\nPick a widget *below*")`. The `# Gallery` headline becomes a plain-`Label` row in a large proportional font.

Before the fix, the chain for that row was split-brained:

```text
pointer over "a" ──▶ uniform estimate ──▶ span lags ~1 glyph ──▶ CoreText paints TRUE extent of wrong span
      (proportional truth)      (assumes G is average-width)            (blue box left of the drag)
```

`G` is much wider than the average, so every index right of it mapped one glyph early, and the box sat over the G–a boundary instead of the drag. After the fix, the pointer and the paint read the same stated offsets, so the box lands exactly on the dragged glyphs.

Reproduce / verify it yourself:

1. `cmake --build build --target darling_gallery && ./build/darling_gallery`
2. Drag across "Gallery" — the blue box should track the pointer glyph-for-glyph, including the wide `G` (try starting the drag mid-`G`: left half selects `G`, right half selects from `a`).
3. `Cmd+C` copies the exact dragged text (no `&` artifacts, no tag leakage on rich rows).
4. Headless proof: `./build/projects/darling-framework/label_test` (#7 feeds a synthetic wide-`G` table and asserts the mapping, plus multibyte rewind and fallback).

---

## 5. Event Flow: Who Calls the Seams

Two paths deliver pointer events to text, and they exist for different reasons:

```text
OS event ──▶ vexspoke input rings ──▶ Darling bridge listeners ──▶ Darling_firePointer(root, ev)
                                                                          │
                                                              dispatchPick (reverse child order,
                                                              MarkdownPanel preferred over its rows)
                                                                          │
                              ┌───────────────┬───────────────┼───────────────┐
                              ▼               ▼               ▼               ▼
                        Button/handle…  Label/RichLabel/   Textarea/       (others ;;INCOMPLETE)
                                        MarkdownPanel     Input
                                        5-arg handlePointer(node, kind, lx, ly, window)
                                        window = Darling_bridgeGetWindow()
```

- **Focus gate:** `PTR_DOWN` sets `s_focusedPanel` only for `Input`/`Textarea` or a *highlightable* text kind (weak `isHighlightable` getters). Plain labels never steal focus. `Darling_fireKey` routes to the explicit target or the focused panel.
- **The gallery keeps its own forwarder** (`main/darling_gallery.c`: `onMouseMove/Down/Drag/Up` + highlightable tables + `Darling_bridgeSetWindow`). This is intentional, not legacy: `Container_resolve` is pure layout with no scroll-offset awareness (the offset is baked only in `ScrollContainer_childFrame` for the layer bridge), so `dispatchPick` at raw viewport coordinates cannot hit scrolled content. The forwarder adds the scroll offset first, then calls the same 5-arg seams. `dispatcher_test` proves the dispatch path on full-viewport trees.
- **Cursor lifecycle** rides the same calls: enter/hover → I-beam on highlightable text (needs a real window — handlers guard `if (window)`; tests pass `nullptr`), leave/outside-move → default.

---

## 6. File Map

| File | Role |
|---|---|
| `darling/label/label.h/.c` | `Label` struct (`glyphX`/`glyphN` cache), `ensureRaster` (strip map + offsets + install), `charIndexAt`, pointer/key seams, symmetric getters |
| `darling/label/label_test.c` (#7) | Synthetic-table hit-test proof: proportional, multibyte rewind, fallback, null-safety |
| `darling/label/rich_label.c` | Quad-based hit-test / spans / tag-stripped copy (self-consistent by construction) |
| `darling/panel/markdown_panel.c` | Document space, `markdownDocIndexAt`, `refreshRowSelection` row mirroring |
| `text/text_core.h` | `TextCore_lineOffsets` contract |
| `objc/text_core.m` | CoreText offsets implementation (mirrors the raster's font chain) |
| `text/text_core_stub.c` | Always `-1` → uniform fallback off Apple |
| `text/text_select.h/.c` | The shared `{anchor, active, hovered}` part + fixed-anchor verbs |
| `event/dispatch.c` | `dispatchPick`, text arms, focus gate, `dispatchWindow()` |
| `event/bridge.c/.h` | Listener install, `s_window` seam (`SetWindow`/`GetWindow`), repeat-mods mapping |
| `event/dispatcher_test.c` | Headless routing/focus/clipboard proof over a static tree |

## 7. Known Limits (honest, not roadmap promises)

- **Multiline `Label`s** still hit-test uniformly — the offset table is single-line by contract (`lineOffsets` fails closed on `\n`). No gallery surface exercises this today.
- **The SDF fallback** (`drawSdfFallback`) paints no selection highlight at all; it owns pixels only when CoreText fails.
- **`glyphX` costs one small heap array per label per raster rebuild** (cold path; pointer-drag re-rasters already dwarf it). No steady-state allocation was added to tick/render paths.
- `Input`/`Textarea` caret positioning is a separate system, untouched by this fix.

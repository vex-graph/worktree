# The darling gallery — a multi-faceted exhibit proving darling's flexibility

`../../main/darling_gallery.c`. One binary, zero web layers, zero foreign frameworks: a real macOS window, a live scrollable widget tree, native Vulkan rendering over hardware `IOSurface`s.

```sh
# build + run (CLion-bundled cmake)
cmake-build-debug/darling_gallery
# scroll the trackpad, press O to cycle window opacity, Esc to exit
```

Companion references:
- `_docs/darling.md` — full class blueprints, getter/setter contracts, compositor laws.
- `projects/darling/UI_CATALOG.md` — inventory of widgets and render nodes.

---

## 1. The Core Philosophy: From "Stress Twins" to "Permutation Matrix"

The original gallery was a stress test: seven full-width 876pt slabs followed by 100 identical placeholder boxes. It proved layer count, but failed to prove design flexibility. As of now the gallery holds twelve curated sections (S1–S12: widgets + property showcases below) followed by 100 stress twins ($S_{13} \dots S_{112}$).

The refreshed architecture treats the gallery as a **Multi-Gallery Exhibit**:
1. **No Uniform Canvas Mandate**: Panels break out of the single-column 876pt box. Panels take dimensions tailored to what they host — compact 260pt mobile drawers, 380pt dual comparison cards, 200×130pt metric tiles, and fluid hero banners.
2. **Permutation Over Monotony**: Instead of displaying one lonely `Label` or `Button`, the gallery repeats the same component across multiple contrasting configurations:
   - *Typography*: Monospace code blocks vs. proportional body copy vs. native multi-page color emoji (`🚀 📦 ⚡ 🎨`).
   - *Scale*: 9pt micro badges up to 32pt display headlines.
   - *Constraints*: Fixed-width truncated badges vs. self-sizing multiline paragraphs.
   - *Containers*: Dense tabular data grids vs. fluid chat bubbles with dynamic margins.
3. **Honest Geometry**: Where a specialized shader or glyph painter is live (Labels, RichText, solid quads, scrollbar chrome), it renders natively through Vulkan. Where a control painter is pending (Buttons, Checkboxes, Inputs), it renders honest colored geometry with clear captions explaining what is pending.

---

## 2. The Multi-Gallery Exhibit Layout

The window is anchored by a master `ScrollContainer` hosting diverse exhibits, each engineered to showcase a distinct capability:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        DARLING GALLERY EXHIBITS                        │
├────────────────────────────────────────────────────────────────────────┤
│  [EXHIBIT 1: Typography Matrix]                                        │
│  ┌───────────────────────┐ ┌───────────────────────┐ ┌──────────────┐ │
│  │ Sans-Serif Proport.   │ │ Monospace Code Font   │ │ Color Emoji  │ │
│  │ SF Pro Body & Display │ │ Menlo / SF Mono Logs  │ │ Native Atlas │ │
│  └───────────────────────┘ └───────────────────────┘ └──────────────┘ │
├────────────────────────────────────────────────────────────────────────┤
│  [EXHIBIT 2: Responsive Card Rack]                                     │
│  ┌─────────────────┐ ┌─────────────────┐ ┌───────────────────────────┐ │
│  │ Metric Tile     │ │ Status Pill Bad.│ │ Asymmetric Dual-Pane Card │ │
│  │ 200x130pt       │ │ 200x130pt       │ │ 420x220pt                 │ │
│  └─────────────────┘ └─────────────────┘ └───────────────────────────┘ │
├────────────────────────────────────────────────────────────────────────┤
│  [EXHIBIT 3: Interactive Controls & Variations]                        │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │ Primary CTA · Secondary Ghost · Icon Pill · Toggle · Checkbox     │ │
│  └───────────────────────────────────────────────────────────────────┘ │
├────────────────────────────────────────────────────────────────────────┤
│  [EXHIBIT 4: Form & Text Input Laboratory]                             │
│  ┌───────────────────────────────────┐ ┌─────────────────────────────┐ │
│  │ Single-line Search with Caret     │ │ Segmented OTP/PIN Inputs    │ │
│  ├───────────────────────────────────┴─────────────────────────────┤ │
│  │ Multiline Code / Markdown Textarea with Line Numbers            │ │
│  └─────────────────────────────────────────────────────────────────┘ │
├────────────────────────────────────────────────────────────────────────┤
│  [EXHIBIT 5: Container Layouts & Viewports]                            │
│  ┌───────────────────────┐ ┌─────────────────────────────────────────┐ │
│  │ 260pt Sidebar Drawer  │ │ 3x3 GridContainer with Alternating Fills    │ │
│  │ Asymmetric Bubbles    │ │ Cell-anchored coordinate stamps         │ │
│  └───────────────────────┘ └─────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────┘
```

### Exhibit 1: The Typography & Glyph Matrix
Demonstrates font engine adaptability and texture atlas integration:
- **Proportional Sans-Serif (SF Pro)**:
  - Hero display title (28pt, high contrast).
  - Editorial body paragraphs (14pt with 1.35x line spacing via `setSpacingHeight`).
  - Muted secondary captions (11pt slate).
- **Typography & Styling Permutations**:
  - **Ligatures & Kerning**: Toggle ligatures on/off (`setLigatures`), letter tracking delta (`setSpacingWidth`).
  - **Underline Gallery**: `UNDERLINE_BASIC` (crisp baseline stroke), `UNDERLINE_STRIKETHROUGH` (mid-character strike), and `UNDERLINE_JAGGED` (diagnostic wavy squiggle) with custom `setUnderlineColor` / `setUnderlineColorRGBA`.
  - **Mnemonics**: `setMnemonic` parsing accelerator prefixes (`&File`, `Save &As...`) with native character-specific underlines.
  - **Interactive Selection (no caret)**: `setHighlightable` providing rounded corner selection background quads (`setHighlightRadius`, `setHighlightColor`), fixed-anchor drag selection across characters — Labels, RichLabels, and MarkdownPanel documents are non-editable, so they never draw a blinking caret. Blinking caret and cursor-lifecycle hover adaptation are `Input`/`Textarea` work; selection semantics match the browser: down anchors, drag moves the active edge, up collapses a plain click, outside-down clears. In the live gallery: S1 rounded highlight labels, S2 the whole `MarkdownPanel` document, S20 RichLabel runs (S21 mono code lines).
- **Monospace Code Font (SF Mono / Menlo)**:
  - Terminal log block inside a dark slate container: `0x7FFF5FBFF8C0 [INFO] engine initialized in 1.4ms`.
  - Tabular aligned numbers testing monospaced glyph advance parity.
- **Color Glyph & Emoji Cascade**:
  - Direct rendering of multi-page RGBA color glyphs (`⚡ 🚀 📦 🎨 💻 🔥`) handled via `Vk_drawColorGlyph` without dropping into SDF grayscale.
- **Micro-Badges & Tags**:
  - High-density pill labels (9pt uppercase with 4pt horizontal padding, rounded corners, contrasting tints).

### Exhibit 2: Asymmetric Card Rack
Breaks the full-width monotony with multi-column, varying aspect ratio panels:
- **Metric Cards (Dual 200×130pt)**:
  - Left card: Large numeric readout (`124.8 MB/s`), trend indicator badge, subtle 8pt background radius.
  - Right card: GPU memory allocation gauge (`14 / 64 MB`), status dot indicator.
- **Hero Comparison Card (876×200pt)**:
  - Left half: Source markdown string.
  - Right half: Live `MarkdownPanel` rendered row-by-row into sharp native text quads.

### Exhibit 3: Component Permutations
Shows how identical underlying types represent different design languages:
- **Button Permutations**:
  - Primary filled button with bold text.
  - Ghost / outline button with translucent fill.
  - Circular icon button / toggle pill.
  - Disabled state with 0.38 opacity.
- **Toggles & Selection**:
  - Switch in ON and OFF states.
  - Checkbox in checked, unchecked, and indeterminate states.
  - Segmented radio buttons side by side.

### Exhibit 4: Form & Field Laboratory
Interactive field states and caret rendering:
- **Single-Line Search Field**: Left-docked search icon placeholder, live blinking caret, input text.
- **Segmented OTP Field**: Four distinct square boxes with single-character centered layout.
- **Multiline Code Textarea**: Deep background with line gutter and multi-row content model.

### Exhibit 5: Container Layouts & Viewports
Container geometry and nesting laws:
- **Chat Feed (`ListContainer`)**: Variable width speech bubbles (left-aligned incoming, right-aligned outgoing) with auto-spacing and asymmetric corner radiuses.
- **Structured Data (`GridContainer`)**: 3×3 matrix testing cell alignment, row spanning, and diagonal tinting.
- **Embedded `ScrollContainer`** (roadmap, NOT built): A mini-scrollable list embedded *inside* a section panel, proving nested scissor clipping and localized coordinate resolution. What exists today is the scrollpanel-inside-scrollpanel `bounds` content (transparent clamp panel, zero VRAM) — see `_docs/darling.md` #49.

### Built today: property showcases S8–S12 (live in `../../main/darling_gallery.c`)
- **S8 Opacity ladder**: same `0xFF2563EB` fill at `1.00 / 0.66 / 0.33 / 0.12` via `Panel_setOpacity` — per-node alpha folding, the library's transparency story in one row.
- **S9 Spacing & margins**: three `ListContainer`s at gap `4 / 12 / 24` with margin-4 bubbles — spacing and margin law, side by side.
- **S10 Label scale**: `9 / 12 / 18 / 28pt` plus a Menlo monospace line (`Label_setFontFamily(mono, "Menlo")`) — scale + typeface permutations, CoreText sharp path each.
- **S11 RichLabel**: bold-20pt headline + underline-14pt accent runs (`[0]/[1]` style tags, `Font_loadSystem("Helvetica")`, SDF quads). No system font → honest pending caption, never blank rows. Live drag-select proof in the gallery.
- **S12 Code field**: IDE-style well (`0xFF0B1220`) with gutter line numbers + Menlo lines, one accent line. Single-style quads per line — token colors pending, captioned honestly.
- **S2 Documents**: the `MarkdownPanel` document is live-selectable as ONE unit — click-drag highlights across the stacked headline + body rows (fixed anchor, no caret), the document-level counterpart to the per-row Label/RichLabel selection. Highlights land via `MarkdownPanel_setHighlightable` + per-row `Label/RichLabel_setSelection`. The gallery's mouse handler forwards pointer events into the 5-arg text seams (`Label/RichLabel/MarkdownPanel_handlePointer(node, kind, lx, ly, window)`), passing the OS window; markdown selection routes through the same seam. The town dispatch (`event/dispatch`) additionally routes these text kinds for full-viewport trees (`dispatcher_test`), but the gallery keeps its own scroll-aware forwarder because `Container_resolve` is pure layout — the scroll offset is baked only in `ScrollContainer_childFrame`, so `dispatchPick` cannot hit scrolled content. The bridge window seam (`Darling_bridgeSetWindow`) is registered so dispatch/cursor handlers share the OS window.

---

## 3. Surface & Coordinate Architecture

Every panel in the exhibit obeys the **Surface / Rect Separation Law**:

```c
Panel_RenderFn(panel, renderer, cmdBuffer, surfaceW, surfaceH, x, y, w, h);
```

### 1. The Surface Domain (`surfaceW`, `surfaceH`)
- Passed to Vulkan draw calls (`Vk_fillRect`, `Vk_drawTexture`, `Vk_drawSDFText`, `Vk_drawColorGlyph`).
- Establishes the viewport bounds, NDC normalization divisor, and global scissor bounds of the enclosing `IOSurface` or swapchain.
- Never conflated with the element's local width or height.

### 2. The Rect Domain (`x`, `y`, `w`, `h`)
- Defines the widget's axis-aligned bounding box within the surface.
- Formatted in bottom-up coordinates for Vulkan presentation into macOS CoreAnimation layers.
- Handles offsets inside nested containers (`ox + rect.x * k`, `surfH - ky - kh`).

### 3. Native Retina Resolution
All `IOSurface` backing allocations scale by the monitor backing factor ($k_x, k_y$, typically $2.0$ on Apple Silicon Retina):
$$\text{pxW} = \text{round}(w_{\text{pt}} \times k_x), \quad \text{pxH} = \text{round}(h_{\text{pt}} \times k_y)$$
The corresponding `CALayer` maintains frame in logical points with `contentsScale = backingScaleFactor`, ensuring pixel-sharp text without double-scaling.

---

## 4. The Complete Widget Matrix

Every widget in the gallery must satisfy the four pillars of Darling component completeness:

| Widget | Exhibit Form Factors | Painter Status | Verification Suite |
|---|---|---|---|
| **`Panel`** | `bgRoot`, cards, badges, metric tiles, gutters | `Vk_fillRect` with radius & opacity | Margin, opacity, radius modes |
| **`Label`** | S1 trio + S10 scale ladder + Menlo lines (emoji cascade = roadmap) | `Vk_drawTexture` (raster) / `Vk_drawSDFText` / `Vk_drawColorGlyph` | Raster cache, glyph metrics |
| **`RichLabel`** | S20 bold headline + underline accent | `RichLabel_renderFn` (SDF quad runs) | Quad count, style runs, drag selection |
| **`MarkdownPanel`** | S2 single-pane rows (dual-pane preview = roadmap) | Scanned rows $\to$ child `Label`/`RichLabel`s | Markdown parser, row rebuild, document drag selection |
| **`Button`** | Primary, outline, pill, disabled | Rect-only geometry + label painter | Click dispatch, active state |
| **`Switch`** | ON / OFF toggles | Rect-only toggle geometry | Value change event |
| **`Checkbox`** | Checked / Unchecked / Indeterminate | Rect-only box + indicator | Toggle event |
| **`Slider`** | Continuous value bar, step markers | Rect-only track + thumb | Value math, range clamping |
| **`Input`** | S4 single-line + caret (search/OTP/password = roadmap) | Rect-only background + LIVE caret | Caret blink, cursor navigation |
| **`Textarea`** | Multi-line code card with gutter | Rect-only container + text lines | Multiline wrap |
| **`ListContainer`** | Chat bubble feed, variable-size card stack | Layout calculation (children paint in surface) | Child count, indexing, spacing |
| **`GridContainer`** | 3×3 metric grid, tabular comparison | Layout calculation (cells paint in surface) | Row/column indexing, cell span |
| **`ScrollBar`** | Point-accurate & gesture-accelerated tracks | `scrollbar_render` chrome thumb | Range math, extent proportions |
| **`ScrollContainer`** | Master scroll `y` + `bounds` content (embedded viewports = roadmap) | Math + scissor clipping | Viewport tracking, overscroll feel |

---

## 5. Implementation Roadmap

To transition `../../main/darling_gallery.c` to this specification:
1. **Curate Asymmetric Section Builders**: Replace the uniform `section(title, h)` factory with specialized card builders:
   - `section_wide(...)` for full-width comparisons.
   - `section_card(...)` for multi-column side-by-side tiles.
   - `section_card_dual(...)` for left/right split showcases.
2. **Typography Showcase** (partially LANDED — S10/S11/S12 live; remainder open):
   - LANDED: label scale ladder + Menlo line (S10), RichLabel bold/underline runs (S11), monospace code well with gutter (S12).
   - OPEN: emoji badge row testing `Vk_drawColorGlyph` coverage; weight permutations beyond bold.
3. **Stress Twins**: S13–S112 still placeholder boxes — replace with genuine layout variations (different densities, card sizes, widget combinations). Remaining open exhibits: OTP blocks, search field, embedded `ScrollContainer`, dual-pane markdown preview.
4. **Preserve High-FPS Present-on-Demand**: Keep the event-driven render loop (1 FPS at rest, 60+ FPS during scroll/fling), bounded present fence waits, and clean teardown.


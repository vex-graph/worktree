# Darling & Hotcwap UI Element Checklist

> Comprehensive inventory of all UI components, layout nodes, interactive controls, and proposed widgets across the engine ecosystem.
>
> ### The 5 Status Levels (audit law — audited 2026-09-07 against callback invocation sites, `PointerEvent` handling, painter existence, and CMake wiring):
> 1. **`Implemented and Polishing`**: Renders AND handles events — clickable/scrollable/hoverable with live callbacks or pointer handling. Claim requires evidence: a fired callback or an `onPointer`/scroll path, not a stored fn pointer.
> 2. **`Implemented`**: Renders (own painter or live gallery geometry), but has NO events — callbacks stored-never-fired, no pointer/key handling.
> 3. **`Incomplete`**: Wired to CMake (`.c` in `projects/darling/CMakeLists.txt`) but NOT rendered — no painter, not shown in the gallery, needs more work.
> 4. **`Draft`**: Struct-only header with NO `.c` and NO CMake entry — not wired, not rendered.
> 5. **`Not Implemented`**: Purely conceptual / architectural proposals specced in `UI_CATALOG.md` with zero source code written yet.
>
> Hard facts behind this table: 11 controls now have live event handling, hit-testing, and verified callbacks in automated test suites (`Label`, `Switch`, `ScrollContainer`, `Button`, `Checkbox`, `RadioGroup`, `Slider`, `Knob`, `ScrollBar`, `Input`, `Textarea`); header-only files are `material_panel.h`, `object3d.h`, `viewer3d.h`, `video_panel.h`, `dialog.h`, `alertdialog.h`, `colordialog.h`.

---

## 1. Core Substrates & Layout Primitives

| Component | File / Location | Status | Details & Next Polish Tasks |
|---|---|---|---|
| **`Container`** | `darling/container.h/.c` | `Implemented` | The layout source of truth: 9-grid parent anchors, 4-corner self anchors, pivot, additive margin, corner radius (circular + superellipse), clipping, visibility, and hit-testing. Renders nothing itself, handles no events — layout substrate. |
| **`Panel`** | `darling/panel/panel.h/.c` | `Implemented` | Base visual tree node: solid color quad, image/filter slots, custom `renderHandler` slot, child attachment (detach-only). Painted by parent surfaces; no events. |
| **`Canvas`** | `darling/scene/canvas.h/.c` | `Implemented` | Root layout surface managing dirty-node fanning and frame layout passes. No events. |
| **`Scene`** | `darling/scene/scene.h/.c` | `Implemented` | 2D/3D composite stamp node for Vulkan swapchain presentation. No events. |
| **`Compositor`** | `darling/compositor.h/.c` | `Implemented` | Multi-IOSurface front-to-back layer compositor routing paint commands to Vulkan pipelines and AppKit CALayers. No events. |
| **`OverlayRoot`** | `_docs/UI_CATALOG.md #10` | `Not Implemented` | Top-level full-window overlay layer escaping child clip rects. Zero source — required for dropdown popups, modal dialogs, and tooltips. |
| **`Theme System`** | `_docs/UI_CATALOG.md #1` | `Not Implemented` | Central design token table (`THEME_SURFACE`, `THEME_PRIMARY`, `THEME_ON_SURFACE`, etc.), dual light/dark ramps, and WCAG contrast auditing. Zero source. |
| **`FocusRing`** | `_docs/UI_CATALOG.md #9` | `Not Implemented` | Accessible focus ring indicator driven by keyboard Tab navigation and `:focus-visible` state. Zero source. |

---

## 2. Panels & Containers

| Component | File / Location | Status | Details & Next Polish Tasks |
|---|---|---|---|
| **`ScrollContainer`** | `darling/panel/scrollcontainer.h/.c` | `Implemented and Polishing` | Live trackpad scrolling (`onScroll → scrollBy`), fling/spring `tick`, two-way bar sync, end-clamped offsets. Events: yes. **Polish**: elastic edge-bounce resistance, smooth deceleration, theme scrollbar styling. |
| **`ListContainer`** | `darling/panel/listcontainer.h/.c` | `Implemented` | Indexed vertical and horizontal stack layout with configurable item spacing and cross-axis alignment. Used in chat bubbles and gallery sections. No events. |
| **`GridContainer`** | `darling/panel/gridcontainer.h/.c` | `Implemented` | Fixed-dimension row × column grid with uniform cell gaps and cell panel assignment. No events. |
| **`SectionContainer`** | `darling/panel/sectioncontainer.h/.c` | `Implemented` | Tabbed switcher: header strip + one visible child (hidden detached, zero layers), `SCROLL`/`SHRINK` overflow, `NONE`/`CROSSFADE` transitions with bounded fade clock. Suite: `sectioncontainer_test`. No events. |
| **`LayeredContainer`** | `darling/panel/layeredcontainer.h/.c` | `Implemented` | Z-stacked overlapping container for HUD overlays, floating badges, and modal backdrops. No events. |
| **`SplitContainer`** | `darling/panel/splitcontainer.h/.c` | `Implemented` | Tiled splitter: N children share the box by normalized fractions along one axis (all live); lift-then-set layout tracks growth. Suite: `splitcontainer_test`. Drag-resize + min sizes deferred. No events. |
| **`MarkdownPanel`** | `darling/panel/markdown_panel.h/.c` | `Implemented` | Document parser scanning Markdown strings to vertically stacked `Label` and `RichLabel` rows. No events. |
| **`RichTextPanel`** | `darling/panel/richtext_panel.h/.c` | `Implemented` | Rich formatted text document panel backed by the `RichText` styled-run model. No events. |
| **`MaterialPanel`** | `darling/panel/material_panel.h` | `Draft` | Header-only shell, unwired to CMake. Awaiting graphvex lit material path. |
| **`FlexPanel`** | `_docs/UI_CATALOG.md #10` | `Not Implemented` | Proposed CSS-flex-style container with row/column flow, wrapping, gap, justify, align, and grow/shrink factors. |
| **`SplitPanel`** | `_docs/UI_CATALOG.md #10` | `Not Implemented` | Proposed two-pane container with draggable divider bar, split ratio, and min-size enforcement. |
| **`TabPanel`** | `_docs/UI_CATALOG.md #10` | `Not Implemented` | Proposed tabbed interface with top/side tab strip and active body swapping. |
| **`DockPanel`** | `_docs/UI_CATALOG.md #10` | `Not Implemented` | Proposed IDE-style docking container with left/right/top/bottom/center regions and splitters. |
| **`CardPanel`** | `_docs/UI_CATALOG.md #10` | `Not Implemented` | Proposed SaaS surface card with header, body, and footer slots, elevation shadows, and corner presets. |

---

## 3. Buttons & Selection Controls

| Component | File / Location | Status | Details & Next Polish Tasks |
|---|---|---|---|
| **`Button`** | `darling/button/button.h/.c` | `Implemented and Polishing` | PROMOTED (Pkg 2): `Button_press` invokes `onPress(ctx)`, `Button_handlePointer` handles `PTR_ENTER/HOVER/LEAVE/DOWN/UP` (click-on-release inside bounds). Verified by `button_test`. **Polish**: painter state styling (bgHover/bgPressed). |
| **`Switch`** | `darling/button/switch.h/.c` | `Implemented and Polishing` | Live event toggling (`Switch_handlePointer` on `PTR_UP` inside bounds invokes `Switch_setOn`). Verified by `switch_test`. **Polish**: animated thumb, focus ring. |
| **`Checkbox`** | `darling/field/checkbox.h/.c` | `Implemented and Polishing` | PROMOTED (Pkg 2): `Checkbox_toggle` clears indeterminate and invokes `onChange(ctx)`, `Checkbox_handlePointer` toggles on `PTR_UP` inside bounds. Verified by `checkbox_test`. **Polish**: checkmark custom painter styling. |
| **`RadioGroup`** | `darling/field/radiogroup.h/.c` | `Implemented and Polishing` | PROMOTED (Pkg 2): dynamic options via `List_1(TYPE_POINTER)`, `RadioGroup_select` enforces mutual exclusion and fires `onSelect(ctx)`, `RadioGroup_handlePointer` maps clicks to column/row items on `PTR_UP`. Verified by `radiogroup_test`. |

---

## 4. Fields & Inputs

| Component | File / Location | Status | Details & Next Polish Tasks |
|---|---|---|---|
| **`Input`** | `darling/field/input.h/.c` | `Implemented and Polishing` | PROMOTED (Pkg 4): `Input_handlePointer` DOWN focuses and positions caret; `Input_handleKey` consumes printable chars, backspace, and navigation arrows; fires `onChange(ctx)` on edit and `onSubmit(ctx)` on Enter. Verified by `darling_input_test`. **Polish**: selection drag, font measure hook. |
| **`Knob`** | `darling/field/knob.h/.c` | `Implemented and Polishing` | PROMOTED (Pkg 3): `Knob_handlePointer` handles rotary drag tracking via `atan2f` angle mapped to normalized `[0..1]`; `Knob_setNormalized` fires `onChange(ctx)`. Verified by `knob_test`. **Polish**: snap detents, bipolar bipolar indicator arc. |
| **`ColorPicker`** | `darling/field/colorpicker.h/.c` | `Incomplete` | DEMOTED (audit): `setHSV` stub, no painter, never shown in gallery, `onChange` dead. Wired to CMake but unrendered. |
| **`InputOTP`** | `darling/field/inputotp.h/.c` | `Incomplete` | DEMOTED (audit): `pushDigit` stub, no painter, not in gallery, no events. Wired but unrendered. |
| **`Select`** | `darling/field/select.h/.c` | `Incomplete` | DEMOTED (audit): `add`/`clear` stubs, no painter, popup needs `OverlayRoot`. Wired but unrendered. |
| **`ColorSwatch`** | `darling/field/colorswatch.h/.c` | `Incomplete` | DEMOTED (audit): `onSelect` never fired, no painter, not in gallery. Wired but unrendered. |
| **`Slider`** | `darling/field/slider.h/.c` | `Implemented and Polishing` | PROMOTED (Pkg 3): `Slider_handlePointer` handles `PTR_DOWN` and `PTR_DRAG` across horizontal/vertical orientation with step snapping (`roundf`) and bounds clamping; fires `onChange(ctx)`. Verified by `slider_test`. **Polish**: thumb painter styling, tick marks. |
| **`Textarea`** | `darling/field/textarea.h/.c` | `Implemented and Polishing` | PROMOTED (Pkg 4): `Textarea_handlePointer` DOWN focuses; `Textarea_handleKey` handles multi-line typing, enter newline, backspace line joining, cursor arrows (up/down/left/right) with column clamping and scroll tracking; fires `onChange(ctx)`. Verified by `textarea_test`. **Polish**: horizontal scroll, selection range. |
| **`ScrollBar`** | `darling/field/scrollbar.h/.c` | `Implemented and Polishing` | PROMOTED (Pkg 3): `ScrollBar_handlePointer` handles `PTR_DOWN` and `PTR_DRAG`, mapping local offset ratio to `ScrollBar_clickAt` fraction and scroll bounds clamping. Verified by `scrollbar_test`. **Polish**: thumb grip styling, fading timer. |
| **`DatePicker`** | `darling/field/datepicker.h/.c` | `Incomplete` | MOVED from Draft (audit): `.c` IS wired to CMake, so not Draft — but `setToday` stub, no painter, no popup, no events. Wired but unrendered. |

---

## 5. Labels & Typography

| Component | File / Location | Status | Details & Next Polish Tasks |
|---|---|---|---|
| **`Label`** | `darling/label/label.h/.c` | `Implemented and Polishing` | CONFIRMED (audit): CoreText cached raster + SDF fallback rendering AND `Label_onPointer` hover handling with `Cursor` switching (`IBEAM` on hover). Renders + events. **Polish**: text auto-wrapping, truncation ellipsis (`...`), design token roles. |
| **`Kbd`** | `darling/label/kbd.h/.c` | `Implemented` | DEMOTED (audit): keycap badge renders, no events. **Polish**: 3D keycap bottom shadow/depth, border contrast, standard size presets. |
| **`Typography`** | `darling/label/typography.h/.c` | `Implemented` | DEMOTED (audit): type scale roles render via the label path, no events. **Polish**: dynamic binding to global `Theme` font tokens. |
| **`RichLabel`** | `darling/label/rich_label.h/.c` | `Implemented` | Multi-run styled text node with bold, italic, code, color, and underline spans rendered via SDF glyphs (`RichLabel_renderFn`). No events. |

---

## 6. Media, 3D & Data Visualization

| Component | File / Location | Status | Details & Next Polish Tasks |
|---|---|---|---|
| **`Picture`** | `darling/picture/picture.h/.c` | `Implemented` | DEMOTED (audit): texture backing + UV crop + fit modes render, no events. **Polish**: aspect ratio edge-case clamping, placeholder fallback on load failure, border/radius clipping. |
| **`Plot`** | `darling/plot/plot.h/.c` | `Incomplete` | DEMOTED (audit): data/range setters store values but `autorange`/`hitPick` are stubs, no painter, absent from gallery. Wired but unrendered. |
| **`VideoPanel`** | `darling/picture/video_panel.h` | `Draft` | Header-only shell, unwired. Awaits VFS media decoder backend. |
| **`Object3D`** | `darling/scene/object3d.h` | `Draft` | Header-only shell, unwired. Awaits graphvex `Mesh` GPU draw path. |
| **`Viewer3D`** | `darling/scene/viewer3d.h` | `Draft` | Header-only shell, unwired. Awaits `Object3D` + orbit camera. |

---

## 7. Interaction, Animation & Windowing Substrate

| Component | File / Location | Status | Details & Next Polish Tasks |
|---|---|---|---|
| **`Cursor`** | `darling/cursor/cursor.h/.c` | `Implemented` | Darling cursor abstraction with zero-allocation predefined singletons and native window application via `Cursor_apply` (driven by `Label_onPointer` hover). Substrate bridge — no render of its own. |
| **`Window`** | `hotcwap/window/window.h/.c` | `Implemented` | Native macOS Cocoa window bridge supporting vibrancy blur, borderless/decorated styles, swapchain alpha, and `NSCursor` switching. Substrate. |
| **`Anim`** | `darling/anim/anim.h/.c` | `Implemented` | Property animation player with easing curves and keyframe interpolation. Substrate — drives visuals, handles no events. |

---

## 8. Dialogs & Overlays

| Component | File / Location | Status | Details & Next Polish Tasks |
|---|---|---|---|
| **`FileDialog`** | `darling/overlay/filedialog.h/.c` | `Incomplete` | MOVED from Draft (audit): `.c` IS wired to CMake with navigation/filter logic, but GUI rendering pending overlay phase. Wired but unrendered. |
| **`Dialog`** | `darling/dialog/dialog.h` | `Draft` | MOVED from Incomplete (audit): header-only shell, unwired to CMake — exactly Draft. Awaits `OverlayRoot`. |
| **`AlertDialog`** | `darling/dialog/alertdialog.h` | `Draft` | MOVED from Incomplete (audit): header-only, unwired. Awaits `OverlayRoot`. |
| **`ColorDialog`** | `darling/color/colordialog.h` | `Draft` | MOVED from Incomplete (audit): header-only, unwired. Awaits `OverlayRoot`. |
| **`Toast` / `ToastStack`** | `_docs/UI_CATALOG.md #9` | `Not Implemented` | Proposed non-modal notification banner queue with automatic timeout dismissal and action buttons. |
| **`Tooltip`** | `_docs/UI_CATALOG.md #11` | `Not Implemented` | Proposed hover/focus hint bubble with directional pointer arrow escaping container bounds. |
| **`Popover`** | `_docs/UI_CATALOG.md #11` | `Not Implemented` | Proposed click-anchored floating card with light dismiss and focus trap. |
| **`Menu` / `ContextMenu`** | `_docs/UI_CATALOG.md #11` | `Not Implemented` | Proposed hierarchical dropdown / right-click menu with menu items, icons, shortcuts, and separators. |

---

## 9. Proposed Everyday & SaaS Kit Widgets

| Component | File / Location | Status | Details & Next Polish Tasks |
|---|---|---|---|
| **`ProgressBar`** | `_docs/UI_CATALOG.md #9` | `Not Implemented` | Proposed progress indicator with determinate percentage fill and indeterminate loading sweep. |
| **`Spinner`** | `_docs/UI_CATALOG.md #9` | `Not Implemented` | Proposed circular rotating loading indicator. |
| **`Skeleton`** | `_docs/UI_CATALOG.md #9` | `Not Implemented` | Proposed shimmer animated placeholder card/text rows for loading states. |
| **`Avatar`** | `_docs/UI_CATALOG.md #11` | `Not Implemented` | Proposed user avatar supporting photo image, fallback initials, and status presence dot. |
| **`Badge` / `Pill`** | `_docs/UI_CATALOG.md #11` | `Not Implemented` | Proposed compact status badge with tone variants (`SUCCESS`, `WARNING`, `DANGER`, `INFO`). |
| **`Chip`** | `_docs/UI_CATALOG.md #11` | `Not Implemented` | Proposed interactive tag token with optional remove icon button. |
| **`SearchField`** | `_docs/UI_CATALOG.md #11` | `Not Implemented` | Proposed search input with leading icon, clear button, and shortcut badge. |
| **`Breadcrumb`** | `_docs/UI_CATALOG.md #11` | `Not Implemented` | Proposed hierarchical path navigation with clickable segments and separators. |
| **`Pagination`** | `_docs/UI_CATALOG.md #11` | `Not Implemented` | Proposed page number navigator with previous/next controls and page size selector. |
| **`Accordion`** | `_docs/UI_CATALOG.md #11` | `Not Implemented` | Proposed expandable/collapsible disclosure groups with smooth height animation. |
| **`TreePanel`** | `_docs/UI_CATALOG.md #10` | `Not Implemented` | Proposed hierarchical tree view with collapsible rows for file trees and scene graphs. |
| **`TablePanel` / `DataTable`** | `_docs/UI_CATALOG.md #10, #12` | `Not Implemented` | Proposed data grid with column headers, sorting, row selection, column resizing, and pagination. |
| **`CommandPalette`** | `_docs/UI_CATALOG.md #12` | `Not Implemented` | Proposed modal quick-open palette (`⌘K`) with fuzzy search and action dispatching. |
| **`StatCard`** | `_docs/UI_CATALOG.md #12` | `Not Implemented` | Proposed KPI metric card composing `CardPanel`, trend `Pill`, and sparkline `Plot`. |

---

## 10. Summary Matrix by Status

```
┌────────────────────────────┬───────┬────────────────────────────────────────────────────────┐
│ Status Level               │ Count │ Components                                             │
├────────────────────────────┼───────┼────────────────────────────────────────────────────────┤
│ 1. Implemented & Polishing │  11   │ Label (pointer+hover), Switch (pointer+fires onChange),│
│   (renders + events)       │       │ ScrollContainer (trackpad scroll + bar sync),              │
│                            │       │ Button (pointer+fires onPress),                        │
│                            │       │ Checkbox (pointer+fires onChange),                     │
│                            │       │ RadioGroup (pointer+options+fires onSelect),           │
│                            │       │ Slider (drag+step+fires onChange),                     │
│                            │       │ Knob (rotary drag+fires onChange),                     │
│                            │       │ ScrollBar (drag+clickAt fraction),                     │
│                            │       │ Input (caret+pointer focus+keys+fires onChange/submit),│
│                            │       │ Textarea (multiline+keys+pointer focus+fires onChange) │
├────────────────────────────┼───────┼────────────────────────────────────────────────────────┤
│ 2. Implemented             │  18   │ Container, Panel, Canvas, Scene, Compositor,           │
│   (renders, no events)     │       │ ListContainer, GridContainer, SectionContainer, LayeredContainer,      │
│                            │       │ MarkdownPanel, RichTextPanel, RichLabel, Cursor,       │
│                            │       │ Window, Anim, Kbd, Typography, Picture                 │
├────────────────────────────┼───────┼────────────────────────────────────────────────────────┤
│ 3. Draft                   │   7   │ MaterialPanel, VideoPanel, Object3D, Viewer3D,         │
│   (struct-only, unwired)   │       │ Dialog, AlertDialog, ColorDialog                       │
├────────────────────────────┼───────┼────────────────────────────────────────────────────────┤
│ 4. Incomplete              │   7   │ DatePicker, FileDialog, Plot, Select, InputOTP,        │
│   (wired, unrendered)      │       │ ColorPicker, ColorSwatch                               │
├────────────────────────────┼───────┼────────────────────────────────────────────────────────┤
│ 5. Not Implemented         │  26   │ FlexPanel, SplitPanel, TabPanel, DockPanel,            │
│   (zero source)            │       │ CardPanel, Toast/ToastStack, Tooltip, Popover,         │
│                            │       │ Menu/ContextMenu, ProgressBar, Spinner, Skeleton,      │
│                            │       │ Avatar, Badge/Pill, Chip, SearchField, Breadcrumb,     │
│                            │       │ Pagination, Accordion, TreePanel, DataTable,           │
│                            │       │ CommandPalette, StatCard, OverlayRoot, Theme,          │
│                            │       │ FocusRing                                              │
├────────────────────────────┼───────┼────────────────────────────────────────────────────────┤
│ Total Tracked Inventory    │  69   │ Complete UI element landscape across all engine layers │
└────────────────────────────┴───────┴────────────────────────────────────────────────────────┘
```

Audit trail: every DEMOTED/PROMOTED/MOVED row above cites mechanics (`Switch_setOn` fires; `Button_press` no-op; `dispatch.c` stubs; `Label_onPointer` live; CMake source list). A row reclaims its old status only by landing the named missing piece (painter, fired callback, or CMake entry) — not by argument.

# darling — Widget Interfaces, Layout & Host Bridges

> **R2 split:** [vexspoke](#file-vexspoke-md) owns CPU computation/behavior; [relational-engine](#file-relational-engine-md)
> owns memory/storage/native C search. Darling's include allowlist stays Vexspoke
> + Graphvex + Hotcwap. Migration is staged with unchanged default allocation;
> this creates no direct engine dependency or automatic schema migration. R1 owns
> lifetimes/residency; Graphvex R3 owns graphics composition, shaders and dispatch.

> R4 UI architecture. Current status is source-based, not inherited from retired code.
> Governed by the Single Class Per File Law (Java Law), Living Documentation Law,
> Vertical Integration Law, Native Pixel Law and Timestamped Test Checklist Law.

---

## Current implementation checklist (2026-10-04)

**The current toolkit is a working substrate, not the old completed widget library.**
Text really is missing. ScrollPanel has a low-level implementation, but not all
the pieces needed for a ready-to-use scrolling control. Canonical current gaps:
`../interface/darling-framework/STATUS.md`.

| Component | Implemented now | Scoped lab evidence | Remaining work |
| :--- | :--- | :--- | :--- |
| Frame | Window/root + retained presentation/revalidation implementation | Existing code; not run as a real-window test in this audit | User visual/interaction approval; native scope not re-proved here |
| Panel | Element wrapper, child tree/ownership, geometry and paint properties | Fresh headless `panel_test`, `properties_test`, `panel_events_test` pass | Higher-level controls/layouts are not supplied by a plain Panel |
| ScrollPanel | Partial viewport/content, offset clamp/reclamp, clipping/revalidation | Fresh headless `scroll_panel_test`; synthetic scroll callback in `panel_events_test` | Default wheel/trackpad behavior, typed attachment/ownership, ScrollBar and user visual approval |
| Shared properties/events | Live add/remove/location/size/bounds/radius, registration/bubbling | Fresh `properties_test`, `event_invoke_test`, `event_kinds_test` | Draft operations and focus/control policies; native input not exercised |
| Hover cursor | Live preference/inheritance and hit selection | Fresh headless `set_cursor_test` | Native appearance remains user-unverified |
| TextCore / Label / typography | 🟥 Draft only — no callable text widget API/storage | Scaffold structure/compilation only; **not text behavior** | Driver font/glyph path, measurement, Label paint/storage, then selection/editing |
| Buttons, inputs, layouts, overlays, etc. | 🟥 125 draft pairs in `scaffolds.json` | Compilation of drafts is not implementation | Implement one real component at a time |

### Catch-up checklist

- [x] Establish the Frame/Panel substrate, shared property operations and event/cursor plumbing.
- [x] Establish ScrollPanel's programmatic viewport/clamp core and explicit callback registration.
- [ ] Deliver automatic/nested wheel scrolling, typed ScrollPanel attachment and scrollbar widgets.
- [ ] Restore/reimplement **real text rendering**: live raster `drawText` is a no-op;
  Vulkan `drawText` ignores the string and submits glyph zero. Neither is a font/shaping pipeline.
- [ ] Implement a basic Label on that driver path; TextCore/Label declarations currently remain drafts.
- [ ] Run meaningful owner lab tests, then collect the user's visual feedback.

Fresh audit scope: **7 headless checks passed**, no windows or demos executed.
Actual Unix completion times, file hashes and command descriptions are in
`../../tests/test-checklist.md`; this table is implementation status, not blanket proof.
Earlier text/Label/font code remains in `_trash/darling-framework/` and
`_trash/graphvex/`, outside the live build. Do not blindly resurrect old APIs.

## Current Remastered Scaffold Map (2026-10-03)

> The older component ratings below describe a previous implementation generation.
> They are not readiness claims for the current remastered source tree. The new
> source pairs listed here are **drafts only**, with definitions/overviews and
> opaque class declarations or procedural placeholders: no runtime APIs or storage.
> Compilation/structure lab evidence is not implementation or visual approval.

Canonical source inventory: `../interface/darling-framework/scaffolds.json`.
Implementation boundaries and sequence: `../interface/darling-framework/SCAFFOLDS.md`.
Existing Frame, Panel, ScrollPanel, event dispatch and shared operations are untouched.
Their current limitations are listed above; "untouched" does not mean complete.
Legacy Container names map to Panel compositions; native Window, Color representation,
font/raster/Surface and leaf I/O remain owned by their existing lower-level repositories.

| Component/module | Current source pair | Current scope/status |
| :--- | :--- | :--- |
| `Anim` | `src/anim/anim.c` / `.h` | 🟥 Draft — Owner-driven property-animation player with easing/spring policies; no independent tick thread or duplicated scheduler. |
| `Clipboard bridge` | `src/bridge/clipboard.c` / `.h` | 🟥 Draft — Translate UI selection/copy/paste intent into existing vexspoke io/clipboard.h; do not redeclare or duplicate Clipboard_* native functions. |
| `Font bake bridge` | `src/bridge/font_bridge.c` / `.h` | 🟥 Draft — UI font request/cache binding over borrowed graphvex font resources; no new font baker. |
| `Panel Cocoa bridge` | `src/bridge/panel_bridge.c` / `.h` | 🟥 Draft — UI Panel/Board attachment and lifecycle glue over the existing single Frame presentation seam. |
| `Text ObjC bridge` | `src/bridge/text_bridge.c` / `.h` | 🟥 Draft — Platform-capability routing for text shaping/rasterization supplied by the driver/host, with no native implementation in this draft. |
| `Window bridge` | `src/bridge/window_bridge.c` / `.h` | 🟥 Draft — UI root attachment/resize/input glue over hotcwap Window; never a second Window class or native backend. |
| `Button` | `src/button/button.c` / `.h` | 🟥 Draft — Pressable compound Panel with label/icon/accessory slots, variants, enabled/loading state and keyboard activation intent. |
| `Checkbox` | `src/button/checkbox.c` / `.h` | 🟥 Draft — Checked/indeterminate Panel with label hit region, value notifications and keyboard activation intent. |
| `Switch` | `src/button/switch.c` / `.h` | 🟥 Draft — Boolean-choice Panel with track/thumb composition, change notifications and eventual animated state transitions. |
| `Darling type registry` | `src/c23/darling-type.c` / `.h` | 🟥 Draft — Future single Darling class registry; allocate no identities for unimplemented drafts and never duplicate lower-level registry IDs. |
| `Canvas` | `src/canvas/canvas.c` / `.h` | 🟥 Draft — Coordinate a root content tree and borrowed Surface/Boards; fan dirty branches and keep multiwindow presentation independent. |
| `CodeField` | `src/code/code_field.c` / `.h` | 🟥 Draft — Editable code-text widget with language tokens, line-number gutter, caret/selection and future folding/multicaret policies. |
| `Color helpers` | `src/color/color.c` / `.h` | 🟥 Draft — UI color-format conversion policy using the existing graphvex Color scalar; do not introduce an incompatible second Color typedef. |
| `Select` | `src/combo/select.c` / `.h` | 🟥 Draft — Compound selection widget with trigger/value/content/item roles, keyboard selection and overlay popup/filter policy. |
| `Compositor` | `src/compositor/compositor.c` / `.h` | 🟥 Draft — Order borrowed scene/content/overlay Boards into the single Frame presentation seam, with no second OS window or duplicate rendering loop. |
| `Cursor` | `src/cursor/cursor.c` / `.h` | 🟥 Draft — UI cursor-selection facade; native cursor handles and application remain with the R1 host. |
| `Hover cursor property` | `src/properties/set_cursor.c` / `.h` | 🟨 Implemented for Element/Panel/ScrollPanel/Frame; macro-generated class APIs, per-node inheritance and masked hit resolution. Headless selection/lifetime tests pass; native appearance and pointer-lock/window-exit policies remain unverified. Draft widgets have no runtime cursor setters yet. |
| `AlertDialog` | `src/dialog/alert_dialog.c` / `.h` | 🟥 Draft — Dialog composition for title, body and confirmation actions, preserving modal close/cancel policy. |
| `ColorDialog` | `src/dialog/color_dialog.c` / `.h` | 🟥 Draft — Dialog composition for a ColorPicker and live color-change/result notifications. |
| `Dialog` | `src/dialog/dialog.c` / `.h` | 🟥 Draft — Modal UI wrapper over an owned/borrowed Frame contract; modal focus/close policies must use the R1 host window seam. |
| `FileDialog` | `src/dialog/file_dialog.c` / `.h` | 🟥 Draft — Dialog composition for path/filter/entry selection; file access is borrowed from vexspoke, never a new filesystem backend. |
| `InputDialog` | `src/dialog/input_dialog.c` / `.h` | 🟥 Draft — Dialog composition for a text prompt, bounded input, submit/cancel results and focus return. |
| `OptionDialog` | `src/dialog/option_dialog.c` / `.h` | 🟥 Draft — Dialog composition for action choices and explicit result/cancellation ownership. |
| `Object3D` | `src/drawable/object_3d.c` / `.h` | 🟥 Draft — UI scene-node wrapper for borrowed mesh/material resources and transform hierarchy; GPU mesh ownership remains in graphvex. |
| `Picture` | `src/drawable/picture.c` / `.h` | 🟨 Borrowed RGBA8 CPU-shadow image, native initial size/stretch and explicit wrapper lifetime; `../../../tests/darling/drawable/picture_test.c` and native `filter_gallery --smoke` pass. Crop/fit modes and automatic filters remain absent; appearance not approved. |
| `Viewer3D` | `src/drawable/viewer_3d.c` / `.h` | 🟥 Draft — Scene3D viewer composition with orbit camera, lighting controls and Object3D content. |
| `Emoji text support` | `src/emoji/emoji.c` / `.h` | 🟥 Draft — Text fallback/emoji presentation policy for Label and rich-text content; shaping and native font capabilities remain borrowed. |
| `Action events` | `src/event/action.c` / `.h` | 🟥 Draft — Abstract UI command dispatch and activation policy using borrowed handler/context lifetimes. |
| `Event bridge` | `src/event/bridge.c` / `.h` | 🟥 Draft — Translate host event payloads into existing c23/event_invoke dispatch, preserving window-scoped coordinates and ownership. |
| `Document events` | `src/event/document.c` / `.h` | 🟥 Draft — Text mutation notification policy for insertion/removal/replacement over existing document event carriers. |
| `Focus events` | `src/event/focus.c` / `.h` | 🟥 Draft — Focus acquisition/release, traversal, focus-visible and modal trapping policy over the retained tree. |
| `Gesture events` | `src/event/gesture.c` / `.h` | 🟥 Draft — Gesture-recognition policy over borrowed scroll/pinch/pan payloads and owner-driven timing. |
| `Key events` | `src/event/key.c` / `.h` | 🟥 Draft — Focused-target keyboard delivery policy over shared event carriers; no Key struct duplication or blanket widget opt-ins. |
| `Tree events` | `src/event/tree.c` / `.h` | 🟥 Draft — Hierarchy mutation notification policy for attach/detach/dirty changes without duplicating the live tree operations. |
| `Value events` | `src/event/value.c` / `.h` | 🟥 Draft — Value-change notification policy for controls, with explicit delivery/reentrancy contracts to be defined. |
| `HtmlExporter` | `src/export/html_exporter.c` / `.h` | 🟥 Draft — UI-tree-to-HTML serialization policy; source tree is borrowed and output ownership/escaping must be defined before implementation. |
| `FocusRing` | `src/feedback/focus_ring.c` / `.h` | 🟥 Draft — Keyboard-focus indicator Panel tied to focus-visible policy, theme color and explicit offset. |
| `ProgressBar` | `src/feedback/progress_bar.c` / `.h` | 🟥 Draft — Determinate/indeterminate progress Panel with normalized value, fill and owner-driven animation. |
| `Skeleton` | `src/feedback/skeleton.c` / `.h` | 🟥 Draft — Loading-placeholder Panel with shape tokens and eventual owner-driven shimmer. |
| `Spinner` | `src/feedback/spinner.c` / `.h` | 🟥 Draft — Loading-indicator Panel with owner-driven phase and rendering intent; no independent animation thread. |
| `CooldownButton` | `src/game/cooldown_button.c` / `.h` | 🟥 Draft — Button composition with owner-driven cooldown phase, radial progress and hotkey/ready indicators. |
| `DamageNumbers` | `src/game/damage_numbers.c` / `.h` | 🟥 Draft — Pooled floating-text Panel coordinator with bounded combat-text lifetime and owner-driven motion. |
| `DialogBox` | `src/game/dialog_box.c` / `.h` | 🟥 Draft — NPC-dialogue Panel composition with portrait, text reveal and action choices. |
| `GamepadNav` | `src/game/gamepad_nav.c` / `.h` | 🟥 Draft — Spatial focus-navigation policy for D-pad directions, bumper tabs and device glyph requests. |
| `HudBar` | `src/game/hud_bar.c` / `.h` | 🟥 Draft — HUD value-bar Panel with primary fill, delayed ghost drain and damage-feedback intent. |
| `InventoryGrid` | `src/game/inventory_grid.c` / `.h` | 🟥 Draft — GridPanel composition for item slots, stack counts, tier styles, locks and drag/drop intent. |
| `Minimap` | `src/game/minimap.c` / `.h` | 🟥 Draft — Scene/Panel composition for map/radar content, player direction, pings and fog-mask intent. |
| `NodeEditor` | `src/graph/node_editor.c` / `.h` | 🟥 Draft — Retained graph-canvas widget with node/pin/socket models, connection curves and edit/selection intent. |
| `Plot` | `src/graph/plot.c` / `.h` | 🟥 Draft — Retained data-chart widget with borrowed data spans, line/bar/scatter modes, axes and data hit/tooltip intent. |
| `History` | `src/history/history.c` / `.h` | 🟥 Draft — UI command-history model with undo/redo and explicit borrowed command/payload lifetime contracts. |
| `Input` | `src/input/input.c` / `.h` | 🟥 Draft — Single-line text-entry widget with buffer ownership, caret, selection, placeholder, clipboard and submit/change intent. |
| `InputOTP` | `src/input/input_otp.c` / `.h` | 🟥 Draft — Passcode-entry Panel with digit slots, focus advance, paste splitting and bounded code storage. |
| `Knob` | `src/input/knob.c` / `.h` | 🟥 Draft — Rotary range-control Panel with angle math, detents, fine adjustment and value readout. |
| `ScrollBar` | `src/input/scroll_bar.c` / `.h` | 🟥 Draft — Track/thumb Panel composition driven by viewport/content ratios, seek/drag intent and horizontal/vertical orientation. |
| `SearchField` | `src/input/search_field.c` / `.h` | 🟥 Draft — Compound text input with search icon, clear action and optional shortcut badge. |
| `Slider` | `src/input/slider.c` / `.h` | 🟥 Draft — Range-selection Panel with normalization, step snapping, orientation, track/thumb composition and keyboard nudging. |
| `Textarea` | `src/input/textarea.c` / `.h` | 🟥 Draft — Multiline text-entry widget with document mutations, wrapping, line navigation and viewport/caret synchronization. |
| `Avatar` | `src/kit/avatar.c` / `.h` | 🟥 Draft — Photo/initials Panel composition with optional presence badge and image fallback policy. |
| `Badge` | `src/kit/badge.c` / `.h` | 🟥 Draft — Status-badge Panel with semantic tone, size and text/icon slots. |
| `Breadcrumb` | `src/kit/breadcrumb.c` / `.h` | 🟥 Draft — Hierarchical navigation-path Panel with separators, current item and action intent. |
| `Chip` | `src/kit/chip.c` / `.h` | 🟥 Draft — Interactive tag Panel with dismiss action, optional avatar and selection/enabled policy. |
| `Pagination` | `src/kit/pagination.c` / `.h` | 🟥 Draft — Page-navigation Panel with page count/current page, boundaries and previous/next actions. |
| `Pill` | `src/kit/pill.c` / `.h` | 🟥 Draft — Compact pill-shaped status/tag Panel, sharing Badge/theme conventions without duplicating layout machinery. |
| `StatCard` | `src/kit/stat_card.c` / `.h` | 🟥 Draft — KPI CardPanel composition with value, trend and borrowed Plot/sparkline content. |
| `Kbd` | `src/label/kbd.c` / `.h` | 🟥 Draft — Keycap text badge with monospaced typography, key-symbol presentation and theme spacing. |
| `Label` | `src/label/label.c` / `.h` | 🟥 Draft — Text widget with owned/borrowed text contracts, font requests, glyph-position hit testing, selection and clipboard intent. |
| `RichLabel` | `src/label/rich_label.c` / `.h` | 🟥 Draft — Text widget with multiple styled runs, shared selection coordinates and plain-text copy across markup. |
| `Container` | `src/layout/container.c` / `.h` | 🟥 Draft — Layout policy adapter over the existing graphvex Element; anchors, pivots, padding and sizing policies must not introduce a second geometry authority. |
| `ListPanel` | `src/list/list_panel.c` / `.h` | 🟥 Draft — Panel composition with indexed horizontal/vertical stacking, gaps, cross-axis alignment and content sizing. |
| `CommandPalette` | `src/overlay/command_palette.c` / `.h` | 🟥 Draft — Quick-action overlay with query/filter results, command selection and focus restoration. |
| `ContextMenu` | `src/overlay/context_menu.c` / `.h` | 🟥 Draft — Context-triggered Menu composition with point anchoring, action routing and dismissal/focus return. |
| `Menu` | `src/overlay/menu.c` / `.h` | 🟥 Draft — Hierarchical action-menu overlay with shortcuts, item selection and keyboard traversal policy. |
| `OverlayRoot` | `src/overlay/overlay_root.c` / `.h` | 🟥 Draft — Explicit top-level overlay tree that escapes content clips while retaining modal input isolation and one Frame presentation seam. |
| `Popover` | `src/overlay/popover.c` / `.h` | 🟥 Draft — Click-anchored overlay card with light-dismiss, focus return and clipping escape policy. |
| `Toast` | `src/overlay/toast.c` / `.h` | 🟥 Draft — Nonmodal notification Panel with message/action composition and owner-driven dismissal. |
| `ToastStack` | `src/overlay/toast_stack.c` / `.h` | 🟥 Draft — Retained queue/layout coordinator for Toast children, deadlines and removal without owning a timer thread. |
| `Tooltip` | `src/overlay/tooltip.c` / `.h` | 🟥 Draft — Hover-hint overlay with placement/arrow intent and bounded lifetime; timers are borrowed from the owner loop. |
| `Accordion` | `src/panel/accordion.c` / `.h` | 🟥 Draft — Disclosure-group Panel composition with single/multiple expansion policies and eventual animated layout. |
| `CardPanel` | `src/panel/card_panel.c` / `.h` | 🟥 Draft — Compound Panel with header, title, description, body and footer roles; elevation and spacing are properties. |
| `DockPanel` | `src/panel/dock_panel.c` / `.h` | 🟥 Draft — Panel composition with named dock regions and splitters, borrowing Frame geometry rather than owning native windows. |
| `FlexPanel` | `src/panel/flex_panel.c` / `.h` | 🟥 Draft — Panel composition with row/column flow, wrapping, gap, justification, alignment and hug/fill/fixed sizing policies. |
| `GridPanel` | `src/panel/grid_panel.c` / `.h` | 🟥 Draft — Panel composition with rows, columns, independent gaps, cell placement and future spanning policies. |
| `LayeredPanel` | `src/panel/layered_panel.c` / `.h` | 🟥 Draft — Overlapping child Panels with explicit ordering and topmost visible hit routing. |
| `MarkdownPanel` | `src/panel/markdown_panel.c` / `.h` | 🟥 Draft — Markdown block/inline parsing into retained text children, with selection, links and future code/table composition. |
| `MaterialPanel` | `src/panel/material_panel.c` / `.h` | 🟥 Draft — Panel facade for borrowed graphvex material-rendered content; no material shader or GPU ownership belongs here. |
| `RichTextPanel` | `src/panel/rich_text_panel.c` / `.h` | 🟥 Draft — Retained rich-text document Panel with styled runs, wrapping and document-wide selection. |
| `SectionPanel` | `src/panel/section_panel.c` / `.h` | 🟥 Draft — Compound titled header/body Panel with collapsible content and future animated height. |
| `SplitPanel` | `src/panel/split_panel.c` / `.h` | 🟥 Draft — Panel composition with pane ratios, divider interaction and min/max pane constraints; child ownership follows Panel. |
| `SvgPanel` | `src/panel/svg_panel.c` / `.h` | 🟥 Draft — Retained SVG display Panel with path/layout interpretation and borrowed driver rendering resources. |
| `TabPanel` | `src/panel/tab_panel.c` / `.h` | 🟥 Draft — Panel composition with tab strip, active content, close/reorder policies and focus transfer. |
| `TablePanel` | `src/panel/table_panel.c` / `.h` | 🟥 Draft — Multi-column data-grid Panel with sorting, headers, resize and paginated or virtualized rows. |
| `TreePanel` | `src/panel/tree_panel.c` / `.h` | 🟥 Draft — Hierarchical disclosure rows for file/scene trees, selection and large-tree virtualization policies. |
| `VideoPanel` | `src/panel/video_panel.c` / `.h` | 🟥 Draft — Panel facade for decoded media frames; decoder/process supervision and image upload remain with their lower-level owners. |
| `WebPanel` | `src/panel/web_panel.c` / `.h` | 🟥 Draft — Capability-gated native-web-content Panel facade; platform handles are borrowed through a host bridge, not an embedded browser runtime. |
| `ColorPicker` | `src/picker/color_picker.c` / `.h` | 🟥 Draft — Color-selection widget with HSV/hex editing, hue/saturation/value controls and borrowed sample intent. |
| `ColorSwatch` | `src/picker/color_swatch.c` / `.h` | 🟥 Draft — Selectable color-chip Panel with selection/change notifications and shared Color representation. |
| `DatePicker` | `src/picker/date_picker.c` / `.h` | 🟥 Draft — Date-selection widget with calendar model, month navigation and future popup/month-grid composition. |
| `set_alignment` | `src/properties/set_alignment.c` / `.h` | 🟥 Draft — Future content/cross-axis alignment operation; do not conflate it with anchor/pivot. |
| `set_anchor` | `src/properties/set_anchor.c` / `.h` | 🟥 Draft — Parent anchor property routing over existing Element/Panel placement; migrate existing setters here rather than define parallel behavior. |
| `set_background_color` | `src/properties/set_background_color.c` / `.h` | 🟥 Draft — Background paint routing; eventually migrate current setters while preserving explicit window-transparency independence. |
| `set_blur` | `src/properties/set_blur.c` / `.h` | 🟥 Draft — Own-edge/backdrop effect property routing with explicitly separate contracts and capability gates. |
| `set_border` | `src/properties/set_border.c` / `.h` | 🟥 Draft — Border width/color property routing; eventually migrate current widget setters and preserve CPU/GPU paint contracts. |
| `set_enabled` | `src/properties/set_enabled.c` / `.h` | 🟥 Draft — Future control enabled-state operation with input and appearance policy. |
| `set_focus` | `src/properties/set_focus.c` / `.h` | 🟥 Draft — Future focus-state operation over the event/focus coordinator and retained tree. |
| `set_font` | `src/properties/set_font.c` / `.h` | 🟥 Draft — Future typography/font request operation that borrows lower-level font resources. |
| `set_gap` | `src/properties/set_gap.c` / `.h` | 🟥 Draft — Future flow/grid child-gap operation with layout revalidation policy. |
| `set_margin` | `src/properties/set_margin.c` / `.h` | 🟥 Draft — Future additive external-spacing operation; semantics must remain separate from anchor/location and be defined before implementation. |
| `set_padding` | `src/properties/set_padding.c` / `.h` | 🟥 Draft — Future inner-spacing operation; layout contribution and interaction with child sizing must be specified before implementation. |
| `set_pivot` | `src/properties/set_pivot.c` / `.h` | 🟥 Draft — Self-pivot property routing over existing Element/Panel placement; migrate existing setters here rather than define parallel behavior. |
| `set_scroll_offset` | `src/properties/set_scroll_offset.c` / `.h` | 🟥 Draft — Future shared scroll-offset operation preserving ScrollPanel clamp/revalidation semantics. |
| `set_shadow` | `src/properties/set_shadow.c` / `.h` | 🟥 Draft — Shadow offset/blur/color property routing; eventually migrate existing setters and retain layout-versus-paint bounds. |
| `set_sizing_mode` | `src/properties/set_sizing_mode.c` / `.h` | 🟥 Draft — Future fixed/hug/fill layout policy operation with explicit measurement semantics. |
| `set_text` | `src/properties/set_text.c` / `.h` | 🟥 Draft — Future text-content ownership/mutation operation for text widgets; no setters declared until their types/lifetimes exist. |
| `set_theme` | `src/properties/set_theme.c` / `.h` | 🟥 Draft — Future theme-token binding operation for widgets and compound parts. |
| `set_value` | `src/properties/set_value.c` / `.h` | 🟥 Draft — Future typed control-value operation with range/clamp/notification contracts. |
| `set_visible` | `src/properties/set_visible.c` / `.h` | 🟥 Draft — Visibility property routing and eventual revalidation/input consequences; migrate existing setters rather than add competing implementations. |
| `RadioGroup` | `src/radio/radio_group.c` / `.h` | 🟥 Draft — Exclusive option-list Panel with selection, disabled-option policy and eventual arrow-key traversal. |
| `Scene` | `src/scene/scene.c` / `.h` | 🟥 Draft — Common retained scene interface that borrows graphvex Board/Image targets and participates in the Frame revalidation cascade. |
| `Scene2D` | `src/scene/scene_2d.c` / `.h` | 🟥 Draft — Retained 2D scene composition with transforms, ordering and pixel/percentage sizing; GPU execution remains in graphvex. |
| `Scene3D` | `src/scene/scene_3d.c` / `.h` | 🟥 Draft — Retained 3D scene composition with camera, lighting and sizing policies; mesh rendering and resource retirement remain in graphvex. |
| `IconImage` | `src/shape/icon_image.c` / `.h` | 🟥 Draft — Vector/SDF icon-display widget requesting borrowed icon atlas resources and theme-driven sizing/color. |
| `PropertyInspector` | `src/spatial/property_inspector.c` / `.h` | 🟥 Draft — Retained property-editing Panel composition with explicit bindings for geometry, paint and text; edits use shared properties operations. |
| `SpatialCanvas` | `src/spatial/spatial_canvas.c` / `.h` | 🟥 Draft — Retained pan/zoom content-canvas policy with guides, minimap and borrowed driver transforms; no separate render loop. |
| `TransformBox` | `src/spatial/transform_box.c` / `.h` | 🟥 Draft — Interactive bounding-handle Panel with translation/scale/rotation intent, aspect locking and geometry constraints. |
| `TextCore` | `src/text/text_core.c` / `.h` | 🟥 Draft — UI-side styled-run, text-layout and selection model; native glyph shaping/rasterization is a borrowed driver capability. |
| `Typography` | `src/text/typography.c` / `.h` | 🟥 Draft — UI type-role policy mapping caption/body/title/display/mono roles to borrowed font resources and theme tokens. |
| `Theme` | `src/theme/theme.c` / `.h` | 🟥 Draft — UI design tokens for color ramps, spacing, typography and elevation; styles reuse graphvex Color/Property rather than redefining them. |

---

<details>
<summary>Historical generation archive — all ratings, binaries and priorities below are non-current</summary>

**Archive only.** The old green/yellow widget ratings and `darling_gallery`
proof below describe retired source, not the current remastered build. In
particular, old Label/text/font/scroll-container claims must not override the
current implementation checklist. Keep this material as design/reference history,
not as a readiness checklist, build instruction or current task order.

## 🎯 Tier-0 Integration Proofs (Ground Truth)

*The live binary is the final judge. This table gates the repo headline — never the rows below, which keep their own independent truth. Statuses are re-verified, never copied from memory.*

| Proof Binary | End-to-End User Verification | Status | Evidence |
|---|---|:---:|---|
| `darling_gallery` | Boot window → drag text select (tracks glyphs) → Cmd+C copies → button hover states | 🟨 | Builds clean `-Wall -Wextra -Werror`, boots to event loop (observed); click/hover/type unverified headless |

## The Darling Standard: The Four Pillars

Darling does not choose between developer-ergonomic SaaS toolkits and raw game-engine UI. It bridges them into a singular, high-performance retained architecture that surpasses **Dear ImGui**, **raylib GUI**, and standard web frameworks:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             THE DARLING STANDARD                                 │
├─────────────────────────┬─────────────────────────┬──────────────────────────────┤
│ 1. Compound Ergonomics │ 2. Design Tokens        │ 3. Vector Visual Fidelity     │
│ • Compound parts        │ • 50..950 color ramps   │ • G2 smooth superellipses    │
│ • Variants & size matrix│ • 4pt spacing scale     │ • Frosted glass backdrop blur│
│ • Micro-interactions    │ • Elevation shadows 0..5│ • Inner & drop shadows       │
│ • Accessible focus ring │ • Auto-Layout Engine    │ • Linear/radial gradients    │
│ • Portal light-dismiss  │   (hug, fill, fixed)    │ • Spatial transform handles  │
├─────────────────────────┴─────────────────────────┴──────────────────────────────┤
│ 4. Game-Dev Bare-Metal Speed & HUD Primitives (Crushing Dear ImGui / raylib)    │
│ • 120Hz/240Hz zero-GC retained tree — zero steady-state heap allocations        │
│ • No Double-Render Law: Vulkan 3D swapchain stamped under Retina IOSurface UI   │
│ • MMORPG HudBar: primary fill + delayed ghost lag drain + critical damage flash │
│ • CooldownButton: 360° radial sweep clock + hotkey badge + ready flash         │
│ • DamageNumbers: high-throughput pooled floating combat text with crit bounce   │
│ • InventoryGrid: drag-and-drop slots, stack counts, tier glow, slot locks       │
│ • NodeEditor: retained graph canvas with cubic bezier wires and pin sockets    │
│ • Gamepad Navigation: spatial D-pad focus engine, bumper tabs, glyph prompts    │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## Status Legend & Grading Standards

Every element and individual sub-feature is strictly graded based on the current reality of the codebase, test suites, and live runtime behavior (accounting for defect reports in `_bugs/`):

| Emoji | Level | Definition |
|:---:|:---|:---|
| 💚 | **98% Done** | Basically 98% done: fully wired, compiles, runs, production-ready, actively polished |
| 🟩 | **95% Done** | Implemented & functional: wired, compiles and runs, minor polish remaining |
| 🟨 | **85% Done** | Substantially implemented: core works or has tests proving behavior, missing specific features/edge cases/painters |
| 🟧 | **75% Done** | Partial implementation: core struct/concept exists, but major features missing or unwired in live harness |
| 🟥 | **Concept / Draft** | Still a concept or spec'd in docs/headers only, zero working source |
| ⬜ | **Vital Future Work** | Not implemented yet, but vital roadmap feature (+1 on the feature) |

---

## High-Level Component Summary

| # | Element / Component | Category | Scope Summary | Overall Status |
|:---:|:---|:---|:---|:---:|
| 1 | `Container` | Base Substrate | Layout truth: 9-grid anchors, pivot, margin, radius, auto-layout hug/fill/fixed | 🟩 |
| 2 | `Panel` | Base Substrate | Base visual tree node: solid fill, render handler, child tree, gradients, blur | 🟩 |
| 3 | `Canvas` | Base Substrate | Root layout surface, dirty-node fanning, multi-pass layout, DPI scaling | 🟩 |
| 4 | `Scene` / `Scene2D` / `Scene3D` | Base Substrate | COMPOSITED retained offscreen VkLayer flight target (no per-scene Metal surface; seam canvas is the single on-screen layer), pixel/percent modes, decoupled thread sync | 🟨 |
| 5 | `Compositor` | Base Substrate | Multi-IOSurface front-to-back zero-double-render layer compositor; 3-slot batch ring (non-blocking claim, drift-defer, 100ms bounded drain); proof `_tests/darling/compositor_batch_test` | 🟩 |
| 6 | `Label` | Text & Typography | Subpixel CoreText text rendering, selection drag, underline, copy | 🟨 |
| 7 | `Button` | Buttons & Choice | Pressable button shell, variants/sizes, compound slots, hover/pressed styling | 🟧 |
| 8 | `Switch` | Buttons & Choice | Boolean toggle; needs built-in track/thumb painter & smooth sliding animation | 🟧 |
| 9 | `Checkbox` | Buttons & Choice | Check toggle + indeterminate; needs built-in checkmark & dash painter | 🟧 |
| 10 | `RadioGroup` | Buttons & Choice | Exclusive option list; needs built-in radio painter & keyboard arrow navigation | 🟨 |
| 11 | `Slider` | Fields & Inputs | Range drag + snap; needs built-in track/thumb painter & tooltip readout | 🟧 |
| 12 | `Knob` | Fields & Inputs | Rotary atan2f drag; dial painter exists, pointer routing unwired in gallery | 🟧 |
| 13 | `ScrollBar` | Fields & Inputs | Fractional scroll drag; monolithic struct, needs two-panel composition | 🟧 |
| 14 | `Input` | Fields & Inputs | Single-line buffer; lacks built-in caret/text painter, key dispatch unwired | 🟧 |
| 15 | `Textarea` | Fields & Inputs | Multiline buffer; lacks multiline text painter, key dispatch unwired | 🟧 |
| 16 | `ScrollContainer` | Containers | Viewport clipping, trackpad scroll; needs horizontal bar & pick offset fix | 🟨 |
| 17 | `Anim` | Platform Core | Property animation player with easing curves and tick loop | 🟩 |
| 18 | `Cursor` | Platform Core | Predefined singletons + native Cocoa NSCursor apply | 🟩 |
| 19 | `Window` (Darling bridge) | Platform Core | Panel bridge to hotcwap window, needs window-scoped routing | 🟨 |
| 20 | `ListContainer` | Containers | Indexed vertical/horizontal linear stack layout with gap spacing | 🟩 |
| 21 | `GridContainer` | Containers | Row × column 2D grid with cell gaps and placement | 🟩 |
| 22 | `SectionContainer` | Containers | Titled header + collapsible body panel with animated height | 🟨 |
| 23 | `LayeredContainer` | Containers | Z-stacked overlapping panels with depth ordering and hit filtering | 🟩 |
| 24 | `SplitContainer` | Containers | Two-pane split container; divider drag interaction pending | 🟨 |
| 25 | `MarkdownPanel` | Text & Typography | Markdown parser → stacked Label/RichLabel rows + text selection | 🟩 |
| 26 | `RichTextPanel` | Text & Typography | Rich formatted text panel with styled runs | 🟩 |
| 27 | `RichLabel` | Text & Typography | Multi-run styled text + drag selection + tag-stripped copy | 🟩 |
| 28 | `Kbd` | Text & Typography | Keycap badge rendering with border and monospaced font | 🟩 |
| 29 | `Typography` | Text & Typography | Type scale roles mapped to fonts, weights, and sizes | 🟩 |
| 30 | `Picture` | Media & Graphics | Texture backing + UV crop + aspect fit/fill modes | 🟨 |
| 31 | `Event dispatch` | Event Subsystem | Event routing core; needs robust coordinate translation | 🟨 |
| 32 | `Event bridge` | Event Subsystem | Bridge mapping hotcwap events to darling handlers | 🟨 |
| 33 | `Pointer events` | Event Subsystem | Enter/hover/leave/down/up/drag dispatch pipeline | 🟨 |
| 34 | `Key events` | Event Subsystem | Key event handling; gallery loop lacks Key_dispatchEvents call | 🟧 |
| 35 | `Focus events` | Event Subsystem | Focus enter/leave & keyboard navigation traversal | 🟧 |
| 36 | `Gesture events` | Event Subsystem | Gesture recognition (pinch, pan, trackpad scroll) | 🟨 |
| 37 | `Action events` | Event Subsystem | Abstract command action dispatch pipeline | 🟨 |
| 38 | `Value events` | Event Subsystem | Generic value change notification channels | 🟩 |
| 39 | `Tree events` | Event Subsystem | Hierarchy mutation notifications (attach/detach/dirty) | 🟩 |
| 40 | `c23/add` | Language Binding | Unified Darling_add() _Generic compile-time dispatcher | 🟩 |
| 41 | `darling-type.h` | Language Binding | Darling class ID registry bridging vexspoke oop/type | 🟩 |
| 42 | `Font bake` | Platform Bridge | CoreText + SDF font atlas baking via graphvex | 🟩 |
| 43 | `IO mmap` | Platform Bridge | memory-mapped asset and font I/O | 🟩 |
| 44 | `IO bake` | Platform Bridge | Binary font package serialization | 🟩 |
| 45 | `Render raster` | Render Subsystem | CPU software rasterizer for off-screen quads and runs | 🟩 |
| 46 | `Render surface` | Render Subsystem | Raster surface allocation and pixel buffer management | 🟩 |
| 47 | `Text core` | Platform Bridge | Rich text styled-run model and layout metrics | 🟩 |
| 48 | `Panel Cocoa bridge` | Platform Bridge | ObjC board ↔ C panel retained offscreen VkLayer bridge (boards-only; no per-pane Metal layers) | 🟩 |
| 49 | `Text core ObjC` | Platform Bridge | Native Apple CoreText rasterization bridge | 🟩 |
| 50 | `DatePicker` | Fields & Inputs | Calendar date storage; missing month grid painter & popup | 🟧 |
| 51 | `FileDialog` | Overlays & Dialogs | Directory navigation & filter logic; GUI list painter missing | 🟧 |
| 52 | `Plot` | Media & Data | Line/Bar/Scatter data chart; autorange/hitPick stubs only | 🟨 |
| 53 | `Select` | Fields & Inputs | Dropdown list storage; popup menu blocked by OverlayRoot | 🟧 |
| 54 | `InputOTP` | Fields & Inputs | Passcode digit advance logic and visual box painter | 🟩 |
| 55 | `ColorPicker` | Fields & Inputs | HSV math stubs; missing interactive spectrum painter | 🟧 |
| 56 | `ColorSwatch` | Fields & Inputs | Color chip container; onSelect unwired, painter missing | 🟧 |
| 57 | `MaterialPanel` | Media & Graphics | Header-only, awaits graphvex lit material shader path | 🟧 |
| 58 | `VideoPanel` | Media & Graphics | Header-only, awaits VFS media decoder | 🟧 |
| 59 | `Object3D` | Media & Graphics | Header-only, awaits graphvex Mesh GPU draw pipeline | 🟧 |
| 60 | `Viewer3D` | Media & Graphics | Header-only, awaits Object3D + orbit camera controls | 🟧 |
| 61 | `Frame` | Overlays & Windows | Host frame gluing Window (R1) & Graphics (R3), CAMetalLayer presentsWithTransaction=YES, FBO stacking; composable present-callback slots (`Frame_addFrameFunction`, dt per render) + KeyMap input bindings (`Frame_addKeyFunction`/`Frame_addMouseFunction`, resolved per render) | 🟩 |
| 62 | `Dialog` | Overlays & Dialogs | Modal frame inheriting Frame, base for dialog family; modal/clinging enforced (OS key gate + pair glue + bridge capture via `Dialog_show(dialog, frame)`, red-close routed through `Dialog_requestClose`, held dialogs not minimizable) | 🟩 |
| 63 | `OptionDialog` | Overlays & Dialogs | Modal option selection dialog (OK, Cancel, Yes, No, Retry) inheriting Dialog | 🟩 |
| 64 | `InputDialog` | Overlays & Dialogs | Modal single-line text input prompt inheriting Dialog | 🟩 |
| 65 | `Color` | Base Substrate | Format-independent Color class (RGBA, ARGB32, RGBA32, HSV, HSL, Hex) | 🟩 |
| 66 | `ColorDialog` | Overlays & Dialogs | Modal color picker dialog inheriting Dialog with live color updates | 🟩 |
| 67 | `AlertDialog` | Overlays & Dialogs | Title/message/action buttons; blocked by OverlayRoot | 🟧 |
| 68 | `OverlayRoot` | Overlays & Dialogs | Top-level layer escaping child clips for popups/modals | 🟥 |
| 69 | `Theme System` | Polish & Styling | Token table (50..950), light/dark ramps, WCAG contrast auditing | 🟥 |
| 70 | `FocusRing` | Polish & Styling | Accessible keyboard Tab focus indicator with custom offset/color | 🟥 |
| 71 | `Toast` / `ToastStack` | Overlays & Dialogs | Non-modal notification banner queue with auto-dismiss | 🟥 |
| 72 | `Tooltip` | Overlays & Dialogs | Hover hint bubble with directional arrow escaping clips | 🟥 |
| 73 | `Popover` | Overlays & Dialogs | Click-anchored floating card with light dismiss | 🟥 |
| 74 | `Menu` / `ContextMenu` | Overlays & Dialogs | Hierarchical dropdown & right-click context menu | 🟥 |
| 75 | `FlexPanel` | Containers | Auto-layout flow (row/col, wrap, gap, hug/fill/fixed) | 🟥 |
| 76 | `SplitPanel` | Containers | Two-pane container with draggable divider bar | 🟥 |
| 77 | `TabPanel` | Containers | Tabbed interface with top/side strip and page stack | 🟥 |
| 78 | `DockPanel` | Containers | IDE-style multi-dock workspace with splitters | 🟥 |
| 79 | `CardPanel` | Containers | Structured card with header/body/footer and elevation | 🟥 |
| 80 | `ProgressBar` | Polish & Feedback | Determinate progress fill + indeterminate sweep | 🟥 |
| 81 | `Spinner` | Polish & Feedback | Circular rotating loading indicator arc | 🟥 |
| 78 | `Skeleton` | Polish & Feedback | Shimmer placeholder shapes for loading states | 🟥 |
| 79 | `Avatar` | SaaS & App Kit | Photo / initials badge with online status dot | 🟥 |
| 80 | `Badge` / `Pill` | SaaS & App Kit | Status tag with tone variants (success/warn/danger/info) | 🟥 |
| 81 | `Chip` | SaaS & App Kit | Interactive tag token with dismiss icon and avatar slot | 🟥 |
| 82 | `SearchField` | SaaS & App Kit | Input with search icon, clear button, and shortcut badge | 🟩 |
| 83 | `Breadcrumb` | SaaS & App Kit | Hierarchical path navigation trail with separators | 🟥 |
| 84 | `Pagination` | SaaS & App Kit | Page navigator with page numbers and prev/next buttons | 🟥 |
| 85 | `Accordion` | Containers | Expandable/collapsible disclosure groups with animated height | 🟥 |
| 86 | `TreePanel` | Containers | Hierarchical expandable tree view for file/scene graphs | 🟥 |
| 87 | `TablePanel` / `DataTable` | SaaS & App Kit | Multi-column data grid with sorting, resize, and pagination | 🟥 |
| 88 | `CommandPalette` | SaaS & App Kit | Quick-open modal (Cmd+K) with fuzzy action filtering | 🟥 |
| 89 | `StatCard` | SaaS & App Kit | KPI metric card with sparkline chart and trend pill | 🟥 |
| 90 | `WebPanel` | Media & Graphics | Native Web View bridge without Chromium bloat (WKWebView) | 🟥 |
| 91 | `CodeField` | Text & Typography | Rich code editor: syntax runs, line numbers, gutter, fold | 🟩 |
| 92 | `Clipboard` | Platform Bridge | Native OS pasteboard bridge for text, images, and MIME | 🟩 |
| 93 | `History` | Platform Core | Universal undo/redo command stack with branching timeline | 🟥 |
| 94 | `IconImage` | Media & Graphics | Vector/SDF icon widget binding to Lucide/Tabler icon sets | 🟥 |
| 95 | `SvgPanel` | Media & Graphics | Scalable Vector Graphics renderer via bezier strokes & SDF | 🟥 |
| 96 | `HtmlExporter` | Platform Core | Tree-to-HTML serializer transpiling layouts to web code | 🟥 |
| 97 | `HudBar` | Game Dev Kit | MMORPG health/mana bar: ghost lag drain + crit flash + pulse | 🟥 |
| 98 | `CooldownButton` | Game Dev Kit | 360° radial sweep clock + keybind badge + cooldown timer | 🟥 |
| 99 | `DamageNumbers` | Game Dev Kit | High-throughput pooled floating combat text with crit bounce | 🟥 |
| 100 | `InventoryGrid` | Game Dev Kit | Item slot grid: drag-and-drop, stack counts, rarity glow borders | 🟥 |
| 101 | `DialogBox` | Game Dev Kit | NPC dialogue: typewriter text stream + portrait + choice buttons | 🟥 |
| 102 | `Minimap` | Game Dev Kit | Radar/map: player frustum cone + pings + fog of war mask | 🟥 |
| 103 | `NodeEditor` | Game Dev Kit | Visual graph: blueprint nodes, input/output pins, bezier wires | 🟥 |
| 104 | `GamepadNav` | Game Dev Kit | Spatial D-pad focus engine, bumper tab cycling, button prompts | 🟥 |
| 105 | `SpatialCanvas` | Spatial Studio | Infinite 120Hz pan/zoom canvas, smart guides, mini-map navigator | 🟥 |
| 106 | `TransformBox` | Spatial Studio | 8-point bounding transform handles, rotation pin, aspect lock | 🟥 |
| 107 | `PropertyInspector` | Spatial Studio | Two-way property inspector: geometry, fills, strokes, type | 🟥 |

---

## Detailed Feature Breakdowns

### 1. Base Substrate (`Container`, `Panel`, `Canvas`, `Scene`, `Compositor`)

#### 1.1 Container
Layout source of truth. Every widget embeds `Container` as its first member (`&(*node).base` upgrades directly to layout).

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| 9-Grid Parent Anchoring | `ANCHOR_NW`, `N`, `NE`, `W`, `CENTER`, `E`, `SW`, `S`, `SE` pin layout to parent rect | 🟩 |
| 4-Corner Self Anchoring / Pivot | Normalized pivot offset coordinates `(pivotX, pivotY)` | 🟩 |
| Coordinate & Bounds Resolution | `Container_resolve()` calculates final screen rect without state stomping | 🟩 |
| Additive Margin System | Additive margin law: `final = location + margin`, separate from anchor position | 🟩 |
| Inner Padding Subsystem | Dedicated container-internal padding offsets distinct from children's margin | 🟧 |
| Corner Radius Modes | Arc mode (`CORNER_ARC`) vs smooth superellipse squircle (`CORNER_SUPERELLIPSE`) | 🟨 |
| Clip-to-Bounds Enclosure | Strict bounding clip flag preventing child overflows | 🟩 |
| Min / Max Dimension Clamping | `minW`, `maxW`, `minH`, `maxH` layout constraint enforcement | 🟩 |
| Percentage Dimension Modes | Sizing defined as parent-relative percentage (`w%`, `h%`) | 🟩 |
| Container Sizing Modes | `SIZING_FIXED`, `SIZING_HUG_CONTENTS`, `SIZING_FILL_CONTAINER` | 🟥 |
| Dirty-Flag Tree Propagation | Invalidation cascade walking upward to parent surface | 🟩 |
| Bounded Hit-Testing | `Container_hitTest()` checking coordinate bounds and visibility flag | 🟩 |
| Affine Transform & Scale | Scale and 2D rotation matrix transformations | 🟨 |

#### 1.2 Panel
Base visual tree node embedding `Container`. Owns background color, custom render handlers, and child hierarchy.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Solid Background Fill | Direct solid color quad rendering (`Panel_setBackgroundColor`) | 🟩 |
| Border Styling | Border width, border color, and corner radius properties | 🟨 |
| Custom Render Handler Slot | `Panel_setRenderHandler(p, fn)` registering draw callbacks for Vulkan/Raster | 💚 |
| Detach-Only Tree Hierarchy | `add`/`insert` attach child, `remove` detaches without freeing memory | 🟩 |
| Structural Subtree Cloning | Deep-copy of layout structure with aliased payload pointers | 🟩 |
| Texture / Image Backing Slot | Image handle slot for texture binding | 🟨 |
| Multi-Stop Gradients | Linear and radial multi-stop color gradients (`Panel_setLinearGradient`) | 🟥 |
| Drop Shadows (Offset, Blur, Spread) | Outer drop shadow with X/Y offset, blur radius, spread, and color | 🟥 |
| Inner Shadows | Inset shadow for wells, depressed buttons, and form inputs | 🟥 |
| Frosted Glass / Backdrop Blur | Backdrop blur shader filter pass behind panel rect (glassmorphism) | 🟥 |

#### 1.3 Canvas
Root layout surface managing passes and display surfaces.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Root Layout Surface | Master surface bounding the UI hierarchy | 🟩 |
| Dirty-Node Fanning | Traversal pass resolving only dirty subtrees | 🟩 |
| Frame Presentation Scheduling | Decoupled render/present pass coordination | 🟨 |
| Multi-Window Canvas Decoupling | Independent canvas instances per OS window | 🟨 |
| Retina / DPI Dynamic Adaptation | Backing scale factor propagation across elements | 🟩 |

#### 1.4 Scene / Scene2D / Scene3D
Vulkan swapchain stamp surface embedding 3D/2D views into the UI layer.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Vulkan Swapchain Stamping | Zero-copy blit stamp into presentation swapchain | 🟨 |
| Pixel vs Percentage Sizing | Responsive sizing modes for 3D viewports | 🟩 |
| Multithreaded Render Sync | Decoupled background render thread with foreground UI compositor | 🟨 |
| MSAA / HDR Presentation Modes | Multi-sample anti-aliasing and wide-gamut swapchain support | 🟥 |

#### 1.5 Compositor
Multi-layer front-to-back hardware compositor.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Multi-IOSurface Front-to-Back Blit | Hardware-accelerated zero-copy compositing | 🟩 |
| Batch Ring (3 slots) | Non-blocking slot claim, skip-and-retry on saturation, unsettled drift-defer, per-slot 100ms bounded wait + shutdown drain | 🟩 |
| Resize Gate + Introspection | `Darling_compositorIdleForResize` resize gate, `BatchDepth/Capacity` counters; proof `_tests/darling/compositor_batch_test` | 🟩 |
| No Double-Render Law | Skips non-scene UI quads in Vulkan pass; leaves overlays to WindowServer | 🟩 |
| Subpixel Quad Retina Alignment | Integer pixel snapping to avoid subpixel blur | 🟩 |
| Linux / Wayland Compositor Backend | Cross-platform compositor bridge for non-macOS platforms | 🟥 |

---

### 2. Text & Typography (`Label`, `RichLabel`, `MarkdownPanel`, `RichTextPanel`, `Typography`, `Kbd`, `CodeField`)

#### 2.1 Label
Single-styled text rendering node.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| String Storage & Ownership | Owned (`Label_setText`) and borrowed (`Label_setTextBorrowed`) string buffers | 💚 |
| CoreText Subpixel Rasterization | Line-by-line sharp Apple CoreText raster quad caching | 🟩 |
| SDF Font Atlas Fallback Path | Scale-invariant signed distance field atlas rendering for outline/glow | 🟨 |
| Text & Background Colors | Packed 32-bit ARGB color configuration | 💚 |
| Font Family & Size Control | Dynamic font family resolution and point size adjustment | 💚 |
| Glyph Pen Offset Table | Exact per-glyph point offsets (`glyphX`, `glyphN`) from CoreText shaper | 🟩 |
| Accurate Hit-Testing | `Label_charIndexAt()` shares the stated `glyphX` table with paint (midpoint boundaries, continuation rewind); uniform `roundf` fallback without a table | 🟩 |
| Selection Highlight Drag | Fixed-anchor drag selection via shared `TextSelect` part; active edge tracking | 🟩 |
| Rounded Selection Highlight Box | Rounded rectangle highlight rendering (`highlightRadius`, `highlightColor`) | 🟩 |
| Underline Styling | `UNDERLINE_BASIC` style rendering via CoreText styled runs | 🟩 |
| Custom Underline Color | Independent underline color (`Label_setUnderlineColor`) | 🟩 |
| Mnemonic Accelerator Parsing | Parses `&` prefix, underlines accelerator char, records mnemonic index; selection span mapped into clean coordinates for paint | 🟩 |
| Hover Cursor Switching | Automatic I-beam cursor on hover when highlightable, default on exit | 🟩 |
| Clipboard Copy | Cmd/Ctrl+C keyboard handler copying selected text via TextCore seam | 🟩 |
| Strikethrough Styling | Strikethrough line rendering across glyph metrics | ⬜ |
| Multiline Text Wrapping | Word-wrapping and multiline layout inside standard Label | 🟧 |
| Ellipsis Truncation | Trailing ellipsis (`...`) clipping on bounded overflow | 🟨 |
| Text Alignment Modes | Explicit Left, Center, Right, and Justified alignment flags | 🟨 |
| Font Fallback Cascade | Automatic fallback font resolution when glyphs are missing | 🟨 |

#### 2.2 RichLabel & RichTextPanel
Multi-run styled text nodes for mixed formatting.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Multi-Run Styled Text Chunks | Runs with distinct font, size, weight, and color in one flow | 🟩 |
| Markup / Tag Decoder | Parsing inline tags for bold, italic, underline, and color | 🟨 |
| Drag Selection Across Runs | Contiguous selection highlighting across multiple styled spans | 🟩 |
| Tag-Stripped Clipboard Copy | Cmd+C copies plain text content stripping formatting tags | 🟩 |
| Embedded Inline Widgets | Inline badges, icons, and interactive links embedded in text flow | ⬜ |

#### 2.3 MarkdownPanel
CommonMark / Markdown layout panel converting markdown to UI elements.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Block Parsing | Headers (`#`–`######`), blockquotes, paragraphs, and list items | 🟩 |
| Inline Formatting | Bold (`**`), italic (`*`), strikethrough (`~~`), inline code (`` ` ``) | 🟩 |
| Stacked Element Layout | Generated rows of Label / RichLabel containers inside ListPanel | 🟩 |
| Document-Wide Selection Drag | Selection across multiple paragraph blocks via shared TextSelect | 🟩 |
| Code Block Syntax Highlighting | Fenced code blocks with language grammar token coloring | 🟧 |
| Markdown Tables | GFM-compliant markdown table parsing and grid rendering | ⬜ |
| Embedded Links & Images | Clickable markdown links and inline image rendering | 🟨 |

#### 2.4 Kbd
Keycap badge chip for keyboard shortcuts.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Visual Keycap Badge | Distinct background well, rounded border, and inset padding | 🟩 |
| Monospaced Typography | Monospace font styling for key symbols | 🟩 |
| Key Symbol Parsing | Automatic rendering of symbols (`⌘`, `⌥`, `⇧`, `⌃`, `↵`) | 🟨 |

#### 2.5 Typography
Design system type scale tokens.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Type Scale Roles | `TEXT_CAPTION`, `TEXT_BODY`, `TEXT_TITLE`, `TEXT_DISPLAY`, `TEXT_MONO` | 🟩 |
| Theme Token Binding | Automatic role mapping to font family, size, weight, and tracking | 🟨 |

#### 2.6 CodeField
Advanced code editor widget.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Monospace Syntax Surface | Monospace font surface with tab stop and line formatting | 🟩 |
| Line Number Gutter | Left-anchored gutter showing line numbers and active line marker | 🟩 |
| Code Folding Rails | Collapsible code blocks with fold/unfold arrows | 🟥 |
| Multi-Caret Editing | Multiple cursor placement and synchronized typing | 🟥 |

---

### 3. Buttons & Choice Primitives (`Button`, `Switch`, `Checkbox`, `RadioGroup`)

#### 3.1 Button
Pressable button shell. Embraces clean compound composition and immediate tactile feedback.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Label Storage & Font Config | Text buffer, font, fontSize, and textColor setters/getters | 🟩 |
| Press Callback Dispatch | `onPress(ctx)` callback executed on click-on-release inside bounds | 🟩 |
| Pointer State Tracking | Updates `hovered` and `pressed` flags on enter/leave/down/up | 🟩 |
| Live Hover State Styling | Automatic color transition on hover (BUG-002: no default state painter) | 🟧 |
| Live Pressed State Styling | Darkening / inset visual feedback on active press | 🟧 |
| Built-in Text Rendering | Native text painter inside button (gallery currently requires manual Label child) | 🟧 |
| Component Variant Matrix | `BUTTON_DEFAULT`, `BUTTON_SECONDARY`, `BUTTON_DESTRUCTIVE`, `BUTTON_OUTLINE`, `BUTTON_GHOST`, `BUTTON_LINK` | 🟥 |
| Component Size Scale | `BUTTON_SIZE_SM`, `BUTTON_SIZE_MD`, `BUTTON_SIZE_LG`, `BUTTON_SIZE_ICON` | 🟥 |
| Prefix Icon Slot | Leading icon slot automatically positioned and aligned | 🟧 |
| Suffix Accessory Slot | Trailing badge, shortcut `<kbd>`, or dropdown arrow slot | 🟧 |
| Loading Spinner State | Built-in loading spinner replacing/accompanying label, disables clicks | ⬜ |
| Keyboard Focus Ring & Activation | Focus indicator ring; Enter and Space bar triggers | 🟥 |

#### 3.2 Switch
Compact on/off boolean toggle.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Boolean Toggle State | `setOn()`, `isOn()`, pointer click toggle | 🟩 |
| Value Change Callback | `onChange(bool val, void *ctx)` dispatch | 🟩 |
| Built-in Track & Thumb Painter | Visual pill track + circle thumb (BUG-012: gallery lacked painter, renders invisible quad) | 🟧 |
| Smooth Animated Sliding | Thumb transition easing between ON and OFF positions | 🟧 |
| Hover & Pressed Visual States | Track highlight and thumb scale feedback | 🟧 |
| Disabled State Styling | Desaturated track and non-interactive thumb | 🟨 |
| Keyboard Space Activation | Toggle via Space key when focused | 🟥 |

#### 3.3 Checkbox
Square checkbox with checkmark and indeterminate state.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Checked State Toggle | `setChecked()`, `isChecked()`, click toggle | 🟩 |
| Indeterminate State | Tri-state flag (`indeterminate`), clears on user toggle | 🟨 |
| Change Callback | `onChange(bool checked, void *ctx)` dispatch | 🟩 |
| Built-in Box & Check Painter | Visual rounded square + vector checkmark (BUG-012: needs built-in painter) | 🟧 |
| Indeterminate Dash Painter | Centered horizontal dash for indeterminate selection | 🟧 |
| Clickable Label Row Binding | Unified hit-testing where clicking accompanying label toggles checkbox | 🟨 |
| Keyboard Space Activation | Space key toggle when focused | 🟥 |

#### 3.4 RadioGroup
Mutually exclusive single-choice option group.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Option List Management | Add option, clear options, get option count | 🟩 |
| Mutual Exclusion Tracking | Strict single selected index enforcement | 🟩 |
| Selection Callback | `onSelect(int index, void *ctx)` dispatch | 🟩 |
| Built-in Radio Painter | Outer ring + centered active filled dot painter | 🟧 |
| Pointer Hit-Testing | Per-row hit testing and selection highlight | 🟨 |
| Keyboard Arrow Navigation | Up/Down arrow keys cycling through options | 🟥 |
| Individual Disabled Options | Selectively disabling specific options in list | 🟨 |

---

### 4. Fields & Inputs (`Input`, `Textarea`, `Slider`, `Knob`, `ScrollBar`, `Select`, `DatePicker`, `ColorPicker`, `ColorSwatch`, `InputOTP`)

#### 4.1 Input
Single-line editable text field.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Bounded Text Buffer | memory-allocated character buffer with capacity bounds | 🟩 |
| Placeholder Text | Dimmed placeholder text when buffer is empty | 🟨 |
| Password Masking Mode | Masks characters with bullet symbols (`•` or `*`) | 🟨 |
| Focus / Blur Lifecycle | Focus entry/exit state tracking and visual borders | 🟨 |
| Key Typing Input Delivery | Typing characters into buffer (BUG-005, BUG-010: missing key dispatch loop) | 🟧 |
| Backspace & Delete Handling | Backward and forward character deletion | 🟨 |
| Caret Movement & Arrow Keys | Left, Right, Home, End caret navigation | 🟨 |
| Caret Blink & Rendering | Blinking vertical caret bar (BUG-013: no text/caret painter in gallery) | 🟧 |
| Built-in Text / Glyph Painter | Subpixel font rendering for buffer text (BUG-013) | 🟧 |
| Text Selection Within Field | Mouse drag & Shift+arrow text selection highlighting | 🟧 |
| Clipboard Cut / Copy / Paste | Cmd+X, Cmd+C, Cmd+V OS pasteboard integration | 🟨 |
| Callbacks | `onChange` on keystroke, `onSubmit` on Enter key | 🟩 |
| Prefix & Suffix Icon Slots | Leading icon (magnifier) and trailing action button (clear `×` or password eye) | ⬜ |
| Floating Label Animation | Smooth floating label transition on focus | ⬜ |
| Validation Error State | Red outline + helper error message text slot | 🟥 |

#### 4.2 Textarea
Multiline editable text area.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Multiline Buffer Management | Text buffer handling newline (`\n`) characters | 🟨 |
| Line Wrapping & Layout | Soft wrapping text at container edge | 🟨 |
| Multiline Cursor Navigation | Up, Down, Left, Right, Home, End, PageUp, PageDown | 🟧 |
| Multiline Text & Caret Painter | Visual rendering of multiline text lines and blinking cursor (BUG-013) | 🟧 |
| Multiline Text Selection | Drag selection across multiple lines | 🟧 |
| Viewport Scrolling Sync | Automatic scrolling to keep active cursor visible | 🟨 |
| Line Numbers & Gutter | Left-hand line numbering rail | ⬜ |

#### 4.3 Slider
Linear range drag slider.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Range & Value Normalization | Min, max, normalized 0.0..1.0 value mapping | 🟩 |
| Pointer Drag Interaction | Click and drag thumb tracking pointer position | 🟩 |
| Step Snapping | Snapping values to discrete step increments | 🟩 |
| Value Change Callback | `onChange(float val, void *ctx)` dispatch | 🟩 |
| Built-in Track & Fill Painter | Track background + filled progress bar (BUG-014: gallery had no painter) | 🟧 |
| Built-in Thumb Knob Painter | Draggable thumb handle with hover/pressed states (BUG-014) | 🟧 |
| Horizontal vs Vertical Modes | Horizontal track vs vertical track orientation | 🟨 |
| Keyboard Nudging | Left/Right/Up/Down arrow key adjustments | 🟥 |
| Floating Value Readout Tooltip | Bubble displaying current numeric value while dragging | ⬜ |

#### 4.4 Knob
Rotary dial controller.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Rotary Angle Drag Math | `atan2f(dy, dx)` rotary calculation with 270° sweep | 🟩 |
| Value Range & Normalization | 0.0..1.0 value mapping and clamping | 🟩 |
| Value Change Callback | `onChange(float val, void *ctx)` dispatch | 🟩 |
| Built-in Dial & Tick Painter | Circular body + inner groove + indicator tick painter (implemented in gallery) | 🟨 |
| Pointer Event Delivery | Interactive drag in live window (BUG-001, BUG-003: pointer events unrouted) | 🟧 |
| Detent Snapping | Tactile angle detents and snapping intervals | 🟨 |
| Shift+Drag Fine Control | Precision dragging mode with reduced rotational sensitivity | ⬜ |
| Numeric Value Readout Label | Centered or bottom text display of current value | 🟨 |

#### 4.5 ScrollBar
Scrollbar track and thumb.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Scroll Value Clamping | Fractional position clamping (0.0..1.0) | 🟩 |
| Thumb Sizing from Ratio | Thumb size calculated from viewport/content ratio | 🟨 |
| Thumb Drag Pointer Handling | Dragging thumb updates scroll offset | 🟩 |
| Track Click-to-Seek | Clicking track jumps to fraction | 🟩 |
| Persistent Point Mode | Constant visible thumb (`SCROLL_BAR_POINT`; BUG-006) | 🟨 |
| Auto-Fading Gesture Mode | Trackpad auto-fading thumb (`SCROLL_BAR_GESTURE`; BUG-006) | 🟧 |
| Two-Panel Composition | Separation into track panel + child thumb panel (BUG-015: currently monolithic) | 🟧 |
| Horizontal ScrollBar | Horizontal track and thumb support (BUG-008) | 🟧 |
| Two-Way Range Bar | Dual handles for range selection (`ValueBar`; BUG-007) | 🟥 |

#### 4.6 Select (Dropdown / Combobox)
Compound dropdown selection field with keyboard navigation.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Selected Item Display | Collapsed trigger button displaying current selection | 🟨 |
| Item Storage & Indexing | Item string list, add/remove/clear methods | 🟨 |
| Compound Part Architecture | `Select_trigger`, `Select_value`, `Select_content`, `Select_item`, `Select_group`, `Select_separator` | 🟥 |
| Dropdown Menu Popup | Escaping container clip via OverlayRoot (BUG-004) | 🟧 |
| Search Filter Combobox | Built-in search input inside open popup | 🟥 |
| Keyboard Selection | Up/Down arrow selection with Enter to confirm | 🟥 |

#### 4.7 DatePicker
Calendar date selection widget.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Date Storage & Math | Year, month, day setters and `setToday` helpers | 🟨 |
| Month Grid Painter | Calendar month grid visual rendering | 🟧 |
| Month Navigation Controls | Prev/next month arrow buttons | 🟧 |
| Date Popup Overlay | Floating popup dialog (awaits OverlayRoot) | 🟥 |

#### 4.8 ColorPicker & ColorSwatch
Color selection components.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Color Storage & Hex / HSV Math | Packed 0xAARRGGBB storage, HSV conversion stubs | 🟨 |
| Color Swatch Chip | Visual chip displaying color (`ColorSwatch`) | 🟨 |
| Swatch Selection Callback | `onSelect` callback on swatch click | 🟧 |
| Hue Spectrum Canvas Painter | 2D saturation/value box + 1D hue ring/slider painter | 🟧 |
| Interactive Color Drag | Dragging crosshair across color spectrum | 🟧 |
| Eyedropper Screen Sampler | Magnified pixel sampler sampling screen colors | ⬜ |

#### 4.9 InputOTP
One-time passcode digit boxes.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Digit Storage Array | N-box digit storage (`setLength(6)`) | 🟩 |
| Auto-Advance on Keystroke | Automatically moving focus to next box on digit entry | 🟩 |
| Visual Box Array Painter | Distinct outlined boxes for each digit | 🟩 |
| Paste Auto-Split | Splitting 6-character pasted string across boxes | 🟩 |

---

### 5. Containers & Layout (`ListContainer`, `GridContainer`, `SectionContainer`, `LayeredContainer`, `SplitContainer`, `ScrollContainer`, `FlexPanel`, `TabPanel`, `DockPanel`, `CardPanel`, `TreePanel`, `TablePanel`)

#### 5.1 ListContainer / ListPanel
Linear indexed stack layout.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Vertical Stacking | Vertical ordering of child panels | 🟩 |
| Horizontal Stacking | Horizontal row ordering of child panels | 🟩 |
| Gap / Spacing Property | Spacing in points between adjacent elements | 🟩 |
| Add / Insert / Remove / Count | Full indexed child mutation API | 🟩 |
| Detach-Only memory Preservation | Removing children detaches without freeing memory | 🟩 |
| Cross-Axis Alignment | Align children to Start, Center, End, or Stretch | 🟨 |
| Dynamic Content Auto-Sizing | Expanding container bounds based on child bounds | 🟨 |

#### 5.2 GridContainer / GridPanel
2D tabular grid layout.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Row × Column Grid Geometry | Fixed rows and columns (`GridPanel_2(r, c)`) | 🟩 |
| Cell Panel Placement | `setCell(r, c, panel)` and `getCell(r, c)` | 🟩 |
| Cell Gap Properties | Independent horizontal and vertical gaps (`gapX`, `gapY`) | 🟩 |
| Cell Spanning | Colspan and rowspan across multiple grid cells | 🟧 |
| Auto-Flow Dynamic Cells | Dynamic row creation as children are added | ⬜ |

#### 5.3 SectionContainer / SectionPanel
Titled collapsibles.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Header + Content Layout | Header label panel + body panel structure | 🟩 |
| Collapsible Toggle | Expand and collapse body visibility | 🟨 |
| Animated Height Transition | Smooth easing transition on expand/collapse | 🟧 |

#### 5.4 LayeredContainer / LayeredPanel
Z-stacked overlapping containers.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Overlapping Child Placement | Overlapping siblings occupying identical or offset rects | 🟩 |
| Explicit Z-Index Ordering | Front-to-back sorting of child layers | 🟩 |
| Multi-Layer Hit-Testing | Hit-testing frontmost visible active child | 🟨 |

#### 5.5 SplitContainer / SplitPanel
Tiled split view container.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Pane Partitioning | Splitting area into two or N panes | 🟩 |
| Normalized Split Ratios | Fractional sizing (`setRatio(0.28f)`) | 🟩 |
| Interactive Draggable Divider | Draggable splitter bar resizing adjacent panes | 🟧 |
| Min / Max Pane Constraints | Clamping pane sizes to minimum and maximum thresholds | 🟨 |

#### 5.6 ScrollContainer / ScrollPanel
Scrollable viewport container.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Viewport Bounds & Clipping | Clips child contents to visible viewport rect | 🟩 |
| Vertical Scroll Offsets | Vertical offset tracking and boundary clamping | 🟩 |
| Trackpad & Wheel Scroll Routing | Mouse wheel and trackpad scroll event translation | 🟩 |
| Inertial Fling & Bounce Physics | Inertial deceleration and spring edge bounce | 🟨 |
| Horizontal Scrolling & Bar | Horizontal scrolling and bottom scrollbar (BUG-008: vertical only today) | 🟧 |
| Pick Offset Translation | Compensating hit-test pick coordinates by scroll offsets (BUG-009) | 🟧 |
| ScrollBar Auto-Synchronization | Updating scrollbar thumb position and scale dynamically | 🟨 |

#### 5.7 Advanced & Compound Containers

| Container | Scope & Capabilities | Status |
|:---|:---|:---:|
| `FlexPanel` | Auto-layout / CSS Flexbox: row/col, wrap, gap, justify, align, hug/fill/fixed | 🟥 |
| `TabPanel` | Top/side tab strip + stacked body panels, closable tabs, tab reordering | 🟥 |
| `DockPanel` | Multi-dock layout regions (Left/Right/Top/Bottom/Center) with docking splitters | 🟥 |
| `CardPanel` | Compound card layout: `Card_header`, `Card_title`, `Card_description`, `Card_content`, `Card_footer` | 🟥 |
| `TreePanel` | Indented hierarchical tree view for file trees and scene graphs with expand arrows | 🟥 |
| `TablePanel` / `DataTable` | Multi-column grid with column resize, sorting headers, row selection, pagination | 🟥 |
| `Accordion` | Mutually exclusive or multi-expand disclosure groups with animated heights | 🟥 |

---

### 6. Media, 3D & Graphics (`Picture`, `Plot`, `VideoPanel`, `MaterialPanel`, `Object3D`, `Viewer3D`, `IconImage`, `SvgPanel`, `WebPanel`)

#### 6.1 Picture
Off-heap image display node.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Texture Backing | GPU texture or memory bitmap backing | 🟩 |
| UV Crop Coordinates | Sub-rect texture cropping via normalized UV coordinates | 🟩 |
| Aspect Fit / Fill Scaling | `FIT_COVER`, `FIT_CONTAIN`, `FIT_STRETCH` aspect ratios | 🟨 |
| Asynchronous Image Decoding | Background thread decoding from VFS/disk | 🟥 |

#### 6.2 Plot
Data visualization chart widget.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Data Buffer Binding | Borrowed float array buffers for X and Y coordinates | 🟨 |
| Chart Modes | `PLOT_LINE`, `PLOT_BAR`, `PLOT_SCATTER` | 🟨 |
| Autorange Math | Automatic min/max bounding calculation | 🟨 |
| Grid Lines & Axes Drawing | Coordinate axes and background reference grid | 🟨 |
| Point Hit-Testing (`hitPick`) | Hover hit-test identifying nearest data point | 🟧 |
| Interactive Data Tooltip | Floating callout displaying point coordinates on hover | ⬜ |
| Donut / Sparkline / Heatmap Modes | Compact sparklines, donut distribution, and activity heatmaps | ⬜ |

#### 6.3 3D & Advanced Graphics Nodes
3D scene nodes bridging into graphvex and external media decoders.

| Node | Scope & Capabilities | Status |
|:---|:---|:---:|
| `MaterialPanel` | Lit material rendering surface, awaits graphvex pipeline | 🟧 |
| `VideoPanel` | Video playback surface, awaits VFS media decoder | 🟧 |
| `Object3D` | 3D mesh node with transform hierarchy, awaits graphvex Mesh GPU draw | 🟧 |
| `Viewer3D` | Interactive 3D scene viewer with orbit camera and lighting controls | 🟧 |
| `IconImage` | Vector/SDF icon widget binding to Lucide/Tabler icon sets | 🟥 |
| `SvgPanel` | Scalable Vector Graphics renderer via bezier curves and SDF atlas | 🟥 |
| `WebPanel` | Lightweight native Web View bridge (macOS WKWebView / WebKitGTK) | 🟥 |

---

### 7. Overlays, Windows & Dialogs (`OverlayRoot`, `Dialog`, `AlertDialog`, `FileDialog`, `ColorDialog`, `Window`, `Tooltip`, `Popover`, `Menu`, `Toast`)

#### 7.1 OverlayRoot & Modal Subsystem
Top-level full-window layer escaping child container clipping. Required for dropdowns, tooltips, and modals.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Unclipped Overlay Layer | Highest Z-index layer spanning full window above clipping boundaries | 🟥 |
| Modal Scrim & Dimming | Semi-transparent background barrier blocking input to layers beneath | 🟧 |
| Light-Dismiss Click Gate | Clicking outside active popup closes overlay | 🟥 |
| Focus Trap Management | Restricting keyboard Tab cycle within active modal dialog | 🟥 |

#### 7.2 Frame & Dialogs (WindowServer Aligned Architecture)
Host frames and modal dialogs gluing R1 (`hotcwap` `Window`) and R3 (`graphvex` GPU device context).
Window hierarchy on macOS: `NSWindow` -> `NSVisualEffectView` -> `CAMetalLayer` (`mtklayer`).
`mtklayer` is configured with `presentsWithTransaction = YES` to align atomically with the macOS `WindowServer` during live resize, minimize, and zoom events (bridged from `window_cocoa.m`).
Inside `mtklayer`, $X$ amount of `VkImage` / Framebuffer (FBO) layers stack on top of each other (Layer 0: Scene, Layer 1: Content/UI, Layer 2: Modals).
Frames and Dialogs bridge into the R1 host supervisor via `Frame_addFrameHandler(frame, app)` and `Dialog_addDialogHolder(dialog, app)` with `Dialog_open(dialog)`.

| Component | Scope & Capabilities | Status |
|:---|:---|:---:|
| `Frame` | Base host frame: `{ *window, *graphics, rootPanel, layers[8], layerCount }`, CAMetalLayer atomic presentation, `Frame_addFrameHandler` | 🟩 |
| `Dialog` | Base modal frame inheriting `Frame`: embeds `{ *window, *graphics, *stuff }`, `Dialog_addDialogHolder`, `Dialog_open`, modal scrim | 🟩 |
| `OptionDialog` | Modal dialog inheriting `Dialog` with action buttons (OK, Cancel, Yes, No, Retry) and selection dispatch | 🟩 |
| `InputDialog` | Modal dialog inheriting `Dialog` with prompt label, input buffer, placeholder, and submit dispatch | 🟩 |
| `FileDialog` | File system navigation dialog inheriting `Dialog` with path, filters, and entry selection | 🟩 |
| `Color` | Unified format-independent color: normalized float RGBA, ARGB32, RGBA32, HSV, HSL, Hex strings | 🟩 |
| `ColorDialog` | Modal color picker dialog inheriting `Dialog` with unified `Color` class and change dispatch | 🟩 |
| `AlertDialog` | Confirmation alert dialog with title, body message, and action buttons | 🟧 |

#### 7.3 Window (Darling Side)
Window bridge linking Darling panels to hotcwap OS windows.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| OS Window Bridge | Bridge connecting root Canvas to hotcwap native window | 🟩 |
| Resize & DPI Adaptation | Dynamic canvas resizing and Retina backing scale updates | 🟩 |
| Window-Scoped Event Routing | Window-isolated dispatch (BUG-016: global listener vs window-scoped) | 🟨 |

#### 7.4 Floating Overlays
Contextual floating UI primitives.

| Primitive | Scope & Capabilities | Status |
|:---|:---|:---:|
| `Tooltip` | Hover hint bubble with directional arrow escaping container clipping | 🟥 |
| `Popover` | Click-anchored floating card with light dismiss | 🟥 |
| `Menu` / `ContextMenu` | Hierarchical dropdown menu with shortcuts and right-click context menu | 🟥 |
| `Toast` / `ToastStack` | Non-modal notification queue with auto-dismiss timers and action buttons | 🟥 |

---

### 8. Platform, Event & Polish Substrates

#### 8.1 Event Subsystem & Bridges
Event capture, translation, and dispatch hierarchy.

| Subsystem / Event | Scope & Technical Details | Status |
|:---|:---|:---:|
| Event Dispatch Core | Top-down hit-testing and bubbling dispatch | 🟨 |
| Bridge Wiring | `Darling_bridgeAttach` connecting hotcwap to darling (BUG-001) | 🟨 |
| Pointer Events | Enter, hover, leave, down, up, drag event routing | 🟨 |
| Keyboard Events | Key press, release, character input (BUG-010: missing in main loop) | 🟧 |
| Focus Events | Focus acquire/release and keyboard focus cycling | 🟧 |
| Gesture Events | Multitouch trackpad scroll, fling, and pinch gestures | 🟨 |
| Value Change Events | Event channels for Slider, Knob, Switch, Checkbox, Select changes | 🟩 |
| Hierarchy Tree Events | Mutation events when nodes are attached, detached, or marked dirty | 🟩 |

#### 8.2 Animation, Cursor & Platform Bridges
System bridges and motion runtime.

| Subsystem | Scope & Technical Details | Status |
|:---|:---|:---:|
| `Anim` | Property animator with easing curves (linear, ease-in, ease-out, cubic, spring) | 🟩 |
| `Cursor` | Predefined cursors (Arrow, I-beam, Hand, Resize) + Cocoa NSCursor apply | 🟩 |
| `Font bake` | TrueType font parsing (`stb_truetype.h`) and SDF atlas baking | 🟩 |
| `IO mmap` & `IO bake` | memory-mapped I/O and binary font packaging | 🟩 |
| `Render raster` & `Surface` | CPU software rasterizer and pixel buffer memory surface | 🟩 |
| `Text core` & ObjC bridge | Subpixel CoreText rasterizer quad cache on macOS | 🟩 |
| `Panel Cocoa bridge` | ObjC board registry — retained offscreen VkLayer targets (single on-screen seam canvas) | 🟩 |
| `c23/add` & `darling-type.h` | Unified `Darling_add()` _Generic dispatcher and class ID registry | 🟩 |
| `Clipboard` | OS pasteboard bridge for text, images, and custom MIME payloads | 🟥 |
| `History` | Undo/redo command stack with branching history timeline | 🟥 |
| `HtmlExporter` | Layout-to-HTML serializer transpiling containers to web code | 🟥 |

#### 8.3 Layout Polish & Utility Styling Substrate
Visual polish primitives required for modern UI.

| Subsystem | Scope & Capabilities | Status |
|:---|:---|:---:|
| `Theme System` | Token table (50..950 ramps across slate, primary, success, warning, danger), WCAG audits | 🟥 |
| `FocusRing` | Theme-colored focus indicator outline on `:focus-visible` | 🟥 |
| `ProgressBar` | Determinate progress bar + indeterminate shimmer sweep | 🟥 |
| `Spinner` | Continuous rotating circular arc indicator | 🟥 |
| `Skeleton` | Shimmering placeholder blocks for loading UI | 🟥 |

---

### 9. SaaS & App Shell Kit (`Avatar`, `Badge`, `Chip`, `SearchField`, `Breadcrumb`, `Pagination`, `CommandPalette`, `StatCard`)

SaaS components composed on top of base primitives.

| Component | Scope & Capabilities | Status |
|:---|:---|:---:|
| `Avatar` | User avatar with initials fallback, photo loader, and online status dot | 🟥 |
| `Badge` / `Pill` | Status badge with tone variants (Success, Warning, Danger, Info) | 🟥 |
| `Chip` | Removable tag token with optional avatar and dismiss icon | 🟥 |
| `SearchField` | Input composite with search icon, clear button, and shortcut badge (Cmd+K) | 🟥 |
| `Breadcrumb` | Path navigation trail with segment links and chevron separators | 🟥 |
| `Pagination` | Page navigator with numbered buttons, page size selector, and prev/next | 🟥 |
| `CommandPalette` | Modal spotlight launcher (Cmd+K) with fuzzy action filtering | 🟥 |
| `StatCard` | Metric card displaying KPI value, trend delta pill, and sparkline chart | 🟥 |

---

### 10. Game Dev Kit — Bare-Metal HUD & Interactables

Game-grade UI nodes designed to outperform Dear ImGui and raylib GUI in visual quality, responsiveness, and zero-allocation frame execution.

#### 10.1 HudBar (MMORPG Status Bar)
Dynamic health, mana, stamina, or energy bar with lagging ghost drain.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Primary Instant Fill | Current resource value rendered immediately | 🟥 |
| Delayed Ghost Lag Bar | Secondary bar holding prior value before draining smoothly (visualizes damage taken) | 🟥 |
| Critical Damage Flash | White/red screen or bar flash on large health reductions | 🟥 |
| Low Resource Pulse | Ambient breathing/pulsing animation when value drops below 20% | 🟥 |
| Segmented Tick Dividers | Vertical divider notches every 100/250/500 HP | 🟥 |

#### 10.2 CooldownButton (Skill & Action Bar)
Action button featuring radial cooldown sweeps and hotkey prompts.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| 360° Radial Sweep Overlay | Darkened sweep clock tracking remaining cooldown time | 🟥 |
| Numeric Cooldown Timer | Large centered countdown text (`4.2s`, `1s`) fading out when ready | 🟥 |
| Ready Flash Animation | High-contrast radial flare animation upon cooldown completion | 🟥 |
| Keybind Badge Slot | Top-right or bottom-right keycap chip (`Q`, `E`, `R`, `Shift+1`) | 🟥 |
| Dimmed State on Insufficient Mana | Dimming button when player lacks resources to cast | 🟥 |

#### 10.3 DamageNumbers (Floating Combat Text)
High-throughput pooled combat text particle engine.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Zero-Alloc Particle Pool | Bounded pre-allocated pool of text nodes recycled each frame | 🟥 |
| Upward Velocity & Easing | Initial upward pop followed by gentle floating rise and alpha fade | 🟥 |
| Critical Hit Bounce & Scale | Oversized pop scale with color emphasis (yellow/red/gold) on critical hits | 🟥 |
| Damage Type Styling | Distinct color and icon styling for Physical, Magic, Fire, Poison, and Heals | 🟥 |

#### 10.4 InventoryGrid (RPG Item & Bag Grid)
Cell grid with drag-and-drop item management.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Drag-and-Drop Item Moving | Smooth pointer drag with floating ghost icon and target cell highlight | 🟥 |
| Item Stack Counters | Bottom-right item quantity numbers | 🟥 |
| Rarity Tier Borders | Colored border glow representing item tier (Common, Rare, Epic, Legendary) | 🟥 |
| Slot Lock & Cooldown Tint | Visual lock icon or cooldown clock over disabled item slots | 🟥 |
| Rich Item Hover Tooltip | Instant or delayed stat comparison card escaping container clipping | 🟥 |

#### 10.5 DialogBox (Visual Novel / NPC Dialogue)
Narrative dialogue box with typewriter animation and branch choices.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Typewriter Text Stream | Letter-by-letter text advance with audio tick hook and click-to-skip | 🟥 |
| Character Portrait Slot | Left or right textured quad displaying speaking NPC portrait | 🟥 |
| Choice Branching Buttons | Stack of interactive response buttons advancing dialogue state | 🟥 |
| Advance Prompt Indicator | Bouncing animated chevron indicating more dialogue is available | 🟥 |

#### 10.6 Minimap (Radar & World Map)
Real-time overhead tactical radar.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Player Frustum View Cone | Rotated triangle visualizing current camera orientation | 🟥 |
| Dynamic Entity Markers | Colored pings for allies (green), enemies (red), and objectives (yellow) | 🟥 |
| Fog of War Mask | Dynamic mask texture revealing discovered terrain | 🟥 |
| Minimap Zoom & Pan | Interactive mouse wheel zoom and click-to-move minimap navigation | 🟥 |

#### 10.7 NodeEditor (Blueprint & Graph Canvas)
Node-based visual scripting and shader graph canvas.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Retained Node Blocks | Movable card panels with header, title, and pin rows | 🟥 |
| Typed Input / Output Pins | Execution pins, data pins (float, int, vec3, string) with type colors | 🟥 |
| Cubic Bezier Wire Routing | Smooth bezier spline curves connecting output to input pins | 🟥 |
| Interactive Wire Drag | Dragging from pin to spawn dynamic wire with cursor snapping | 🟥 |
| Marquee Multi-Select | Bounding box drag selection selecting multiple nodes | 🟥 |

#### 10.8 GamepadNav (Gamepad Spatial Focus Engine)
First-class controller support for console and TV gameplay.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Directional D-Pad Focus Traversal | Algorithmic closest-widget raycast finding next target in 2D space | 🟥 |
| Shoulder Bumper Tab Cycling | L1/R1 cycling through TabPanels and inventory bags | 🟥 |
| Dynamic Action Button Prompts | Automatic rendering of contextual button glyphs (A/B/X/Y, ✕/○/□/△) | 🟥 |
| Virtual Cursor Fallback | Analog stick controlling smooth virtual pointer when spatial nav is disabled | 🟥 |

---

### 11. Spatial Studio & Live Property Inspector

Spatial tools enabling Darling to power spatial canvas layout and node editing and in-engine visual editing.

#### 11.1 SpatialCanvas (Infinite Canvas)
High-performance infinite 2D canvas.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Infinite Pan & Zoom | Smooth 120Hz pan/zoom transform matrix with inertial damping | 🟥 |
| Mini-Map Overview | Picture-in-picture bird's-eye navigator showing active viewport rect | 🟥 |
| Snapping & Smart Guides | Dynamic magenta alignment lines and equidistant distance badges | 🟥 |

#### 11.2 TransformBox (Spatial Manipulator)
Interactive bounding box for resizing and transforming UI nodes.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| 8-Handle Bounding Box | 4 corners + 4 edge handles for resizing nodes interactively | 🟥 |
| Rotation Pin | Extended stem handle for rotating panels in 2D space | 🟥 |
| Shift-Constrained Proportions | Locking aspect ratio during corner drag | 🟥 |

#### 11.3 PropertyInspector (Two-Way Design Inspector)
Sidebar property inspector editing layout and style properties live.

| Feature / Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Geometry Controls | Real-time editing of X, Y, W, H, Rotation, Corner Radius (Arc / Superellipse) | 🟥 |
| Auto-Layout Controls | Switching between Fixed, Hug, and Fill; padding and gap sliders | 🟥 |
| Paint & Stroke Controls | Color picker chips, opacity sliders, gradient angle rings, stroke width | 🟥 |
| Live Reflection | Changes made in inspector immediately update rendered canvas with zero reload | 🟥 |

---

## Strategic Implementation Priorities

To build towards the Darling Standard without regressions:

1. **P0: Event & Painter Fixes (Defect Resolution)**
   - Fix event delivery in live applications (`Darling_bridgeAttach` & `Key_dispatchEvents()`; BUG-001, BUG-010).
   - Add built-in state painters for `Button` (hover/pressed colors; BUG-002) and text rendering (BUG-013).
   - Add built-in painters for `Switch`, `Checkbox` (BUG-012), and `Slider` track/thumb (BUG-014).
   - Wire `Knob` pointer interaction in live gallery (BUG-003).
   - Fix `ScrollPanel` hit-test pick offset calculation (BUG-009).

2. **P1: Polish Substrate & Overlays**
   - Implement `OverlayRoot` to unblock `Select` dropdowns, `Tooltip`, and `Dialog` modals.
   - Implement the `Theme System` (50..950 token ramps, light/dark modes, contrast audits).
   - Implement `FocusRing` for accessible keyboard navigation.
   - Implement `ProgressBar`, `Spinner`, and `Skeleton` loading primitives.

3. **P2: Container & Layout Expansion (Auto-Layout & CSS Flex)**
   - Implement `FlexPanel` (row/col, wrap, gap, hug/fill/fixed).
   - Implement two-panel composition for `ScrollBar` (BUG-015) and horizontal scrolling (BUG-008).
   - Implement `SplitPanel`, `TabPanel`, `CardPanel`, and `TablePanel`.

4. **P3: Game Dev Kit & HUD Primitives**
   - Implement `HudBar` (lagging ghost drain + critical flash).
   - Implement `CooldownButton` (360° radial sweep clock + hotkey badge).
   - Implement `DamageNumbers` (zero-alloc floating particle pool).
   - Implement `InventoryGrid` (drag-and-drop item slots + rarity glow).
   - Implement `GamepadNav` (spatial D-pad navigation).

5. **P4: SaaS & Tooling Packs (Property Inspector & Node Editor)**
   - Implement `SearchField`, `CommandPalette`, `DataTable`, and `StatCard`.
   - Implement `CodeField` for text/syntax editing.
   - Implement `NodeEditor` (retained graph canvas with bezier wires).
   - Implement `SpatialCanvas` and `PropertyInspector`.

</details>

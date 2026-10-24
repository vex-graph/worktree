# drawling — 2D Drawing & Frame Animation Studio

> **Unfinished R5 application—not a shipped drawing studio.** This page is a
> roadmap, not whole-app readiness. R2 comprises [vexspoke](#file-vexspoke-md) CPU
> computation/behavior and [relational-engine](#file-relational-engine-md) memory/storage/native C search.
> Migration is staged with retained Vexspoke ABI/default allocator. R1 owns
> lifetimes/residency; GPU shaders/dispatch remain [graphvex](#file-graphvex-md). No completed
> engine integration or automatic schema migration is implied.

> R5 Interactable. Fluid 2D raster drawing studio and frame-by-frame animation workbench.
> The First Vertical Slice: Real input → Real pixels → Real file. Proves the stylus/mouse loop through Key/Mouse/Touch into retained nodes.
> Laws: Software-First Rasterization, Layers as Panels, Bounded Stroke Ring Undo, Zero-GC Frame Timeline.

---

## 🎯 Tier-0 Integration Proofs (Ground Truth)

*The live binary is the final judge. This table gates the repo headline — never the rows below, which keep their own independent truth. Statuses are re-verified, never copied from memory.*

| Proof Binary | End-to-End User Verification | Status | Evidence |
|---|---|:---:|---|
| `drawling_boot` (no target) | Stroke → pixels → save file (first vertical slice) | 🟥 | LICENSE + README only; zero working source |

## The Drawling Standard: Fluid Drawing & 2D Frame Animation in C23

Drawling provides fluid raster and vector brush dynamics with an accessible frame-by-frame animation timeline, backed by the high-framerate **Darling UI layer compositor**:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                            THE DRAWLING STANDARD                                 │
├─────────────────────────┬─────────────────────────┬──────────────────────────────┤
│ 1. Sub-8ms Input Loop   │ 2. Dual Canvas Core     │ 3. Layered Compositor        │
│ • 1000Hz raw event pump │ • CPU software raster   │ • LayeredContainer stack     │
│ • Pressure & tilt curve │ • GPU VkSceneCanvas path│ • Picture nodes per layer    │
│ • Lazy-brush stabilizer │ • Infinite pan/zoom     │ • 16 layer blend modes       │
│ • Zero dropped strokes  │ • Subpixel antialiasing │ • Alpha clipping masks       │
├─────────────────────────┴─────────────────────────┴──────────────────────────────┤
│ 4. Frame-by-Frame Animation Timeline + Hot-Reloadable Brush Engines              │
│ • Multi-frame animation scrubber with real-time 12/24/60 fps playback           │
│ • Multi-color onion skinning (red past, green future ghost frames)               │
│ • Hot-swappable brush modules (`brush_watercolor.dylib`, `brush_ink.dylib`)      │
│ • Native `.antibake` format + animated GIF / APNG / PNG sprite sheet exporters   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## Status Legend & Grading Standards

Every subsystem and mini-achievement is strictly graded based on the current reality of the codebase, test suites, and live runtime behavior:

| Emoji | Level | Definition |
|:---:|:---|:---|
| 💚 | **98% Done** | Basically 98% done: fully wired, compiles, runs, production-ready, actively polished |
| 🟩 | **95% Done** | Implemented & functional: wired, compiles and runs, minor polish remaining |
| 🟨 | **85% Done** | Substantially implemented: core works or has tests proving behavior, missing specific features/edge cases |
| 🟧 | **75% Done** | Partial implementation: core struct/concept exists, but major features missing or unwired |
| 🟥 | **Concept / Draft** | Still a concept or spec'd in docs/headers only, zero working source |
| ⬜ | **Vital Future Work** | Not implemented yet, but vital roadmap feature (+1 on the feature) |

---

## High-Level Subsystem Summary

| # | Subsystem | Scope Summary | Overall Status |
|:---:|:---|:---|:---:|
| 1 | `Retained Input Loop` | Stylus/mouse down-move-up, 1000Hz sampling, sub-8ms latency proof | 🟥 |
| 2 | `Dual Canvas Core` | Software Raster/Surface CPU canvas, Vulkan VkSceneCanvas GPU path | 🟥 |
| 3 | `Layered Compositing Stack` | LayeredContainer, per-layer Picture nodes, layer hierarchy, reordering | 🟥 |
| 4 | `Layer Blend Modes & Masks` | Multiply, Screen, Overlay, Soft Light, Alpha clipping masks | ⬜ |
| 5 | `Brush Engine & Dynamics` | Stamp dabs, spacing, opacity, pressure dynamics, vector ribbons | 🟥 |
| 6 | `Stroke Smoothing & Symmetry` | Lazy mouse stabilizer, exponential smoothing, mirror & radial symmetry | ⬜ |
| 7 | `Pixel Tools & Selection` | Eraser tool, scanline flood fill, lasso, rectangular marquee, transform | ⬜ |
| 8 | `Frame-by-Frame Animation Timeline`| Multi-frame scrubber, 12/24/60 fps playback, duplicate/reorder frames | ⬜ |
| 9 | `Onion Skinning Engine` | Configurable past/future ghost frames with tint overlays and opacity | ⬜ |
| 10 | `Formats & Multi-Exporters` | Native `.antibake` format, PNG/JPEG, animated GIF, and APNG export | 🟥 |

---

## Detailed Mini-Achievements Breakdown

### 1. Retained Input Loop & Stylus Dynamics

The core input-loop prover validating event-to-pixel throughput across the engine.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 1.1 | Sub-8ms Event-to-Pixel Latency | Routing pointer down/move/up from `hotcwap` directly to raster buffer | 🟥 |
| 1.2 | High-Frequency Subpixel Polling | Sampling pointer events at 1000Hz with subpixel float coordinates | 🟥 |
| 1.3 | Pressure Sensitivity Mapping | Mapping graphics tablet / Apple Pencil pressure to brush size and opacity | ⬜ |
| 1.4 | Stylus Tilt & Azimuth Angle | Modulating brush footprint orientation based on stylus physical tilt | ⬜ |
| 1.5 | Palm Rejection Filtering | Distinguishing touch contacts from active stylus pen inputs | ⬜ |

### 2. Dual Canvas Core (Software & Vulkan GPU)

High-performance 2D drawing surfaces.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 2.1 | Software Raster Canvas (`Raster`) | CPU pixel drawing backed by `graphvex` `Surface` and `ColorBuffer` | 🟥 |
| 2.2 | GPU Canvas Path (`VkSceneCanvas`) | Hardware Vulkan render path when brush strokes outrun 60fps on CPU | ⬜ |
| 2.3 | Smooth Canvas Pan & 2-Finger Zoom | 2D affine transform matrix with trackpad pinch and canvas rotation | 🟥 |
| 2.4 | Canvas Flip & Rotation Controls | One-click horizontal/vertical canvas flip and freeform angle rotation | 🟥 |
| 2.5 | 50-Stroke Bounded Undo Ring | Bounded circular undo history backed by `vexspoke` `RingBuffer` | 🟥 |

### 3. Layered Compositing Stack

Non-destructive drawing layers built directly on Darling panels.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 3.1 | Layer Stack Container | Multi-layer visual composition using Darling `LayeredContainer` | 🟥 |
| 3.2 | Picture Node per Layer | Each drawing layer backed by a distinct `Picture` bitmap node | 🟥 |
| 3.3 | Layer Opacity Slider | Independent alpha multiplier per drawing layer (0.0 to 1.0) | 🟥 |
| 3.4 | Layer Visibility & Lock Toggles | Hiding layers and locking layers against accidental modification | 🟥 |
| 3.5 | Layer Reordering & Merging | Dragging layer order and merging active layer down into lower layer | 🟥 |
| 3.6 | Layer Groups & Folders | Grouping related drawing layers into collapsible folders | 🟥 |

### 4. Layer Blend Modes & Clipping Masks

Comprehensive 16-mode layer compositing math.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 4.1 | Standard Blend Modes | Normal, Multiply, Screen, Overlay, Darken, Lighten, Color Dodge | ⬜ |
| 4.2 | Advanced Blend Modes | Soft Light, Hard Light, Difference, Exclusion, Hue, Saturation, Luminosity | ⬜ |
| 4.3 | Alpha Clipping Mask | Clipping upper layer drawing strictly to the non-transparent pixels of base | ⬜ |
| 4.4 | Alpha Lock Mode | Drawing on current layer without affecting already transparent pixels | ⬜ |

### 5. Brush Engine & Stroke Dynamics

Raster stamp and vector extrusion brush systems.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 5.1 | Round Stamp Brush Core | Circular raster stamp dab with radius, edge softness, and opacity | 🟥 |
| 5.2 | Dynamic Stamp Spacing | Computing step distance along stroke path to prevent bead artifacts | 🟥 |
| 5.3 | Vector Ribbon Extrusion (`VectorBrush`) | Continuous 2D triangle strip extrusion with smooth width curves | 🟩 |
| 5.4 | Hot-Reloadable Brush Modules | Custom brush math loaded as dynamic libraries via `hotcwap` | 🟥 |
| 5.5 | Textured Grain & Brush Shapes | Stamping custom alpha masks and paper grain textures along stroke | ⬜ |
| 5.6 | Wet Edge & Paint Bleed Simulation | Soft water-bleed edge darkening algorithm | ⬜ |

### 6. Stroke Smoothing & Symmetry Guides

Assisted drawing tools for clean linework.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 6.1 | Lazy Mouse Stabilizer | Trailing elastic string pulling brush tip for ultra-smooth linework | ⬜ |
| 6.2 | Exponential Moving Average Filter | Real-time jitter filter smoothing shaky hand movements | ⬜ |
| 6.3 | Vertical & Horizontal Mirror Symmetry | Real-time bilateral reflection drawing across central axis | ⬜ |
| 6.4 | Radial / Kaleidoscope Symmetry | Multi-segment radial symmetry (4, 6, 8, 12 rotational slices) | ⬜ |
| 6.5 | QuickShape Auto-Geometric Snap | Pausing stroke at end snaps hand-drawn shapes to perfect lines/circles | ⬜ |

### 7. Pixel Tools & Selection Mechanics

Manipulation tools for pixel art and illustration.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 7.1 | Dedicated Eraser Tool | Dual-mode eraser: pixel-clearing stamp or vector stroke delete | ⬜ |
| 7.2 | Scanline Flood Fill (Bucket) | Fast 4-way scanline flood fill with configurable color tolerance | ⬜ |
| 7.3 | Freehand Lasso Selection | Drawing arbitrary closed loops to create floating selection masks | ⬜ |
| 7.4 | Rectangular & Elliptical Marquee | Geometric selection box with feathering radius | ⬜ |
| 7.5 | Selection Transform Manipulator | Translating, rotating, and scaling active selection with bicubic sampling | ⬜ |
| 7.6 | Live Eyedropper Color Picker | Long-press or shortcut sampling exact RGBA color under pointer | 🟨 |

### 8. Frame-by-Frame Animation Timeline

Traditional 2D frame-by-frame animation engine.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 8.1 | Horizontal Frame Scrubber Strip | Bottom timeline showing thumbnail previews of sequential animation frames | ⬜ |
| 8.2 | Add, Delete, Duplicate Frames | Quick one-click timeline actions inserting blank or duplicated frames | ⬜ |
| 8.3 | Real-Time Animation Playback | Configurable frame rates: 12 fps (traditional 2s), 24 fps (film), 60 fps | ⬜ |
| 8.4 | Frame Hold Duration Multiplier | Holding individual drawings across 2, 3, or N playback ticks | ⬜ |
| 8.5 | Loop & Ping-Pong Playback Modes | Continuous looping or back-and-forth animation review | ⬜ |

### 9. Onion Skinning & Animation Assist

Visual ghost overlays for smooth in-betweening.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 9.1 | Configurable Onion Skin Frames | Displaying 1, 2, or 3 previous and subsequent frames as semi-transparent ghosts | ⬜ |
| 9.2 | Dual-Tone Color Ghosting | Red/orange tint for preceding frames, green/blue tint for succeeding frames | ⬜ |
| 9.3 | Ghost Opacity Falloff | Progressively fading opacity for frames further away in time | ⬜ |
| 9.4 | Flip-Between Quick Scrub | Rapidly toggling between adjacent frames to check motion flow | ⬜ |

### 10. Formats, Packaging & Multi-Exporters

Saving artwork and exporting animated creations.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 10.1 | Native `.antibake` Project Format | Saving layers, strokes, and metadata using `io/bake.c` quad format | 🟥 |
| 10.2 | High-Resolution PNG / JPEG Export | Flattening layers and exporting static artwork to standard raster files | 🟥 |
| 10.3 | Animated GIF Exporter | Encoding frame timeline into optimized animated GIF with palette quantization | ⬜ |
| 10.4 | Animated PNG (APNG) Exporter | Exporting full 24-bit color animations with alpha transparency | ⬜ |
| 10.5 | Game Sprite Sheet Packager | Packing animation frames into packed 2D texture atlas with JSON frames metadata | ⬜ |

---

## Strategic Implementation Priorities for Drawling

1. **P0: Input-Loop Prover (Stylus to Pixels)**
   - Connect `hotcwap` pointer events to a single `Raster` canvas in a live window.
   - Implement the round stamp brush and verify sub-8ms stroke responsiveness.
   - Implement the 50-stroke undo ring.

2. **P1: Multi-Layer Compositor**
   - Assemble `LayeredContainer` holding multiple `Picture` layer nodes.
   - Add layer opacity and visibility controls in a Darling sidebar.

3. **P2: Frame-by-Frame Animation Timeline**
   - Implement the bottom frame timeline strip and playback clock.
   - Implement two-frame onion skinning (red past, green future).

4. **P3: Exporters & File Formats**
   - Wire native `.antibake` serialization and animated GIF export.

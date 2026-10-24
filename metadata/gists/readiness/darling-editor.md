# darling-editor — Spatial Prototyping & Layout Canvas

> **Unfinished R5 concept—not a shipped spatial studio.** No independent app
> checkout exists in this workspace; framework capabilities do not prove the
> editor. R2 comprises [vexspoke](#file-vexspoke-md) CPU computation/behavior and
> [relational-engine](#file-relational-engine-md) memory/storage/native C search. Migration is staged with
> retained Vexspoke ABI/default allocator. R1 owns lifetimes/residency; Graphvex
> owns GPU work/composition. No engine integration or schema migration implied.

> R5 Interactable. Spatial design studio and UI prototyping workbench.
> Built on darling-framework, graphvex, and sesh for real-time multiplayer collaboration.
> Laws: Infinite Spatial Coordinates, Dogfooding Darling Widgets, Hardware JFA Vector Baking, Multi-Format Exporters (C23/HTML/SVG).

---

## 🎯 Tier-0 Integration Proofs (Ground Truth)

*The live binary is the final judge. This table gates the repo headline — never the rows below, which keep their own independent truth. Statuses are re-verified, never copied from memory.*

| Proof Binary | End-to-End User Verification | Status | Evidence |
|---|---|:---:|---|
| `darling-editor_boot` (no target) | Boot canvas → pan/zoom → export layout | 🟥 | No source tree in `..`; spec only |

## The Darling-Editor Standard: The Spatial Prototyping Studio

Darling-Editor provides infinite spatial whiteboard freedom with vector layout precision and high-framerate rendering, outputting production-ready native C23 code:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                           THE DARLING-EDITOR STANDARD                            │
├─────────────────────────┬─────────────────────────┬──────────────────────────────┤
│ 1. 120Hz Infinite Canvas│ 2. Auto-Layout Engine   │ 3. Spatial Whiteboard Canvas   │
│ • Smooth pan/zoom matrix│ • Hug, Fill, Fixed modes│ • Color-coded sticky notes   │
│ • Zero blur on zoom (SDF│ • Gap & padding controls│ • Smart orthogonal mindmaps  │
│ • Bird's-eye mini-map   │ • G2 superellipse cards │ • Discussion comment pins    │
│ • Snapping smart guides │ • Auto-align distribution│ • Interactive voting dots   │
├─────────────────────────┴─────────────────────────┴──────────────────────────────┤
│ 4. Multi-Format Production Code Generators + Real-Time Multiplayer Sync          │
│ • One-click C23 layout exporter (`Class(...)` with 9-grid anchors)               │
│ • Semantic HTML5 + CSS web layout exporter                              │
│ • Infinite vector SVG & multi-scale PNG/JPEG raster exporter                    │
│ • Multiplayer live cursors, presence avatars, and node sync via sesh             │
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
| 1 | `Infinite 120Hz Canvas Core` | Smooth 2D pan/zoom matrix, inertial damping, grid coordinates, mini-map | 🟥 |
| 2 | `Spatial Selection & Transform` | 8-point bounding transform handles, rotation stem, multi-node marquee | 🟥 |
| 3 | `Smart Guides & Snapping` | Alignment guidelines, equidistant gap badges, pixel snapping engine | 🟥 |
| 4 | `Sticky Notes & Markdown Cards` | Color-coded note pads, rich text markdown editing, comment pin badges | 🟥 |
| 5 | `Mindmapping & Flowchart Wire` | Orthogonal line routing, curved bezier splines, magnetic node pins | 🟥 |
| 6 | `Darling UI Widget Stamping` | Tool palette stamping Button, Input, Slider, Card, and Dialog elements | 🟥 |
| 7 | `Auto-Layout Engine (Fixed / Hug / Fill)` | Interactive Fixed / Hug / Fill resizing, auto-gap, padding adjustment | 🟥 |
| 8 | `Icon Browser & JFA Vector Bake` | Searchable icon palette (Lucide/Tabler), vector SVG import, SDF baking | 🟥 |
| 9 | `Multi-Format Code Exporters` | Native C23 code gen, semantic HTML5/CSS, SVG, high-res PNG | 🟥 |
| 10 | `Prototype Presentation Runner` | Full-screen runner, click interaction hotspots, transition animations | ⬜ |
| 11 | `Multiplayer Sesh Sync` | Live remote user cursors, presence avatars, real-time node locks | 🟥 |

---

## Detailed Mini-Achievements Breakdown

### 1. Infinite 120Hz Spatial Canvas Core

High-framerate infinite 2D plane powered by Vulkan.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 1.1 | 2D Affine Pan/Zoom Transform Matrix | Translation, scale, and zoom centered on mouse cursor position | 🟥 |
| 1.2 | Inertial Scroll & Pinch Zoom Damping | Smooth trackpad pinch-to-zoom and pan with momentum decay | 🟥 |
| 1.3 | Dynamic Procedural Coordinate Grid | Infinite dot/line grid scaling seamlessly through zoom levels | 🟥 |
| 1.4 | Picture-in-Picture Mini-Map Navigator | Bottom-corner bird's-eye navigator displaying entire board extent | 🟥 |
| 1.5 | Zoom-to-Fit & Zoom-to-Selection | Instant keyboard shortcuts (Shift+1, Shift+2) centering content | 🟥 |
| 1.6 | Infinite Canvas Bounds Virtualization | Viewport frustum culling skipping off-screen nodes | 🟥 |

### 2. Spatial Selection & Transform Manipulator

Interactive manipulation of canvas nodes.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 2.1 | 8-Point Bounding Transform Handles | 4 corner handles + 4 edge midpoint handles for interactive resizing | 🟥 |
| 2.2 | Rotation Stem Handle | Top-extended rotation pin rotating nodes in 2D space | 🟥 |
| 2.3 | Shift-Constrained Aspect Ratio | Holding Shift locks 1:1 aspect ratio during corner drag | 🟥 |
| 2.4 | Alt-Centered Transform Scaling | Holding Alt resizes symmetrically around the node's center point | 🟥 |
| 2.5 | Marquee Multi-Node Selection | Click-and-drag rubberband rectangle selecting all intersecting nodes | 🟥 |
| 2.6 | Grouping & Hierarchy Compound Nodes | Grouping nodes (`Cmd+G`) into unified parent bounds | 🟥 |

### 3. Smart Guides, Alignment & Snapping

Precision geometric layout assistance.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 3.1 | Real-Time Alignment Snapping Lines | Magenta guidelines appearing when edges/centers align with siblings | 🟥 |
| 3.2 | Equidistant Gap Distribution Chips | Visual numeric badges displaying distance between adjacent cards | 🟥 |
| 3.3 | Snap-to-Grid Mode | Optional snapping of node positions and sizes to 8pt/16pt grid | 🟥 |
| 3.4 | Multi-Selection Distribution Actions | One-click align Left, Center, Right, Top, Middle, Bottom; distribute evenly | 🟥 |

### 4. Sticky Notes, Cards & Discussion Pins

Collaborative brainstorming cards, notes, and mindmap connectors.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 4.1 | Color-Coded Sticky Note Pads | Yellow, cyan, lime, peach, and lavender square sticky notes with shadow | 🟥 |
| 4.2 | Direct In-Place Text Editing | Double-click sticky note or card to type text directly | 🟥 |
| 4.3 | Rich Text Markdown Formatting | Headings, bold, italic, bullet lists, and checkboxes inside notes | 🟥 |
| 4.4 | Discussion Comment Pins | Click anywhere to drop avatar comment pin with reply thread | 🟥 |
| 4.5 | Interactive Voting Emoji Badges | Stamping reaction dots (👍, ❤️, 🔥, 🚀) onto cards | 🟥 |

### 5. Mindmapping & Flowchart Connectors

Intelligent connecting lines between ideas and wireframe states.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 5.1 | Smart Orthogonal Line Routing | Right-angle line routing navigating cleanly around obstacle cards | 🟥 |
| 5.2 | Smooth Curved Bezier Splines | Flowing cubic bezier connector curves with adjustable tension | 🟥 |
| 5.3 | Directional Arrowhead Endings | Open arrow, filled triangle, circle, and diamond terminal caps | 🟥 |
| 5.4 | Magnetic Node Connection Anchors | 4 cardinal connection magnets per node (N, S, E, W) snapping lines | 🟥 |
| 5.5 | Connector Text Labels | Inline editable text tags centered along connector lines | 🟥 |

### 6. Darling UI Widget Stamping Palette

Dogfooding the entire Darling component library inside the visual editor.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 6.1 | Drag-and-Drop Tool Palette | Sidebar dock containing all 107 Darling UI primitives | 🟥 |
| 6.2 | Stamping Buttons & Switches | Dragging interactive Buttons, Switches, and Checkboxes onto canvas | 🟥 |
| 6.3 | Stamping Input Fields & Sliders | Placing editable Text Fields, Sliders, Knobs, and DatePickers | 🟥 |
| 6.4 | Stamping Structured Card Panels | Dropping pre-styled `CardPanel` structures with headers and footers | 🟥 |
| 6.5 | Stamping Dialogs & Modal Frames | Placing modal dialogs with scrim overlays and action buttons | 🟥 |
| 6.6 | 9-Grid Anchor Visualizer | Interactive anchor selector setting NW, N, NE, Center parent anchors | 🟥 |

### 7. Auto-Layout Studio (Fixed / Hug / Fill)

Modern flexbox layout modeling directly on the canvas.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 7.1 | Sizing Mode: Hug Contents | Container auto-resizes its bounds to tightly wrap its children | 🟥 |
| 7.2 | Sizing Mode: Fill Container | Child element expands to stretch across parent container's width/height | 🟥 |
| 7.3 | Sizing Mode: Fixed Dimensions | Explicit pixel width and height constraints | 🟥 |
| 7.4 | Interactive Padding Controls | Dragging margin/padding handles directly on the canvas surface | 🟥 |
| 7.5 | Direction & Wrap Switching | One-click toggle between Horizontal Row, Vertical Column, and Wrap | 🟥 |
| 7.6 | G2 Superellipse Corner Smoothing | Apple-smooth squircle corner radius adjustment | 🟥 |

### 8. Icon Browser & JFA Vector Baking

Integrated vector assets rendered crisply via GPU compute.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 8.1 | Searchable Icon Palette | Browsing 2,000+ vector icons (Lucide & Tabler sets via `api-haven`) | 🟥 |
| 8.2 | SVG File Drag-and-Drop Import | Dragging external `.svg` files onto canvas as editable vector paths | 🟥 |
| 8.3 | GPU Jump-Flood Algorithm Baking | Realtime baking of SVG vectors to SDF textures (`sdf_jfa.comp`) | 🟥 |
| 8.4 | Infinite Zoom Sharpness | Vectors zoom from 10% to 5000% with zero pixelation at 120fps | 🟥 |

### 9. Multi-Format Production Exporters

Translating visual designs directly into shippable engineering artifacts.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 9.1 | Native C23 Code Generator | Generating production-ready `Class(...)` code with 9-grid Darling anchors | 🟥 |
| 9.2 | One-Click Code Copy (Cmd+Shift+C) | Copying highlighted component directly as C23 source code to clipboard | 🟥 |
| 9.3 | Semantic HTML5 + CSS Exporter | Serializing visual containers to clean web divs with semantic styling classes | 🟥 |
| 9.4 | Vector SVG File Exporter | Exporting diagrams and frames to standard `.svg` vector files | 🟥 |
| 9.5 | Multi-Scale Raster Exporter | Exporting selected frames to 1x, 2x, 3x Retina PNG/JPEG images | 🟥 |

### 10. Interactive Prototype Presentation Runner

Live preview mode for user testing and presentations.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 10.1 | Full-Screen Prototype Player | Dedicated presentation window hiding editor chrome | ⬜ |
| 10.2 | Interactive Click Hotspots | Wiring button clicks to navigate to target artboard screens | ⬜ |
| 10.3 | Screen Transition Animations | Slide Left/Right, Push, Dissolve, and Instant page transitions | ⬜ |
| 10.4 | Interactive Form Inputs in Preview | Live typing and toggling within prototype components | ⬜ |

### 11. Real-Time Multiplayer Collaboration (`../interface/sesh`)

Multiplayer synchronization via WebSockets and Cloudflare edge.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 11.1 | Live Remote User Cursors | Real-time 60Hz cursor positions with colored user name badges | 🟥 |
| 11.2 | Active Presence Avatar Rail | Top-right avatar row showing online collaborators | 🟥 |
| 11.3 | Optimistic CRDT Node Replication | Synchronizing node positions, text edits, and colors via `sesh` | 🟥 |
| 11.4 | Node Lock During Active Edit | Preventing edit collisions by highlighting actively selected nodes | 🟥 |

---

## Strategic Implementation Priorities for Darling-Editor

1. **P0: Canvas Pan/Zoom & Node Quad Rendering**
   - Implement `SpatialCanvas` pan/zoom matrix and Vulkan grid rendering.
   - Implement node selection bounding box with 8 transform handles.

2. **P1: Sticky Notes & Markdown Cards**
   - Implement editable text pads built on Darling `Label` / `Textarea`.

3. **P2: Darling UI Widget Stamping & Palette**
   - Create the widget palette sidebar allowing users to stamp Darling buttons, inputs, and cards.

4. **P3: C23 Code Exporter**
   - Implement tree-to-C23 transpiler generating idiomatic Darling layout code.

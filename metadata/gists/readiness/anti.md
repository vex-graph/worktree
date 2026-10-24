# anti — R6 Creative Superapp R&D

> **Unfinished R6 superapp—not a shipped game engine or creative suite.** Rows below are design
> targets or granular feature claims, not whole-app readiness. R2 comprises
> [vexspoke](#file-vexspoke-md) CPU computation/behavior and [relational-engine](#file-relational-engine-md) memory/storage,
> stable rows, bindings and native C search. Migration is staged; existing
> Vexspoke ABI/default allocator remain. R1 owns lifetimes/residency; GPU work
> stays [graphvex](#file-graphvex-md). No automatic schema migration or app integration is implied.
> No local lawbook (`anti-preferences.md`) exists yet; that missing repo-local
> preferences file is an explicit gap, and the universal constitution plus
> applicable test laws still bind.

> R6 Superapp: composes IDE, DAW, drawing and game/creative workflows over R1–R5
> public contracts. No lower tier includes R6 code; implementation ownership stays
> with the lower-tier owner. The legacy game-engine roadmap below is one future
> workflow, not a shipped product or a restriction to one app category.
> Baseline target: 6-digit FPS empty-window loop on base-model Apple Silicon Mac.
> Laws: 5-Column Studio Law, Bindless or Bust, Relational DOD Pointer Buses, Reversible Physics Until Disturbed, Whole-Model Meshlet Swaps.

---

## 🎯 Tier-0 Integration Proofs (Ground Truth)

*The live binary is the final judge. This table gates the repo headline — never the rows below, which keep their own independent truth. Statuses are re-verified, never copied from memory.*

| Proof Binary | End-to-End User Verification | Status | Evidence |
|---|---|:---:|---|
| `anti_sandbox` (no target) | Boot studio loop at baseline FPS | 🟥 | LICENSE + README only; zero working source |

## The Anti Standard: The Next-Gen 3D Relational Engine

Anti's legacy game-workflow design targets a high-performance C23 studio with
visual fidelity, agility and relational DOD cache locality. These are unmeasured
aspirations: this repository has no working source or executable workflow.

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                               THE ANTI STANDARD                                  │
├─────────────────────────┬─────────────────────────┬──────────────────────────────┤
│ 1. 5-Column Studio Law  │ 2. Bindless GPU Core    │ 3. Relational DOD Engine     │
│ • Left icon rail        │ • Bindless objects & tex│ • DOD pointer buses          │
│ • 5-item left sidebar   │ • 150+ stackable filters│   {pool_id, pool_index}      │
│ • Main 2x overscan view │ • 4-tier lighting stack │ • O(1) reactive updates      │
│ • 4-item right inspector│ • Virtualized meshlets  │ • Darkbase native store      │
│ • Right utility rail    │ • Golyporphism glass OIT│ • Universal search engine    │
├─────────────────────────┴─────────────────────────┴──────────────────────────────┤
│ 4. Reversible Physics Scrubber + Tesseract Portals + Apple-Shortcuts Scripting   │
│ • Deterministic physics with timeline scrubber; flips non-deterministic on hit   │
│ • Physics bake button re-syncs simulations back to timeline                      │
│ • Tesseract folding coordinates & seamless spatial portals on Day 1             │
│ • Layered texture painting directly onto 3D object surfaces               │
│ • Apple-Shortcuts declarative one-liner scripting + pre/post lifecycle hooks     │
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
| 1 | `Baseline Runner & Templates` | 6-digit FPS empty loop, base-model Mac UMA, 3 starter templates | 🟥 |
| 2 | `5-Column Studio Workspace` | Left icons, 5-item left sidebar, main viewport, 4-item inspector, right icons | 🟥 |
| 3 | `Multi-Viewport Navigation` | Multiple simultaneous viewports, 2x overscan, breadcrumb focus, tab detach | 🟥 |
| 4 | `Universal Persistent Undo` | Cross-focus persistent undo tree across scenes, items, and script edits | 🟥 |
| 5 | `Two Play Simulation Modes` | In-place scene simulation vs dedicated game window with profiling preview | 🟥 |
| 6 | `Bindless GPU Pipeline` | BindlessHeap object/texture descriptors, 150+ stackable filter graph | 🟥 |
| 7 | `4-Tier Stackable Lighting` | Baked path-traced → Deferred → GI surfel cache → Full path tracing | 🟥 |
| 8 | `Advanced Graphics & Glass OIT` | Golyporphism order-independent transparency, floor grid, volumetric fog | 🟥 |
| 9 | `Virtualized Meshlet Geometry` | 128-triangle meshlets with whole-model tier swaps (1/4 → 1/8 → 1/16) | 🟥 |
| 10 | `Per-Object Painting Canvas` | Layered texture painting on 3D object surfaces with filters | 🟥 |
| 11 | `Tesseract & Portal Engine` | 4D tesseract folding coordinates and seamless portal transitions on Day 1 | 🟥 |
| 12 | `Relational DOD Engine Core` | `{pool_id, pool_index}` pointer buses, struct reflection, reactive updates | 🟥 |
| 13 | `Darkbase & Universal Query` | Built-in DBMS, paged TOC storage, universal search across code and assets | 🟥 |
| 14 | `Deterministic Scrubber Physics` | Reversible timeline physics with scrubber; instant non-deterministic flip | 🟥 |
| 15 | `Precision & Thread Scheduling` | fp32/fp64 coordinate precision switch, 4-level thread scheduler | 🟥 |
| 16 | `Declarative Scripting & Hooks` | Apple-Shortcuts style one-liners, pre-start and post-teardown lifecycle hooks | 🟥 |
| 17 | `Device Profiles & Telemetry` | Per-device calibration profiles, vexspoke system event probes, bug reporter | 🟥 |
| 18 | `Viewer3D & Object Turntable` | Future 3D object inspection, orbit camera, turntable framing law, MaterialPanel | 🟥 |

---

## Detailed Mini-Achievements Breakdown

### 1. Baseline Performance & Starter Templates

Proving zero-overhead execution on base-model hardware.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 1.1 | 6-Digit FPS Empty Window Baseline | Pure event pump + minimal present loop validating zero-overhead baseline | ⬜ |
| 1.2 | Base-Model Apple Silicon Optimization | Proposed UMA consumer integration; no app implementation or transfer proof | 🟥 |
| 1.3 | Template: "Nothing" | Blank slate template with all optional engine modules stripped | 🟥 |
| 1.4 | Template: "Regular" | Balanced standard template: 3D scene, basic lighting, physics, audio | 🟥 |
| 1.5 | Template: "Cutting Edge" | High-fidelity template: surfel GI, virtualized meshlets, tesseract portals | 🟥 |

### 2. 5-Column Studio Workspace Law

The disciplined, clean editor interface layout.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 2.1 | 5-Column Grid Geometry | Left icons / Left sidebar / Main scene / Right sidebar / Right icons | 🟥 |
| 2.2 | Left Rail: Mode & Tool Switchers | One-click toggles for workspace modes and primary toolbars | 🟥 |
| 2.3 | Left Sidebar Item 1: File Directory | VFS project explorer with asset previews and folder organization | 🟥 |
| 2.4 | Left Sidebar Item 2: Toolbox | Selection, translate, rotate, scale, terrain brush, and spawn tools | 🟥 |
| 2.5 | Left Sidebar Item 3: Exports | Target platform packager (Mac, Linux, Windows, Mobile, WebAssembly) | 🟥 |
| 2.6 | Left Sidebar Item 4: Game Hierarchy | Scene entity tree with grouping, parenting, and visibility toggles | 🟥 |
| 2.7 | Left Sidebar Item 5: Asset Marketplace | Online asset browser binding to api-haven providers (Openverse, Poly Haven) | 🟥 |
| 2.8 | Right Dynamic Inspector (4 States) | Automatically switches: Game Props → Scene Props → Group Props → Object Props | 🟥 |
| 2.9 | Game Properties Combobox | 10-item picker: App, Window, Renderer, Structs, Variables, Events, DB, Server, Bugs, Export | 🟥 |
| 2.10 | Bottom Bar Breadcrumbs & Git | Active hierarchy path links on left; git branch and sync status | 🟥 |
| 2.11 | Bottom Bar AI Visual Advisor | Visual guidance button analyzing scene composition and lighting balance | 🟥 |

### 3. Multi-Viewport Navigation & Spatial Workflow

Flexible camera perspectives and viewport overscan.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 3.1 | Multiple Simultaneous Viewports | Rendering different camera angles of the same live scene side-by-side | 🟥 |
| 3.2 | 2x Viewport Overscan Rendering | Editor renders 2× visible viewport (1/3 fallback) for smooth camera panning | 🟥 |
| 3.3 | Hierarchical Breadcrumb Navigation | Clickable path trail tracking nested group and prefab depths | 🟥 |
| 3.4 | Isolate in New Tab | Popping selected prefab, mesh, or character into an isolated workspace tab | 🟥 |
| 3.5 | Peekable & Detachable Tabs | Tearing off editor tabs into independent OS windows managed by `hotcwap` | 🟥 |
| 3.6 | Camera Orbit, Pan & Fly Modes | Proposed orbit, pan and fly-through controls; no app implementation | 🟥 |

### 4. Universal Persistent Undo & Versioning

Non-linear history preserved across entire sessions.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 4.1 | Cross-Focus Persistent Undo Tree | Undo history tracking scenes, assets, materials, and scripts in unified tree | 🟥 |
| 4.2 | Timeline History Scrubber | Visual slider scrubbing backward and forward through editor modifications | 🟥 |
| 4.3 | Branching Timeline Navigation | Branching undo states when actions are taken after rewinding | 🟥 |
| 4.4 | Scene Snapshot Serializer | Saving delta snapshot states directly into Darkbase project database | 🟥 |

### 5. Two Play Simulation Modes

Instant testing without restarting the editor.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 5.1 | In-Place Scene Simulation | Simulating physics, particles, and scripts directly inside editor viewport | 🟥 |
| 5.2 | Dedicated Game Play Window | Spawning standalone `Window` instance running the compiled game build | 🟥 |
| 5.3 | Live Profiling Preview Bar | In-game HUD overlay displaying frame time breakdown, draw calls, memory | 🟥 |
| 5.4 | Hot-Reloading During Play | Modifying C23 scripts and reloading live logic while game window runs | 🟥 |

### 6. Bindless GPU Architecture & Filter Graph

Modern graphics submission without descriptor thrashing.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 6.1 | Bindless Object & Texture Heap | All scene textures and mesh buffers indexed in a single GPU heap | 🟥 |
| 6.2 | 150+ Stackable Post-Processing Filters | Pre-authored composable filters: Bloom, Vignette, Cel-Shade, Film Grain | 🟥 |
| 6.3 | Order-Dependent Filter Stacking | Arbitrary filter ordering in render graph with predictable layer blending | 🟥 |
| 6.4 | Choice-Over-Code Architecture | Rich parameter sliders replacing manual GLSL/HLSL writing for creators | 🟥 |

### 7. 4-Tier Stackable Lighting Engine

Unified lighting model scaling from baked speed to path-traced realism.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 7.1 | Tier 1: Baked Path-Traced Maps | Offline lightmaps baked via compute shaders for static geometry | 🟥 |
| 7.2 | Tier 2: Deferred Directional Lighting | Dynamic shadow-casting directional and point lights with shadow cascades | 🟥 |
| 7.3 | Tier 3: Surfel Cache Global Illumination | Dynamic indirect lighting cache updated via surfel ray probes | 🟥 |
| 7.4 | Tier 4: Realtime Path Tracing | Full hardware ray-traced reflections and global illumination | 🟥 |
| 7.5 | Inter-Tier Light & Shadow Bleeding | Higher tier lighting smoothly composites over lower tiers | 🟥 |

### 8. Advanced Graphics & Glass OIT (Golyporphism)

High-fidelity optical and transparency effects.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 8.1 | Golyporphism (Glass OIT) | Order-independent transparency via compute tile buckets without sorting | 🟥 |
| 8.2 | Procedural Ground Grid Pipeline | Proposed ground grid; no app pipeline implementation or GPU proof | 🟥 |
| 8.3 | Volumetric Fog & Atmospheric Scatter | Ray-marched light shafts and height-based atmospheric fog | 🟥 |
| 8.4 | Frosted Glass & Surface Refraction | Screen-space refractions with chromatic aberration for glass surfaces | 🟥 |

### 9. Virtualized Geometry & Meshlet LOD

High-density geometry rendering without popping artifacts.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 9.1 | 128-Triangle Meshlet Clusters | Proposed meshlet consumer workflow; no app implementation or owner proof | 🟥 |
| 9.2 | Whole-Model Tier Swapping | Seamless model-level swaps as screen size shrinks (Full → 1/4 → 1/8 → 1/16) | 🟥 |
| 9.3 | Max 8 Cooked Tiers per Model | Precomputing up to 8 cooked geometric tiers per asset | 🟥 |
| 9.4 | Terrain Meshlet Cluster Culling | Proposed GPU culling consumer workflow; no app implementation or owner proof | 🟥 |

### 10. Per-Object Dedicated Painting Canvas

Layered 3D texture painting directly inside the viewport.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 10.1 | 3D Surface Brush Raycasting | Raycasting pointer coordinates to UV coordinates on 3D meshes | 🟥 |
| 10.2 | Multi-Layer Texture Painting | Painting on discrete texture layers with opacity and blend modes | 🟥 |
| 10.3 | Layered Texture Filter Stack | Applying 2D filters (blur, sharpen, tint) to individual texture layers | 🟥 |
| 10.4 | Texture Export & Rebaking | Serializing painted texture layers back into project asset bundles | 🟥 |

### 11. Tesseract Folding Coordinates & Portals

Seamless spatial transitions and non-Euclidean geometry on Day 1.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 11.1 | 4D Tesseract Coordinate Transformations | Mathematical coordinate system supporting folded spatial topologies | 🟥 |
| 11.2 | Seamless Portal Viewport Stamping | Rendering recursive portal views through doorway stencils | 🟥 |
| 11.3 | Teleportation & Momentum Handoff | Preserving velocity, orientation, and physics across portal planes | 🟥 |

### 12. Relational DOD Engine Core

Data-Oriented Design relational database over raw memory pointer buses.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 12.1 | DOD Pointer Bus Architecture | Managing entities as `{pool_id, pool_index}` pairs over integer buses | 🟥 |
| 12.2 | Reactive O(1) Position Updates | Moving entities updates memory in O(1) time without pointer chasing | 🟥 |
| 12.3 | Custom Struct Reflection | User-defined structs reflect automatically into relational tables | 🟥 |
| 12.4 | Hot-Adding Entity Components | Dynamically attaching and detaching component structs at runtime | 🟥 |

### 13. Darkbase Integration & Universal Search

Built-in database management system and project query engine.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 13.1 | Built-in Darkbase DBMS | Lightweight relational database storing project assets, scenes, and entities | 🟥 |
| 13.2 | Paged TOC File Serialization | Secure, backward-compatible paged file format with table of contents | 🟥 |
| 13.3 | Universal Search & Query Bar | Querying `player.speed` finds code definition, scene usages, and live settings | 🟥 |
| 13.4 | In-Search Value Mutation | Directly editing property values inside search bar results | 🟥 |

### 14. Deterministic Scrubber Physics & Simulation

Reversible physics with instant non-deterministic branching.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 14.1 | Deterministic Physics Loop | Fixed-timestep physics simulation recordable into a scrubbable buffer | 🟥 |
| 14.2 | Timeline Physics Scrubber | Scrubbing backward and forward to review physics interactions | 🟥 |
| 14.3 | Disturbance State Flip | Instantly flipping disturbed objects from deterministic to non-deterministic | 🟥 |
| 14.4 | Physics Bake Engine | "Bake" button re-syncing and cementing simulation results to timeline | 🟥 |

### 15. Precision Coordinates & 4-Level Thread Scheduler

Configurable numerical precision and fine-grained CPU scheduling.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 15.1 | Switchable Coordinate Precision | Toggle between `fp32`, `fp64`, `int32fp32`, `int64fp64` via project setting | 🟥 |
| 15.2 | 4-Level Thread Priority Model | Unused, Sleep, Dynamic, and Busy-Wait thread execution tiers | 🟥 |
| 15.3 | Hot-Adding Scripting Threads | Spawning additional dedicated worker threads during high script loads | 🟥 |
| 15.4 | SSD-to-VRAM Paged Streaming | Direct asset paging from disk to VRAM via memory-mapped I/O | 🟥 |

### 16. Declarative Scripting & Lifecycle Hooks

Boilerplate-free logic and engine events.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 16.1 | Apple-Shortcuts Style One-Liners | Compact declarative scripting syntax mapping directly to relational IDs | 🟥 |
| 16.2 | Observable Scripting Variables | Properties trigger event callbacks automatically when values change | 🟥 |
| 16.3 | Pre-Engine Start Hook | Scripts executing before graphics engine boots (asset verification, setup) | 🟥 |
| 16.4 | Post-Window Teardown Hook | Scripts executing after window closes (cleanup, telemetry sync, auto-save) | 🟥 |

### 17. Device Profiles, Telemetry & Shipping

Hardware integration and distribution tools.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 17.1 | Saved Hardware Device Profiles | Remembering user controller, graphics tablet, and keyboard calibrations | 🟥 |
| 17.2 | System Event Probes | Detecting USB connection, app install/launch/quit via `vexspoke` probes | 🟥 |
| 17.3 | Diagnostic Bug Catcher | Built-in crash reporter sending full scene snapshots to developer server | 🟥 |
| 17.4 | One-Click Mobile / Console Export | AOT C compiler exporting games to iOS, Android, and consoles | 🟥 |

### 18. Viewer3D, Object Turntable & Material Lab (`darling`)

Prebuilt Darling panels for inspecting 3D assets.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 18.1 | `Viewer3D` Shell | Proposed orbit camera viewport; no app implementation | 🟥 |
| 18.2 | `Object3D` Turntable Node | Proposed turntable; no app implementation | 🟥 |
| 18.3 | `MaterialPanel` Lab | Proposed material controls; no app implementation | 🟥 |
| 18.4 | `VideoPanel` Viewer | Proposed video viewer; no app implementation | 🟥 |

---

## Strategic Implementation Priorities for Anti

1. **P0: Viewport & Turntable Foundations**
   - Implement `minimal_lit` and `floor_grid` shaders in `graphvex` to unblock `Viewer3D` and `Object3D`.
   - Build orbit camera navigation controls inside `Viewer3D`.

2. **P1: 5-Column Studio Layout Construction**
   - Assemble the 5-column editor layout using Darling containers (`SplitContainer`, `TreePanel`, `TabPanel`).
   - Implement the right-hand dynamic inspector switching between Game, Scene, and Object properties.

3. **P2: Relational DOD Entity Core**
   - Implement `{pool_id, pool_index}` pointer buses using `vexspoke` memory arenas and bitpools.
   - Connect Darkbase native database to store scene graphs.

4. **P3: Reversible Physics Scrubber**
   - Build fixed-timestep physics simulation with state recording ring buffer and timeline scrubber.

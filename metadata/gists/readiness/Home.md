# Vexgraph Ecosystem — Master Roadmap & Feature Readiness Matrix

> **Canonical feature readiness matrix (Gist).** The retired `ecosystem/ecosystem` wiki is no longer maintained.
> Live inventory of the C23/Rust ecosystem. Updated same-cycle as code (the Living Documentation Law).
> Companion open-work backlog: [ecosystem blockers Gist](https://gist.github.com/vex-graph/e921fa188eebbd0c68c4e59646109887).
> *"4,000 mini-achievements is better than 100 impossible ones."*

> **This ecosystem is unfinished.** Repositories include implemented slices,
> partial foundations, drafts and source-free blueprints. **R5 apps and R6 superapps
> are not finished products**: agent client, DAW, studios and composed creative/IDE
> workflows remain incomplete.
> Feature names, design targets and architecture roles are not shipped behavior.
> Existing status rows are granular claims, not blanket repository certification;
> current executed evidence lives in `../test-checklist.md`. Untested, stale or
> missing proof remains a gap. No visual acceptance is implied.

---

## Status Legend

| Emoji | Label | Meaning |
|:---:|-------|---------|
| 💚 | **98% Done** | Basically 98% done, production-ready, fully wired, compiles, runs, actively polished |
| 🟩 | **95% Done** | Implemented & functional, wired, compiles and runs, minor polish remaining |
| 🟨 | **85% Done** | Substantially implemented, missing specific features/edge cases/painters |
| 🟧 | **75% Done** | Partial implementation, core struct exists, major features missing or unwired |
| 🟥 | **Concept / Draft** | Still a concept or spec'd in docs/headers, zero working source |
| ⬜ | **Vital Future Work** | Not implemented yet but very vital in the future, a plus one on the feature |

---

## Architecture Tiers (R1–R6 Runtime Hierarchy)

| Tier | Name | Role & Scope | Core Subsystems |
|:---:|---|---|---|
| **R1** | **Host** | Supervisor, Kernel, registries, OS windows, dynamic hot-loader; lifetime/residency owner | [hotcwap](#file-hotcwap-md) |
| **R2** | **Computation + Storage** | Vexspoke: CPU computation/behavior. Relational Engine: memory/storage, stable rows, bindings, native C search | [vexspoke](#file-vexspoke-md), [relational-engine](#file-relational-engine-md) |
| **R3** | **Driver** | Hardware GPU compute, native audio device/DSP, network connectors, AST grammars, native vex entity store | [graphvex](#file-graphvex-md), [samplerate](#file-samplerate-md), [api-haven](#file-api-haven-md), [language](#file-language-md), [darkbase](#file-darkbase-md) |
| **R4** | **Interfaces** | Widget interfaces, layout, input/focus, host bridges, session collaboration; graphics composition is R3 | [darling](#file-darling-md), [sesh](#file-sesh-md) |
| **R5** | **Interactables** | End-user interactive applications and creative studios | [primeagen](#file-primeagen-md), [impedance](#file-impedance-md), [darling-editor](#file-darling-editor-md), [drawling](#file-drawling-md) |
| **R6** | **Superapps** | Compose R1–R5 public contracts and registered app-level workflows without absorbing their implementations | [semicolon](#file-semicolon-md), [anti](#file-anti-md) |

---

## Ecosystem Repositories Index

R2 responsibilities are split, not automatically migrated. Existing Vexspoke
memory/container ABI and its default allocator remain until explicit migration
and owner proof. R3 may borrow either R2 public contract. R1 keeps storage/code
resident until active users stop; no C/Rust atomic-layout compatibility or
automatic record-schema migration is assumed. GPU shaders/dispatch stay Graphvex.

| Repository | Tier | Production Standard & Architectural Scope | Detailed Checklist |
|---|:---:|---|:---:|
| **hotcwap** | **R1 Host** | **Dynamic Application Host & Supervisor**: 12 subsystems, 112 mini-achievements (arenas, dylib reloader, decoupled windowing, process taxonomy) | [hotcwap](#file-hotcwap-md) |
| **vexspoke** | **R2 Computation / Behavior** | CPU computation, math, algorithms, synchronization and behavior; existing storage/container ABI retained during staged migration | [vexspoke](#file-vexspoke-md) |
| **relational-engine** | **R2 Memory / Storage** | Rust-owned allocation, stable row chunks and variable bindings; native C search over borrowed spans. Partial backend, not an allocator replacement or completed engine | [relational-engine](#file-relational-engine-md) |
| **graphvex** | **R3 Driver** | **The Modern Bindless GPU Driver**: 15 subsystems, 80+ mini-achievements (off-heap rasters, SDF font compute, meshlets, Vulkan/IOSurface) | [graphvex](#file-graphvex-md) |
| **api-haven** | **R3 Driver** | **Universal Connector & AI Switchboard**: 260+ AI providers, 25 DB catalogs, 12 blessed assets, 10 subsystems, 65+ mini-achievements (MCP stdio server, OpenAI/Anthropic/Gemini envelopes, incremental SSE, Discord/Slack webhooks) | [api-haven](#file-api-haven-md) |
| **language** | **R3 Driver** | **Relational AST & Grammar Matrix**: 30+ hot-swappable grammars, 10 subsystems, 55+ mini-achievements (L3 module ABI, zero-alloc lexer, relational AST nodes, highlighter bridge, LSP JSON-RPC client, bootstrap trio) | [language](#file-language-md) |
| **darkbase** | **R3 Driver** | **Native Vex Entity Store** over R2 reflection: in-memory Database and legacy snapshot compatibility; separate single-file page Store with embedded redo, reopen/repair and free-page reuse, proved by scoped optimized/C-sanitizer owners. Relational Database/Headless integration, catalog/indexes and journal recycling remain unfinished; no blanket production-readiness claim | [darkbase](#file-darkbase-md) |
| **samplerate** | **R3 Driver** | **Low-Latency Native Audio Driver**: 10 subsystems, 60+ mini-achievements (lock-free mixer, Vulkan compute shader DSP, hot DSP modules, 3D HRTF acoustics, CoreAudio bridge) | [samplerate](#file-samplerate-md) |
| **darling** | **R4 Interface** | **Retained UI Toolkit & Layer Compositor in C23**: 107+ components & granular feature matrix | [darling](#file-darling-md) |
| **sesh** | **R4 Interface** | **Multiplayer Session & Telemetry Relay**: 10 subsystems, 50+ mini-achievements (zero-alloc session records, 120Hz remote cursors, canvas sync, C relay daemon `seshd`, bug snapshot ingestion, Cloudflare edge) | [sesh](#file-sesh-md) |
| **determinant** | **R3 Terminal Toolkit** | Terminal-cell rendering, reusable widgets, CLI parsing and caller-fed input; resident terminal state with replaceable callbacks. Foundation scope, not Primeagen reload proof | [determinant](#file-determinant-md) |
| **harness** | **R4 Interface** | Draft agent-interface values; agent/provider/UI integration remains unfinished | [harness](#file-harness-md) |
| **primeagen** | **Standalone R5** | Personal agent client; future Semicolon inclusion is a consumer seam, not a reverse dependency | [primeagen](#file-primeagen-md) |
| **semicolon** | **R6 Superapp** | IDE workflow blueprint composing Language, bounded b tooling and future independent Primeagen integration; unfinished | [semicolon](#file-semicolon-md) |
| **impedance** | **R5 Interactable** | **GPU/CPU Hybrid Digital Audio Workstation**: 6 subsystems, 25+ mini-achievements (multi-track mixer, voice allocation, piano keys, DJ turntable scratching, CoreAudio AudioUnit HAL streaming, zero-redownload asset cache) | [impedance](#file-impedance-md) |
| **darling-editor** | **R5 Interactable** | **Spatial Canvas for Layouts, Diagrams & Prototypes**: 11 subsystems, 60+ mini-achievements (Auto-layout engine, spatial board, mindmaps, C23/HTML/SVG exporters) | [darling-editor](#file-darling-editor-md) |
| **drawling** | **R5 Interactable** | **Fluid Drawing & 2D Frame Animation in C23**: 10 subsystems, 60+ mini-achievements (sub-8ms input loop, layered compositor, brush dynamics, 2D animation, onion skinning) | [drawling](#file-drawling-md) |
| **anti** | **R6 Superapp** | Creative workflow blueprint composing IDE, DAW, drawing and game tooling; unfinished | [anti](#file-anti-md) |

# hotcwap — Host Supervisor Kernel & Platform Foundation

## Current cold-update assessment (2026-10-12)

The historical readiness percentages/timing/safety assertions below are not
current certification. Current scoped proof for this cycle is the following;
untouched subsystem claims require their own source review and executed owners.

| Feature | Status | Scope / proof / gaps |
| :--- | :---: | :--- |
| Explicit cold library update | 🟧 | `Hot_updateCold`: caller excludes every module user, complete mounted section set plus trusted SHA256 references, all private copies verified before constructors, trusted `Hot_cold_abi`/export admission, synchronous save and candidate-only restore, detected disk undo and recovery-required latch. `tests/hotcwap/hot/cold_update_test.{c,py}`: real two-section 20-update state-preserving swaps, checksum/ABI/restore rejection, promotion stamp-failure undo and retry. Host ASan/UBSan, module UBSan; Apple fully-ASan module reload crashes in sanitizer global registration. No signatures, hostile-parent sandbox, crash journal, all-stage injection, leaks or other-platform proof. Legacy poll-aged retirement is a distinct contract. |
| Growable symbol dispatch | 🟧 | `hot/hot_trampoline.{c,h}`: cold doubling/reuse, reader exclusion for backing relocation, exact symbol identity, count published after initialization, one diagnostic/count per refusal epoch. `../../../tests/hotcwap/hot/hot_trampoline_test.c`: 4096 symbols, 10000 replacements, extent refusal/preservation/reset/recovery and bounded projections; strict/ASan-UBSan. Atomics do not pin code; allocation-failure injection, legal concurrent publication and full pressure coverage remain gaps. |
| Terminal-application kind (CommandLine) | 🟧 | `kernel/commandline.{c,h}` + `kernel/commandline_ncurses.c`: the fourth process kind — owns the TTY (raw mode, alt screen, one cell grid), the ALWAYS-honored resize surface (`CommandLine_revalidate` grows the grid and repaints in one step), bounded normalized input, a single present flush and a swappable `CommandLineApp` seam that never re-acquires the device. Registered in `Kernel` alongside processes/applications/consoles. `../../../tests/hotcwap/kernel/commandline_test.c` drives a fake `CommandLineIo` headlessly (arity, open/close, resize growth/refusal, app swap/rejection-preservation, poll, projections, Kernel registration). No physical TTY, ncurses appearance, physical input, or live Primeagen reload is proven here. |

Primeagen consumes this boundary for terminal view/command updates; it does not
complete agent roles, tools, live remote policy proof or whole-runtime migration.

> **R2 lifetime contract:** [vexspoke](#file-vexspoke-md) owns CPU computation/behavior;
> [relational-engine](#file-relational-engine-md) owns memory/storage, stable rows, variable bindings and
> native C search. R1 owns code/storage residency and excludes active users before
> destruction. Existing Lifetime wiring, Vexspoke memory/container ABI and default
> allocator remain during staged migration. No direct engine-header dependency,
> live engine reload integration, automatic schema migration or C/Rust atomic
> layout equivalence is implied. GPU shaders/dispatch remain [graphvex](#file-graphvex-md).

> R1 Host. Boots first, tears down last (the Vertical Integration Law).
> Bounded joins obey the Bounded Wait Law; top-down teardown obeys the Vertical Integration Law (Teardown).

---

## 🎯 Tier-0 Integration Proofs (Ground Truth)

*The live binary is the final judge. This table gates the repo headline — never the rows below, which keep their own independent truth. Statuses are re-verified, never copied from memory.*

| Proof Binary | End-to-End User Verification | Status | Evidence |
|---|---|:---:|---|
| `vk_test` (`../../_trash/main/test_suite.c`, umbrella root) | Boot Kernel → app × window → present probe frame via graphvex present chain | 🟩 | Wired target linking `hotcwap`; the only end-to-end probe by decision (single-harness doctrine — no gallery, no parallel demos; coverage grows inside `test_suite.c`) |
| `_tests/hotcwap/` + `../../../tests` headless suite | `spoke_test` + `window_event_test` + `window_test` wired; `bridge_seam_test` in-repo and proven 8/8; manifest smoke 42/42 (JSON catalog + per-library ladder); manifest rollback PASS | 🟩 | Bridge seam, window events, lifetime memory, manifest hot reload, and rollback all verified green |

## Production Readiness Verdict (2026-09-16 sweep)

macOS host trail: **106/111 green (95.5%)** — the denominator excludes the
4-row platform appendix (#12), which tracks ports, not host readiness.
Counts: every lib translation unit (all 10 `.c` + `window_cocoa.m` under ARC)
compiles `-Wall -Wextra -Werror`, zero `TODO`/`FIXME`, zero `../../..` includes
(the Canonical Include Paths Law), zero hot-path allocation, zero global
listener tables. Proven by direct compile & run: `window_event_test` PASS,
`bridge_seam_test` 8/8 PASS (in-repo), manifest smoke 42/42 PASS,
`manifest_hot_test` PASS, `manifest_rollback_test` PASS, `spoke_test` PASS,
`window_test` + `vk_test` compile cleanly under C23.

This sweep caught hotcwap RED and fixed two build breaks: `application.c` included phantom `io/vfs.h` and called darling-owned `Vfs_init()` (a Vertical Integration Law violation — R1 reaching into R4; the VFS boots itself in darling, `System_initializeAll()` covers the R1 side), and `kernel.c` failed on a `VexspokeApi` vs `VexspokeAPI` typedef mismatch (canonical casing restored per the Single Class Per File Law). Also fixed this cycle: `console.c` fn-table hops spelled `(*io).` (the No Arrow Sugar Law wording, now the Semantic Consistency Law (Reference form)), `hot_behavior` texture path made asset-relative, host-tier wording, `process/` tree and `test_suite` harness names across README/overviews, and the `objc/` → `window/` move completed (`objc/window_cocoa.m` deleted).

Known limitations (honest 🟧/🟥, not hidden):
- Single-harness doctrine, enforced: `../../_trash/main/test_suite.c` (`vk_test`) is the only end-to-end probe. The stale `_tests/hotcwap/enginetest.c` demo is deleted, the disabled `darling_gallery` block is removed from the umbrella build — multi-app hot-swap coverage grows inside `test_suite.c` incrementally, never as a second harness.
- Platform drafts: `window/window_win32.c` (Win32, WIN32 default) and `window/window_wayland.c` (Wayland, `-DHOTCWAP_USE_WAYLAND=ON`) are complete 1:1 cocoa mirrors but `;;DRAFT` — they have never compiled on a real host, and the macOS trail deliberately excludes them (platform-guarded build). `window.c`/`window_linux.c` remain the safe-default fallbacks — macOS is the production platform.
- Standalone builds need `-DHOTCWAP_USE_VEXSPOKE=ON` (or the umbrella include path): `spoke/lifetime.c` and `window/window.h` include `event/*` headers owned by vexspoke R2, and hotcwap ships no local `event/` dir.
- `APP_MODE_TUI` is partial (🟨); state save/restore works, schema migration is manual, #8.5 automated rollback lands with `manifest_rollback_test`.

## The Hotcwap Standard: The Zero-Downtime Nano-VM

Hotcwap is not a conventional monolithic game loop or simple window wrapper. It is an **R1 Host Nano-VM** inspired by Erlang/OTP fault tolerance and dynamic systems, designed to make crashes impossible to propagate to the OS window:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             THE HOTCWAP STANDARD                                 │
├─────────────────────────┬─────────────────────────┬──────────────────────────────┤
│ 1. OS Window Decoupling │ 2. Microsecond Reloader │ 3. Multi-Layer Compositor    │
│ • Thread 0 owns NSWindow│ • Sub-ms dylib swap     │ • Native CALayer / IOSurface │
│ • Window outlives code  │ • ABI version frozen    │ • Zero-copy Vulkan swapchain │
│ • 1000Hz raw event pump │ • Trampoline dispatch   │ • Live resize without drag   │
│ • Zero flicker on reload│ • Deferred retirement   │   stalls (sync render hook)  │
├─────────────────────────┴─────────────────────────┴──────────────────────────────┤
│ 4. Erlang-Grade Process Supervision & memory Isolation                           │
│ • Master session arena + transient per-tick scratch arena (Teardown Order)      │
│ • State handoff blobs: save → swap → restore → schema migrate                    │
│ • Bounded thread timeouts (100ms hard cap, Bounded Wait drop-degrade)            │
│ • Multi-application multiplexing (N apps × M windows per process)                │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## Status Legend & Grading Standards

Every subsystem and micro-achievement is strictly graded based on the current reality of the codebase, test suites, and live runtime behavior:

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
| 1 | `Kernel Supervisor` | Opaque provider-attested arenas via spoke table, multi-app registry, completion reactor `Kernel_runAll` (terminal-run contract, no Kernel tick) | 🟩 |
| 2 | `Process Taxonomy` | `kernel/` trio: one-shot Process, windowed Application (CLI/TUI/GUI), session Console; telemetry (FPS/frametime), window list | 🟩 |
| 3 | `Native Windowing Core` | Pure-AppKit window backend (`window/window_cocoa.m`, zero Vulkan/Metal), geometry, display topology, focus/monitor/size mirroring | 🟩 |
| 4 | `Window Chrome & Vibrancy` | Borderless, naked titlebar, opacity, blur (NSVisualEffectView), transparency ticket, centered-on-main-monitor by default, macOS traffic-light API (per-button visibility + header position, public AppKit only) | 🟩 |
| 5 | `Event Pump & Adapters` | Key/Mouse/Touch adapter dispatch, per-window `WindowEvent` lifecycle registry (10 slots incl. occlusion demand), focus framing (`event/*` contracts owned by vexspoke R2) | 🟩 |
| 6 | `Compositor Migration Seam` | Live atomic slots + inert pixel contracts pinned by `bridge_seam_test` (docs/bridging.md) | 🟩 |
| 7 | `Dynamic Module Reloader` | dylib change detection, dlopen/dlsym swap, struct-contract trampolines, `MANIFEST(...)` install ladder + `manifest.json` library catalog (MODE-1 hot swap + MODE-2 cold-swap promote); older JSON `HotManifest` pixel gate retired | 🟩 |
| 8 | `State Handoff & Migration` | Save, restore, and schema migration of module state across swaps (manual migrate; #8.5 automated rollback on restore rejection) | 🟩 |
| 9 | `Live SPIR-V Reloader` | Owned by graphvex (`src/vulkan/spv_watch.c`) — hotcwap holds zero shader-watch code | 🟩 |
| 10 | `Vulkan Device Substrate` | Owned by graphvex — hotcwap holds no Vulkan code, no `vulkan/` dir, zero `Vk_*` calls (one seam comment in window.h marking the `VkPane` retirement) | 🟩 |
| 11 | `Teardown & Thread Safety` | 100ms bounded joins (the Bounded Wait Law), top-down teardown protocol (the Teardown Order Law) | 🟩 |
| 12 | `Cross-Platform Backends` | macOS live; Linux X11 fallback (`window_linux.c`) + Win32 (`window_win32.c`, legacy `window.c` stub) + Wayland (`window_wayland.c`) lean drafts all wired, host-compiles pending, headless future | 🟧 |

---

## Detailed Mini-Achievements Breakdown

### 1. Kernel Supervisor & Arena Lifecycle (`kernel/`)

The master supervisor process owning memory lifecycles and application multiplexing.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 1.1 | Sized Master Arena Allocation | `Kernel_create` allocates isolated 64MB master session arena | 🟩 |
| 1.2 | Per-Tick Transient Scratch Arena | 64MB transient scratch arena reset every frame, never freed mid-frame | 🟩 |
| 1.3 | Overloaded Constructor Dispatch | `Kernel()`, `Kernel(masterBytes)`, `Kernel(masterBytes, transBytes)` | 🟩 |
| 1.4 | Multi-Application Registration | Up to 8 concurrent `Application` slots (`KERNEL_MAX_APPS`) | 🟩 |
| 1.5 | Swap-Remove App Unregistration | Unregistering applications via fast swap-remove preserving slot bounds | 🟩 |
| 1.6 | Completion-Reactor Run | `Kernel_run(k)` / `Kernel_runAll()` — arm → dispatch by kind → supervise until ALL kinds finish (no tick, no pump thread) | 🟩 |
| 1.7 | Per-Kind Dispatch Forwarding | `Kernel_runProcess` → `Process_run`, `Kernel_runConsole` → `Console_run`, `Kernel_runApplication` → graphvex `GfxLoop` attach | 🟩 |
| 1.8 | Atomic Supervisor Active Flag | `_Atomic bool running` allowing cross-thread shutdown signaling | 🟩 |
| 1.9 | Symmetric Arena Getters | `Kernel_getArena()`, `Kernel_getTransientArena()` (the Symmetric Getter/Setter Completeness Law) | 🟩 |
| 1.10 | Top-Down Teardown Execution | Stops apps, drains workers, frees transient arena, destroys master last | 💚 |

### 2. Process Taxonomy & Execution Modes (`kernel/`)

Executable identity, window registry, and operational mode orchestrator.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 2.1 | Fixed-Storage Identity Metadata | Name (64B), Author (64B), Version (16B), IconPath (512B) with zero malloc | 🟩 |
| 2.2 | Overloaded Identity Constructors | `Application()`, `Application(name)`, `Application(name, author, ver)` | 🟩 |
| 2.3 | Multi-Window Registry Table | Fixed table of up to 16 top-level `Window*` slots (`APP_MAX_WINDOWS`) | 🟩 |
| 2.4 | Window Registration & Query API | `Application_addWindow()`, `removeWindow()`, `getWindow()`, `getWindowCount()` | 🟩 |
| 2.5 | Auto-Detection Execution Mode | `APP_MODE_AUTO` auto-switching to GUI if windows exist, CLI if 0 windows | 🟩 |
| 2.6 | Headless CLI Execution Mode | `APP_MODE_CLI` for command-line tools and daemons without graphics overhead | 🟩 |
| 2.7 | Interactive TUI Console Mode | `APP_MODE_TUI` for terminal user interfaces | 🟨 |
| 2.8 | Windowed GUI Mode | `APP_MODE_GUI` — windowed apps attach into graphvex's `GfxLoop` (hotcwap launches no swapchain/worker itself) | 🟩 |
| 2.9 | Custom Run Handler Override | `Application_setRunHandler(fn, userdata)` for specialized loop control | 🟩 |
| 2.10 | Per-Frame Tick Callback | `Application_onTick(fn, userdata)` firing each simulation cycle | 🟩 |
| 2.11 | Hot-Reload Event Callback | `Application_onHotReload(fn, userdata)` notified when dylibs are swapped | 🟩 |
| 2.12 | Live Telemetry Counters | Thread-safe atomic FPS and frametime in microseconds (`frametimeUs`) | 🟩 |
| 2.13 | Detach-Only Free Contract | `Application_free()` destroys runtime struct; leaves OS windows untouched | 🟩 |

### 3. Native OS Windowing Core (`window/window_cocoa.m`)

Platform-agnostic window abstraction with native macOS AppKit/Cocoa implementation.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 3.1 | Parameterized `WindowDesc` Builder | Title, width, height, x, y, centered, shown options with sensible defaults | 🟩 |
| 3.2 | Overloaded Window Constructors | `Window()`, `Window(title)`, `Window(title, w, h)`, `Window_new(&desc)` | 🟩 |
| 3.3 | Hidden Construction Contract | Windows construct hidden by default; show explicitly via `Window_show()` | 🟩 |
| 3.4 | OS Close Request Mirroring | `Window_shouldClose()` tracking red traffic light / Cmd+W requests | 🟩 |
| 3.5 | Global Desktop Location Mapping | `Window_setLocation()`, `Window_getLocation()` in global screen points | 🟩 |
| 3.6 | Content Area Origin Resolution | `Window_getContentOrigin()` returning top-left below titlebar chrome | 🟩 |
| 3.7 | Screen Centering Utility | `Window_center()` centering window across active display bounds | 🟩 |
| 3.8 | Size Clamping Constraints | `Window_setMinSize()`, `Window_setMaxSize()` enforcing resize limits | 🟩 |
| 3.9 | Window Spotlight Focus Tracking | `Window_focus()`, `Window_isFocused()`, atomic key window ID tracking; `Window_setKeyEnabled()` key gate (Cocoa `canBecomeKeyWindow` refusal for modal-held parents) | 🟩 |
| 3.10 | Multi-Monitor Screen Identity | `Window_getMonitorId()` tracking `CGDirectDisplayID` with hand-off events | 🟩 |
| 3.11 | Native Spaces Fullscreen | `Window_setFullscreen()`, `toggleFullscreen()` using macOS Spaces | 🟩 |
| 3.12 | Window Minimization | `Window_minimize()`, `restore()`, `isMinimized()` | 🟩 |
| 3.13 | DRM / Screen Capture Protection | `Window_setDRM()` hiding window contents from screen capture tools | 🟩 |
| 3.14 | Cursor Style Switching | Default, I-Beam, Pointing Hand, Crosshair, Resize EW/NS, Not-Allowed, Hidden | 🟩 |
| 3.15 | FPS Cursor Lock & Re-Warp | `Window_setCursorLocked()` hides cursor and re-warps to center for FPS games | 🟩 |

### 4. Window Chrome, Vibrancy & Visual Styling (`window/window_cocoa.m`)

Custom titlebar styling, transparency, and macOS visual effects.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 4.1 | Standard Decorated Chrome | `WINDOW_DECORATED`: native opaque titlebar with window title | 🟩 |
| 4.2 | Borderless Undecorated Chrome | `WINDOW_UNDECORATED_BORDERLESS`: completely borderless window frame | 🟩 |
| 4.3 | Naked Titlebar Chrome | `WINDOW_UNDECORATED_NAKED`: transparent titlebar, hidden title, traffic lights kept | 🟩 |
| 4.4 | Floating Traffic Lights | `Window_setFloatingTrafficLights()` overlaying traffic lights directly over UI | 🟩 |
| 4.5 | Chrome Capability Toggles | Selectively toggle Resizable, Closable, Miniaturizable, Fullscreen buttons | 🟩 |
| 4.6 | Window Surface Opacity | `Window_setOpacity(float)` controlling overall window transparency | 🟩 |
| 4.7 | Clear Background for Vulkan Holes | `Window_setTransparentBackground()` clearing window backdrop for GPU quads | 🟩 |
| 4.8 | Native Frosted Glass Vibrancy | `Window_setBlur()` adding `NSVisualEffectView` frosted glass behind UI | 🟩 |
| 4.9 | Always-On-Top Floating Level | `Window_setAlwaysOnTop()` elevating window to floating utility level | 🟩 |
| 4.10 | Click-Through Transparent HUD | `Window_setClickThrough()` ignoring pointer clicks for transparent overlays | 🟩 |
| 4.11 | Movable by Background Click | `Window_setMovableByBackground()` dragging window by clicking empty canvas | 🟩 |
| 4.12 | Window Shadow Toggle | `Window_setShadow(bool)` toggling OS drop shadow | 🟩 |
| 4.13 | Non-Focus Stealing Bring-To-Front | `Window_bringToFront()` raising window without stealing keyboard focus; `Window_attachChild()`/`detachChild()` pair glue (Cocoa child windows, parity no-ops elsewhere) | 🟩 |

### 5. Event Pump & Device Adapters (`window/`, vexspoke `event/` contracts)

Ultra-low-latency 1000Hz input event capture and dispatch pipeline.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 5.1 | OS Event Queue Drain | `Window_pollEvents()` pumping native AppKit/Cocoa event queue on Thread 0 | 🟩 |
| 5.2 | Decoupled Ring Buffer Delivery | Raw keyboard, mouse, and touch events buffered in lock-free device rings | 🟩 |
| 5.3 | Window-Scoped Event Dispatch | `Window_dispatchEvents()` draining rings to adapters attached to this window | 🟩 |
| 5.4 | Keyboard Adapter Interface | `Window_addKeyAdapter()`, `removeKeyAdapter()` with `KeyHandler` vtables | 🟩 |
| 5.5 | Mouse Adapter Interface | `Window_addMouseAdapter()`, `removeMouseAdapter()` with `MouseHandler` vtables | 🟩 |
| 5.6 | Multitouch Trackpad Adapter | `Window_addTouchAdapter()`, `removeTouchAdapter()` with `TouchHandler` | 🟩 |
| 5.7 | Window Lifecycle Adapter | `WindowEvent` dispatching close, focus, resize, move, monitor change, and occlusion demand (10 slots via `Window_getLifecycle`) | 🟩 |
| 5.8 | Input Killswitch Gate | `Window_setEnabled(false)` silencing all input delivery to adapters | 🟩 |
| 5.9 | Adapter Dispatch Proof | `window_event_test` PASS (registry fire/dispatch) + `window_test.c` compiles (native queue → per-window adapter path) — no gallery, the bridge is the harness | 🟩 |
| 5.10 | Window-Scoped Routing Isolation | Adapters attach by window id (`Key_attachWindow(id, …)`); zero global listener tables in the backend — verified by grep | 🟩 |

### 6. Compositing Seam: Live Registry + Inert Present (`window/`)

Panel slots and present policy are live atomic state on the cocoa backend; every function that would touch pixels is an inert `;;INTENTION` stub (no IOSurface, no Metal, no swapchain in hotcwap — the render repos own pixels).

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 6.1 | Single Root Container Slot | `Window_setContainer()` / `getContainer()` — live atomic store/load of the master panel root | 🟩 |
| 6.2 | Content/Scene Panel Slots | `Window_setContentPanel()` / `setScenePanel()` (+ getters) — live atomic stores, zero compositing | 🟩 |
| 6.3 | Inert Pane-Seam Slot Contract | `attach/resize` → `false`, `composite*` no-op — retained as no-op seams for the migrating darling compositor (the Single-Seam Canvas Law: the render repo owns the seam pass); pinned by `bridge_seam_test` 8/8 | 🟩 |
| 6.4 | Worker Present Contract | `Begin/End` no-op — no layer, nothing to commit; pinned by `bridge_seam_test` | 🟩 |
| 6.5 | Metal/Gravity Contract | `metalLayer` → `nullptr`, gravity no-op — by design; pinned by `bridge_seam_test` | 🟩 |
| 6.6 | Present Pacing Policy | `WINDOW_PRESENT_FIFO` (vsync) vs `WINDOW_PRESENT_IMMEDIATE` (uncapped) — live stored policy | 🟩 |
| 6.7 | Swapchain Transparency Policy | `Window_setTransparent()` / `isTransparent()` — live stored policy consumed by graphvex | 🟩 |
| 6.8 | Monotonic Render Generation | `Window_renderGeneration()` / `sizeGeneration()` — live generation counters for GPU consumers | 🟩 |
| 6.9 | Live-Resize State Mirror | `Window_isLiveResizing()` — live atomic mirror of NSView live-resize notifications; hotcwap freezes nothing with it (continuous-present policy is the consumer's job, the Continuous Real-Time Live Resize Law) | 🟩 |
| 6.10 | In-Drag Synchronous Render Hook | `Window_setResizeRenderHook()` — live stored hook slot for the consumer's sync render | 🟩 |
| 6.11 | Content View Anchor | `Window_contentView()` — live AppKit view handle GPU backends layer onto | 🟩 |
| 6.12 | Present Contract | `Window_present` → `false` — no raster target on a pure AppKit window; pinned by `bridge_seam_test` | 🟩 |

### 7. Dynamic Module Hot-Reloader & ABI Trampoline Ring (`hot/`)

Microsecond code hot-swapping without process restart.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 7.1 | Directory Hot-Watcher | `Hot_init("hot/")` monitoring filesystem directories for new dylib builds | 🟩 |
| 7.2 | Non-Blocking Poll Tick | `Hot_poll()` checking file timestamps and returning reloaded module count | 🟩 |
| 7.3 | ABI & Version Hash Verification | Validating exported module hashes before loading to prevent ABI mismatch crashes | 🟩 |
| 7.4 | Zero-Overhead Function Trampolines | Atomic function pointer swapping redirecting calls to new module instances | 🟩 |
| 7.5 | Dynamic Symbol Lookup | `Hot_get_symbol()` and `Hot_get_api()` resolving stable function tables | 🟩 |
| 7.6 | Safe Deferred Retirement Ring | Staging old dylib handles in a retirement ring to finish in-flight GPU frames | 🟩 |
| 7.7 | Module Lifecycle Hooks | Triggering `Hot_init_module` and `Hot_shutdown_module` exports | 🟩 |
| 7.8 | Hot Manifest Parser | `hot/manifest.c` reading module descriptions and entry-point lists, plus provider-owned consumer allow-list (`consumers[]`, `HotManifest_allows` gate) — **retired this cycle**: the JSON `Hot_manifest`/`HotManifest` parser is dead code, deleted with its test | ⬜ |
| 7.9 | Build Staging Synchronizer | `hot/stage.c` synchronizing compiler build outputs with runtime hot directories — **retired this cycle**: `HotStage_verify` was the old JSON/stage gate; vexspoke now drops payloads straight into `bin/new` and calls `MANIFEST_UPDATE()` | ⬜ |
| 7.10 | Diagnostic Error Tracking | `Hot_last_error()` capturing dlopen, dlsym, and ABI error strings | 🟩 |
| 7.11 | MANIFEST Install-Layout Authority | `hot/manifest.{h,c}` — the "manifest binary way": per-app ladder + `manifest.json` catalog. One-shot `MANIFEST(kind, org, app)` (second call fails) resolving `<app-data>/<org>/<app>`, `APPLICATION_PATH` per-platform defines + `$VEX_MANIFEST` test seam, ladder `bin/{backward,previous,current,new}` + `hot/` + `cache/`, the `HOT_MANIFEST_MAX_NAME`/`HOT_MANIFEST_MAX_EXPORTS` trampoline constants, plus `HOT_MANIFEST_MAX_LIBRARIES`/`HOT_MANIFEST_MAX_SECTIONS`. Self-contained bounded JSON reader/writer keeps R1 in its allowlist | 🟩 |
| 7.12 | First-Run Reflection | `MANIFEST_REFLECT(library, sourceDir)` seeds a library's section list in `manifest.json` from its bundled payload (dylib stems), copies the payload into `bin/current/<library>` (temp + atomic rename), and drops the per-library `.install-mark` fingerprint; `MANIFEST_IS_FIRST_RUN` gates the install | 🟩 |
| 7.13 | MODE-2 Cold-Swap Promote | `MANIFEST_LIBRARY(...)` registers library KEYS (empty section lists — the downloader owns the arrays); `MANIFEST_UPDATE(library, payloadDir)` fail-closes any undeclared payload entry, then stages `bin/new/<library>` (never promotes alone); `MANIFEST_PROMOTE` slides PER-LIBRARY renames `previous→backward`, `current→previous`, `new→current` (no staged set = pinned). Smoke 42/42 | 🟨 |

### 8. State Preservation & Versioned Schema Migration (`hot/`)

Preserving live state across dynamic library reloads.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 8.1 | State Serialization Extraction | `Hot_save_module()` extracting opaque state blob from old module prior to swap into 16-byte aligned buffer; proven by `manifest_hot_test` | 🟩 |
| 8.2 | State Restoration Handoff | `Hot_restore_module()` reinjecting state blob into new module instance in Phase B before commit; proven by `manifest_hot_test` & `manifest_rollback_test` | 🟩 |
| 8.3 | Versioned Schema Migration | `Hot_migrate_module()` transforming oldVersion state blobs into new schemas + automatic `Hot_migrate` fallback during `perform_swap()` | 🟩 |
| 8.4 | In-memory Struct Reflection | Planned R2 storage schema migration; `Lifetime.relational` alone proves no migration, rollback or live engine reload integration | 🟧 |
| 8.5 | Automated State Rollback | Restore-before-commit: a `Hot_restore` rejection (or missing restore on a snapshotted section) reverts to the previous module generation — old code + state stay live, the stamp never advances, the next poll self-heals on a fixed promote. Proven by `tests: manifest_rollback_test` (foreign-magic gen-2 rejected twice, gen-1 state preserved, gen-3 heal) | 🟩 |

### 9. Live SPIR-V Shader Reloader (owned by graphvex)

Hot-reloading compiled Vulkan SPIR-V shaders lives in graphvex (`src/vulkan/spv_watch.c`) with zero runtime stutter. hotcwap holds zero shader-watch code — the rows below are the graphvex-owned contract this repo used to carry:

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 9.1 | SPIR-V Directory Watcher | graphvex `src/vulkan/spv_watch.c` — zero watch code in hotcwap | 🟩 |
| 9.2 | Shader Modification Polling | graphvex-owned nanosecond mtime detection | 🟩 |
| 9.3 | Pipeline Invalidation Notification | graphvex-owned reload callbacks | 🟩 |
| 9.4 | Vulkan Pipeline Cache Swap | graphvex-owned `VkPipeline` / `VkShaderModule` recreation | 🟩 |
| 9.5 | Built-in Core Shaders | Staged precompiled shaders (`hello_triangle`, `solid_quad`) via umbrella `${CMAKE_BINARY_DIR}/spv/` | 🟩 |

### 10. Vulkan Device Substrate & Retained Board Chains (owned by graphvex)

Hardware Vulkan runtime, the single seam canvas, and the retained board/compositor chains live in graphvex (darling consumes). hotcwap holds no `vulkan/` dir, no `vk_loader.c`, and zero `Vk_*` calls — the rows below are the graphvex-owned contract:

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 10.1 | Dynamic Vulkan GPA Loader | graphvex-owned — zero loader code in hotcwap | 🟩 |
| 10.2 | Hardware CAMetalLayer Binding | graphvex-owned — hotcwap exposes only the `Window_contentView()` anchor | 🟩 |
| 10.3 | Physical Device Selection | graphvex-owned — zero device code in hotcwap | 🟩 |
| 10.4 | Logical Device & Queue Families | graphvex-owned — zero queue code in hotcwap | 🟩 |
| 10.5 | Dedicated `VkPane` Swapchains | **RETIRED** — the pane-era per-scene `CAMetalLayer` + `VkPane` swapchain path is deleted from graphvex (zero `VkPane_*` calls anywhere); hotcwap's seam comment marks the retirement, the single seam canvas hosts all boards | 🟩 |
| 10.6 | Vulkan Device Context Abstraction | graphvex-owned (`VkContext`) — hotcwap holds opaque handles only | 🟩 |
| 10.7 | Vulkan Pipeline State Module | graphvex-owned (`VkModule`) — zero pipeline code in hotcwap | 🟩 |
| 10.8 | Swapchain Rebuild on Extent Change | graphvex-owned — hotcwap publishes `renderGeneration`/`sizeGeneration`, never rebuilds | 🟩 |

### 11. Process Supervision, Teardown & Thread Safety

Deterministic shutdown order and multi-threaded synchronization laws.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 11.1 | Top-Down Teardown Protocol | Window → Compositor → Vulkan → Worker joins → Memory_freeAll (the Teardown Order Law) | 💚 |
| 11.2 | 100ms Bounded Thread Joins | Hard 100ms timeout on joining worker threads with drop-degrade (the Bounded Wait Law) | 💚 |
| 11.3 | Present Worker Thread Isolation | Present thread lives in graphvex, decoupled from Thread 0 event loop (the Window Decoupling Law) | 🟩 |
| 11.4 | Atomic Present Worker Coordination | Producer-consumer synchronization using atomic sequence counters (graphvex side) | 🟩 |
| 11.5 | Type Attestation Seam | No `hotcwap-type.h` registry file — attestation lives in `spoke/vexspoke.h` (`VEXSPOKE_TYPE_ARENA`) + manifest `type_ids[]`, proven by `spoke_test` | 🟨 |
| 11.6 | Single-Harness Doctrine | `test_suite.c` is the only probe — stale `enginetest.c` deleted, no parallel demo harnesses by decision | 🟩 |
| 11.7 | Headless & GUI Window Test Suite | `_tests/hotcwap/window_test.c` + `window_event_test.c` wired; green build run pending | 🟨 |

### 12. Cross-Platform Backends & Headless CI (platform appendix — outside the macOS denominator)

Expanding Hotcwap beyond macOS. These four rows track ports, not host
readiness: the macOS milestone counts 108/112 rows, and this appendix is
worked only when a non-macOS target is live. The 2026-09-16 cycle added
complete 1:1 cocoa-mirror lean drafts for both Win32 and Wayland plus their
Build wiring (platform-guarded); each still needs its own host to compile
and verify — the macOS trail never compiles them.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 12.1 | Linux X11 Window Backend | `window/window_linux.c` — `;;DRAFT`/`;;INCOMPLETE` stub, safe-default returns; the default Linux build when Wayland libs are absent or `-DHOTCWAP_USE_WAYLAND=OFF` | 🟧 |
| 12.2 | Linux Wayland Compositor Bridge | `window/window_wayland.c` — complete 1:1 cocoa mirror (xdg-shell, seat/keyboard/pointer/touch, retained wl_shm software present, id registry + output tracking); wired opt-in via `-DHOTCWAP_USE_WAYLAND=ON` (pkgconfig `wayland-client` + `xkbcommon`), auto-fallback to 12.1. `;;DRAFT` — compiled against zero real wayland headers yet; needs a Linux host to promote | 🟧 |
| 12.3 | Windows Win32 Window Backend | `window/window_win32.c` — complete 1:1 cocoa mirror (WndProc pump, USER32/GDI32 `StretchDIBits` software present, `WIN32_LEAN_AND_MEAN`, id registry); the WIN32 default with `window.c` kept as the legacy safe-default stub via `-DHOTCWAP_WIN32_LEGACY=ON` (links `user32 gdi32`). `;;DRAFT` — compiled against zero real win32 headers yet; needs a Windows host to promote | 🟧 |
| 12.4 | Headless Off-Screen Render Target | Virtual display surface for CI testing without physical display | ⬜ |

---

## Strategic Implementation Priorities for Hotcwap

1. **P0: Tier-0 Proof — Build Green on the Single Harness**
   - Run the full build + `vk_test` + all four `_tests/hotcwap/` suites green to promote Tier-0 to 🟩.
   - Grow `test_suite.c` incrementally (multi-app, hot-swap) — never a second harness.
   - Window-scoped adapter isolation over legacy global bridges (tracked in #5.9–5.10).

2. **P1: State Preservation & Schema Migration**
   - Solidify `Hot_save_module()` and `Hot_restore_module()` with automated struct serialization.
   - Add integration test proving live state preservation across dylib recompilation.

3. **P2: Linux Display Backend Completion**
   - Compile `window_wayland.c` on a real Linux host against `libwayland` + `xkbcommon`, fix findings, then promote #12.2 toward 🟨/🟩 — a `;DRAFT`-free parse is the first gate.
   - Bring `window_linux.c` (X11 fallback) from stub status to functional X11 window creation and input pump; verify `window_win32.c` the same way on a Windows host.

4. **P3: Headless CI Presentation Runner**
   - Enable automated headless Vulkan testing in continuous integration environments.

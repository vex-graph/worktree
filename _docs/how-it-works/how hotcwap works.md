# How hotcwap Works: The Host Supervisor

> The 2am README for R1 Host. If you forgot everything, read
> sections 1-3 and go back to sleep. If it's 2pm and you're adding a
> feature, read the API surface at the bottom.
> Answers the fundamental question: **"What owns the window and the
> Vulkan device?"**
> Answer: **hotcwap owns both. They survive dylib reloads.**

---

## 1. The Short Answer: A Thin Nano-VM

hotcwap is the process supervisor. It owns:
- The **Kernel** (master arena, transient arena, application registry)
- The **OS Window** (NSWindow via one ObjC file)
- The **Vulkan device** (created in the loader, survives reloads)
- The **hot-loader** (watches, verifies, swaps, retires dylibs)

Everything else — darling widgets, api-haven connectors, language
grammars, engines — lives in hot-swappable dylibs that the Kernel
supervises.

| Piece | What it is | Level | Role |
|---|---|---|---|
| `Kernel` | nano-VM | L4 | master session, app registry, present worker |
| `Application` | executable identity | L2 | name, version, windows, hot-loader, run loop |
| `Window` | OS window shim | L4 | 1 ObjC file, NSWindow + CAMetalLayer |
| `HotModule` | dynamic loader | L4 | watches, verifies, swaps, retires dylibs |
| `HotTrampolineTable` | atomic fn-ptr swap | L4 | 1024-row table, fallback covers mid-swap |
| `HotRetireRing` | generational dlclose | L4 | 4-poll grace period for in-flight calls |
| `Vulkan` | GPU chain setup | L4 | device, swapchain, present, blit |
| `VkLayer` (graphvex) | retained offscreen boards | L4 | scene/content boards + depth-1 children collaged into the single seam canvas |
| `VkLoader` | device owner | L4 | VkDevice persists across reloads |

---

## 2. Where It Sits (Read This Once)

```text
R1 hotcwap   — boots first, owns Kernel/Window, tears down last. WE ARE HERE.
R2 vexspoke  — arenas, net/http, threads, system probes (hotcwap includes this)
R3 graphvex  — GPU only (hotcwap includes this for Buffer/Font/Texture)
R4 darling   — UI toolkit (hotcwap registers windows, never includes darling)
R5 apps      — your IDE, your game (registered as opaque handles)
```

hotcwap is R1 — it boots first and tears down last. It includes
vexspoke (R2) and graphvex (R3) shapes only. It never includes
darling, api-haven, or any engine headers.

---

## 3. The 7-Step Lifecycle

```c
1. Kernel *k = Kernel();                    // master + transient arenas
2. Application *app = Application("vex");    // executable identity
3. Kernel_addApplication(k, app);            // register in the nano-VM
4. Window *w = Window();                     // OS-owned, never hot-updated
5. Application_addWindow(app, w);
6. Application_run(app);                     // GUI loop with present worker
7. Kernel_destroy(k);                        // stop → join → Vk_shutdown → arenas LAST
```

---

## 4. The Kernel (the nano-VM)

The Kernel owns two arenas:
- **Master arena** (64MB): everything allocated during the session
- **Transient arena** (64MB): per-tick scratch, reset every frame

`Kernel_tick` order per frame:
1. `MemoryArena_freeAll(transientArena)` FIRST
2. `Window_pollEvents()` + `Mouse_dispatchEvents()` + `Key_dispatchEvents()`
3. `KEY_ESCAPE` → stop
4. Poll `SpvWatch` per app (shader hot-reload)
5. Tick each running app (all closed → stop)
6. Presentation — owned by present worker if non-null

**Two-thread live-resize model:**
- **Thread 0**: OS event pump, AppKit live-resize tracking, window chrome mutations
- **Present worker**: `Vk_clearPresent()` on the single seam canvas every frame
  (the pane-era `VkPane_presentAll` walk is retired)

The present worker is bounded-joined via `Thread_stop` before teardown
(Rule 26/27). Never bare spin — fence-paced healthy, budget-paced
always, ≥2 consecutive failures → 8ms backoff.

---

## 5. The Window (the ONE Objective-C file)

`objc/window_cocoa.m` is the only `.m` file in the project. It exists
only to talk to AppKit. Everything above this boundary stays C.

**Only two NSViews in the entire application:**
1. `AntiContentView` — intercepts OS events, pushes into C23 input rings
2. `AntiVulkanView` — layer host for the CAMetalLayer (draws nothing itself)

The window has three panel slots:
- `container` — content root (nullptr = clear-only pass)
- `contentPanel` — UI tree (retained VkLayer board, composited into the seam)
- `scenePanel` — scene tree (retained VkLayer board)

`setReleasedWhenClosed:NO` is CRITICAL — we own the window object;
only `destroy()` releases it.

---

## 6. The Hot-Loader (the most complex subsystem)

### 6a. HotModule

`Hot_poll` runs on main thread only, every frame:
1. Advance retire ring generation
2. Scan hot_dir for `.dylib`/`.so` files
3. New module or mtime-changed → clone the file
4. `dlopen` the clone → parse manifest → ABI compatibility check
5. Dependency gate (missing dep = retry next poll)
6. Save old state → register trampolines (with rollback snapshot)
7. Phase-2 state restore with `Hot_migrate` on version bump
8. On success: commit swap, retire old handle
9. On failure: `dlclose` clone, unlink clone

### 6b. HotTrampolineTable

One atomic function-pointer table per HotModule instance. 1024 rows.
Each row has `ptr` (current generation) and `fallback_ptr` (prior
generation, mid-swap cover). `get` does a brief spin (4 retries with
`yield` on aarch64) for in-flight swap, then falls back to prior
generation rather than returning NULL.

### 6c. HotRetireRing

Old dylibs park here for 4 poll generations so in-flight calls drain
before `dlclose`. Full ring evicts the oldest entry. Shutdown drains
all.

### 6d. VkLoader

**The VkDevice is created HERE, NOT in the vulkan module.** The device
persists across module reloads. Only pipelines, render passes, and
framebuffers are recreated on reload.

---

## 7. The Vulkan Present Model

Each monitor owns a giant off-screen cache (`VkView`). Every present
loop:
1. Clear the WHOLE cache to background color
2. Render ONE layer (direct children of the container) at absolute
   desktop coordinates
3. Blit the window's region into the acquired swapchain image

Windows are a scissor into the desktop. This means:
- Multiple windows share the same cache
- Live resize = seam canvas frame tracks natively (autoresizingMask),
  boards pin top-left at their own extent, swapchain rebuilt immediately
  on extent drift (the Continuous Real-Time Live Resize Law)
- The frozen board frame is never stretched mid-drag: pinned `kCAGravityTopLeft`
  (freeze-exact), the seam past its extent is transparent (blur shows through)

---

## 8. The single seam canvas (one on-screen Metal layer)

The window owns exactly ONE on-screen Metal layer — the seam `CAMetalLayer`
(the Window Compositing Layer Order Law + the Single-Seam Canvas Law).
Scene/content boards are retained OFFSCREEN `VkLayer` targets registered via
the render repo and composited into the seam image by the seam pass
(`Darling_renderFrame` in darling's compositor). No per-scene, per-child
`CAMetalLayer` or per-pane swapchain exists anywhere in the tree
(the pane-era `VkPane` registry is deleted).

Thread contract: board registration/resize on thread 0 (idle-gated via
`Darling_compositorIdleForResize`); rendering and presents flow through the
render repo's frame loop / resize hook.

---

## 9. Application

The Application is the truth about the running executable: name,
author, version, icon, execution mode (CLI/TUI/GUI). It owns the
application lifecycle: bootstrap, presentation worker threading,
event pumping, and clean exit.

Three run loops:
- `run_cli`: 10ms slice
- `run_tui`: 5ms slice
- `run_gui`: 1ms slice + present worker thread

Application REGISTERS windows, never destroys them during steady state.

---

## 10. Key Architectural Principles

1. **Arena ownership**: Kernel owns the arenas; everything else borrows.
   `Memory_freeAll` is always the final teardown step.
2. **Vulkan device ownership**: VkLoader/vulkan.c owns the device;
   vk_module.c dylib only owns pipelines/render passes/framebuffers.
3. **Window state families**: POLICY (present pacing), CONTENT (panel
   slots), ADAPTERS (vtable listeners by pointer identity).
4. **HotModule per-instance**: two loaders never collide — trampolines
   + retire ring are INSTANCE state, not globals.
5. **Two-thread model**: Thread 0 = OS events; present worker = GPU
   presentation. Bounded-joined before teardown.
6. **Teardown order**: stop apps → join worker → Vk_shutdown → clear
   apps → destroy transient → destroy master arena → free self.

# Hotcwap — Living Docs

> The 2am README for R1 Host. See also
> [`_docs/how-it-works/how hotcwap works.md`](../how-it-works/how%20hotcwap%20works.md)
> and [`how hot-loading works.md`](../how-it-works/how%20hot-loading%20works.md)

---

## 1. Position

R1 Host — boots first, tears down last. Owns the Kernel, OS windows
(`objc/window_cocoa.m` is the ONE ObjC file), the Vulkan device,
and the hot-loader. Includes vexspoke (R2) + graphvex (R3) shapes
only.

```text
Kernel ── nano-VM: master arena + transient arena + app registry
  ├─ Application[8]     (opaque handles, AppRunFn/AppTickFn)
  │    └─ Window[16]    (OS-owned, never hot-updated)
  │         ├─ contentPanel   (retained VkLayer board, composited into seam)
  │         ├─ scenePanel     (retained VkLayer board)
  │         └─ input adapters (Key/Mouse/Touch vtables)
  ├─ Vulkan (graphvex, in-tree) ── device, swapchain, present, blit
  │    ├─ vulkan_mac.c  ── MoltenVK loader + seam CAMetalLayer surface
  │    └─ VkLayer       ── retained offscreen boards (scene/content + depth-1)
  │                        collaged into the ONE on-screen seam canvas
  └─ Hot pipeline
       ├─ HotModule        ── watch/verify/swap/retire dylibs
       ├─ HotTrampolineTable ── atomic fn-ptr swap (fallback covers)
       ├─ HotRetireRing    ── 4-poll grace before dlclose
       ├─ HotManifest      ── ABI verification
       ├─ SpvWatch         ── shader mtime → pipeline rebuild
       ├─ HotStage         ── verify-then-promote updates
       ├─ VkLoader         ── owns VkDevice ACROSS reloads
       └─ dylibs: vk_module (vulkan.dylib), hot_behavior
```

## 2. Key Contracts (memorize these)

- **Teardown order (Rule 26)**: stop apps top-down → 50ms pause →
  `Vk_shutdown` → clear apps → destroy transient → destroy master
  arena LAST.
- **Two-thread live-resize**: Thread 0 = OS events + AppKit tracking;
  the frame loop = `Vk_clearPresent()` on the single seam canvas.
  Bounded-join via `Thread_stop` before teardown.
- **Present model**: each monitor owns a giant off-screen cache
  (`VkView`); every loop clears the WHOLE cache, renders ONE layer
  (direct children of the container), then blits the window's region
  into the swapchain. Windows are a scissor into the desktop.
- **Rule 14 (no double render)**: scenes render only into their retained
  offscreen `VkLayer` targets; the seam pass samples published boards and
  never re-renders them.
- **`setReleasedWhenClosed:NO`** — we own the NSWindow; only
  `destroy()` releases it.
- **HotModule per-instance**: trampolines + retire ring are INSTANCE
  state, not globals — two loaders never collide.
- **VkDevice ownership**: created in `VkLoader`, NOT in the vulkan
  module — survives reloads. Only pipelines/render passes/framebuffers
  are recreated.

## 3. Subsystem Map

| Subsystem | Classes | Level |
|---|---|---|
| `app/` | Application | L2 |
| `kernel/` | Kernel | L4 |
| `hot/` | HotModule, HotTrampolineTable, HotRetireRing, Manifest, SpvWatch, Stage, VkLoader, vk_module, hot_behavior | L1-L4 |
| `vulkan/` (graphvex-owned) | Vulkan, VkLayer, vulkan_mac | L4 |
| `window/` | Window (Win32/X11 stubs) | L4 |
| `objc/` | Window (real, window_cocoa.m) | L4 |
| `main/` | enginetest (windowed demo) | L3 |
| `tests/` | window_test | — |

## 4. Window State Families

- **POLICY**: present pacing + transparency (`renderGeneration`
  reflects swapchain rebuilds)
- **CONTENT**: exactly ONE container slot; nested via
  `Panel_addContainer`
- **ADAPTERS**: vtable listeners by pointer identity, dispatched on
  thread 0
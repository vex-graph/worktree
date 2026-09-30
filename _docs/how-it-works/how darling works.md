# How Darling Works Under the Hood: NSView, CALayer, IOSurface, and Vulkan Explained

> A complete architectural breakdown of the rendering and compositing pipeline in `darling` and `hotcwap`.
> Answers the fundamental question: **"Are we using NSViews, CALayers, or IOSurfaces?"**

---

## 1. The Short Answer: We Use All Three, but with Strict Separation of Concerns

You do not choose between `NSView`, `CALayer`, and `IOSurface`—they form a **vertical pipeline** where each technology solves one specific layer of the macOS desktop problem:

| Component | Technology | Count in App | Role / Purpose |
|---|---|---|---|
| **`Panel` / `Container`** | Pure C23 structs | Hundreds/Thousands | Layout math, 9-part anchors, hit-testing, widget state, and input routing. Zero AppKit overhead. |
| **`NSView`** | AppKit (macOS) | **Exactly 2** | The OS window gatekeepers. Manages the Cocoa window hierarchy, responder chain, and mouse/keyboard events. |
| **`CALayer`** | Core Animation | **Tens (first-gen sections only)** | The hardware compositor nodes. WindowServer moves, transforms, and clips these layers at 120Hz during live resize and scroll. |
| **`IOSurface`** | Apple Hardware Framework | **1 per active CALayer** | Zero-copy VRAM buffers. Vulkan renders into them; macOS WindowServer reads directly from them with zero CPU copying. |
| **`CAMetalLayer`** | QuartzCore / Metal | **1 Board + N Scene Panes** | Hosts Vulkan swapchains for the window background board and independent 3D/2D animation panes. |

---

## 2. The 4-Layer Compositing Stack (Top to Bottom)

Per `../../preferences.md` Rule 11, the compositing stack from the user's eye down to the desktop is fixed:

```text
[ User's Eye / Display ]
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. Floating Panels (CALayers backed by IOSurfaces)          │  <-- HUD, Picture, Gallery Sections S1..S112, Scrollbar
├─────────────────────────────────────────────────────────────┤
│ 2. Scene Panes (CAMetalLayers with own swapchains)          │  <-- Fixed-size 3D/2D animation panes (sceneTL, sceneTR, etc.)
├─────────────────────────────────────────────────────────────┤
│ 3. Board Panel (CAMetalLayer Window Swapchain)              │  <-- Vulkan background scene (or transparent clear)
├─────────────────────────────────────────────────────────────┤
│ 4. NSVisualEffectView (AppKit Blur & Vibrancy)              │  <-- macOS behind-window frosted glass
├─────────────────────────────────────────────────────────────┤
│ 5. NSWindow (Window Frame & Chrome)                         │  <-- Title bar, traffic lights, window border
└─────────────────────────────────────────────────────────────┘
        │
        ▼
[ Desktop Wallpaper / Other Windows ]
```

---

## 3. Deep Dive: The Role of Each Component

### A. `NSView`: The Two Window Gatekeepers
In a standard Mac app, every button, text box, and panel is an `NSView`. That is notoriously slow, bloated with Objective-C allocations, and impossible to integrate cleanly with Vulkan.

In `darling`, there are **only two `NSView`s in the entire application**:
1. **`AntiContentView`**: The root content view of the `NSWindow`.
   - Its sole purpose is to intercept OS mouse, keyboard, scroll, and touch events in `routeEvent()` and push them into the C23 input rings (`Key_pushEvent`, `Mouse_pushMoveEvent`, `Touch_pushTouchEvent`).
2. **`AntiVulkanView`**: A child subview of `AntiContentView`.
   - It is an AppKit view that acts as the **Layer Host** for Core Animation.
   - It does not draw anything itself. Its layer is the `CAMetalLayer` that hosts the primary Vulkan swapchain.

### B. `CALayer`: The WindowServer Compositor Tree
Core Animation (`CALayer`) is Apple's GPU compositor. WindowServer (the macOS process that draws your screen) knows how to composite `CALayers` with hardware acceleration.

- When you create UI sections (like the HUD in `vk_test` or sections S1..S12 in `darling_gallery`), each section gets **one `CALayer`**.
- All these section layers are added as sublayers to `AntiVulkanView.layer`.
- **Why use `CALayer`?** Because when you scroll or resize the window, WindowServer can shift and pin these layers instantly on the GPU compositor thread without waiting for the CPU or Vulkan to re-render.

### C. `IOSurface`: The Zero-Copy VRAM Bridge
A `CALayer` needs pixels to display. Traditionally, software renders into memory and copies it to a texture.
- `IOSurface` is a low-level macOS C API for **sharing hardware GPU textures directly across processes without copies**.
- Each surfaced `CALayer` points its `contents` to an `IOSurfaceRef`:
  ```objc
  (*pc).layer.contents = (__bridge id)(*pc).surface;
  ```
- **How Vulkan uses it**: Vulkan binds the `IOSurface` as a `VkImage` / `VkFramebuffer` via `VkIOSurface`. Vulkan draws the section's background, buttons, and text glyphs directly into the `IOSurface` in VRAM.
- The moment Vulkan finishes drawing, WindowServer can immediately display it. Zero CPU copies, zero texture transfers.

### D. `Panel` & `Container`: The Pure C23 UI Model
If only sections have `CALayers`, what about buttons, labels, switches, and sliders?
- They are **pure C23 structs** (`Panel`, `Button`, `Label`, etc.).
- **The "Few Layers, Deep Paint" Law**:
  - Only first-generation children of the content container own a `CALayer + IOSurface`.
  - All widgets living *inside* a section do **not** own a layer.
  - Instead, the section's render callback (`section_render`) loops over its child widgets and uses Vulkan primitives (`Vk_fillRect`, text glyph SDFs, etc.) to paint them **inside the section's existing `IOSurface`**.

```text
Section Panel (owns CALayer + IOSurface)
  ├── Widget 1 (Button)   --> Painted directly into Section's IOSurface by Vulkan
  ├── Widget 2 (Label)    --> Painted directly into Section's IOSurface by Vulkan
  └── Widget 3 (Switch)   --> Painted directly into Section's IOSurface by Vulkan
```

---

## 4. CALayer vs. CAMetalLayer: Know the Difference

A common architectural question when building a hardware-accelerated UI with Vulkan on macOS is:
> *"Shouldn't every first-generation child panel be a `CAMetalLayer` so that they are all rendered by Vulkan and repaint themselves when dirty?"*

The short answer is **no**: both `CALayer` (backed by `IOSurface`) and `CAMetalLayer` are painted by Vulkan, but they solve fundamentally different problems with vastly different overheads.

### A. Architectural Comparison

| Dimension | `CALayer` (+ `IOSurface`) | `CAMetalLayer` ("Pane of Glass") |
|---|---|---|
| **What It Truly Represents** | A single **GPU VRAM Texture Buffer** (`VkImage` / `VkFramebuffer`) | A complete **Vulkan Swapchain** (`VkSwapchainKHR`) with 2–3 in-flight drawables |
| **Vulkan Driver Entity** | Bound via MoltenVK's `VK_MVK_iosurface` extension | Bound via MoltenVK's `VK_MVK_macos_surface` as a presentation surface |
| **Presentation Mechanism** | Direct VRAM write; macOS WindowServer displays `layer.contents` with zero copies | Full `vkQueuePresentKHR` presentation cycle per frame |
| **GPU Memory & Overhead** | **Near zero** (1 texture buffer; no semaphores, fences, or present queues) | **High** (3 swapchain textures, present semaphores, fences, and OS WindowServer presentation queues) |
| **Repaint Cadence** | **On Demand**: only repaints when `Panel_isTreeDirty` is true | **Continuous**: driven at display refresh rate (60–120 FPS) |
| **Role in the Architecture** | 2D UI panels, HUDs, pictures, buttons, labels, scroll containers | Independent 3D/2D real-time simulation scenes (`sceneTL`, `sceneTR`, etc.) |

### B. The "50-Swapchain Trap"
If every UI section, button card, HUD, and sidebar was given its own `CAMetalLayer`:
- An application with 50 UI components would allocate **50 separate Vulkan swapchains** (150 GPU framebuffer textures!).
- Every dirty tick would require WindowServer to synchronize and arbitrate 50 distinct Metal presentation queues.
- This creates massive GPU memory churn, fence contention, and severe presentation hitching.

By contrast, using `CALayer` with an underlying `IOSurface`:
- **Vulkan still does 100% of the painting**: when a panel is dirtied, Vulkan records draw calls into its command buffer and renders directly into the `IOSurface` in VRAM.
- Once submitted, the pixels are already in GPU memory. Core Animation simply composites the layer—no swapchain overhead, no frame presentation queue!

### C. Does CoreText Support Vulkan?
**No. CoreText has zero native knowledge of Vulkan.** CoreText is an Apple-proprietary framework built exclusively for Core Graphics (`CGContextRef`).

`vexgraph` bridges text into Vulkan using two complementary tiers:
1. **Tier A: Pure GPU SDF Pipeline (Primary)**:
   - Font outlines from `.ttf`/`.otf` files are parsed, and glyphs are baked into a **GPU Signed Distance Field (SDF) Texture Atlas** via the jump-flood algorithm.
   - When a `Label` renders, Vulkan draws vector quads using the **Vulkan SDF shader pipeline** (`s_sdfPipeline`).
   - This runs **100% on the GPU inside Vulkan command buffers**, producing resolution-independent, razor-sharp text with subpixel antialiasing at zero CoreText runtime cost.
2. **Tier B: `TextCore` Rasterization Bridge (Ligatures & Emoji Fallback)**:
   - For complex native typography (rich OpenType ligatures, bidirectional text, system emoji), `TextCore_rasterStyled` invokes CoreText to lay out and rasterize strings into an RGBA pixel buffer.
   - That buffer is uploaded into a Vulkan texture via `Texture_loadRaw()`, which Vulkan then paints into the target `IOSurface` within the standard render pass.

---

## 5. The 9-Part Anchoring System: Mathematical Consistency

In `projects/darling/darling/container.h`, there are 9 anchor and pivot points:
```text
TOP_LEFT (0)      TOP_CENTER (1)      TOP_RIGHT (2)
MIDDLE_LEFT (3)   MIDDLE_CENTER (4)   MIDDLE_RIGHT (5)
BOTTOM_LEFT (6)   BOTTOM_CENTER (7)   BOTTOM_RIGHT (8)
```

In `vk_test.c`:
- `sceneTL`: `CONTAINER_ANCHOR_TOP_LEFT`
- `sceneTR`: `CONTAINER_ANCHOR_TOP_RIGHT`
- `sceneBL`: `CONTAINER_ANCHOR_BOTTOM_LEFT`
- `sceneBR`: `CONTAINER_ANCHOR_BOTTOM_RIGHT`
- `pic` (sunflower): `CONTAINER_ANCHOR_MIDDLE_CENTER`, pivot `CONTAINER_PIVOT_CENTER`
- `hud`: `CONTAINER_ANCHOR_TOP_LEFT`

### A. How C23 Anchors Control Core Animation (`PanelCocoa_setAnchors`)
In `projects/darling/objc/panel_cocoa.m`:
1. **`selfAnchor`** sets `CALayer.anchorPoint` (from `(0,0)` to `(1,1)`) and `CALayer.contentsGravity` (`kCAGravityTopLeft` to `kCAGravityBottomRight`).
2. **`parentAnchor`** sets `CALayer.autoresizingMask` (`kCALayerMinXMargin`, `kCALayerMaxXMargin`, etc.).

During live window resize:
- Core Animation automatically repositions each child `CALayer` according to its `autoresizingMask` and pins the texture according to its `contentsGravity`.
- For example, `sceneBR` stays glued to the bottom-right corner of the window in real time on the GPU, even before Vulkan renders the next frame.

### B. Dynamic Sizing without Dimensional Clamping
- Previously, `Container_setSize` clamped `maxW` and `maxH` to initial dimensions, preventing the root `contentPanel` from expanding when the window resized or zoomed.
- The root `contentPanel` now expands dynamically via `anti_SetPanelSize(contentPanel, w, h)` on window frame changes.
- `PanelCocoa_setAnchors` configures both `autoresizingMask` (margins) and `anchorPoint` on the underlying `CALayer`. WindowServer repositions the sublayers in hardware during the live resize transaction, and the settle pass reconciles exact layout bounds synchronously on Thread 0.

---

## 6. Live Resize, Zoom-to-Fill, and Native Fullscreen Transitions

Handling dynamic macOS window resizing while running a multi-threaded Vulkan presentation pipeline requires strict orchestration between AppKit (Thread 0), Core Animation (WindowServer), and the Vulkan background worker (Thread 1).

### A. The Three Window Transitions
1. **Interactive Edge Drag (`inLiveResize`)**:
   - The user drags the window border or corner.
   - `viewWillStartLiveResize` fires: sets `liveResizing = true`, switches `contentsGravity = kCAGravityResize`, and sets `presentsWithTransaction = NO`.
   - The board swapchain freezes its pixel grid: WindowServer scales the last committed frame on the GPU without intermediate swapchain destructions (`Rule 11`).
   - Child panes (the 4 corner `Scene3D`s) are anchored via `autoresizingMask` and `anchorPoint`; WindowServer moves their `CALayer`s at display refresh rate while they render independently into fixed-size swapchains.
   - On release, `viewDidEndLiveResize` triggers `settleAfterResize`: clears `liveResizing`, restores `kCAGravityTopLeft` and `presentsWithTransaction = YES`, updates `drawableSize` once, resizes `contentPanel`, re-composites, and Vulkan rebuilds the swapchain exactly once at the final extent.

2. **Instant Zoom-to-Fill (Title Bar Double-Click)**:
   - `window:animationResizeTime:` returns `0.0`, eliminating WindowServer's blurry non-rendering bitmap stretch animation.
   - Sets `liveResizing = true` and `_zooming = YES`, putting the renderer into live-resize mode so intermediate frame events do not thrash swapchains.
   - `setFrameSize:` records the new target size, and `windowDidResize` / `viewDidEndLiveResize` lands the true final size in one clean settle pass.

3. **Native macOS Fullscreen (Green Orb / `toggleFullScreen:`)**:
   - When entering or exiting fullscreen, macOS animates the window across desktop Spaces (a slide animation lasting ~1.5 to 2.0 seconds).
   - **The 11ms Cocoa Trap**: During initial setup, Cocoa resizes the window frame and calls `viewDidEndLiveResize` almost immediately (~11ms into the 2000ms transition!).
   - If settle executes at 11ms, it sets `presentsWithTransaction = YES` and clears `liveResizing = false`. When the background worker presents to a window detached in a Space transition, Core Animation transactions are suspended by WindowServer, causing `[CAMetalLayer nextDrawable]` and fence waits to hit their full 100ms–1000ms timeouts across all swapchains, freezing the app for seconds.
   - **The Fullscreen Lifecycle Solution**:
     - `AntiWindowDelegate` implements `windowWillEnterFullScreen:`, `windowDidEnterFullScreen:`, `windowWillExitFullScreen:`, `windowDidExitFullScreen:`, and failure hooks.
     - `windowWillEnterFullScreen:` marks `_fullScreenTransitioning = YES`, `liveResizing = true`, `contentsGravity = kCAGravityResize`, and `presentsWithTransaction = NO`.
     - `viewDidEndLiveResize` checks `_fullScreenTransitioning` and defers the settle pass.
     - `presentsWithTransaction = NO` allows background Vulkan presentation to continue without blocking on suspended Core Animation transactions.
     - When the macOS Space transition completes, `windowDidEnterFullScreen:` (or `windowDidExitFullScreen:`) marks `_fullScreenTransitioning = NO` and executes `settleAfterResize` at the true final settled screen size.

---

## 7. Summary: The Mental Model

When writing code in `vexgraph`:
- **You create**: `Panel`, `Button`, `Label`, `ScrollContainer` (C23 structs in `darling`).
- **The Engine creates**: One `CALayer` + `IOSurface` for each top-level section, plus fixed-size `CAMetalLayer` panes for 3D/2D scenes.
- **Vulkan paints**: Colors, textures, and glyphs into those `IOSurfaces`, and 60fps scenes into the `CAMetalLayer` panes.
- **macOS WindowServer composites**: Those `CALayers` on top of your `CAMetalLayer` background.
- **The Result**: 120 FPS native macOS fluid resizing, instant title-bar zoom, zero-freeze Space fullscreen transitions, and consistent 9-part corner/center anchoring.

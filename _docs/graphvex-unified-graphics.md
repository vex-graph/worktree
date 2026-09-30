# graphvex — Unified Graphics Reading & Target Architecture

> Status: DRAFT (`;;DRAFT`). R3 Driver. This is the READING we do before the
> seam restructure — what graphvex is today, where it is tangled, and the
> unified shape we want. Binds: the Vertical Integration Law (R3 = vexspoke
> only), the Single Class Per File Law, the Present-On-Demand Law, the
> Single-Seam Canvas Law, the Continuous Real-Time Live Resize & Presentation
> Law, the Native Pixel Law, the Dynamic Scalability & Anti-Hardcoding Law.

---

## 1. What "unified graphics" means

There is already a **Graphics seam** (`graphics/graphics.h`): ONE `Graphics`
struct = a function-pointer table (frame lifecycle + every drawable verb), and
each backend is a class exporting one `const Graphics *` row
(`VkGraphics_getRow`, `MetalGraphics_getRow`, `RasterGraphics_getRow`).
`Graphics_setGraphics(id)` stamps the row; `Graphics_<verb>` forwarders call
through it. Callers switch backends with one line.

**That seam is the target, and it is correct.** The problem is what sits
*behind* the Vulkan row: a 2582-line god-file plus four overlapping offscreen
canvas models. The restructure is: make `VkInstance` + `VkRender` + `Surface` +
`Image` the clean implementation behind `VkGraphics`.

---

## 2. Current inventory (by role)

### Context / device
| File | LOC | Role |
|---|---:|---|
| `vulkan/vk_instance.c` | 2582 | **GOD FILE** — instance, device, queue, surface, swapchain, rebuild/retire, present, draw primitives (`fillRect`/`drawTexture`/`drawSDFText`), dump |
| `vulkan/vk_loader.c` | 549 | hot-reload adapter over the vulkan module (trampolines) |
| `vulkan/vk_context.h` | 112 | `VkDevice` transfer protocol across reloads |
| `vulkan/vk_mac.c` | 284 | macOS loader + `CAMetalLayer` surface + IOSurface pass |
| `vulkan/vk_iosurface.c` | 359 | Vulkan ↔ IOSurface bridge (`VK_EXT_metal_objects`) |
| `vulkan/vk_window_seam.c` | 190 | opaque window callbacks (hotcwap seam) |
| `vulkan/vk_guard.h` | 87 | safety-net guards |

### Offscreen canvases — FOUR overlapping models
| File | LOC | Role |
|---|---:|---|
| `surface/surface.c` | 238 | **Surface** — IOSurface canvas (zero-swapchain, monitor-max) |
| `image/image.c` | 311 | **Image** — unified texture/image primitive |
| `image/swapchain.c` | 330 | CPU-stub swapchain |
| `vulkan/vk_view.c` | 538 | per-MONITOR giant cache (OLD model: window = scissor into monitor) |
| `vulkan/vk_layer.c` | 1251 | retained offscreen registry (boards + `COMPOSITED` scenes) |
| `vulkan/vk_scene.c` | 778 | per-SCENE offscreen canvases |
| `image/bindless_heap.c` | 201 | bindless texture heap |

### Board / loop / backend row
| File | LOC | Role |
|---|---:|---|
| `vulkan/graphics_layer.c` | 352 | **GraphicsLayer** — one board (scene/content) shim |
| `graphvex/graphics_loop.c` | 511 | **GraphicsLoop/GfxLoop** — frame scheduler, demand, present |
| `vulkan/vk_graphics.c` | 383 | **VkGraphics** — the Graphics backend row |

### Effects / pipelines / draw
`effect/visual_effect.c` (205) · `scene/{pipeline,render_pass,scene}.c` ·
`draw/{drawable,layered_drawable,vector_drawable,layered_vector_drawable}.c` ·
`sdf_gpu.c` (688) · `spv_watch.c` (227) · `font/*` · `metal/metal_graphics.c`.

---

## 3. The tangle (what we are fixing)

1. **`vk_instance.c` is a god-file** mixing four unrelated jobs: context
   (instance/device/queue), per-window surface+swapchain, presentation
   (fence/device-lost/extent-drift), and DRAW PRIMITIVES. Only the first two
   are "instance"; the draw verbs are rendering.
2. **Four overlapping canvas models** for what is conceptually "an offscreen
   image": `Surface` (IOSurface), `Image` (unified), `VkView` (per-monitor
   cache), `VkLayer` (retained targets), `VkSceneCanvas` (per-scene). The
   `VkView` per-monitor cache is the OLD "window is a scissor into the
   monitor" model, which the fixed-buffer seam + boards superseded.
3. **Swapchain + IOSurface coexist.** The seam is a `VkSwapchainKHR` on a
   `CAMetalLayer`, yet `Surface` (IOSurface) is already wired into R4. Two
   presentation mechanisms for one seam.
4. **No `vk_render.c`.** The "master renderer" (all render functions) is
   scattered: `fillRect`/`drawTexture`/`drawSDFText` in `vk_instance.c`, the
   seam pass in `presentFrameTail`, the board collage in darling.

---

## 4. Target architecture

```
                         Graphics (graphics/graphics.h)  ← the one seam/table
                                   ▲
        ┌──────────────────────────┼───────────────────────────┐
   RasterGraphics            VkGraphics                    MetalGraphics
   (row)                     (row)                         (row)
                                   │ implements
                     ┌─────────────┴──────────────┐
              VkInstance (vk_instance.c)      VkRender (vk_render.c)
              device / instance / queue       MASTER RENDERER:
              + per-window Surface            all render functions +
              + pipelines + IOSurface pass    pass recording + present
                     │                               │
              Surface (surface.c)             Image (image.c)
              the ONE on-screen IOSurface     the two board VkImages
              (fixed monitor px, top-left)    scene (bottom) / content (top)
```

### Responsibility split

| Class | Owns | Never does |
|---|---|---|
| **VkInstance** (`vk_instance.c`) | `VkInstance`/`VkPhysicalDevice`/`VkDevice`/`VkQueue`; the **per-window Surface** (create/attach/destroy); pipeline layouts + the IOSurface render pass; the Vulkan device lifecycle | Record frames, present, draw verbs |
| **VkRender** (`vk_render.c`) | The **master renderer**: every render function (`fillRect`, `drawRect`, `drawTexture`, `drawSDFText`, `drawColorGlyph`), the board composite, the seam pass recording, the fence/submit/present | Device/instance/queue creation |
| **Surface** (`surface.c`) | The ONE on-screen IOSurface canvas: IOSurface + CALayer (`presentsWithTransaction`, `kCAGravityTopLeft`), fixed monitor px, its seam `VkImage` | Render, draw, own boards |
| **Image** (`image.c`) | An offscreen `VkImage` (+ CPU shadow): the two boards (scene/content) and, later, retained scene worlds | Present, own the seam |

### What consolidates
- `VkView` (per-monitor cache) retires — superseded by the fixed-buffer seam
  + the two board Images.
- `VkLayer` + `VkSceneCanvas` fold onto **Image** (one offscreen primitive).
- The seam swapchain retires in favor of **Surface** (IOSurface).
- `vk_instance.c` shrinks to context + per-window Surface; all rendering moves
  to `vk_render.c`.

---

## 5. Migration order (upstream-first)

1. **`feat(vk_render): extract the master renderer`** — move `fillRect`/
   `drawTexture`/`drawSDFText`/`drawColorGlyph` + the pass recording out of
   `vk_instance.c` into `vk_render.c`. Pure code motion; no behavior change.
2. **`feat(surface): make the seam an IOSurface`** — retire the
   `VkSwapchainKHR`; `Surface` owns the seam `VkImage`; `VkRender` presents
   into it; the `CAMetalLayer` shows the IOSurface. (The step-1 we specced.)
3. **`feat(image): boards as Images`** — the two boards become `Image`s
   (scene/content); `VkLayer` retained targets become `Image`s.
4. **`refactor(vk_view): retire the per-monitor cache`** — delete `vk_view.c`
   once nothing samples it.
5. **`feat(vk_instance): per-window Surface`** — `VkInstance` owns one
   `Surface` per window (N windows ⇒ N seams), driven by the window seam.

---

## 6. Open questions

1. Does **`Surface` own the seam `VkImage`**, or does an `Image` inside the
   Surface? (Target: Surface owns it; boards are separate Images.)
2. Does **`VkRender` own the command buffer/queue**, or borrow it from
   `VkInstance`? (Target: VkInstance owns the queue; VkRender records + submits.)
3. **N windows ⇒ N Surfaces**: one device, many seams — confirm the seam
   callbacks (currently process-global in `vk_window_seam.c`) become
   per-window.
4. `VkView` retirement: is anything still sampling the per-monitor cache, or
   is it already dead code?

# Graphvex Uniform API — Manifest (Vulkan Hidden Behind `Gx` Boards)

> Why: darling spells `Vk_*`/`Texture_*`/`VkIOSurface_*` directly, so every
> backend quirk leaks into UI code. This manifest makes graphvex the only
> place that knows Vulkan/Metal/Direct. Darling/hotcwap speak `Image`,
> `Drawable`, `Brush`, `Mesh` — never `VkImage`, `VkFence`, `VkCommandBuffer`.
> Sources: `../../projects/graphvex/src/graphvex/device.h` (backend seam sketch),
> `../../projects/graphvex/src/graphvex/type.h` (IDs `0x0100-0x01FF`),
> `projects/graphvex/src/buffer/*`, `src/font/font.h`, `src/vulkan/*`,
> `../../preferences.md` Rules 3/4/9/17/18/23/24/28.

---

## 1. Law: backend lives in one folder, API lives everywhere else

* `src/vulkan/*`, `src/metal/*`, `src/direct/*` are drivers. They may include
  `<vulkan/...>`, `<Metal/...>`, `<d3d12.h>`. Nobody else may.
* Public headers (`src/image/image.h`, `src/sync/fence.h`, `src/draw/drawable.h`,
  ...) expose opaque structs + `Class_verb` functions only. Zero `Vk*` types
  in signatures — handles cross as `void *` or graphvex structs.
* `GraphicsDevice + GraphicsBackend` (`src/graphvex/device.h`) owns init,
  `beginFrame/submit/present`. `GraphicsDrawable{handle, w, h}` flows DOWN
  from hotcwap (owns `NSWindow/CAMetalLayer`); graphvex never includes
  `window.h`, never retains the handle.
* One class per file pair (Rule 3). Lowercase filename = lowercase class
  (`image.h/image.c`, `fence.h/fence.c`). Second public struct = defect.
  Private rows stay file-local under `PRIVATE HELPERS`.
* Every class: `;;OVERVIEW` + 4-tier registry (Rule 23), symmetric
  `set/get` (Rule 24), dest-last outs (Rule 9), `T *name` decls /
  `(T*) var` casts, `(*p).field` only, `-Wall -Wextra -Werror`.

---

## 2. Class inventory (requested set, frozen names)

| Class | File pair | Level    | Role |
|---|---|----------|---|
| `Image` | `src/image/image.h/.c` | L2       | GPU image. Replaces `Texture_*` ids + `VkIOSurface_*` wrap. `Image_0()` empty, `Image_2(w,h)`, `Image_fromRgba(data,w,h,tmp)` |
| `Swapchain` | `src/image/swapchain.h/.c` | L4       | Framebuffer chain behind a `GraphicsDrawable`. `acquire/next/present`. Only hotcwap feeds it the handle |
| `Semaphore` | `src/sync/semaphore.h/.c` | L4       | GPU-GPU ordering. Opaque; `Semaphore_0()`, `Semaphore_wait/signal` are backend ops, never ints |
| `Fence` | `src/sync/fence.h/.c` | L4       | CPU-GPU join. Bounded wait only (Rule 27: 100 ms, drop frame, never `UINT64_MAX`) |
| `Shape` | `src/vector/shape.h/.c` | L2       | SVG reader + path store. `Shape_fromSvg(path, dest)`, `Shape_rect/circle/path(...)`. No raster in it |
| `Font` | `src/font/font.h/.c` | L2       | Exists. Keep API, hide `Vk_drawSDFText`/`Vk_drawColorGlyph` behind `Drawable_drawGlyphRun` |
| `Mesh` | `src/mesh/mesh.h/.c` | L2       | Whole mesh: vertex/index blobs off-heap, `Mesh_fromObj(path,dest)`, `Mesh_vertexCount/indexCount` |
| `Meshlet` | `src/mesh/meshlet.h/.c` | L2       | 128-triangle slice of a `Mesh`. `Meshlet_build(mesh,i,dest)`, `Meshlet_pack` for GPU dispatch. Borrowed view, never owns verts |
| `Scene` | `src/scene/scene.h/.c` | L3       | Rendered scene: mesh + transform + material list. `Scene_addMesh`, `Scene_render(scene,drawable)` |
| `Stroke` | `src/paint/stroke.h/.c` | L2       | `width + dash + cap + join + color`. Plain data, no device |
| `Brush` | `src/paint/brush.h/.c` | L2       | Base solid brush: `color + opacity`. `VectorBrush`/`RasterBrush` extend by embedding it first |
| `VectorBrush` | `src/paint/vector_brush.h/.c` | L2       | Gradient/pattern brush: `stops + transform`. Lives in vector space, resolution-free |
| `RasterBrush` | `src/paint/raster_brush.h/.c` | L2       | Stamp brush: 32×32 R8 SDF tip (`uint8_t tip[1024]`, shape-only) + `size + opacity + spacing + jitter + softness`. Tint from `Brush.color`; textured tips use optional `Image *tipImage` override. Round/soft/square baked once; airbrush = low-alpha buildup, eraser = inverse blend |
| `Drawable` | `src/draw/drawable.h/.c` | L3       | One-layer board. Owns one `Image`. All `fill*/draw*` hang here |
| `LayeredDrawable` | `src/draw/layered_drawable.h/.c` | L3       | Ibis board: N `Drawable` layers + `active + opacity + blend + visibleMask` |
| `VectorDrawable` | `src/draw/vector_drawable.h/.c` | L3       | Infinite-canvas vector board: `Shape + Stroke/Brush` list, float world coords, camera `pan/zoom` |
| `LayeredVectorDrawable` | `src/draw/layered_vector_drawable.h/.c` | L3       | Layered infinite canvas: N `VectorDrawable` layers, same mask/active law as raster twin |

Rule 29 applies: `LayeredDrawable` exposes layers only via
`LayeredDrawable_layer*` verbs, never by piercing. Same for caret-like
sub-parts elsewhere.

---

## 3. Draw API (stroke vs fill, vector vs raster share verbs)

`draw` = stroke outline with `Stroke`. `fill` = solid/brush interior.
Every call takes `(self, rect/circle/path, paint, dest)` with dest last
where a result lands; pure draws return `void` and dirty the board.

```c
/* raster board */
void Drawable_fillRect(Drawable *self, float x, float y, float w, float h, const Brush *brush);
void Drawable_drawRect(Drawable *self, float x, float y, float w, float h, const Stroke *stroke);
void Drawable_fillCircle(Drawable *self, float cx, float cy, float r, const Brush *brush);
void Drawable_drawCircle(Drawable *self, float cx, float cy, float r, const Stroke *stroke);
void Drawable_fillPath(Drawable *self, const Shape *shape, const Brush *brush);
void Drawable_drawPath(Drawable *self, const Shape *shape, const Stroke *stroke);
void Drawable_drawImage(Drawable *self, const Image *img, float x, float y, float w, float h);
void Drawable_drawGlyphRun(Drawable *self, const Font *font, const uint32_t *cps, size_t n,
                           float x, float y, float size, const Brush *brush);

/* vector board mirrors the same verbs in world coords */
void VectorDrawable_fillRect(VectorDrawable *self, float x, float y, float w, float h, const Brush *brush);
void VectorDrawable_drawRect(VectorDrawable *self, float x, float y, float w, float h, const Stroke *stroke);
void VectorDrawable_fillCircle(VectorDrawable *self, float cx, float cy, float r, const Brush *brush);
void VectorDrawable_drawCircle(VectorDrawable *self, float cx, float cy, float r, const Stroke *stroke);
```

Backend mapping (darling never sees): raster board records quads into the
current `GraphicsFrame`; SDF/JFA stay inside `sdf_gpu.c` + `texture.c`;
`Vk_fillRect`/`Vk_drawSDFText`/`Vk_drawColorGlyph` become static helpers
called only by `drawable.c`/`vector_drawable.c`.

---

## 4. Type IDs (Rule 17: graphvex owns `0x0100-0x01FF`)

Extend `src/graphvex/type.h`; vexspoke never includes this file:

```c
#define ID_FONT               0x0100u  /* exists */
#define ID_IMAGE              0x0101u
#define ID_SWAPCHAIN          0x0102u
#define ID_SEMAPHORE          0x0103u
#define ID_FENCE              0x0104u
#define ID_SHAPE              0x0105u
#define ID_MESH               0x0106u
#define ID_MESHLET            0x0107u
#define ID_SCENE              0x0108u
#define ID_STROKE             0x0109u
#define ID_BRUSH              0x010Au
#define ID_VECTOR_BRUSH       0x010Bu
#define ID_RASTER_BRUSH       0x010Cu
#define ID_DRAWABLE           0x010Du
#define ID_LAYERED_DRAWABLE   0x010Eu
#define ID_VECTOR_DRAWABLE    0x010Fu
#define ID_LAYERED_VECTOR_DRAWABLE 0x0110u
/* TYPE_X_SINGLETON = (PROJ_GRAPHVEX | FORM_SINGLETON | ID_X) */
```

---

## 5. Includes + seams (Rules 17/18/19)

```c
#include "image/image.h"     /* yes — rooted at src/ */
#include "../image/image.h"  /* no — parent hop banned */
```

* graphvex depends on vexspoke only. Never `window.h`, never `darling/*`.
* `../../CMakeLists.txt`: one `add_library(graphvex ...)` entry per new `.c`;
  keep `if(NOT TARGET vexspoke)` FetchContent seam; shaders stay under
  `shader/` with `VEX_SPV_DIR` resolution (Rule 21).
* Migration is upstream-first (Rule 20): land `Image/Fence/Semaphore` in
  graphvex, then convert darling `compositor.c`/`panel_cocoa.m` off
  `VkIOSurface_*`, then delete the leaky shims. One class per commit
  (Rule 6/25), e.g. `feat(image): add Image_2 + rgba upload`.

---

## 6. Build order (small, reviewable)

1. `Image + Fence + Semaphore + Swapchain` — boot a triangle without darling
   spelling `Vk*`.
2. `Stroke + Brush + Drawable(fill/drawRect/Circle)` — replace `Vk_fillRect`
   call sites; gallery sections paint through boards.
3. `Shape (rect/circle first, SVG second) + VectorBrush` — paths + gradients.
4. `Font hookup` — `Drawable_drawGlyphRun`; delete `Vk_draw*` from darling
   includes.
5. `Mesh + Meshlet + Scene` — `vk_scene.c` moves behind `Scene_render`.
6. `RasterBrush + LayeredDrawable` (Ibis) then `VectorDrawable +
   LayeredVectorDrawable` (infinite canvas: world coords + camera, tiles on
   demand, never one giant `Image`).

---

## 7. Done means

* `rg "Vk[A-Z]|Texture_|VkIOSurface_|SdfGpu_" projects/darling projects/hotcwap`
  returns only `device.c`/driver shims — zero UI-tree hits.
* Gallery + `darlingtest` pixel-identical, present-on-demand intact, 100 ms
  fence bound intact, teardown order intact (Rules 26/27).
* Each new class has `;;OVERVIEW`, symmetric `get/set`, null-safe getters,
  no `->`, dest-last, per-class commit.

---

## 8. Common denominator: command buffers, bindless, instancing, parallelism (core vs optional)

Darling never sees `VkCommandBuffer` / `MTLCommandBuffer` / `ID3D12GraphicsCommandList`.
It sees `CommandBuffer`, `CommandQueue`, `GpuBuffer`, `BindlessHeap`, `Pipeline`.
Drivers translate. Web-search grounding: bindless is portable (Vulkan
`VK_EXT_descriptor_indexing`, core in 1.2 + `nonuniformEXT`; Metal argument
buffers; DX12 SM6.6 `ResourceDescriptorHeap`), multi-thread recording is
per-thread pools + secondary buffers, ray tracing is NOT portable on Apple
(MoltenVK issue #427 open; `VK_KHR_ray_tracing_pipeline` unsupported over
Metal, Metal RT exists natively but has no MoltenVK mapping).

### 8.1 Missing classes (add to #2 table)

| Class | File pair | Role |
|---|---|---|
| `CommandBuffer` | `src/sync/command_buffer.h/.c` | Per-thread record handle. `CommandBuffer_begin/rec/end`. One pool per thread per frame; never shared across threads (Vulkan spec rule; D3D12 allocators + Metal buffers same law) |
| `CommandQueue` | `src/sync/command_queue.h/.c` | Queue family: `GRAPHICS / COMPUTE / COPY`. Async JFA bake goes to COMPUTE, uploads to COPY, never blocks GRAPHICS |
| `GpuBuffer` | `src/buffer/gpu_buffer.h/.c` | Device-visible storage/uniform/vertex/index/indirect buffer. `GpuBuffer_upload` stages via COPY queue. This is the "store things in different things": device-local vs host-visible vs write-combined heaps hidden behind usage flags |
| `BindlessHeap` | `src/image/bindless_heap.h/.c` | The `Texture_*` successor: one heap for sampled images, one for storage, one for samplers. `BindlessHeap_register(image, dest)` returns a stable `uint32_t` handle used as `nonuniformEXT` / `NonUniformResourceIndex` / argument-buffer index. Dummy white texture at slot 0 so `-1` never hangs the GPU |
| `Pipeline` | `src/scene/pipeline.h/.c` | Compiled raster/compute state (shaders + blend + depth). HLSL-6 as single shader source (MethaneKit pattern), compiled per backend at build time |
| `Pass` | `src/scene/pass.h/.c` | One render pass instance (shadowmap, scene, UI). Parallel passes record on separate threads, joined with barriers — the Vulkan multithreading-render-passes pattern |

### 8.2 What IS the denominator (ship in v1)

* Bindless: yes. Descriptor-indexing + update-after-bind + partially-bound +
  variable-count on Vulkan; argument buffers on Metal; descriptor tables/heaps
  on DX12. Shader rule: divergent indices go through `NonUniformResourceIndex`
  (HLSL) / `nonuniformEXT` (GLSL). Root/push constants for per-draw params.
* Instanced: yes. `DrawInstanced + InstanceBuffer + instanceID`
  (`SV_InstanceID` / `instance_id` / `gl_InstanceIndex`) on all three.
  `Meshlet` (128 tris) rides this path toward mesh shaders later.
* Heaps: yes. Device-local (GPU-only), host-visible staging, write-combined
  upload — all three APIs have the trio, names differ.
* Parallelism: yes, at record time. One `CommandBuffer` + one descriptor arena
  per thread per frame; primary-per-pass or secondary-inherit-pass execution;
  reset pools not individual buffers (allocate-and-free is the slow path per
  Khronos samples); `ONE_TIME_SUBMIT` for transient boards. SDF bake and
  texture upload never sit on the graphics queue.

### 8.3 What is NOT the denominator (capability query, not core)

* Ray tracing: optional `Capability_RAY_QUERY / RAY_PIPELINE`. MoltenVK does
  not implement it, so compiling it into core breaks macOS Vulkan. Native
  Metal RT and DXR/VK-KHR paths live behind
  `GraphicsDevice_supports(dev, CAP)`. Boards degrade to raster when false.
* Mesh shaders, tessellation-geometry splits, pipeline statistics queries,
  PVRTC-via-staging: same treatment — query bits, never `#ifdef` in darling.

```c
uint32_t caps = GraphicsDevice_capabilities(dev);  /* bitmask */
bool rt = (caps & GRAPHVEX_CAP_RAY_QUERY) != 0;
Scene_render(scene, drawable);                     /* raster always */
if (rt) Scene_traceRays(scene, drawable);          /* gated */
```

---

## 9. Strict constructor / setter-getter / varargs law (Rules 3/4/9/23/24)

* Arity-only dispatch via `CONSTRUCTOR_DISPATCH` (`c23/constructor.h`).
  Never C `...` ellipse / `va_list` for constructors — count selects,
  types do not.
* Every class exposes one shim: `#define Class(...) CONSTRUCTOR_DISPATCH(Class, __VA_ARGS__)`
  plus contiguous `Class_0 .. Class_N` with zero gaps. A missing arity in
  the middle is a defect (stricter than the generic header, which tolerates gaps).
* Each arity is documented in the `;;OVERVIEW` FUNCTION REGISTRY:
  `ClassName() : ClassName_0()`, `ClassName(w,h) : ClassName_2(w,h)`.
* Symmetric `set/get` per Rule 24 for every state-bearing field:
  `void Class_setX(Class *self, T val)` / `T Class_getX(const Class *self)`.
  Multi-value outs are dest-last per Rule 9:
  `void Class_getSize(const Class *self, float *outW, float *outH)`.
* Getters are null-safe: `nullptr` self returns `nullptr` / `0` / `false` / `0.0f`.
* Style: no `->` (always `(*p).field`), decls are `T *name`,
  casts are `(T*) var` with one space after `)` (Rules 1/2/16).

```c
Drawable *Drawable_0(void);
Drawable *Drawable_1(Image *img);
#define Drawable(...) CONSTRUCTOR_DISPATCH(Drawable, __VA_ARGS__)
void Drawable_setOpacity(Drawable *self, float opacity);
float Drawable_getOpacity(const Drawable *self);
void Drawable_getSize(const Drawable *self, float *outW, float *outH);
```

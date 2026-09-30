# Graphvex — Living Docs

> The 2am README for R3 Driver. See also
> [`_docs/how-it-works/how graphvex works.md`](../how-it-works/how%20graphvex%20works.md)
> for the architecture walkthrough, and
> [`graphvex_uniform_api.md`](graphvex_uniform_api.md) for the backend
> abstraction manifest (the `Gx` boards law).

---

## 1. Position

R3 Driver — raw GPU/hardware. Includes vexspoke (R2) only. Never
hotcwap, darling, api-haven, or engines (Rule 17). Two rendering
paths: CPU raster → IOSurface (UI, AppKit-composited) and Vulkan
swapchain (scenes).

```text
CPU path (UI):   Buffer → IOSurface → CALayer → AppKit compositing
GPU path (scene): scene → VkSceneCanvas → VkView cache → swapchain blit → present
Compute:         coverage → SdfGpu (jump-flood) → SDF atlas
```

## 2. Subsystem Map

| Subsystem | Classes | Level |
|---|---|---|
| `buffer/` | Buffer (base) + Color/Depth/Stencil/Height/Normal/Shadow/Frame, GpuBuffer | L2 |
| `font/` | Font, FontBake (SDF atlas, bake-on-demand), stb_truetype | L2/L3 |
| `vulkan/` | SdfGpu, VkView (monitor cache), VkSceneCanvas, VkIOSurface | L4 |
| `vulkan/texture/` | Texture (bindless 1024-slot registry) | L4 |
| `image/` | Image, Swapchain, BindlessHeap, FrameImporter | L2 |
| `mesh/` | Mesh (interleaved verts, OBJ), Meshlet (128-tri clusters) | L2 |
| `paint/` | Brush (base), Stroke, RasterBrush, VectorBrush | L2 |
| `draw/` | Drawable, LayeredDrawable, VectorDrawable, LayeredVectorDrawable | L3 |
| `scene/` | Scene, Pipeline, Pass | L2/L3 |
| `sync/` | Fence, Semaphore, CommandBuffer, CommandQueue (CPU stubs) | L2 |
| `vector/` | Shape (SVG paths) | L2 |
| `io/` | Vfs (anti://, project:// URIs) | L2 |
| `graphvex/` | type.h (IDs 0x0100-0x0117), device.h (Gx seam), version | L1 |

## 3. Key Contracts (memorize these)

- **Backend seam (the Gx law)**: only `src/vulkan/*`, `src/metal/*`,
  `src/direct/*` may include vendor headers. Public headers expose
  opaque structs + `Class_verb` functions only. Zero `Vk*` types in
  signatures — handles cross as `void*` or graphvex structs.
  Darling/hotcwap speak `Image`, `Drawable`, `Brush`, `Mesh` — never
  `VkImage`, `VkFence`, `VkCommandBuffer`.
- **Module-level Vulkan state**: Texture/SdfGpu/VkView/VkSceneCanvas/
  VkIOSurface use static globals; `*_initModule` once,
  `*_shutdown` once.
- **Texture replace/retire (Rule 39 net)**: same-size `Texture_replaceRaw`
  is an in-place `Texture_updateSubRaw` (zero destroy); a resize detaches
  the old row, publishes fresh handles + `UpdateDescriptorSets`, and rings
  the old `(image, memory, view, sampler)` on the bounded `RETIRE_MAX 8`
  ring — reap only after fence signal or 2 drained frames, never
  `DeviceWaitIdle`/`QueueWaitIdle` between another CB Begin/End. Uploads
  submit with a per-upload fence + two 100ms waits max (Rule 27),
  throttled log, drop-degrade false; timeout leaks the flying CB + staging
  once (pool/shutdown reclaim) rather than use-after-free the GPU read.
  `Texture_free` retires instead of destroying inline; `Texture_shutdown`
  bounded-drains the ring first (Rule 26). Introspection:
  `Texture_retireDepth/Capacity/frameSeq` (Rule 24) — plus the
  sampler-flight seam, Rule 33/39: the render-flight owner (compositor)
  registers its leak-work proof `Texture_setRetireGuard(bool (*)())`; the
  ring reaps fence-less rollover rows ONLY while the guard returns true
  (2-frame CPU lag = standalone fallback, no guard bound), never
  `DeviceWaitIdle` between CB Begin/End. Symmetric Rule 24 introspection
  `Texture_getRetireGuard()`. Cold entries reject  null/zero-size/overflow once (Rule 35). Proof:
  `_tests/graphvex/texture_retire_test.c`.
- **VkGuard queue contract (Rule 39)**: submit/fence/present seams pass
  their live queue — null queue returns false. Device-resource seams
  (create/destroy/record/export) use the explicit opt-out
  `VkGuard_checkResource`. NDEBUG tree-shakes both to no-ops.
- **Font plug-and-play**: `Font_open(family)` — baked+fresh → fast
  path; missing/stale → bake on the spot; not installed → live TTF.
- **Meshlet packing**: `MESHLET_MAX_VERTICES 64`,
  `MESHLET_MAX_TRIANGLES 128`. Cluster = AABB + normal cone + 8-bit
  local indices.
- **Embed-first upcast**: RasterBrush/VectorBrush embed Brush first;
  `*_asBrush()` is address arithmetic (Rule 29).
- **CPU-shadow stubs**: Image/GpuBuffer/Swapchain/FrameImporter carry
  owned CPU mirrors — testable with no GPU linked.
- **Dest-last, arena-first**: constructors try `Memory_alloc`
  (vexspoke) first, fall back to `calloc` standalone.

## 4. Shader Inventory (shader/)

| Shader | Stage | Purpose |
|---|---|---|
| hello_triangle | vert/frag | triangle demo |
| solid_quad | vert/frag | solid quad |
| text_sdf | vert/frag | SDF text |
| texture_quad | vert/frag | textured quad (atlas) |
| sdf_jfa | compute | jump-flood SDF |
| sdf_combine | compute | SDF finalize |

Source of truth: `projects/graphvex/shader/spv/` (Rule 21).
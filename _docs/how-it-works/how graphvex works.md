# How graphvex Works: The GPU Driver

> The 2am README for R3 Driver. If you forgot everything, read
> sections 1-3 and go back to sleep. If it's 2pm and you're adding a
> feature, read the API surface at the bottom.
> Answers the fundamental question: **"How do pixels get to the
> screen?"**
> Answer: **CPU raster → IOSurface → AppKit compositing. Vulkan for
> scenes. WGPU for compute.**

---

## 1. The Short Answer: CPU-First, GPU-When-Needed

graphvex is the R3 GPU driver. It includes vexspoke (R2) only. It
never includes hotcwap, darling, api-haven, or any engine.

The core insight: the UI layer (darling) renders to IOSurfaces via
CPU raster. AppKit composites those surfaces into the window. Vulkan
is used ONLY for scene backgrounds and GPU compute (SDF baking,
jump-flood). WGPU is used for compute shaders.

| Piece | What it is | Level | Role |
|---|---|---|---|
| `Buffer` family | 2D multi-channel rasters | L2 | CPU pixel storage (Color, Depth, Stencil, etc.) |
| `GpuBuffer` | device-visible byte range | L2 | storage/uniform/vertex/index with CPU shadow |
| `Font` / `FontBake` | TrueType → SDF atlas | L2/L3 | live TTF raster or prebaked dictionary |
| `Texture` | bindless GPU registry | L4 | 1024-slot descriptor array, BGRA8 |
| `VkView` | per-monitor render cache | L4 | giant off-screen image, window blit source |
| `VkSceneCanvas` | per-scene offscreen | L4 | double-buffered, stale-bridge for live resize |
| `VkIOSurface` | Vulkan/IOSurface bridge | L4 | zero-copy via VK_EXT_metal_objects |
| `SdfGpu` | GPU jump-flood SDF | L4 | 24 compute dispatches per atlas page |
| `Mesh` / `Meshlet` | geometry containers | L2 | 128-triangle clusters, normal cones |
| `Brush` / `Stroke` | paint primitives | L2 | solid, raster stamp, vector gradient |
| `Drawable` / `LayeredDrawable` | raster boards | L3 | CPU draw ops, multi-layer compositing |
| `Shape` | vector paths | L2 | moveTo/lineTo/cubicTo, SVG parsing |
| `Scene` / `Pipeline` / `Pass` | render graph | L2/L3 | mesh nodes, transforms, materials |

---

## 2. Where It Sits (Read This Once)

```text
R1 hotcwap   — owns the Vulkan device and window
R2 vexspoke  — arenas, types, math. graphvex includes this only.
R3 graphvex  — GPU driver. WE ARE HERE.
R4 darling   — UI toolkit (includes graphvex for Buffer/Font/Brush/Drawable)
R5 apps      — your IDE, your game (consume graphvex through darling)
```

graphvex is R3 — it includes vexspoke shapes only. It never includes
hotcwap, darling, api-haven, or engine headers.

---

## 3. The Two Rendering Paths

### Path A: CPU Raster → IOSurface (UI)

This is the primary path for darling widgets:
1. darling renders to a `Buffer` (CPU pixel storage)
2. Buffer data is uploaded to an `IOSurface`
3. `CALayer` backs the IOSurface
4. AppKit compositing puts it on screen

Zero Vulkan involvement. This is how labels, buttons, scrollbars,
and all UI widgets render.

### Path B: Vulkan Swapchain (Scenes)

This is for 3D/2D animation scenes:
1. Scene renders into a `VkSceneCanvas` (offscreen)
2. Canvas is stamped onto the monitor cache (`VkView`)
3. Window blit region from cache into swapchain
4. Vulkan present

The monitor cache is the key insight: one giant off-screen image per
monitor, rendered in absolute desktop coordinates. Windows are a
scissor into this cache.

---

## 4. The Buffer Family

All buffers are 2D multi-channel rasters backed by Memory-allocated
blocks. Width × height × channels, stored as contiguous 64-bit
elements.

| Buffer | Channels | Use |
|---|---|---|
| `ColorBuffer` | 4 (RGBA) | primary pixel storage |
| `DepthBuffer` | 1 (float) | depth testing |
| `StencilBuffer` | 1 (uint8) | stencil operations |
| `HeightBuffer` | 1 (float) | heightmap |
| `NormalBuffer` | 3 (XYZ float) | normal map |
| `ShadowBuffer` | 1 (float) | shadow cascade |
| `FrameBuffer` | 4 (RGBA) | composite render target |

`GpuBuffer` is different — it's a device-visible byte range with a
CPU shadow mirror. Used for uniform buffers, vertex buffers, index
buffers.

---

## 5. The Font System

### Live Fonts (TTF on disk)

`Font_load(path)` parses TTF via stb_truetype. On-demand SDF raster:
request a glyph at a pixel height, get UV bounds into an atlas page.
Atlas pages are 2048×2048 BGRA8 images.

### Baked Fonts (.antifont files)

`FontBake_bakeOne` turns a TTF into a multi-page SDF atlas + glyph
dictionary. Two bake paths:
- **CPU**: per-glyph SDF raster, ~1ms each
- **GPU**: coverage raster → jump-flood compute → combine (24
  dispatches per page, much faster)

`Font_open(familyName)` is plug-and-play: baked entry present and
fresh → fast path; missing/stale → bake on the spot; not installed →
fallback to live TTF.

---

## 6. The Vulkan Subsystem

### VkView (per-monitor cache)

One giant off-screen BGRA8 image per attached monitor at native
resolution. Rendered in absolute desktop coordinates. All windows
blit from this cache.

### VkSceneCanvas (per-scene offscreen)

Double-buffered with stale-bridge support for live resize. When the
canvas resizes, the previous-geometry front is kept alive so the
collage never shows a hole. Generation guard prevents stale flips.

### VkIOSurface (Vulkan/IOSurface bridge)

Zero-copy interop via `VK_EXT_metal_objects`. A VkImage is exported
as an `IOSurfaceRef` for AppKit compositing, or vice versa. Shared
GPU memory in BGRA8.

### SdfGpu (GPU jump-flood SDF baker)

During font install, bakes whole coverage pages in ~24 compute
dispatches instead of thousands of per-glyph CPU SDF rasters. Uses
`sdf_jfa.spv` (jump-flood) and `sdf_combine.spv` (combine pass).

---

## 7. The Mesh System

`Mesh` holds interleaved vertex data (8 floats: xyz + nxnynz + uv)
and a triangle index buffer. Supports Wavefront OBJ parsing.

`Meshlet` is a 128-triangle cluster slice of a parent Mesh. Borrowed
view (never owns or frees mesh data). Computes cluster AABB and normal
cone for cluster culling. Packs cluster header + 8-bit local indices
for GPU payload dispatch.

---

## 8. The Paint System

**Brush** is the base (color + opacity). Two variants embed it as
first member (Rule 29):
- **RasterBrush**: stamp brush with 32×32 R8 SDF tip, per-dab dynamics
- **VectorBrush**: gradient/pattern brush, 8 stops + affine transform

**Stroke** is plain data (width, dash, cap, join, color).

**Shape** is pure vector path geometry (moveTo, lineTo, cubicTo, close).
Supports SVG path parsing.

---

## 9. The Draw System

**Drawable**: single-layer raster board owning one Image. CPU stub —
every fill/draw/clear verb null-guards and marks dirty.

**LayeredDrawable**: N Drawable layers + active index + opacity + blend
+ visibleMask. Max 32 layers.

**VectorDrawable**: infinite-canvas vector board. Records vector
commands in float world coordinates with camera pan/zoom. Commands
render onto a raster Drawable board.

**LayeredVectorDrawable**: N VectorDrawable layers. Renders visible
layers to destination raster Drawable.

---

## 10. Key Architectural Principles

1. **CPU-first rendering**: UI widgets render via CPU raster to
   IOSurfaces. Vulkan is for scenes and compute only.
2. **Module-level Vulkan state**: Texture, SdfGpu, VkView,
   VkSceneCanvas, VkIOSurface use static globals for device state.
   Initialized once via `*_initModule`, destroyed via `*_shutdown`.
3. **Embed-first upcast**: Brush is the first member of RasterBrush
   and VectorBrush. `RasterBrush_asBrush()` is address arithmetic.
4. **Borrowed views**: Meshlet borrows Mesh; Pass borrows Image;
   FontPage glyphs borrow Font fontinfo.
5. **Arena-aware allocation**: every constructor tries `Memory_alloc`
   first (vexspoke arena), falls back to `calloc` for standalone.
6. **Dest-last parameters**: all output parameters come last.
7. **Leaf architecture**: graphvex includes vexspoke only.

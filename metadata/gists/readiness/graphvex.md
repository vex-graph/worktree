# graphvex — GPU Compute, Graphics Pipelines & Shaders

> R3 GPU Driver Substrate. Supervised by R1 `hotcwap`. May borrow either R2 public
> contract: [vexspoke](#file-vexspoke-md) CPU computation/behavior or [relational-engine](#file-relational-engine-md)
> memory/storage/native C search (the Vertical Integration Law). Current builds
> retain Vexspoke allocation; permission is not implemented engine integration.
> Migration is staged, with no automatic schema migration or C/Rust atomic-layout
> assumption. R1 owns lifetimes/residency; GPU shaders/dispatch remain Graphvex.
> Central home for SPIR-V shaders (the SPIR-V Shader Deployment Law). Owns GPU buffers, bindless descriptors, meshlets, fonts, SDF rasterization, and render passes.

---

## The Graphvex Standard: The Modern Bindless GPU Driver

Graphvex rejects outdated OpenGL fixed-function wrappers, bloated cross-platform rendering engines, and unnecessary CPU-GPU memory copies. It provides a pure C23, zero-GC, hardware-native graphics substrate engineered for maximum GPU throughput:

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             THE GRAPHVEX STANDARD                                │
├─────────────────────────┬─────────────────────────┬──────────────────────────────┤
│ 1. Bindless & Off-Heap  │ 2. Dual-Path Typography │ 3. Meshlet Geometry Core     │
│ • Off-heap 2D rasters   │ • Subpixel CoreText quad│ • 128-triangle mesh clusters │
│ • BindlessHeap index    │ • JFA GPU Compute SDF   │ • Bounding cone backface cull│
│ • Zero steady-state alloc│ • .antifont binary pack │ • Direct vertex/index stream │
│ • Strict buffer bounds  │ • Scale-invariant glow  │ • Fast OBJ / glTF loaders    │
├─────────────────────────┴─────────────────────────┴──────────────────────────────┤
│ 4. Zero-Copy IOSurface Hardware Compositing + Sub-Millisecond Sync               │
│ • Zero-copy Vulkan-to-IOSurface bridge for macOS CALayer overlays               │
│ • Bounded 100ms GPU fence synchronization (the Bounded Wait Law)                  │
│ • Runtime shader resolution protocol: VEX_SPV_DIR → exe/spv → Resources → CWD   │
│ • Multi-pass render graph: shadows, depth pre-pass, post-processing FXAA/Bloom   │
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
| 1 | `Off-Heap 2D Raster Buffers` | Buffer, ColorBuffer, DepthBuffer, StencilBuffer, FrameBuffer | 💚 |
| 2 | `Specialized Spatial Buffers` | HeightBuffer, NormalBuffer, ShadowBuffer | 🟩 |
| 3 | `GPU Image & Swapchain` | Image allocation, layout barriers, Swapchain presentation, BindlessHeap | 🟩 |
| 4 | `Frame Importer & Stream Seam` | Pure RGBA8-to-Image memory upload seam with zero libav/popen weight | 🟩 |
| 5 | `Typography & Font Parsing` | TrueType parsing, glyph metrics, kerning table, native macOS font resolution | 💚 |
| 6 | `SDF GPU Compute Engine` | Jump-Flood Algorithm (JFA) compute shaders, SDF combine, distance field atlas | 💚 |
| 7 | `Vector Drawing & Shapes` | Drawable, LayeredDrawable, VectorDrawable, Bezier curves, Shape primitives | 🟩 |
| 8 | `Brushes & Stroke Extrusion` | Stroke miter/round joins, line caps, RasterBrush, VectorBrush | 🟩 |
| 9 | `Meshes & Meshlet Geometry` | Vertex/Index Mesh containers, 128-triangle Meshlet clusters, cone culling | 🟩 |
| 10 | `Command Recording & Sync` | CommandBuffer, CommandQueue, bounded Fence sync (the Bounded Wait Law), Semaphore barriers | 🟩 |
| 11 | `Scene & Pipeline State` | Retained GPU Scene, Pass load/store ops, Pipeline cache, VkView uniforms | 🟩 |
| 12 | `Zero-Copy IOSurface Interop` | `vk_iosurface.c` bridging Vulkan render targets to macOS CALayers | 🟩 |
| 13 | `SPIR-V Registry & Resolution` | Central shader directory, automated build script, 4-tier lookup protocol | 🟩 |
| 14 | `3D Shading & Mesh Parsers` | Wavefront OBJ parser, minimal lit directional pipeline, procedural floor grid | 🟧 |
| 15 | `Advanced Compute & Lighting` | PBR Cook-Torrance BRDF, GPU particle system, Order-Independent Transparency | ⬜ |

---

## Detailed Mini-Achievements Breakdown

### Filter vocabulary (`src/filter/`)

| Capability | Scope & Technical Details | Status |
|:---|:---|:---:|
| Filter operation registry and token constructors | Canonical registry and pure constructors including HSL/HSV; CPU color extension reverted. Vulkan ColorPass executes brightness/contrast, grayscale/channel grayscale, invert and B&W with `../../../tests/graphvex/compositor/color_pass_test.c` GPU pixel/order/lifetime proof. Other effects, typed parameter allocation/COW/migration, automatic scope/tree attachment and other-platform GPU proof remain gaps. | 🟨 |
| Explicit GPU scopes and gallery scatter | `compositor/gpu_scope` binds real Vulkan additive float scatter and scope composition shaders. Backdrop prefix replacement, clipped foreground and whole-element halo use one GPU pipeline family; gallery CPU fixture removed. `../../../tests/graphvex/compositor/gpu_scope_test.c` proves numeric radius/alpha/clip/spill/rejection/retry plus injected timeout retention; `../../../tests/graphvex/compositor/filter_gallery_fixture_test.c` executes all three 360x300 GPU views. One final Image/Picture bridge readback, no CPU filtering. Automatic tree/rounded scopes, zero-copy display, OOM/real device-loss and other-platform proof remain gaps; migrated gallery appearance is user-owned. | 🟨 |

### 1. Off-Heap 2D Raster Buffers (`src/buffer/`)

Foundational 2D pixel memory containers allocated outside the garbage collector.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 1.1 | Base Raster Buffer (`Buffer`) | Off-heap 2D byte buffer with width, height, stride, and pitch | 💚 |
| 1.2 | Color Buffer (`ColorBuffer`) | Packed 32-bit RGBA pixel attachment buffer with clear and blend ops | 💚 |
| 1.3 | Depth Buffer (`DepthBuffer`) | 24-bit / 32-bit floating point depth attachment buffer | 💚 |
| 1.4 | Stencil Buffer (`StencilBuffer`) | 8-bit stencil mask buffer for masking and clipping | 💚 |
| 1.5 | Frame Buffer (`FrameBuffer`) | Composite multi-attachment target binding color, depth, and stencil | 💚 |
| 1.6 | General GPU Buffer (`GpuBuffer`) | Vertex, index, uniform, and storage buffer memory allocations | 💚 |
| 1.7 | CPU-to-GPU Staging memory | Host-visible staging buffers with mapped pointer writes and unmap flushes | 🟩 |
| 1.8 | Sub-Rect Blitting & Copying | Fast memory copy of 2D sub-rectangles between raster buffers | 🟩 |

### 2. Specialized Spatial Buffers (`src/buffer/`)

Specialized buffers for 3D game engines, terrain, and lighting.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 2.1 | Height Buffer (`HeightBuffer`) | 16-bit / 32-bit elevation buffer for terrain elevation and displacement | 🟩 |
| 2.2 | Normal Buffer (`NormalBuffer`) | Tangent/world-space packed normal vector buffer for deferred shading | 🟩 |
| 2.3 | Shadow Buffer (`ShadowBuffer`) | High-precision depth target for cascaded directional shadow mapping | 🟩 |
| 2.4 | Bilinear Elevation Sampling | Smooth interpolation sampling for terrain height queries | 🟨 |
| 2.5 | Normal Map Regeneration | Generating surface normals on CPU/GPU from heightfield gradients | 🟨 |

### 3. GPU Image, Textures & Bindless Heap (`src/image/`, `src/vulkan/texture/`)

Vulkan image resources and descriptor table management.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 3.1 | Vulkan Image Wrapper (`Image`) | Allocating `VkImage` and `VkDeviceMemory` with dimension attributes | 🟩 |
| 3.2 | Image Layout Transition Barriers | Pipeline barriers executing layout transitions (Undefined → Color → Shader Read) | 🟩 |
| 3.3 | GPU Texture Upload & Mipmaps | Uploading uncompressed pixel arrays with automated mipmap generation | 🟩 |
| 3.7 | Texture Replace Retire Ring | Same-size replace = in-place sub-update; resize retires old row on bounded RETIRE_MAX 8 ring (fence-or-2-frame reap, no DeviceWaitIdle/QueueWaitIdle, 100ms bounded uploads); proof `_tests/graphvex/texture_retire_test` | 🟩 |
| 3.4 | Sampler Configuration Cache | Nearest, linear, clamp-to-edge, repeat, and anisotropic samplers | 🟩 |
| 3.5 | Bindless Heap Indexing (`BindlessHeap`) | Global descriptor indexing table allowing shader access without rebinding | 🟩 |
| 3.6 | Swapchain Presentation Engine | Managing swapchain images, semaphores, and presentation queues | 🟩 |

### 4. Frame Importer & Media Seam (`src/image/frame_importer.c`)

Pure memory upload seam for external video and media streams (the Vertical Integration Law managed exception).

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 4.1 | Zero-Dependency memory Seam | Pure RGBA8-to-Image upload interface with zero linked `libav` or `popen` | 🟩 |
| 4.2 | PBO Asynchronous Upload Ring | Staged texture stream uploading 60fps video frames without CPU stalls | 🟨 |
| 4.3 | YUV-to-RGBA Compute Shader | GPU compute conversion from NV12 / YUV420 to RGB textures | ⬜ |

### 5. Typography, Font Metrics & macOS Resolution (`src/font/`, `src/objc/`)

High-precision vector typography and glyph layout metrics.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 5.1 | TrueType File Parsing | `stb_truetype.h` integration loading TTF/OTF tables from memory | 💚 |
| 5.2 | Glyph Metrics & Bounding Boxes | Extracting advance width, left side bearing, ascent, descent, line gap | 💚 |
| 5.3 | Kerning Pair Cache | Fast hashtable lookup for typographic kerning adjustments | 🟩 |
| 5.4 | Native macOS System Font Resolution | `font_cocoa.m` resolving system font paths (San Francisco, Helvetica) | 🟩 |
| 5.5 | Custom Binary Font Packaging | Serializing baked fonts into fast `.antifont` binary packages in `~/vex/fonts` | 🟩 |
| 5.6 | Subpixel Text Layout Shaping | Translating character strings into precise glyph pen coordinates | 🟩 |

### 6. SDF GPU Compute Engine & Font Atlas Baking (`src/font/`, `src/vulkan/sdf_gpu.c`)

Scale-invariant signed distance field generation accelerated via Vulkan compute.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 6.1 | Glyph Bitmap Rasterization | Rendering high-resolution glyph alpha masks into atlas staging memory | 💚 |
| 6.2 | Jump-Flood Algorithm Compute (`sdf_jfa.comp`) | Log(N) GPU compute shader generating high-precision distance fields | 💚 |
| 6.3 | SDF Combine Shader (`sdf_combine.comp`) | Finalizing signed distance values into compact 8-bit / 16-bit texture atlases | 💚 |
| 6.4 | Vector Text Shader Pipeline (`text_sdf.frag`) | Rendering text at arbitrary zoom scales with crisp subpixel edges | 💚 |
| 6.5 | Realtime Text Outlines & Glow | Dynamic procedural stroke width and glow radius computed in fragment shader | 🟩 |
| 6.6 | Dynamic Font Atlas Packing | Guillotine/Skyline 2D bin packing algorithm packing glyphs into atlas | 🟩 |

### 7. Vector Drawing & Shape Primitives (`src/draw/`, `src/vector/`)

Retained vector paths, bezier curves, and procedural 2D geometry.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 7.1 | Polymorphic Drawable Interface (`Drawable`) | Base virtual table for all 2D/3D renderable nodes | 🟩 |
| 7.2 | Layered Drawable Composite (`LayeredDrawable`) | Z-ordered multi-layer draw list with front-to-back sorting | 🟩 |
| 7.3 | Vector Drawable (`VectorDrawable`) | Cubic and quadratic bezier curve path representation | 🟩 |
| 7.4 | Multi-Path Layered Vector Composite | Layered vector art with individual path fills and strokes | 🟩 |
| 7.5 | Vector Shape Primitives (`Shape`) | Procedural generation of Rectangles, Circles, Ellipses, Rounded Rectangles | 🟩 |
| 7.6 | Polygon Triangulation | Ear-clipping triangulation converting arbitrary 2D polygons to triangle fans | 🟨 |

### 8. Brushes & Stroke Extrusion (`src/paint/`)

Drawing studio strokes and path outlines.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 8.1 | Stroke Geometry Pipeline (`Stroke`) | Expanding 1D path centerlines into 2D triangle strips | 🟩 |
| 8.2 | Line Join Styles | Miter, Bevel, and Round join geometry generation | 🟩 |
| 8.3 | Line Cap Styles | Butt, Square, and Round line cap generation | 🟩 |
| 8.4 | Raster Stamp Brush (`RasterBrush`) | Texture-based dabs stamped along cursor trajectory with spacing control | 🟩 |
| 8.5 | Vector Extrusion Brush (`VectorBrush`) | Smooth continuous ribbon extrusion with pressure dynamics | 🟩 |
| 8.6 | Pressure & Tilt Dynamics | Modulating stroke width and opacity based on tablet pen pressure | 🟨 |

### 9. Meshes & Meshlet Geometry (`src/mesh/`)

High-performance 3D mesh representations and modern GPU meshlet culling.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 9.1 | Vertex Buffer Containers (`Mesh`) | Interleaved vertex attributes (Position, Normal, UV, Color, Tangent) | 🟩 |
| 9.2 | Index Buffer Containers | 16-bit and 32-bit triangle index buffers | 🟩 |
| 9.3 | Meshlet Partitioning (`Meshlet`) | Partitioning large meshes into bounded 128-triangle / 64-vertex clusters | 🟩 |
| 9.4 | Bounding Cone Backface Culling | Precomputing normal bounding cones for cluster-level backface culling | 🟩 |
| 9.5 | Bounding Sphere Frustum Culling | Fast frustum culling per meshlet prior to rasterization | 🟩 |
| 9.6 | Mesh Normal & Tangent Calculation | Generating smooth vertex normals and MikkTSpace tangents | 🟨 |

### 10. Command Recording & GPU Synchronization (`src/sync/`)

Low-overhead command submission and bounded thread safety.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 10.1 | Command Buffer Recording (`CommandBuffer`) | Recording Vulkan draw calls, dispatches, and pipeline barriers | 🟩 |
| 10.2 | Command Queue Dispatch (`CommandQueue`) | Submitting command buffers to Graphics, Compute, and Transfer queues | 🟩 |
| 10.3 | 100ms Bounded GPU Fence Wait (`Fence`) | `Fence_waitBounded()` enforcing the Bounded Wait Law timeout to prevent GPU hangs | 🟩 |
| 10.4 | GPU-to-GPU Semaphores (`Semaphore`) | Queue-to-queue synchronization for compute-to-graphics handoffs | 🟩 |
| 10.5 | Multi-Threaded Command Pools | Thread-local command pools for parallel secondary command recording | 🟨 |

### 11. Scene & Pipeline State Management (`src/scene/`, `src/vulkan/`)

Retained graphics state and uniform bindings.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 11.1 | Retained GPU Scene (`Scene`) | Tree of active drawables rendered in depth order | 🟩 |
| 11.2 | Render Pass Descriptor (`Pass`) | Configuring color/depth attachments with Clear, Store, and DontCare ops | 🟩 |
| 11.3 | Pipeline State Cache (`Pipeline`) | Caching compiled graphics and compute pipelines | 🟩 |
| 11.4 | Camera View Uniforms (`VkView`) | View matrix, projection matrix, camera position, and viewport rect | 🟩 |
| 11.5 | Scene Presentation Bridge (`VkScene`) | Executing scene draw calls directly into target swapchains | 🟩 |

### 12. Zero-Copy IOSurface Interop (`src/vulkan/vk_iosurface.c`)

macOS hardware layer compositing without readback overhead.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 12.1 | IOSurface-Backed Vulkan Image | Creating `VkImage` bound directly to Apple Silicon `IOSurfaceRef` memory | 🟩 |
| 12.2 | Zero-Copy CALayer Blit Seam | WindowServer compositing rendered surfaces directly into AppKit CALayers | 🟩 |
| 12.3 | Dynamic IOSurface Reallocation | Resizing hardware IOSurface buffers on window dimension changes | 🟩 |
| 12.4 | Metal Texture Cache Interop | Fast binding of IOSurface to Metal texture handles | 🟩 |

### 13. Central SPIR-V Registry & Resolution Protocol (`shader/`)

Central repository for all ecosystem shaders and runtime discovery rules (the SPIR-V Shader Deployment Law).

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 13.1 | Centralized Shader Directory | All vert/frag/comp sources located in the repo's `src/shaders/` | 🟩 |
| 13.2 | Automated glslang Compilation Script | `build_shaders.sh` compiling all shaders into `.spv` binaries | 🟩 |
| 13.3 | 4-Tier Shader Resolution Protocol | Runtime lookup order: `VEX_SPV_DIR` → `<exe>/spv` → `Resources/spv` → `CWD` | 🟩 |
| 13.4 | Core Staged Shader Suite | Built-in `hello_triangle`, `solid_quad`, `text_sdf`, `texture_quad` binaries | 🟩 |
| 13.5 | SPV Change Detector | `SpvWatch` mtime snapshots over the blob chain feeding `Vk_reloadShaders` (migrated from hotcwap) | 🟩 |
| 13.6 | Vulkan Module Loader | `vk_loader.c` dylib module protocol with trampoline swap + pipeline-cache persist (dormant, seam rewire pending) | 🟧 |

### 14. 3D Shading & Mesh Parsers

Geometry importing and basic 3D rendering.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 14.1 | Wavefront OBJ Mesh Parser | Fast text parser in CPU VFS extracting vertices, normals, and UVs | 🟧 |
| 14.2 | Minimal Lit Directional Pipeline | Vertex/fragment shader implementing flat/Phong shading with 1 light | 🟧 |
| 14.3 | Procedural Floor Grid Pipeline | Blender-style infinite ground grid shader rendered at `y=0` | 🟧 |
| 14.4 | Binary glTF 2.0 Loader (`.glb`) | Loading glTF meshes, materials, and scene hierarchies | ⬜ |

### 15. Advanced Compute & Modern Rendering Roadmap

Next-generation graphics pipelines for Anti and high-end tools.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 15.1 | PBR Cook-Torrance Material Pipeline | Metallic-roughness BRDF, image-based lighting (IBL) environment maps | ⬜ |
| 15.2 | GPU Compute Particle System | Emitter, physics simulation, and billboarding executed entirely on GPU | ⬜ |
| 15.3 | Order-Independent Transparency (OIT) | Per-pixel linked lists or compute tile buckets for glass and UI blending | ⬜ |
| 15.4 | Post-Processing Render Graph | HDR tone mapping (ACES), bloom with downsample/upsample blur, FXAA | ⬜ |
| 15.5 | SVG Vector-to-SDF JFA Baker | Realtime baking of arbitrary SVG paths to SDF textures via compute | ⬜ |
| 15.6 | Dynamic Icon Texture Atlas Packer | Runtime SDF packing of Lucide/Tabler vector icons | ⬜ |
| 15.7 | Hardware Ray Tracing Pipeline | `VK_KHR_ray_tracing_pipeline` acceleration structure building and tracing | ⬜ |

---

## Strategic Implementation Priorities for Graphvex

1. **P0: Complete Minimal Lit & Floor Grid Pipelines**
   - Implement `minimal_lit.vert`/`frag` for single directional light 3D rendering (unblocks `Object3D` and `Viewer3D`).
   - Implement `floor_grid.vert`/`frag` for the editor visual ground plane.

2. **P1: Wavefront OBJ Parser Wire-Up**
   - Finalize OBJ loader reading models directly into `Mesh` and `Meshlet` structs.

3. **P2: glTF 2.0 Binary Loader (`.glb`)**
   - Build lightweight glTF parser for modern PBR asset loading.

4. **P3: Post-Processing Render Graph**
   - Implement basic HDR tone mapping and FXAA anti-aliasing pass.

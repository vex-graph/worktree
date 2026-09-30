# Swapchain-free single-seam migration — proposed plan

## Background and invariant

Target hierarchy: hotcwap `NSWindow` owns the window; its `NSView` routes window,
mouse and keyboard events; darling `Frame` attaches one `NSVisualEffectView` and
exactly one on-screen `CAMetalLayer`. Graphvex renders scene and content into
two retained, offscreen Vulkan Boards and composites their images at anchored
native-pixel rectangles within the seam. Only the Metal drawable is displayed;
no `VkSwapchainKHR`, `VkSurfaceKHR` WSI presentation, per-panel swapchain or
periodic presentation survives in the active path.

The user observed a screen height of 1506 physical pixels; **not a constant**.
The seam's `drawableSize` is the **window content area's** native-pixel extent,
which only equals the screen's physical height when the window covers that
screen area. Obtain its size at runtime from AppKit backing conversion; derive
board geometry from those bounds. Use points only for AppKit/Core Animation
frames, pixels for GPU targets, and recompute on resize, fullscreen, zoom and
display-scale changes.

**Refinement from the user:** A Frame's two Boards are private and allocated
at the *current display mode's physical pixel width and height*, not the
smaller window drawable's size. The public inputs are borrowed Panel roots
(`Frame_setContentPanel`, `Frame_setScenePanel`), not Boards. The drawable
tracks window-content backing pixels; composite an unscaled crop of each
  monitor-sized Board into it, mapping panel-resolution pixels to the layer's
  backing pixels at presentation. Query the current display's **native panel
  resolution**, not the active HiDPI mode's larger backing allocation: among
  `CGDisplayCopyAllDisplayModes`, select the highest 1:1 mode (logical mode
  dimensions equal its pixel dimensions). Re-query on display moves.
  The CLI reports panel resolution 2408x1506; the active Retina backing is
  3274x2048 and the desktop layout is 1637x1024 points. None is hardcoded.

Existing state: `Frame` can hold two Boards, `VkGraphics` can render/snapshot
them and composite them into an RGBA offscreen image, and `GraphicsLoop` already
gates rendering on demand. But `VkGraphics_present` currently blits that image
into `VkSwapchain` and calls `vkQueuePresentKHR`. `frame_cocoa.m` builds a
Vulkan WSI surface from the layer. The archived darling compositor and panel
bridge are not part of the current build; do not resurrect them accidentally.

## Proposed changes by owner

### graphvex (GPU driver; first)

- Replace windowed Vulkan WSI device/presentation with an offscreen Vulkan
  device and an explicit macOS bridge from the completed RGBA Vulkan canvas to
  a Metal drawable. Prefer an interoperable, retained GPU resource (e.g.
  supported Metal/IOSurface export) with explicit Vulkan/Metal completion and
  ownership; validate capability on this machine before committing to an API.
  If no supported zero-copy route exists, agree on a retained staging-buffer
  fallback rather than pretending the drawable is a Vulkan image.
- Delete `src/vulkan/vk_swapchain.{h,c}`, associated CMake wiring, extension
  probing, present-wait/release helpers and swapchain tests once the replacement
  passes real window presentation tests. Retain only Vulkan offscreen image,
  board and compositing APIs; avoid confusing the graphvex presentation Surface
  with a Vulkan WSI surface.
- Ensure board resize invalidates/recreates cached Vulkan target images only
  after bounded completion, and that old targets cannot outlive their Board.
- Update driver tests for no-swapchain device creation, board resize, drawable
  presentation, demand-gating and teardown.

### darling-framework (frame/compositor; next)

- Make `objc/frame_cocoa.m`'s one `CAMetalLayer` the on-screen owner: obtain a
  drawable only when a frame is demanded, encode the transfer/composite to its
  Metal texture, present, and maintain balanced Core Animation transactions.
- Have `Frame` privately own exactly the scene/content Board pair, sized to
  the current monitor's physical pixel dimensions. Derive Panel/Scene anchor
  rectangles from live seam bounds on every relevant size or scale change;
  sample the relevant Board region and scale it into the Retina backing
  drawable without conflating the two pixel domains. Preserve a
  clearly defined
  offscreen Frame path for tests.
- Delete or migrate parked panel/surface/compositor implementations that
  conflict with the new source of truth; update the active build and tests.

### hotcwap (host/window; as required)

- Preserve `NSWindow` ownership and `NSView` event routing. Remove obsolete
  swapchain/layer-slot contracts and update resize/teardown comments and
  repo-local preferences so they describe the single Metal seam accurately.

### workspace demo, tests and documentation (last)

- Move the demo's direct-to-seam UI drawing into the Frame's private content
  Board; use Panel/Scene root geometry derived from Frame seam bounds.
- Remove stale swapchain references from active headers, build wiring, tests,
  preferences and architecture docs, including any conflicting parked source;
  inspect non-macOS backends separately so no platform regresses silently.
- Preserve unrelated uncommitted changes in all independent repositories.
  Make cohesive per-repo commits only if requested; never push.

## Trade-offs / approval questions

1. **Screen vs window:** recommended interpretation is *window-content native
   pixels* from `CAMetalLayer.drawableSize`, not a fixed full-display canvas.
   A fullscreen window can coincide with the screen's 1506-pixel height.
2. **Anchors:** borrowed Panel/Scene roots own their placement and sizing;
   the Frame resolves those roots against the live window bounds.
3. **Interop:** the bridge must be proven on this Mac. A GPU-sharing path is
   preferred; a retained CPU staging fallback has bandwidth/latency cost.
4. **Removal scope:** remove all live swapchain code and current architectural
   claims. Historical snapshots outside active repositories should remain
   archival unless explicitly requested for deletion.

## Verification before acceptance

- Verify driver interop feature support; exercise one real on-screen drawable.
- Compile affected repos/superbuild with `-Wall -Wextra -Werror`; run unit and
  integration tests, plus a real macOS launch.
- Trace resize, fullscreen, zoom, display migration, repeated content-only
  frames, retained board reuse, background/minimize, and shutdown.
- Search active source/build/tests/preferences/docs for `VkSwapchain`,
  `VkSurfaceKHR` WSI and `vkQueuePresentKHR`; confirm no active presentation
  implementation or obsolete wiring remains. Confirm one CAMetalLayer and
  on-demand drawing with correct native-pixel dimensions.

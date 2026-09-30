# Swapchain-free seam — implementation walkthrough

## Changed

- `graphvex`: deleted Vulkan swapchain implementation/test/build wiring and
  removed Vulkan WSI creation and presentation extension requirements. Surface
  now retains only the borrowed native layer handle and runtime pixel extent.
  Offscreen Vulkan rendering produces an RGBA canvas in a retained readback
  buffer. Cached Board render targets are recreated when Board size changes.
- `darling-framework`: Frame privately owns two monitor-sized Vulkan Boards.
  Consumers attach borrowed `Panel *` roots with `Frame_setContentPanel` and
  `Frame_setScenePanel` (a `Scene` has a Panel prefix); neither public setter
  takes or exposes a Board. The frame resolves panel anchors against the live
  window bounds, paints their trees into its Boards, and crops the native-pixel
  monitor-sized image into the seam using the appropriate panel-to-backing
  scaling, independently of window-content backing bounds. Cocoa derives
  Board dimensions from the highest 1:1 display mode, not the active HiDPI
  mode's backing dimensions. Screen point dimensions supply the conversion
  between Panel coordinates, monitor-resolution Board coordinates and the
  separately sized CAMetalLayer drawable.
  The completed canvas is displayed using
  a retained BGRA Metal upload texture and a CAMetalLayer drawable. GPU work
  in flight is checked before reusing that texture; the loop retries failed
  or deferred presents.

## Resize correction

- Prior code resized the CAMetalLayer drawable, Device/Surface and Vulkan seam
  image to every window backing-pixel extent. That destroyed and recreated
  image, buffer, framebuffer, Metal upload texture and drawable storage during
  a drag. These resources now stay at the selected **2408 × 1506 display
  resolution** on this monitor. The layer frame remains the display's logical
  size, pinned top-left; the window's host view clips it. Normal resize only
  updates panel layout and the visible crop. Display moves/mode changes are
  the exceptional reallocation path.
- `Frame_platformDisplay` no longer reads pixels on the CPU. On Apple the
  seam `VkImage` is created with `VkExportMetalObjectCreateInfoEXT`
  (`VK_EXT_metal_objects`) and exported to an `MTLTexture`;
  `VkGraphics_borrowMetalTexture` returns it after a bounded fence wait once
  the frame is complete. The Metal compositor samples that borrowed texture in
  a `texture2d<float>` render pass that writes the drawable directly and
  presents it, so channel handling stays GPU-side.
- A whole-frame CPU readback, channel swap and texture upload path existed
  during development; it was removed once the export path was proven. The
  host still owns presentation: `Frame_platformDisplay` obtains the drawable
  and commits the Metal command, and draws only when the previous Metal
  command has completed (`Frame_platformCanRender`), so the Vulkan target is
  never rewritten while Metal still samples it.

## GPU seam export verification

- Verified on this Mac that the offscreen Vulkan device advertises
  `VK_EXT_metal_objects` (131 device extensions) and that
  `VkGraphics_hasMetalTexture` and `VkGraphics_borrowMetalTexture` succeed.
- Verified the exported texture is 64x64 `MTLPixelFormatRGBA8Unorm` and holds
  the rendered RGBA bytes exactly (Vulkan `0x112233FF` read back as
  R=0x11 G=0x22 B=0x33 A=0xFF) via a Metal consumer.
- The app window's live presentation path has not yet been visually confirmed
  in a running session; only headless tests and the standalone export probe
  have run.
- `hotcwap`: updated window-facing architectural language for the one-layer
  arrangement. No window ownership or event routing moved out of R1.

## Verification performed

- Strict `-Wall -Wextra -Werror` build of graphvex/hotcwap/darling and the
  `vk_test`, `scroll_probe`, and `frame_test` targets in `build-verify`.
- Executed `frame_test` (`frame assembly OK`), the board resize regression,
  and `ctest --test-dir build-verify --output-on-failure -j 6` (94/94 passed).
- Checked active graphvex Vulkan source for `VkSwapchain`, `VkSurfaceKHR` and
  `vkQueuePresentKHR`; none remains. No physical display dimension is coded.
- Queried the display via CLI: the panel resolution is **2408 × 1506**;
  **3274 × 2048** is the active Retina backing allocation, not the monitor
  resolution. The frame selects the panel mode at runtime. These values are
  diagnostic observations, not dimensions coded into the renderer.
- Headless Frame test uses two borrowed Panel roots without accessing Boards;
  it simulates a monitor-resolution-to-logical-size ratio different from the
  drawable's backing scale. Compositor regression verifies an explicit crop
  of a larger Board into a smaller drawable.

## Known limits / remaining cleanup

- The real AppKit presentation path has **not** been visually exercised in a
  running window. Passing a headless test is not proof of live-resize/display
  behavior or bounded drawable acquisition.
- The bridge currently reads pixels through a persistent Vulkan readback
  buffer, swaps RGBA/BGRA into retained CPU memory, then uploads to Metal.
  This is a correct-shaped compatibility transport, **not zero-copy GPU
  interop**; it has per-frame transfer cost. A proven shared-resource bridge
  would improve latency and remove the CPU copy without restoring WSI.
- Panel/Scene root placement, anchor and size come from their graphics layout
  fields; auto-sized roots follow the live window. The graphvex demo still
  uses a legacy content callback because it is a `GraphicsPanel`, not a
  darling `Panel`; its callback only paints into the Frame's private content
  Board, never straight to the layer.
- Parked pre-migration compositor, software-buffer and legacy tests/docs
  remain outside the active build. They should not be mistaken for the live
  pipeline. They were not wholesale deleted because some contain pre-existing
  unrelated workspace edits; old references outside live source remain.
- No commit or push was performed.

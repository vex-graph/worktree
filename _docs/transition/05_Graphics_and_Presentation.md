# Lesson 5: Graphics, Presentation, and Synchronization

When building a native window backend on macOS (especially without GLFW) and plugging a graphics API like Vulkan or Metal into it, you have to bridge your C23 core to Apple's Core Animation and the GPU driver. 

Here is how the rendering pipeline actually connects, from the window layer down to GPU synchronization.

## 1. CALayer and CAMetalLayer
Everything drawn on a modern macOS or iOS screen is backed by **Core Animation** (`CA`).
* **`CALayer`:** The fundamental building block of Apple's UI. A layer is essentially a rectangle of pixels that the OS compositor (WindowServer) knows how to draw to the screen. Every `NSView` in your `anti` window is backed by a `CALayer`.
* **`CAMetalLayer`:** A specialized subclass of `CALayer`. Instead of holding standard UI elements (like text or buttons), it holds raw GPU textures. When you use Vulkan on macOS (via MoltenVK), MoltenVK takes your Vulkan commands and ultimately renders them into the textures provided by a `CAMetalLayer`. 

## 2. IOSurface
An `IOSurface` is Apple's low-level C framework for **sharing hardware-accelerated image buffers across different processes**.
* Why do you need it? Your engine is one process. The macOS WindowServer (which actually draws the screen) is a *different* process. 
* When your `CAMetalLayer` finishes drawing a frame, the OS needs to composite it onto the desktop. An `IOSurface` allows your engine to hand that frame's GPU memory directly to the WindowServer with **zero-copy overhead**. It's a cross-process pointer to video memory.

## 3. Layer Gravity (`contentsGravity`)
When you resize a window, the size of your `CAMetalLayer` changes instantly, but the GPU might take a few milliseconds to render a new frame at the new resolution. 
**Gravity** tells Core Animation what to do with the *old* image while waiting for the new one.
* `kCAGravityResize`: Stretches the old image to fit the new window (looks distorted).
* `kCAGravityResizeAspectFill`: Scales the image to fill the window, cropping the edges.
* `kCAGravityTopLeft`: Anchors the image to the top left, leaving blank space on the bottom/right until the GPU catches up.
In a high-performance engine, you often handle resizing manually, but gravity acts as the fallback during those microsecond window-resize transitions.

---

## 4. Vulkan Sync: Swapchains, Fences, and Semaphores
When your engine loop pushes a frame, you have the CPU (your C23 code) and the GPU running at different speeds. Synchronization prevents them from colliding.

### The Swapchain and Images
* **Swapchain:** A queue of pre-allocated textures (usually 2 or 3, known as Double or Triple Buffering). The OS owns the one currently on the monitor. You own the ones currently in the background.
* **Swapchain Image:** A single texture within that swapchain queue. You must ask the swapchain: *"Give me the next available image I can draw to."*

### Semaphores (GPU-to-GPU Sync)
A Semaphore is a signal that stays entirely on the GPU. The CPU (your engine) doesn't wait for it.
* **Image Available Semaphore:** When you ask the swapchain for an image, it might not be ready yet (the monitor is still reading it). You give the GPU a command: *"Start drawing the scene, but wait for THIS semaphore before you write to the image."*
* **Render Finished Semaphore:** When the GPU finishes drawing, it signals THIS semaphore. The presentation engine waits for it before slapping the image onto the screen.

### Fences (GPU-to-CPU Sync)
A Fence is a signal from the GPU to the CPU. 
* Imagine your CPU sends a command buffer to the GPU. The CPU then loops around to the next frame and wants to reuse that command buffer's memory. If the GPU is still reading it, you get a crash.
* **The Fix:** You attach a Fence to the submission. The CPU calls `vkWaitForFences`, which physically halts your C23 thread until the GPU says, *"I'm done with that memory, you can safely overwrite it."*

### Summary of a Frame Loop:
1. **CPU:** Wait on **Fence** (Wait for GPU to finish last frame's data).
2. **CPU:** Acquire **Swapchain Image** (Provides `ImageAvailableSemaphore`).
3. **CPU:** Submit rendering commands to GPU.
   * *GPU waits on `ImageAvailableSemaphore`.*
   * *GPU signals `RenderFinishedSemaphore`.*
   * *GPU signals **Fence** when completely done.*
4. **CPU:** Present the Image to the screen. (Presentation engine waits on `RenderFinishedSemaphore`).

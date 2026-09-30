# Lesson 2: The Host / Module Architecture

To achieve seamless hot-reloading, the engine is physically divided into two distinct parts: the **Host (Cradle)** and the **Hot Module (DLL)**. 

## The Host (Never Unloads)
The Host executable is the stable foundation of the engine. It owns everything that cannot or should not be destroyed during a hot reload:
1. The OS Window and Event Pump.
2. The `mem.c` global memory registry (`s_head`).
3. The Vulkan `VkInstance`, `VkDevice`, and Swapchain.
4. The Master Thread Pool.

## The Hot Module (Volatile)
The Module is compiled as a dynamic library (e.g., `vulkan.dylib` or `game.dylib`). It contains the volatile logic that programmers want to iterate on rapidly:
1. Render Graph / Pipeline setup.
2. Gameplay systems.
3. Shaders and draw calls.

## The Handshake (Context Transfer)
When the Host loads the Module, they must communicate without intertwining their memory states. This is done via **Context Passing**.

Take the Vulkan renderer (`vk_loader.c` vs `vk_module.c`) as an example.
1. The Host (`vk_loader.c`) initializes the GPU. It creates a `VkHotContext` struct containing the `VkDevice` and pipeline caches.
2. The Host loads `vulkan.dylib`. 
3. The Host calls the Module's `VkModuleInit(const VkHotContext* context)`.
4. The Module reads the context but **does not own it**. It uses the Host's `VkDevice` to create pipelines and framebuffers.

### Safe Unloading
Before the Host unloads the DLL, it calls `VkModuleShutdown()`. The DLL destroys its pipelines and render passes, but it leaves the `VkDevice` untouched. The Host then swaps in the new DLL, passes the same `VkDevice` back in, and the new DLL recreates the pipelines using updated logic.

Because the GPU device was never destroyed, the screen doesn't flicker, and the OS doesn't kill the window.

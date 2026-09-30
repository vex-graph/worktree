# Lesson 3: ID-Based Resource Tracking and Bindless Rendering

One of the greatest challenges of hot-reloading graphics code is dealing with GPU handles. If your gameplay code holds a `VkImage` pointer, and the graphics module reloads, that pointer is incredibly dangerous to serialize or deserialize.

The `anti` engine solves this by adopting a **Top-Down, ID-Based, Bindless** architecture.

## 1. ID-Based Resource Management
In `anti`, the DLL never sees a raw Vulkan handle. The Host engine acts as the **Resource Manager**. 
When the DLL needs a texture, it asks the Host: `LoadTexture("sunflower.png")`.
The Host allocates the `VkImage` memory, puts it into a private array at Slot #5, and simply returns the integer `5` to the DLL.

**Why this is genius:** Integers don't break during a hot reload. When the new DLL loads, the player's texture ID is still `5`. The Host still knows that `5` maps to the `sunflower.png` Vulkan object. No pointers were serialized, and no memory was corrupted.

## 2. Bindless Descriptor Indexing
This ID-based system pairs flawlessly with modern Vulkan's `VK_EXT_descriptor_indexing` (Bindless Rendering).

Instead of the CPU binding textures one by one (`vkCmdBindDescriptorSets`), the engine binds one massive array of 10,000 textures at the start of the frame. 
In the GLSL shader, this looks like:
```glsl
layout(set = 0, binding = 0) uniform sampler2D global_textures[];
```

Because the DLL only knows the Texture ID (e.g., `5`), it simply passes the number `5` to the GPU as a Push Constant. The GPU looks up `global_textures[5]` and draws it.

## The Hot Reload Synergy
If you modify `hot_texture.c` to swap `sunflower.png` for `other-sunflower.png`:
1. The Host loads the new image.
2. The Host overwrites Slot `5` in its private array.
3. The Host updates Index `5` in the Vulkan descriptor set.
4. The Game DLL doesn't even know it happened. It just keeps passing `ID 5` to the GPU, but the GPU is now drawing the new texture.

This creates a bulletproof separation between volatile game logic and persistent GPU memory.

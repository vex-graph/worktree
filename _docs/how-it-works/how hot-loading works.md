# How Hot-Loading Works: Per-Dylib

> Answers: **"How does a running app swap its own code without
> restarting?"**
> Answer: **dlopen a clone → verify ABI → atomic fn-ptr swap → retire
> the old handle after a grace period.**

---

## 1. The Contract: One Module One Dylib

Hot-loading is per-dylib. Each module is a `.dylib` (macOS) or `.so`
(Linux) in the watched hot directory, exporting:

```c
int  Hot_module_init(void);
void Hot_module_shutdown(void);
int  Hot_module_save(void *buf, int bufCap, int *outLen);
int  Hot_module_restore(void *buf, int len);
int  Hot_module_migrate(const char *oldVersion,
                        void *oldBuf, int oldLen,
                        void *newBuf, int newCap, int *outLen);
const HotManifest *Hot_module_manifest(void);
```

The manifest declares: name, version, type_ids (ABI surface),
exports, dependencies.

---

## 2. The Verify-Before-Commit Pipeline

Every frame, `Hot_poll` (main thread only):

```
Hot_poll
 ├─ 1. Advance retire ring generation
 ├─ 2. Scan hot_dir for .dylib/.so
 ├─ 3. New/mtime-changed?  →  clone the file (.name.clone)
 ├─ 4. dlopen the clone
 ├─ 5. Parse manifest → ABI compatibility check vs previous
 ├─ 6. Dependency gate: all deps loaded? (else retry next poll)
 ├─ 7. Save old state (256 bytes, binary)
 ├─ 8. Register trampolines with rollback snapshot
 │        (mid-list dlsym failure restores prior pointers)
 ├─ 9. Phase-2 state restore: Hot_migrate on version bump
 └─ 10. Commit: swap old handle → retire
         (on failure: dlclose clone, unlink clone, keep old)
```

The key word is **clone**: the new dylib is loaded from a cloned file,
so a partially-written build artifact is never loaded.

---

## 3. Two Manifest Conventions

| Convention | How |
|---|---|
| JSON | `Hot_manifest(json_string, len, out)` — hand-rolled parser |
| Struct | `VkModuleGetManifest()` → returns struct directly |

Both define the same fields: name, version, type_ids, exports,
dependencies. Compatibility check: `type_ids` must match by
name→value.

---

## 4. The Trampoline Table (atomic swap)

One `HotTrampolineTable` per HotModule instance. 1024 rows, each:

```c
_Atomic(void*) ptr;         // current generation target
_Atomic(void*) fallback_ptr; // prior generation (mid-swap cover)
char name[64];
```

`get(idx)` returns `ptr`, with a brief spin (4 retries + `yield` on
aarch64) if a swap is in flight, then falls back to `fallback_ptr`
rather than returning NULL. Readers never see a torn pointer.

Reload swaps a row's `ptr` while `fallback_ptr` covers mid-swap
readers. Two loaders sharing this code never collide — tables are
INSTANCE state, not globals.

---

## 5. The Retire Ring (generational dlclose)

Old dylib handles park in `HotRetireRing` for **4 poll generations**
before `dlclose`. In-flight calls drain during the grace period. Full
ring evicts the oldest entry; shutdown drains via `drainAll`.

This is why `Hot_poll` runs on main thread only: the retire ring
generation advances once per poll, and each advance expires handles
whose grace period elapsed.

---

## 6. The Vulkan Special Case

`VkLoader` is the critical piece: **the VkDevice is created here, NOT
in the vulkan module.** The device persists across module reloads.

What survives a reload (transferable):
- VkDevice, VkQueue, VkPhysicalDevice
- VkPipelineCache
- VkImage from IOSurface
- VkDeviceMemory

What must be recreated (non-transferable):
- VkPipeline, VkDescriptorSetLayout, VkRenderPass, VkFramebuffer

The transfer protocol is `VkHotContext` in `hot/vk_context.h`.

---

## 7. Shader Hot-Reload (SpvWatch)

Separate from dylib hot-loading. `SpvWatch` watches the 8 SPIR-V
shader names (hello_triangle, solid_quad, texture_quad, text_sdf,
each vert+frag) by mtime. On change:
1. Resolve through the loadSpvAny precedence chain
2. Rebuild pipelines (Phase-3 live shader reload, try-lock)

---

## 8. Key Insight

Hot-loading is three independent mechanisms with one architecture:
- **dylib swap** = clone → verify → atomic swap → retire (HotModule)
- **shader swap** = watch mtime → rebuild pipelines (SpvWatch)
- **device persistence** = VkDevice survives reloads (VkLoader)

Everything is verify-before-commit. Nothing is loaded from a
half-written file. Nothing is closed while in flight.
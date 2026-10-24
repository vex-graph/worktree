# vexspoke — R2 CPU Computation, Behavior & System Probes

> **R2 split:** Vexspoke owns CPU computation, math, algorithms, synchronization
> and behavior. [relational-engine](#file-relational-engine-md) owns memory/storage, stable row chunks,
> variable bindings and native C search. Existing storage/container rows below
> describe retained C ABI during staged collection migration. IO/NIO implementation
> and owners have moved to [relational-engine](#file-relational-engine-md) and default builds link it.
> Native allocation semantics remain unchanged; status must be checked against current
> owner evidence. No C/Rust atomic-layout equivalence or schema migration implied.

> **Architectural Tier**: R2 Behavior — pure leaf (includes nothing above it; the Vertical Integration Law).
> **Production Standard**: *The Pure Relational Leaf: Slab Arenas + BitPool Allocators + Uniform 64-bit Type Registry + Off-Heap Relational Pointer Engine + Zero Steady-State Allocation*.
> **Governing Laws**:
> 1. **Reference form**: `(*ptr).field` always, never `->` (the Semantic Consistency Law (Reference form)).
> 2. **Cast spelling**: `(T*) ptr`, space after the closing parenthesis (the Semantic Consistency Law (Cast and pointer spelling)).
> 3. **Dest-last parameter order**: `fn(src, dest)` (the Semantic Consistency Law (Argument order)).
> 4. **Two-layer access cap**: base + offset only, zero pointer chasing (the Semantic Consistency Law (Access depth)).
> 5. **Everything is a Pointer**: every symbol maps to an address in off-heap memory.
> 6. **16-Byte Arena Doctrine**: 16-byte `MemoryHeader` prefix (`[typeId u64][length u32][sugar u32]`) with negative pointer math O(1) header recovery.
> 7. **Bounded Wait Law**: max 100ms wait with drop-degrade on timeout.
> 8. **GPU ownership:** GPU shaders, dispatch and driver resources belong to R3 [graphvex](#file-graphvex-md). Vexspoke is an R2 CPU leaf; the responsibility split does not move GPU work into either R2 repository.

---

## Subsystem 1: Master Arena memory (`nio/mem`)

This implementation and owner proof now belong to [relational-engine](#file-relational-engine-md), not
Vexspoke. The historical ABI inventory below is not Vexspoke implementation proof.

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 1.1 | Engine 16-Byte MemoryHeader Layout | `[typeId (64b)][length (32b)][sugar (32b)]`; tests/relational-engine/nio/mem_test.c | 🟨 | Engine-owned ABI; header geometry preserved, not rewritten into Rust. |
| 1.2 | 16-Byte Payload Alignment | Payloads satisfy `(uintptr_t)p & 15 == 0` | 💚 | Enforced by construction on Apple Silicon and POSIX malloc. |
| 1.3 | O(1) Negative Pointer Recovery | Read `MemoryHeader` via `(MemoryHeader*)userPtr - 1` | 💚 | Zero locking, single subtraction, instant metadata reads. |
| 1.4 | Master Arena Initialization | `Memory_init(size_t totalBytes)` | 💚 | Carves master slab arena (default 64MB lazy init). |
| 1.5 | Power-of-Two Slab Buckets | Partitioning into size-class slabs | 💚 | O(1) slot claiming and cache-hot recycling. |
| 1.6 | O(1) Slab Allocation | `Memory_alloc(typeId, numBytes)` | 💚 | Stamps the typeId and the recomputed `sugar` veto; no magic cookie. |
| 1.7 | Slab Free-List Recycling | `Memory_free(void *userPtr)` | 💚 | Pushes slot back onto slab freelist in O(1) cache-hot time. |
| 1.8 | In-Place & Realloc Growing | `Memory_realloc(void *userPtr, size_t newBytes)` | 💚 | Preserves header typeId and payload contents. |
| 1.9 | Type & Length Introspection | `Memory_type(ptr)` and `Memory_length(ptr)` | 💚 | Pure header reads, O(1), thread-safe without locks. |
| 1.10 | Type-Filtered Pointer Scan | `Memory_findAll(typeId, outArray, maxCount)` | 💚 | Scans active slab blocks matching target type ID. |
| 1.11 | Always-Last Teardown | `Memory_freeAll(void)` | 💚 | Resets all slabs in O(1); the Vertical Integration Law (Teardown) sink. |
| 1.12 | Isolated Secondary Arenas | `MemoryArena_create`, `MemoryArena_destroy` | 🟩 | Arena-B instancing; isolated slab sets without polluting global. |
| 1.13 | Address-Range Registry Dispatch | Free routes to correct arena via address range | 🟩 | Bounded registry (default + 3 secondary arenas). |
| 1.14 | Transient Frame Allocator | `Transient_alloc(typeId, numBytes)` | 🟩 | Linear bump allocator for per-frame scratchpads. |
| 1.15 | Transient Reset & Generation Tag | `Transient_reset(void)`, `Transient_getGeneration()` | 🟩 | O(1) bump reset with generation counter for stale pointer detection. |
| 1.16 | Lifetime Borrow Checker | `Memory_getLifetime(ptr)` & `DEBUG_BORROW_CHECK` | 🟩 | Flags transient pointers stored into permanent arenas. |

---

## Subsystem 2: Lock-Free BitPool Allocators (`bit/bit`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 2.1 | Tagged ABA Free-List Head | `_Atomic uint64_t free_head` | 💚 | Upper 16 bits ABA counter, lower 48 bits pointer. |
| 2.2 | Fixed-Width Slot Layout | `BitSlot` header `[type_id][length][pad][_Atomic next]` | 💚 | Direct payload pointer return; walking back finds header. |
| 2.3 | BitPool Initializer | `BitPool_init(pool, element_size, capacity)` | 💚 | Single calloc'd arena, strictly non-growing. |
| 2.4 | Lock-Free CAS Alloc | `BitPool_alloc(pool, type_id)` | 💚 | Atomic CAS pop from tagged free list; zero syscalls. |
| 2.5 | Lock-Free CAS Free | `BitPool_free(pool, user_ptr)` | 💚 | Atomic CAS push back to tagged free list with incremented ABA tag. |
| 2.6 | Arena Bounds Verification | `BitPool_contains(pool, user_ptr)` | 💚 | Validates pointer falls inside pool's continuous arena bounds. |
| 2.7 | BitPool Metadata Helpers | `BitPool_type(pool, ptr)`, `BitPool_length(pool, ptr)` | 💚 | Safe header reads for mixed-allocator primitives. |
| 2.8 | Dedicated Width Pools | Global pools for `Bit8`, `Bit16`, `Bit32`, `Bit64` | 🟩 | Avoids internal slab fragmentation for scalar primitives. |

---

## Subsystem 3: Type Registry (`oop/type`) — algebra owned by [relational-engine](#file-relational-engine-md)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 3.1 | vexspoke Class Registry | `oop/type.h` `ID_*`/`TYPE_*` ids (includes the engine `type/type.h`) | 🟩 | Owns only vexspoke's 1-based class numbers. The 64-bit encoding, form/modifier/wrapper tags, `Type_make`/`Type_class`, `Type_arch` and the parent-chain resolver (`Type_registerParents`/`Type_registerBareParents`/`Type_isA`) moved to [relational-engine](#file-relational-engine-md) `type/type`; proven by tests/relational-engine/type/type_algebra_test.c. |
| 3.12 | Field Descriptor Registry | `Field` struct `[name, offset, size, classId, isStruct]` | 💚 | Dynamic reflection metadata for C structs. |
| 3.13 | Struct Stride Calculation | `Stride` calculator with 16-byte alignment padding | 💚 | Computes off-heap struct offsets matching C ABI padding. |

---

## Subsystem 4: Relational Symbols & Spotlight Engine (`relational/variable`, `relational/relational`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 4.1 | 32-Byte String Slot / 16-Byte Symbol Row | `StringSlot` `[self 8B][name 24B]`; `SymbolRow` `[slot u32][classId u32][pointer u64]` | 💚 | Name slot = intrusive self link + exact 24-byte name; the symbol row maps a name to a typed address. |
| 4.2 | Lowercase Name Canonicalization | 24-byte name (23 chars + NUL) folded lowercase, compared with a 24-byte `memcmp` | 💚 | Fast fixed-width name equality without a NUL scan. |
| 4.3 | Open-Addressing Symbol Map | 40-byte map slots (4 longs name + varId) with linear probe | 💚 | Fast O(1) string symbol resolution without malloc. |
| 4.4 | Symbol Registration | `Variable_instant(v, name, classId, targetPointer)` | 💚 | Registers or updates symbol with assigned varId. |
| 4.5 | Symbol Rename | `Variable_rename(v, oldName, newName)` | 💚 | Atomic name switch; verifies old exists and new is free. |
| 4.6 | Atomic CAS on Pointers | `Variable_compareAndSetPointer(v, varId, exp, newPtr)` | 💚 | Lock-free pointer swapping for hot reload state migration. |
| 4.7 | Dual-Scope Hierarchy | `Relational` facade over Global and Local `Variable` tables | 💚 | Local overrides global; clean lexical scoping. |
| 4.8 | Typed Value Getters/Setters | `Relational_getValue`, `Relational_setValue` | 💚 | Direct pointer exchange without data copies. |
| 4.9 | Managed String Symbols | `Relational_getString`, `Relational_setString` | 💚 | Auto-reclaims old string blocks on symbol reassignment. |
| 4.10 | Function Pointer Binding | `Relational_getFunction`, `Relational_setFunction` | 💚 | Binds executable code blocks `void (*)(void*)` as relational symbols. |
| 4.11 | Spotlight Substring Search | `Relational_search(scope, query, outIds, cap)` | 💚 | Ranks exact matches > prefix matches > substring matches. |
| 4.12 | Combined Scope Search | `Relational_searchAll(global, local, query, outIds, cap)` | 💚 | Unified search across local and global symbol registries. |

---

## Subsystem 5: C23 Ergonomics & Dispatch (`c23/*`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 5.1 | Macro Constructor Dispatch | `CONSTRUCTOR_DISPATCH(Name, ...)` | 💚 | Arity-overloaded constructors `Name_0` to `Name_8`. |
| 5.2 | ISO C23 Comma Elision | `__VA_OPT__(,) __VA_ARGS__` | 💚 | Standard portable macro dispatch without compiler extensions. |
| 5.3 | Generic Type Overloading | `_Generic` arithmetic overloads for `add`, `sub`, `mul`, `div` | 💚 | Dispatches based on operand types to C-promoted scalar/vector math. |
| 5.4 | Dual Arity Math Forms | Value form `add(a, b)` vs Dest-last form `add(a, b, &dest)` | 💚 | Value form for pure math; dest-last form for zero copy (the Semantic Consistency Law (Argument order)). |
| 5.5 | Vector Broadcast Arithmetic | `v op s` and `s op v` for Vec2, Vec3, Vec4 with float/double | 💚 | Full elementwise scalar broadcast. |
| 5.6 | Matrix-Vector Overloads | `mul(Mat4, Mat4)` and `mul(Mat4, Vec4)` via `_Generic` | 💚 | Matrix multiplication and coordinate transformations. |
| 5.7 | Compile-Time Overload Errors | `ov_type_error` on unsupported type combinations | 💚 | Loud compile-time failure rather than silent incorrect casts. |
| 5.8 | Schema-Driven Deep Equality | `isEqual(const void *a, const void *b)` | 💚 | Type header check -> length check -> `Fields` schema comparison. |
| 5.9 | Padding-Immune Comparisons | `equalsFields` skips C struct padding holes | 💚 | Only registered fields are compared via memcmp. |
| 5.10 | Relational Symbol Equality | `isEquallyNamed(v, nameA, nameB)` | 💚 | Resolves two symbols and runs schema-driven equality. |
| 5.11 | Type-Aware Destructor Free | `c23_free(ptr)` hijacking standard libc `free` | 🟨 | Dispatches custom destructors by `Memory_type` before `Memory_free`. |
| 5.12 | Memset Zero Helper | `zero(ptr)` | 🟩 | Zeroes entire payload length read from block header. |

---

## Subsystem 6: 12-Frame Spatial Coordinates & Vector Hierarchy (`math/coord_frame`, `lang/vec2/*`, `lang/vec3/*`, `lang/vec4/*`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 6.1 | 12 Orthogonal Coordinate Frames | `CoordFrame` enum (`Y_UP_LEFT` Unity default, `Y_UP_RIGHT` OpenGL, `Z_UP_RIGHT` Blender, etc.) | 💚 | Complete 12-frame basis matrix with $O(1)$ swizzle tables. |
| 6.2 | Semantic Spatial Axes | `horizontal`, `vertical`, `depth` ($x, y, z$) | 💚 | Decoupled semantic naming from physical layout. |
| 6.3 | Directional Inverse Invariant | `getBack() == -getFront()`, `getLeft() == -getRight()`, `getDown() == -getUp()` | 💚 | Setting `setBack(28)` stores `-28` in front component. |
| 6.4 | `Vec3` 16-Byte SIMD Vector | `[horizontal][vertical][depth][uint32_t frame]` | 💚 | Frame embedded directly in 4th float slot as true metadata. |
| 6.5 | `Vec3d` 32-Byte SIMD Double Vector | 32-byte double precision vector with embedded coordinate frame | 💚 | High-precision scientific simulation. |
| 6.6 | Multi-Precision Sector Vectors | `Vec3IntFloat` and `Vec3LongDouble` | 💚 | Large-world coordinate system with automatic sector rebalancing. |
| 6.7 | `Vec2` & `Vec2d` 2D Vector Systems | `(horizontal, vertical)` in `src/lang/vec2/` | 💚 | Single Class Per File with 2D coordinate frame mapping. |
| 6.8 | `Vec4` & `Vec4d` Homogenous Vectors | `(horizontal, vertical, depth, w)` in `src/lang/vec4/` | 💚 | 16-byte SIMD vector aligned for shader uniforms. |
| 6.9 | `Mat4` Struct & Layout | Column-major 16-float array `float m[16]` | 💚 | Aligned for Vulkan/Metal matrix uniforms. |
| 6.10 | Matrix Transforms & Projections | `Mat4_translate`, `Mat4_rotate`, `Mat4_perspective`, `Mat4_ortho` | 💚 | Camera and model transformation matrices. |

---

## Subsystem 7: Off-Heap Relational & Spatial Data Structures (`struct/*`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 7.1 | `Collection` Base Header | Common header for dynamic containers | 💚 | Stores `element_class`, `stride`, capacity, and element count. |
| 7.2 | `Array` Contiguous Dynamic Buffer | Dynamic growable array with capacity scaling | 💚 | Index-based reads, append, pop, and shrink operations. |
| 7.3 | `List` Doubly-Linked Node Chain | Off-heap linked list nodes | 💚 | O(1) insert/remove at head/tail. |
| 7.4 | `Map` Open-Addressing Hash Map | 32-byte slot hash table: key(8)+val(8)+hash(8)+state(8) | 💚 | Power-of-2 capacity, 0.75 load factor rehash. |
| 7.5 | Reference Key Hashing in Map | Strings and structs hashed via block header | 💚 | Off-heap pointer keys hashed safely. |
| 7.6 | `Set` Hash Set | Value-only open-addressing hash set | 💚 | Fast membership tests and deduplication. |
| 7.7 | `SparseSet` ECS Core | Dense entity array + Sparse lookup array + Component data | 💚 | O(1) add, remove (swap-back), and lookup for game entities. |
| 7.8 | `MinHeap` Priority Queue | Binary min-heap over typed priorities | 💚 | O(log N) push and pop min; used in schedulers. |
| 7.9 | `Deque` Double-Ended Queue | Circular buffer deque | 💚 | O(1) push/pop at both front and back. |
| 7.10 | `Queue` FIFO Buffer | FIFO wrapper around Deque | 💚 | Standard work queues. |
| 7.11 | `Stack` LIFO Buffer | LIFO wrapper around Array | 💚 | Call/state stacks. |
| 7.12 | Spatial `Octree` | 3D spatial partitioning tree with AABB and spherical range queries | 💚 | `src/struct/octree.c`, `octree.h`; verified in `spatial_struct_test`. |
| 7.13 | 2D `CircleArray` Matrix | 2D circular matrix evaluated via Pythagorean theorem ($dx^2 + dy^2 \le r^2$) | 💚 | `src/struct/circle_array.c`, `circle_array.h`; verified in `spatial_struct_test`. |
| 7.14 | 3D `SphereArray` Voxel Matrix | 3D spherical voxel volume evaluated via 3D Pythagorean theorem | 💚 | `src/struct/sphere_array.c`, `sphere_array.h`; verified in `spatial_struct_test`. |
| 7.15 | Fast `CircularArray` / `RingBuffer` | Atomic MPMC ring buffer with power-of-2 wrapping index mask | 💚 | `atomic/ring.c`, `ring.h`; verified in `input_test`. |

---

## Subsystem 8: Concurrency & Atomic Primitives (`atomic/*`, `thread/*`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 8.1 | C11 Atomics Wrapper | `atomic_load`, `atomic_store`, `atomic_compare_exchange` | 💚 | Standard C11 lock-free memory primitives. |
| 8.2 | User-Space `SpinLock` | Test-and-set spinlock with CPU pause hints | 💚 | Lightweight mutual exclusion for micro-critical sections. |
| 8.3 | MPMC `RingBuffer` | Fixed-capacity lock-free FIFO with power-of-2 masking | 💚 | Atomic head/tail counters, zero runtime allocation. |
| 8.4 | Concurrent `Registry` | Lock-free thread-safe pointer registry | 💚 | Shared catalog for cross-thread subsystems. |
| 8.5 | Unified `Thread` Engine | Worker thread lifecycle: spawn, join, submit, stop, free | 💚 | Pthread wrapper managing task ring and idle ticks. |
| 8.6 | Core Thread Protection | `ROLE_CORE` handles immune to routine stop/free | 💚 | Critical threads survive until `Thread_freeAllSystem()`. |
| 8.7 | Specialized Subsystem Threads | `UIThread`, `DrawThread`, `NetworkingThread`, `ScriptingThread` | 💚 | Dedicated threads for engine loop separation. |
| 8.8 | Bounded Thread Joins | 100ms max join wait before drop-degrade (the Bounded Wait Law) | 🟩 | Prevents deadlock on hanging background tasks during shutdown. |
| 8.9 | Top-Down System Teardown | `Thread_stopAll` -> `Thread_freeAll` -> `Thread_freeAllSystem` | 💚 | Adheres strictly to the Vertical Integration Law (Teardown). |

---

## Subsystem 9: Monotonic Time & Engine Clock (`time/*`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 9.1 | Engine Epoch Initialization | `NanoTime_init(void)` | 💚 | Captures process start epoch via `CLOCK_MONOTONIC_RAW`. |
| 9.2 | Raw Monotonic Nanosecond Reader | `NanoTime_now(void)` | 💚 | Microsecond/nanosecond precision without drift. |
| 9.3 | Elapsed Time Introspection | `NanoTime_elapsedNanos(void)` | 💚 | Nanos elapsed since engine startup. |
| 9.4 | Frame Timer Accumulator | `NanoTimer` tracking `deltaTime` and `totalTime` | 💚 | Computes delta between successive frame ticks. |
| 9.5 | Scalable Simulation Clock | `NanoTimer_tickWithClock(timer, clock)` | 💚 | Scales deltaTime by timeScale; freezes cleanly when paused. |
| 9.6 | Wall-Clock Calendar Primitives | `Calendar`, `DateTime`, `Clock` formatting | 💚 | ISO timestamps, local date/time string rendering. |

---

## Subsystem 10: VexHome File Hierarchy & Caches (`io/vexhome`)

Implementation and tests have moved to [relational-engine](#file-relational-engine-md); these historical
ABI rows are not current Vexspoke-owned readiness claims.

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 10.1 | Root Resolution Precedence | `$VEX_HOME` -> macOS App Support -> Windows LocalAppData -> XDG | 💚 | 5-tier resolution hierarchy for platform portability. |
| 10.2 | Canonical Directory Layout | `<root>/` with `../../projects`, `logs/`, `fonts/`, `cache/` | 💚 | Stable directory tree guaranteed before subsystems start. |
| 10.3 | Idempotent Tree Creation | `VexHome_ensure(void)` | 💚 | Creates entire directory layout safely; never fails if dirs exist. |
| 10.4 | Subsystem Cache Isolation | `VexHome_cache(subsystem)` | 💚 | Isolates caches per subsystem (e.g. `darling`, `semicolon`). |
| 10.5 | Living Cache Manifest Index | `VexHome_cacheEnsure` writes `dictionary.ini` | 💚 | Ensures cache folder and initial manifest without clobbering existing. |
| 10.6 | Default Binary Log Sink | `VexHome_defaultLogPath` -> `<root>/logs/engine.bin` | 💚 | Standard path for high-throughput engine telemetry. |

---

## Subsystem 11: Legacy Engine IO Rows (moved to Relational Engine)

Implementation and tests have moved to [relational-engine](#file-relational-engine-md). Current scoped
proof and remaining gaps are recorded there rather than inferred from these rows.

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 11.1 | Bounded Child-Job Table | Fixed 8-slot table `ProcessSpawnJob jobs[8]` | 💚 | Zero heap allocation during child process execution. |
| 11.2 | `posix_spawnp` Process Launch | Non-blocking execution without shell or `system()` | 💚 | Safe argument passing with dest-last table write. |
| 11.3 | Non-Blocking Waitpid Slices | `ProcessSpawn_poll` with ~1ms slices and 100ms max budget | 💚 | Reaps child exit codes via `WNOHANG` without blocking engine frame. |
| 11.4 | Graceful Cancellation | `ProcessSpawn_cancel` sending `SIGTERM` to active jobs | 💚 | Prevents zombie processes; allows clean reap on next poll. |
| 11.5 | Thread-Free Frame Inbox | Relational Engine `FrameInbox` with fixed 4KB pending buffer `rxBuf[4096]` | 💚 | Caller-fed bounded byte inbox; not a WebSocket client. Vexspoke `net/` owns network sockets; WebSocket protocol support is not implemented. |
| 11.6 | Bounded Frame Draining | `FrameInbox_poll` with 100ms max timeout and cancellation check | 💚 | Drains pending bytes through caller output arguments; that inbox API remains a Value Return Law migration gap. |
| 11.7 | Hot File Modification Watcher | `HotFileSys`; tests/relational-engine/io/hot_file_test.c lifecycle-only | 🟧 | Engine-owned draft no-op; no working watcher claimed. |
| 11.8 | Structured Engine Logger | `Log_info`, `Log_warn`, `Log_error`, `Log_fatal` | 💚 | Binary and text logging sinks with level filtering. |
| 11.9 | Log Stream Parser | `LogParser` decoding structured engine logs | 🟩 | Parses binary log records back into inspection structs. |

---

## Subsystem 12: Zero-Alloc JSON Document Engine (`net/json`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 12.1 | Caller-Owned Document Pool | Fixed `JsonNode` array + scratch arena | 💚 | Zero malloc anywhere; returns false on pool exhaustion. |
| 12.2 | Zero-Copy String Views | Values point directly into input string buffer | 💚 | Only escaped strings are copied into caller scratch arena. |
| 12.3 | Tree Navigation API | `Json_root`, `Json_member`, `Json_at`, `Json_count` | 💚 | Array/object element traversal with `JsonRef` indices. |
| 12.4 | Dotted Path Evaluation | `Json_path(doc, root, "a.b[0].c")` | 💚 | Fast traversal across nested objects and repeated array indices. |
| 12.5 | Null-Coalescing Getters | `Json_getBool(..., def)`, `Json_getNumber(..., def)` | 💚 | Safe fallback values on missing keys or type mismatches. |
| 12.6 | Streaming JsonWriter Builder | `JsonWriter` with fixed output buffer | 💚 | Bounded JSON stringifier with automatic comma handling. |

---

## Subsystem 13: HTTP Transport & TLS Backend (`net/*`, `objc/tls_*`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 13.1 | BSD Socket HTTP/1.1 Client | `Http_perform` with `Connection: close` semantics | 🟩 | Caller-owned buffers; zero internal heap allocation. |
| 13.2 | Embedded Micro HTTP Server | `HttpServer_start` with background accept thread | 🟩 | Ephemeral port binding, request parsing, and `Http_respond`. |
| 13.3 | RFC URL Parser | `Url_parse` decomposing scheme, host, port, path, query | 🟩 | Handles absolute and relative URLs into caller structs. |
| 13.4 | Apple Security Framework TLS | `tls_apple.m` native TLS via Network.framework | 🟧 | Currently `;;DRAFT` stub failing closed (`return false`). |
| 13.5 | Libcurl TLS Fallback | `tls_curl.c` for Linux/Windows | 🟧 | Currently `;;DRAFT` stub failing closed (`return false`). |
| 13.6 | Pluggable TLS Transport Contract | Full secure handshake, send/recv loop, certificate verification | ⬜ | Roadmap: complete wiring of native Apple Network.framework TLS. |

---

## Subsystem 14: System Probes & Discovery (`system/*`, `objc/discovery.m`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 14.1 | Hardware Specification Probe | `HardwareInfo` (model, CPU brand, core/thread count, RAM) | 💚 | Sysctl-based query on macOS; verified passing in `system_test`. |
| 14.2 | Battery & Power Status | `HardwareInfo_hasBattery`, level percentage, charging status | 💚 | IOKit power source introspection. |
| 14.3 | Graphics API & VRAM Probe | `GraphicsInfo` reporting Metal/Vulkan API and VRAM budget | 💚 | Probes unified memory architecture and allocation limits. |
| 14.4 | Display Enumeration & Refresh Rate | `DisplayMonitor` enumerating connected screens and Hz | 💚 | CoreGraphics active display list scan. |
| 14.5 | Retina Scale & Density Inspection | Logical points, physical pixels, native hardware panel grid | 💚 | Accurately calculates scale factor and hardware panel scale. |
| 14.6 | `AppDetect` Local Tool Registry | Hand-curated catalog of developer tools (`apps.inc`) | 💚 | Slots for `opencode`, `codex`, `claude`, `cursor`, etc. |
| 14.7 | Zero-Subprocess PATH Resolution | `AppDetect_which` via `getenv("PATH")` and `access(X_OK)` | 💚 | Resolves binaries without spawning shell or child processes. |
| 14.8 | macOS Bundle Check | `AppDetect_isAppBundle` scanning `/Applications` | 💚 | Case-insensitive bundle existence verification. |
| 14.9 | Live Process Liveness Probe | `ProcessProbe_isRunning` using darwin `libproc` | 💚 | Non-intrusive PID enumeration and basename matching. |
| 14.10 | Audio HAL Driver Scan | `ProcessProbe_isDriverLoaded` scanning `/Library/Audio/Plug-Ins/HAL` | 💚 | Detects virtual audio drivers (BlackHole, Soundflower). |
| 14.11 | `CaptureTool` Screen Capture Detector | Registry of capture tools (`capture_tools.inc`) | 💚 | Tracks OBS, QuickTime, Screen Studio, etc. |
| 14.12 | Capture Liveness Classification | Counts active screen recorders, streamers, and audio capturers | 💚 | Honest proxy for system-wide capture activity. |
| 14.13 | Native macOS Image Decoder | `image_mac.m` NSImage to raw bitmap raster bridge | 🟩 | Off-heap raster conversion for UI textures. |
| 14.14 | Biometric TouchID Authentication | `touchid_cocoa.m` via Apple `LAContext` | 🟩 | Generates single-use cryptographic tokens; verified in `touchid_demo`. |

---

## Subsystem 15: Audio Seams & Playback (`audio/*`, `objc/audio_cocoa.m`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 15.1 | macOS AVFoundation Audio Engine | `AVAudioEngine` + `AVAudioPlayerNode` backend | 🟩 | Fully implemented in `src/objc/audio_cocoa.m`. |
| 15.2 | PCM Audio File Loading | `AudioClip_load` reading disk files via `AVAudioFile` | 🟩 | Decodes audio file into `AVAudioPCMBuffer`. |
| 15.3 | Sine Wave Tone Synthesis | `AudioClip_tone(freq, seconds)` | 🟩 | Synthesizes pure sine buffers for chiptunes and audio tests. |
| 15.4 | Multi-Voice Playback Nodes | `AudioVoice` handle with volume, pitch rate, looping controls | 🟩 | Dynamic scheduling and playback via player nodes. |
| 15.5 | Cross-Platform Audio Stub | `src/audio/audio_stub.c` | 🟧 | Silent stub on non-Apple platforms without native audio backend. |
| 15.6 | Full Realtime Audio Engine Seam | CoreAudio HAL low-latency bridge with ring buffer feeding | ⬜ | Seam connecting directly to `samplerate` DAW backend. |

---

## Subsystem 16: Primitive Types & Scalar Boxing (`primitive/*`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 16.1 | Integer Primitives | `Int`, `Long`, `Short`, `Byte` | 💚 | Value storage, BitPool slot allocation, CAS operations. |
| 16.2 | Floating-Point Primitives | `Float`, `Double`, `LongFloat`, `LongDouble` | 💚 | IEEE 754 float/double wrappers. |
| 16.3 | Fixed-Point Arithmetic | `Fixed32` (16.16), `Fixed64` (32.32) | 💚 | Deterministic fixed-point math for physics engines. |
| 16.4 | Mixed Fixed/Float Types | `IntFloat`, `IntDouble` | 💚 | Combined precision value containers. |
| 16.5 | Boolean Primitive | `Bool` | 💚 | Single-byte boolean type with bitwise logic operations. |
| 16.6 | Owned String Primitive | `String` off-heap string buffer | 💚 | Length-prefixed string blocks in memory arena. |
| 16.7 | Bit-Packing Utility | `Pack_packByte`, `Pack_packShort`, `Pack_packInt` | 💚 | Bit-shifting helpers packing scalars into wider words. |
| 16.8 | Brain `bfloat16` Primitive | `Brain` bf16 converter (`Brain_floatToBFloat16`) | 💚 | Uses `Bit16` pool; neural net and ML weight representation. |

---

## Subsystem 17: Relational Object Models (`objects/*`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 17.1 | `Choice` Dynamic Enum Object | Variant choice wrapper | 🟩 | Tagged enum value container. |
| 17.2 | `Future` Deferred Promise Object | Asynchronous completion holder | 🟩 | Stores resolved value pointer and ready state flag. |
| 17.3 | `Global` / `Local` Scoped References | memory reference wrappers | 🟩 | Encodes scope lifetime in type header modifier nibble. |
| 17.4 | `Passive` / `Reactive` Observer State | State observation objects | 🟩 | Proactive/reactive event notification wrappers. |
| 17.5 | `Probable` / `ProbableObjects` | Probabilistic choice tables | 🟩 | Weighted selection and probabilistic object dispatch. |

---

## Subsystem 18: CLI Command Engine & Annotations (`cli/*`, `annotation/*`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 18.1 | Parsed `Command` Block | Flat `[namePtr][argumentCount][padding][arguments...]` | 💚 | Single memory block owning all parsed arguments. |
| 18.2 | Command Line Scanner & Parser | `Scanner`, `CommandParser` | 💚 | Tokenizes whitespace-delimited shell command strings. |
| 18.3 | Command Dispatch Registry | `CommandRegistry` | 💚 | Registers handler callbacks mapped to command names. |
| 18.4 | Interactive Console Wrapper | `Console` reading stdin and routing to registry | 🟩 | Headless debugging console. |
| 18.5 | Built-in CLI Diagnostics | `LogCommands` | 🟩 | Debug commands dumping memory, threads, and system info. |
| 18.6 | Architectural Annotations | `;;OVERVIEW`, `;;DRAFT`, `;;INCOMPLETE`, `;;INTENTION` | 💚 | Compile-time and static-analysis doc macros. |
| 18.7 | Platform Guard Macros | `;;PLATFORM_EXCLUSIVE("Mac")` | 💚 | Explicit platform documentation annotations. |
| 18.8 | Native Hardware Events | `piano_key.c, turntable.c, gesture.c, gamepad.c, hardware_event.c` | 💚 | Piano keys, DJ turntable scratch/crossfader, gestures, gamepad deadzones. |
| 18.9 | System Clipboard Bridge | `clipboard.h, clipboard_mac.m, clipboard_stub.c` | 💚 | Native NSPasteboard text and bitmap clipboard bridge. |

---

## Subsystem 19: Three-Tier Math Architecture (`math/*`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 19.1 | Strict IEEE 754 Math | `strict_math.c, strict_math.h` with float & double precision | 💚 | Complete IEEE compliance for physics simulations (`StrictMath_sin`, `StrictMath_sqrt`, `StrictMath_atan2`). |
| 19.2 | Relaxed Fast Approximations | `fast_math.c, fast_math.h` deliberately relaxing IEEE 754 | 💚 | Bhaskara rational trig, Quake bit-hack `invSqrt`, Newton-Raphson fast reciprocal. |
| 19.3 | Unified Math Facade | `math.c, math.h` strict by default, `fast_` prefixed approximations | 💚 | `Math_sin` delegates strictly; `Math_fast_sin` invokes approximation. |
| 19.4 | Angle & Interpolation Helpers | `Math_radToDeg, Math_degToRad, Math_clamp, Math_lerp` | 💚 | Standard geometric utilities across float and double. |

---

## Subsystem 20: Search, String Math & Spotlight Engine (`search/*`, `algo/*`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 20.1 | String Math Expression Evaluator | `search/calc.c, calc.h` recursive descent / Pratt parser | 💚 | Evaluates complex nested expressions like `"sin(rad(90)) * atan(34) * pi"`. |
| 20.2 | IDE Find Flags & SQL LIKE | `search/find.c, find.h` with case-sensitive, exact-word, wildcard | 💚 | Full support for SQL-style `%` and `_` wildcards with word boundary detection. |
| 20.3 | Ranked Spotlight Search | `search/spotlight.c, spotlight.h` ranked relevance scoring | 💚 | Exact ($1000$) > Prefix ($500$) > Boundary ($250$) > Substring ($100$) > Acronym. |
| 20.4 | Calculation Query Integration | Automatic routing of `=...` and math expressions in Spotlight | 💚 | Spotlight seamlessly evaluates calculator expressions. |
| 20.5 | Algorithmic Scaffolding | `algo/draft_sort.c, draft_sort.h` marked with `;;INTENTION` and `@Draft` | 🟩 | Quickselect partition, in-place 64-bit quicksort, and 3D Morton spatial code. |
| 20.6 | Byte Regex Engine | `regex/*` — one class per file: `regex.c` (public `Regex`), `regex/parser.c` (pattern → AST), `regex/nodelist.c` (flat AST), `regex/program.c` (Thompson-NFA emitter), `regex/vm.c` (linear Pike-VM), `regex/charclass.c` (256-bit bitmap), `regex/span.c`; mirrored owners in `../../../tests/vexspoke/regex` | 🟩 | Literals/anchors/alternation/greedy quantifiers/`{m,n}`/groups/classes/backslash-d-w-s/escapes; `REGEX_CASE_INSENSITIVE`/`DOTALL`/`MULTILINE`; capture offsets via `RegexSpan` (`RegexSpan_none` for an unmatched group); dest-last truncated projections; loud compile rejection with one reason per refusal. Greedy-only: no lazy/lookaround/backreferences/word-boundaries/Unicode; documented node/program/class/nesting/repeat ceilings; every scratch block allocated once in `RegexVm_init` and freed on every path (cold path). |

---

## Subsystem 21: Security & Cryptography Engine (`security/*`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 21.1 | NIST FIPS 180-4 SHA-256 Digest | `security/crypto.c, crypto.h` streaming and one-shot SHA-256 | 💚 | Passes standard NIST vectors; zero heap allocation. |
| 21.2 | Constant-Time memory Equality | `Crypto_constantTimeEquals` side-channel-safe check | 💚 | Accumulates XOR differences; immune to timing leakage attacks. |
| 21.3 | Fast Relational Hash Mixers | `Crypto_hash64` and `Crypto_hash32` | 💚 | High-avalanche 64-bit and 32-bit hash mixer for symbol keys. |
| 21.4 | XorShift128+ PRNG Engine | `Crypto_prngU64, Crypto_prngBytes` | 💚 | Deterministic (SplitMix64-seeded) pseudo-random generator. **Never for credentials** — secrets come from `SecureRandom_bytes` (OS CSPRNG); the renamed API makes the determinism hard to miss. |
| 21.5 | SHA-1 (FIPS 180-4) | `sha1_test` | 🟩 | Streaming digest kept for HMAC-SHA1/TOTP interop; collision weakness does not apply to HMAC. |
| 21.6 | Base32 (RFC 4648) | `base32_test` | 🟩 | Pure byte-to-byte encoding: the TOTP setup secret's transport form; tolerates case/grouping, rejects a bad alphabet. |
| 21.7 | HMAC (RFC 2104) | `hmac_test` | 🟩 | Over SHA-1 and SHA-256, streamed (no concatenation buffer), key material scrubbed. |
| 21.8 | TOTP (RFC 6238) | `totp_test` | 🟩 | Code + verify with a clock window and **replay refusal**; the second factor every authenticator app reads. |
| 21.9 | PBKDF2 password hash | `password_test` | 🟩 | RFC 6070 vectors; slow by design, cold path only. Salt policy bound lives in the generator, not the derivation. |
| 21.10 | otpauth:// setup URI | `otpauth_test` | 🟩 | The whole authenticator integration: percent-encoded label + base32 secret; query built with a checked, never-truncated format. |
| 21.11 | OS keychain seam | `keychain_test` | 🟧 | Apple backend; Windows/secret-service are a stated gap and report UNSUPPORTED (never a plaintext fallback). Safe paths pass; the write round trip is opt-in and currently unproven. |
| 21.5 | Hex Serialization Helpers | `Crypto_toHex` and `Crypto_fromHex` | 💚 | Zero-allocation hexadecimal encoder and decoder. |
| 21.6 | Biometric TouchID Token Protocol | `security/touchid.c, touchid.h` single-use token challenge-response | 💚 | Validates and burns tokens; verified in `crypto_security_test`. |

---

## Subsystem 22: Algorithmic Suite (`algo/*`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 22.1 | LSD Radix Sort | `radix_sort.c, radix_sort.h` | 💚 | Linear O(N) 256-bucket integer and pair sorting for u32 and u64. |
| 22.2 | Dijkstra Shortest Path | `dijkstra.c, dijkstra.h` | 💚 | Single-source shortest path solver on weighted graphs via priority queue. |
| 22.3 | 3D Spatial KD-Tree | `kd_tree.c, kd_tree.h` | 💚 | 3D cycling plane KD-Tree for nearest neighbor and radius queries. |
| 22.4 | Bounding Volume Hierarchy | `bvh.c, bvh.h` | 💚 | AABB bounding box hierarchy with fast stack-based ray intersection. |
| 22.5 | Relational Tree-Sitter AST | `tree_sit.c, tree_sit.h` | 💚 | AST hierarchy walker with pre/post-order visitor and byte span queries. |

---

## Subsystem 23: On-Disk Cache & Download Manager (`io/cache.*`, `net/download.*`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 23.1 | Cryptographic Persistent Cache | `io/cache.c, cache.h` | 💚 | SHA-256 keyed cache with TTL expiry, atomic writes, and zero redownloads. |
| 23.2 | Package & File Downloader | `net/download.c, download.h` | 💚 | Safe curl downloader with integrated cache lookup (`Download_fetch_cached`). |

---

## Subsystem 24: CoreAudio HAL Real-Time Engine (`audio/audio_hal.*`, `objc/audio_hal_mac.m`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 24.1 | Native CoreAudio HAL Output | `objc/audio_hal_mac.m, audio/audio_hal.h` | 💚 | Real-time pull AudioUnit stream feeding low-latency DSP to hardware. |
| 24.2 | Audio HAL Fallback Stub | `audio/audio_hal_stub.c` | 💚 | Graceful fallback on non-Apple operating systems. |

---

## Subsystem 25: Input Binding Registry (`input/key_map`, `input/key`, `input/mouse`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 25.1 | Composable int64 Combo Encoding | KMODE gesture (4b) + KMOD_* modifier nibbles (5×4b) + key/button code (32b) in one `int64_t` | 💚 | `KMODE_TAP/DOUBLE_TAP/TRIPLE_TAP/LONG_PRESS/DRAG/SCROLL/ZOOM`; exact modifier space via `KMOD_ALL_MASK`. |
| 25.2 | KeyMap Registry (bind/unbind/replace) | `KeyMap_create(arena)`, `KeyMap_bind/unbind`, in-place replace, doubling growth | 💚 | Arena-owned, zero steady-state alloc; per-map `multiTapEnabled` + `longPressNanos` recognition config; `tests/key_map_test`. |
| 25.3 | Combo Builders from Live State | `KeyMap_buildCombo*` for key / mouse / hold | 💚 | Multi-tap aware — TAP auto-upgrades to DOUBLE/TRIPLE for the current code. |
| 25.4 | Per-Frame Gesture Resolution | `KeyMap_resolve` exact-match, specificity (KMODE wins, ties bind-order), tap consumed before callback | 💚 | Windowed settlement: taps are OFFERED while the per-key window (250ms) is open, settle into SINGLE/DOUBLE/TRIPLE at close; TAP requires release; LONG_PRESS fires once per press (one-shot latch); rhythm mode (`setMultiTapEnabled(false)`) resolves every press as an instant single; stale settled taps declined on modifiers expire; verified in `key_map_test` + darling `frame_test`. |
| 25.5 | Mouse Button Symmetry | `Mouse_resetTaps`/`Mouse_tapPhase`/latch (mirrors `Key_*`), tap counters for buttons 0..7 | 💚 | Cross-restart tap session semantics; modifier change between presses breaks the click sequence. |
| 25.6 | Resolve-Deferred Gestures | DRAG/SCROLL/ZOOM bindable but not resolvable under per-frame polling | 🟨 | `;;DRAFT` — event-stream resolver ships later. |

---

## Subsystem 26: Reactive Generics (`reactive/*`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 26.1 | One reactive engine | `Reactive` — one atomic word + shadow + dirty + four channel lists | 💚 | `set` never fires; the owner `drain` coalesces the batch; atomic from any thread. `tests/vexspoke/reactive_test`. |
| 26.2 | Generic spelling `Reactive(T)` | `Reactive(int)` / `Reactive(Vec4)` / `Reactive(Buffer)` | 🟩 | Lowercase C spellings bridge to the camelCase class. |
| 26.3 | Four typed channels | `onSet`, `onChanged`, `onGet` (one-fire read), `onNullptr` | 🟩 | Callback `fn(T value)`; `removeOn` matches the function-pointer address; `onRemove` retired (freeing is just freeing). |
| 26.4 | Object one-liner | `TYPEDEF_REACTIVE(NAME)` / `IMPLEMENT_REACTIVE(NAME)` | 🟩 | Stamps any object type in two lines; then `Reactive(NAME)`. |
| 26.5 | Scalar family | `reactive_primitive.{h,c}` (Bool Byte Short Char Int Long Float Double String IntFloat) | 🟩 | One file pair (`;;INTENTION` waiver); integer cast / bit-cast / pointer packings. |
| 26.6 | Object family | `reactive_object.{h,c}` (Vec2/3/4, Rectangle, IntDouble, LongFloat, LongDouble) | 🟩 | One file pair; value = a pointer (rebind = change). |
| 26.7 | Merged probable | `ReactiveProbable(T)` — `{ value, chance }`, `get()` rolls | 🟩 | `reactive_probable.{h,c}`; no nesting by intent. Verified 0.5 -> ~half. |
| 26.8 | Generic function surface | `Reactive_set`/`Reactive_get`/`Reactive_addOnChanged`/… via `_Generic` | 🟩 | One name for any type; a bare `Reactive*`/`nullptr` routes to the raw engine channel. |

---

## Defect Log & Seam Status

- **Regex correctness slice:** full-match VM admission keeps competing branches
  alive past premature MATCH; unsupported alphabetic escapes/backreferences and
  repeated/lazy/possessive quantifiers reject explicitly. Seven mirrored owners
  pass through `python3 tests/vexspoke/regex/run.py` in strict optimized C23 and
  ASan/UBSan builds. Workspace execution was blocked by missing Graphvex
  `quad.vert`, not a regex test failure. Allocation failure, execution budgets,
  iterative emission, comprehensive differential/concurrency pressure and other
  platforms remain unproved; older full-suite counts below are historical.

- **Network.framework TLS Wired**: `src/objc/tls_apple.m` now wires native macOS `nw_connection_t` TLS connections.
- **Dynamic Destructor Dispatch**: `c23_free` now supports registered custom destructors via `Destructor_register` and `Destructor_lookup`.
- **All Core, Spatial, Algorithm & Hardware Test Suites Passing**:
  - `math_coord_test`: 39/39 assertions PASS (12-frame math, directional inverses, multi-precision vectors).
  - `search_calc_test`: 29/29 assertions PASS (string math expressions, IDE find flags, SQL LIKE, spotlight).
  - `regex` subsystem: seven mirrored owners all PASS — `regex_test` (literals/search offsets, quantifiers, captures, classes, escapes, anchors, flags, projections, loud compile rejection with the `[vex]` diagnostic, hostile backtracking shape, safety ceilings), plus `parser_test`, `program_test`, `vm_test`, `nodelist_test`, `charclass_test`, `span_test` for each unit's own seam. Full `./tools/b test` 285 passed / 0 failed / 3 skipped under strict C23 with the coverage ratchet green; ASan/UBSan clean and 0 leaks per owner.
  - `spatial_struct_test`: 38/38 assertions PASS (`CircleArray`, `SphereArray`, `Octree`).
  - `crypto_security_test`: 16/16 assertions PASS (NIST SHA-256 vectors, constant-time compare, PRNG, TouchID tokens).
  - `hardware_input_test`: All assertions PASS (piano keys, turntable scratch/crossfade, gestures, gamepad deadzones).
  - `algo_suite_test`: All assertions PASS (radix sort, dijkstra, kd-tree, bvh, tree-sit).
  - `clipboard_test`: All assertions PASS (clipboard set/get/clear, persistent cache, destructor dispatch).
  - `reactive_test` & `reactive_typed_test`: PASS (fan-out, atomic set/drain, mid-fire remove, cross-thread; the typed family round-trips; the generic `_Generic` surface + `ReactiveProbable` verified).
  - `spoke_test` & `manifest_hot_test`: All assertions PASS with zero regressions.

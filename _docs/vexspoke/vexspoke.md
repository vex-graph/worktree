# Vexspoke — Living Docs

> The 2am README for R2 Behavior. See also
> [`_docs/how-it-works/how vexspoke works.md`](../how-it-works/how%20vexspoke%20works.md)
> for the architecture walkthrough, and
> `../../projects/vexspoke/preferences.md` for the constitutional law.

---

## 1. Position

Pure relational leaf. Includes NOTHING from graphvex, hotcwap,
darling, api-haven, or engines (Rule 17). Every higher layer includes
vexspoke shapes.

```text
MemoryArena ── stamps typeId ──▶ every block
BitPool     ── lockless slots ─▶ primitive types
Variable    ── name => (classId, ptr)
Type        ── 64-bit ID scheme (project/form/modifier/wrapper/class)
Class/Fields── runtime struct schemas (dual-stream partitioning)
Struct      ── allocate typed blocks via Memory + Class
Collections ── List/Array/Map/Set/Stack/Deque/Queue/MinHeap (Collection base)
String      ── arena blocks, length in header
Json        ── zero-alloc parse/write
SpinLock    ── owner-embedded CAS
RingBuffer  ── pow2 MPMC FIFO
WsClient    ── bounded frame slot (100ms max poll)
ProcessSpawn── bounded child-job table (posix_spawnp)
VexHome     ── per-user fs layout
```

## 2. Subsystem Directory Map

| Subsystem | Classes | Level |
|---|---|---|
| `atomic/` | SpinLock, RingBuffer, Atomic*, ThreadRegistry | L4 |
| `bit/` | BitPool | L4 |
| `c23/` | CONSTRUCTOR_DISPATCH, zero(), fnbind | L1 |
| `io/` | File, Log, VexHome, WsClient, ProcessSpawn | L2/L4 |
| `lang/` | Vec2, Vec3, Vec4, Mat4, FastMath | L2 |
| `net/` | Json, HTTP, URL, TLS | L2 |
| `nio/` | MemoryArena (master arena + slabs) | L4 |
| `oop/` | Type register, Class/Fields, Struct, Stride | L1/L2 |
| `primitive/` | Bool, Int, Long, Float, Double, String, Fixed*, Pack, Brain | L2 |
| `relational/` | Variable, Relational search facade | L2 |
| `struct/` | List, Array, Map, Set, Stack, Deque, Queue, MinHeap, SparseSet | L2 |
| `system/` | AppDetect, ProcessProbe, CaptureTool, DisplayMonitor | L2 |
| `thread/` | Thread (role-indexed), Draw, Network, Scripting, Event, UI | L4 |
| `time/` | Clock, Nanotime, Calendar, DateTime | L2 |
| `util/` | Hash (FNV1a, murmur3), Random | L2 |

## 3. Key Contracts (memorize these)

- **`Memory_alloc(typeId, bytes)`** — slab pop (64B-4KB) or bump.
  Negative pointer math recovers type/length. MAGIC `0x56455821`.
- **`Memory_freeAll()`** — O(1) reset. ALWAYS the final teardown step.
- **Type ID bits**: `0x F PRPR M W1 W2 PDPD CCCCCCCC`. Projects:
  vexspoke=0x01, graphvex=0x02, hotcwap=0x03, darling=0x04,
  api-haven=0x05. Custom structs start at class 0x4000.
- **Variable slots**: 48 bytes = 32 name + 4 classId + 4 pad + 8 ptr.
  Names lowercase, 32 chars max, open-addressed.
- **Bounded waits**: WsClient/ProcessSpawn/SpinLock timeouts ≤100ms.
- **Dest-last**: `String_appendInto(a, b, dest)`, `Json_getString(doc,
  ref, dest, cap)`, `Vec4_add(a, b, dest)`.

## 4. Checklist Status

See `../../_checklist/` for per-class build status (untracked,
local-only).

## 5. Tests

`projects/vexspoke/tests/` — headless harnesses. Run with
`ctest` from the build dir. Cold-seam test matrix per Rule 35.
# How vexspoke Works: The Relational Memory Substrate

> The 2am README for R2 Behavior. If you forgot everything, read
> sections 1-3 and go back to sleep. If it's 2pm and you're adding a
> feature, read the API surface at the bottom.
> Answers the fundamental question: **"Where does memory come from?"**
> Answer: **one 64MB arena, carved once.**

---

## 1. The Short Answer: Everything Is a Pointer With a Type ID

vexspoke is a pure behavioral leaf (R2). It includes NOTHING from
hotcwap, graphvex, darling, api-haven, or any engine. Every higher
layer includes vexspoke shapes.

The core idea: one 64MB arena (`MemoryArena`) is carved from the OS
at boot. All subsequent "allocations" are slab pops or bump pointers —
never `malloc`. Every allocated block carries a 32-byte header with a
64-bit type ID that encodes project, form, modifier, wrapper, and
class. Negative pointer math recovers metadata at zero cost.

| Piece | What it is | Role |
|---|---|---|
| `MemoryArena` | slab + bump allocator | 64MB master arena, 7 size classes (64B-4KB), bump for large |
| `BitPool` | lockless fixed-width pool | CAS-tagged freelist, one pool per element width |
| `Variable` | name => (classId, pointer) registry | relational symbol table, open-addressing hash map |
| `Type` | 64-bit type ID scheme | every block carries project + form + class |
| `Class/Fields` | runtime struct schema engine | field descriptors, dual-stream partitioning |
| `Json` | zero-allocation parser/writer | caller-owned node pool + scratch arena |
| `String` | arena-allocated byte blocks | length from header, not NUL scan |
| `SpinLock` | owner-embedded CAS lock | 0 = free, `(threadId << 1) | 1` = held |
| `RingBuffer` | fixed-capacity MPMC FIFO | power-of-two, SpinLock-serialized copy |

---

## 2. Where It Sits (Read This Once)

Per `../../preferences.md` Rule 17 the stack has ONE order:

```text
R1 hotcwap   — boots first, owns Kernel/Window, tears down last
R2 vexspoke  — arenas, net/http, threads, system probes. WE ARE HERE.
R3 graphvex  — GPU only (includes vexspoke only)
R4 darling   — UI toolkit (includes vexspoke + graphvex + hotcwap)
R5 apps      — your IDE, your game, other CLIs
```

vexspoke is the **pure behavioral leaf**. It includes zero headers
from any other repo. If a new file wants any other `#include`, the
design is wrong, not the rule.

---

## 3. The Memory Model (the most important section)

### 3a. The Arena

```text
Memory_init(64MB)  →  one calloc(64MB) call
Memory_alloc(typeId, numBytes)  →  slab pop (O(1), 7 size classes)
Memory_free(ptr)   →  slab push back to free list
Memory_freeAll()   →  O(1) reset, ALWAYS the final teardown step
```

**Size classes**: 64, 128, 256, 512, 1024, 2048, 4096 bytes.
Allocations larger than 4KB go to a bump allocator (monotonic, reset
with `Memory_freeAll`). The magic cookie `0x56455821` ("VEX!") in
every header detects corruption.

**Negative pointer math**: every payload pointer is preceded by a
32-byte `MemoryHeader`. To get the type or length:

```c
Memory_type(ptr)   →  *((MemoryHeader*)ptr - 1).typeId   // O(1)
Memory_length(ptr) →  *((MemoryHeader*)ptr - 1).length   // O(1)
```

No lock, no lookup, no hash — just pointer subtraction.

### 3b. The Type ID (64 bits)

```text
0x F PRPR M W1 W2 PDPD CCCCCCCC
  | |    | |  |  |    `-- class        (32 bits: 0x4000+ = custom struct)
  | |    | |  |  `------- padding      (8 bits)
  | |    | |  `---------- wrapper 2    (probable/future/choice)
  | |    | `------------- wrapper 1    (proactive/reactive)
  | |    `---------------- modifier    (global/locale/transient)
  | `--------------------- project     (8 bits: vexspoke=0x01, graphvex=0x02, ...)
  `---------------------- form         (singleton/array/pointer/struct variants)
```

Every allocated block is stamped with this ID at `Memory_alloc` time.
The ID is composed by `Type_make(proj, form, classId)` and decomposed
by `Type_class(typeId)`, `Type_form(typeId)`, etc.

### 3c. The Transient Arena

A separate bump-only arena (64MB default) for frame/scratchpad data.
`Transient_alloc` pushes the bump cursor; `Transient_reset` snaps it
back to zero in O(1). Every frame, the Kernel calls
`MemoryArena_freeAll(transientArena)` first — before any event
polling, before any tick, before any presentation.

---

## 4. The Relational Symbol Table

`Variable` maps a lowercase 32-char name to a `(classId, pointer)`
payload. Two Variable tables serve as scopes (global + local).

```c
Variable_instant(scope, "camera_matrix", TYPE_MAT4, &camera);
void *ptr = Variable_getPointer(scope, Variable_getId(scope, "camera_matrix"));
```

The `Relational` facade adds spotlight search: type a query, get
ranked results (exact > prefix > substring). Case-insensitive.

---

## 5. The Struct Schema Engine

`Class/Fields` defines runtime struct layouts. Each field has a name,
size, offset, and isPartition flag. Dual-stream partitioning separates
hot flat primitives (Stream 1) from nested struct sub-objects
(Stream 2), enabling GPU-friendly SoA layouts.

```c
uint32_t types[] = { ID_FLOAT, ID_FLOAT, ID_VEC3 };
Fields *f = Fields(types, 3);   // anonymous fields
// or named:
Class *c = Class(ID_FLOAT, 4.0f, "x", ID_FLOAT, 4.0f, "y", ID_VEC3, 12.0f, "pos");
```

---

## 6. Zero-Alloc JSON

Json is a single-pass recursive-descent parser. Caller provides a
fixed node pool + scratch arena. Documents that don't fit report
failure — never allocate, never fail silently.

```c
JsonNode nodes[256];
char scratch[4096];
JsonDoc doc;
Json_parse(&doc, nodes, 256, scratch, 4096, "{\"key\": \"value\"}");
// Navigate:
JsonRef val = Json_member(&doc, Json_root(&doc), "key");
const char *str = Json_string(&doc, val, NULL);
```

The writer builds into a caller byte buffer; overflow flips `ok` once
and later calls no-op. Max parse depth: 24.

---

## 7. Strings

Strings are Memory-allocated blocks. Length is stored in the
MemoryHeader, not computed from NUL. `string_length(ptr)` reads
`Memory_length(ptr)` and subtracts 1 (the NUL terminator).

All string operations allocate through the arena. `String_append`
creates a new block; the caller owns the result.

---

## 8. Synchronization

**SpinLock**: owner-embedded in the lock word. `SpinLock_unlock`
refuses to release if the calling thread is not the owner
(fail-closed). ARM64: `yield`; x86: `pause`. 16 iterations of pause
between CAS attempts.

**RingBuffer**: fixed-capacity MPMC FIFO. Power-of-two capacity for
bitmask indexing. One SpinLock serializes push/pop (prevents torn
reads). Monotonic head/tail counters never wrap.

**ThreadRegistry**: lock-free probe-and-CAS over 256 slots. Each
thread gets a dense index. Roles: MAIN(1), ENGINE(2), DRAW(3),
PRESENT(4), NETWORKING(5), SCRIPTING(6), CONSOLE(7), UI(8).

---

## 9. I/O Layer

| Class | What it is | Key contract |
|---|---|---|
| `File` | stdio wrapper, arena block | Creates parent dirs on CREATE |
| `Log` | CAS ring logger | 16K slots, 64B each, writer drains to file |
| `WsClient` | bounded WebSocket frame slot | 4096B rx buf, 100ms max poll (Rule 27) |
| `ProcessSpawn` | child-process job table | 8 slots, `posix_spawnp`, non-blocking reap |
| `VexHome` | per-user fs layout | `~/Library/Application Support/vexgraph` on macOS |

---

## 10. Key Architectural Principles

1. **Zero steady-state allocation**: `Memory_init` allocates once.
   `Memory_freeAll` is always last. Never `malloc` on the hot path.
2. **Everything is a pointer with a type ID**: single allocator serves
   every type across the entire stack.
3. **Negative pointer math**: `Memory_type(ptr)` and
   `Memory_length(ptr)` are single pointer-subtractions.
4. **Lock-free where possible**: BitPool uses CAS-tagged freelist;
   SpinLock uses CAS with owner-embedding.
5. **Dest-last parameters**: all output parameters come last.
6. **Bounded waits everywhere**: WsClient, ProcessSpawn, SpinLock
   tryLockTimeout all capped at 100ms (Rule 27).
7. **Leaf architecture**: vexspoke includes NOTHING from any other repo.

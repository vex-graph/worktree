# The Reflection Engine — Implementation Plan

> Status: DRAFT (`;;DRAFT`). R2 `vexspoke` only. This is the plan; no code yet.
> Binds: the Self-Describing Memory Block Law, the 24-Byte Variable Slot Law
> (The 23+1 Rule), the BitPool Slot Segregation Law, the Data-Oriented Storage
> Law & Object-Oriented Ergonomics, the Dynamic Scalability & Anti-Hardcoding
> Law, the No Hardcoding Law, the Arity and Constructive Convenience Law, the
> Single Class Per File Law, the Two-Semicolon Annotation Style Law, the
> Vertical Integration Law (R2 stays a pure leaf), the Test Segregation Law,
> the Living Preferences Law, the Conflict Triage Law.

---

## 0. Decisions (resolved in review)

| Question | Decision |
| :-- | :-- |
| Phase order | Approved; Phase 0 landing first, review between phases. |
| Hash A | **Identity** hash of the pointer (`Hash_murmur3Mix64((uint64_t) p)`). Variable *objects* use the avalanched System B instead — two systems, as designed. |
| Alphabet | Canonical 39 = `a-z`, `0-9`, `_`, `$`, `-`. `.` is **not** a bucket character: it is the **path splitter** for dereference (`a.field`), never a bucket of its own. |
| Dashcode | `Hash_murmur3Mix64(tailBytes) & 1023` — same 1024 surface, real avalanche. |
| Reactive | Extend `objects/reactive.c` **and** relocate into `src/reactive/`, overhauled so the value is a referenced `void*`; `Reactive_getValue(reactive)` is O(1). |
| Atom | **Box + cell.** Name box = `[name 24B][ptr 8B]` (the variable slot). Value lives in an identity cell = `[MemoryHeader 16B][value-or-ptr 8B][pad 8B]` = 32 B, typed by `type.c`. No new header (the existing `MemoryHeader` is the identity). Retires `StringSlot`'s `[self]` link (amends the 24-Byte Variable Slot Law). See section 3.7. |
| The shelf | **One global shelf**, nodes linked to one another — a graph (cyclic allowed) stored as a linked list inside an array list: cells in a `ChunkedList`. See section 3.7. |
| Deep-layer paths | **Node-based walk**, `class name + variables`, pointer-chasing by design, marked `;;INTENTION` (section 3.8). Guardrail: the chase stays cold; hot iteration stays DOD. |
| `;;INHERITS` | A **note only** naming the identity-defining classes/interfaces that make the class exist, comma-separated (`;;INHERITS("GraphicsPanel, Reactive")`). Not primitives (`uint64_t`), not collections (`List`). No build-time enforcement. |
| WHAT rollout | Retrofit as noticed — annotate each `void*` as its file is touched. |
| ChunkedList API | Variadic macro: `ChunkedList(elementClass, stride, r0…leaf)`; the byte-budget form stays `ChunkedList_1/_2/_3` **unchanged** so `hotcwap` is never touched. |
| ChunkedList sentinels | `CHUNKED_LIST_TWO/THREE_LAYER_DEFAULT` (FourCC `ÔWO!`/`ÔHRE`, high bit set → negative) select the depth; explicit numbers override. Stamped `INTENTIONAL(vex)`. |
| ChunkedList storage | N-level radix page table, growable COW root, page-sized leaf, shift/mask hops — **landed** (commit `627bb5a`, section 3.4). |

**Phase 0 — done.** Landed `src/annotation/{what,inherits,reactive}.h` and the
WHAT Law in the canonical `preferences.md` (commits `7b5a3e0`, `3617967`,
inside `vexspoke`). No mirror sweep: per-repo `<repo>-preferences.md` files
carry *exclusive* laws only; universal laws live in the canonical, so the WHAT
Law binds everywhere with no per-repo edit.

**Phase 1 — started (the atom landed).**
- Codified the **Cold-Only Reflection Law** (the walk is a cold rendezvous,
  never a frame path) and named the R2 facility the **Relational Engine** —
  commit `3d0d49e`.
- `feat(hash): Hash_pointer` — the pointer-identity hash — commit `d156c52`.
- `feat(variable_slot): the 32-byte name box` — commit `160de41`; the atom is
  real, `ID_VARIABLE_SLOT = 0x008C`, wired into CMake, with a local headless
  suite (`tests/vexspoke/variable_slot_test.c`, 43/43). The workspace root is
  not a git repo, so umbrella `tests/` are local-only (like `main/`, `_docs/`).
- **Next in Phase 1:** the identity cell, the global shelf (a `ChunkedList`
  radix page table — now landed, section 3.4), and the `;;INTENTION`-marked
  node-walk resolver.

---

## 1. Purpose

The Relational Engine is only as strong as its reflection: the ability to ask a
live pointer "what are you, what do you carry, and who is watching you?" at
runtime. Today `vexspoke` has the *parts* of reflection scattered across four
subsystems — `oop/` (class/field/type schema), `relational/` (name ⇒ pointer
symbols), `objects/reactive.c` (one event emitter), and `nio/mem.c` (the
16-byte self-describing header) — but no single, uniform **reflection system**
that treats a class, a field, a variable, a method, and a generic as one kind
of thing.

This plan unifies them under one atom (**a Variable is a name and a pointer**),
gives names two deterministic **hash** systems, and grows a proper **reactive**
subsystem that shares *one* value pointer across many observers.

The thesis in one line: **everything is a pointer, so a name is a pointer with
a 24-byte label and an 8-byte destination.**

---

## 2. What exists today (inventory)

| Concern | File | Current shape |
| :-- | :-- | :-- |
| Symbol registry | `relational/variable.h` | `Variable` + `VariableRow { i32 slot; u32 classId; uptr pointer; }` (16 B row) |
| Name pool | `relational/variable_pool.h` | `StringSlot { u64 self; char name[24]; }` (32 B), interned once per process |
| Class schema | `oop/class.h` | `Class { genericId, stride, stream1/2Stride, count, Field *items }` |
| Field descriptor | `oop/field.h` | `Field { char name[32]; u32 size, offset, ...; bool isStruct; }` |
| Type identity | `oop/type.h` | 64-bit `0x F PRPR M W1 W2 PDPD CCCCCCCC` + `TypeHeader` (legacy shadow) |
| Memory header | `nio/mem.h` | `MemoryHeader { u64 typeId; u32 length; u32 sugar; }` (16 B, live) |
| Event emitter | `objects/reactive.h` | `Reactive`: atomic `uint64` payload + 3 observer lists, owner-affine drain |
| Chunked storage | `struct/chunked_list.h` | `ChunkedList_{1,2,3}`, **byte** budget (default 128), COW directory |
| Hash utility | `util/hash.h` | `Hash_fnv1a64`, `Hash_murmur3Mix64`, `Hash_murmur3Mix32` |
| Name policy | `relational/variable.c` | `clean_name`: `[A-Za-z0-9_.]`, folded lowercase, ≤ 23 |

The 16-byte "identity" the design asks for **already exists** — it is
`MemoryHeader`. Every `Memory_alloc` payload is prefixed by
`[typeId 8B][length 4B][sugar 4B]`. `Reactive_check(ptr, ID_X)` therefore does
not need a new header; it must read the header already there.

---

## 3. The proposed system

### 3.1 The reflection atom — `Variable` = `[name 24B][ptr 8B]`

One 32-byte record, cache-aligned like `StringSlot`, used for **all five kinds**:

```c
typedef struct Variable {
    char name[24];      // 23 ASCII + NUL, zero-padded (the 24-Byte Variable Slot Law)
    uintptr_t pointer;  // the destination: a value, a Field, a Class, a method, a generic
} Variable;             // 32 bytes
```

The *kind* is **not** a second tag field — it is the memory block's own
`typeId`. The pointer points at a self-describing block (or a code address whose
`typeId` lives in a registered method table), so `Memory_type((*v).pointer)`
answers "is this a class, a field, a method, a generic?" with zero extra bytes.
This keeps the atom at 32 bytes and reuses the Self-Describing Memory Block Law.

Reflection verbs (dest-last per the Dest-Last Law):

```c
Reflect_kind(ptr)                     -> uint64_t        // Memory_type of the target
Reflect_class(field, src, dest)       // synthesize a Class schema from fields
Reflect_fields(class, dest, cap, outTruncated)
Reflect_methods(class, dest, cap, outTruncated)
```

### 3.2 Two hashing systems

**System A — the whole-pointer hash.** One function, 8 input bytes:

```c
uint64_t Hash_pointer(const void *p);          // Hash_murmur3Mix64((uint64_t) p)
```

**System B — the relational variable hash.** Folds the name to lowercase,
buckets by first character, then a "dashcode" (a 23-character, 184-bit integer
reduced to an index) selects a slot.

### 3.3 `VariableHashMap` — 39 × 1024 lazy chunked slots

```
name ──fold──▶ [first char] ──▶ one of 39 buckets (a-z, 0-9, _, $, -)
                 tail (chars 1..22) ──dashcode──▶ index 0..1023
                    slot = ChunkedList(void*) created lazily on first insert
```

- The 39 first-char buckets give a cheap, human-legible top level.
- The 1024 slots under each bucket start empty; a `ChunkedList` is minted only
  when a slot is first hit (the Dynamic Scalability & Anti-Hardcoding Law — no
  baked ceiling, no eager 40k allocation).
- Collisions chain inside the slot's `ChunkedList`; the record stores the full
  24-byte name so a chain resolves by byte compare (24-byte scalar, the
  24-Byte Variable Slot Law's branchless compare).

**The per-scope mini map.** Field and method names are class-scoped, so they
get the same shape with a smaller fan-out: `void*[39]` first-char buckets, each
a `ChunkedList` with a **16-slot** chunk (16 × 8 B = 128 B = today's default
chunk budget). One mini map per `Class`.

### 3.4 `ChunkedList` — the radix page table (landed)

`ChunkedList` is no longer a 2-level convenience: it is an **N-level radix page
table** — a growable copy-on-write root, any number of fixed-radix internal
levels, and a page-sized leaf. Every hop is shift/mask; a leaf is a contiguous
run of rows. That keeps never-moved addresses *and* stays data-oriented (the
Data-Oriented Storage Law): a bounded page walk, not a linked list.

```c
// radix form — any depth, no ceiling (the root grows)
ChunkedList *l3 = ChunkedList(ID_VARIABLE_SLOT, 32u, 1024, 1024, 128);
// sentinels (FourCC, high bit set; stamped INTENTIONAL(vex))
ChunkedList *two   = ChunkedList(ID_VARIABLE_SLOT, 32u, CHUNKED_LIST_TWO_LAYER_DEFAULT);
ChunkedList *three = ChunkedList(ID_VARIABLE_SLOT, 32u, CHUNKED_LIST_THREE_LAYER_DEFAULT);
```

- **Leaf = one page of rows** (`pow2 <= 4096 / stride`; 128 rows for 32-byte
  cells) — one streaming unit, one translation entry.
- **The 2-level byte-budget form is unchanged** (`ChunkedList_1/_2/_3`) and now
  reduces exactly to the general path, so `hotcwap`/`graphvex` callers need
  **no migration** — the 303-check byte-budget suite is the proof.
- **Growable root** → no capacity ceiling (the Dynamic Scalability &
  Anti-Hardcoding Law); only the tiny root ever copies.
- **Leaf tail-link chain** — every leaf carries an 8-byte link to the next, so
  a sequential sweep follows the chain (`ChunkedList_nextChunk` /
  `ChunkedList_forEachChunk`) while `slot(i)`/`getChunk(i)` stay O(1). This is
  the "chunk → chunk" chase the design wanted, layered on the page table so it
  never costs the O(1) lookup. Commit `ae1ca73`.
- Landed commits `627bb5a` + `ae1ca73`; 39→50-check radix suite; both suites
  ASan+UBSan clean.

### 3.5 The `reactive/` subsystem

New directory `src/reactive/` (the Canonical Include Paths Law: consumers write
`#include "reactive/reactive.h"`). The reactive object is a self-describing
block:

```
[MemoryHeader 16B: typeId | length | sugar]
[void *valuePtr]     // points at the ONE live value (shared by N observers)
[void *valueShadow]  // the block's own address, for intrusive validity
[value bytes ...]    // optional inline copy for scalars
```

- One `valuePtr` shared across many labels ⇒ writing the value through
  `*valuePtr` updates every observer at once (no per-observer copy).
- `Reactive_check(const void *p, uint64_t typeId)` reads `Memory_type(p)` and
  compares — the 16-byte identity does the classification.
- Owner-affine notification is preserved from `objects/reactive.c`
  (`Reactive_set` never fires; the owner calls `Reactive_drain`) so the
  Bounded Wait Law holds (no lock, no unbounded wait).
- Likely classes: `reactive/reactive.{c,h}`, `reactive/reactive_binding.{c,h}`
  (the observer list), `reactive/reactive_check.{c,h}` (or a static in
  `reactive.c` if behaviorless) — one class per file.

### 3.6 Annotations and the WHAT Law

Three new headers in `src/annotation/`, same `_Static_assert` pattern as
`;;INTENTION` (the Two-Semicolon Annotation Style Law):

```c
;;INHERITS("Base")           // annotation/inherits.h  — the `extends` marker
;;REACTIVE("HealthReactive") // annotation/reactive.h  — which reactive type
;;WHAT("uint64_t")           // annotation/what.h      — the pointee type of a void*
```

**The WHAT Law** (new, Tier 2): every `void*` whose pointee type is not
self-evident from its name must carry a `;;WHAT("<type>")` on the line above
it, so neither the human author nor a language model has to guess. It is the
declaration-site twin of the `toString` Law's runtime struct dump.

Note: the inline form `void* WHAT("uint8_t") x;` is **not expressible** with a
`_Static_assert` marker (it is not a declarator). The line-above form is the
one that compiles.

### 3.7 The atom, settled — the name box and the global identity cell

> Confirmed in review: the `[name 24B][ptr 8B]` box is the **variable slot**,
> and the value does not live in it — it lives in a **global shelf** of identity
> cells that node to one another ("a linked list inside an array list", the
> nodes held in a `ChunkedList`). `type.c` (the One Type Registry Law) is the
> identity that makes the shelf work — "thats why we have type.c across all
> vexgraph."

Two structures, one chain:

```text
NAME BOX  (pool, 32 B) : [ name 24B ][ pointer 8B ]              -> the LABEL
IDENTITY CELL (shelf)  : [ type 8B ][ length 4B ][ sugar 4B ][ value/ptr 8B ][ pad 8B ]
                         └──────── MemoryHeader 16 B ────────┘ └──── 16 B (32 B cell) ────┘
```

- **The name box** is the interned variable slot: `[name 24B][pointer 8B]`. It
  carries no value, only the address of its cell. This retires the old
  `StringSlot`'s `[self 8B]` link (validity moves to the memory header, the
  Self-Describing Memory Block Law) — an amendment to the 24-Byte Variable Slot
  Law.
- **The identity cell** is `[MemoryHeader 16 B][value-or-ptr 8 B][pad 8 B]` =
  32 B. Its identity is the **existing** `MemoryHeader { typeId u64; length u32;
  sugar u32; }` — **no new header, no amendment** (the Self-Describing Memory
  Block Law holds as written). The third field is a thin pointer to the value,
  or the value inline for small kinds; the pad rounds the cell to 32 B.
- The same identity-cell shape already appears in the reactive layout, so it is
  the engine's **one identity-cell form**, not a one-off.
- **The shelf is a graph.** One global table whose nodes link to each other — a
  graph, cyclic is fine — stored as a linked list inside an array list: the
  cells live in a `ChunkedList` (never-moved rows, the Data-Oriented Storage
  Law) and each cell's pointer links to the next. Hot sweeps over the
  `ChunkedList` stay flat; the links serve the cold walk.

**Deep-layer paths — node-based, and deliberately so.** A dotted path `a.b.c.d`
splits on `.` (the splitter) and walks **node to node**: `a` resolves in the
global scope to a node, `b` resolves inside that node's scope, and so on down to
the last-layer field. The reviewer's call: *class name + variables, node-based,
pointer-chasing, marked `;;INTENTION`.* Agreed, with the reasoning written down
(section 3.8) and one guardrail: the chase stays **cold** (search, debugger,
scripts); hot per-frame iteration still runs flat (the Data-Oriented Storage
Law).

```c
;;INTENTION("cold path search is a node walk by design; hot iteration stays DOD")
;;WHAT("Variable")
void *root;
bool Reflect_resolve(void *root, const char *path, Variable *dest, bool *outTruncated);
```

### 3.8 Talking back on the node walk

The reviewer invited an argument, so here it is — and the honest answer is
*yes, and the law may not even apply* (the Conflict Triage Law, step 2:
**assess before blocking** — a misapplied law is not a violation):

- The **Two-Layer Access Cap Law** governs how a *member chain is written in
  source* (`(*p).a.b`), to keep dereference hops visible. It says nothing about a
  runtime function walking a graph it was handed. A node walk is one hop per
  call frame, each hop hoisted into a local — which is precisely what the cap
  asks for.
- The **Data-Oriented Storage Law** governs *hot, bulk iteration* (sweep
  10,000 rows without jumping). Cold single-path search is the opposite
  workload, and the relational header already claims it: *"hot iteration stays
  DOD; cold rendezvous comes here."* A pointer-chasing resolver is that cold
  rendezvous.
- So the node graph is not a violation we tolerate — it is the right tool. The
  `;;INTENTION(...)` earns its place as a **signpost** (a future reader sees a
  chase and asks "why?"; the marker answers), and the guardrail keeps the
  honesty: if this resolver ever gets called per frame, that is the defect, not
  the chase itself.

### 3.9 Parked thread — reactive switching and `revalidate`

Raised in review, deferred by the reviewer ("another turn of asking"), captured
here so it is not lost:

- `;;INHERITS` names the **identity-defining classes/interfaces** that make the
  class exist — comma-separated (`;;INHERITS("GraphicsPanel, Reactive")`). It is
  not a primitive type (`uint64_t`) and not a collection (`List`): a `List` does
  not mean you inherit `[]`. It is "without these, this thing would not be
  itself." It is a **note only** (no build-time enforcement), so a reader can see
  at a glance what the class is built out of.
- Those interfaces carry a contract: e.g. a darling element must expose
  `;;WHAT("float") void *x;` and an `ElementName_revalidate()`.
- On a **reactive switch**, the reactive calls `ElementName_revalidate()`, which
  is the **sole** updater — so a value change never has to deep-propagate
  through the graph.
- **The one holdout is strings**: a string field genuinely needs a deep change
  (the bytes move). Two candidate escapes: a **reactive string** (a string whose
  own cell mutates in place), or accepting a bounded deep change for text only.
  This needs its own discussion next turn.

---

## 4. Conflicts and triage (the Conflict Triage Law)

| # | Conflict | Tiers | Proposed managed exception |
| :-- | :-- | :-- | :-- |
| 1 | `Variable` as `[24B name][8B ptr]` vs today's 16-byte `VariableRow` (name lives in the shared pool, referenced by slot) | T2 (both) | New 32-byte record for reflection; keep `Variable` registry rows as the pool-indexed fast path. Names duplicated only where reflection demands it. **Open question 1.** |
| 2 | Hash alphabet `[a-z0-9_$-]` (39) vs `clean_name` charset `[A-Za-z0-9_.]` | T2 | Reconcile one charset for both (decide `.` vs `$`,`-`). **Open question 3.** |
| 3 | `ChunkedList_1` currently means `elementClass`; design wants `ChunkedList(chunkAmount)` | T3 | Keep arity 1; add an explicit rows constructor (section 3.4). |
| 4 | "128 blocks" (rows) vs 128-byte budget | T2 | Add `VEX_CHUNKED_ROWS_DEFAULT`; convert rows ⇒ bytes once at construction. |
| 5 | New `Reactive` (shared `valuePtr`, identity check) vs `objects/reactive.c` (atomic `uint64` + observers) | T2 | Move the observer machinery into `src/reactive/`, extend the payload to a pointer mode; no second class silently named `Reactive`. **Open question 5.** |
| 6 | "16-byte identity" described as new vs `MemoryHeader` already 16 B | T1 | Reuse `MemoryHeader`; do not invent a second header (the Self-Describing Memory Block Law's "zero secondary storage"). |
| 7 | 39 vs "38 (first char)" in the design | — | Treat 38 as a typo; canonical is 39. **Open question 3.** |
| 8 | Dashcode as 184-bit integer `% 1024` | T2 | Equivalent to a rolling hash mod 2^10 (weak low bits on ASCII). Recommend `Hash_murmur3Mix64(tail) & 1023` — same 1024 surface, real avalanche. **Open question 4.** |

---

## 5. Phased plan (each phase = cohesive per-file-pair commits inside `vexspoke`)

**Phase 0 — Vocabulary and law (docs only, no code).**
- `src/annotation/what.h`, `inherits.h`, `reactive.h` (+ build wiring if headers are listed).
- `preferences.md`: add the **WHAT Law**; add `;;INHERITS`/`;;REACTIVE` to the annotation list under the Two-Semicolon Annotation Style Law.
- `vexspoke-preferences.md`: mirror per the Per-Repo Preferences Extension Law (`;;SYNC` bump).
- New `oop/type.h` ids as needed (`ID_REFLECT`, `ID_VARIABLE_HASH`, `ID_METHOD`, program registry `PROJ_VEXSPOKE`).
- Commits: `docs(annotation): add WHAT/INHERITS/REACTIVE markers`, `docs(prefs): add the WHAT Law`.

**Phase 1 — The reflection atom.**
- `relational/variable.h` (or a new `reflection/` pair) gains the 32-byte record + `Reflect_*` verbs.
- Overview + definition blocks; symmetric getters/setters; `toString`/`toStringStruct`.
- Commit: `feat(reflection): unify name+pointer reflection atom`.

**Phase 2 — Hashing.**
- ✅ `util/hash.h`: `Hash_pointer` (`d156c52`).
- ✅ `relational/variable_hash_map.{c,h}`: the 39 × 1024 lazy `VariableHashMap`
  (`1bd6da5`, `63a5ea9`); 129-check suite green, ASan+UBSan clean.
- ⬜ `oop/class.*`: the per-class 39-bucket mini map for field/method lookup.

**Phase 3 — ChunkedList radix page table. DONE (commit `627bb5a`).**
- `struct/chunked_list.*`: generalized to N radix levels with a growable COW
  root; the variadic `ChunkedList(elementClass, stride, r0…leaf)` form and the
  `*_LAYER_DEFAULT` FourCC sentinels; page-sized leaves.
- The byte-budget form reduces exactly → hotcwap/graphvex untouched.
- Proof: 303-check byte-budget suite + 39-check radix suite, ASan+UBSan clean.

**Phase 4 — The `reactive/` subsystem.**
- `src/reactive/`: migrate `objects/reactive.c` in, add `valuePtr` mode + `Reactive_check`.
- Update `CMakeLists.txt` wiring; keep `objects/reactive.h` as a thin re-export shim if needed.
- Commit: `feat(reactive): add shared-value reactive with identity check`.

**Phase 5 — Proof and status.**
- `_tests/vexspoke/reflection_test.c` (the Test Segregation Law), building with `-Wall -Wextra -Werror`.
- `../../_repositories/.ecosystem/vexspoke.md` row writes (the Living Feature Readiness Law).

**Order note:** everything above is R2 `vexspoke`, a pure leaf (the Vertical
Integration Law), so there is no cross-repo dependency ordering — only the
prefs-first rule (the Living Preferences Law).

---

## 6. Verification

1. `cmake --build` the standalone `vexspoke` (the Standalone Autonomy Law) with
   `-Wall -Wextra -Werror -mcpu=native`, C23.
2. `_tests/vexspoke/reflection_test`: name-fold hashing determinism,
   collision chains, `Reactive_check` true/false on every id, `valuePtr` shared
   across N observers, drain coalescing, null/overlong/illegal name rejection
   (the Cold-Strict, Hot-Minimal Validation Law).
3. `-fsanitize=address,undefined` pass on the test binary.
4. No `->`, cast spacing, dest-last, two-layer access — grep-verifiable.

---

## 7. Open questions

**Resolved:** hash A = pointer identity; alphabet = 39 with `.` as splitter;
dashcode = Murmur3 `& 1023`; reactive = extend + `src/reactive/` + `void*` value;
atom = box + global identity cell (section 3.7); deep-layer paths = node walk
with `;;INTENTION` (section 3.8); `;;INHERITS` = note only; WHAT rollout =
retrofit as noticed; Phase 0 landed.

**Parked (next turn):** the reactive-switch contract — `;;INHERITS` signposts
`ElementName_revalidate()`, which is the sole updater on a reactive switch
(no deep propagation); the **string holdout** (deep bytes vs a reactive string)
needs its own discussion. See section 3.9.

**Remaining:**
1. Does the **name box** get a pointer *to the cell* only, or also a back-link
   field so `Reflect` can go box ⇄ cell in O(1) both ways?
2. Should the global phonebook be **one process-global table** or **one per
   scope** (global + per-object), matching today's two `Variable` tables?
3. `;;INHERITS` names a contract — should the required fields/functions be
   **listed in the annotation text** (`;;INHERITS("Element", "revalidate")`) or
   discovered by convention (`ElementName_revalidate`)?

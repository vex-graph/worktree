# Reflection Engine — Manifesto Audit & TODO

> Living checklist. Maps every bullet of the original manifesto dump to a status,
> with the commit or law that proves it and the exact work remaining.
> Legend: ✅ done · 🟧 partial · ⬜ not started · 🅿️ parked (decided, waiting).

---

## A. Reflection — the nested hierarchy

Names are free (`oop` Class/Field/Struct deleted; the registry renamed to
`SymbolTable` — commit `f6ff66b`), and the records now live under `reflection/`
and nest — commit `c2a560a`:

| Record | Shape | Size |
| :-- | :-- | :-- |
| `Variable` | name + read + target (base metadata) | 40 B |
| `Field` | **embeds** a `Variable` + setter — `field { variable }` | 48 B |
| `Method` | name + invoke + target | 40 B |
| `Struct` | name + count + a `ChunkedList` of Field rows — `struct { field }` | 40 B |
| `Class` | name + construct + `Struct *layout` + a `ChunkedList` of Method rows | 56 B |

- **Generic is gone** — a `Class` IS generic.
- Kind = the header `typeId` (`TYPE_REFLECT_*`); `Struct`/`Class` store their
  rows in never-moved `ChunkedList`s (page-sized leaves), so field/method rows
  are address-stable and growable.
- The class layout is borrowed; `Class_free` releases only the method list.

**Remaining sliver:** the names are records, not a *registry* — nothing yet
indexes them by name across a whole program (a `Reflection` registry of
segregated per-kind arrays).

---

## B. The variable atom — `[name 24 B][ptr 8 B]`

| Manifesto | Status | Evidence |
| :-- | :-- | :-- |
| 23 chars + 1 ending = 24-byte name | ✅ | `VariableSlot` `_Static_assert(sizeof == 32)`, `commit 160de41`. |
| 24 B name + 8 B ptr | ✅ | same. |
| used for variables + fields + classes + methods | 🟧 | atom exists; adoption across the four uses is pending (ties into A). |

Aligned with the **24-Byte Variable Slot Law (The 23+1 Rule)**.

---

## C. Hashing — two systems

| Manifesto | Status | Evidence / remaining |
| :-- | :-- | :-- |
| System A: `hash(void*)`, `sizeof(void*)` | ✅ | `Hash_pointer` (`commit d156c52`). |
| System B: relational hash → `VariableHashMap` | ✅ | landed (`commit 63a5ea9`). |
| 39 first-char buckets | ✅ | 39 = `a-z 0-9 _ $ -` (capitals fold; `.` is the **path splitter**, not a bucket). |
| dashcode → 1024 slots | ✅ | `Hash_murmur3Mix64(FNV1a(tail)) & 1023` (the decided delta from a raw 184-bit `% 1024`). |
| slots are lazily-minted chunked lists | ✅ | each occupied (bucket, slot) mints a `ChunkedList` of `VariableSlot` rows; collisions chain. |
| mini map for field/method names, per class (`void*[39].chunkedList`, 16/chunk) | ✅ | `VariableMiniMap` (39 single-level buckets, 16-row leaves — the manifesto's "16 indices per chunk") + `SegmentIndex_buildFromMini` scoped search (`5fd321a`). |
| "chunked lists already exist" | ✅ | and upgraded: radix page table + leaf tail-chain. |
| `ChunkedList(chunk amount)` arity ctor | ✅ | `ChunkedList(elementClass, stride, r0, …, leafRows)` variadic (`commit 627bb5a`). |

**Remaining:** Phase 2 — the 39 × 1024 `VariableHashMap` + Hash system B, then
the per-class mini map for field/method lookup.

---

## D. Reactive

The engine moved to `reactive/` and the typed reactives are landing.

| Manifesto | Status | Evidence / remaining |
| :-- | :-- | :-- |
| `vexspoke/reactive` directory | ✅ | `src/reactive/` — engine + typed reactives (`89d195a`, `9339427`). |
| one engine, typed facades | 🟧 | `Reactive` engine landed; **4 of 12** typed reactives (`Bool`, `Int`, `Double`, `String`). 8 left: `Char`, `Short`, `Long`, `Float`, `IntFloat`, `IntDouble`, `LongFloat`, `LongDouble`. |
| one word shared by N labels | 🟧 | the engine owns the atomic word; every facade casts it. |
| `Reactive_check(ptr, ID_…)` | ⬜ | reads the 16-byte header (`Memory_type`). |
| `Reactive_variable_set(ptr, value)` (relational) | ⬜ | the table-bound verb; next. |
| lazy promotion (only watched values react) | ⬜ | the scale answer: don't make 200M reactives. |
| `mem.c` 16-byte identity at malloc | ✅ | already live: `MemoryHeader { typeId, length, sugar }`. |
| atomic write + owner-affine drain | ✅ | the engine: write anywhere, notify on the owner, exact old/new (`(0, dirty, drain)`). |
| `objects/reactive.h` | ✅ | thin re-export shim → `reactive/reactive.h` (graphvex untouched). |

**Remaining:** Phase 4 — relocate + overhaul into `src/reactive/` with a shared
`void*` value, O(1) `Reactive_getValue`, and `Reactive_check`.

---

## E. Annotations & laws

| Manifesto | Status | Evidence |
| :-- | :-- | :-- |
| `;;INHERITS` (extends) | ✅ | `annotation/inherits.h` + clarified semantics (`commits 7b5a3e0`, `814d713`). |
| `;;REACTIVE("<objectName>")` | ✅ | `annotation/reactive.h` (`7b5a3e0`). |
| `;;WHAT("<type>")` | ✅ | `annotation/what.h` (`7b5a3e0`). |
| "the WHAT Law" | ✅ | Law 40 in `preferences.md` (`3617967`). |
| inline `void* WHAT("x") v;` | ✅ | decided: not expressible (annotation ≠ declarator) → line-above form only. |
| *(bonus)* Relational Engine proper name | ✅ | Identity & Naming Transition Law (`3d0d49e`). |
| *(bonus)* Cold-Only Reflection Law | ✅ | Law 41 (`3d0d49e`). |

---

## F. Storage (`ChunkedList`)

| Manifesto | Status | Evidence |
| :-- | :-- | :-- |
| chunked lists exist | ✅ | — |
| "128 blocks / 16 per chunk" growth feel | ✅ | radix page table, page-sized leaves (`627bb5a`). |
| no 64 MB up-front, flexible growth | ✅ | lazy leaves + growable root; chunk → chunk tail chain (`ae1ca73`). |

---

## G. Settled design, not yet built

| Item | Status | Note |
| :-- | :-- | :-- |
| Identity cell `[MemoryHeader 16][value/ptr 8][pad 8]` | ✅ | `Cell` landed (`commit 6879a6c`). |
| Global shelf (one table, graph, **u32 index edges**) | ✅ | `Shelf` landed: never-moved `ChunkedList` nodes, u32 edges, one cell per node (`6879a6c`). |
| Dotted-name **search** (the dot is a filter, not an address) | ✅ | positional `SegmentIndex` + ranked query (`c46768f`, `665b1b0`); retires the literal path getter. |
| `;;INTENTION` cold-walk marker | ✅ | on `SegmentIndex_query` (`665b1b0`). |
| Reactive switch + `ElementName_revalidate()` | 🅿️ | parked, section 3.9. |
| Reactive strings (the string holdout) | 🅿️ | parked, section 3.9. |

---

## Phases recap

| Phase | Status |
| :-- | :-- |
| 0 — annotations + WHAT Law | ✅ done |
| 1 — reflection atom | ✅ atom + cell + shelf + dotted-name search |
| 2 — hashing | ✅ `Hash_pointer` + `VariableHashMap` + scoped `VariableMiniMap` |
| 3 — `ChunkedList` radix page table | ✅ done |
| 4 — `reactive/` subsystem | ⬜ not started |
| 5 — tests + readiness rows | 🟧 tests green for what's landed; wiki rows not written |

---

## Ordered next TODOs

1. ~~**Phase 2a — Hash system B + `VariableHashMap`.**~~ ✅ **DONE** (`commits 1bd6da5`, `63a5ea9`).
2. ~~**Phase 1b — identity cell + the global shelf.**~~ ✅ **DONE** (`commit 6879a6c`).
3. ~~**Phase 1c — node-walk resolver.**~~ ✅ **REVISED + DONE**: the dot is a
   filter, not an address — the literal getter is retired and replaced by the
   ranked positional search (`c46768f`, `665b1b0`).
4. ~~**Phase 2b — per-class mini map.**~~ ✅ **DONE** (`5fd321a`): the 39-bucket
   `VariableMiniMap` + scoped `SegmentIndex_buildFromMini`. A small follow-up can
   wire one into `Class` so each class owns its field/method index.
5. **Reflection kinds + nesting** — ✅ done (`1e3ab12`, `c2a560a`): Variable ⊂
   Field ⊂ Struct ⊂ Class, plus Method; Generic dropped. The segregated
   `Reflection` registry is the remaining sliver.
6. **Phase 4 — `src/reactive/`** overhaul: shared `void*` value,
   `Reactive_getValue` O(1), `Reactive_check`.
7. **Phase 5 — readiness rows** in `_repositories/.ecosystem/vexspoke.md`
   (the Living Feature Readiness Law) for everything landed.
8. **Parked** — reactive switch / `revalidate` / reactive strings.

---

## Honest verdict

**Not done.** Everything but the reflection registry and reactive is in: laws,
atom, storage, hashing, search, the scoped mini map, the identity cell, the
shelf, and the nested reflection hierarchy. Rough completion of the manifesto:
**~92%**, and the remaining ~8% is the `Reflection` registry plus Phase 4.

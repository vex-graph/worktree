# Lesson 7: FFM Alignment → C Alignment (The Padding You Cannot See)

In Java FFM you called `getLongUnaligned()` and packed layouts byte-tight without fear. In C, the compiler inserts invisible padding into structs, and misaligned access is undefined behavior that happens to work on arm64 — until it doesn't (vector instructions, atomics, and future CPUs fault).

## 1. `sizeof` Lies About Your Mental Model
Java FFM: layout is exactly what you declared. C: `struct { uint32_t a; uint64_t b; }` is 16 bytes, not 12 — 4 hidden pad bytes after `a`.
- Your `MemoryHeader` is 4×`uint32_t` = exactly 16 bytes with no padding (`_Static_assert(sizeof == 16)` in `src/nio/mem.h`). That assert is load-bearing: if anyone adds a field, the 16-byte doctrine silently breaks.
- Watch for: adding a field to any header/packed struct without re-checking `sizeof` and slot math.

## 2. Unaligned Access Has No `getLongUnaligned` Here
`ForeignMemory.getLongUnaligned()` does not exist in C. The safe equivalent is `memcpy` into a local:
```c
uint64_t v; memcpy(&v, ptr, sizeof(v));   // safe, optimizer folds it
```
Never `*(uint64_t*) ptr` on a possibly-odd address — that is UB even when it works.
- Watch for: parsing network/file bytes (`net/`, `io/`) by casting. Copy first.

## 3. The `&15` Guards Are a Contract, Not a Check
`Memory_free/length/type` reject pointers where `(u & 15) != 0` (`src/nio/mem.c`). This is only valid because every allocator path guarantees 16-alignment by construction (malloc base + multiples of 16). The guard documents an invariant; it does not create one.
- This toolchain's `_Alignas` rejects typedef application, so the compiler cannot enforce it — the comment in `mem.h` says so. If you ever change slab sizes to a non-multiple of 16, the guards start rejecting *valid* pointers.
- Watch for: any new slab size, any new arena, any `malloc` path must preserve 16-alignment or the guards become a self-inflicted DoS.

## 4. Atomics Demand Their Alignment Too
`_Atomic` loads/stores on misaligned addresses fault on some ARM cores even when plain access works. Every `atomic_*` target (`SpinLock`, generation counters, FPS telemetry) must be naturally aligned.
- Watch for: packing atomics into byte-tight structs. Keep atomics in their own 4/8-byte-aligned fields, never inside packed layouts.

## Watch-out Summary
| Java habit | C consequence | Defense |
|---|---|---|
| Tight FFM layouts | Hidden compiler padding | `sizeof` static asserts on every header |
| `getLongUnaligned()` | UB misaligned deref | `memcpy`-into-local idiom |
| Assuming alignment | Guards reject valid ptrs | New slabs/sizes must stay ×16 |
| Atomics in packed structs | Hardware fault on some cores | Atomics only in aligned fields |

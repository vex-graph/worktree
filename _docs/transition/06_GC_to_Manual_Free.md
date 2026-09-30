# Lesson 6: GC → Manual Free (Ownership Is Your New Garbage Collector)

In Java, even off-heap, you had `arena.close()` as a backstop and the GC watching everything else. In C there is no backstop. Every `Memory_alloc` must have exactly one owner who frees it, or it leaks forever. There is no leak detector unless you build one.

## 1. The One-Owner Rule
Java: last reference drops, GC reclaims. C: nobody reclaims. Before writing any allocation, answer: **who frees this, and when?** If you cannot name the owner in one sentence, do not allocate.
- `Picture_0()` allocates base + picture → `Picture` owns both; `Memory_free(pic)` must release both (see `darling/picture.c`).
- Watch for: allocating in a constructor and freeing only half in the teardown path.

## 2. Double-Free Is a Crash, Not an Exception
Java: `arena.close()` twice is (mostly) safe. C: `free` twice corrupts the pool and crashes *later*, far from the bug.
- Your defense is the magic poison: `Memory_free` sets `(*h).magic = 0` (`src/nio/mem.c`), so a second free fails the magic check and returns silently.
- Watch for: any new pool/freelist you write MUST poison on free and check on alloc, or double-free becomes silent corruption.

## 3. `Memory_freeAll` Is Not `arena.close()`
`freeAll` rebuilds every slab freelist in O(1) — it does not run destructors, close file handles, or release `IOSurfaceRef`s. Java finalizers (unreliable as they were) at least existed. Here, non-memory resources leak silently across `freeAll`.
- Watch for: `VkIOSurface`, `CALayer`, file descriptors, `malloc` overflow blocks (`SLAB_SYSTEM` calls `free`, but only via `Memory_free`, not `freeAll`).
- Rule: if a struct owns anything that is not slab memory, it needs an explicit teardown function called *before* `freeAll`.

## 4. Leak Detection Checklist (Run Monthly)
- [ ] Every `Memory_alloc` site has a matching free on all paths (including early `return nullptr` paths — the most common leak).
- [ ] Every early-return after a partial construction frees what was already built (`Picture_0` pattern: free `p` if `basePanel` fails).
- [ ] No `malloc` outside `mem.c` overflow fallback and image decode scratch (grep it).
- [ ] `s_masterArena` growth is flat across 10 minutes of `vk_test` (growth = leak).

## Watch-out Summary
| Java habit | C consequence | Defense |
|---|---|---|
| Forgetting `free` | Silent native leak, no GC to save you | One-owner rule, checklist |
| Double `close()` | Heap corruption, delayed crash | Magic poison on free |
| `arena.close()` cleanup | Leaked GPU/file handles | Explicit teardown before `freeAll` |
| Early return | Half-built object leaks | Free-before-return discipline |

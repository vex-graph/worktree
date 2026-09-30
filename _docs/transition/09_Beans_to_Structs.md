# Lesson 9: Beans → Structs (Identity, Equality, and the `void*` Trap)

Java objects have identity (`==`), equality (`.equals`), and types the compiler checks. Your C structs have addresses, and half your APIs take `void*`. This lesson is about what you lost in translation and how your conventions buy it back.

## 1. Pointer Equality Is Identity — Nothing Else
Java: `a.equals(b)` compares content. C: `child == scenePanel` compares addresses. Two panels with identical fields are *different* objects.
- Your dispatch pattern (`Type_class(Memory_type(node)) == ID_PICTURE` in `darling/canvas.c`) recovers *kind*, not value. There is no `.equals` anywhere — if you ever need content comparison (dirty-checking, layout caching), you must write a field-by-field comparator. Do not use `memcmp` on structs: hidden padding bytes make identical structs compare unequal.
- Watch for: `memcmp` on any struct with padding. Compare field by field.

## 2. `void*` Is `Object` Without `instanceof`
Java: casting `Object` to the wrong type throws `ClassCastException`. C: casting `void*` to the wrong struct silently reinterprets memory.
- `Picture.image`, `Panel.filters`, `Panel_RenderFn(renderer, cmdBuffer)` are all `void*` — every one is a cast waiting to be wrong. Your only runtime check is the `Memory_type` header *when the pointer came from your allocator*. Foreign pointers (stack, static, CoreFoundation) have no header — `Memory_type` on them is UB, which is why the `&15` + magic guards exist.
- Watch for: every new `void*` field needs a one-line comment naming the real type AND a `Memory_type` check at the cast site when the pointer is allocator-owned. `Canvas_resolveRoot` is the template.

## 3. Getters/Setters Are API, Not Encapsulation
Java: `private` fields + beans = enforced encapsulation. C: every field is one `(*p).field` away from anyone — your getters are convention, not walls.
- Their real value here is threefold: (a) null-safety at one choke point, (b) dirty-marking on mutation (`Container_markDirty` inside setters — the thing direct writes skip), (c) a stable surface for AI callers. Skipping a setter to write a field directly drops the dirty mark and produces a stale-layout bug that looks like a render bug (your picture investigation nearly went there).
- Watch for: direct field writes outside the owning file. If you write `(*x).field = v` and the struct has a setter, you probably just dropped a side effect. Grep your own diffs for this.

## 4. Lifetimes Are Not Reachability
Java: referenced objects stay alive. C: `Panel_addContainer` stores a raw pointer — if the child is freed elsewhere, the parent holds a dangling pointer with no `WeakReference` to warn you. The hot-swap retirement ring exists precisely because C has no reachability.
- Watch for: removing/freeing a panel without detaching it from its parent and the `PanelCocoa` registry first. Detach order is: registry → parent → free. Never free-then-detach.

## Watch-out Summary
| Java habit | C consequence | Defense |
|---|---|---|
| `.equals()` | `memcmp` lies on padding | Field-by-field comparators |
| Bad cast throws | Bad cast corrupts silently | Comment the real type; `Memory_type` at cast |
| Private + beans | Convention only, no walls | Always use setters (dirty marks) |
| GC reachability | Dangling parent/child ptrs | Detach → free; retirement rings |

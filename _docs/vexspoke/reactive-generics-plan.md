# Reactive Generics Plan (vexspoke)

Status: **DRAFT for review** — nothing here is built yet. Scope is `ecosystem/vexspoke` only.

## Goal

Give vexspoke a real **generic reactive** — `Reactive(T)` — that stamps the whole typed
family (`ReactiveInt`, `ReactiveVec4`, `ReactiveString`, …) over the existing `Reactive`
engine, plus the **merged** `ReactiveProbable(T)`. This is the first real "generics"
surface in the ecosystem.

## The load-bearing insight (agreed)

The reactive's bell can only ring from **inside** the object that owns the value. So
"reactive" and "probable" cannot be nested — they must be **merged** into one class.
Therefore:

- `Reactive(T)` — a plain typed reactive over `T`.
- `ReactiveProbable(T)` — the merged probable+reactive; the value is *both* weight-gated
  and observable.
- **No nesting, ever.** `Reactive<Probable<T>>` does not exist. If a consumer wants a
  reactive over a probable, they reach for the merged class, by intent.
- The plain (bell-less) `Probable<T>` stays a separate, non-reactive thing.

## Agreed design

### The engine (`Reactive`) — unchanged contract

One atomic word + shadow + `_Atomic bool dirty` + observer arrays. `set` is atomic from
any thread and **never** fires; the owner thread calls `drain`, which coalesces the
pending writes into one batch and fires observers **on the owner's thread** (the
Present-On-Demand Law; no locks, no unbounded waits — the Bounded Wait Law).

The raw ops keep this contract but are **renamed** (`Reactive_set` → `Reactive_store`,
`Reactive_get` → `Reactive_load`, …) because the plain names become the generic dispatch
macros (see *Generic functions* below).

### Storage: one uniform slot, typed by the class

"Can it be both?" — yes. Behind the scenes the engine is a single `void*`-shaped word;
the class is the face:

- **Scalar T** (int, long, float, double, bool, short, byte, char): the value rides
  *inside* the word (bit-cast for floats, so every pattern round-trips).
- **Struct T** (Vec2/Vec3/Vec4, Rectangle, …): the word holds a **`T*`** — a pointer to
  the value. A change is a **re-bind** (publish a new block), exactly like
  `ReactiveString` today.

Same engine either way. The class decides what to stuff in the slot.

### Channels (four)

| Channel | Fires when | Notes |
|---|---|---|
| `onSet` | a set happened | fires even if the value is the same |
| `onChanged` | the value actually moved | never fires on a same-value set |
| `onGet` | the value is read | fires **in the same call** that returns the value |
| `onNullptr` | the slot became empty | **pointer-family only** |

- **`onGet` is a one-fire read.** `get` returns the value **and** fires the `onGet`
  observers in the same call (immediate; not deferred to `drain`). Observer code runs on
  the caller's thread, so `get`-with-observers is an owner-thread call, marked
  `;;INTENTION` per the Conflict Triage Law. With no `onGet` observer bound, the get stays
  a single atomic load (safe against the Cold-Strict, Hot-Minimal Validation Law).
- **`onNullptr` only means something for pointer-y T.** For `ReactiveInt`, zero is a real
  value, not "empty." So it is offered on the pointer family (String, Vec*, Rectangle,
  probable) and not on scalars.
- **No `onRemove` channel.** The bound value cannot be "removed" — it is bound. (The
  engine's internal teardown notify for unbinding observers is separate from the four
  event channels and stays.)

### Observers: the `**()[]` system

Each channel is a **growable array of function pointers backed by a vexspoke container**
(`struct/List`), whose elements are observer records
(`ReactiveObserver { void* cb; void* userdata; }`). Add appends (multiple callbacks per
channel); firing runs **all** of them; remove compares the **function-pointer address**
(plus `userdata`) and drops the match, so the removed callback can never fire again.

Mid-fire removal stays safe (`reactive_test.c` asserts a callback can remove itself while
firing). `List_remove` shifts the tail left, so a fire must be shift-safe: walk the list
**backward** (a removal only touches already-visited indices), or **tombstone** the slot
(zero it, reuse it on the next add). Decision noted under Resolved.

### Typed callbacks

Callbacks are typed against `T`:

```c
typedef void (*ReactiveIntSetFn)(int32_t value, void *userdata);
typedef void (*ReactiveIntChangedFn)(int32_t oldValue, int32_t newValue, void *userdata);
typedef void (*ReactiveIntGetFn)(int32_t value, void *userdata);
typedef void (*ReactiveIntNullptrFn)(void *userdata);
```

The engine's slots hold the function pointer as `void*` (so `**()[]` is untouched); the
per-type class casts each slot back to its **proper typed signature** and fires it. The
engine carries `void*`; the face knows the types.

### The generic surface

```c
// reactive/generic.h
#define VEX_CAT_(a, b) a##b
#define VEX_CAT(a, b)  VEX_CAT_(a, b)

#define Reactive(T)         VEX_CAT(Reactive_, T)
#define ReactiveProbable(T) VEX_CAT(ReactiveProbable_, T)

// alias table: mangled token -> camelCase class name (the Function/Class Naming Law)
#define Reactive_int    ReactiveInt
#define Reactive_Vec4   ReactiveVec4
#define Reactive_String ReactiveString
```

`Reactive(Probable(int))`-style *nesting* is deliberately rejected by design; the type
argument is always a leaf type (`int`, `Vec4`, `String`, …), and each resolved name is a
real, concrete, single-class-per-file class.

### Generic functions — Java-like, statically typed

The type is not the only generic; the **functions** are too. Proven under
`-std=c23 -Wall -Wextra -Werror`:

```c
Reactive(Rect) *bounds = Reactive(Rect)(&box);   // ctor via the generic spelling
Reactive(Int)  *count  = Reactive(Int)(7);

Rect    *b = Reactive_get(bounds);               // statically Rect*
int32_t  n = Reactive_get(count);                // statically int32_t

Reactive_set(bounds, &box);                      // -> ReactiveRect_set
Reactive_set(count, n + 1);                      // -> ReactiveInt_set
```

Each generic function is a `_Generic` dispatch on the reactive pointer, listing the
family plus a `Reactive*` arm for the bare engine:

```c
#define Reactive_set(r, v) _Generic((r), \
    ReactiveInt  *: ReactiveInt_set,     \
    ReactiveRect *: ReactiveRect_set,    \
    Reactive     *: Reactive_store       \
    )((r), (v))
```

`Reactive(Rect)(&box)` composes: the mangle yields `ReactiveRect`, which is then called as
the class constructor. The same dispatch covers `Reactive_get`, `Reactive_drain`,
`Reactive_addOnSet`, `Reactive_addOnChanged`, `Reactive_addOnGet`, `Reactive_addOnNullptr`
(and their `removeOn*`).

Consequence: the engine's raw ops are renamed (see above), and every consumer includes
`reactive/generic.h` — which pulls the family headers so **every `_Generic` arm is
declared** before use. Existing `tests/` and the graphvex `Label` keep compiling unchanged
in text; they resolve through the `Reactive*` arm.

### Why `Reactive(T)` and not `REACTIVE(T)`

`Reactive(...)` was **already a macro** — the base engine's arity-constructor chooser
(`c23/constructor.h`). But a workspace-wide grep shows that chooser is **never called
anywhere** (only comments mention it). So this cycle **retires** the bare chooser and
**promotes the token** to the generic:

```c
// before — the bare class's constructor chooser (unused; retired)
#define Reactive(...) CONSTRUCTOR_DISPATCH(Reactive, __VA_ARGS__)

// after — the family constructor (the generic)
#define Reactive(T) VEX_CAT(Reactive_, T)
```

`Reactive_1` / `Reactive_2` remain the engine's real constructors for embedding; a bare
engine is never built through `Reactive(...)` in the first place. `Reactive` stops being
"the bare class's constructor" and becomes "the family constructor" — the same honesty
move that abolished the `;;REACTIVE` annotation (reactivity is expressed by the **type**).
This is a Tier-3 (syntactic) managed exception under the Conflict Triage Law: the base
class's `Class(...)` sugar is retired because the token is promoted to the generic surface.

## Dead code to remove

`src/annotation/reactive.h` (`;;REACTIVE("...")`) is **never included and never used**
anywhere in the ecosystem — verified by grep. It is abolished this cycle. Reactivity is
now expressed by the **type** (`ReactiveInt`), not by an annotation. This cycle also
retires the unused bare `Reactive(...)` constructor chooser so the token can serve as the
generic (see above).

## Mechanism (proven)

The two-level `VEX_CAT` indirection lets a nested macro argument expand before pasting
(GCC Argument Prescan; MS Learn on `##`). Verified on this machine under
`-std=c23 -Wall -Wextra -Werror`:

```
Reactive(int)              -> Reactive_int  -> ReactiveInt
Reactive(Probable(int))    -> rejected by intent (no nesting)
```

A macro body can also emit a complete concrete class. (Nesting *is* mechanically
possible; we are choosing not to use it.)

## Files

**Add**
- `src/reactive/generic.h` — the `VEX_CAT` mangle, `Reactive(T)` / `ReactiveProbable(T)`,
  and the alias table.
- `src/reactive/reactive_tmpl.{h,c}` — the template (no include guard), parameterized by
  `VEX_NAME` / `VEX_T`; emits the struct, the four channels, `addOn`/`removeOn`, typed
  `drain`, `set`/`get`, `toString`/`toStringStruct` (the toString Law), and the arity
  constructors (the Construction and arity clause).
- Per-instantiation pairs generated from the template: `reactive_int.{h,c}` (rebuilt as
  the parity proof), then the rest of the family.
- `src/reactive/reactive_probable.{h,c}` + per-T instantiations for the merged class.

**Change**
- `src/reactive/reactive.{h,c}` — retire the `Reactive(...)` constructor chooser; expose
  the batch-consume step (`Reactive_take`) so the typed `drain` can fire typed; add any
  missing channel lists.
- `CMakeLists.txt` — wire the new sources and the `-Wall -Wextra -Werror` test harnesses.
- `src/oop/type.h` — class ids for the new instantiations (the One Type Registry Law);
  the wrapper nibbles (`WRAP_REACTIVE`, `WRAP2_PROBABLE`) already carry the composition.

**Delete**
- `src/annotation/reactive.h`.

**Tests** (`tests/vexspoke/`, the Test Segregation Law)
- Keep `reactive_test.c` and `reactive_typed_test.c` green.
- Add `reactive_generic_test.c`: build `Reactive(int)`, add three `onChanged` callbacks,
  remove one by address, prove it can never fire again; same for `onNullptr` on a
  pointer-backed type.

## Resolved (this cycle)

1. **Observer storage — a vexspoke `List`, reused as the engine's channel arrays.** One
   source of truth. Because callbacks are typed (`fn(T value)`) but the slots are `void*`,
   the **per-type class casts each slot back to its typed signature** when firing — the
   generic reactive fires through its own typed `drain`, never the raw `Reactive_drain`
   (rule marked `;;INTENTION`). Fire is shift-safe (backward walk or tombstone).
2. **`onGet` — kept, as a one-fire read** (returns the value and fires in the same call).

## Open questions

3. **Merged macro spelling** — `ReactiveProbable(T)` → `ReactiveProbableInt`? Confirm the
   final names.
4. **Family member list** — confirm the full 18: Byte, Short, Char, Int, Long, Float,
   Double, LongFloat, IntFloat, IntDouble, LongDouble, String, Vec2, Vec3, Vec4,
   Rectangle, (Probable, ProbableObjects merged), + engine.

## Verification

- `cmake --build` clean under `-Wall -Wextra -Werror`.
- `reactive_test` and `reactive_typed_test` still pass unchanged.
- New `reactive_generic_test` proves: multi-callback fan-out, remove-by-address kills a
  callback, `onSet` fires on a same-value set while `onChanged` does not, `onNullptr`
  fires on the pointer family, `onGet` fires only on the cold path.
- `Reactive(int)` produces a class byte-identical in behavior to the hand-written
  `ReactiveInt` (the parity proof that the generic is not a regression).

## Commit sequence (the Git Workflow Law)

1. **Remove the dead annotation** — delete `src/annotation/reactive.h`, drop any
   preference/index mention. One concern.
2. **Generic layer + parity proof** — add `generic.h`, `reactive_tmpl.{h,c}`, retire the
   `Reactive(...)` chooser, rebuild `ReactiveInt` from the template; tests green.
3. **Roll the scalar family** — Byte, Short, Char, Long, Float, IntFloat, IntDouble,
   LongFloat, LongDouble.
4. **Pointer family** — Vec2, Vec3, Vec4, Rectangle (pointer-word; rebind = change).
5. **Generic function dispatch** — add the `Reactive_*` `_Generic` macros in `reactive/generic.h`;
   rename the engine raw ops (`Reactive_store`/`Reactive_load`/…); add the `Reactive*` arm
   so `tests/` and the graphvex `Label` keep compiling. **This step needs the family to
   exist first** (every `_Generic` arm must be declared).
6. **Merged `ReactiveProbable(T)`** (+ `ReactiveProbableObjects<T>`).
7. **Living docs** — `vexspoke-preferences.md` + readiness row in the same cycle
   (the Living Documentation Law).

## Law notes

- Single Class Per File Law (Java Law): every instantiation is its own `.h`/`.c` pair.
- Semantic Consistency Law (Construction and arity, Argument order, Access depth): the
  template emits `_0`/`_1`/… and the `Class(...)` chooser, dest-last, `(*p).field`.
- toString Law: every generated class ships `toString` and `toStringStruct`.
- WHAT Law: `void*` observer slots carry `;;WHAT("...")`.
- AI-First Architecture Manifesto Law: the template is written once; the family is
  stamped out by machine.

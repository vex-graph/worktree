# Lesson 8: Exceptions → Error Codes (Fail Closed, Fail Loud)

Java gave you `try/catch`, stack traces, and `NullPointerException` pointing at the line. C gives you a segfault, a corrupt frame three seconds later, or silence. Your error strategy must be: **validate at the boundary, fail closed inside**.

## 1. Every Pointer Parameter Is Guilty Until Proven Innocent
Java: NPE tells you where. C: dereferencing `nullptr` kills the process with no message.
- Your convention is already right: getters return safe defaults (`nullptr`, `0`, `false`) on null `self` (preferences Rule 24 #5). Keep it absolute — no getter may dereference before the null check.
- Watch for: new setters that write `(*p).field` before checking `p`. Setters mutate; a null write is a crash, not an exception.

## 2. Sentinels Replace `throw`
Java: `throw new DecodeException(path)`. C: return `-1` / `nullptr` and log at the call site.
- `Texture_load` returns `-1`, `Texture_loadRaw` returns `-1`, `PanelCocoa_new` returns `nullptr`. Callers MUST branch: `vk_test.c:pic_render` checks `s_sunflowerId < 0` and draws the orange fallback. That fallback is the C equivalent of a catch block — visible degradation instead of a crash.
- Watch for: the two failure modes Java devs write in C — (a) ignoring a `-1` and using it as an array index, (b) logging the error and *continuing as if it succeeded*. Log-and-continue is the C version of swallowing exceptions.

## 3. Magic Numbers Are Exceptions Without Types
`text_sdf.frag` used `u_bold < -0.1` as a shadow flag — a secret protocol between shader and C with no type, no name, no compiler check. Java would have made this an enum. The fix (`MODE_SHADOW_SENTINEL`, `MODE_COLOR_GLYPH_SENTINEL`) is the same lesson: name every out-of-band signal.
- Watch for: any new `if (x < 0)` / `if (x == -1)` special-case. Give it a named constant at minimum, a separate field or flag at best.

## 4. Asserts Are Development Seatbelts, Not Runtime Brakes
`_Static_assert` (layout sizes, annotation markers) costs zero and catches refactors at compile time — use it aggressively. Runtime `assert()` vanishes under `-DNDEBUG` (Release), so it must never guard a code path the program depends on.
- Rule: `_Static_assert` for invariants the compiler can check; explicit `if (!x) return default;` for everything at runtime.

## Watch-out Summary
| Java habit | C consequence | Defense |
|---|---|---|
| NPE with stack trace | Silent segfault | Null-check every deref, safe defaults |
| `throw` + `catch` | Ignored `-1` becomes index/handle | Branch on every sentinel; fallback render |
| Log-and-continue | Corruption downstream | Fail closed: return, skip, or degrade visibly |
| Magic values | Untyped cross-layer protocol | Named constants; separate flags |
| `assert` as logic | Vanishes in Release | `assert` never guards live paths |

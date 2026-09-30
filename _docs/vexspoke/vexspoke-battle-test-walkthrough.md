# vexspoke Battle-Test — Walkthrough (Wave 0 + Wave 1, slice 1)

**Date:** 2026-09-29 · **Host:** macOS arm64, C23, Debug (`DEBUG_BORROW_CHECK=1`).
**Constitution:** `ecosystem/vexspoke/preferences.md` + `tests/test-preferences.md`; laws cited by
**Title** (the Law Identity Doctrine).

This is the first execution slice of `vexspoke-battle-test-plan.md`. It lands the continuous gate and
the first three per-file owner tests of the memory core (Wave 1).

---

## 1. Wave 0 — unblock the umbrella build (DONE)

Five targets failed to compile after the reactive-generics refactor (`ReactiveFloat`/`ReactiveBool`
became pointer types while call sites still used scalars). Fixed to the `GraphicsComponent_setSize` /
`Reactive*_get` idiom:

| File | Fix |
| :--- | :--- |
| `tests/darling/slider_test.c` | `(*cnt).w/h = …` → `GraphicsComponent_setSize(cnt, 200, 20)` |
| `tests/darling/knob_test.c` | → `GraphicsComponent_setSize(cnt, 40, 40)` |
| `tests/darling/scrollbar_test.c` | → `GraphicsComponent_setSize(cnt, 20, 200)` and `(cnt, 20, 0)` |
| `ecosystem/graphvex/tests/panel_paint_test.c` | `(*gc).visible` → `ReactiveBool_get((*gc).visible)` |

`main/test_suite.c` was already corrected to `GraphicsComponent_getWidth/Height`. Result: **full
umbrella build green (0 failures)**.

---

## 2. The continuous process (DONE)

Three of the four wiring pieces are now in place:

1. **Owner-test registry.** `ecosystem/vexspoke/CMakeLists.txt` records every created `*_test` target
   in a GLOBAL property (`VEXSPOKE_OWNER_TESTS`), so the aggregator never re-lists them.
2. **`ctest` registration + `run_vexspoke_tests`.** `tests/CMakeLists.txt` registers every registered
   owner test with a bounded `TIMEOUT 60` and defines the `run_vexspoke_tests` gate. Count went
   **4 → 94** vexspoke tests under `ctest`.
3. **Coverage ratchet.** `tests/tools/vexspoke_coverage_ratchet.py` derives the compiled-unit list from
   the owning repo's CMakeLists and fails when a unit has no dedicated owner test. The baseline
   `tests/vexspoke/coverage_baseline.txt` (101 → **98** entries) may only shrink.

**Gate result:** `ctest --test-dir build-verify` → **100% passed, 95/95** (incl. the ratchet).

*(Pending #4: the ledger paragraph in `tests/test-preferences.md`.)*

---

## 3. Wave 1, slice 1 — three owner tests (DONE)

| Unit | Owner test | Rows exercised |
| :--- | :--- | :--- |
| `nio/mem.c` | `tests/vexspoke/nio/mem_test.c` | boundary (0-len, nullptr getters), overflow guard, pointer legitimacy in an isolated `fork` child, failure atomicity (refused realloc), freed-header rejection, double-free, `freeAll`, arena isolation + destroy guards, transient lifetime/generation |
| `oop/type.c` | `tests/vexspoke/oop/type_test.c` | bit-field isolation, every form/modifier/wrapper predicate, arch byte, buffer-family chain, registry adversarial rejections (zero/stray/`PROJ_VEXSPOKE`/null-with-count), idempotence, exponential slate growth |
| `util/hash.c` | `tests/vexspoke/util/hash_test.c` | FNV-1a pinned reference vectors, nullptr/empty boundaries, determinism, Murmur3 avalanche (≥¼ bits flip per input bit) |

Baseline shrank 101 → 98; ratchet re-verified green.

---

## 4. Sanitizers (per-wave, always-on) — DONE for this slice

A sanitizer build (ASan + UBSan) compiled the vexspoke library and 12 owner tests. **All 12 exited 0**,
including the three new tests. No address, alignment, or undefined-behaviour findings in the exercised
paths.

---

## 5. Defect found (report only — not fixed)

**D1 — `Transient_alloc` lacks the `UINT32_MAX` overflow guard** (`ecosystem/vexspoke/src/nio/mem.c`).
The Overflow Guard Law states `Transient_alloc` "carries the `UINT32_MAX` guard that `arena_alloc`
has". It does not: `Transient_alloc(ID_INT, SIZE_MAX)` returns a **non-null** pointer (the `(n + 15) &
~15` alignment wraps to 0, so the capacity check passes). `arena_alloc` correctly rejects with
`numBytes > UINT32_MAX`.

`mem_test.c` records this as a **stated gap** (`KNOWN GAP (unproved)`, non-failing) per the Executable
Evidence Law — a skip is neither a pass nor a failure. Proposed one-line fix: add
`if (numBytes > UINT32_MAX) return nullptr;` at the top of `Transient_alloc`. On approval, the gap is
converted to a strict assertion.

---

## 6. Remaining in Wave 1

- **c23 header-only owners (4):** `fn.h`, `overload.h`, `constructor.h`, `zero.h` — own test each.
- **Upgrade the 6 existing owners** to the full battle-test contract: `bit/bit_test`, `c23/equals_test`,
  `c23/free_test`, `oop/stride_test`, `util/arrays_test`, `util/random_test`.
- Then Wave 2 (scalars + math: 36 units).

---

## 7. Commit boundaries (uncommitted; no push — the No Auto-Pushing Law)

- `tests/` repo: `darling/{slider,knob,scrollbar}_test.c`, `CMakeLists.txt`, `tools/`, `vexspoke/{nio,oop,util}/…`,
  `vexspoke/coverage_baseline.txt`.
- `graphvex` repo: `tests/panel_paint_test.c`.
- `vexspoke` repo: `CMakeLists.txt` (owner-test registry + unit list). *(The `main/test_suite.c` fix is
  in the umbrella root, which has no remote.)*

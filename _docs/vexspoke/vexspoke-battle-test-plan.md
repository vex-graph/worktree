# vexspoke Battle-Test Plan — One Real Owner Test Per File Unit

**Status:** `;;IN PROGRESS` — Wave 0 (build unblock) **done**; the continuous gate is **live**
(scoreboard: 95/95 ctest pass, coverage ratchet baseline 98); Wave 1 slice 1 (memory core: `nio/mem`,
`oop/type`, `util/hash`) **done** and ASan/UBSan-clean. See
`vexspoke-battle-test-walkthrough.md`. Next: c23 header-only owners + the 6 existing-test upgrades.
**Scope:** `ecosystem/vexspoke` (R2 substrate) + the umbrella `tests/` repository.
**Supersedes:** the report-only assessment (`vexspoke-test-assessment.md`); that document is the
baseline this plan moves from.
**Constitution:** `ecosystem/vexspoke/preferences.md` (architecture) and `tests/test-preferences.md`
(proof law). Laws are cited by **Title**, never number (the **Law Identity Doctrine**).

---

## 1. The standard (what the user asked for)

> "Each file and its own thing should have a test — and I mean real freaking stress: negative,
> overflow, nullptr, racing conditions, unusual behavior, freeing — to ensure it really worked in
> production."

Restated as law: **one owner test per file unit** (the **Per-File Battle Test Law**), and that test is
a **battle test**, not a smoke test. A green smoke test is not evidence. "Battle tested" is a recorded,
repeatable result with declared limits (the **Executable Evidence and Readiness Law**).

### 1.1 The per-file battle-test contract (the checklist every owner test must satisfy)

Each owner test for a unit is written against that unit's public contract (the **Contract Before
Cases Law**) and must carry the applicable rows below. "Applicable" is asserted explicitly — an
inapplicable law is stated as such, never silently skipped.

| Part I law | Concrete obligation in the owner test |
| :--- | :--- |
| **Contract Before Cases Law** | Read the `.h`; every asserted result traces to a documented post-condition. |
| **Public Surface Proof Law** | Every public function/symbol of the unit is invoked at least once. |
| **Value Boundary Matrix Law** | `0`, empty, one, size, size+1, `SIZE_MAX`/overflow; `NULL`/`""`/`{}`; negatives where representable. |
| **Pointer, Identity, and Dereference Safety Law** | wrong / misaligned / interior / foreign-arena / freed-stale pointer, forged type or project id, tampered header. Each rejection preserves unrelated state. |
| **Arity and Variadic Dispatch Law** | variadic / dispatch paths get their own arity cases. |
| **Failure Atomicity and Recovery Law** | a refused operation leaves the object byte-identical; the next good op succeeds. |
| **Failure Observability Law** | record the exact observable (`false` / `0` / `nullptr` / safe default) **and** the stderr line on cold rejections. |
| **Determinism and Reproducibility Law** | identical input → identical output; any randomness is seeded and recorded; no clock/address dependence. |
| **Resource and Lifetime Law** | construct→use→destroy; double-init; use-after-shutdown; failed-construction cleanup; leak-free under ASan; borrowed-vs-owned asserted once. |
| **Concurrency and Bounded Progress Law** | race-bearing units run MPMC / lock-contention cases under **TSan** with an external bounded watchdog (no unbounded wait). |
| **Adversarial and Hostile-Input Proof Law** | garbage, truncated, huge, and malformed inputs are rejected, not UB. |
| **Hot-Path Minimal Guard Law** | hot getters/setters keep minimal guards; `;;HOTCODE` sites are covered. |
| **Runtime-Level Seam Law** | the unit is exercised through its real R2 seam (the header the rest of the ecosystem includes). |

### 1.2 Per-file readiness ladder (recorded for every unit)

`unmapped` → `mapped but unwired` → `failing` → `passing with stated gaps` → `battle tested`.
A unit is promoted to **battle tested** only when every applicable row above has executed evidence,
recorded with command, platform, config, seed, skips, and result.

---

## 2. Baseline (measured, current tree)

From the executed assessment on this host (158 compiled `.c` units):

- **57** units have a dedicated `*_test.c` owner — all **75** wired owner tests currently **pass**.
- **56** units are covered only *indirectly* (a shared test `#include`s the header) — no dedicated proof.
- **45** units have **no owner test at all**.
- **8 of 9** Seams-to-Prove owner tests named by `test-preferences.md` **do not exist**.
- `ctest` registers **4 of 75**; `run_all_tests` is **graphvex-only**; there is **no coverage ratchet**.
- The umbrella build currently **fails on 5 non-vexspoke targets** (reactive refactor call sites).

**Total file units to own: 192** (158 `.c` + 34 header-only).

---

## 3. Harness and template

### 3.1 Decision: self-contained tests over a shared runner

The existing convention is a self-contained `main` with a local `CHECK` macro, linking `vexspoke`,
exiting nonzero on any failure (`struct/array_test.c` is the model). It has zero header coupling and
compiles under `-Wall -Wextra -Werror -UNDEBUG`.

**Proposal:** keep self-contained `main`, but extract the macro/boilerplate into one tiny
`tests/vexspoke/support/test_support.h` (`CHECK`, `CHECK_STREQ`, `RUN_CHILD` for isolated
death/fault tests, `WATCHDOG` helper). This removes ~190 copy-pasted blocks while keeping each test a
single translation unit. *(Open decision — see §8.)*

### 3.2 Death / fault isolation

The **Pointer Legitimacy** and **adversarial** rows require proving a rejection in an **isolated child
process** with a bounded timeout (so an unmapped-address dereference aborts the child, not the suite).
`transient_lifetime_test.c` already does this (`child correctly aborted with SIGABRT`); its
`fork`/`wait` pattern becomes the shared `RUN_CHILD` helper.

### 3.3 Sanitizers

Add two sanitizer build configurations (no preset exists today):

- **ASan + UBSan** for the **Resource and Lifetime**, **Boundary**, and **Overflow Guard** rows.
- **TSan** for the **Concurrent Substrate** rows (`atomic/*`, `thread/*`, `deferred/dispatch`,
  `reactive/*`, `io/ws_client`, `input/*`).

Each sanitizer test keeps an **external bounded watchdog** (the **Bounded Wait Law**); no unbounded wait,
no `UINT64_MAX`.

---

## 4. Wiring — the continuous process

This is the "continue process" the user asked for. All four are required; a passing suite that no
target runs is not a process.

1. **Register every owner test with `ctest`.** Replace today's four hand-listed names with a loop over
   the produced `*_test` targets, each with a bounded `TIMEOUT`.
2. **Add a `run_vexspoke_tests` aggregate target** (mirroring `diagnostic_smoke_tests` /
   `run_all_tests`) that depends on and executes the full vexspoke battery and fails on the first
   nonzero exit.
3. **Add a coverage ratchet** — a script that derives the unit list from the library's sources and
   **fails when any compiled unit lacks an owner test**, ending the silent drift in §2.
4. **Record the ledger** in `tests/test-preferences.md` as the vexspoke *Owner coverage* section,
   matching the hotcwap precedent (this document → that section on completion).

---

## 5. Work breakdown — waves (dependency-ordered)

Each wave = one cohesive, bisectable commit set growing the owner corpus and the gate together
(the **Cohesive Commits Law**). Wave 0 is a prerequisite.

| Wave | Directories | Units | Notes |
| :--- | :--- | :--- | :--- |
| **0 — unblock** | — | — | Fix the 5 reactive-refactor call sites so the umbrella builds (D1). No gate can be green until this lands. |
| **0.5 — enable** | — | — | Add `test_support.h`, sanitizer configs, ctest registration loop, `run_vexspoke_tests`, coverage ratchet. |
| **1 — memory core** | `nio`, `bit`, `c23`, `oop`, `util` | 1+1+6+2+3 = 13 | The arena/identity primitives every other unit depends on. Pointer Legitimacy + Lifetime rows are load-bearing here (`nio/mem` alone is only *indirectly* covered today). |
| **2 — scalars & math** | `primitive`, `math`, `lang(+subdirs)` | 16+4+16 = 36 | Determinism + float boundaries (`-0.0`, NaN, Inf). |
| **3 — containers** | `struct` | 14 | The Boundary Value matrix: empty/one/size/size+1/overflow per container. |
| **4 — relational & objects** | `relational`, `objects`, `reflection` | 8+8+5 = 21 | The "pointers that lie" surface: forged type/project id, sugar-tampered headers. |
| **5 — reactive & dispatch** | `reactive`, `deferred` | 8+1 = 9 | TSan; MPMC, mid-fire remove, cross-thread teardown. |
| **6 — search & algo** | `search`, `algo` | 3+7 = 10 | Property/metamorphic oracles; seeded determinism. |
| **7 — time & exception** | `time`, `exception` | 4+6 = 10 | Clock determinism seams; `Try*` value-or-error boundaries. |
| **8 — security & io** | `security`, `io` | 3+12 = 15 | Overflow guards (`Url_base64`, `Transient_alloc`), adversarial parsers, cache/clipboard lifetime. |
| **9 — net** | `net` | 8 | Offline transport failure codes; hostile JSON/URL; no live network in CI. |
| **10 — input & thread** | `input`, `thread`, `atomic` | 10+6+3 = 19 | TSan contention (MPMC ring, ticket spin, ABA tags); bounded watchdogs. |
| **11 — host-adjacent** | `system`, `cli`, `engine`, `spoke`, `audio`, `event`, `annotation` | 10+6+1+1+4+3+12 = 37 | Platform probes mocked; header-only annotation units prove via their nearest stable seam. |

*(Header-only units — 34 across `annotation`, `event`, `c23`, `reactive`, `net`, `io`, `system`,
`audio`, `objects`, `exception` — get an owner test that exercises the behavior the header emits,
through the nearest stable seam, per the **Per-File Battle Test Law**.)*

---

## 6. Special cases

- **Platform-excluded on macOS** (`audio_stub`, `audio_hal_stub`, `clipboard_stub`, `tls_curl`,
  `touchid.c`): the owner test must exist but is recorded as **explicitly unproved on macOS**, requiring
  a non-Apple host run before "battle tested" (the precedent set for hotcwap's window backends).
- **Interactive demos** (`touchid_demo`) are **not** tests; they must be removed from any test
  aggregate so an absent operator cannot masquerade as a red test.
- **`main/main.c`** is a guarded demo reference that does not exist on disk; not a file unit.

---

## 7. Sequencing, blockers, and commit discipline

- **Blocker B1:** the umbrella does not build (§2). Wave 0 is mandatory and upstream-first
  (**vexspoke → graphvex → … **): the darling/graphvex/main call sites adopt the reactive pointer API.
- **Blocker B2:** `detached`-style interactive tests must be excluded from the gate (§6).
- Commits are per-repo and cohesive: `tests/` commits land in the `tests` repo; any production fix
  lands in `vexspoke` **before** the `tests` commit that depends on it (upstream-first).
- **No Auto-Pushing Law** holds: nothing is pushed without an explicit instruction.

---

## 8. Decisions (locked)

1. **Harness:** **fully self-contained** owner tests — every test repeats its own `CHECK` macro and
   boilerplate. No shared `test_support.h`. (§3.1 resolved against the shared header.)
2. **Sanitizers:** **per-wave, always-on** — ASan + UBSan on every wave; TSan additionally on the
   race-bearing waves (`atomic`, `thread`, `reactive`, `deferred`, `io`).
3. **Header-only units:** **all 34 get their own owner test** (strict **Per-File Battle Test Law**).
4. **Start point:** **Wave 0 + Wave 1** (memory core).

---

## 9. Deliverable of this cycle

This plan artifact only. No source, test, or CMake file has been modified. On approval, execution
begins at Wave 0 and proceeds wave-by-wave, each wave leaving the umbrella building, `ctest` green,
and the coverage ratchet stricter than before.

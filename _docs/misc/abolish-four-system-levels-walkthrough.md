# Walkthrough — Four System Levels Law abolished (R ranks are the single order)

;;INTENTION("per the Living Preferences Law: same-cycle constitution + annotations + guidance, zero drift")

## What changed

**Constitution (`ecosystem/vexspoke/preferences.md`, uncommitted):**

- Law Index: deleted the *Four System Levels Law* row; renumbered old 26–45 → 25–44 (44 laws total).
- Tier 1 list: removed the law from the key-rules enumeration.
- Header template (*Living `;;OVERVIEW` & `;;DEFINITION` Blueprint Law*): deleted the mandatory `* LEVEL: L2 — Behavior (...)` line.
- Deleted the full `## 25. Four System Levels Law` section (diagram + 4 bullets); renumbered followers.
- `rg` residual: CLEAN.

**Source annotations (uncommitted, comment-line deletions only):**

- Deleted every `* LEVEL: L[1-4] ...` overview line (361 lines, 361 files):
  - `vexspoke`: 164 files (+ constitution = 165 changed)
  - `graphvex`: 85 files (includes `src/_old/` legacy tree)
  - `api-haven`: 21 files
  - `hotcwap`: 21 files
  - `darling-framework`: 70 files
- Sample result (`kernel.c`):
  ```c
   * CLASS: Kernel (kernel/kernel.c)
   * ============================================================================
  ```
- `rg -n 'LEVEL: L[1-4]|Four System Levels' ecosystem` → CLEAN.

**Workspace guidance (superbuild local-only, no commit needed):**

- `CONTRIBUTING.md`: Tier-1 key rules no longer list the abolished law.
- `_docs/misc/per-repo-preferences-overhaul-plan.md`: two references reworded to the *Vertical Integration Law*.
- `_docs/transition/session/02_Reading_Any_File.md`: anatomy no longer lists `LEVEL:`.
- Deleted `_docs/transition/session/03_The_Four_Levels.md` (historical lesson for the abolished law).
- `_docs/_thoughts/darling-framework/layout-panels.md`: stale `LEVEL: L2 (Rule 23)` + numeric citations rewritten Title-only.
- Plan artifact: `_docs/misc/abolish-four-system-levels-plan.md` (this walkthrough's sibling).

## Validation

- `cmake --build build --target vexspoke graphvex hotcwap api_haven darling -j4` → **all green** (`-Wall -Wextra -Werror` clean on library targets).
- Full `cmake --build build -j4` → fails ONLY in `tests/darling/scroll_scene_cull_test.c` (`-Wunused-variable` / `-Wunused-parameter`, 5 errors). **Pre-existing, untouched by this change** (file mtime predates the sweep; sweep touched only `ecosystem/*.[chm]` comment lines + docs). Left for its owner.
- No `->` introduced (deletions only); no logic, no headers, no include allowlist touched — the *Vertical Integration Law* `R1 > R2 > R3 > R4 > R5` allowlist is byte-identical.

## Commit status (deliberately uncommitted)

NOT committed, NOT pushed — on purpose:

- Pre-existing unrelated dirt exists in `hotcwap` (`M hot/manifest.c`, `?? hot/ledger.c/h`), `graphvex` (`M src/_old/raster/raster_graphics.c` + prior work), `api-haven` (`M CMakeLists.txt`), `darling-framework` (`M darling-framework-preferences.md`), `sesh` (`M CMakeLists.txt`). Auto-committing would mix concerns against the *Cohesive Commits Law*.
- Per the *No Auto-Pushing Law*, no push was run and none will be without an explicit order.

**Suggested cohesive commits (upstream-first, user to run):**

1. `ecosystem/vexspoke`: constitution abolition (+ its 164 annotation deletions may ride along or split as `preferences:` + `overview:` — your call).
2. `ecosystem/graphvex` + `ecosystem/api-haven` (R3, either order).
3. `ecosystem/hotcwap` (R1 — triage against the in-progress ledger work first; `hot/manifest.c` carries both).
4. `ecosystem/darling-framework` (R4 — triage against the preferences dirt first).

Say the word and I will stage per-repo, show `git diff --stat` per repo for approval, and commit locally (never push).

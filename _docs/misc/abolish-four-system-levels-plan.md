# Abolition Plan — Four System Levels Law (L1–L4)

;;INTENTION("per the Living Preferences Law + the Vertical Integration Law: R1–R5 is the single order, L1–L4 edit-risk is redundant")

## Background

The *Four System Levels Law* requires every file to carry exactly one
`LEVEL: L1–L4` edit-risk tag (metadata / behavior / module / self-management)
and teaches L as "how safe is it to edit this file?" versus R as
"who boots/supervises whom at runtime?".

Rationale for abolition (user directive):

- Redundant with the *Vertical Integration Law* single order
  (`R1 Host > R2 Behavior > R3 Drivers > R4 Interfaces > R5 Interactables`).
- Behavior is already implemented through `extern` functions and opaque
  shapes + fn-tables; no separate L validation is needed.
- `R2–R5` coexist fine; supervision flows top-to-bottom
  (`supervises ▼` runtime, `borrows shape ▲` compile-time). The L ladder
  (upper rests on lower, never reverse) inverts the working mental model
  and duplicates the R allowlist.
- Stale numeric citations already in the wild (`Rule 28` inside `LEVEL:`
  lines) prove the second axis drifts per the *Law Identity Doctrine*.

Single order after abolition: R only. No `LEVEL:` line in any `;;OVERVIEW`.

## Proposed changes (grouped by repo, upstream-first)

### 1. `vexspoke` (constitution + template) — FIRST

File: `ecosystem/vexspoke/preferences.md`

- Law Index table: delete row
  `| 25 | Four System Levels Law (L1–L4 — File Stability, NOT Runtime Rank R1–R5) |`,
  renumber old 26–45 down to 25–44.
- Separation of Concerns Tier 1 list: remove
  `the Four System Levels Law (L1–L4, distinct from R1–R5 Supervisor Order),`.
- Required header template (`Living ;;OVERVIEW & ;;DEFINITION Blueprint Law`):
  delete line
  `* LEVEL: L2 — Behavior (Four System Levels Law: ...)`.
- Delete section `## 25. Four System Levels Law ...` in full (diagram +
  four bullets), renumber old `## 26.` through end down by one.
- Verify zero remaining `Four System Levels|L1–L4|LEVEL: L` hits in the file.

Commit (in `ecosystem/vexspoke`): constitution-only, e.g.
`preferences: abolish Four System Levels Law, R ranks are the single order`.

### 2. Workspace guidance (local-only, no push)

- `CONTRIBUTING.md`: remove `the Four System Levels Law,` from Tier-1 key rules.
- `_docs/misc/per-repo-preferences-overhaul-plan.md`: lines 116, 191 reference
  the abolished law — reword to the *Vertical Integration Law* or drop.
- `_docs/transition/session/03_The_Four_Levels.md`: historical lesson for the
  abolished law — delete file or prepend `> ABOLISHED` banner. Recommend delete
  (local notes only, per README `_docs/` is never pushed).
- `_docs/transition/session/02_Reading_Any_File.md`: step 2 `LEVEL: L1–L4`
  — reword to `CLASS:`-only anatomy.
- `_docs/hotcwap/hotcwap.md`, `_docs/misc/*`: leave unless `rg` hits remain.

No commit (superbuild root has no remote by design).

### 3. Source `;;OVERVIEW` annotations (per-repo, upstream-first)

Delete every line matching `^\s*\*\s*LEVEL: L[1-4]\b.*$` (the whole line only,
no code logic touched). Counts from `rg -l 'LEVEL: L'`:

- `ecosystem/vexspoke`: ~165 files
- `ecosystem/darling-framework`: ~70 files
- `ecosystem/graphvex`: ~26 files
- `ecosystem/hotcwap`: ~21 files (note: pre-existing unrelated
  `M hot/manifest.c`, `?? hot/ledger.c/h` stay untouched — separate concern)
- `ecosystem/api-haven`: ~21 files
- `language`, `darkbase`, `sesh`, `samplerate`, `projects/*`: zero hits

Example (`ecosystem/hotcwap/kernel/kernel.c`):

```c
 * CLASS: Kernel (kernel/kernel.c)
-* LEVEL: L4 — Self-Management (R1 Host; the Vertical Integration Law vs the Four System Levels Law: L = edit-risk, R = supervision)
 * ============================================================================
```

becomes:

```c
 * CLASS: Kernel (kernel/kernel.c)
 * ============================================================================
```

Each repo gets its own cohesive local commit (no push per the
*No Auto-Pushing Law*), in dependency order:
`vexspoke` → `graphvex`/`api-haven` → `hotcwap` → `darling-framework`.
Verify `rg -n 'LEVEL: L[1-4]|Four System Levels' <repo>` returns zero
(excluding this plan file) before committing each repo.

## Open questions / trade-offs

1. **Replacement header?** Plan proposes no replacement — `CLASS:` +
   `STRUCT FIELDS` + `FUNCTION REGISTRY` already carry the needed signal,
   and R-rank is per-repo (allowlist), not per-file. Alternative rejected:
   `RANK: R1` per file would reintroduce the exact L-vs-R confusion
   (`Never write LEVEL: R1`).
2. **History lessons?** `_docs/transition/session/03_*` documents the
   abolished law as invented history. Deleting rewrites teaching history;
   keeping with an ABOLISHED banner preserves it. Recommend delete since
   `_docs/` is local-only scratch, but either satisfies zero-drift.
3. **Renumber churn.** Ordinals 26–45 all shift down by one. This is intended
   and legal per the *Law Identity Doctrine* (ordinals are positional, Titles
   are identity) and the *Living Preferences Law*. Citations by Title do not
   break; any stale numeric citation found is fixed in-cycle per Title-Identity
   Enforcement.
4. **Scope risk.** ~303 files is sweeping but mechanical (comment-line deletion
   only). Risk is near-zero for compilation; risk is commit hygiene. Mitigation:
   per-repo commits, `git status` check for unrelated work before each commit
   (notably `hotcwap` ledger work stays out).

## Verification plan

- `rg -n 'Four System Levels|LEVEL: L[1-4]|L1–L4' ecosystem/vexspoke/preferences.md CONTRIBUTING.md ecosystem/<each-repo>` → zero (outside this plan).
- `git -C ecosystem/<repo> diff --stat` reviewed; `git status --porcelain` shows
  only intended `M` entries (no ledger/manifest cross-contamination).
- Comment-only change: no logic edit, so `->` / dest-last / two-layer checks
  are vacuous; still run per-repo build if configured (`cmake --build` with
  `-Wall -Wextra -Werror`) and report results in the walkthrough.
- Final walkthrough artifact summarizing edits, validations, test results.
- No `git push` anywhere (superbuild has no remote; sub-repos push only on
  explicit user order).

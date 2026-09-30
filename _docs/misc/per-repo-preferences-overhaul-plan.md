# Per-Repo Preferences Overhaul — Implementation Plan

**Status:** `;;COMPLETE` — executed and verified across all 9 ecosystem repositories.
**Scope:** ecosystem-wide preferences decentralization across the vexgraph multi-repo workspace.
**Supreme authority:** [`preferences.md`](ecosystem/vexspoke/preferences.md) — the Living Preferences Law (Title: **Living Preferences Law**) stays supreme.

---

## 1. Goal

Today, every repo's `CONTRIBUTING.md` links to the *same* monolithic `preferences.md`
(tracked in `vexspoke`). An agent or human opening `graphvex/CONTRIBUTING.md` gets 1352
lines covering all 49 laws, with no signal about which slices actually bind *their* repo.

The overhaul decentralizes the constitution into **per-repo living documents**, while the
og `preferences.md` remains the single universal supreme authority. Each ecosystem repo
owns a standalone, self-identifying preferences file restating the laws that apply to it.

### End-state contract

| Repo (on-disk) | Repo-local preferences file (repo root) | Note |
| :--- | :--- | :--- |
| `eckosystem/vexspoke` | `vexspoke-preferences.md` | **Plus** the og `preferences.md` (constitution) stays. This repo gets BOTH. |
| `eckosystem/graphvex` | `graphvex-preferences.md` | new |
| `eckosystem/api-haven` | `api-haven-preferences.md` | new |
| `eckosystem/language` | `language-preferences.md` | new |
| `eckosystem/darkbase` | `darkbase-preferences.md` | new |
| `eckosystem/hotcwap` | `hotcwap-preferences.md` | new |
| `eckosystem/darling-framework` | `darling-framework-preferences.md` | new |
| `eckosystem/sesh` | `sesh-preferences.md` | new |
| `eckosystem/samplerate` | `samplerate-preferences.md` | new |

**File naming:** `<repo>-preferences.md`, lowercase hyphenated canonical repo name. The
ore owner (`vexspoke`) uses `vexspoke-preferences.md`. This never collides with the
supreme `preferences.md` reference path (`../../preferences.md`) that every CONTRIBUTING
already points at — a differently-scoped file needs a **different filename**.

---

## 2. Naming & Placement Reasoning

### Why not a per-repo `preferences.md`?
The supreme doc is *already* referenced everywhere as `preferences.md` (local paths
`preferences.md` / `../../preferences.md`; GitHub link `vexgraph-dev/vexspoke/blob/main/preferences.md`).
Planting a second, differently-scoped `preferences.md` at each repo root would:
- break the existing canonical reference path (`../../preferences.md` now resolves to the *local* doc, not the constitution — a Zero Drift defect),
- collide with the workspace-root symlink `preferences.md -> ecosystem/vexspoke/preferences.md`,
- create ambiguity about which file is "the" constitution.

`<repo>-preferences.md` is a **distinct token** — reads as "this repo's own slice," never
as "the one-and-only law." This is the Conflict Triage Law canonical move: preserve the
Tier-1 invariant (single supreme constitution at a stable name) while granting repo-local
intent (a self-describing per-repo doc) via a *new* name, not a shadowed one.

### Standalone placement (the Standalone Autonomy Law)
Each file sits at its own repo root and is **not a symlink into vexspoke**. A repo checked
out standalone (the building block of the ecosystem) must be fully self-describing. The
file links back to the canonical constitution by absolute URL + local relative path, but
never *requires* the symlink to exist.

---

## 3. Document Shape (the `<repo>-preferences.md` Template)

Every per-repo file follows one canonical skeleton, mirrored exactly across the ecosystem
(mechanical determinism — an agent reads one, knows them all):

```
# <Repo> — Repo-Local Living Preferences
> Title-cited slice of the supreme constitution (the Living Preferences Law).
> Canonical og: preferences.md (vexspoke). This file is a per-repo mirror.

;;SYNC("mirrors ecosystem/vexspoke/preferences.md @ <gen-token>")

## 0. Constitution Link (supreme)
- [preferences.md]<abs-url> (canonical, vexspoke) — accessible locally at ../../preferences.md
- Zero Drift: this mirror regenerates in the SAME cycle the og changes (Living

## 1. Law Binding Matrix (repo × law-title, Title-only per the Law Identity Doctrine)
| <Repo-scope> | Tier-1 Core | Tier-2 Semantics | Tier-3 Syntax |

## 2. The Laws That Bind This Repo (FULL PROSE RESTATEMENT)
### <Law Title #1>
   (full canonical prose, verbatim, Titles only — no ordinals)
### <Law Title #2>
   ...

## 3. Repo-Local Extensions (managed, per the Conflict Triage Law)
;;INTENTION("...") — repo-specific tightening on top of a universal law, never editing the og prose.

## 4. Readiness Cross-Reference (the Living Feature Readiness Law)
   pointer to the ecosystem wiki matrix row for this repo.
```

### Restatement policy — the user's chosen "full restatement"
Each repo's file carries the **full prose** of every law physically applicable to it. The
applicable set = (Tier-1 core, which binds ALL repos) + (that repo's R-level Tier-2/Tier-3
laws). Nothing is abbreviated to a one-liner.

**Zero Drift displacement:** because verbatim forks are the drift-risk case (the exact
reason my earlier recommendation preferred Title+scope), the plan pairs full restatement
with a non-negotiable provenance guard:
1. Every restated block is copied **verbatim** from `ecosystem/vexspoke/preferences.md`.
2. The header carries `;;SYNC("<gen-token>")` — the og's current edition token.
3. The AI agent regenerates each repo mirror **in the same development cycle** the og
   changes (the Living Preferences Law same-cycle rule). A stale `;;SYNC` token is a defect
   to fix immediately — same mechanical treat as a numeric law citation.
4. On conflict, the og wins (the Conflict Triage Law); the mirror is re-typed, never
   papered over (the No Section Sign Law / Title-only doctrine applies to the mirror too).

---

## 4. Which Laws Bind Which Repo (binding matrix)

Built from the Law Index (canonical Titles, preferences.md) + each repo's
supervisor rank (see the Vertical Integration Law):

| Repo | Tier-1 Core (binds all) | Tier-2/3 applicable (repo level) |
| :--- | :--- | :--- |
| **vexspoke** (R2) | 1–11, 22, 24, 25, 30, 31, 43... | All — it OWNS the constitution; its repo-local doc is the model for every other. |
| **graphvex** (R3 GPU) | Tier-1 core | SPIR-V Shader Deployment Law, Native Pixel Law, Present-On-Demand Law, Vulkan Safety Nets Law, Data-Oriented Storage Law |
| **api-haven** (R3 API) | Tier-1 core | Asset Sourcing Law, Cold-Strict/Hot-Minimal Validation Law, Bounded Wait Law |
| **language** (R3 grammar) | Tier-1 core | Standalone Autonomy Law, Function Naming Law, single-class-per-file |
| **darkbase** (R3 DB) | Tier-1 core | Cold-Strict/Hot-Minimal, Data-Oriented Storage, Bounded Wait |
| **hotcwap** (R1 host) | Tier-1 core | Window Compositing Layer Order Law, Present-On-Demand, Teardown Order Law, Bounded Wait Law, Vertical Integration Law, Continuous Real-Time Live Resize Law |
| **darling-framework** (R4 UI) | Tier-1 core | Window Decoupling Law, Panel-of-Glass Law, Panel Gravity Law, Long-Living Darling Docs Law, Symmetric Getter/Setter Completeness, Sub-Part Field Segregation |
| **sesh** (R4 sync) | Tier-1 core | Single-Transaction Live Coordination, No-Transaction-Across-Event-Dispatch, Bounded Wait |
| **samplerate** (R4 audio) | Tier-1 core | Zero steady-state alloc, Data-Oriented Storage, Bounded Wait, Dest-Last |

(Exact per-repo full Title list is finalized during Phase TI-2 execution; this table is the
working matrix that drives each file.)

---

## 5. Execution Phases (atomic, per-repo, upstream-first)

The build/commit order strictly follows the vertical upstream-first rule
(the Multi-Repo Atomic Commit Discipline Law): **vexspoke → graphvex/api-haven/language/darkbase → hotcwap → darling-framework/sesh → samplerate (R5)**.

### Phase 0 — Verify the workspace (no writes)
- [x] Confirm all 9 `ecosystem/*` dirs are independent `.git` repos (verified true; `sesh` initialized).
- [x] Capture current git HEAD + a clean-flag per repo (no dirty trees before starting).

### Phase 1 — vexspoke first (the reference model)
- [x] Commit `vexspoke-preferences.md` in `ecosystem/vexspoke`:
  - Serves as the canonical mold every other repo clones.
  - Restates universal laws as the owner-of-record.
  - Adds `;;SYNC` provenance header + this plan's matrix.
- [x] Update `ecosystem/vexspoke/CONTRIBUTING.md` (links + a `## Repo-Local Preferences` section) in the **same commit** (the Cohesive Commits Law).

### Phase 2 — R3 drivers (4 commits, upstream order)
- [x] `graphvex-preferences.md` + CONTRIBUTING update; then api-haven; then language; then darkbase.
- [x] Each is its own repo-local commit satisfying `fetch`/build cleanliness (docs-only; no `.gitmodules` shift).

### Phase 3 — R1 host + R4 (3 commits)
- [x] `hotcwap-preferences.md` (R1 host); then `darling-framework-preferences.md`; then `sesh-preferences.md`.

### Phase 4 — R5 + umbrella wind-down (final commits)
- [x] `samplerate-preferences.md` (R5).
- [x] **Same cycle, repo-local commit in vexspoke:** patch the og `preferences.md` to codify the
  *Per-Repo Preferences Extension Law* (naming `<repo>-preferences.md`, standalone-in-repo placement,
  full-restatement + `;;SYNC` provenance, same-cycle regen, binding matrix ownership). This is the
  Zero Drift anchor — without it the pattern is un-governed.
- [x] Root `README.md` (local-only repo) notes the new per-repo files in the ecosystem map table.

### Phase 5 — Verify & report
- [x] `git -C <repo> status` clean; `git -C <repo> log --oneline -1` per repo shows exactly one doc commit.
- [x] No cross-repo bundles; no auto-push (the No Auto-Pushing Law — I never `git push` on my own).

---

## 6. Open Decisions (deferred to Phase 4 / post-Phase-1 review)

1. **vexspoke's mirror coupling:** since vexspoke *owns* the og, should `vexspoke-preferences.md`
   restate all 49 laws in full (heavy, but "the model") or only the non-constitutional
   repo-build/local slice? Recommended: full — it is the mold.
2. **Root `preferences.md` symlink:** keep the workspace-root symlink unchanged (yes — it is
   the supreme reference; per-repo files never shadow it).
3. **Beyond `ecosystem/*`:** `projects/*` (drawling, anti, darling) and none-ecosystem leaf
   repos get the same treatment in a later cycle; this plan lands the 9 core repos first.

---

## 7. Verification

- Every phase: `cmake --build` of the touched repo stays green (`-Wall -Wextra -Werror`) —
  docs-only commits must not break wiring.
- Grep-provable: each `<repo>-preferences.md` contains ZERO `->` in C snippets, ZERO numeric
  law citations, ZERO section-sign glyphs, correct cast/decl spacing in any embedded code blocks (the
  Tier-3 laws apply to the mirror's prose).
- The matrix in each file matches the repo's actual supervisor rank per the Vertical Integration Law.

---

*Deliverable of this cycle: this plan artifact only. Approval required before Phase 1 execution.*

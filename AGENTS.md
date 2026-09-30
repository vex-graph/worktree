# AGENTS.md — read this first

Entry point for **any** agent (or human) working in this workspace.
It is the root of the `vex-graph/worktree` repository.

> If you only read one thing: **this root repo is scaffolding + docs only.**
> The actual source lives in nested, independent git checkouts that are
> `.gitignore`d here. Commit and push *in those checkouts*, not here. See
> [`docs/COMMITTING.md`](docs/COMMITTING.md).

---

## 1. What this is

`~/vexgraph` is the **umbrella superbuild workspace** for the vexgraph
ecosystem. It contains:

- the top-level CMake superbuild (`CMakeLists.txt`) and the `_main/` demo harness,
- shared tooling (`tools/`),
- personal notes and per-layer explainers (`_docs/`),
- and — under `ecosystem/`, `repos/`, `projects/`, `tests/`, `trash/` —
  **separate git repositories**, each with its own GitHub remote.

This root repo (`vex-graph/worktree`) tracks the first group and documents the
whole thing. It does **not** track the nested repositories.

## 2. Read before doing anything

| File | Why |
|---|---|
| `preferences.md` (symlink → `ecosystem/vexspoke/preferences.md`) | **The constitution.** Read it in full. |
| `<repo>-preferences.md` (per-repo root) | Repo-local laws. |
| `README.md` | The workspace map + layer order. |
| `docs/WORKTREE.md` | Topology: what every path is, and its remote. |
| `docs/COMMITTING.md` | Git workflow, commit granularity, the push law. |
| `_docs/how-it-works/*` | Per-layer explainers (vexspoke, hotcwap, darling, …). |

**Two laws you must not break:**

- **The Git Workflow Law** — *never push without an explicit, one-off order.*
  See `docs/COMMITTING.md`.
- **The Law Identity Doctrine** — cite every law by its canonical **Title**,
  never by number.

Scope discipline: cosmetic edits stay cosmetic. Functional identifiers (header
guards, `@…_MAGIC`, `anti://` URIs, `~/anti` paths, `ANTI_*` env vars) change
only via a deliberate migration — never a drive-by rename.

## 3. Lesson from the last migration

The workspace root was moved from `~/CLionProjects/vexgraph` to `~/vexgraph`,
and two directory renames were applied in the process:

- `main/` → `_main/`
- `ecosystem_repos/` → `repos/`

That rename was applied to **file contents** too (comments, CMake paths, test
files) — which is why many files "differ" from the old tree by name alone.
When you see `_main` where an old note says `main`, that is the rename, not a
bug. See `docs/WORKTREE.md` §"Known drift".

## 4. Build

The superbuild is driven from the root `CMakeLists.txt` (Apple / Cocoa +
Vulkan/WGPU). Tooling lives in `tools/` (`build_stripped.sh`,
`app_build_native.sh`, `run_debug.sh`, `linter.py`, …). `_main/` holds the
umbrella demo/probe targets (`test_suite`, `gallery`, `image_load.m`, …).

Generated build trees (`cmake-build-*/`, `build/`) are git-ignored.

## 5. Quick map

```
~/vexgraph
├── CMakeLists.txt        # umbrella superbuild
├── AGENTS.md             # ← you are here
├── README.md             # workspace map (layer order)
├── preferences.md        # symlink → the constitution
├── _main/                # umbrella demo/probe harness
├── _docs/                # notes, plans, walkthroughs, how-it-works/
├── tools/                # build + lint scripts
├── resources/            # image/assets
├── docs/                 # agent docs (this repo)
├── ecosystem/  [ignored] # R1–R5 library checkouts
├── repos/      [ignored] # meta repos (.ecosystem, .github, .vexgraph-dev)
├── projects/   [ignored] # R5 app repos (anti, darling, drawling, …)
├── tests/      [ignored] # shared test suite repo
└── trash/      [ignored] # retired repos (graphvex, darling-framework)
```

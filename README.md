# vexgraph — the worktree

> The umbrella workspace for the **vexgraph** ecosystem, and the root of the
> public [`vex-graph/worktree`](https://github.com/vex-graph/worktree) repo.
>
> This repo tracks **only** the scaffolding and documentation. The actual
> source lives in nested, **independent** checkouts — `ecosystem/`, `repos/`,
> `projects/`, `tests/`, `_trash/` — which are `.gitignore`d here. Commit and
> push *inside each of those*, never here.

## Build with `b`

`b` is our own build system: a single C23 program, [`tools/b.c`](tools/b.c).
**Not CMake. Not Ninja.** It holds the target graph in C, asks the compiler what
is stale (`-MMD` depfiles), reuses a content-addressed object cache, and drives
`clang` / `ar` / `ld` directly.

```sh
./tools/b targets           # list targets
./tools/b build             # build everything
./tools/b build vexspoke    # build one target (and its deps)
./tools/b test [substr]     # build + run every *_test
./tools/b run <name>        # run a target (an app launches as a real .app)
./tools/b watch             # rebuild on change (hotload loop)
./tools/b cc                # write b.json (the clangd database)
./tools/b doctor            # resolved toolchain + flags
./tools/b clean             # remove build output
```

Flags: `--release`, `-j N`, `-v`.

### Add an app, get a `.app`

Drop any `_main/<name>.c` that has a `main()`. `b` auto-discovers it, links the
base libraries, wraps it in an ad-hoc-codesigned `<name>.app`, and launches it:

```sh
# write _main/scroll_probe.c ...
./tools/b run scroll_probe      # builds → bundles → opens the .app
```

Any `main`-less sibling `.c` in `_main/` is compiled into every app (shared
scenes / helpers). All binaries, objects and caches live **outside** the tree,
under `~/Library/Application Support/vexgraph/b/` (override with `$B_HOME`); the
only build artefact left in the tree is the git-ignored `b.json`.

## Workspace map

Each nested directory is its own repository with its own remote. Listed in layer
order (R1 → R5).

| Path | What it is | Remote |
|---|---|---|
| `ecosystem/hotcwap` | **R1** kernel host, hotloading, windows | `vexgraph-ecosystem/hotcwap` |
| `ecosystem/vexspoke` | **R2** behavior core (relational C23 runtime) — holds `preferences.md` | `vexgraph-ecosystem/vexspoke` |
| `ecosystem/graphvex` | **R3** GPU driver — *deleted, restarting from scratch* | `vexgraph-ecosystem/graphvex` |
| `ecosystem/api-haven` | **R3** API/connector surface (MCP, AI, DB, asset) | `vexgraph-ecosystem/api-haven` |
| `ecosystem/language` | **R3** language grammars *(scaffold)* | `vexgraph-ecosystem/language` |
| `ecosystem/darkbase` | **R3** database driver *(scaffold)* | `vexgraph-ecosystem/darkbase` |
| `ecosystem/sesh` | **R4** session sync / relay | `vexgraph-ecosystem/sesh` |
| `ecosystem/samplerate` | **R4** audio engine *(scaffold)* | `vexgraph-ecosystem/samplerate` |
| `projects/anti` | **R5** 3D game engine *(scaffold)* | `vexgraph-ecosystem/anti` |
| `projects/drawling` | **R5** drawing studio *(scaffold)* | `vexgraph-ecosystem/drawling` |
| `projects/semicolon` | **R5** mini IDE *(scaffold)* | `vexgraph-ecosystem/semicolon` |
| `projects/impedance` | audio/UI bridge | `vexgraph-ecosystem/impedance` |
| `projects/darling` | UI toolkit *(sources pending)* | `vexgraph-ecosystem/darling` |
| `tests` | the shared test suite | `vexgraph-ecosystem/tests` |
| `repos/.ecosystem` | ecosystem meta / orchestration | `vexgraph-ecosystem/ecosystem.wiki` |
| `repos/.github` | org profile & workflow templates | `vexgraph-ecosystem/.github` |
| `repos/.vexgraph-dev` | developer portal & tooling | `vexgraph-dev/vexgraph-dev` |
| `_trash/` | retired checkouts (graphvex, darling-framework) | — |
| `_notes/` | notes, plans, walkthroughs, `how-it-works/` | **local** |
| `_main/` | umbrella apps + shared scenes (built by `b`) | **local** |
| `tools/` | build system (`b`, `b.c`) and scripts | **local** |
| `docs/` | agent docs (`WORKTREE.md`, `COMMITTING.md`) | **local** |
| `resources/` | private assets — **git-ignored, never published** | **local** |

## Read before doing anything

The workspace is governed by a constitution:

- **`preferences.md`** (→ `ecosystem/vexspoke/preferences.md`) — the constitution. Read it in full.
- **`<repo>-preferences.md`** (per-repo root) — repo-local laws (the Per-Repo Preferences Extension Law).
- **`docs/WORKTREE.md`** — topology and known drift.
- **`docs/COMMITTING.md`** — git workflow, commit granularity, the push law.

Cite every law by its canonical **Title**, never by number (the Law Identity Doctrine).
Never push without an explicit, one-off order (the **Git Workflow Law**).

Scope discipline — cosmetic edits stay cosmetic; functional identifiers (header
guards, `@…_MAGIC`, `anti://` URIs, `~/anti` paths, `ANTI_*` env vars) change
only via deliberate migration, never a drive-by rename.

## Public-repo hygiene

This repository is public. `resources/` (personal assets) is git-ignored, and
the nested checkouts are never duplicated here. Before pushing, confirm nothing
private slipped into `_notes/`, `_main/`, `docs/`, or `tools/`.

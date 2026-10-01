# vexgraph — the worktree

A **thin wrapper repo**. It holds the many independent vexgraph repositories
side by side and nothing else — like a folder of small repos, not a monorepo.
Each nested directory is its own checkout with its own remote: commit and push
*inside each of those*, never here. Everything private (notes, the local app
harness, assets) is git-ignored, so this repo stays tiny.

## Build: `b`

The workspace build system is `b` — a single C23 program, `tools/b.c`.
**Not CMake. Not Ninja.**

```sh
./tools/b build            # build everything (libs, tests, apps)
./tools/b test [substr]    # build + run every *_test
./tools/b run <name>       # run a target (an app launches as a real .app)
./tools/b targets | watch | cc | doctor | clean
```

Drop a `_main/<name>.c` containing a `main()` and `./tools/b run <name>` builds,
bundles and launches it as an ad-hoc-codesigned `.app`. All build state lives
*outside* the tree (`~/Library/Application Support/vexgraph/b/`, override
`$B_HOME`); the only artefact left here is the git-ignored `b.json`.

## The repositories

| Path | Layer | Remote |
|---|---|---|
| `ecosystem/hotcwap` | R1 kernel host · windows | `vexgraph-ecosystem/hotcwap` |
| `ecosystem/vexspoke` | R2 behavior core (**the constitution**) | `vexgraph-ecosystem/vexspoke` |
| `ecosystem/graphvex` | R3 GPU driver (rect-first, no swapchain) | `vexgraph-ecosystem/graphvex` |
| `ecosystem/api-haven` | R3 API / connectors | `vexgraph-ecosystem/api-haven` |
| `ecosystem/language`, `ecosystem/darkbase` | R3 *(scaffolds)* | `vexgraph-ecosystem/*` |
| `ecosystem/sesh`, `ecosystem/samplerate` | R4 | `vexgraph-ecosystem/*` |
| `projects/{anti,drawling,semicolon,darling,impedance}` | R5 | `vexgraph-ecosystem/*` |
| `tests` | the shared test suite | `vexgraph-ecosystem/tests` |
| `repos/.ecosystem`, `repos/.github`, `repos/.vexgraph-dev` | meta | `vexgraph-*/*` |

Local-only (git-ignored, never published): `_trash/` retired checkouts ·
`_notes/` notes · `_main/` apps · `tools/` the `b` build system · `resources/`
assets.

## Rules

The workspace is governed by a constitution: **`preferences.md`** — read it in
full; each repo adds its own `<repo>-preferences.md`. Locally it is a symlink
(`→ ecosystem/vexspoke/preferences.md`); **on the web** (the symlink won't render
on GitHub) read it here:

**https://github.com/vexgraph-ecosystem/vexspoke/blob/main/preferences.md**

Cite every law by its canonical **Title**, never by
number (the Law Identity Doctrine). **Never push without an explicit, one-off
order** (the Git Workflow Law).

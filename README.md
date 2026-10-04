# vexgraph — the worktree

A **thin wrapper repo**. It holds the many independent vexgraph repositories
side by side and nothing else — like a folder of small repos, not a monorepo.
Each nested directory is its own checkout with its own remote: commit and push
*inside each of those*, never here. Everything private (notes, the local app
harness, assets) is git-ignored, so this repo stays tiny.

## Build: `b`

The build system lives in the independent [`vex-graph/b`](https://github.com/vex-graph/b)
checkout at `b/`. Its C23 language CLI owns `run`, `build` and the planned `export`
surface. `b/workspace.c` preserves the existing framework graph, shaders, cache
and tests. `tools/b` is only a forwarding compatibility launcher.

```sh
./tools/b build            # build everything (libs, tests, apps)
./tools/b test [substr]    # build + run every *_test
./tools/b run <name>       # run a target (an app launches as a real .app)
./tools/b targets | watch | cc | doctor | clean
```

Drop a `_main/<name>.c` containing a `main()` and `./tools/b run <name>` builds,
bundles and launches it as an ad-hoc-codesigned `.app`. All build state lives
*outside* the tree (`~/Library/Application Support/vexgraph/b/`, override
`$B_HOME`); compilation databases in `b/` are ignored.

For standalone projects, add the `b/` checkout to `PATH`, or invoke `./b/b`:

```sh
./b/b run exec ./hello.c
./b/b java ./Hello.java
./b/b build c ./native-project
./b/b build java ./java-project
```

See `b/README.md` for the implemented command contract and packaging roadmap.
`run instance` runs directly through a runtime or an existing executable;
`run exec` builds the source artifact before launching it. Generic export
packaging is not implemented yet. The former CMake adapter is no longer the
workspace entry point.

## The repositories

| Path | Layer | Remote |
|---|---|---|
| `b` | standalone build-system CLI + workspace engine | `vex-graph/b` |
| `ecosystem/hotcwap` | R1 kernel host · windows | `vexgraph-ecosystem/hotcwap` |
| `ecosystem/vexspoke` | R2 behavior core (**the constitution**) | `vexgraph-ecosystem/vexspoke` |
| `ecosystem/drivers/graphvex` | R3 GPU driver (rect-first, no swapchain) | `vexgraph-ecosystem/graphvex` |
| `ecosystem/drivers/api-haven` | R3 API / connectors | `vexgraph-ecosystem/api-haven` |
| `ecosystem/drivers/language`, `ecosystem/drivers/darkbase` | R3 *(scaffolds)* | `vexgraph-ecosystem/*` |
| `ecosystem/interface/sesh`, `ecosystem/drivers/samplerate` | R4 | `vexgraph-ecosystem/*` |
| `projects/{anti,drawling,semicolon,darling,impedance}` | R5 | `vexgraph-ecosystem/*` |
| `tests` | the shared test suite | `vexgraph-ecosystem/tests` |
| `repos/.ecosystem`, `repos/.github`, `repos/.vexgraph-dev` | meta | `vexgraph-*/*` |

Local-only (git-ignored, never published): `_trash/` retired checkouts ·
`_notes/` notes · `_main/` apps · `tools/` workspace helpers · `resources/`
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

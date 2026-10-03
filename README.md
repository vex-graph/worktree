# vexgraph — the worktree

A **thin wrapper repo**. It holds the many independent vexgraph repositories
side by side and nothing else — like a folder of small repos, not a monorepo.
Each nested directory is its own checkout with its own remote: commit and push
*inside each of those*, never here. Everything private (notes, the local app
harness, assets) is git-ignored, so this repo stays tiny.

## Build: `b`

The workspace build system is `b` — a single C23 program, `tools/b.c`.
`b` remains the canonical framework build. A thin **CMake adapter** provides
CLion indexing, native test Run/Debug targets, and CTest; it reads build metadata
from `b` instead of maintaining a second framework graph.

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

## CLion: click a test and run it

1. Open **this workspace root** (`vexgraph/`) as a CMake project, not an
   individual test file or the independent `tests/` checkout.
2. Reload CMake. Use CLion's bundled CMake and Ninja (or Unix Makefiles).
3. Select a test such as **`ui_anchor_pivot_pixels_test`** in the Run/Debug
   configuration dropdown and click Run or Debug. Remove the old single-file
   `cc <file.c>` configuration: it has no framework includes or libraries.

CMake compiles the actual test sources with include paths, definitions and
archive ordering exported by `./tools/b ide`. Framework libraries, hotload
modules and generated shaders are built by `b`, without running tests or apps.
IDE build state is isolated under `cmake-build-*/b-state/`; terminal `b` builds
remain separate. Test executables live in the CMake build directory's `bin/`.

```sh
cmake -S . -B cmake-build-debug -G 'Unix Makefiles'
cmake --build cmake-build-debug --target console_test
ctest --test-dir cmake-build-debug -R '^console_test$' --output-on-failure
```

CTest registers automated tests with timeouts and exit-77 skip handling.
Real-window hotcwap tests and UI/GPU tests are disabled in bulk CTest runs by
default; set `VEXGRAPH_ENABLE_WINDOW_TESTS=ON` in the CLion CMake profile to opt
in. Their native Run/Debug targets remain available for you to select manually.
Neither a lab pass nor a successful build is visual approval. Demos/galleries
are not added as automated tests. After adding test files, reload CMake.

## The repositories

| Path | Layer | Remote |
|---|---|---|
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

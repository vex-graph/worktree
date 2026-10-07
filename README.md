# vexgraph — the worktree

A **thin wrapper repo**. It holds the many independent vexgraph repositories
side by side and nothing else — like a folder of small repos, not a monorepo.
Each nested directory is its own checkout with its own remote: commit and push
*inside each of those*, never here. Everything private (notes, the local app
harness, assets) is git-ignored, so this repo stays tiny.

## Build: `b`

### CLion: CMake is IDE metadata only

Each code repository has its own `CMakeLists.txt` and README guidance for
navigation, diagnostics and inlay hints. Per-repo source targets are excluded
from default builds: no dependency downloads, release linking or application
runner is wired into them. Supply local dependency header paths where required;
missing headers remain real errors, never fake declarations. Source-free
blueprints explicitly have no source targets. IDE appearance is user-verified.

Use [b](https://github.com/vex-graph/b) for actual builds. The workspace-root and
`tests/` CMake entries retain their existing b-metadata/native-test integration;
they are separate from the per-repo indexing-only entries. See each repository's
README for its current build command and stated standalone/runtime gaps.

The build system lives in the independent [`vex-graph/b`](https://github.com/vex-graph/b)
checkout at `personal/b/`. `b.c` is a language-agnostic CLI — a small suite (`b.h` +
`util.c` + pluggable `languages/*` adapters) that owns `run`, `build` and the
planned `export` surface. The adapter set is open-ended and grows over time;
`personal/b/README.md` lists the languages wired today. `personal/b/workspace.c` remains the
workspace engine that builds the whole ecosystem graph (libs, shaders, tests,
apps); `tools/b` is a thin forwarding launcher for it.

```sh
./tools/b build            # build everything (libs, tests, apps)
./tools/b test [substr]    # build + run every *_test
./tools/b run <name>       # run a target (an app launches as a real .app)
./tools/b targets | watch | cc | doctor | clean
```

Drop a `_main/<name>.c` containing a `main()` and `./tools/b run <name>` builds,
bundles and launches it as an ad-hoc-codesigned `.app`. All build state lives
*outside* the tree (`~/Library/Application Support/vexgraph/b/`, override
`$B_HOME`); compilation databases in `personal/b/` are ignored.

For standalone projects, add the `personal/b/` checkout to `PATH`, or invoke `personal/b/b`:

```sh
./b/b run exec ./hello.c
./b/b java ./Hello.java
./b/b build python ./pkg
./b/b build c ./native-project
```

### Run the file you are looking at (CLion)

The CLion external tool **b Runner → Run current file** runs
`tools/b run "$FilePath$"`, so invoking it from an open source file builds and
launches that file (its stem resolves to a declared target or a `tests/` app).
The project run configuration named **b** triggers the same tool. This is the
"open a file, press Run, it runs" path while `personal/b/workspace.c` is still the
builder.

See `personal/b/README.md` for the implemented command contract and packaging roadmap.
`run instance` runs directly through a runtime or an existing executable;
`run exec` builds the source artifact before launching it. Generic export
packaging is not implemented yet. The former CMake adapter is no longer the
workspace entry point.

## Architecture and implementation status

R2 has two cooperating repositories: **Vexspoke** owns CPU computation, math,
algorithms, synchronization and behavior; **Relational Engine** owns memory
allocation/storage, stable row chunks, variable bindings and native C search over
Rust-owned spans. Migration is staged: the existing Vexspoke memory/container ABI
and default allocator remain until explicit migration and owner proof. R1 owns
storage residency/lifetimes; GPU shaders and dispatch remain Graphvex R3.

**This ecosystem is unfinished.** The layer map describes intended ownership,
not a completion claim. In particular the R5 applications are unfinished shells,
scaffolds or designs—not finished IDE, DAW, studio or game products. See the
[readiness wiki](ecosystem/ecosystem/Home.md) and file-specific test evidence.

## The repositories

| Path | Layer | Remote |
|---|---|---|
| `personal/b` | standalone build-system CLI + workspace engine | `vex-graph/b` |
| `ecosystem/repos/hotcwap` | R1 kernel host · windows | `vexgraph-ecosystem/hotcwap` |
| `ecosystem/repos/relational-engine` | R2 memory/storage · native C search | `vexgraph-ecosystem/relational-engine` |
| `ecosystem/repos/vexspoke` | R2 CPU computation · behavior; legacy storage ABI retained | `vexgraph-ecosystem/vexspoke` |
| `ecosystem/repos/graphvex` | R3 GPU driver (rect-first, no swapchain) | `vexgraph-ecosystem/graphvex` |
| `ecosystem/repos/api-haven` | R3 API / connectors | `vexgraph-ecosystem/api-haven` |
| `ecosystem/repos/language`, `ecosystem/repos/darkbase` | R3 *(scaffolds)* | `vexgraph-ecosystem/*` |
| `ecosystem/repos/darling-framework` | R4 widget interfaces · partial implementation | `vexgraph-ecosystem/darling-framework` |
| `ecosystem/repos/sesh` | R4 interface · session relay blueprint | `vexgraph-ecosystem/sesh` |
| `ecosystem/repos/samplerate` | R5 interactable · audio engine | `vexgraph-ecosystem/samplerate` |
| `ecosystem/projects/{anti,drawling,semicolon,impedance}` | R5 · unfinished apps | `vexgraph-ecosystem/*` |
| `tests` | the shared test suite | `vexgraph-ecosystem/tests` |
| `ecosystem/ecosystem`, `ecosystem/.github`, `personal/vex-graph` | meta | `vexgraph-*/*` |

Local-only (git-ignored, never published): `_trash/` retired checkouts ·
`_notes/` notes · `_main/` apps · `tools/` workspace helpers · `resources/`
assets.

## Rules

The workspace is governed by a constitution: **`preferences.md`** — read it in
full; repositories with local laws add their own `<repo>-preferences.md`.
Locally it is one real, Git-ignored workspace-root file, not a symlink or a
tracked Vexspoke file. Its published canonical edition is:

**https://gist.github.com/vex-graph/4132a6c45cb6d3797c3e8eff2e94035a**

Cite every law by its canonical **Title**, never by
number (the Law Identity Doctrine). **Never push without an explicit, one-off
order** (the Git Workflow Law).

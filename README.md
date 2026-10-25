# vexgraph — the worktree

A **thin wrapper repo**. It holds the many independent vexgraph repositories
side by side and nothing else — like a folder of small repos, not a monorepo.
Each nested directory is its own checkout with its own remote: commit and push
*inside each of those*, never here. Everything private (notes, the local app
harness, assets) is git-ignored, so this repo stays tiny.

## Current State

**Implemented:** the wrapper structure, the `b`-driven build entry (`tools/b` →
`suite/personal/b/b run exec tools/workspace.c`), the workspace build graph, the shared
`tests/` suite, the lint and layout ratchets, the readiness scoreboard and the
per-repository CI caller generator, and this documentation. **Proven:** macOS builds and the scoped
test suites recorded in `metadata/gists/test-checklist.md`; the nested repositories range
from implemented slices to source-free blueprints. **No sibling repository has an
installed CI caller or baseline yet**, and the Windows *build* waits on the
`tools/b` port even though the Python tooling already runs there.
**The R5 applications and R6
superapps are unfinished** — shells, scaffolds or designs, not shipped products.
Semicolon's working R6 terminal shell is a dogfooding surface for editing this
workspace and trying its registered `b` workflows, not proof that the intended
full-stack IDE already exists.

## Build: `b`

### CLion: CMake is IDE metadata only

Open **this workspace root** in CLion. Its `CMakeLists.txt` is the only maintained
project entry: no nested repository, application, personal tool or test checkout
needs one. It imports `b`'s registered contexts and recursively discovers extra
`.c`/`.m`/`.h` files in the declared source roots, with separate owner include
paths and host-platform selection. Reload CMake after adding files; do not add
CMake files per class or folder. Source-free blueprints get no fake target.

Compiler flags and include paths support diagnostics, completion and inlay hints;
enable their display in the IDE. Actual IDE appearance is user-verified. Missing
headers remain real errors. Rust analysis uses the actual `Cargo.toml` packages,
not CMake. Imported engine comparison source remains separate from runtime proof.

Use [b](https://github.com/vex-graph/b) for actual builds. The root retains the
existing b-metadata/native-test integration, with window/GPU/UI tests opt-in.
Excluded supplemental source targets do not link releases or run applications.
No IDE configure pass proves standalone runtime dependency closure.

The build system lives in the independent [`vex-graph/b`](https://github.com/vex-graph/b)
checkout at `suite/personal/b/`. `b.c` is a language-agnostic CLI — a small suite (`b.h` +
`util.c` + pluggable `languages/*` adapters) that owns `run`, `build` and the
planned `export` surface. The adapter set is open-ended and grows over time;
`suite/personal/b/README.md` lists the languages wired today. `tools/workspace.c` remains the
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
`$B_HOME`); compilation databases in `suite/personal/b/` are ignored.

For standalone projects, add the `suite/personal/b/` checkout to `PATH`, or invoke `suite/personal/b/b`:

```sh
./suite/personal/b/b run exec ./hello.c
./suite/personal/b/b java ./Hello.java
./suite/personal/b/b build python ./pkg
./suite/personal/b/b build c ./native-project
```

### Run the file you are looking at (CLion)

The CLion external tool **b Runner → Run current file** runs
`tools/b run "$FilePath$"`, so invoking it from an open source file builds and
launches that file (its stem resolves to a declared target or a `tests/` app).
The project run configuration named **b** triggers the same tool. This is the
"open a file, press Run, it runs" path while `tools/workspace.c` is still the
builder.

See `suite/personal/b/README.md` for the implemented command contract and packaging roadmap.
`run instance` runs directly through a runtime or an existing executable;
`run exec` builds the source artifact before launching it. Generic export
packaging is not implemented yet. The former CMake adapter is no longer the
workspace entry point.

### Dogfooding with Semicolon

[`suite/projects/semicolon`](suite/projects/semicolon/README.md) is the R6
terminal shell for browsing and editing vexgraph itself. From a project
directory, `smc` (or `semicolon`) opens the tree; the per-user `smc` link is
installed explicitly with `sh suite/projects/semicolon/install-command.sh`.
Opening a workspace C test with a text-detected `main` and choosing Run sends
its absolute path through this workspace's `tools/b run` graph rather than
compiling that file alone. Other supported files use the standalone `b` route.
The result appears in a separate, bounded, scrollable console; its reported
exit code or signal belongs to the launched `b` process. A successful launch
of a windowed app is not a visual test or proof its GUI behaved correctly.
Semicolon's own terminal build is currently `suite/projects/semicolon/build.py`;
do not infer a registered R6 build target or a general project-graph resolver.

## CI and readiness

Three workspace tools answer "what is good to go?" without adding a second build
system:

```sh
python3 tools/linter.py --baseline .github/lint-baseline.json     # lint ratchet
python3 tools/arrange.py --baseline .github/arrange-baseline.json  # layout ratchet
python3 tools/readiness.py [--markdown|--json|--execute]          # scoreboard
python3 tools/ci_repos.py list|clone|check|baselines|callers      # manifest wiring
```

`tools/platforms.json` is the single manifest: every repository, its tier, the
platforms it declares support for and the platforms its own documentation claims
as proven. `readiness.py` composes that manifest with the checklist ledger and
the linter; a skip, a compile-only job or an unproven platform is never counted
as a pass. `ci_repos.py` validates the manifest, clones missing checkouts (dry
run by default), records each repository's repo-relative ratchet baseline, and
installs the reusable-workflow caller. It refuses to install a caller into a
repository that has no lawbook or baseline, because that caller would be red on
arrival.

The root workflow (`.github/workflows/ci.yml`) clones every declared repository,
runs the tooling tests, then runs preference integrity, the checklist check, the
lint and layout ratchets and the secret audit on Linux. The tooling tests,
preference check and both ratchets repeat on `windows-latest`; the byte-hash
ledger gate stays on Linux because a CRLF checkout would report every row stale
for a line-ending artifact. The clone is not decoration: the tests and the
ledger live in nested checkouts, and the ratchets, the lawbook check and the
checklist are workspace-scoped, so a root-only checkout would find no tests,
scan zero ecosystem files and report every recorded violation "retired".
The windows job is a real portability check, not a build claim: it proves the
Python tools and the ratchets behave identically there, while the ecosystem
build stays macOS/Linux. A weekly scoreboard job clones every declared
repository and publishes the table to the job summary. Each repository can call
`.github/workflows/repo-check.yml` through a generated
`.github/workflows/vexgraph-ci.yml`: that caller lints and arranges against the
repository's own baselines, checks its lawbook exists, audits secrets, and
accepts optional trusted build/test commands. The lint job of that reusable
workflow runs on both Ubuntu and Windows.

**Declared proof is not observed proof.** Today macOS is proven for 14 of 24
repositories; Linux and Windows are proven for none. No sibling repository has a
checked-in baseline or caller yet, and eight have no `<repo>-preferences.md`.
The Windows **build** is deliberately absent until `tools/b` is ported off
macOS-only flags and POSIX calls; a compile-only placeholder would be a false
green. Windows tooling coverage is real but narrower than a build: it runs the
Python tools, the checklist and both ratchets on a Windows runner. Linux is
exercised by the Semicolon job and the weekly scoreboard. The ratchets record
899 lint entries and 60,804 layout findings. Both baselines are generated from
clean `origin/main` checkouts of every declared repository, not from a live
working tree: the audit job clones `main`, so a tree snapshot would either hide
debt that is already published or, once the working tree retires findings,
report the published state as new debt. A live tree can therefore show new
findings in files a session has not pushed yet, and the snapshot has to be
regenerated immediately before the root commit that carries it. New debt is
blocked while old debt is retired gradually. `--write` is opt-in and has not
been run across the workspace.

## Architecture and implementation status

R2 has two cooperating repositories: **Vexspoke** owns CPU computation, math,
algorithms, synchronization and behavior; **Relational Engine** owns memory
allocation/storage, stable row chunks, variable bindings and native C search over
Rust-owned spans. Native IO/NIO has migrated to RE and default production builds
link that implementation; Vexspoke contains no copies. Native C allocation semantics
are preserved, not rewritten into Rust; broader collection migration is staged. R1 owns
storage residency/lifetimes; GPU shaders and dispatch remain Graphvex R3.

### Vertically integrated across vexgraph's stack

**`b` is orchestration, not another R tier.** `tools/b` delegates to the
independent `suite/personal/b` tool and this workspace's target graph in
`tools/workspace.c`; it compiles/links selected owners and runs registered
targets. Semicolon consumes that graph through a child-process Run seam; it
does not own compilers, drivers, or lower-tier implementations.

| Layer | Semicolon today | Intended seam, not current integration |
| :--- | :--- | :--- |
| R1 Hotcwap | No direct runtime host integration in the terminal shell. | Supervised hot module and application lifetime. |
| R2 Relational Engine + Vexspoke | Its build directly links engine native Memory and Vexspoke CPU helpers. | Broader resident storage/computation contracts remain separately proved. |
| R3 Determinant + Language | Determinant's terminal-cell panel, input and Markdown toolkit plus Language's C23 lexer and conservative `C23Highlights` pass are linked into the shell. SemicolonSyntax supplies live `.c`/`.h` colors for keywords, types, functions, variables, macros, literals, brackets, and distinct regular/doc comments. | Semantic classification, inlays, Language project/index services and Graphvex GUI remain future integration. |
| R4 interfaces | No Darling, Sesh, or Harness integration in this terminal path. | GUI widgets, sessions, and agent interface through their public seams. |
| R5 applications | Primeagen stays independent. | Optional registered consumer workflow, not a reverse dependency. |
| R6 Semicolon | A working, limited file-browser/editor and `b` run-console shell. | Full workflow composition and the graphical IDE remain unfinished. |

The [Semicolon README](suite/projects/semicolon/README.md) records the current
console, platform proof, and limitations. Language's own source and
[status](suite/ecosystem/language/README.md) govern what its lexical subset
actually offers; this direct lexical consumer is not a parser, semantic IDE or
generic adapter/project-engine integration.

**This ecosystem is unfinished.** The layer map describes intended ownership,
not a completion claim. In particular the R5 applications and R6 superapps are
unfinished shells, scaffolds or blueprints—not finished IDE, DAW, studio, game or
superapp products. See the
[readiness Gist](https://gist.github.com/vex-graph/6943f92acb931b25dad1073c46da6ce7) and file-specific test evidence.

## The repositories

| Path | Layer | Remote |
|---|---|---|
| `suite/personal/b` | standalone build-system CLI; workspace graph under `tools/` | `vex-graph/b` |
| `suite/personal/func` | standalone compile-time opcode orchestrator | `vex-graph/func` |
| `suite/ecosystem/hotcwap` | R1 kernel host · windows | `vexgraph-ecosystem/hotcwap` |
| `suite/ecosystem/relational-engine` | R2 memory/storage · native C search | `vexgraph-ecosystem/relational-engine` |
| `suite/ecosystem/vexspoke` | R2 CPU computation · behavior; legacy storage ABI retained | `vexgraph-ecosystem/vexspoke` |
| `suite/ecosystem/graphvex` | R3 GPU driver (rect-first, no swapchain) | `vexgraph-ecosystem/graphvex` |
| `suite/ecosystem/api-haven` | R3 API / connectors | `vexgraph-ecosystem/api-haven` |
| `suite/ecosystem/determinant` | R3 terminal rendering, widgets, CLI parsing and caller-fed input | `vexgraph-ecosystem/determinant` |
| `suite/ecosystem/language` | R3 caller-fed lexer/project/index slice; parser and LSP unfinished | `vexgraph-ecosystem/language` |
| `suite/ecosystem/darkbase-engine` | R3 native vex store · `Database` M1 + `.vexdb` persistence implemented | `vexgraph-ecosystem/darkbase-engine` |
| `suite/ecosystem/darling-framework` | R4 widget interfaces · partial implementation | `vexgraph-ecosystem/darling-framework` |
| `suite/ecosystem/sesh` | R4 interface · session relay partial implementation | `vexgraph-ecosystem/sesh` |
| `suite/ecosystem/harness` | R4 interface · the user's own agent (partial local objects) | `vexgraph-ecosystem/harness` |
| `suite/ecosystem/samplerate` | R3 driver · native audio engine (CoreAudio/WASAPI/ALSA) | `vexgraph-ecosystem/samplerate` |
| `suite/projects/{drawling,impedance}` | R5 · unfinished apps | `vexgraph-ecosystem/*` |
| `suite/personal/primeagen` | standalone personal R5 agent client; future Semicolon consumer seam | `vex-graph/primeagen` |
| `suite/projects/semicolon` | R6 · working terminal dogfooding shell; GUI and cross-tier workflow composition unfinished | `vexgraph-ecosystem/semicolon` |
| `suite/projects/anti` | R6 · unfinished superapp | `vexgraph-ecosystem/anti` |
| `tests` | the shared test suite | `vexgraph-ecosystem/tests` |
| `suite/personal/vex-graph` | profile/meta | `vex-graph/vex-graph` |

Local-only (git-ignored, never published): `_trash/` retired checkouts ·
`_notes/` notes · `_main/` apps · `resources/` assets. (`tools/` helpers are
tracked and published.)

## Rules

The workspace is governed by a constitution: **`metadata/gists/preferences/PREFERENCES.md`** — read it in
full; repositories with local laws add their own `<repo>-preferences.md`.
Locally it is one real, Git-ignored Gist-owned file, not a symlink or a
tracked Vexspoke file. Its published canonical edition is:

**https://gist.github.com/vex-graph/4132a6c45cb6d3797c3e8eff2e94035a**

Cite every law by its canonical **Title**, never by
number (the Law Identity Doctrine). **Never push without an explicit, one-off
order** (the Git Workflow Law).

## Scope and Limitations

**Scope:** a thin wrapper that nests the independent repositories and builds them
together through `b`; it owns no product code. **Deliberately not covered:**
feature implementation (each repo owns its own) and visual acceptance (the
user's). **Known limits and gaps:** no monorepo semantics — each nested repo is
committed and pushed independently; nothing here proves any application runtime,
and the readiness Gist plus `metadata/gists/test-checklist.md` are the evidence of record.
CI observes lint debt, the evidence ledger, lawbook presence, the Semicolon
macOS/Linux job and the Python tooling on Windows; it does not prove the other
repositories' runtimes, and the Windows ecosystem build is unported. The
readiness table reports declared proof separately from observed CI so the two
cannot be confused.

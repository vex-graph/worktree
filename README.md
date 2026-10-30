# vexgraph — the worktree

A **workspace repository**. It contains independent repositories under `suite/`,
workspace-owned build and policy tools under `tools/`, shared test/evidence
material under `tests/` and `metadata/`, and root CI/IDE integration. It is not a
single product-code monorepo: each nested repository retains its own source
ownership and is committed independently. Check `git status` before assuming a
nested path is a separate checkout.

## Current State

The root workspace coordinates independent projects. `tools/b` directly
launches the `b` build engine in `vexgraph-hobby-projects/b`. Root CI also owns
workspace-wide documentation and tooling checks. Test evidence is recorded per
executable owner in `metadata/gists/test-checklist.md`; consult that ledger and
the readiness report for current results rather than relying on counts copied
into this README. Product readiness varies by repository. Read each repository's
own README and lawbook before treating a planned integration or roadmap item as
implemented.

## Build: `b`

### CLion: CMake is IDE metadata only

Open **this workspace root** in CLion. Its `vexgraph-ecosystem` is the only maintained
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
checkout at `suite/b`. `b.c` is a language-agnostic CLI — a small suite (`b.h` +
`util.c` + pluggable `languages/*` adapters) that owns `run`, `build` and the
planned `export` surface. The adapter set is open-ended and grows over time;
`tools/b` is a forwarding launcher directly executing `vexgraph-hobby-projects/b/b`.
The workspace uses `b workspace` to register/refresh targets into `.b/workspace.json`,
and `b build` to compile declared targets in dependency order.

```sh
./tools/b workspace          # scan workspace and write .b/workspace.json
./tools/b build [target...]  # compile all targets, or named targets and deps
./tools/b breeze <file.c>    # run a single file directly (alias: ./tools/b run)
./tools/b box [<action>]     # package management (--init, --apply, etc.)
./tools/b adapter <name>     # adapter operations (e.g. adapter list)
```

Running tests across the workspace is handled by the dedicated test runner:

```sh
./tools/shell/test.sh [substr]  # run test binaries, reporting PASS/SKIP/FAIL
```

Drop a `_main/<name>.c` containing a `main()` and `./tools/b run <name>` builds,
bundles and launches it as an ad-hoc-codesigned `.app`. All build state lives
*outside* the tree (`~/Library/Application Support/vexgraph/b/`, override
`$B_HOME`); compilation databases in `suite/b` are ignored.

For standalone projects, add the `suite/b` checkout to `PATH`, or invoke `suite/b`:

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

See `suite/b` for the implemented command contract and packaging roadmap.
`run instance` runs directly through a runtime or an existing executable;
`run exec` builds the source artifact before launching it. Generic export
packaging is not implemented yet. The former CMake adapter is no longer the
workspace entry point.

### Dogfooding with Semicolon

[`suite/semicolon`](suite/semicolon/README.md) is the R6
terminal shell for browsing and editing vexgraph itself. From a project
directory, `smc` (or `semicolon`) opens the tree; the per-user `smc` link is
installed explicitly with `sh suite/projects/semicolon/install-command.sh`.
Opening a workspace C test with a text-detected `main` and choosing Run sends
its absolute path through this workspace's `tools/b run` graph rather than
compiling that file alone. Other supported files use the standalone `b` route.
The result appears in a separate, bounded, scrollable console; its reported
exit code or signal belongs to the launched `b` process. A successful launch
of a windowed app is not a visual test or proof its GUI behaved correctly.
Semicolon's own terminal build is currently `suite/semicolon`;
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

`tools/platforms.json` declares repository platforms. `readiness.py` composes
those declarations with the checklist and lint state; consult its output for
current readiness. `ci_repos.py` validates repository wiring and can prepare
checkouts, baselines and reusable-workflow callers. Its command details are
available through `python3 tools/ci_repos.py --help`.

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

CI coverage and platform support change over time. The workflow files under
`.github/workflows/` are authoritative for configured jobs; the readiness
scoreboard and checklist report observed evidence. A configured job or declared
platform is not, by itself, proof that a product runs there. The root workspace
does not claim a platform result beyond what those records currently show.

## Architecture and implementation status

Tier ownership is governed by the Vertical Integration Law and the owning
repositories' lawbooks. The table below records observed Semicolon composition
at the time represented by its own README; it is not a full integration map for
the ecosystem.

### Vertically integrated across vexgraph's stack

**`b` is orchestration, not another R tier.** `tools/b` directly executes the
`b` build engine in `vexgraph-hobby-projects/b`. It compiles and links declared
targets via `.b/workspace.json`. Semicolon consumes that graph through a
child-process Run seam; it does not own compilers, drivers, or lower-tier implementations.

| Layer | Semicolon today | Intended seam, not current integration |
| :--- | :--- | :--- |
| R1 Lifetime | No direct runtime host integration in the terminal shell. | Supervised application and OS lifetime. |
| R2 Relational Engine + Vexspoke | Its build directly links engine native Memory and Vexspoke CPU helpers. | Broader resident storage/computation contracts remain separately proved. |
| R3 Determinant + Language | Determinant's terminal-cell panel, input and Markdown toolkit plus Language's C23 lexer and conservative `C23Highlights` pass are linked into the shell. SemicolonSyntax supplies live `.c`/`.h` colors for keywords, types, functions, variables, macros, literals, brackets, and distinct regular/doc comments. | Semantic classification, inlays, Language project/index services and Graphvex GUI remain future integration. |
| R4 interfaces | No Darling, Sesh, or Harness integration in this terminal path. | GUI widgets, sessions, and agent interface through their public seams. |
| R5 applications | Primeagen stays independent. | Optional registered consumer workflow, not a reverse dependency. |
| R6 Semicolon | A working, limited file-browser/editor and `b` run-console shell. | Full workflow composition and the graphical IDE remain unfinished. |

The [Semicolon README](suite/semicolon/README.md) records the current
console, platform proof, and limitations. Language's own source and
[status](suite/language/README.md) govern what its lexical subset
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
| `suite/b` | standalone build-system CLI; workspace graph under `tools/` | `vex-graph/b` |
| `suite/func` | standalone compile-time opcode orchestrator | `vex-graph/func` |
| `suite/lifetime` | R1 kernel host · windows · OS lifetime | [vexgraph-ecosystem/lifetime](https://github.com/vexgraph-ecosystem/lifetime) |
| `suite/hotcwap` | R1 host supervisor · hot reload | [vexgraph-ecosystem/hotcwap](https://github.com/vexgraph-ecosystem/hotcwap) |
| `suite/relational-engine` | R2 memory/storage · native C search | `vexgraph-ecosystem/relational-engine` |
| `suite/vexspoke` | R2 CPU computation · behavior; legacy storage ABI retained | `vexgraph-ecosystem/vexspoke` |
| `suite/graphvex` | R3 GPU driver (rect-first, no swapchain) | `vexgraph-ecosystem/graphvex` |
| `suite/api-haven` | personal API / connectors | [vexgraph-ecosystem/api-haven](https://github.com/vexgraph-ecosystem/api-haven) |
| `suite/determinant` | R3 terminal rendering, widgets, CLI parsing and caller-fed input | `vexgraph-ecosystem/determinant` |
| `suite/language` | R3 caller-fed lexer/project/index slice; parser and LSP unfinished | `vexgraph-ecosystem/language` |
| `suite/darkbase` | R3 native vex store · `Database` M1 + `.vexdb` persistence implemented | `vexgraph-ecosystem/darkbase-engine` |
| `suite/darling-framework` | R4 widget interfaces · partial implementation | `vexgraph-ecosystem/darling-framework` |
| `suite/sesh` | R4 interface · session relay partial implementation | `vexgraph-ecosystem/sesh` |
| `suite/harness` | R4 interface · the user's own agent (partial local objects) | `vexgraph-hobby-projects/harness` |
| `suite/samplerate` | R3 driver · native audio engine (CoreAudio/WASAPI/ALSA) | `vexgraph-ecosystem/samplerate` |
| `suite/drawling` | R5 · unfinished drawing studio | [vexgraph-ecosystem/drawling](https://github.com/vexgraph-ecosystem/drawling) |
| `suite/impedance` | R5 · unfinished audio application | [vexgraph-ecosystem/impedance](https://github.com/vexgraph-ecosystem/impedance) |
| `suite/primeagen` | standalone personal R5 agent client; future Semicolon consumer seam | `vex-graph/primeagen` |
| `suite/semicolon` | R6 · working terminal dogfooding shell; GUI and cross-tier workflow composition unfinished | `vexgraph-ecosystem/semicolon` |
| `suite/anti` | R6 · unfinished superapp | `vexgraph-ecosystem/anti` |
| `tests` | shared executable-owner evidence and test lawbook | [vexgraph-ecosystem/tests](https://github.com/vexgraph-ecosystem/tests) |
| `metadata/vex-graph` | profile/meta | `vex-graph/vex-graph` |

Some paths may be Git-ignored local material. Use `git status --ignored` and the
root `.gitignore` to determine what is local-only; do not infer that `resources/`
or `_main/` exists or is ignored in every checkout.

## Rules

The workspace constitution's compressed law list is
[`metadata/gists/preferences/gist.md`](metadata/gists/preferences/gist.md).
Use `./tools/prefs list` and read only the relevant law; do not load the full
documentation wholesale. Repositories can add their own `<repo>-preferences.md`.
The published canonical edition is:

**https://gist.github.com/vex-graph/4132a6c45cb6d3797c3e8eff2e94035a**

Cite every law by its canonical **Title**, never by
number (the Law Identity Doctrine). **Never push without an explicit, one-off
order** (the Git Workflow Law).

## Scope and Limitations

**Scope:** workspace-level build orchestration, CI/tooling integration,
preferences, readiness and shared evidence. Feature implementation remains with
the owning repository. **Known limits:** root documentation and CI do not imply
that every nested repository is integrated, portable or product-ready. Use the
owning source, README, lawbook, current readiness report and test checklist for
those claims. Visual acceptance remains the user's assessment.

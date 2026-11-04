# vexgraph's worktree

A **workspace repository**. It contains independent repositories under `vex/`,
workspace-owned build and policy tools under `tools/`, and root IDE integration.
Shared evidence material and the constitution live one level up, in the personal
hub. It exists so that the tools that run the workspace, the development cycle,
and the shared repositories stay three separable concerns — each with its own
owner, its own commit discipline and its own documentation. It is not a
single product-code monorepo: each nested repository retains its own source
ownership and is committed independently. Check `git status` before assuming a
nested path is a separate checkout.

## Workspace shape, and its three nested levels

The workspace is three nested levels, like a hotel: the lobby contains the
room, the room contains the bathroom. (cant find a better analogy sorry). Each level is its own workspace with its
own owner, its own commit discipline and its own documentation.

| Level | Path | What it is | What it owns |
| :--- | :--- | :--- | :--- |
| 1 — hub | `<whatever>` you desire | personal, discrete, per-person, depends on you | the agent harnesses (`.claude`, `.opencode`, `.idea`) if you do use them, the agent bus and name registry (`_notes/agents/`), personal notes (`_notes/`), and the working copies of the published Gists (`metadata/gists/`) |
| 2 — workspace | `<whatever>/worktree` (this repository) | the whole thing | `tools/` — the tools that run the whole thing — plus the development cycle; root scaffolding and documentation only |
| 3 — shared stack | `<whatever>/worktree/vex` | where repositories share together | the vertically integrated R1–R6 dogfooding stack as independent repository checkouts |

The rules of the nesting:

- **Level 1 is personal.** It can be per person, and agents hook into it here.
  Nothing at this level is cloned or shared; the Gist is its distribution
  channel. The constitution's local copy lives here because injection is
  per-session; its published form is the Gist.
- **Level 2 separates two concerns.** `tools/` runs the whole thing and is
  fine with it (`prefs`, `orchestrator`, `b`, the shell gates, the Python
  ratchets); the development cycle — build, test, prove, commit per repository
  — flows through level 3. This repository tracks scaffolding, tools and
  documentation only: `vex/` is ignored except the two tracked exceptions
  below.
- **Level 3 does not care about ecosystem membership.** Whether a repository
  is "part of the ecosystem" or not no longer matters. What matters is that it
  is a share in one vertically integrated stack that dogfoods itself: R1
  lifetime and supervision, R2 compute and storage, R3 drivers, R4 interfaces,
  R5 applications, R6 superapps — each tier consuming what the tiers below
  own, never rebuilding beside them.
- **The two tracked exceptions inside `vex/`** are `vex/annotation/` (the
  shared `;;ANNOTATION` vocabulary, tracked here because every repository
  consumes it and no single repository owns it) and `vex/vex-test/` (the
  app-level contract test this workspace runs). Everything else under `vex/`
  is committed inside its own checkout, never here.

## Current State

The root workspace coordinates independent projects. `tools/b` directly
launches the `b` build engine checked out at `vex/b`. Root CI is removed from
the working tree in the current restructure; the local gate is
`./tools/orchestrator ci`. Test evidence is recorded per executable owner in
the hub's `metadata/gists/test-checklist.md`; consult that ledger and the
readiness report for current results rather than relying on counts copied into
this README. Product readiness varies by repository. Read each repository's
own README and lawbook before treating a planned integration or roadmap item as
implemented.

## Build: `b`

### CLion: CMake is IDE metadata only

Open **this workspace root** in CLion (or any JetBrains IDE). Its `vex` directory is the only maintained
project entry: no nested repository, application, personal tool or test checkout
needs one. `CMakeLists.txt` is self-sufficient — it reads nothing from `b`,
derives every repository, include root and source from `vex/` itself, and
creates one excluded object library indexing the whole tree. That is the whole
adapter: it supplies compile commands for colours, symbol resolution, inlay
hints and debug info.

It creates **no executable and no test target**, so CLion's CMake integration
contributes nothing to the run dropdown. Reload CMake after adding files; do not
add CMake files per class or folder. Missing headers remain real errors. Rust
analysis uses the actual `Cargo.toml` packages, not CMake.

Use [b](https://github.com/vex-graph/b) for every build and every run. CLion's
run list lives in `.idea/runConfigurations/` (git-ignored, like the rest of
`.idea/`) and is regenerated from `b.assembly.json` by:

```sh
python3 tools/ide/runners.py           # write .idea/runConfigurations
python3 tools/ide/runners.py --check   # fail if the run list is stale
```

Each unit of type `app` or `executable` gets one configuration named
`b: <unit>` that runs `./tools/b run <unit>` in a terminal. `b: build all`
chains one `b build` per unit in dependency order. Add a unit to `b.assembly.json` and rerun the generator;
there is no other place to register a runner.

The build system lives in [`vex`](https://github.com/vex-graph/b); `tools/b`
is a thin forwarding launcher for its dispatcher. `b.assembly.json` declares the
units (type, sources, include roots, deps); `.b/workspace.json` is the generated
file inventory and `.b/out/` holds the artifacts. `b build` compiles units in
dependency order and `b run` builds one unit and launches it.

```sh
./tools/b generate            # rescan the tree into .b/workspace.json
./tools/b assembly            # validate/normalize b.assembly.json
./tools/b build [unit...]     # compile all units, or named units and deps
./tools/b run <unit> [args]   # build one unit, then launch it
```

Running tests across the workspace is handled by the dedicated test runner:

```sh
./tools/shell/test.sh [substr]  # run test binaries, reporting PASS/SKIP/FAIL
```

All build state lives *outside* the tree (`~/Library/Application Support/b/`,
override `$B_HOME`). Unit type `lib` produces a `.a`, `executable` a bare
binary, `app` a macOS `.app` bundle, and `module` a reloadable `.dylib`.

### Run configurations and debugging (CLion)

Every runnable unit (`app` or `executable`) has one shared configuration named
`b: <unit>` that executes `./tools/b run <unit>` in the terminal. There is no
CMake run target to compete with it, and no per-file launcher beside it. Adding
a unit means adding it to `b.assembly.json` and rerunning
`python3 tools/ide/runners.py`.

`b` compiles with `-g -O0` by default (`B_CFLAGS` overrides), so the binary in
`.b/out/` is fully debuggable. Debug it with LLDB:

```sh
b run <unit>            # in one shell
lldb -p "$(pgrep -f '.b/out/<unit>')"      # attach from another
```

or launch it directly under LLDB with the arguments you need. CLion's Debug
action needs an executable target it owns, which this adapter deliberately does
not create; attach to the running process instead.

### Dogfooding with Semicolon

[`vex/semicolon`](vex/semicolon/README.md) is the R6
terminal shell for browsing and editing vexgraph itself. From a project
directory, `smc` (or `semicolon`) opens the tree; the per-user `smc` link is
installed explicitly with `sh vex/semicolon/install-command.sh`.
Opening a workspace C test with a text-detected `main` and choosing Run sends
its absolute path through this workspace's `tools/b run` graph rather than
compiling that file alone. Other supported files use the standalone `b` route.
The result appears in a separate, bounded, scrollable console; its reported
exit code or signal belongs to the launched `b` process. A successful launch
of a windowed app is not a visual test or proof its GUI behaved correctly.
Semicolon's own terminal build is currently `vex/semicolon`;
do not infer a registered R6 build target or a general project-graph resolver.

## CI and readiness

Root CI (`.github/workflows/`) is removed from the working tree in the current
restructure, and the ratchet baselines went with it; whether root CI returns,
and in what shape, is an open decision. The local gate is the same policy on
demand:

```sh
./tools/orchestrator ci                  # tools/shell/ci.sh, read-only
```

Observed on 2026-11-02, mid-restructure: workflow references, preferences
integrity and the secret scan PASS. The declared-checkout and tooling-test
steps FAIL because `tools/platforms.json` still keys repositories by their
remote identities (`vexgraph-ecosystem/<repo>`) while the checkouts live flat
under `vex/<repo>`; the checklist-ledger step FAILs until the ledger is
re-synced to the new geography. `readiness.py` likewise sees only the workspace
row for the same reason.

`tools/platforms.json` declares repository platforms; `tools/python/readiness.py`
composes those declarations with the checklist and lint state;
`tools/python/ci_repos.py` validates repository wiring and can prepare
checkouts. Consult their output for current readiness — a declared platform or
configured job is not, by itself, proof that a product runs there.

## Architecture and implementation status

Tier ownership is governed by the Vertical Integration Law and the owning
repositories' lawbooks. The table below records observed Semicolon composition
at the time represented by its own README; it is not a full integration map for
the ecosystem.

### Vertically integrated across vexgraph's stack

**`b` is orchestration, not another R tier.** `tools/b` directly executes the
`b` build engine checked out at `vex/b`. It compiles and links declared
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

The [Semicolon README](vex/semicolon/README.md) records the current
console, platform proof, and limitations. Language's own source and
[status](vex/language/README.md) govern what its lexical subset
actually offers; this direct lexical consumer is not a parser, semantic IDE or
generic adapter/project-engine integration.

**This ecosystem is unfinished.** The layer map describes intended ownership,
not a completion claim. In particular the R5 applications and R6 superapps are
unfinished shells, scaffolds or blueprints—not finished IDE, DAW, studio, game or
superapp products. See the
[readiness Gist](https://gist.github.com/vex-graph/6943f92acb931b25dad1073c46da6ce7) and file-specific test evidence.

## The repositories

The shared stack lives one level down: [`vex/README.md`](vex/README.md) is the
clickable map — every repository is public, and each row links out to its
remote. This repository intentionally tracks none of their content.

### Library names

Two repositories are addressed by their conventional library names rather than
their full repository names:

| directory | name used in code | library |
|---|---|---|
| `vex/re` | `re` | the relational engine — the memory owner, R0 |
| `vex/darling` | `darling` | the UI framework |

Every include and every build manifest spells the short name, because that is
what a consumer writes:

```c
#include "re/nio/mem.h"
#include "darling/frame/frame.h"
```

The remote URLs keep the long names (`vexgraph-ecosystem/relational-engine`,
`vexgraph-ecosystem/darling-framework`); only the local checkout and the
include roots are short. The two names are the same library — `re` is not a
fork or a shim, it is `relational-engine` under the name it is imported by.

## Clone the whole ecosystem

To reproduce this exact three-level shape from public sources only:

```sh
./tools/shell/clone-ecosystem.sh <destination>            # dry run: prints every step
./tools/shell/clone-ecosystem.sh <destination> --execute  # builds it
```

It clones this repository as `<destination>/worktree`, every manifest-declared
repository flat into `<destination>/worktree/vex/<name>` (the manifest keys are
remote identities, so each lands at `vex/<basename>`), the five published
Gists into `<destination>/metadata/gists/`, and the profile checkout into
`<destination>/metadata/vex-graph/`. It deliberately does not copy the
per-person level: harness configuration (`.claude`, `.opencode`, `.idea`), the
agent bus and `_notes/` are yours to set up; the hub's `AGENTS.md` orients
agents once that is done (SETUP.md was retired into it).

Two honest limits: uncommitted local material is never imported — the script
builds the public shape only — and until this restructure's commits land on the
published `main`, a freshly cloned worktree still carries the pre-restructure
tool geography (its `tools/prefs` reports zero lawbooks under the new `vex/`
layout). The script's shape is the target state.

## Rules

The workspace constitution's compressed law list is
[`metadata/gists/preferences/gist.md`](../metadata/gists/preferences/gist.md)
(the hub's working copy, one level up). Use `./tools/prefs list` and read only
the relevant law; do not load the full documentation wholesale. Repositories
can add their own `<repo>-preferences.md`. The published canonical edition is:

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

**Restructure limits (2026-11-02):** the three-level shape above is locked in
and the migration is mid-flight. `tools/platforms.json` keys are remote
identities, not local paths, so the CI gate, the readiness scoreboard and the
checklist inventory see only the workspace row until the manifest is re-keyed
to `vex/<repo>`. The CLion adapter is self-sufficient — everything is derived
from `vex/`, no `b.assembly.json`, no `b` — and its syntax checks expose
pre-existing source debt, not wiring: `annotation/debug.h` is referenced
(`vexspoke/struct/collection.h`, `re/nio/mem.h`) but does not
exist, blocking half the ecosystem's include chains; `b/b/b.c` and
`primeagen/session/session_bridge.c` use `strcmp`/`memchr` without
`<string.h>`; lifetime's ObjC permission file overshoots its annotation hop.
`tools/b` and `tools/orchestrator`
reach the engine at `vex/b`; the engine's own `dispatch` front door still
hardcodes the pre-rename hub path and belongs to the b rewrite. Repository
lawbooks carry dead relative links from the same three moves (constitution
lifted to the hub, `suite/` flattened to `vex/`, `tests/` moved under `vex/`);
`./tools/prefs check` reports them by name. Evidence rows in the test checklist
are workspace-relative paths, so the move reset the ledger; greens must be
re-executed, not copied.

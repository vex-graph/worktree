# Mini IDE (the jGRASP dream)

**Idea (in vexgraph's words):** a mini IDE for many things — like jGRASP,
that 3 MB little IDE that supports C, Python, Java and builds itself.
Support 30 more languages. ObjC shims and even Swift (needs a Mac to
sign). Its own Xcode. Zed feel, JetBrains depth: ASTs, colors, everything
simplified, everything relational, bare metal. Vulkan feels overkill —
that's the point.

## What "like jGRASP" means here
- **Tiny and self-building**: the IDE compiles itself, ships small, starts
  fast. No Electron, no JVM warm-up, no 2 GB download.
- **Many languages, one roof**: 30+ grammars behind a single AST/highlight
  interface — each language a hot-swappable L3 module (the driver pattern
  from `/Users/vexgraph/CLionProjects/vexgraph/_docs/_thoughts/darkbase/database-switchboard.md`, reused: `lang_python.dylib`, ...).
- **Apple-native without Xcode**: ObjC shims already exist in-tree;
  Swift support via toolchain + Mac signing. Goal: build Apple apps
  without opening Xcode.
- **Feel**: Zed's speed and calm + JetBrains' understanding (real ASTs,
  real colors, real navigation) − their weight.

## Why the current stack already points here
- **hotcwap** = the plugin engine: languages, themes, and tools as
  reloadable modules. Edit the Python grammar without restarting the IDE.
- **Per-instance loader state** = multi-project: two folders open, same
  framework, zero collision (that's the IDE case it was built for).
- **`Application` + multiwindow** = the shell: one identity, N windows,
  OS-owned.
- **Relational everything** (`Variable`, `Type`, BitPacked OOP) = the
  AST substrate: code as relations, not text. Highlighting, navigation,
  and refactoring all read the same tree.
- **Vulkan renderer** = the canvas: overkill on purpose. One GPU path for
  text, minimaps, and visualizations at 120 Hz — the thing Zed proved
  matters and JetBrains never had.

## Constraints (sized honestly)
1. **5 MB binary budget.** The shell (editor, window chrome, database
   client) must fit in 5 MB: dead-stripped Release, system frameworks
   only, no vendored weight that isn't on the hot path. Everything heavy
   lives outside the binary (see 4).
2. **Shell-out philosophy.** Git, compilers, formatters, and linters are
   terminal tools invoked as subprocesses — never linked in (no libgit2,
   no bundled toolchain). The IDE is a fast UI over bash, not a platform.
   `git`, `clang`, `python3` are assumed present, detected, degraded
   cleanly when absent.
3. **Database rides along, tiny.** The `Database` interface from
   `/Users/vexgraph/CLionProjects/vexgraph/_docs/_thoughts/darkbase/database-switchboard.md` backs project state (open files, symbols,
   history) — native vex store, kilobytes of code, inside the budget.
   MariaDB/Postgres/online APIs stay behind the interface, out of the
   binary, reached over the network only.
4. 30 grammars is the long pole — each needs tokenizer + parser + AST
   mapping. Start with 3 (C, Python, Java — the jGRASP trio) to prove
   the `Language` module contract, then fan out.
5. Swift requires a Mac for signing, full stop. Everything else stays
   portable; Apple-targeting detects the toolchain and degrades cleanly.
6. Bare metal cuts both ways: no framework means every widget (caret,
   completion popup, minimap) is hand-built on the darling tree. Fast
   forever, but nothing is free.

## Sequencing
1. `Language` module contract (tokenize/parse/highlight AST) + C driver.
2. Editor shell: `Application` + one window + GPU text (darling text
   stack already exists).
3. Self-host: the IDE builds vexspoke/hotcwap/darling from inside itself.
4. Python, Java → the jGRASP trio. Then 30.

## Status
Envisioned, not started. Substrate in place (loader, windows, text,
compositor); no `Language` contract, no editor shell.

## Next step
After the `Database` interface turn, draft the `Language` module
contract the same way: struct fields, registry, manifest exports
(`Lang_tokenize/parse/highlight/...`).

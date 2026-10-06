# Vexgraph build and CLion entry points

`./tools/b build` remains the project build entry point. Vexgraph owns
`tools/workspace.c` and `tools/build_annotation.h`: repository names, dependencies,
shader generation and registered tests belong here, not in the generic b repo.
The launcher uses `personal/b/b run exec tools/workspace.c -- <arguments>`.
Generic b compiles and executes the C coordinator; it has no workspace subcommand.
This is a project-owned executable graph, not a new declarative manifest format.

The saved CLion **b Runner → Run current file** tool invokes `tools/run-current`
with the active file path. The existing **b** play configuration still references
that same tool action. Reopen CLion to load the corrected saved settings.

- C files under `tests/` or `ecosystem/projects/` use the project graph for linking.
- Other files use generic `b run exec`, selected by extension.
- No file, missing files, compiler errors and program exit status propagate.
- Finder-launched CLion gains Homebrew/rustup search paths after its existing PATH.
- A standalone Rust file must have a `main`; Cargo library modules are not standalone
  programs. Use `personal/b/b build cargo <crate-directory>` for the crate.

For example, select `personal/relational-engine/rust/src/helloworld.rs` and use
the b action. Its current code prints its arguments and deliberately exits 5;
an exit-code-5 report is not a compiler or launcher failure. That file is untouched.

Automated proof uses `tests/tools/run_current_test.py` and
`tests/b/workspace_test.py`, without opening windows. Saved XML wiring is proved;
CLion UI operation and appearance still need user confirmation after reopening.

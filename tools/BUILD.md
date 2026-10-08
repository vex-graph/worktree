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

For example, select `../ecosystem/repos/relational-engine/rust/src/helloworld.rs` and use
the b action. Its current code prints its arguments and deliberately exits 5;
an exit-code-5 report is not a compiler or launcher failure. That file is untouched.

Automated proof uses `tests/tools/run_current_test.py` and
`tests/b/workspace_test.py`, without opening windows. Saved XML wiring is proved;
CLion UI operation and appearance still need user confirmation after reopening.

The workspace-root `CMakeLists.txt` is an IDE adapter. Open the root as a CMake
project and reload it in CLion to index production C/Objective-C with the flags
exported by `b ide`. Excluded `vexgraph_index_*` object targets supply the code
model only; runtime builds still delegate to b. Native test Run/Debug targets
retain assertions, and window/GPU/UI CTest execution is disabled by default.

The adapter also indexes every registered application/tool and its shared helper
sources, including `tests/darling/compositor/filter_gallery.c` and
`tests/darling/darling_tests.c`. Each keeps its own transitive include context;
gallery indexing does not register or launch it as a test. The tests-only
`tests/CMakeLists.txt` reuses this same complete graph. After changing the graph,
reload the active CMake project so CLion replaces its old source contexts.

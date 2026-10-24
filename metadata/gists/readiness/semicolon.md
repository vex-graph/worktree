# semicolon — R6 IDE Superapp

> **Unfinished R6 superapp—not a finished IDE.** This page is a roadmap, not
> whole-app readiness. R2 comprises [vexspoke](#file-vexspoke-md) CPU computation/behavior and
> [relational-engine](#file-relational-engine-md) memory/storage/native C search. Migration is staged with
> retained Vexspoke ABI/default allocator. R1 owns lifetimes/residency; GPU work
> stays [graphvex](#file-graphvex-md). No engine integration or automatic schema migration implied.
> No local lawbook (`semicolon-preferences.md`) exists yet; that missing repo-local
> preferences file is an explicit gap, and the universal constitution plus
> applicable test laws still bind.

> R6 Superapp: composes Language support, bounded `b` tool integration and future
> Primeagen AI workflows through public R1–R5 contracts. Primeagen remains
> independently buildable R5; it never depends on Semicolon. Lower tiers never
> include R6 code. The roadmap below is aspirational, not implemented integration.
> Design target: 5 MB stripped binary budget. <10ms launch, relational AST depth, and visual runtime data structure stepping in C23.
> Laws: Shell-out philosophy (subprocesses via ProcessSpawn, no linked libgit2), Relational AST substrate, Hot-swappable language drivers, Vulkan 120Hz canvas.

---

## 🎯 Tier-0 Integration Proofs (Ground Truth)

*The live binary is the final judge. This table gates the repo headline — never the rows below, which keep their own independent truth. Statuses are re-verified, never copied from memory.*

| Proof Binary | End-to-End User Verification | Status | Evidence |
|---|---|:---:|---|
| `semicolon_boot` (no target) | Launch → open `main.c` → AST highlight → type → save | 🟥 | Reserved empty source directories, no stub files or working source |
| `semicolon_tui` (this checkout) | `cd <project> && smc` → browse/edit files and switch tabs → Markdown Code/Preview → Run supported files through `b` → inspect actual child exit/signal in a separate bounded, scrollable console → Ctrl-C restores and saves per-project state | 🟨 | `tests/semicolon/tui_main_test.py`, `run_console_test.py`, `rail_interaction_test.py`, `gitignore_rail_test.py`, `icon_catalog_test.py`, `install_command_test.py` and `readme_test.py` pass on macOS arm64 with strict C23/PTy or mechanical scopes. The console keeps 10,000 lines (2,048 bytes per line); workspace C tests route through `tools/b`, external C through standalone `b`. Tabs, basic edits with idle autosave and bounded 64-state Ctrl-Z/Ctrl-Y undo/redo, dot-entry filtering, icon catalog and persisted rail width are implemented. The build probes `-std=gnu23` once and falls back to `-std=gnu2x` for Apple clang before 16; file-revision checks read `st_mtimespec` on Apple and `st_mtim` elsewhere, keeping the nanosecond ignore/save compare portable (the non-Apple branch is source-guarded and awaits CI). Scroll motion is Determinant's `TerminalScrollGlide`; Semicolon supplies the document bounds. Fake `b` asserts routing without running windowed apps. `exit 0` is a child result, not visual approval. Physical-terminal appearance, other platforms, arbitrary project graphs, Language C23 adapter consumption and R1/R4/R5 integration remain unproved. |

### C23 lexical consumer

| Feature | Scope and executed evidence | Status |
| :--- | :--- | :---: |
| `SemicolonSyntax` and live editor ink | Direct static Language `C23Lexer` + `C23Highlights` consumption for lowercase `.c`/`.h`; copied complete row snapshot, configurable role pens, multiline lexical context, cold edit refresh, bold brackets, failed-refresh stale-ink suppression, unchanged glyph/caret/save coordinates. `C23Highlights` paints keywords, literals, brackets, gray regular comments, muted-green documentation comments, and heuristic type/function/variable/member/macro colors; line-start preprocessor markers and directive names (`#include`, `#define`) share the macro pen, and the header path after `#include` uses string green for both quoted and `<...>` forms while ordinary `<`/`>` are not string-colored. `tests/semicolon/editor/semicolon_syntax_test.c`, `language_bridge_test.c` via `python3 tests/semicolon/editor/run.py`: macOS arm64 strict optimized C23/assertions and ASan/UBSan, 2,560-span growth, bridge allocation-stage refusal/count/recovery/accounting, hostile bytes, wide cells, scroll and action-layer preservation, missing-dependency artifact preservation and scripted xterm-256color PTY edit recoloring/exact autosave. Whole-document synchronous analysis, not incremental or latency proof; true semantic classification, parameter-specific inlays, italic documentation comments, exact truecolor, diagnostics, generic adapter/project engine and other platforms remain unproved/unwired. Physical-terminal appearance is user-owned. | 🟨 |

The older TUI row's unproved C23 *adapter* consumption means the generic
`C23Adapter`/registry/project seam; this new consumer calls public `C23Highlights`
directly, not that engine. Language remains R3 and Semicolon owns only the R6
consumer/palette/cache; no lower-tier implementation is copied into the app.
`tests/semicolon/launcher_language_test.py` additionally proves Language-header
mtime invalidation and no-change reuse with a disposable fake builder/artifact;
it does not substitute for the real compiler/Language link owner above. The ten
existing Semicolon regression owners pass after accounting for token-style
escapes in exact source-text assertions; no physical terminal was launched.

## The Semicolon Standard: A Mini IDE That Builds Big Things

Pointer-routed scrolling: both wheel axes pan file tabs by whole tabs; tree
children scroll vertically and pan horizontally (modified vertical wheel also
pans sideways), independent of source scrolling. Selected tabs reveal once and
clipped titles retain close controls. Plain and Markdown source clicks now share
the painted source-row origin; exact persisted insertion bytes are asserted by
`tests/semicolon/tui_main_test.py`. Five rail/editor/console owners pass on
macOS arm64 with strict native C23 and scripted PTY execution. Ghostty physical
terminal behavior, appearance and other platforms remain unproved.

The project root is pinned to the rail's top row beside its neutral-gray canonical
location (`~/...` only inside HOME); clipped locations show an ellipsis. Children
scroll below it with two-space indentation per level, capped at six levels.
`tests/semicolon/rail_format_test.py` proves location resolution, HOME-component
matching, neutral indexed-gray PTY output, root folding/reopen and exact nesting
steps; the rail/editor/Markdown/run-console regressions pass on macOS arm64.
Physical-terminal appearance remains user-owned and unverified.
The hover divider and its mouse target sit at x=railWidth, one cell to the right
of the former position, outside the file list. The rail interaction owner proves
the former seam stays free of the grip and last-cell folder/file clicks work;
resize/collapse/reopen and the TUI/run-console regressions pass on macOS arm64.

Terminal icon update: Nerd Font BMP file/folder icons are implemented by default,
with a shared filename lookup for tree rows and tabs. `--icons plain` and
`SEMICOLON_ICONS=plain` select the non-private-use fallback; explicit CLI overrides
a valid environment setting. `tests/semicolon/tui_main_test.py` proves mapping,
open/closed folders, defaults, fallback, override, invalid-mode rejection and wide
ncurses PTY output on macOS arm64. There is no settings screen or font detection;
physical font appearance/width and other platforms remain unproved. Earlier
assessment-only Nerd icon notes in the table above are superseded by this owner evidence.

Semicolon's legacy IDE design targets a small, responsive C23 application with
relational AST tooling. The footprint and launch-time targets below are unmeasured
aspirations. One executable exists today — the terminal shell with a limited
editor and `b` run console — but the graphical and relational subsystems below
are not built. `b` is a standalone orchestration tool, not an R tier.

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                             THE SEMICOLON STANDARD                               │
├─────────────────────────┬─────────────────────────┬──────────────────────────────┤
│ 1. Sub-5MB Binary Shell │ 2. Shell-Out Toolchains │ 3. Relational AST Substrate  │
│ • Dead-stripped C23     │ • Subprocess engine     │ • Code as relations, not text│
│ • Zero vendored weight  │ • Invokes git/clang/py  │ • Symbol tables via Darkbase │
│ • <10ms launch time     │ • No bloated libgit2    │ • Semantic highlighting at   │
│ • Self-compiling core   │ • Clean degradation     │   120Hz via graphvex SDF     │
├─────────────────────────┴─────────────────────────┴──────────────────────────────┤
│ 4. Visual Data Structure Workbench + 30+ Hot-Swappable Language Drivers         │
│ • Dynamic L3 grammar modules (lang_c23.dylib, lang_python.dylib, lang_java.dylib)│
│ • Live visual data structure stepping (arrays, trees, graphs)      │
│ • Apple-native toolchain: build & codesign Mac apps without opening Xcode        │
│ • Built-in spreadsheet viewer: ZIP+XML .xlsx reader rendered on GridContainer    │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## Status Legend & Grading Standards

Every subsystem and mini-achievement is strictly graded based on the current reality of the codebase, test suites, and live runtime behavior:

| Emoji | Level | Definition |
|:---:|:---|:---|
| 💚 | **98% Done** | Basically 98% done: fully wired, compiles, runs, production-ready, actively polished |
| 🟩 | **95% Done** | Implemented & functional: wired, compiles and runs, minor polish remaining |
| 🟨 | **85% Done** | Substantially implemented: core works or has tests proving behavior, missing specific features/edge cases |
| 🟧 | **75% Done** | Partial implementation: core struct/concept exists, but major features missing or unwired |
| 🟥 | **Concept / Draft** | Still a concept or spec'd in docs/headers only, zero working source |
| ⬜ | **Vital Future Work** | Not implemented yet, but vital roadmap feature (+1 on the feature) |

---

## High-Level Subsystem Summary

| # | Subsystem | Scope Summary | Overall Status |
|:---:|:---|:---|:---:|
| 1 | `Binary Shell & Self-Hosting` | 5 MB stripped binary target, zero vendored weight, self-compiling harness | 🟥 |
| 2 | `Shell-Out Subprocess Engine` | Proposed bounded tool orchestration; no superapp implementation | 🟥 |
| 3 | `Relational AST Substrate` | Code represented as relational tables via `Variable`, `Type`, BitPacked OOP | 🟥 |
| 4 | `Language Module Contract` | Hot-swappable L3 grammar dylibs (`Lang_tokenize/parse/highlight/format`) | 🟥 |
| 5 | `Language Grammar Catalog` | Bootstrap trio (C23, Python, Java) expanding to 30+ hot-reloadable grammars | 🟥 |
| 6 | `Core Text Buffer Engine` | Line-array document with bounded 64-state snapshot undo/redo; still not a piece table/gap buffer, UTF-8 character indexing or multi-branch history | 🟧 |
| 7 | `Syntax Highlighting Canvas` | Token and AST-based semantic coloring rendered at 120Hz via graphvex | 🟥 |
| 8 | `Editor Chrome & Gutter` | Line numbers, code folding rails, active line highlight, multi-caret editing | 🟥 |
| 9 | `High-Framerate Minimap` | Zoomed-out code overview map with viewport slider rendered on GPU | 🟥 |
| 10 | `Project Explorer & Tree` | VFS-backed file tree built on darling TreePanel with git status glyphs | 🟥 |
| 11 | `Multi-Tab & Split Workspace` | Tab strip with dirty flags, horizontal/vertical splits, detached windows | 🟥 |
| 12 | `Command Palette & Quick Open` | Cmd+K fuzzy file/symbol/command launcher built on darling CommandPalette | 🟥 |
| 13 | `LSP & Autocomplete Engine` | Language Server Protocol client bridge, completion popup, signature hover | 🟥 |
| 14 | `Symbol Navigation & Refactor` | Go-to-definition, find all references, symbol rename, breadcrumb bar | 🟥 |
| 15 | `Inline Diagnostics & Linter` | Squiggly error lines, margin warning badges, hover problem cards | 🟥 |
| 16 | `Compiler Pipeline & Errors` | Build output log with clickable regex error jump-to-line | 🟥 |
| 17 | `Embedded Terminal Panel` | PTY-driven terminal emulator surface with ANSI color support | 🟥 |
| 18 | `Git Version Control Gutter` | Gutter diff indicators (added/modified/deleted), inline hunk review | 🟥 |
| 19 | `Visual Data Structure Workbench` | Live visual data structure stepping (linked lists, trees, memory relations) | 🟥 |
| 20 | `Apple Toolchain & Codesigning` | ObjC/Swift compilation and Mac codesigning without Xcode dependency | 🟥 |
| 21 | `Project State in Darkbase` | Native vexdb store backing open files, recent files, and cursor memory | 🟥 |
| 22 | `Tabular Spreadsheet Viewer` | Lightweight ZIP+XML .xlsx reader displaying sheets in darling GridContainer | 🟥 |
| 23 | `Terminal Shell (tty host)` | The IDE design drawn on a real terminal through Determinant's panel/text tree and `TerminalTreeView`, with scroll motion from `TerminalScrollGlide`: reads a real file into a two-axis scrollable editor with per-file line-number alignment, borderless mode/tab header that tracks the resizable rail, an invisible-at-rest rail seam revealed as a centered bold 3/4-cell hover grip and used as the drag target, breadcrumb/status footer, wheel + edge autoscroll on both axes, UTF-8 locale plus wide-character ncurses output, mouse reporting enabled for any-motion plus SGR and disabled on exit, and no panel background so the terminal's theme shows through; Nerd Font file/folder icons are implemented, while physical font appearance remains user-owned | 🟨 |

---

## Detailed Mini-Achievements Breakdown

### 1. Binary Shell, Footprint & Self-Hosting

The lightweight core executable container designed to build itself.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 1.1 | 5 MB Binary Footprint Budget | Stripped release binary target linked against system frameworks only | 🟥 |
| 1.2 | Instant Cold Launch (<10ms) | Sub-10ms startup time bypassing runtime warmup and heavy dynamic link chains | 🟥 |
| 1.3 | Self-Hosting Compiler Invocation | IDE compiles its own binary and sibling repos (vexspoke/hotcwap/darling) | 🟥 |
| 1.4 | Headless Build-Runner Mode | Running compilation and test suites headlessly via CLI flags (`semicolon --build`) | 🟥 |
| 1.5 | Single-Instance Window Multiplexing | Secondary file openings forward to active process via OS sockets | 🟥 |

### 2. Shell-Out Subprocess Engine

Invoking external command-line tools without linked binary bloat.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 2.1 | Bounded Subprocess Spawning | Proposed consumption of R2 process contracts; no superapp implementation or integration proof | 🟥 |
| 2.2 | Toolchain Auto-Detection | Proposed tool discovery; no superapp implementation | 🟥 |
| 2.3 | Graceful Feature Degradation | Proposed unavailable-tool disposition; no superapp implementation | 🟥 |
| 2.4 | Asynchronous Process Streaming | Proposed bounded streaming; no superapp implementation | 🟥 |
| 2.5 | Child Process Cancellation | Proposed cancellation/reap workflow; no superapp implementation | 🟥 |

### 3. Relational AST & Symbol Substrate

Representing code as relational entities rather than raw text streams.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 4.1 | Relational AST Node Schema | Nodes represented via `vexspoke` `Variable`, `Type`, and BitPacked OOP | 🟥 |
| 4.2 | Project Symbol Index Table | Relational symbol registry: structs, functions, macros, enums, variables | 🟥 |
| 4.3 | memory-Efficient Scope Tree | Lexical scope hierarchy mapped to parent-relative arena blocks | 🟥 |
| 4.4 | Incremental AST Invalidation | Re-parsing only modified function bodies rather than whole translation units | 🟥 |
| 4.5 | Cross-File Symbol Resolution | Querying symbol definitions across multiple translation units | 🟥 |

### 4. Language Module Contract (`drivers/language` workspace checkout)

Hot-swappable L3 dynamic grammar driver architecture.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 4.1 | Standard Grammar Driver Interface | `Lang_tokenize()`, `Lang_parse()`, `Lang_highlight()`, `Lang_format()` exports | 🟥 |
| 4.2 | Dynamic Grammar Hot-Reloading | Reloading grammar `.dylib`s via `hotcwap` without restarting the IDE | 🟥 |
| 4.3 | Token Stream memory Pool | Fast slab-allocated token array populated in a single linear pass | 🟥 |
| 4.4 | Fault-Tolerant Error Recovery | Parser continues scanning and highlighting past syntax error sites | 🟥 |
| 4.5 | Grammar Version Hash Check | Verifying grammar ABI compatibility prior to loading | 🟥 |

### 5. Language Grammar Catalog

The multi-language support matrix spanning 30+ languages.

| # | Language Grammar | Category / Scope | Status |
|:---:|:---|:---|:---:|
| 5.1 | C23 / C11 Driver | Bootstrap Trio: preprocessor, types, struct field offset reflection | 🟥 |
| 5.2 | Python 3 Driver | Bootstrap Trio: indentation rules, f-strings, type annotations | 🟥 |
| 5.3 | Java Driver | Bootstrap Trio: class models, packages, annotations, generics | 🟥 |
| 5.4 | Swift Driver | Apple Native: closures, protocols, actor concurrency keywords | 🟥 |
| 5.5 | Objective-C Driver | Apple Native: message brackets `[obj msg]`, properties, protocols | 🟥 |
| 5.6 | Rust Driver | Extended Catalog: lifetimes, traits, borrow checker syntax | ⬜ |
| 5.7 | Go Driver | Extended Catalog: goroutines, channels, interface definitions | ⬜ |
| 5.8 | Zig Driver | Extended Catalog: comptime blocks, error unions, build.zig syntax | ⬜ |
| 5.9 | JavaScript / TypeScript Driver | Extended Catalog: JSX/TSX tags, arrow functions, async/await | ⬜ |
| 5.10 | Bash / Zsh Shell Driver | Extended Catalog: parameter expansions, pipes, subshells | ⬜ |
| 5.11 | SQL Driver | Extended Catalog: queries, DDL, table joins, keywords | ⬜ |
| 5.12 | JSON / YAML / TOML Driver | Data Configurations: key-value pairs, nested arrays, validation | ⬜ |
| 5.13 | Markdown / GFM Driver | Documentation: headers, bold/italic, fenced code blocks | ⬜ |
| 5.14 | GLSL / SPIR-V Shader Driver | Graphics: vertex/fragment stages, uniform buffers, qualifiers | ⬜ |

### 6. Core Text Buffer Engine

Underlying high-speed text representation and editing buffer.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 6.1 | Piece Table / Gap Buffer Core | Fast insertions and deletions with minimal re-allocation overhead | 🟥 |
| 6.2 | UTF-8 Byte & Character Indexing | Translating byte offsets, UTF-8 code points, and column visual widths | 🟥 |
| 6.3 | Line Ending Normalization | Seamless handling of LF (`\n`) and CRLF (`\r\n`) line endings | 🟥 |
| 6.4 | Multi-Branch Undo/Redo Tree | Universal command history with branching states and timeline scrubbing | 🟥 |
| 6.5 | memory-Mapped File Loading | Instant opening of large files via `vexspoke` `mmap` with zero copy | 🟥 |
| 6.6 | Bounded Linear Undo/Redo | Per-document 64-state owned-line snapshots with monotonic revisions and saved-point tracking; Ctrl-Z/Ctrl-Y through raw-mode input, one transaction per edit or UTF-8 scalar, failed edits preserve both text and redo. `tests/semicolon/tui_main_test.py` proves typed-byte undo/redo, redo discard after a new edit and exact autosaved bytes on macOS arm64; `tests/semicolon/editor/run.py` runs the production tui-main history under ASan/UBSan for a multibyte scalar. Allocation-failure injection remains a gap; whole-document copies, not a piece tree or multi-branch timeline. | 🟨 |
| 6.7 | Read-Only & Scratch Modes | Protecting generated or read-only files from accidental edits | 🟥 |

### 7. Syntax Highlighting & Visual Presentation

120Hz GPU text rendering and semantic token coloring.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 7.1 | Lexical Token Color Mapping | Keywords, literals, strings, comments, operators mapped to theme colors | 🟥 |
| 7.2 | AST Semantic Highlighting | Differentiating function calls, type definitions, and local parameters | 🟥 |
| 7.3 | Rainbow Bracket Matching | Color-coded nested parenthesis, square brackets, and curly braces | 🟥 |
| 7.4 | Matching Delimiter Highlights | Subtle background box highlighting matching opening/closing brackets | 🟥 |
| 7.5 | Indentation Guidelines | Vertical guide lines showing current indentation depth | 🟥 |
| 7.6 | Whitespace & Tab Visibility | Visual dots for spaces and arrows for tab characters | 🟥 |

### 8. Editor Chrome & Gutter (`CodeField`)

The editor framing controls and interactive margins.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 8.1 | Line Number Gutter | Left-anchored gutter showing line numbers and active line emphasis | 🟥 |
| 8.2 | Active Line Background Highlight | Subtle highlight band highlighting the active cursor line | 🟥 |
| 8.3 | Code Folding Rail & Arrows | Expandable/collapsible arrows on scopes, functions, and block comments | 🟥 |
| 8.4 | Multiple Caret Editing | Alt+Click placing multiple cursors with synchronized character typing | 🟥 |
| 8.5 | Column / Rectangular Selection | Shift+Alt+Drag selecting vertical blocks of text | 🟥 |
| 8.6 | Soft Word-Wrapping | Wrapping text at editor margin preserving indent levels | 🟥 |
| 8.7 | Smooth Caret Animation | Fluid caret repositioning and blinking animation | 🟥 |

### 9. High-Framerate Minimap

Vulkan-powered bird's-eye code overview.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 9.1 | Zoomed-Out Code Overview | Scaled-down syntax-highlighted render of entire source file | 🟥 |
| 9.2 | Interactive Viewport Slider | Highlighted rectangle tracking active view with drag-to-scroll | 🟥 |
| 9.3 | Diagnostic Margin Marks | Error red dots and warning yellow marks rendered along minimap rail | 🟥 |
| 9.4 | Search Match Indicators | Highlighting occurrences of searched tokens across the file | 🟥 |

### 10. Project Explorer & File Tree

Workspace navigation and file system hierarchy.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 10.1 | VFS File Hierarchy Scanning | Scanning folder trees via `vexspoke` I/O with `../../../.gitignore` filtering | 🟥 |
| 10.2 | TreePanel Integration | Rendering expandable directory rows built on darling `TreePanel` | 🟥 |
| 10.3 | File Type Icon Badges | File extension-specific vector icons (C, H, Py, Java, Sh, JSON) | 🟥 |
| 10.4 | Git Status Glyph Overlays | Color-coded indicators for Untracked (green), Modified (blue), Ignored (gray) | 🟥 |
| 10.5 | Inline File Operations | Right-click context menu: New File, New Folder, Rename, Delete, Reveal | 🟥 |

### 11. Multi-Tab & Split Workspace

Flexible layout workspace built on darling containers.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 11.1 | Multi-Tab File Strip | Tab bar displaying open files with close (`×`) buttons | 🟥 |
| 11.2 | Dirty State Indicator | Visual dot on tab title indicating unsaved modifications | 🟥 |
| 11.3 | Horizontal & Vertical Splits | Tiling editor panes side-by-side using darling `SplitPanel` | 🟥 |
| 11.4 | Drag-and-Drop Tab Reordering | Interactive tab dragging to reorder or move between split panes | 🟥 |
| 11.5 | Detached Floating Windows | Tearing off tabs into independent OS windows managed by `hotcwap` | 🟥 |

### 12. Command Palette & Quick Open

Keyboard-centric modal command hub.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 12.1 | Quick File Open (Cmd+P) | Fuzzy matching file paths across the workspace with instant preview | 🟥 |
| 12.2 | Action Command Palette (Cmd+Shift+P) | Searchable action registry (Toggle Terminal, Format Document, Rebuild) | 🟥 |
| 12.3 | Workspace Symbol Search (Cmd+T) | Fuzzy matching structs, functions, and symbols across all indexed files | 🟥 |
| 12.4 | Jump-to-Line Prompt (Ctrl+G) | Numeric line:column jump dialog | 🟥 |

### 13. LSP & Autocomplete Engine

Intelligent code assistance and completion popups.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 13.1 | Stdio LSP Process Harness | Launching and communicating with language servers via stdin/stdout JSON-RPC | 🟥 |
| 13.2 | Completion Suggestion Popup | Floating popup list anchored to active caret escaping container clips | 🟥 |
| 13.3 | Completion Item Details | Displaying type signatures, doc summaries, and completion kind icons | 🟥 |
| 13.4 | Signature Help Tooltip | Floating callout showing active parameter during function calls | 🟥 |
| 13.5 | Hover Documentation Card | Hovering over symbols shows markdown-rendered documentation and types | 🟥 |

### 14. Symbol Navigation & Refactoring

Deep code structure traversal.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 14.1 | Go-to-Definition (F12 / Cmd+Click) | Instant navigation to symbol declaration or definition site | 🟥 |
| 14.2 | Find All References (Shift+F12) | Search results panel listing all usages of target symbol | 🟥 |
| 14.3 | Semantic Symbol Rename (F2) | Project-wide renaming of identifiers with preview diff | 🟥 |
| 14.4 | Breadcrumb Navigation Trail | Top bar showing `Project > Folder > File > Struct > Function` hierarchy | 🟥 |
| 14.5 | Jump Back / Forward History | Navigating back (`Cmd+[`) and forward (`Cmd+]`) through cursor jump history | 🟥 |

### 15. Inline Diagnostics & Problem Gutter

Visual compiler and linter feedback.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 15.1 | Squiggly Underline Overlays | Red (error), Yellow (warning), Blue (info) wavy underlines under text | 🟥 |
| 15.2 | Gutter Diagnostic Badges | Red circle and yellow triangle icons aligned with failing lines | 🟥 |
| 15.3 | Problem Tooltip on Hover | Hovering squiggly lines reveals exact compiler/linter error message | 🟥 |
| 15.4 | Project Problems Panel | Aggregated workspace error list with click-to-navigate rows | 🟥 |

### 16. Compiler Pipeline & Build Output

Direct toolchain execution and error parsing.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 16.1 | One-Key Build Trigger (Cmd+B) | Asynchronous build execution using the project's build system (`b`) | 🟥 |
| 16.2 | Clickable Regex Error Jump | Parsing `file.c:42:10: error:` to jump directly to offending line and column | 🟥 |
| 16.3 | Build Status Banner | Green/red status banner showing compile duration and exit code | 🟥 |
| 16.4 | Target Execution Runner (Cmd+R) | Launching compiled executable with console output attached | 🟥 |

### 17. Embedded Terminal Emulator

Built-in command-line console panel.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 17.1 | PTY Pseudoterminal Allocation | Allocating native pseudoterminal via `openpty` attached to default shell | 🟥 |
| 17.2 | ANSI / VT100 Escape Parser | Decoding cursor positioning, color codes, and line clearing sequences | 🟥 |
| 17.3 | Terminal Screen Buffer Grid | Fixed character grid rendered using darling monospaced typography | 🟥 |
| 17.4 | Interactive Keyboard Stream | Raw keystrokes and escape sequences forwarded directly to PTY fd | 🟥 |

### 18. Git Version Control Gutter & Staging

Lean source control interface powered by shell-out git.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 18.1 | Gutter Diff Indicators | Green bar (added), blue bar (modified), red triangle (deleted line) | 🟥 |
| 18.2 | Inline Hunk Diff Popup | Clicking gutter indicator opens diff card with Stage / Revert actions | 🟥 |
| 18.3 | Lightweight Git Status Bar | Branch name, dirty file count, and sync status displayed in footer | 🟥 |
| 18.4 | Commit Compose Box | Simple commit message input and Stage All / Commit buttons | 🟥 |

### 19. Visual Data Structure Workbench

The signature visual understanding dream: live animated data structures.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 19.1 | Array Visualizer | Live box array visualizing element values and index pointers | 🟥 |
| 19.2 | Linked List Visualizer | Node blocks with connecting pointer arrows dynamically drawn | 🟥 |
| 19.3 | Binary Tree & Graph Visualizer | Hierarchical tree layout showing parent/child nodes and balances | 🟥 |
| 19.4 | Variable Step Inspector | Step-by-step debugger stepping with value change animations | 🟥 |
| 19.5 | memory Canvas Integration | Drawing memory representations directly on the Vulkan 120Hz canvas | 🟥 |

### 20. Apple Native Toolchain & Codesigning

Zero-Xcode macOS application building and deployment.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 20.1 | Clang / Swiftc Command Generator | Formulating native compilation commands with Apple SDK frameworks | 🟥 |
| 20.2 | App Bundle Structure Creator | Generating `.app` bundles with `Contents/MacOS`, `Info.plist`, and icons | 🟥 |
| 20.3 | Developer Certificate Discovery | Probing macOS Keychain for valid Apple Developer codesigning identities | 🟥 |
| 20.4 | Codesign Subprocess Invocation | Invoking `codesign` with entitlements and hardened runtime flags | 🟥 |

### 21. Project State Storage in Darkbase

Instant workspace restoration powered by native vex store.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 21.1 | Open Files & Tab Order Persistence | Saving active tabs, split layouts, and active editor index | 🟥 |
| 21.2 | Caret & Scroll Position memory | Restoring exact cursor line, column, and scroll offset on file re-open | 🟥 |
| 21.3 | Workspace Project Settings Store | Key-value settings stored in native Darkbase database file | 🟥 |
| 21.4 | Recent Projects & History List | Tracking recent workspaces with instant one-click switching | 🟥 |

### 22. Tabular Spreadsheet Viewer (`.xlsx`)

Built-in spreadsheet inspection without external office suites.

| # | Mini-Achievement / Capability | Scope & Technical Details | Status |
|:---:|:---|:---|:---:|
| 22.1 | ZIP Archive Inflator | Decompressing `.xlsx` archives via lightweight zip reader | 🟥 |
| 22.2 | Sheet XML Parser | Streaming XML parser extracting cells, formulas, and strings | 🟥 |
| 22.3 | darling GridContainer Presentation | Displaying spreadsheet rows and columns in interactive `GridContainer` | 🟥 |
| 22.4 | Multi-Sheet Tab Navigation | Switching between workbook sheets via bottom sheet tabs | 🟥 |

---

## Strategic Implementation Priorities for Semicolon

To realize a mini IDE that builds big things in systematic, achievable phases:

1. **P0: Editor Shell Bootstrap**
   - Create the initial `semicolon` `Application` window using `hotcwap`.
   - Wire `CodeField` with basic line numbers and CoreText/graphvex text rendering.
   - Implement Piece Table / Gap Buffer for keyboard typing.

2. **P1: The Bootstrap Language Trio (`drivers/language` workspace checkout)**
   - Define the `Language` module C API contract.
   - Implement the C23 grammar driver (`lang_c23.dylib`) for syntax highlighting.
   - Implement Python and Java grammar drivers.

3. **P2: Shell-Out Toolchains & Build Pipeline**
   - Wire `ProcessSpawn` to run `clang` / `make` / `cmake`.
   - Implement build output log with clickable regex error jumping.

4. **P3: Workspace Ergonomics**
   - Integrate darling `TreePanel` for project file explorer.
   - Integrate darling `CommandPalette` for Cmd+P quick open.
   - Add multi-tab and split window support.

5. **P4: The Signature Visual Data Structure Workbench**
   - Build the interactive array, linked list, and tree visualization canvas.

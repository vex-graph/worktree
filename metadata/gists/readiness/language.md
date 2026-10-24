# language — Grammars, Relational AST & Language Server Provider

> **R2 dependency contract:** this R3 blueprint may borrow [vexspoke](#file-vexspoke-md) CPU
> computation/behavior and/or [relational-engine](#file-relational-engine-md) memory/storage/native C
> search public contracts. Existing Vexspoke memory/container ABI and default
> allocator remain during staged migration. No implemented engine integration,
> C/Rust atomic-layout compatibility or automatic schema migration is claimed.
> R1 owns lifetimes/residency; GPU shaders/dispatch remain [graphvex](#file-graphvex-md).

> **Architectural Tier**: R3 Driver (Language Server Provider & AST driver matrix for semicolon).
> **Production Standard**: *The 30+ Grammar Hot-Swappable AST Matrix: L3 HotModule Contract + Relational AST Substrate (`Variable`, `Type`, `BitPool`) + Zero-Alloc Lexer + LSP JSON-RPC Bridge + Semicolon Syntax/Diagnostic Driver*.
> **Governing Laws**:
> 1. **Code as Relations (Java/Relational Law)**: AST nodes are off-heap relational blocks or `{pool_id, pool_index}` handles in `vexspoke`. Syntax trees, highlighting, and symbol resolution all read the same relational graph.
> 2. **Hot-Swappable Language Drivers**: Each language is an isolated L3 module dylib (`lang_c.dylib`, `lang_python.dylib`, etc.) hot-reloaded via `hotcwap` without restarting the host IDE.
> 3. **Zero-Alloc Lexing**: Token streaming yields `TokenSpan` records into fixed caller-owned memory buffers.
> 4. **Two-Layer Access Cap**: AST node relationships (parent, child, next sibling) resolve in at most 2 lookups (the Semantic Consistency Law (Access depth)).
> 5. **Dest-Last Output**: Lexer, parser, and highlighter methods follow `fn(src, dest)` (the Semantic Consistency Law (Argument order)).

---

## Subsystem 1: L3 Language Module ABI Contract (`LangModule`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 1.1 | `LangDriver` VTable Contract | Function pointers: `tokenize`, `parse`, `highlight`, `format`, `complete`, `resolve` | 🟥 | Core ABI exported by language dylibs. |
| 1.2 | HotManifest Module Header | `hotcwap` module manifest identifying language ID, file extensions, and capabilities | 🟥 | Registers with `hotcwap` dynamic reload pipeline. |
| 1.3 | Language Capability Flags | Bitmask: `LANG_CAP_HIGHLIGHT`, `FOLDING`, `COMPLETION`, `FORMAT`, `LSP` | 🟥 | Declares language features supported by driver. |
| 1.4 | File Extension Discovery | Maps `.c`, `.h`, `.py`, `.java`, `.rs`, `.zig`, etc. to language IDs | 🟥 | Fast extension-to-driver lookup table. |
| 1.5 | Grammar Hot-Reloading | Reload grammar dylib live on file edit without editor restart | 🟥 | Instant iteration during language development. |

---

## Subsystem 2: Zero-Alloc Lexical Scanner & Tokenizer (`Lexer`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 2.1 | `TokenSpan` Record Layout | `[start (32b)][end (32b)][kind (16b)][flags (16b)]` (12 Bytes) | 🟥 | Flat, cache-aligned token slice representation. |
| 2.2 | Token Categories | Keywords, identifiers, literals, operators, comments, punctuation, preprocessor | 🟥 | Universal token kind enumeration. |
| 2.3 | Streaming Tokenizer Loop | `Lang_tokenize(src, len, destSpans, maxSpans, outCount)` | 🟥 | Dest-last token output into caller-owned buffer (the Semantic Consistency Law (Argument order)). |
| 2.4 | Multi-Line Token State | Encodes in-comment, in-string, and heredoc states across line boundaries | 🟥 | High-performance incremental line re-tokenization. |
| 2.5 | Unicode & UTF-8 Byte Offsets | Correct handling of multi-byte glyphs and grapheme clusters | 🟥 | Prevents offset skew on emojis and international identifiers. |

---

## Subsystem 3: Relational AST Substrate (`RelationalAST`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 3.1 | Relational AST Node Block | AST node stored in `nio/mem` arena stamped with `TYPE_AST_NODE` | 🟥 | Direct integration with `vexspoke` memory architecture. |
| 3.2 | DOD Handle Topology | Nodes linked via `{pool_id, pool_index}` handles (`parent`, `first_child`, `next_sibling`) | 🟥 | Two-layer access cap (the Semantic Consistency Law (Access depth)) without pointer chasing. |
| 3.3 | BitPool AST Node Allocator | AST nodes claimed from dedicated `BitPool` in O(1) time | 🟥 | Zero malloc during file parsing. |
| 3.4 | Symbol Registration in `Variable` | Function, class, and variable definitions registered into `Variable` table | 🟥 | Symbols queryable via `Relational_search` spotlight. |
| 3.5 | Incremental Subtree Invalidation | Re-parses only modified syntax blocks without rebuilding full tree | 🟥 | Fast 120Hz typing response in `semicolon`. |
| 3.6 | Code Folding Boundaries | Computes foldable line ranges from block/scope AST nodes | 🟥 | Powers editor gutter folding arrows. |

---

## Subsystem 4: Syntax Highlighter & Text Styling Bridge (`Highlight`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 4.1 | Token-to-Style Mapping | Maps `TokenSpan` kinds to theme colors (syntax tokens) | 🟥 | Configurable syntax theme palette. |
| 4.2 | Darling `RichText` Adapter | Generates `RichSpan` runs for Darling UI text renderers | 🟥 | Direct feed into `darling` and `graphvex` SDF text pipeline. |
| 4.3 | Semantic Highlighting Overlay | Elevates token styles using AST symbol resolution (type vs variable vs macro) | 🟥 | Deep semantic syntax highlighting. |
| 4.4 | Gutter Annotation Generation | Line numbers, error marks, git diff markers, and folding indicators | 🟥 | Layout data passed to `semicolon` editor gutter. |
| 4.5 | Unified Diff Structural Classification | File headers, metadata, hunks, additions, removals, and context as shared token kinds | 🟧 | Strict C23 and ASan/UBSan owner pass; no source lexer composition, line map, or UI integration. |
| 4.6 | C23 Lexical Highlight Roles | Conservative presentation classification over `C23Lexer` spans: keyword/literal/bracket/comment roles preserved; identifiers refined into type, function, variable, member and macro; line-start `#include`/`#define` markers and names join the macro role, in-code `#`/`##` stay punctuation, and a well-formed `<...>` header path after `#include` is one string-role span while ordinary `<`/`>` keep operator roles | 🟩 | `tests/language/adapters/c/c23_highlights_test.c` via `python3 tests/language/run.py`: strict optimized C23/assertions and ASan/UBSan, ordered/non-overlapping spans, regular versus doc comments, include-header string/operator separation, Unicode boundaries, constructor arity/recovery, bounded projections. Lexical heuristic only: no parser, macro expansion, symbol resolution, parameters, diagnostics or consumer palette; semantic overlay remains 4.3. |

---

## Subsystem 5: Scope & Symbol Resolution Engine (`Scope`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 5.1 | Lexical Scope Stack | Block-level scope hierarchy (global, file, namespace, function, local) | 🟥 | Scoped identifier lookups. |
| 5.2 | Definition Lookup ("Go to Definition") | Resolves identifier under caret to declaration AST node | 🟥 | Instant jump to symbol declaration. |
| 5.3 | Reverse Reference Walk ("Find Usages") | Finds all AST nodes referencing a given symbol | 🟥 | Uses relational reverse index in `Variable`. |
| 5.4 | Document Symbol Outline | Extracts flat/tree list of classes, methods, and functions | 🟥 | Powers `semicolon` symbol outline and breadcrumb bar. |
| 5.5 | Auto-Completion Provider | Ranks visible symbols matching prefix at cursor | 🟥 | Fast sub-5ms completion popup feeding `darling` Menu. |

---

## Subsystem 6: Code Formatting & Indentation Engine (`Format`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 6.1 | Indentation Rule Evaluator | Computes expected indentation level based on AST depth and open braces | 🟥 | Configurable spaces vs tabs and indentation width. |
| 6.2 | On-Type Auto-Indent | Indents newly inserted lines on newline and closing braces | 🟥 | Seamless typing ergonomics. |
| 6.3 | Full Document Reformatter | Reconstructs clean source formatting from AST / token stream | 🟥 | Configurable line wrapping and operator spacing rules. |
| 6.4 | Selection Range Reformatting | Reformats selected line ranges without altering surrounding code | 🟥 | Localized formatting passes. |

---

## Subsystem 7: LSP JSON-RPC Client & Server Bridge (`LSP`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 7.1 | LSP JSON-RPC Protocol Framer | Reads/writes `Content-Length: ...\r\n\r\n{...}` messages | 🟥 | Stdio pipe communication using `net/json`. |
| 7.2 | Background Language Server Process | Spawns external LSP servers (`clangd`, `pyright`, `jdtls`) via `ProcessSpawn` | 🟥 | Non-blocking execution without freezing UI thread. |
| 7.3 | LSP Lifecycle Handshake | `initialize`, `initialized`, `shutdown`, `exit` sequence | 🟥 | Standard protocol handshake with capability negotiation. |
| 7.4 | Diagnostic Ingestion | Ingests `textDocument/publishDiagnostics` into relational error tables | 🟥 | Displays live red/yellow squigglies in editor canvas. |
| 7.5 | Workspace Symbol Queries | Dispatches `workspace/symbol` queries to external LSP | 🟥 | Cross-project symbol navigation. |

---

## Subsystem 8: Bootstrap Language Drivers: The Bootstrap Trio (`drivers/*`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 8.1 | C23 Grammar Driver (`lang_c`) | Full ISO C23 keywords, attributes `[...](#file--md)`, preprocessor directives | ⬜ | Core dogfooding driver for the entire `vexgraph` ecosystem. |
| 8.2 | Python Grammar Driver (`lang_python`) | Indentation-sensitive tokenizer (INDENT/DEDENT), f-strings, decorators | ⬜ | Powers scripting and tooling workbench in `semicolon`. |
| 8.3 | Java Grammar Driver (`lang_java`) | Class definitions, annotations, generics, enum structures | ⬜ | Completes the classic bootstrap language trio. |

---

## Subsystem 9: Graphics & Data Grammars (`drivers/*`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 9.1 | GLSL / SPIR-V Driver (`lang_glsl`) | Vulkan GLSL (#version 460), layout uniforms, vertex/fragment/compute stages | ⬜ | In-engine shader editing for `graphvex` and `anti`. |
| 9.2 | JSON & JSONC Grammar (`lang_json`) | High-speed JSON parser with comment support (JSONC) and error locations | ⬜ | Config files, theme files, and settings. |
| 9.3 | Markdown Grammar (`lang_markdown`) | CommonMark headers, tables, fenced code blocks, task lists | ⬜ | Powers `MarkdownPanel` in `darling` and documentation cards. |
| 9.4 | INI / VexConfig Grammar (`lang_ini`) | Key-value pairs and sections for `dictionary.ini` and engine configs | ⬜ | System config file editing. |

---

## Subsystem 10: Extended 30+ Grammar Ecosystem (`drivers/*`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 10.1 | Systems Grammars: Rust, Zig, Go, C++ | memory safety keywords, defer syntax, channels, templates | ⬜ | Full modern systems languages matrix. |
| 10.2 | Web Grammars: JS, TypeScript, HTML, CSS | JSX tags, CSS properties, DOM nesting, modern JS syntax | ⬜ | Web and scripting language support. |
| 10.3 | Scripting Grammars: Bash, Zsh, Lua, Ruby | Shell parameter expansions, Lua tables, regexes | ⬜ | Build script and automation editing. |
| 10.4 | Apple Grammars: Swift, Objective-C | Objective-C message syntax `[...]`, Swift optionals and guard | ⬜ | Native Apple application compilation without Xcode. |
| 10.5 | Database Grammars: SQL (Postgres/MySQL) | SELECT, JOIN, DDL, table constraints | ⬜ | In-IDE query editing for `darkbase`. |
| 10.6 | Tree-Sitter Seam Bridge | Optional foreign function bridge to borrow external Tree-sitter parsers | ⬜ | Instant coverage for esoteric or niche languages. |

---

## Defect Log & Seam Status

- **Status**: Initial C23 value-object scaffolding and a tested unified-diff structural line classifier exist in `../repos/language`. The grammar adapters, semantic analysis, project index, and LSP remain blueprint work.
- **Foundation targets, not runtime closure:** storage/bindings belong to [relational-engine](#file-relational-engine-md), with retained Vexspoke C APIs during migration. Host loading uses a supervisor seam, not R1 headers in this R3 driver. No current grammar/engine integration is implied.
- **Implementation Strategy**:
  1. Define L3 `LangModule` ABI and tokenizer contract.
  2. Implement C23 grammar driver (`lang_c.dylib`) to dogfood on `vexgraph` itself.
  3. Implement Python and Java drivers to complete the bootstrap trio.
  4. Wire the LSP JSON-RPC bridge for external language servers.

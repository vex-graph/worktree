# Vexgraph — Universal Architecture Preferences (compressed)

This is the author's live architecture preferences for the vexgraph ecosystem
(memory layout, ownership, tiering, validation, teardown, security, documentation,
proof). Not an AI prompt or a vibe-coding style guide. Full text + rationale:
`/PREFERENCES.md` (root, Git-ignored), published as
`preferences-full-documentation.md` in the Gist. Cite laws by **Title** (and clause
name in parentheses), never by number.

Greppable shape: `grep '^## '` lists every law, `grep '^### '` lists a law's
sub-sections, and each bullet is one atomic clause of that sub-section. Numbers
(`1`, `1.1`, `1.2`, ...) are positional only: they keep the list readable and are
never cited when you mean a law or a clause.

Read one law, never the whole file: `./tools/prefs list` is the law map, then
`./tools/prefs law 6`, `./tools/prefs section 6.4`, `./tools/prefs find "…"`,
`./tools/prefs repo <name>`. By hand the same slice is `grep -n '^## '` plus
`awk '/^## 6\. /{f=1} f&&/^## 7\. /{exit} f' /PREFERENCES.md`. The full
documentation says the same thing at `preferences-full-documentation.md` in the
Gist, with the same `N` / `N.M` headings; numbers are slice addresses inside
their own file, never identity.

The per-request block carries this file whole plus a **title index** of
`tests/test-preferences.md` and of every `<repo>-preferences.md`; their bodies are
not injected, so the index is not the rule. Before work in a repository read
`./tools/prefs repo <name>`. Before writing proof read
`./tools/prefs test "<law>"`. The index proves a lawbook exists; only the command
shows what it says.

## 1. Semantic Consistency Law

### 1.1 Reference form
* Never `->`.
* Field access is `(*ptr).field`.

### 1.2 Access depth
* At most two layers
* hoist deeper chains into a local.
* `(*level1).level2`. Thats it.

### 1.3 Control flow
* Single-statement body takes no braces.
* Single-statement body should have a space before the statement
* code below:
```c
if(foo) 
   doo();
```
* A statement should have one empty line before and after itself.
* Multi-statement bodies always use braces.

### 1.4 Cast and pointer spelling
* `nullptr` not `NULL` (its C23 Standard)
* one space after `)` in casts.
* `T *name`, `(T*) name`.

### 1.5 Function and field naming
* Regular: `ClassName_functionName(params);`
* field ops: `ClassName_fieldName_verb(params)`.
* Manifest exception: `MANIFEST_VERB(params)`

### 1.6 Construction and arity
* `Class(...)` macro
* `Class_add()` macro
* `Class_zero` macro
* named constants.

### 1.7 Value Return
* No caller-provided destination params
* return by value.

## 2. Single Class Per File Law (Java Law)

### 2.1 One public struct per file
* One public struct per `.h`/`.c`
* tag and typedef share the name.

### 2.2 Helpers and slot records
* Helpers private in `.c`;
* one SLOT RECORD co-location allowed.

### 2.3 Symmetric accessors
* Symmetric getters/setters for state-bearing fields;
* null-safe defaults.

## 3. Two-Semicolon Annotation Style Law

### 3.1 Annotation syntax
* Annotations carry two semicolons on the left only;
* marker expands to `_Static_assert`.

### 3.2 Rust spelling
* Rust uses `#[...]` attributes;
* C uses `;;ANNOTATION_NAME`.

## 4. Build & Naming Conventions Law

### 4.1 Compiler flags and casing
* `-Wall -Wextra -Werror`, C23 (`gnu23`);
* files lowercase, classes CapitalCase.

## 5. Git Workflow Law

### 5.1 Commit discipline
* Document → verify → commit locally → push only on explicit one-off instruction.

### 5.2 Commit granularity
* One class per commit;
* never bundle;
* never auto-push.

## 6. Vertical Integration Law (R1 > R2 > R3 > R4 > R5 > R6)

### 6.1 Boot and teardown order
* Boot bottom-up, teardown top-down: R1 host → R2 compute/storage → R3 drivers → R4 interfaces → R5 apps → R6 superapps.

### 6.2 Include allowlist
* Include allowlist is strict;
* lower tiers never include higher tiers.

### 6.3 Compose down, never rebuild
* R4 interfaces and R5 interactables / R6 superapps arrange what R1–R3 already own;
* a capability that exists below is referenced, never rebuilt beside it;
* two legal moves: reference the lower contract, or grow it in the tier that owns it;
* "make my own from scratch" is **not** one of them.
* No shadow owners: **never** re-implement storage, IO, transport, rendering, input, session or supervision;
* a duplicate is a defect even when its own tests pass.
* A wrapper may adapt names, defaults, handles or narrow a contract;
* it may not copy behavior and let the two drift;
* new behavior lands in the owner, never in the wrapper.
* A missing capability is built in the tier that owns it, then consumed;
* building it above because the lower change is inconvenient is the drift the allowlist forbids.

### 6.4 Application entry shape
* One `main` per application, at the top of its tier;
* each owned object is built by a file-local `create<Object>()` helper that returns it;
* the helpers are the bespoke layer: custom UI and custom algorithms assembled FROM lower-tier parts;
* `main` wires the objects, starts the application, ends it, returns `0`;
* the entry file composes tiers and holds no business logic of its own;
* objects are released in reverse creation order, detach before free, arena last;
* worked example: `main-template.c`.

## 7. One Type Registry Law

### 7.1 Project-scoped identity
* Type identity is project-scoped;
* full id = project byte + class number;
* bare id = vexspoke legacy.

### 7.2 Cross-project parents
* Cross-project parent chains registered via `Type_registerParents`.

## 8. Canonical Include Paths Law

### 8.1 Zero parent hops
* No `..`/`../..` hops;
* every include rooted at canonical subsystem dir.

## 9. Standalone Autonomy Law

### 9.1 Root owns build
* Only root owns CMakeLists.txt;
* standalone builds resolve real contracts;
* no per-repo CMake.

## 10. Living Documentation Law

### 10.1 Self-contained source files
* Every `.c`/`.m` self-contained via `;;OVERVIEW` and `;;DEFINITION`.

### 10.2 Same-cycle updates
* Preferences updated same cycle;
* readiness gist per repo.

## 11. Bounded Wait Law

### 11.1 No unbounded waits
* No unbounded waits on joined threads;
* explicit timeouts with drop-degrade.

## 12. AI-First Architecture Manifesto Law

### 12.1 Intentional extremes
* Zero arrow sugar
* single class per file
* explicit constructors
* vtable dispatch
* intentional AI-human pair programming manifesto.

## 13. Conflict Triage Law

### 13.1 Managed exceptions
* Managed exceptions, not vetoes;
* name tiers;
* propose indirection;
* patch prefs in-cycle.

## 14. Cold-Strict, Hot-Minimal Validation Law

### 14.1 Crash-guard split
* Cold paths validate exhaustively once;
* hot paths guard minimally;
* never log.

## 15. Data-Oriented Storage Law

### 15.1 Flat backing storage
* Flat index-based backing storage with OO class API.

## 16. Test Segregation Law

### 16.1 Zero source pollution
* No tests in production trees;
* tests live in `tests/<subsystem>/`.

## 17. No Section Sign Law

### 17.1 ASCII only
* U+00A7 forbidden everywhere;
* write "section" in plain ASCII.

## 18. Per-Repo Preferences Extension Law

### 18.1 Repo-local lawbooks
* Each repo has `<repo>-preferences.md` at root;
* inherits universal laws.

## 19. toString Law

### 19.1 Dual projections
* Every class ships `toString` (value)
* and `toStringStruct` (structure)
* cold-path only.

## 20. Authorial Intent Law

### 20.1 Provenance stamps
* Deliberate decisions stamped `// INTENTIONAL(vex):` at definition site.

## 21. No Hardcoding Law

### 21.1 Defaults not finals
* Constants are defaults, not final;
* growable storage;
* derive geometry;
* time from clock not frame count.

## 22. WHAT Law

### 22.1 void* receipt
* Every non-obvious `void*` carries `;;WHAT("<type>")` on the line above.

## 23. Cold-Only Reflection Law

### 23.1 Reflection is cold
* Reflection is cold-only;
* hot paths stay flat DOD;
* resolve once, hold the pointer.

## 24. Install Ledger Law

### 24.1 Machine-scoped record
* Machine-scoped install record outside the tree;
* uninstall keeps record.

## 25. Platform Support Floor Law

### 25.1 Minimum baseline
* macOS Apple Silicon arm64 / macOS 14+;
* Windows 10+;
* `-mcpu=apple-m1` baseline.

## 26. Capability Gating Law

### 26.1 Runtime probing
* Runtime-probed capabilities;
* probe once cold, cached bitset, stated fallback.

## 27. THROW Law

### 27.1 Loud cold rejection
* `THROW(fmt,...)` → `[vex] file:line: msg` to stderr;
* caller returns safe default;
* no unwind.

## 28. Native Pixel Law

### 28.1 Hardware pixels
* All dimensions/input in native hardware pixels;
* platform points encapsulated at boundary.

## 29. Timestamped Test Checklist Law

### 29.1 Evidence ledger
* `/test-checklist.md` is the per-file automated lab evidence ledger;
* only executable tests inventoried.

## 30. Feature Implementation and Adversarial Proof Law

### 30.1 Full cycle
* Inspect → implement → attack contract → execute/repair → close with evidence.

## 31. Transparent Competency Law

### 31.1 Live documentation
* Every tracked `.md` is a live statement of current competency;
* `## Current State` + `## Scope and Limitations`.

## 32. Groundedness Law

### 32.1 Read before assess
* No claim without reading the source;
* report read boundary.

## 33. Exhaustion Loudness Law

### 33.1 Loud refusal
* Finite-storage refusal: THROW once per epoch, queryable count always;
* epoch reset clears.

## 34. Voice Preservation Law

### 34.1 Preserve voice
* Author's voice in comments/docs preserved verbatim;
* cleanup excludes voice.

## 35. Value Return Law

### 35.1 No destinations
* No caller-provided destination params
* return by value.

## 36. Security Baseline Law

### 36.1 Access not obscurity
* Access not obscurity;
* no secret in code;
* untrusted input validated at cold seam;
* model output is data;
* refusals counted;
* delays governed;
* honest policy.

## 37. Relational Memory Law (No malloc, No free)

### 37.1 One owner
* The relational engine owns every runtime byte the ecosystem allocates;
* `Memory_alloc`, `MemoryArena_alloc` and `Transient_alloc` are the only allocation entry points;
* no repository keeps a second general-purpose allocator beside it.

### 37.2 The ban
* `malloc`, `calloc`, `realloc`, `free`, `strdup`, `strndup`, `posix_memalign`, `aligned_alloc` and `alloca` appear nowhere in ecosystem source but the engine's own allocator implementation;
* Rust `Box`, `Vec` and `String` are not a second heap: ecosystem storage that outlives its statement or crosses a seam lives in engine memory;
* `grep -rn` is the audit; a hit outside the owner is a defect, not a style choice.

### 37.3 Self-describing blocks
* every block carries the 32-byte header: id, hash, length, pointer;
* an address names its own project and class without a registry lookup;
* there is no untracked heap block, so there is no untracked free.

### 37.4 Arena lifetimes
* the master arena holds process-lifetime objects and resets last (`Memory_freeAll`);
* the transient arena holds frame and scratch memory and resets at the frame boundary (`Transient_reset`);
* secondary arenas are isolated ownership domains, created and destroyed by their owner (`MemoryArena_create`/`MemoryArena_destroy`);
* `freeAll` invalidates every block in its arena at once.

### 37.5 Release is ownership
* `Memory_free` returns a block to its slab in O(1);
* a block is freed exactly once, by its owner, and never after its arena's `freeAll`;
* a borrowed block is never freed by the borrower;
* reallocation moves the block and frees the old address (`Memory_realloc`).

### 37.6 Hot paths allocate nothing
* steady-state frames and callbacks allocate zero bytes;
* growth is cold, then the hot path reads the resolved pointer;
* an allocation on a per-frame path is a defect, not a tuning choice.

### 37.7 Refusal is loud
* a refused allocation returns `nullptr` and reports once per epoch;
* the count is queryable (`Memory_exhaustionCount`, `MemoryArena_exhaustionCount`, `Transient_exhaustionCount`);
* there is no untracked heap fallback.

### 37.8 What is not a block
* OS and driver resources (mappings, IOSurface, Vulkan/Metal handles, dylib images) belong to the tier that acquired them and are released there;
* they are never routed through a second general allocator and never counted as heap blocks;
* third-party library internals are outside this law; the seams we own are not.

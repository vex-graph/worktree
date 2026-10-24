<!--
PROPOSAL — not yet canonical. Compressed draft of /PREFERENCES.md for review.
If approved as written, this text replaces /PREFERENCES.md and is republished
verbatim to the existing Gist (Canonical File & Gist Publication); remove this
comment on replacement. Every law Title, clause name, Tier-1 number and API
spelling is preserved; rationale prose, duplicated tables and decorative
examples are condensed; legacy title maps moved to the appendix.
-->

# vexgraph — C23/Rust Ecosystem & Multi-Repo Preferences

The engine is a relational system where **everything is a pointer**. These laws are hard requirements, not suggestions. This is the **Universal Supreme Constitution** governing all repositories across the vexgraph ecosystem; repo-local slices are codified in per-repo `<repo>-preferences.md` files (the Per-Repo Preferences Extension Law).

## Canonical File & Gist Publication

- The universal constitution is one real, Git-ignored `/PREFERENCES.md` in the workspace — not a symlink, not a tracked file in vexspoke. Its published canonical edition is [preferences.md on GitHub Gist](https://gist.github.com/vex-graph/4132a6c45cb6d3797c3e8eff2e94035a) (unlisted, not private). The local file stays available offline and loads into session context.
- Whenever this file changes, upload the complete current file to that same Gist in the same work cycle, then verify the downloaded content matches:

```sh
gh gist edit 4132a6c45cb6d3797c3e8eff2e94035a metadata/PREFERENCES.md
```

- The author authorizes updates to this existing Gist only — never a repository push or publication of other files. Do not create a replacement Gist for ordinary updates. Repo-local preferences and test evidence follow the Git Workflow Law. Legacy paths referring to the universal constitution resolve to workspace `/PREFERENCES.md`; standalone checkouts obtain it from the linked Gist.
- Gist-owned local sources live only under `/`: `PREFERENCES.md`, `metadata/gists/test-checklist.md`, `metadata/gists/BLOCKERS.md`, `readiness/<repo>.md`. Published Gists keep their identities and filenames. These sources stay Git-ignored; publication plus downloaded-content verification record them, never a tests-repo ledger commit. Executable tests and test laws remain in `tests`; local lawbooks remain in their owning repositories. No duplicate root constitution or tracked tests checklist exists.
- Lifecycle is R1 → R2 → R3 → R4 → R5 → R6 (boot), and R6 → R1 (teardown). R1–R4 never include R5/R6 headers; R5 never includes R6 headers; no lower tier includes R6 code. R6 superapps (`anti`, `semicolon`) live under `superapp/`, compose R1–R5 public contracts, and supervise app-level workflows without owning OS, memory, driver or interface implementations. Primeagen remains standalone R5; Semicolon inclusion is a future consumer seam, not a reverse dependency.
- Determinant at `drivers/determinant` is R3: reusable terminal-cell rendering, widgets, CLI parsing and caller-fed terminal input. Its complete local lawbook is `drivers/determinant/determinant-preferences.md`. It borrows R2 public contracts only, exposing opaque/callback seams to R1 and consumers. Vexspoke's bare one-line output remains R2 — never terminal-screen ownership, never a reverse R2→R3 call. Terminal coordinates are cells; the Native Pixel Law still governs graphical surfaces. Reloadable view/command code borrows resident terminal/host state, with admission paused and active users excluded before swap or retirement. Toolkit extraction is not Primeagen reload proof.

## The Law Identity Doctrine (Title Over Number)

**A law is its Title, never its number.** The integer before a section heading is a positional ordinal: it keeps the document readable and nothing more. It is never cited; it may change any moment as laws are inserted, promoted, split or merged. Citations pinned to an active Title survive renumbering. A deliberate merge records former Titles as historical aliases; new citations use the replacement Title and its named clause. **Never quote a number when you mean a law** — code annotations, `;;OVERVIEW` headers, READMEs, `_docs/*` and commit messages all cite the Title:

```c
;;INTENTION("per the Single Class Per File Law + the Living ;;OVERVIEW Blueprint Law")
```

Sub-numbering is abolished. There are no fractional (`n.n`) laws; anything that once carried one is now a whole law with its own Title and ordinal. The literal `n.n` notation is a defect on arrival.

## The Law Index (Canonical Titles)

The only authoritative list of law names. One canonical Title per active law; ordinals may move. Deliberate merges retire old titles with alias records in the replacement law.

1. Semantic Consistency Law
2. Single Class Per File Law (Java Law)
3. Two-Semicolon Annotation Style Law
4. Build & Naming Conventions Law
5. Git Workflow Law
6. Vertical Integration Law — Single Order To Follow (R1 > R2 > R3 > R4 > R5 > R6)
7. One Type Registry Law (Project-Scoped Identity, Uniform Per-Project Numbering)
8. Canonical Include Paths Law (Zero Parent Hops)
9. Standalone Autonomy Law (Target Seam)
10. Living Documentation Law
11. Bounded Wait Law (No Unbounded Waits on Joined Threads)
12. AI-First Architecture Manifesto Law
13. Conflict Triage Law — Managed Exception, Not Veto
14. Cold-Strict, Hot-Minimal Validation Law (Crash-Guard Split)
15. Data-Oriented Storage Law & Object-Oriented Ergonomics
16. Test Segregation Law (Zero Source Pollution — No Tests in Source Trees)
17. No Section Sign Law
18. Per-Repo Preferences Extension Law
19. toString Law (Every Object Has a String)
20. Authorial Intent Law
21. No Hardcoding Law
22. WHAT Law
23. Cold-Only Reflection Law
24. Install Ledger Law (Machine-Scoped Install Memory)
25. Platform Support Floor Law (Apple Silicon macOS 14+, Windows 10+)
26. Capability Gating Law (Runtime Features Above the Floor)
27. THROW Law (Loud Cold Rejection)
28. Native Pixel Law
29. Timestamped Test Checklist Law
30. Feature Implementation and Adversarial Proof Law
31. Transparent Competency Law
32. Groundedness Law (Read Before You Assess)
33. Exhaustion Loudness Law (No Silent Exhaustion)
34. Voice Preservation Law (The Author's Voice Is Not Yours to Edit)
35. Value Return Law (No Caller-Provided Destinations)
36. Security Baseline Law

## Tier Map (Conflict priority: Tier 1 > Tier 2 > Tier 3)

The Semantic Consistency Law spans semantic access/construction/call ordering (Tier 2) and syntactic spelling/naming (Tier 3); the Index lists it once and both tiers apply to its clauses.

- **Tier 1 — critical invariants** (crash/leak/deadlock/memory/thread safety; violations are segfaults, leaks, lockups, codebase pollution): Single Class Per File (core) · Build & Naming · Platform Support Floor · Capability Gating · THROW · Exhaustion Loudness · Vertical Integration (teardown) · Bounded Wait · Cold-Only Reflection · Cold-Strict crash-guard half (never crash/block/allocate/use-after-free) · Test Segregation · Native Pixel. Commit granularity is Git-Workflow documentation policy, not a memory-safety invariant.
- **Tier 2 — semantics, object models, living contracts** (relational memory layout, OO encapsulation in C23, symmetric introspection, self-documenting contracts): Semantic Consistency · Single Class Per File (symmetric accessors) · Living Documentation · Transparent Competency · Groundedness · Timestamped Test Checklist · Vertical Integration (R1–R6 order) · One Type Registry · Canonical Include Paths + Standalone Autonomy · toString · Authorial Intent · No Hardcoding · WHAT · AI-First Manifesto · Conflict Triage · Cold-Strict contract half (setters/getters/seam tests) · Data-Oriented Storage · Per-Repo Preferences Extension.
- **Tier 3 — syntactic aesthetics, mechanical determinism** (un-ambiguous, machine-readable syntax): Semantic Consistency (reference form, control flow, cast/pointer spelling, naming) · Two-Semicolon Annotation Style · No Section Sign.

## Repository Preferences: Mandatory Reading Chain

Read constitution → owning repo lawbook → applicable test laws and current checklist → existing implementation. Per the Per-Repo Preferences Extension Law and the Feature Implementation and Adversarial Proof Law; cross-repo work follows the chain for every changed repository and also reads dependency contracts affecting the seams. Do not apply one repo's exclusive rules to another. Unavailable dependency checkouts or missing local lawbooks are reported as explicit gaps, never exemptions; `darling-framework` and the R6 superapps have no lawbooks yet. Any repo gaining a lawbook adds itself to this table in the same cycle.

Personal tooling is not an extra R tier. `func` at `personal/func` is the standalone compile-time opcode orchestrator: numeric operation IDs and declared arities lower to native artifacts, no shipped VM; its local lawbook owns that forward contract; Harness may invoke `func`/`b` as bounded tools, never include their internals; tool invocation grants no permission to execute, upload or publish unrelated work. Primeagen is the personal standalone R5 CLI at `personal/primeagen`, outside the ecosystem tree; its lawbook owns all standalone consumer-adapter exceptions (Python host, HTTPS/OpenCode consumption, `tools/` consent adapters) without moving ecosystem transport, connector or IO/NIO ownership; offline owner evidence is never live provider or full integration proof; model output never grants consent, and Always yes is exact-tool/arguments, process-local, never blanket permission.

| Repository | Workspace path |
| :--- | :--- |
| vexspoke | `host-behavior/vexspoke/vexspoke-preferences.md` |
| relational-engine | `host-behavior/relational-engine/relational-engine-preferences.md` |
| hotcwap | `host-behavior/hotcwap/hotcwap-preferences.md` |
| graphvex | `drivers/graphvex/graphvex-preferences.md` |
| api-haven | `drivers/api-haven/api-haven-preferences.md` |
| determinant | `drivers/determinant/determinant-preferences.md` |
| language | `drivers/language/language-preferences.md` |
| darkbase | `drivers/darkbase-engine/darkbase-preferences.md` |
| darkbase-headless | `interfaces/darkbase-headless/darkbase-headless-preferences.md` |
| samplerate | `drivers/samplerate/samplerate-preferences.md` |
| sesh | `interfaces/sesh/sesh-preferences.md` |
| harness | `interfaces/harness/harness-preferences.md` |
| func | `personal/func/func-preferences.md` |
| primeagen | `personal/primeagen/primeagen-preferences.md` |

## Semantic Consistency Law

One canonical dialect makes references, access depth, control flow, spelling, naming, calls and construction predictable across repositories. These are binding clauses of **one** law, not separate laws; a clause name identifies the specific check, cited as `Semantic Consistency Law (Access depth)`.

### Reference form

Never `->`. Field access is always `(*ptr).field`: `(*this).x = 5;` yes, `this->x = 5;` no.

### Access depth

A member/index chain touches at most two layers: `(*layer1).layer2` yes; `(*p).items[i]` yes (indexing rides on its base hop); `(*(*ptr).field).field2` and three-deep dot chains no. Anything deeper hoists an intermediate into a local first (`Field *f = &(*layout).items[i];` then `(*f).offset`).

*Rationale:* a Java-style reference is a pointer, not an inline struct. Physical access is one level + offset — exactly `(*ptr).field`, `base_address + field_offset`. Bounded, explicit hops keep every memory hop deliberate, visible in registers, and impossible to overlook.

### Control flow

An `if`, `while` or `for` whose body is one statement takes no braces; the statement sits on the next line. This concerns the body, not the number of condition expressions:

```c
if (foo)
    (*coo).doo(params);
for (size_t i = 0; i < count; ++i)
    visit(i);
```

Multi-statement bodies always use braces.

### Cast and pointer spelling

Owned C23 and Objective-C source uses `nullptr`, never `NULL`. Fixed protocol/API sentinels (`VK_NULL_HANDLE`, numeric zero, Objective-C `nil`) and third-party/attic source are unchanged. Strings and comments are not code tokens. No fallback macros for C23's native `nullptr`, `bool`, `true`, `false` — builds select the C23 dialect. Variadic calls still pass the pointee type the API contract promises, via an explicit cast where needed.

A cast has exactly one space after `)`: `(uintptr_t) ptr` yes, `(uintptr_t)ptr` no. Pointer declarators are `T *name` — one space before `*`, `*` binds to the name, no space after: `Buffer *buf`, `void *Memory_alloc(uint32_t t, size_t n)`. Casts are the sole exception: `(T*) var` — no space before `*` inside the parens, e.g. `(Block*) (aligned - HEADER_SIZE)`, `(int64_t*) addr` (deref casts too). Function pointers follow declaration spacing: `char **argv`, `void (*fn)(void *arg)`. Star binds to the name in declarations, to the type inside cast parens.

### Function and field naming

The symbol is lowercase camelCase; it is called as `ClassName_functionName(params)`:

```c
static uint32_t ticket(uint64_t thread_id) { ... }   // definition
uint32_t t = SpinLock_ticket(0);                      // class operation
```

A new operation on a named field or sub-part uses `ClassName_fieldName_verbVerbName(...)` (`fieldName` lower camelCase, verb first); an operation on the class as a whole uses `ClassName_functionName(...)`. A field-specific name never changes ownership or permits field piercing; repo-local part contracts may be stricter. Existing ABI symbols are never renamed by any documentation change.

### Construction and arity

Every class ships a uniform constructor macro so an object is instantiated with the class name `Object(...)` — never numbered constructor arms or bespoke factories — and every framework speaks one direct construction form.

1. **`Class(...)` every time.** The macro picks the matching implementation by argument count. Numbered arms (`Class_0()`, `Class_1(a)`) are implementation details only, never in examples or call sites. Construction is never a bespoke `make_*` / `new_*` / `create_*`.
2. **`Class_add(...)`.** Every additive or collection class provides its natural additive verb (list add, vector add, set union, string append, …).
3. **`Class_zero()`** (or a `ZERO` constant) — the additive identity / empty element.
4. **Canonical named constants in one header.** Numeric magnitudes and extremes are named once (`ZERO`, `ONE`, `ONE_MILLION`, `ONE_BILLION`, `ONE_TRILLION`, `FLOAT_POS_INF`, `FLOAT_NEG_INF`, `DOUBLE_POS_INF`, `DOUBLE_NEG_INF`, `INT_MAX_VALUE`, `INT_MIN_VALUE`, `TYPE_MAX_VALUE`, `TYPE_MIN_VALUE`, and more), so a call site writes `-ONE` instead of a bare `-1`.

*Rationale (Tesler's Law):* inherent complexity cannot be deleted, only paid once — here, in the library, so call sites never invent factories or spellings.

The rule is universal: every public class ships the macro; additive classes ship `add`; every class ships `zero`; constants live in one header with no bare `-1`, `1000000`, or `INFINITY` at call sites; identical names and shapes across repos (the Per-Repo Preferences Extension Law restates it, never forks it).

### Value Return Law

**Functions never take a caller-provided destination parameter** — not first, last, or middle, not named `dest`, `out`, `result` or any alias, for every operation including getters, projections, formatters, parsers and buffer-writing APIs. Ordinary local assignment is fine: a function returns its value and the caller stores it. Related results travel together in a named value record. One-call operations with no useful result are called directly. Setters and state-changing operations are called directly on the object being changed; an argument is never supplied merely to receive the result.

```c
vec3 whatever = vec3_add(x, y);                 // yes
whatever = vec3_add(whatever, x);               // yes
float x = vec3_getX(vec);                        // yes — getter yields the value
Position position = Window_getLocation(window); // yes — related values in a record
const char *event = AiSse_getEvent(stream);     // yes — borrowed view returned
Class_function(params);                          // yes — direct call
Vec3_add(&sum, x, y);                            // no — output destination
float Vec3_getX(const Vec3 *self, float *dest);  // no — getters return values too
void Vec3_add(const Vec3 *a, const Vec3 *b, Vec3 *dest); // no — dest-last forbidden too
```

Every existing destination-based API is nonconforming and must migrate, together with every caller and test. A cookbook noting an unmigrated signature records a migration blocker — evidence of unfinished work, never a legacy exception. Do not preserve a destination by moving or renaming it `out`. If a result cannot be returned by value or as a documented borrowed view, define an owned result type with explicit lifetime and release semantics.

## Single Class Per File Law (Java Law)

A class is `typedef struct Class {} Class;` — same name for tag and typedef (`typedef struct _spin_lock {...} SpinLock;` is a defect). One public class struct per `.h`/`.c` pair; the file name is the lowercase class name (`spin.h`/`spin.c`, `hot_module.h`/`hot_module.c`). A second public `typedef struct` in the same file is a defect, however small — split it. One problem in one file stays in one file.

The sole exceptions stay private in the owning `.c`, never included by another file:

- **Private file-local helpers:** `static` structs with no behavior, or pure-data sub-records with no `Class_*` functions. The overview MUST list each helper with its full field list (type, name, one-line role) under `PRIVATE HELPERS` — same detail as the main class. Anything with behavior (`trampoline_register/get/set`, `hot_retire_handle`, `find_module`, …) is a class with its own file pair.
- **SLOT RECORD (one co-location allowed):** a behaviorless row/entry struct owned by exactly one class (its table/ring/pool) may live in that class's file pair, documented as `SLOT RECORD`, with zero `Class_*` functions of its own — all behavior hangs off the owning class (`HotTrampoline` row vs `HotTrampolineTable`, `HotRetiredHandle` vs `HotRetireRing`). Two classes with behavior never share a file; one class plus its dumb slots may.

The overview's `STRUCT FIELDS` mirrors exactly the file's own class — the struct matching the file name — field-for-field, in declaration order. No foreign class fields there; kept helpers live only under `PRIVATE HELPERS`.

### Symmetric accessors

In darling and high-level class abstractions, every state-bearing field provides complete, symmetric getters and setters, like an idiomatic Java/C# library; a consumer never manually pierces internals or breaks the Access depth cap to read simple state:

1. **Mutators:** `void Class_set<Prop>(Class *self, <Type> val)`.
2. **Scalar/pointer accessors:** `<Type> Class_get<Prop>(const Class *self)`.
3. **Boolean accessors:** `bool Class_is<Prop>(...)` or `bool Class_has<Prop>(...)`.
4. **Multi-value accessors** return a named value record by value (`Crop Class_getCrop(const Picture *self)`).
5. **Null-safety:** all getters defensively return safe defaults for a null `self` (`nullptr`, `0`, `false`, `0.0f`).

Older references to *Symmetric Getter/Setter Completeness Law* mean this clause.

## Two-Semicolon Annotation Style Law

Annotations (`src/annotation/*.h`) carry two semicolons on the left only — plain null declarations; the marker macro expands to a `_Static_assert` validating the annotation text:

`;;OVERVIEW` `;;DEFINITION` `;;GETTER` `;;SETTER` `;;DRAFT` `;;INCOMPLETE` `;;PLATFORM_EXCLUSIVE("Windows")` `;;INTENTION("reason")` `;;INHERITS("Base")` `;;REACTIVE("objectName")` `;;WHAT("uint64_t")` `;;SECURITY("reason")` `;;FREEZE("reason")` `;;CHECKER` `;;HOTCODE` `;;DEBUG` `;;TEST`

In Rust (the R2 storage engine) the same marker set is expressed as real attributes through a zero-dependency proc-macro crate — never lookalike comments: `#[overview]` `#[definition]` `#[getter]` `#[setter]` `#[draft]` `#[incomplete]` `#[platform_exclusive("Windows")]` `#[intention("reason")]` `#[inherits("Base")]` `#[what("u64")]` `#[checker]` `#[hotcode]` `#[debug]`. Only the spelling differs: C uses `;;NAME` (`_Static_assert`-backed), Rust `#[name]` (proc-macro passthrough that validates its argument and compiles to nothing at runtime). `//! DEFINITION:` / `//! OVERVIEW:` doc comments are prose, not annotations. `REACTIVE` and `INHERITS` are C-only spellings.

- `;;CHECKER` is an optional source marker for an existing cold validator, not a mandatory runtime checker; it expands to a compile-time assertion with no runtime work, and tests prove the actual validation and safe error result. Never compile out validation protecting an external or unsafe boundary.
- `;;HOTCODE` is an optional marker for a measured hot path, not proof of branch count or allocation behavior; it has no runtime work, and a registered test must establish the claimed hot-path properties.
- `;;DEBUG` marks a function, field or entry point that exists to observe, diagnose or inspect — no production semantics. A DEBUG surface may be compiled out (e.g. under `#if defined(DEBUG_BORROW_CHECK)`), may be slow, may print, and is never part of the shipped contract. Production code may call one only on a failure or inspection path: the success path never depends on it, and no correctness decision rests on its result. A load-bearing DEBUG surface is a mis-annotation — promote it to a real API. `grep -rn ';;DEBUG'` lists every surface a release build may drop.
- `;;TEST` marks a function or field existing so a test or tool can observe or drive a class — internal-state getter, probe, reset hook. A test/inspection affordance, not a production necessity: no production path may depend on one for correctness; a load-bearing `;;TEST` is a mis-annotation — promote it to a real API. It is normally still compiled in and some callers may use it. `;;TEST` is C-only in spelling (Rust already reserves `#[test]`; the Rust form is the built-in attribute). The marker is available from the shared `tests` repository as well as `src/`, so `grep -rn ';;TEST'` covers both.

## Build & Naming Conventions Law

- `-Wall -Wextra -Werror`, C23 (`gnu23`). Shipped Apple Silicon targets use the minimum compatible CPU baseline (`-mcpu=apple-m1`); `-mcpu=native` only for an explicitly local, non-shipped build (Platform Support Floor Law). Newer features are Capability Gating Law, never baked into the baseline.
- Files lowercase (`variable.c`, `spin.h`); classes CapitalCase.
- Structs act as classes: state lives on the struct, behavior in `ClassName_functionName(struct Class *self, ...)`.

## Git Workflow Law

Document → verify → commit locally in the owning repository → push only on an explicit, one-off instruction. No step implies permission for the next, except as stated below.

1. **Document and verify the completed work cycle.** Record what changed, why, and the verification actually performed — in code, tests, relevant docs, or the commit message. Build applicable targets with `-Wall -Wextra -Werror`; run relevant tests before calling work complete. Never claim tests that did not run. The Living Documentation Law owns same-cycle updates; the Feature Implementation and Adversarial Proof Law owns implementation-to-proof.
2. **Commit per class in its own repository.** Each changed class gets its own local commit with its `.c`/`.h` pair (plus platform implementation where applicable), including its updated blueprint. Never bundle multiple classes because they depend on each other. Header-only and implementation-only units get their own records. Tests, shared build wiring, configuration and documentation are separate owning-file records when they cannot belong to that class in the same repository. Commits record updates per class or document and do not need to form an independently buildable, bisectable stream; a class commit may depend on another's work-cycle commit — document it and verify the integrated final state. Never stage unrelated pre-existing edits; never treat the local-only umbrella as the owning sub-repository.
   - **Explicit one-time documentation batch exception:** when vex expressly directs a documentation-only sweep grouped by directory, edits in each affected source directory may ship as one directory-scoped local commit even when documenting multiple classes. No behavior, build or test changes ride along; the exception does not itself authorize a push.

   ;;INTENTION("vex expressly authorized this one-time documentation-only directory batch to avoid unnecessary commit-count growth; behavior changes remain excluded.")
3. **Commit dependent work upstream-first.** `relational-engine` → `vexspoke` (when it consumes the engine ABI) → `graphvex`/`api-haven`/`language`/`darkbase`/`samplerate` → `hotcwap` → `darling-framework`/`sesh`/`harness` → R5 applications → R6 superapps. Each changed repository gets its own local commit.
4. **Scope the message locally.** Name the class, subsystem or seam — `feat(cursor): ...`, `fix(label): ...`, `test(mesh): ...` — never the repository name within the repository.
5. **Never auto-push.** Only an explicit instruction authorizes a single push of the requested repositories; then the no-push default resumes. Documentation, passing tests and local commits never grant push permission.
6. **Shared tests-repo batch exception.** The shared `tests` repository commits a battle-tested assessment as one batch commit — many test files assessed together ship in a single `test(<subsystem>): ...` commit; commit count never scales with file count in `tests`. Per-file monitoring lives in the Git-ignored `/test-checklist.md` (Timestamped Test Checklist Law) and the owner tests, never in commit granularity; the checklist is published and byte-verified in its existing Gist, never staged in `tests`. This exception is scoped to the shared `tests` repository only; every per-class production repository commits per class.

Older names — *Cohesive Commits Law*, *No Auto-Pushing Law*, *Commit and Push Discipline Law*, *Multi-Repo Atomic Commit Discipline Law*, *Per-Repo Commit Message Scope Law* — refer to this law.

## Vertical Integration Law — Single Order To Follow (R1 > R2 > R3 > R4 > R5 > R6)

The stack has ONE lifecycle order: boot from the bottom up (R1 → R2 → R3 → R4 → R5 → R6), tear down from the top down (R6 → R1). A lower R boots earlier, stays alive while borrowers exist, and tears down later. R ranks describe supervision and lifetime, **not the direction of header includes** — that direction is fixed by the allowlist below.

**The tiers:** R1 host (`hotcwap`) supervises everything · R2 computation + storage (`vexspoke` + `relational-engine`) · R3 drivers (`graphvex` | `api-haven` | `language` | `darkbase` | `samplerate` | `determinant`) · R4 interfaces (`darling-framework` | `sesh` | `harness`) · R5 interactables (`primeagen` | `impedance` | `darling-editor` | `drawling`) · R6 superapps (`anti` | `semicolon`) · `vexgraph` umbrella integrator (unified binaries, probes `../../_trash/main/vk_test.c`, tooling).

### Allowlist (only these includes are permitted; anything else is a defect)

- **R2 split of ownership.** Vexspoke owns CPU computation, math, algorithms, synchronization, behavior APIs, network protocols under `net/` (BSD-socket HTTP client and micro-server), and system capability probes (`AppDetect`, `CaptureTool`, `ProcessProbe`). The engine owns filesystem IO/NIO, memory allocation/storage (including the default production Memory C implementation), stable row chunks, variable bindings, native C search over Rust-owned spans, and Rust storage. The authorized IO/NIO migration makes `src/io` and `src/nio` the production owners of the existing File/Cache/VexHome and Memory/MemoryArena/Transient C ABI; canonical `io/...` and `nio/...` includes resolve from the engine; the default production build links that implementation, not an opt-in parallel allocator. Native C allocator behavior and existing per-project type IDs are preserved — not rewritten in Rust or replaced by Rust typed pools. Vexspoke consumes the engine-owned production IO/NIO C ABI and the engine-owned type algebra (`type/type.h`); it does not own them. The shared type-id algebra is engine-owned, and so is the 32-byte block header.
- **Pure format algorithms live in vexspoke** as byte-in/byte-out code that owns no file, handle or device: the JSON and URL parsers, and `image/`'s PNG → RGBA8 decoder (system zlib for DEFLATE; interlaced/16-bit/palette/sub-8-bit streams reject plainly, every chunk CRC-verified). The caller supplies the bytes (the engine's File reads them) and receives an engine-backed RGBA buffer the engine owns, so callers hold a stable pointer rather than a copy. Image *decoding* is distinct from image *composition* (Graphvex R3 owns upload/sampling and never decodes) and from terminal *rasterisation* (Determinant R3 turns pixels into cells).
- **R2 `relational-engine`** may borrow Vexspoke CPU-only contracts (synchronization, crypto, constructor/annotation seams) — never R1/R3/R4/R5 headers, no duplicate storage implementation, no recursive build target edge. Imported reflection/relational comparison code is not a production dependency closure. R1 keeps engine code/storage resident across consumer reloads and excludes active readers/writers before destruction. Whole-value replacement is not automatic record-schema migration; such migration requires staged validation, rollback and owner proof. No C/Rust atomic-layout compatibility is assumed.
- **R2 `vexspoke`** consumes the production IO/NIO ABI and the algebra; no R1/R3/R4/R5 includes.
- **R3 `graphvex`** borrows vexspoke and/or relational-engine public contracts; never `hotcwap`/`darling`/`api-haven`/R5 headers. GPU shaders, dispatch and synchronization remain R3-owned.
- **R3 `api-haven`** borrows R2 public contracts, no graphics; may define pure connector contracts — descriptor registries plus fn-pointer client shapes (e.g. `AiProvider`, `DbProvider`, `McpServer`; `AppDetect`/`CaptureTool`/`ProcessProbe` live in vexspoke R2 and are consumed, never re-implemented) — with zero vendor/database includes; contract class names never collide with owner interfaces (the `Database` interface stays with darkbase). MCP tool/resource surfaces (stdio JSON-RPC engines and their `mcp_server` runners) are connector-shape hosting; they host handler closures over those registries/probes only — no exec, no writes, no vendor SDKs.
- **R3 `language`/`darkbase`** borrow R2 contracts (+ `graphvex` for GPU-backed ones); never R5 engines or R1/R4 headers.
- **R3 `samplerate`** borrows R2 contracts plus `graphvex` for GPU-backed audio compute; its native audio platform backend (CoreAudio/WASAPI/ALSA) lives in-repo; never R1/R4/R5 headers. The DAW application `impedance` (R5) consumes samplerate; samplerate never includes it.
- **R3 `determinant`** borrows R2 public contracts only; no R1/R4/R5/R6 headers. Exposes opaque/callback host seams, no competing OS process or allocator. Bare R2 output stays separate; no reverse R2 call.
- **R1 `hotcwap`** includes `relational-engine` (memory/IO), `vexspoke` (event/input/time) + `graphvex` (buffer/GPU). Never `darling`/`api-haven`/database/language/R5 headers.
- **R4 `darling-framework`** includes `relational-engine` (memory/IO), `vexspoke` + `graphvex` + `hotcwap` (`window/window.h`). Never `api-haven`/R5 engines.
- **R4 `sesh`** includes `relational-engine` (memory/IO), `vexspoke` + `api-haven` (`WsFanout`). Never graphics engines.
- **R4 `harness`** borrows `relational-engine` (memory/IO), `vexspoke`, `api-haven` (connectors, consumed as-is), `darling-framework` for interface; drives the user's projects, external tools and R5 applications through registered seams (opaque handles + fn-tables); invokes the personal `func`/`b` as bounded tools, never includes. Never included by R1/R2/R3; never includes R5 headers.
- **R5 engines** (`primeagen`, `impedance`, `darling-editor`, `drawling`) borrow R1/R2/R3/R4 public shapes; own no OS/window/memory management. Standalone-capable or Kernel-registered; never include R6 headers.
- **R6 superapps** (`anti`, `semicolon`) compose R1–R5 public contracts and registered workflows without absorbing lower-tier implementations; lower tiers never include R6 headers or code.

**Arrow reading (the only two directions):** `supervises ▼` (runtime): R1 boots R2, loads R3 dylibs, registers R4 UI and R5 apps; R6 composes admitted app workflows; teardown runs top-down in reverse under the same law. `borrows shape ▲` (compile-time): a file may only `#include` allowlist shapes; a leaf never borrows supervisor shapes. `registers ◀` (engines): R5 is never `#include`d by R1 — R1 holds `void*` + per-kind fn-tables (`ProcessEntry`, `AppRunFn`/`AppTickFn`/`AppHotReloadFn`, `ConsoleIo`, `HotModule`), same feature, no circular link, standalone stays green (Standalone Autonomy Law). Windowed Applications register a frame-handler frame-client into graphvex's `GfxLoop` — opaque handle + callback, never an `#include`.

**R2 Reactive (per-variable event emitter):** atomic payload + dirty flag, so `Reactive_set` is safe from ANY thread; notification is owner-affine — `Reactive_set` never fires observers; the owner (Thread 0 pump/paint) calls `Reactive_drain`, coalescing pending writes into one `onSet`/`onChanged` batch on the owner's thread. Atomicity in the value (no lock, no unbounded wait — the Bounded Wait Law), every observer on the owner's thread (Present-On-Demand applied to data); the observer lists stay owner-affine.

### R1 hotcwap — the four process kinds

Classification is the *primary contract*: surface > terminal > stdio > function. One type per process; a terminal-in-a-window is composition — an Application hosting a child Console via `ProcessSpawn` — never a hybrid.

1. **Application** — presents pixels through a Window/board composite chain (`CAMetalLayer` + swapchain). A lifetime *supervisor*: identity (name/author/version/icon), window registry, and a hot-module slot. Never owns a tick, present worker, frame scheduler or event router. `Application_start` is the blocking lifetime entry; `Application_close`/`stop` request all-window closure; `Application_run` is the keep-alive parked loop (hotcwap's own, graphvex-independent): it BLOCKS until every registered window is closed, letting the Window pump its own events in 5ms parked slices and supervising cancellable worker start events — so an empty window lives on its own and `Kernel_run(kernel, app)` returns only after the user closed all windows. The Kernel dispatches the Application into graphvex's `GfxLoop` (R3), which drives the Thread-0 event pump, frame scheduling, presentation (demand-driven — the Present-On-Demand Law and the Continuous Real-Time Live Resize Law) and telemetry writes through the Window's C callback bridge. Application/Process/Console/CommandLine are final infrastructure; R5 apps rely on them, never the reverse. An Application never grows a loop back: tick/render/present/poll are graphvex (frame) and Kernel-dispatch (start/stop) jobs.
2. **Console** — talks to a tty/stdio, executes shell scripts, hosts a REPL/session; never a window. Borrows R2 `ProcessSpawn`/`File`/`VexHome` for execution. A session pump state machine (`ConsoleIo` fn-table seam per the Conflict Triage Law) is polled in bounded 100ms slices with a cancel flag (the Bounded Wait Law) by a supervised thread — zero sockets, zero threads owned.
3. **CommandLine** — presents a FULL-SCREEN TERMINAL UI through the TTY (raw mode, alternate screen, one cell grid); the terminal analog of Window. It OWNS the tty device (acquisition, the single resize surface, bounded normalized input, a single present flush, teardown) and never widget semantics. Determinant (R3) owns terminal cells and the reloadable view/command module; TerminalApp (R3) composes it. CommandLine includes no R3 header — the seam is an injectable device backend plus the owned grid, and the app is a borrowed, swappable `CommandLineApp` (view/command) that may be replaced WITHOUT re-acquiring the terminal (a hot-loaded view lands in the same process). Resize is ALWAYS honored by `CommandLine_revalidate`, never deferred. It owns ncurses through one backend translation unit (`kernel/commandline_ncurses.c`), the terminal analog of `window/window_cocoa.m`.
4. **Process** — neither of the above; just a function. One-shot invocable wrapping one `int (*ProcessEntry)(void *context)` on the caller's thread. Re-runnable, never ticked; one invocation at a time. `Process_run` returns admission status separately from the callback's exit status. `Process_replace` changes entry/context/hot association together between calls, returning busy rather than waiting. Name and context are borrowed; freeing requires deregistration and external exclusion of API callers. A hot association is not a pin: callers keep code loaded during execution until generation pinning is integrated with the loader.

**Kernel is an object that stores and dispatches work — never an executor.** It owns the arenas, the four registries (`processes`/`applications`/`consoles`/`commandlines`, all doubling arena slabs per the No Hardcoding Law) and the supervised `Thread` registry. There is no `Kernel_tick`, no present-worker field, no Kernel-owned pump thread: `Kernel_run` is a thin reference forward handing each registered kind to its run function — `Process_run()` for one-shot invokables, `Console_run()` for session pumps, `CommandLine_tick()` for terminal applications, and graphvex `GfxLoop` registration for Applications (which then drive the frame loop, the Thread-0 event pump, presentation, and `frame(app, dt)` handler invocation on live bounds as a demand-driven frame scheduler). The Kernel never implements the work itself, so hot-reloading a module swaps running code without touching the supervisor.

**Explicit cold update boundary.** Consumer updates use separate `Hot_updateCold`: pause new admission, finish/exclude active module users, verify the complete trusted release and private load-copy checksums before constructors, admit ABI/export compatibility, restore candidate-only state, resolve success or rejection, then resume. Failed disk undo is unresolved and blocks resumption. Manifest catalogs allow sections; they are not the update engine. Cold trampoline registration grows/reuses symbol rows under reader exclusion; atomics do not pin code or make backing relocation concurrent-safe. This trusted native-code contract is not crash journaling, schema automation, remote-work suspension, a downloader or a sandbox. Primeagen's first slice reloads terminal view/code only; roles/tools remain unfinished.

### Managed exceptions — socket/spawn/decode seams

Waivers under the Conflict Triage Law; Tier 1 preserved:

- Engine `src/io` owns filesystem IO/NIO and the `ProcessSpawn` leaf driver. `FrameInbox` is a bounded caller-fed byte inbox, not a WebSocket implementation: fixed receive buffer, state, cancel flag, timeout; owns no threads or sockets. No WebSocket implementation exists there. `FrameInbox_poll` waits at most 100ms in ~1ms cancel-checked slices (the Bounded Wait Law, drop-degrade false). `ProcessSpawn` is a bounded child-job table (fixed slots, cancel flag): `posix_spawnp` launch (never `system()`), non-blocking `waitpid` reap slices bounded to 100ms, `SIGTERM` cancel — no blocking wait, no `UINT64_MAX`, zero threads.
- Graphvex owns `FrameImporter` (pure RGBA8→`Image` upload via `Image_upload`): no `popen`, no `libav*` include/link, no threads; callers decode through the `ProcessSpawn` shape and never call it from tick/render paths.
- `api-haven` owns `HavenWsFanout` (16-slot fan-out registry over opaque `void*` handles + `WsSource` fn-table `{connect, poll, send, close}`, `pollStep` budget-driven by its host caller) + `AiSse` (pure caller-fed incremental SSE `data:`/`event:` state machine bound explicitly to one fanout slot via the existing `WsSource` table, caller-budgeted `pollStep`, 100ms slices, drop-degrade false, zero socket/thread/alloc, truncation flag per the Cold-Strict, Hot-Minimal Validation Law) + `DbSqliteFile` (catalog-only read-only SQLite file row: path, caps, bounds, fn-table only, zero `sqlite3.h` include/link — execution delegates via opaque handle to the database owner / engine File/VFS) + `AssetBroker` (`AssetBroker_downloadToCache` bounded chunked-copy returned value with truncation state, per-chunk 100ms budget + cancel flag, never a whole-file budget, `VexHome_cache`-confined, closed before `Memory_freeAll`): zero `pthread_*`, zero socket syscalls, no scraping, no exec, no vendor SDK. `WsSource` is only a callback seam: R2's `net/websocket` client owns the protocol and its socket, and R2's `net/vex_ws_source` adapter exposes the same four signatures so a host that can see both layers assigns them directly — structural compatibility, no cross-repo include in either direction. `tests/api-haven/ws_source_binding_test.c` is the host that binds them and asserts the signatures at compile time.

Build/commit order (dependencies first): `relational-engine` → `vexspoke` (engine ABI consumers) → `graphvex`/`api-haven`/`language`/`darkbase`/`samplerate` → `hotcwap` → `darling-framework`/`sesh`/`harness` → R5 → R6. Boot order is the reverse crown: R1 first.

### Teardown (top-down; arena last)

```text
R6 superapps detach and stop their borrowed app-level workflows
  → R5 applications detach and stop using their borrowed resources
  → R4 widget/frame bridges detach views, layers, and panel surfaces
  → R3 drivers retire GPU/device resources after dependent work stops
  → R2 computation/storage users stop and join before their owned state dies
  → R1 host closes windows, releases remaining native handles
  → Memory_freeAll()      // arena reset LAST, after all teardowns
```

- `Memory_freeAll` is always the final step — never earlier. Shims allocate outside the slabs (`calloc`, `IOSurfaceCreate`, `strdup`), so freeing the arena first orphans every surface, layer and native handle with no leak record.
- **Detach before free:** registry → parent → free. `PanelCocoa_free` runs before its `Panel` is freed; a `Window` detaches adapters before `close`. A skipped step is a leak, not a shortcut: a probe that exits without `Window_destroy` leaves the `NSWindow` outliving the process as a ghost.
- Multi-app Kernel order (R1 host, N apps x M windows): `Kernel_destroy` first stops R5 clients, then detaches R4 frames and all `Application`s from graphvex's `GfxLoop`; retires R3 graphics resources (including `Vk_shutdown` and its bounded present-thread join); stops `Console` sessions (`SIGTERM` children, non-blocking reap per the Bounded Wait Law); retires `Process` hot-mod pins; bounded-joins supervised workers before releasing their owned state; closes R1 windows after adapters detach; resets `transientArena`; destroys master `arena` LAST. Never free `arena` while any process kind / Window still runs.

Older citations of *Teardown Order Law* refer to the teardown clause of this law.

## One Type Registry Law (Project-Scoped Identity, Uniform Per-Project Numbering)

- **Type identity is project-scoped, never class-number-scoped.** A bare class number is meaningless without its project: vexspoke `#3` (`ID_DOUBLE`) and darling `#3` (`ID_CANVAS`) are entirely different types. To identify any id, resolve the project first, then switch on the class number within that project's scope:

```c
switch (Type_arch(id)) {              // project dispatch FIRST
    case ARCH_VEXSPOKE:  ... // then Type_class(id) ranks vexspoke's registry 1..N
    case ARCH_GRAPHVEX:   ... // then Type_class(id) ranks graphvex's registry 1..N
    case ARCH_DARLING:    ... // then Type_class(id) ranks darling's registry 1..N
}
```

The 64-bit layout `0xF'PRPR'M'W1'W2'BE6C'CCCCCC` anchors identity on the 8-bit PROJECT byte (`PROJ_VEXSPOKE`, `PROJ_GRAPHVEX`, `PROJ_HOTCWAP`, `PROJ_DARLING`, `PROJ_API_HAVEN`, `PROJ_DARKBASE`, `PROJ_RELATIONAL_ENGINE`, `PROJ_SAMPLERATE`). Fields, high to low: form (4 bits, 60..63), project (8 bits, 52..59), modifier (4 bits, 48..51), wrapper 1 (4 bits, 44..47), wrapper 2 (4 bits, 40..43), the fixed `BE6C` "векс" sugar (16 bits, 24..39), and the **24-bit class field** (bits 0..23) — the only field that indexes a project's registry. `Type_arch` reads the project byte; `Type_class` masks the local number. Every repository owns exactly one class registry in its own `*-type.h` (vexspoke `src/oop/type.h`, darkbase `src/oop/type.h`, samplerate `src/oop/type.h`; darling `src/c23/darling-type.h` is an empty draft; graphvex and hotcwap register no classes yet), numbered **1..N** with gaps allowed — **no global hex windows** (id #1 in darling ≠ id #1 in vexspoke). The shared type algebra — mask constants, `Type_make`/`Type_class`/`Type_form`/`Type_project`, the form/modifier/wrapper predicates, `Type_arch`, and the parent-chain resolver — is owned once by the engine (`type/type.h`); the 32-byte block header `[id u64 with BE6C sugar][hash u64][length u64][pointer u64]` lives with the allocator in `nio/mem.h` (`MemoryHeader`). A repository's `*-type.h` keeps only its own class numbers and includes that algebra.

- **Registry path collision (managed exception, the Conflict Triage Law):** more than one repository uses the path `oop/type.h`, so that relative include is ambiguous the moment a translation unit sees two repositories' `src` roots at once (demonstrated: vexspoke's `exception/exception.c` compiled with darkbase's `src` first lost `TYPE_EXCEPTION_SINGLETON`). Each repository's own TUs are compiled with its own `src` first (which every registered build target does), and a file never includes another repository's `oop/type.h` by that ambiguous path — include the engine-owned algebra (`type/type.h`) or a repo-qualified path. A future single shared include root would need the registry renamed.
- **A full id (project bit set) means exact project dispatch. A bare id (project bit zero) means vexspoke's own legacy class space** — `Type_arch(bare)` reports `ARCH_VEXSPOKE` and class numbers resolve through vexspoke's own chain. Cross-project runtime dispatch passes full ids (`TYPE_*_SINGLETON`) and masks with `Type_class` before comparing; an unmasked comparison against a bare `ID_*` only ever matches vexspoke classes.
- **Single source of truth:** registry macros live only in the repo's `*-type.h`; the shared algebra constants/macros only in engine `type/type.h`. Widget/class headers define no guarded `ID_X`/`TYPE_X` fallbacks — duplicate definitions are the scattered-registry defect (a pre-state where `richtext_panel.h` and `expandable_list_container.h` both claimed `0x006A`). Views and BEHAVIOR-class registries (hotcwap thread ids, etc.) declare their macros in one centralized winner header per repo.
- **Cross-project parent chains are data, not code:** a child repo grants its chain once through `Type_registerParents(proj, parents[], count)`, where `parents[i]` is the parent class NUMBER of class # i (`0` = root). Registration is idempotent (re-register replaces), rejects `proj == 0`, non-project-bit, `PROJ_VEXSPOKE`, and `(nullptr, count != 0)`; the slate grows on demand (arena-backed, exponential doubling per the No Hardcoding Law). An unregistered project byte resolves every class as a root. `Type_isA` keeps the project byte while walking the chain, so `Type_isA(child, bareTarget)` interprets the target as a class number in the child's project. Registration rejects cyclic, self-referential and out-of-range chains atomically (the Bounded Wait Law), and `Type_isA` walks with a budget bounded by the project's chain length — no table can spin it. Vexspoke's own bare-id chain is granted through `Type_registerBareParents` (its owner test grants it; production currently has no caller), so the algebra hardcodes no project class numbers.
- Repos with zero registry classes (hotcwap, api-haven, graphvex today; darling's registry is an empty draft) register nothing. Renumbering a repo's `*-type.h` is its own owner-side feature commit (Git Workflow Law); downstream consumers of changed class numbers are updated upstream-first (`vexspoke` → `graphvex`/`api-haven`/`hotcwap`/`darling-framework`).

## Canonical Include Paths Law (Zero Parent Hops)

Headers never traverse upwards with `..` or `../..` to cross module or repository boundaries; every `#include` is rooted at the canonical subsystem directory:

```c
#include "nio/mem.h"               // yes
#include "../nio/mem.h"            // no — legacy monorepo artifact
#include "vulkan/vk.h"             // yes
#include "darling/panel.h"         // yes
#include "window/window.h"         // yes
#include "io/vfs.h"                // yes
#include "../../io/vfs.h"          // no
```

This keeps include spelling identical in the unified workspace and standalone native build contexts; each build supplies the real subsystem include roots.

## Standalone Autonomy Law (Target Seam)

- The workspace root owns the ecosystem's only maintained `CMakeLists.txt`. Nested repositories, applications, personal tools and the shared tests checkout contain no IDE CMake entry; never add one per class, folder or repository. The root imports `b`'s build-derived contexts and supplies excluded, recursively discovered source targets for draft/unregistered units, with repository-scoped include paths and host-platform selection. Source-free blueprints receive no fake source targets. Missing headers remain real errors, never fake declarations.
- CMake supplies the shared IDE code model and retains the existing opt-in native test integration. It is **not** runtime build truth: `b`, Cargo and other actual owner build paths keep that responsibility. No indexing operation downloads dependencies, launches an application or grants test/visual acceptance. Compiler context and header checks do not prove the IDE's displayed highlighting/inlays. Per-repo README CMake disclaimers are retired; workspace editor guidance lives once in the workspace README. Rust analysis uses the actual Cargo packages.
- Standalone autonomy remains mandatory for actual runtime builds: each owner declares and resolves its real upstream contracts through its native build path, reuses supplied dependencies in-tree instead of duplicating implementations, and proves standalone closure before claiming it. Workspace IDE configuration is not that proof. The former `if(NOT TARGET ...)`/FetchContent example is retired — not a requirement to reintroduce per-repo CMake or automatic dependency downloads.
- This workspace-only rule covers owned project metadata, not third-party build files or disposable external-CMake fixtures. `b` may still build external CMake projects; its adapter and hostile/failure tests remain supported.

## Living Documentation Law

A document is living only when its description changes alongside the code or contract it describes. Three surfaces are maintained together — blueprints, preferences, readiness — and calling a document living never waives its details.

### Source-file blueprints (`;;OVERVIEW` and `;;DEFINITION`)

Every `.c` (and `.m` where applicable) is self-contained: a developer or agent understands the class, its memory layout and all capabilities from the first 100–150 lines of the implementation file without tabbing to the `.h`.

1. `;;DEFINITION` — the architectural raison d'être; fluid paragraph prose, depth scaling with actual complexity: a focused paragraph for a leaf adapter; comprehensive paragraphs (architectural necessity, memory layout, mechanics, concurrency, relationships to adjacent R tiers) for a coordinator.
2. `;;OVERVIEW` — the structural summary and public/private registry: a machine-scannable expanded blueprint near the start of the implementation. Readable separator-line diagram; `CLASS: Name (path)` (or `MODULE:` for a pure procedural entry point with no owned class, plus a full grouped function/helper/contract map — never invent empty structs or list foreign fields); `STRUCT FIELDS (Mirroring path)` with the complete typed field list in declaration order, one-line role for every field; `FUNCTION REGISTRY` grouped by constructors, core operations, setters, getters, projections and lifecycle as applicable, listing actual public signatures and significant private behavior, exports distinct from file-local statics; kept helpers and slot records with complete field maps; ending with the class's admission, null/default, failure-preservation and ownership/thread contract where applicable. Omit empty categories, never real fields or operations. Token cost never shortens a blueprint; the author's expanded Channel-style overview is preserved. Explain difficult paths where they live.
3. When fields, constructors or behavior change, the overview and definition are updated in the same change. A stale field list or an API listed but no longer present is a defect. Existing detailed overviews are never collapsed; retrofit the expanded blueprint when touching a unit — this does not claim untouched files already migrated. Python host modules use an equally explicit near-start docstring map, never fake C annotation tokens.

### Preferences (architectural invariants)

The real Git-ignored `/PREFERENCES.md` in the vexgraph workspace is the supreme constitutional law and single source of truth, published per Canonical File & Gist Publication. If rules live only in memory or chat history they break within days; absolute unbroken alignment across subsystems is the price of a zero-GC, manual-memory-layout ecosystem.

1. **Same-cycle update + Gist publication:** whenever an invariant, convention, rule or preference is introduced, modified, refined or clarified, `/PREFERENCES.md` is updated and uploaded to its existing Gist in the same development cycle, verified against the local file. Out-of-date preferences are an architectural defect. The universal file stays Git-ignored; related repository changes get local commits (Git Workflow Law).
2. **Universal reference:** every sub-repository ships a `CONTRIBUTING.md` explicitly linking back to the canonical constitution as its supreme guiding authority.
3. **Subsystem conformance:** every implementation across `hotcwap`, `darling`, `vexspoke`, `graphvex`, `api-haven` and the rest adheres strictly to these laws; no repository is exempt.
4. **Title-identity enforcement:** no law is cited by number anywhere — code, docs, git history; any stale numeric citation is fixed in the same cycle it is noticed (Law Identity Doctrine).

### Feature readiness (status and proof)

Each repository's feature readiness matrix lives in the ecosystem readiness Gist (https://gist.github.com/vex-graph/6943f92acb931b25dad1073c46da6ce7, one `<repo>.md` per repository): one row per feature (container/widget/module/command) with a scope line and a status emoji. The ecosystem blockers Gist (https://gist.github.com/vex-graph/e921fa188eebbd0c68c4e59646109887) is the companion backlog of genuinely open work, deferred decisions and proof gaps. The retired `ecosystem/ecosystem` wiki is not canonical and is unmaintained. The status column is the machine-readable handshake telling the ecosystem what is real vs stubbed vs absent; architecture maps and roadmap targets never imply completion, R5 apps are unfinished until their own workflow/integration proof exists, and R6 superapps are blueprints until their own composition proof exists.

1. **Same-cycle status law, per file pair.** Any commit that ships, stubs, retires or re-scopes a feature moves its `<repo>.md` row in the readiness Gist in the same cycle — code commit first, then the gist row-write (`gh gist edit <id> <repo>.md`), never a deferred "update checklist" blob (Git Workflow Law). Code and gist live in different stores and ship as separate records, but a green-on-disk row stale-red on the sheet is a broken intermediate state.
2. **Status legend (canonical, mirrors the readiness Gist Home):** 💚 98% done, production-ready · 🟩 95% done, implemented & functional · 🟨 85% done, substantially implemented · 🟧 75% done, partial/draft · 🟥 concept/draft, zero working source · ⬜ vital future work, not implemented (never "dropped/archived"). A row's scope line is rewritten when the actor or deliverable changes, not just the emoji.
3. **Test proof gates the status.** 🟨 rows carry test names in the scope column (`tests/<name>_test`); a row is never 🟩 before its unit tests pass under `-Wall -Wextra -Werror` (Git Workflow Law). Moving a row up without proof is inflation; use the Conflict Triage Law (`;;INTENTION`) instead of silently overstating.
4. **Commits are per-checklist-file, per-repo.** The row ships inside its feature commit; cross-repo rows never bundle (Git Workflow Law). Code commit and Gist edit are separate records in the same cycle.
5. **The spearhead is the wedge, not the tail.** The next work item is the structural keystone unblocking the largest contiguous 🟥 block (e.g. `OverlayRoot` unblocking the dialog/dropdown family); the block then collapses down the matrix — mirroring upstream-first (Git Workflow Law).

Older citations of the *Living `;;OVERVIEW` & `;;DEFINITION` Blueprint Law*, *Living Preferences Law*, and *Living Feature Readiness Law* refer to the corresponding clauses of this law.

## Bounded Wait Law (No Unbounded Waits on Joined Threads)

Any thread another thread joins must reach its exit check within a bounded time on every path. An infinite wait (`UINT64_MAX` fence, endless queue poll) parks `pthread_join` forever and freezes teardown — the window goes ghost, unstopped threads keep logging, `Window_destroy` never runs.

```c
// no — hangs teardown when the drawable dies (fullscreen close)
WaitForFences_fn(dev, 1, &fence, VK_TRUE, UINT64_MAX);
// yes — drop the frame, re-check running, join succeeds in ~100ms
if (WaitForFences_fn(dev, 1, &fence, VK_TRUE, 100000000ULL) != VK_SUCCESS)
    return false;
```

Fences, queue waits and device idles on worker paths take explicit timeouts with a drop-degrade path (skip frame, keep old content, return). The bound is generous (100ms ≈ 6 frames) so healthy hitches never trip it — only a dead resource does. A timeout firing in the log means the resource died: investigate the resource, not the timeout.

## AI-First Architecture Manifesto Law

The extremes of this codebase — zero arrow sugar `(*ptr).field`, strict single-class-per-file, explicit C constructor overloads, vtable dispatches, symmetric getters/setters, value-returning APIs, two-layer dereference caps, zero steady-state allocation — are not accidents or idiomatic-C misunderstandings. They are an intentional, rigorous manifesto of **AI-Human Pair Systems Programming**:

1. **Machine comprehension & context density:** LLMs and agents are most precise when contracts are explicit, typed, un-aliased and local. Arrow sugar hides the dereference boundary; implicit constructors hide init order; multi-class files cross-contaminate reasoning. One class per file holds the complete, un-truncated operational reality in the model's active window.
2. **Deterministic mechanical syntax:** `.` means value access, `->` means pointer dereference; writing `(*ptr).field` keeps every memory hop explicit to human and machine alike, preventing casual indirection and cache-line thrashing.
3. **The AI agent as boilerplate engine:** humans historically used macro trickery to avoid typing boilerplate; here the AI agent writes, verifies and maintains the dense explicit machinery, while the human architect directs invariants, algorithms and concurrency semantics. The boilerplate is a machine-readable safety scaffold, not a typing burden.

> **SANITY NOTICE FOR EXTERNAL CONTRIBUTORS:** this repository is not built for traditional C conveniences, casual hacking or stylistic shortcuts. If you do not approve of this architecture, consider contributing elsewhere for your own sanity. PRs, issues or refactors reintroducing `->`, collapsing classes into single files, removing explicit getters/setters or "modernizing" the code are not accepted. The upstream codebase is maintained exclusively by its author in tandem with the AI agent.

## Conflict Triage Law — Managed Exception, Not Veto

When laws conflict, or intent outgrows a law, the answer is never a bare "this violates X." It is "unless you don't want it, here is how we manage it." The thought prevails; the laws adapt in the same cycle (Living Documentation Law). Tier 1 exists to prevent crashes, not to prevent thinking: every conflict is triaged, given a managed path, and codified so the next agent inherits the decision.

1. **Name the tiers** (see the Tier Map): Tier 1 beats Tier 2 beats Tier 3; state where each conflicting law lives.
2. **Assess before blocking:** does the law actually cover this case (link-time vs runtime, single-app vs Kernel multi-app, global vs per-arena)? A misapplied law is not a violation.
3. **Managed exception:** propose the indirection preserving Tier 1 while granting intent. Canonical moves: opaque handle + callbacks instead of a downstream include; fixed array + count + getter instead of `**` chains; `MemoryArena_create`/`freeAll` + bounded-join instead of globals; `;;INTENTION("reason")` + `;;DRAFT` markers for Tier 2/3 waivers.
4. **Prefs patch in-cycle:** if intent prevails, draft the exact preferences wording change now. Tier 1 waivers additionally require an alternate safety proof (no unbounded wait, no use-after-free, no circular link), reviewed heavily. Tier 2/3 waivers require `;;INTENTION` plus overview/docs updates in the same commit.
5. **Never silent drift:** a managed exception without its prefs + overview + docs update is a defect, same as stale preferences (Living Documentation Law).

## Cold-Strict, Hot-Minimal Validation Law (Crash-Guard Split)

Validation splits by path temperature.

**Tier-1 crash-guard half:** no function ever crashes, blocks unboundedly, allocates, or use-after-frees on null, out-of-bounds, overflow, cancelled, or timed-out input — it returns `false` or a symmetric-accessor safe default instead.

**Tier-2 contract half:** setters validate at least as strictly as getters, with the reject-or-clamp policy stated in the `;;OVERVIEW`; getters return safe defaults (the Java Law).

*Rationale:* unvalidated cold input is how null dereferences and overflows enter; per-element revalidation on a 60fps hot path is how frames die. Validate once where input enters; trust the validated handle where pixels move. A silent truncation or unlogged cold drop corrupts state; a log line per hot frame corrupts performance.

1. **Cold paths validate exhaustively, once.** R1-entry / R2-boundary seams (`AiProvider_get`, `ApiAuth_apply`, `Rest_postJson`, `McpServer_handleLine`, `HavenWsFanout_pollStep`, `ProcessSpawn_spawn`, checksums) check every hostile input: null, empty, wrong-id, bounds, integer overflow, cancelled, timeout. One `THROW(...)` per failure at most (THROW Law), then drop-degrade per the Bounded Wait Law (return `false`, keep old content, move on).
2. **Hot paths guard minimally, never log.** Vk present, `Raster`, `SdfGpu`, darling layout, `GfxLoop_frame`, `presentFrameLocked`: at most one `nullptr` entry guard returning `false`, zero per-element revalidation, zero logging, zero allocation. The hot path trusts the cold-validated handle. Deeper invariants are proven at compile time (`_Static_assert`) or tested at the owning seam, never assumed from an annotation. Optional debug probes may compile out in Release; checks preventing out-of-bounds access, use-after-free, or corrupt input do not compile out:

   ```c
   if (self == nullptr)
       return false;
   ```
3. **The Truncation-Never-Silent clause.** Bounded text production returns a named value record containing the text and truncation state, so the caller degrades loudly:

   ```c
   StringResult Class_copyText(const char *src);
   ```
4. **Seam tests at cold boundaries only.** The full nullptr / empty / wrong-id / overflow / truncation / cancelled / timeout matrix lives at public cold seams in `tests/*.c` `MODULE` harnesses. Hot paths carry `nullptr`-guard-only tests — no per-element matrix, no timing harness on the frame path.

## Data-Oriented Storage Law & Object-Oriented Ergonomics

Collection patterns (nodes, lists, tables, trees) use flat, index-based backing storage while exposing an object-oriented class API.

1. **Storage is flat and index-based.** Parent/child relationships are integer indices into a flat array, never pointer-chased linked lists. Pre-order array layout is canonical for trees: a node's entire subtree occupies the contiguous range `[nodeIndex, nodeIndex + subtreeSize)`, so bulk traversal never jumps. Index-based flat arrays keep CPU cache lines hot and make bulk traversal mechanically simple.
2. **API is object-oriented.** The public class API provides what consumers need without exposing backing indices or forcing internal piercing. Accessors follow the Java Law; naming and output order follow the Semantic Consistency Law. R4-specific part verbs belong to Darling's repo-local preferences.
3. **Application-specific class choices stay local.** Darling's `ExpandableListContainer`, checklist mode and file-tree composition belong in its repo-local contract — examples of the storage/API split, not requirements on every collection ecosystem-wide.

## Test Segregation Law (Zero Source Pollution — No Tests in Source Trees)

Test code and harnesses NEVER reside inside production source directories (`src`, `darling/`, `render/`, `../../_trash/main/`, `app/`, etc.). Tracked test sources live in the independent workspace `tests/<subsystem>/` repository, or an owning repository's top-level `../../../tests` when built standalone. Production trees contain only production classes, headers and build scripts.

*Rationale:* colocating tests pollutes the 1:1 class-to-file architecture (Java Law), confuses directory-based builds and watchers, muddies static analysis and search, and risks circular dependencies or test helpers linking into production shared libraries. Test suites are clients of the subsystems they test.

1. **Zero test files in production trees.** No `*_test.c`, `test_*.c`, `*_test.h`, `test_*.h`, or `*_demo.c` is ever placed in or committed to a production source directory. Violations are rejected in review and failed in CI.
2. **Unified test hierarchy.** The independent tests repository uses `tests/<subsystem>/` (`../../../tests/darling`, `/vexspoke`, `/graphvex`, `/hotcwap`, `/api-haven`, …). Every release-relevant test is built and registered with the runner; a file on disk is not proof of execution.
3. **Subsystem partitioning.** `../../../tests/darling`: UI widgets, containers, text rendering, layout, event dispatcher. `/vexspoke`: core primitives, memory, threading, time, io, relational. `/graphvex`: GPU buffers, rendering passes, texture, font backend. `/hotcwap`: hot reload, manifest parser, kernel, window lifecycle. `/api-haven`: API client, webhooks, MCP server, SSE, AI provider.
4. **Standalone repo test contract:** without the independent tests checkout, an owning repo keeps tracked tests in a top-level `../../../tests` directory, never inside production folders.
5. **Track proof, ignore outputs.** Commit test source and build wiring; ignore generated binaries, scratch dumps and build directories — never the test source tree itself. Release proof includes a test build retaining assertions that executes the registered negative and normal paths; sanitizer/crash suites supplement rather than replace runtime safety checks.

Checkpoint note: this document merges the former standalone *Executable Evidence and Readiness Law* and *Per-File Battle Test Law* rows below into the Feature Implementation and Adversarial Proof Law and the Timestamped Test Checklist Law; see the Appendix.

## No Section Sign Law

The section sign (U+00A7) — the "double-S" — is forbidden everywhere: source comments, `;;OVERVIEW` blocks, docs, commit messages, wiki rows, and this document. Section references are plain ASCII words: "see section 32", "the KeyMap section", "sections 41–48" — never the glyph-prefixed forms.

*Rationale:* the glyph renders as an ugly double-S in monospace, breaks `grep` for section references, mangles fonts and terminal pipelines; the word "section" costs nothing and survives every tool, font and copy-paste. A codebase banning arrow sugar for machine-readability has no business smuggling invisible punctuation into comments.

The workspace-wide migration scrubbed every occurrence (source comments, test-section markers, `_docs/` and `_bugs/` notes, and this document) in the cycle this law landed; the umbrella-local legacy markers now read as plain words (`// section N` test-section comments). A reintroduced glyph is a defect on arrival, same as `->` under the Semantic Consistency Law (Reference form).

## Per-Repo Preferences Extension Law

The central Git-ignored `/PREFERENCES.md`, published through its canonical Gist, serves exclusively as the universal supreme constitution — foundational invariants mandatory across all ecosystems. Individual repositories maintain their own standalone, self-identifying `<repo>-preferences.md` file at their repository root, inheriting universal laws plus domain-specific physically-binding local laws.

1. **Naming:** `<repo>-preferences.md` (e.g. `graphvex-preferences.md`) at the repository root; it never shadows or renames the universal workspace `/PREFERENCES.md`.
2. **Standalone autonomy:** each file sits at its own repository root, never a symlink into vexspoke; repositories checked out standalone remain fully self-describing.
3. **Local definitions:** each lawbook defines its repo-specific laws in full; universal laws inherit through its Markdown link to this file. Repo-local law headers use their Titles (`### <Law Title>`) without numeric ordinals.
4. **Markdown canonical link:** every repo-local lawbook links to the canonical constitution Gist and gives its real workspace-relative `/PREFERENCES.md` path. Standalone checkouts obtain the constitution from the canonical Gist. No edition or synchronization annotation is required for Markdown lawbooks.
5. **Zero-drift same-cycle review:** whenever the universal `/PREFERENCES.md` changes, affected repo-local lawbooks are reviewed in the same development cycle; their Markdown indexes and definitions are updated when local contracts change.
6. **Law Binding Matrix:** each repo-local lawbook starts with a Law Index listing its own rules, scope and enforcement; universal laws are inherited by reference to the canonical Index and never duplicated in that table.
7. **Mandatory chained reading:** before proposing or editing work in a repository, read the complete universal constitution, its complete owning repo-local lawbook, applicable test laws and current checklist, and existing implementation. The Tier Map's repository reading map is the discovery surface; its links are maintained in the same cycle as adding, moving or removing a lawbook. Cross-repo work reads each affected owner's rules; missing files are explicit gaps, not permission to ignore local contracts.

## toString Law (Every Object Has a String)

Every class ships **two bounded string projections**, returned as bounded values with explicit truncation state, cold-path only:

1. `StringResult Class_toString(const Class *self)` — the **VALUE** string: a concise, class-specific summary of the object's state.
2. `StringResult Class_toStringStruct(const Class *self)` — the **STRUCTURE** string: a by-name dump of the object's own fields, **ONE layer only** — a nested object field renders via that object's `toString`, never by recursing into its `toStringStruct`; a class wanting a deeper view calls the child's `toStringStruct` itself.

Rules: every public class ships both (no class is string-blind); fixed signatures as above; a null `self` returns the value `"nullptr"`, never crashes; never called on a frame — it formats; `toStringStruct` mirrors the `;;OVERVIEW` STRUCT FIELDS block (same fields, same order — the two enforce each other, a field added without updating the dump is a defect); string fields are emitted quoted and escaped (`\n`, `\t`, `\"`, `\\`); the returned value is the law, callers supply no destination buffer; the Label formatter's `{object}` placeholder calls `toString`. Depth is bounded by design — no recursion guard needed.

## Authorial Intent Law

Deliberate author decisions — magic sentinels, sugar macros, surprising naming (`SIZE_AUTO` as the FourCC `åuto`, `VEX_*` sugar, their kin) — are documented at their definition site as intentional acts of the author, vex. The stamp is a plain comment, never a `;;` annotation macro:

```c
// INTENTIONAL(vex): SIZE_AUTO is the FourCC "åuto" (0xE575746F) by design —
// negative on every platform so any negative dimension reads as AUTO.
```

Without a provenance stamp, a future reader cannot tell a deliberate aesthetic from an accident, and the next passer-by "fixes" the magic.

1. **Plain comment, fixed shape:** exactly `// INTENTIONAL(vex):` followed by prose. No `;;AUTHOR`, no `;;DELIBERATE`, no new `src/annotation` header (the Two-Semicolon Annotation Style Law is untouched). Greppable: `INTENTIONAL(vex):`.
2. **Definition site, not call sites** — one stamp where the decision is defined; call sites stay clean.
3. **What + why, one breath** — what the decision is and why it is that way. A stamp with no reason is a defect: restate or remove.
4. **Not a waiver:** authorial intent never overrides Tier 1. A deliberate decision risking a crash, leak, deadlock or unbounded wait still goes through the Conflict Triage Law with `;;INTENTION` + safety proof. `INTENTIONAL` documents taste; `INTENTION` justifies exceptions.
5. **Retrofit as noticed:** existing deliberate decisions (`SIZE_AUTO`, `VEX_*` sugar) gain their stamps when touched or noticed, same cycle — no separate migration blob. New deliberate decisions ship their stamp in the same commit as the decision itself (Living Documentation Law).

## No Hardcoding Law

A constant used to initialize a value is a **default**, not a permanent user-visible decision. Name it at its owner, allow the consumer to change the current value through a validated interface, and read the current value at use sites. Never treat a named default as proof the resulting value is final.

**Defaults and final constants:** configurable sizes, thresholds, delays, colors, counts, cadence and layout choices start from named defaults (`SCROLL_BAR_THUMB_MIN_DEFAULT`), then use current state an application or user can adjust; validate updates; expose current state through the class API. A value may be final only when its meaning is inherently fixed by math, ABI, wire protocol, physical format or a justified safety/security bound — state that reason at its definition; never pretend a configurable preference is one of these constants. Changing an external-input safety bound requires an explicit, safe validation policy, never unchecked setter access. Replace non-obvious bare literals with named values (numeric construction follows Semantic Consistency Law, Construction and arity). Runtime-varying values come from their source of truth, never a cached guess.

**Growable work and explicit bounds:** dynamic entity collections, registries, children, layers and task queues use current counts and growable storage; a named initial capacity is not a rejection ceiling; growth may happen on a cold path so hot paths stay allocation-free. Fixed protocol, hardware or safety limits are permitted only when documented at their owner, exhaustion is observable and safe, and tests prove the boundary — never silently ignore excess work or impose a guessed limit on dynamic entities. Layout geometry derives from parent extents and current configuration; continuous resize is never disabled merely to avoid the general case.

**Time and deterministic motion:** cadence comes from the display, caller clock or another explicit source, never a fixed frame rate; motion is a function of elapsed time, not frame count. Headless tests pass explicit time and named magnitudes so the same elapsed time produces the same result.

Older name — *Dynamic Scalability & Anti-Hardcoding Law* — refers to this law.

## WHAT Law

A `void*` is a promise with no receipt. The WHAT Law is the receipt: every `void*` whose pointee type is not self-evident from its own name carries a `;;WHAT("<type>")` annotation on the line above its declaration, naming exactly what it points at. The runtime already carries a 32-byte self-describing header; the WHAT Law is its compile-time twin.

1. Every non-obvious `void*` declares its pointee; a `void*` already named for its type (`messageBytes`, `vertexData`) need not.
2. **Line-above form only:** the marker is a `_Static_assert` (Two-Semicolon Annotation Style Law), hence an annotation line above `void* x;`. No inline `void* WHAT("...") x;` — an annotation is not a declarator.
3. The text names the C type exactly as a cast would spell it: `uint64_t`, `Field`, `Reactive`, `Reactive<uint64_t>`, `char*`.
4. A documented `;;WHAT("T")` agrees with the block's `Memory_type()`; a mismatch is a defect.
5. Tier 2, zero cost: `_Static_assert(1, ...)` compiles to nothing.

## Cold-Only Reflection Law

The engine's reflective walk — resolving a name to a value, or following a dotted path (`character.position.x`) node to node — is a **cold rendezvous**: it runs when a human or a tool asks "where is this thing, right now?" (search box, debugger, script binding, save/load walk, hot-swap rebind, telemetry). It must **never** run on a per-frame or otherwise hot path.

*Rationale:* the walk is pointer-chasing by design (it is a graph); every hop risks a cache miss, and the cost scales with the scene, not the work. A name lookup per entity per frame turns a cache-friendly sweep into thousands of pointer hops. Hot iteration stays data-oriented and flat; cold rendezvous is a Relational Engine rendezvous; mixing them costs frames.

1. **Reflection is cold-only.** Name resolution, dotted-path resolution, any node-graph walk: setup, search, debug, script, save/load, hot-swap, teardown — never per frame, never per entity per tick.
2. **The marker is explicit.** A module hosting a cold resolver carries `;;INTENTION("cold path search is a node walk by design; hot iteration stays DOD")` at the walk site, so a future reader sees a chase and reads *why*.
3. **Hot paths stay flat:** per-frame iteration and per-frame field access use flat data-oriented storage (Data-Oriented Storage Law) and hoisted locals (Semantic Consistency Law, Access depth) — never a reflective walk.
4. **A hot reflective call is the defect, not the chase:** if a resolver shows up on a frame path, the call site is wrong, never the resolver's design.
5. **Resolve once, hold the pointer:** a hot consumer needing a value repeatedly resolves the name or path once, cold, and holds the resulting pointer — it never re-resolves per frame.

## Install Ledger Law (Machine-Scoped Install Memory)

The install ledger is a machine-scoped record of application identities (`org`/`app`) installed on this host. It lives OUTSIDE the install tree, in the OS per-user state directory (macOS `~/Library/Application Support`, Windows `%LOCALAPPDATA%`, Linux `$XDG_STATE_HOME`) as a plain record file. `MANIFEST_REFLECT` records an install; `UNINSTALL` removes the tree but keeps the record (state `uninstalled`); `MANIFEST_IS_FIRST_RUN` consults the ledger, so a wiped tree is never a fresh install. The in-tree `manifest.json` remains the ownership marker for safe deletion; the ledger is the machine's out-of-tree memory.

1. **Out of tree**, machine-scoped, keyed by `org`/`app`; never inside the install root, never the OS secure store or registry — a plain record, not a secure store.
2. **Uninstall keeps the record:** only an explicit `forget` (deliberate machine reset) purges it.
3. **First-run consults the ledger:** true only when the ledger holds no record for the identity and the in-tree mark is absent.
4. **Correctness, not security:** a local user with the machine can always clear the store; the ledger is never a security boundary.

## Platform Support Floor Law (Apple Silicon macOS 14+, Windows 10+)

The ecosystem declares a minimum supported build/runtime baseline, not a ceiling on features. macOS baseline: Apple Silicon `arm64` M1 and macOS 14.0 (Sonoma). Windows: Windows 10. Builds below are unsupported; newer features are gated at runtime (Capability Gating Law).

1. **macOS hardware:** `arm64`, never Intel — `CMAKE_OSX_ARCHITECTURES=arm64`; no `x86_64`, no Universal, no `#if defined(__x86_64__)` paths.
2. **macOS software:** 14.0 (Sonoma) — `CMAKE_OSX_DEPLOYMENT_TARGET=14.0`. Every API newer than the floor is reached through an explicit availability guard; an unguarded newer-API call is a defect, not a warning.
3. **Windows floor:** `_WIN32_WINNT` / `WINVER` pinned to `0x0A00`.
4. **Portable CPU baseline, never `native`, in shipped code:** `-mcpu=apple-m1` so a binary built on an M6 / A18 still runs on an M1; `native` is local-dev-only and never the default.
5. **Platform-exclusive backends state their floor** and their unproved-on-other-host status (the test lawbook's explicit-gap requirement).
6. **The floor moves only by law:** raising it is a deliberate amendment of this law, landed in the same cycle as the CMake change (Living Documentation Law; zero drift).
7. **A feature above the floor is a capability, not a floor move** (Capability Gating Law).

## Capability Gating Law (Runtime Features Above the Floor)

Every capability newer than the floor — a GPU feature (ray tracing on M3+), a CPU instruction set (dot-product, SVE/SME), a post-floor OS API — is a **runtime-probed capability**, never a floor change. Probed **once at cold boot**, cached in a bitset, then used or replaced by a **stated fallback**; a required capability is declared in the manifest and refused at the manifest gate on unsupported hardware.

1. The floor is the compile minimum; a capability never moves it.
2. **Probe once, cold, cached:** resolved once at boot (device / CPU / OS probe) into a bitset; hot paths branch on the cached bit and never re-probe.
3. **Every capability has a disposition — best-effort or required.** Best-effort: a stated fallback (RT absent → the Raster dialect). Required: declared in the manifest and refused at the manifest gate with the reason surfaced. A silently degraded required capability is a defect.
4. **No capability is assumed:** a dependent call site checks the cached bit first; an unguarded post-floor feature is the same defect as an unguarded post-floor API.
5. **CPU capabilities dispatch a variant; GPU capabilities select a dialect:** the floor variant is always compiled (`-mcpu=apple-m1`); the newer arm runs only when its bit is set. A GPU capability selects the pipeline dialect (graphvex's Vulkan/Raster/Null rows).
6. **The probe is owned, named and queryable:** host/CPU/OS capabilities live in the R1 host (`Capability`); device/GPU capabilities in the R3 driver (`graphvex`). Every capability has a stable name and a `has` query (Java Law; toString Law).

## THROW Law (Loud Cold Rejection)

`THROW(fmt, ...)` (`exception/throw.h`) is the recoverable diagnostic a cold, detected rejection uses to report itself: exactly `[vex] <file>:<line>: <message>` to stderr; the caller returns its safe error/default. It never unwinds or terminates.

Stderr output is synchronous and may block: never in a hot loop, signal handler, or teardown path requiring a bounded wait. A segfault before the check cannot be reported by THROW; tests and sanitizers catch such failures.

1. **Cold seams reject loudly:** the caller receives the safe default **and** one `THROW(...)` per failure — never a silent default.
2. **Hot paths never THROW:** a `;;HOTCODE` getter or any per-frame path carries no THROW; its rejection is a silent safe default. Observability is a cold obligation.
3. **One primitive, one format:** rejections go through THROW only — never a bare `fprintf`, `printf`, `perror` or ad-hoc print. Output is exactly `[vex] <file>:<line>: <message>`, greppable and machine-parseable.
4. **THROW does not unwind:** no `longjmp`, no `exit`; it reports synchronously, then the caller returns a safe result. Never claim stderr is nonblocking or allocation-free. A distinct, explicitly fatal host operation owns process-terminating teardown.
5. **THROW is not a control path:** it marks a problem; catching, escalation and terminal disposition belong to the R1 supervisor (Vertical Integration Law). The relational model has no exception stack.
6. **A THROW site is greppable and owned:** `grep -rn THROW` lists recoverable rejections; an owning test checks the emitted diagnostic and safe return. Normal-path tests fail on unexpected diagnostics; sanitizer and crash tests catch faults that never reach THROW.

## Native Pixel Law

Native hardware display pixels are the single, absolute, universal metric: windows, frames, swapchains, render targets, boards, and mouse/touch input events speak exclusively in **native physical hardware pixels** on the target display. Virtual platform coordinate spaces (AppKit "points", Windows DPI units) are encapsulated entirely at the platform boundary, preserving 1:1 hardware pixel determinism.

*Rationale:* on Retina/HiDPI, abstracting into logical points silently multiplies surfaces (an "800x600" window at 2x allocates 1600x1200), distorts visuals, and desynchronizes mouse positions from raster buffers. Engines and spatial interfaces need exact physical coordinates: `Window_setSize(ptr, 800, 600)` means exactly 800x600 hardware pixels, and mouse events map 1:1 to rendered pixels.

1. **Window dimensions in physical pixels:** creation (`Window(...)`, `Window_create`, `WindowDesc`) and sizing (`Window_setSize`, `Window_width`, `Window_height`) operate strictly in native pixels; backends divide/multiply by `backingScaleFactor` internally.
2. **Input events in physical pixels:** pointer and touch coordinates (`Mouse_pushMoveEvent`, `Mouse_pushDragEvent`, `Touch_*`) arrive in native pixels relative to the window's content top-left.
3. **Presentation seam:** `CAMetalLayer.drawableSize` and Vulkan/Metal render targets match the native pixel size 1:1.
4. **Multi-monitor scale transitions:** `Window_revalidate` recalculates platform points on DPI transitions to preserve the exact physical size and dispatches geometry update events.
5. **Points-explicit escape hatch:** when logical points are explicitly needed, classes provide explicit points accessors (`Window_setSizePoints`, `Window_getSizePoints`, `Window_widthPoints`, `Window_heightPoints`, `Window_getScale`).

## Timestamped Test Checklist Law

`/test-checklist.md` is the shared, per-file **automated lab evidence** ledger for executable tests: every test source that compiles and runs (`*_test.c/.m/.rs/.py/.ts`), registered runner scripts (`run.py`, `*_run.py`) and the shared harness (`test_support.h`). Documentation, markdown, images, configuration and production source are never inventoried — a row records a test you can actually execute. Each directory section is a GitHub-friendly Markdown table: filename, lab-tested status (✅ / ❌), actual last-check Unix timestamp, tested content hash, evidence/scope, description, result. No authors, agent names or session identifiers. Visual acceptance is reserved for the user. The local source is Git-ignored and published to the existing test-checklist Gist (https://gist.github.com/vex-graph/26f556f1a3a57b09d5c991d5ef9ef5ab), with downloaded-content verification in the same cycle. No tracked `tests/test-checklist.md` or duplicate root ledger exists.

1. **Consult before changing anything:** read the affected test rows and the test lawbook before work. A capability with no inventoried or executed test is untested, not exempt.
2. **Inventory every executable test:** run `python3 tools/test_checklist.py sync` when tests are added, removed, moved or changed; every non-ignored test unit gets a row, including untracked work. Empty sets still show untested. Inventories are not proof of execution.
3. **Only executed lab evidence earns ✅:** `python3 tools/test_checklist.py run --file <test-file> [...] --description <text> -- <command>`; named subjects must be executable test files (documentation/production files are rejected); the command must exercise each named test. Record scope, host/platform and gaps with `--scope`. Compilation proves only that scope; integration tests do not prove every linked file. Automated numeric/pixel assertions are lab evidence, not visual approval; galleries and interactive demonstrations are never run as verification (the user tests appearance first). `--kind visual` is rejected before execution.
4. **Real Unix time:** last checked is integer seconds since 1970 UTC captured at test completion; "never checked" is `—`, never a fabricated date or epoch zero; estimated historical times belong in explicitly labelled notes and confer no ✅.
5. **Evidence stays current and private:** a changed subject invalidates its ✅ even with an older timestamp; failures, skips, missing proof and stale checks are ❌ with an explicit reason; record exact hashes, command, scope and a useful description, never author identity or session metadata; avoid private details in commands; a pass on one platform is not proof on an untested platform, and a lab pass is never visual acceptance.
6. **Update in the same work cycle:** run applicable checks and update affected rows before calling work verified; `python3 tools/test_checklist.py check` rejects inventory drift and stale greens. Never bulk-promote files from test presence, recollection or a neighboring result.
7. **Stronger proof laws are preserved:** this ledger supplements the Test Segregation, Living Documentation, Per-File Battle Test, and Executable Evidence and Readiness laws without weakening any; test implementations remain in the tests tree, never production trees.

## Feature Implementation and Adversarial Proof Law

An accepted feature or proposal follows a complete development cycle — inspect and define its contract, create or edit the implementation, build aggressive tests around the actual behavior, execute them, repair defects, and record the proof before calling the work good or complete. A proposal is not an implementation, and compiling is not behavioral proof: plausible explanations and friendly examples can hide broken ownership, incompatible layouts, failed recovery and hostile-input crashes.

1. **Read before reasoning.** Every agent reads the complete current constitution before proposing or implementing work, then the applicable repo preferences, current test checklist, test laws and existing implementation. State clearly what exists, what is proposed, what remains unproved; never infer behavior from a name, comment, remembered result or intended architecture alone.
2. **Implement accepted intent.** Create or edit the owning classes of an accepted proposal, documenting the public contract and blueprints. Discussion-only requests stay discussion. Existing tests may guide work; test-only scaffolds and stubs do not deliver a feature.
3. **Attack the implemented contract.** Add or strengthen registered owner tests for every applicable public form, normal path, boundary, invalid input, overflow, truncation, wrong identity, stale reference, failure stage, recovery, ownership, teardown, cancellation, timeout and legal concurrency claim. Test preserved state after rejection; include growth, sharing, copy-on-write isolation and layout migration when offered. Explain inapplicable cases rather than pretending coverage.
4. **Execute, repair, repeat.** Run owner and relevant integration tests with assertions active and `-Wall -Wextra -Werror` for C targets; use applicable sanitizers, fault injection, deterministic inputs and bounded watchdogs. A failure requires a fix and rerun — never deleting the assertion, weakening the contract hidden from the user, or rerunning until a flaky test turns green.
5. **Close with evidence.** Record actual commands, scope, platform gaps and results in the test checklist; update affected readiness/documentation in the same cycle; run the checklist consistency check. Missing, skipped or failing proof remains an explicit gap; visual acceptance belongs to the user. Commit each class and separately owned document (Git Workflow Law); never call a proposal or partially proved feature production-ready.
6. **Earn backend trust under deliberate pressure.** Resource-owning backend proof follows the Deliberate Exhaustion and Backend Trust Law (test lawbook): actually exhaust resource boundaries, prove preservation/reclamation/recovery, test legal concurrent pressure with thousands of simultaneously live allocations where applicable. Operation churn is not concurrent occupancy. Publish interacting-factor coverage and remaining gaps; a green checklist or benchmark alone never grants production readiness, and no finite suite proves every possible thread schedule.

## Transparent Competency Law

Every repository's documentation is a **live statement of its current platform and competency**, not a pitch. Any tracked `.md` file — the README first among them — plainly and currently states what the repository actually is and does: tier and role, what is implemented, what is stubbed or planned, on which platforms it is proven, known gaps. A document may not assert a capability the code does not have; it is updated in the same cycle as any change it describes, even when revising it costs significant context. Multi-repo ecosystems rot silently when documentation lags reality — a README promising a header-stub feature means a reader builds on a capability that is not there. Honest, current competency is load-bearing in an AI-pair-programmed system; token cost is not an excuse to leave a document lying.

1. **Every tracked `.md` is a live document:** READMEs, CONTRIBUTING, architecture pages, repo lawbooks, wiki rows — maintained with the code they describe, same cycle, never a deferred "docs later" batch. The Living Documentation Law's blueprint, preferences and readiness surfaces are the mandatory minimum; this extends the discipline to every `.md`.
2. **Two required README sections:** a **`## Current State`** honest assessment near the top — what the project is right now: role/tier, implemented and proven, stubbed/draft/planned, platforms actually proven (untested platforms stated plainly as unproven); and a **`## Scope and Limitations`** section at the bottom — what the project covers and deliberately does not, scale/platform/performance limits, known gaps. `Current State` is where it stands today; `Scope and Limitations` is the boundary it will not cross and why. No markdown asserts shipped behavior the source does not deliver.
3. **Evidence-based status:** backed by the readiness matrix and `/test-checklist.md`, never inferred from names, diagrams or intent; a capability with no executed proof is described as unproven.
4. **Same-cycle update, even when token-expensive; reading and revising a large document is part of the change.**
5. **Drift is a defect:** stale, inflated or capability-implying documentation is fixed in the cycle it is noticed — never waived for document size or fix cost.
6. **Assess independently; do not self-certify:** a competency claim is reviewed by a reader other than its author — another session/agent, or a mechanical document-owner test where one exists; a session owning a repository invites a peer session to assess its README (or joins the pass) and records the reviewer's findings. Unverified self-flattering status is drift; a green claim with no independent check is unproven.

## Groundedness Law (Read Before You Assess)

No claim about code is made from inference. Before assessing behavior, a bug, a contract, a document's competency, or an architecture, the assessor reads the actual source in the current tree (and its tests/headers where relevant). Names, comments, READMEs, diagrams, remembered results and stated intent are not evidence — the read source is. Guessing is cheaper than reading, which is exactly why it silently corrupts every downstream decision; grounding every assessment in a real read is what makes the tree trustworthy, and token cost never overrides it.

1. **Read before you assess** — behavior, bugs, contracts, readiness and document competency start from the owning source in the current tree.
2. **Ground every claim** — a statement of behavior cites what was read; unavailable scope is reported as unverified or a gap, never inferred.
3. **A competency claim requires the repo's real source** — a `## Current State` is written only after reading that repository's actual source; a docs-only read is an unverified claim, labelled as such.
4. **Token cost is not an excuse** — reading the whole relevant scope, however large, is mandatory.
5. **No remembered green** — re-read the current source and re-run the tests before repeating any status or pass claim (Timestamped Test Checklist Law).
6. **Report the read boundary** — state what was read and what was not, so the reader knows how far the grounding reaches.

## Exhaustion Loudness Law (No Silent Exhaustion)

When a backend that owns finite storage cannot satisfy a request — an arena with no free slot or bump room, a full pool/ring/queue, an exhausted registry, a refused OS handle, a bounded buffer with no capacity left — it reports the refusal through the observable channel, not merely the safe default. The report is **loud but bounded**: the first refusal in an epoch emits one `THROW(...)` naming the owner, the request and the bound reached; every further refusal in that epoch increments a **queryable count**. An epoch ends at the owner's `init`/`create`/`reset`/`freeAll`/`destroy`, which clears both.

*Rationale:* silent exhaustion produces *plausible* corrupt state (a half-built scene, a lost edit) that surfaces far from its origin; an unbounded reporter drowns the signal in thousands of lines. Report **once, count always** gives one unmistakable line and an exact number for tests — legible to human and agent, no flood, no silence. This is Tier-1 trust: R5 interactables and R6 superapps allocate through R1–R4 backends, and a backend hiding its own exhaustion is not safe to build a product on.

1. **No silent exhaustion.** Every finite-storage owner exposes an observable refusal: the caller receives the safe default (`nullptr`/`false`/a `Try` error) **and** the owner records the event. Returning the default with no record is a defect, not an optimization.
2. **Report once per epoch; count always.** The first refusal emits exactly one diagnostic naming the owner, requested size/quantity and bound; later refusals in the epoch change only the counter. A failing hot loop never floods stderr; a single fault is never invisible.
3. **The count is queryable and resets with the epoch** (`Memory_exhaustionCount`, `MemoryArena_exhaustionCount`, `Transient_exhaustionCount`, ...); init/create/reset/freeAll/destroy start a fresh epoch and zero it. Tests assert the count deterministically instead of parsing stderr.
4. **Name the cause and the quantity:** `arena exhausted, request 2097152 bytes (bump used 33554416/33587200)` — a bare "failed" or a numberless banner is not a report.
5. **The return contract is unchanged:** callers still handle `nullptr`/`false`/`Try`; the report is for the human and the tool, the return for the program.
6. **Typed reasons where a reason exists:** a category (no memory, bounds, overflow, absent) carries a named code (a `TryCode`) alongside the diagnostic — never a bare boolean or magic number.
7. **The hot path stays hot-minimal (managed exception):** the *success* path of a hot operation adds no logging, allocation or work; only the *failing* path reports, at most once per epoch. This clause explicitly reconciles this law with the Cold-Strict, Hot-Minimal Validation Law and the Hot-Path Minimal Guard Law (Conflict Triage Law).
8. **Exhaustion proof is a release gate for interactables:** a backend promoted for R5/custom-application use has an executed owner test that actually reaches its boundaries, asserts the counted refusals, checks the one-line diagnostic, and proves recovery — the Deliberate Exhaustion and Backend Trust Law (test lawbook) is the proof procedure; this law is the production contract it proves.

## Voice Preservation Law (The Author's Voice Is Not Yours to Edit)

The author's **voice** in comments, blueprints, docs and commit messages — jokes, asides, "lol", "haha", cheesy or cliché lines, deliberate bad grammar, informal spelling, lowercase shouting, ALL-CAPS emphasis, parenthetical snark, and every other human fingerprint carrying no technical meaning — is **content, not noise**, preserved verbatim by every contributor, human or AI. Tidying, "professionalizing", "cleaning up" or deleting it is a defect of the same weight as deleting a comment that explains the code.

*Rationale:* this ecosystem is written by an AI-human pair; the agent writes the boilerplate, the human supplies the judgment, the taste — and the voice. Silently rewriting `// zero lol` into `// zero` loses the only marker a human was present, loses trust in every diff an agent touches, and destroys a real provenance signal (human-written and model-generated text read differently, and that difference is information). Nothing is degraded by a joke in a comment; something is always lost when one is removed. Voice is the author's fingerprint — the one thing an AI pair must never launder.

1. **Never edit the author's voice** — jokes, asides, "lol"/"haha"/"(:", cheesy or cliché phrasing, deliberate typos, informal grammar, lowercase emphasis and similar human marks stay exactly as written, punctuation included.
2. **Cleanup passes exclude voice:** a refactor, rename, reformat or documentation sweep may change code, identifiers and *technical* prose, never the human register. When a symbol moves between files, its comment moves with it, word for word.
3. **Grammar is not corrected:** spelling/grammar fixes confine to text the same cycle actually authors; pre-existing informal or wrong text stays.
4. **When in doubt, keep it:** a line whose technical meaning is nil is still not yours to delete; if a comment genuinely misdescribes behavior, fix the *meaning* and leave the *voice*.
5. **Distinct from the Authorial Intent Law:** `// INTENTIONAL(vex):` documents a deliberate *technical* strangeness; this law protects the author's *voice*. One line may carry both; neither replaces the other.
6. **Deletion is a defect to reverse:** an agent finding the author's voice was stripped by an earlier pass restores it verbatim where recoverable and reports that it did — never silently re-cleans what a previous pass already flattened.
7. **The one-line test:** would the author recognize this line as theirs? A diff making a comment more boring, more generic, or more obviously machine-written is wrong.

## Value Return Law (No Caller-Provided Destinations)

Full text lives as a named clause of the Semantic Consistency Law above (citation: `Semantic Consistency Law (Value Return)`). Every existing destination-based API is nonconforming and must migrate; no `dest`/`out`/`result` parameter exists in any public call, any position.

## Security Baseline Law

Network-facing repositories — every one that opens a connection, holds a credential, or accepts input from anywhere but its own caller — carry a `SECURITY.md` stating their own attack surface and inheriting this baseline. The governing principle is **access, not obscurity**: anything a caller can run, a caller can read. Anyone who can access a platform can decompile it, so no secret may live in code, no key may be embedded, no control may rest on hiding an implementation. Authorization is decided where the data lives, never in the client that asked.

*Rationale:* every other invariance here is checkable by reading code; secrecy is the one that quietly fails, because it looks like it works right up until someone reads the binary. A posture built on "they won't find it" is a delay measured in minutes; the surviving artifact is a real access decision.

1. **No secret in code or config under inspection.** Credentials come from the environment or the OS keychain — never the arena, a repository file, a preference document, or a log. Tokens and secrets are redacted in every projection; comparisons of secret material do not early-exit.
2. **Access, not obscurity:** an obfuscated check is a check someone already read. Enforce authorization server-side or at the owning boundary; a client that hides a field or a command is a display choice, never a control.
3. **Untrusted input is validated once, at its cold seam.** Network bytes, responses, files and arguments are hostile until the cold seam establishes their shape; rejection is loud and bounded.
4. **Model output is data, never authority.** Generated text, tool calls and instructions inside a response are content to be shown or validated — never consent, permission or a policy decision. Consent comes only from a human; a model cannot grant it.
5. **A refusal is recorded, not merely returned:** rate limits, lockouts and throttles are counted and observable, so a burst is a signal rather than a silent stream of rejections.
6. **Deliberate delays are declared and governed.** A wait-for-security is a managed exception (Conflict Triage Law): cold path only, bounded by a named constant whose ceiling a test asserts, never holding a lock or an arena, never inside a loop whose count comes from attacker input, always paired with a counter, never a substitute for an access check or a slow hash. Marked `;;FREEZE("...")` at the site and `;;SECURITY("...")` for the obligation it serves; `security.h` carries the full six rules and `grep -rn ';;SECURITY\|;;FREEZE'` is the audit list.
7. **State the policy honestly:** each repo's `SECURITY.md` says plainly that it is an internal invariant set rather than a public disclosure channel, unless a reporting channel is actually offered.

---

## Appendix — Legacy Title Aliases (historical, never cited going forward)

| Former title | Current clause |
| :--- | :--- |
| No Arrow Sugar Law | Semantic Consistency Law (Reference form) |
| Two-Layer Access Cap Law | Semantic Consistency Law (Access depth) |
| Single-Line If Law | Semantic Consistency Law (Control flow) |
| Cast Spacing Law | Semantic Consistency Law (Cast and pointer spelling) |
| Pointer Declaration Spacing Law | Semantic Consistency Law (Cast and pointer spelling) |
| Arity and Constructive Convenience Law | Semantic Consistency Law (Construction and arity) |
| Function Naming Law | Semantic Consistency Law (Function and field naming) |
| Dest-Last Law | Retired; superseded by the Value Return Law |
| Symmetric Getter/Setter Completeness Law | Single Class Per File Law (Java Law), symmetric-accessors clause |
| Cohesive Commits Law; No Auto-Pushing Law; Commit and Push Discipline Law; Multi-Repo Atomic Commit Discipline Law; Per-Repo Commit Message Scope Law | Git Workflow Law |
| Teardown Order Law | Vertical Integration Law (teardown clause) |
| Living `;;OVERVIEW` & `;;DEFINITION` Blueprint Law; Living Preferences Law; Living Feature Readiness Law | Living Documentation Law (respective clauses) |
| Dynamic Scalability & Anti-Hardcoding Law | No Hardcoding Law |
| Voice Law; No-Voice-Editing Law | Voice Preservation Law |
| Freeze Law; Deliberate Delay Law | Security Baseline Law (deliberate-delay clause) |
| Executable Evidence and Readiness Law; Per-File Battle Test Law | Test lawbook governing proof; remainder absorbed by the Feature Implementation and Adversarial Proof Law and the Timestamped Test Checklist Law |

*Cite every law by its Title.*


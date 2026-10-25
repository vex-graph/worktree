# Vexgraph blockers and deferred decisions

**Reviewed: 2026-10-08.** A consolidated backlog covering the workspace,
ecosystem repositories, applications, tooling and available development discussions.

Items include deliberate deferrals, implementation gaps, missing proof and
unresolved design decisions. Their inclusion does not imply oversight or forgotten
work. This backlog records outstanding work; it does not authorize implementation,
cloud access, hardware uploads, deletion, installation or repository pushes.

## Primeagen — the real thing (planned 2026-10-13)

Direction accepted: Primeagen becomes the actual client — own users, own servers,
own channels, own messages, own models, over **darkbase (R3)** and **own API
keys**, with no borrowed agent host as the product path. Plan of record:
`personal/primeagen/PLAN.md`. Slice order S0 live frame → S1 bottom input →
S2 darkbase M1 store → S3 entities over darkbase → S4 direct provider default →
S5 live database.

| # | Type | Item | Status |
| :--- | :--- | :--- | :--- |
| P1 | BUILD | S0: wire `cli/screen.c` into the live app; retire the direct-ncurses view and its old-layout assertions | ⬜ |
| P2 | BUILD | S1: bottom `TerminalInputLine` in the frame (typing, caret, backspace, submit, bounded refusal) | ⬜ |
| P3 | BUILD | S2: darkbase M1 — entity model, byte-native rows, zero-alloc scans, B-tree pages, reactive programs, store/executable split | ⬜ |
| P4 | BUILD | S3: User/Server/Channel/Message entities + Primeagen store adapter over darkbase's `Database*` | ⬜ |
| P5 | BUILD | S4: direct API-key provider path as the default; OpenCode session demoted to optional diagnostic | ⬜ |
| P6 | BUILD | S5: live `.vexdb` boot/open/migrate/teardown | ⬜ |
| P7 | DECIDE | D1 credentials: checkout `.env` only, or the OS keychain as the durable home? | ⬜ |
| P8 | DECIDE | D2: is a Server one endpoint+key, or a provider with several endpoints/models? | ⬜ |
| P9 | DECIDE | D3: are Messages append-only forever, or is there an edit/delete revision? | ⬜ |
| P10 | DECIDE | D4: multi-user locally, or one identity per install? | ⬜ |
| P11 | DECIDE | D5: does Primeagen ever sync with another install (identity globally unique), or only talk to model endpoints? | ⬜ |
| P12 | DECIDE | D6: which store events genuinely need reactive programs? | ⬜ |
| P13 | DECIDE | D7: confirm the first `.vexdb` format version and that no migration is needed before v1 | ⬜ |
| P14 | PROVE | Page-level Store has isolated optimized/C-sanitizer recovery proof; full relational Database/Headless workflow and production backend trust remain unproved | ⬜ |

## darkbase — make DARKBASE (noted 2026-10-13)

**darkbase is not done.** What exists is a *dump-file* store: `darkbase-engine` has
M1 (reflection `Struct` entities bound to caller-owned live rows, a dest-last
`DatabaseResult` cursor) and M2 (`Database_save`/`Database_load` — a 64-byte `VEXDB01`
header, flat row bytes by `Struct.size`, a trailing CRC32). That format writes the
**whole store** on every save: cost is O(entire database) per appended row. It is not
a database file; it is a snapshot. "DARKBASE" means finishing it into the real thing:
a paged, crash-safe, single-file, memory-mapped system of record with an explicit
residency tier.

The new `store/store.{h,c}` is a separate working page-level durable primitive,
not a change to that legacy `Database_save`/`Database_load` path. One file contains
bootstrap, embedded redo and mapped data; release/reuse and recovery owners pass
through `tests/darkbase-engine/store/run.py`. It retains all redo and refuses on
the caller-selected journal bound; safe checkpoint recycling and Database/Headless
integration remain open. The global workspace graph is still blocked before owner
execution by the post-migration Vexspoke ownership ratchet; its baseline was not
weakened. The installed Rust standard library also emits macOS27-vs-14 deployment
warnings, so macOS14 runtime closure is not established.

**Decided already** (do not re-litigate): fixed virtual reservation chosen at create,
mapped once (no re-map, pointers survive growth); **sparse, step-wise growth** with a
**free list** of released ranges so the file plateaus; allocate-before-publish; never
expose past the committed length; one file per database with segregation a deployment
choice; **Rust owns the mapping, C reaches it through one thin extern-C ABI**; C owns
the stable ABI, Rust owns new typed storage behind it.

| # | Type | Item | Status |
| :--- | :--- | :--- | :--- |
| D1 | BUILD | C ABI over Rust `FixedMappedFile`: extern-C surface + canonical C header + real C clients in the owner suite (debug and release) | ⬜ |
| D2 | BUILD | `GrowableMappedFile` per its law: fixed reservation, sparse step growth, allocate-before-publish, free-list reuse, never expose past committed | ⬜ |
| D3 | BUILD | Connect the implemented sealed Page/Store bootstrap and replay-derived allocation state to a relational catalog/root; legacy Database still uses whole-file snapshot CRC | ⬜ |
| D4 | BUILD | Page table / B-tree over pages; a row's address is a logical `(pageId, slot)` **re-resolved** through the tree, never a cached byte offset | ⬜ |
| D5 | BUILD | Safe recycling/checkpoint compaction for Store's retained embedded redo; append/sync/apply/reopen and child-exit/torn-page repair owners exist, but journal capacity currently exhausts | ⬜ |
| D6 | BUILD | Integrate Store's proved durable free-page reuse into relational entity/index ownership; no row generation/stale-handle contract exists yet | ⬜ |
| D7 | BUILD | Growth in place: pages appended inside the reservation; retire the O(store) `Database_save` dump path | ⬜ |
| D8 | BUILD | Residency tier — the manual hot path (`pin`/`release`/prefetch) over the mapping (a pin, not a copy); cold path slower but never unavailable; `Reactive` fanout; Exhaustion Loudness on memory pressure | ⬜ |
| D9 | BUILD | Structured query (explicitly not SQL): B-tree range scans and cursors beyond the current single select | ⬜ |
| D10 | BUILD | Reactive store programs (`beforeInsert`/`afterInsert`/`onCommit`) on the cold admission path only | ⬜ |
| D11 | BUILD | The workbench: TUI (R1 `CommandLine` + determinant cells) and a CLI front over one shared model — the pgAdmin-shaped surface | ⬜ |
| D12 | DECIDE | R4 `darkbase` interface tier — reserved with a trigger: graduates only when a SECOND independent app embeds the store-interaction model | ⬜ |
| D13 | DECIDE | First `.vexdb` format version, and whether M2 dump files need a migration path into the paged format | ⬜ |
| D14 | DECIDE | Segmentation policy: when (if ever) to split beyond one file, and by time-append-only — never per-entity | ⬜ |
| D15 | PROVE | Expand page-level Store proof beyond 48 live pages/two capacity limits/three child exits/five injected IO stages: allocator and real OS failures, Rust instrumentation, platform floor and full relational workflows remain gaps; legal use is caller-serialized, not concurrent writers | ⬜ |
| D16 | PROVE | `personal/darkbase` has no remote: the consumer host is committed locally only | ⬜ |

### Darkbase vision TODO — turn the seven gaps into one usable system

These are the seven product gaps from the current Darkbase assessment, in dependency order. They are open work, not claims that the listed behavior already exists. First target: one local database workflow that defines a reflected entity, writes and queries it through the durable store, closes/reopens it, and applies the Headless access gate. Keep the R3 Store separate from R4 identity/transport ownership.

| # | Type | TODO | Exit evidence |
| :--- | :--- | :--- | :--- |
| V1 | BUILD/PROVE | Connect `Database` schemas and owned rows to the page-level `Store`; persist/reopen the catalog and rows without routing through the legacy whole-file snapshot. | A public Database workflow survives close/reopen and Store recovery; rejected schema/row admission preserves existing data. |
| V2 | BUILD/PROVE | Deliver the structured, non-SQL data contract: catalog lookup, field predicates/projection, cursors, and the first useful index/range query over persisted entities. | Registered owners cover empty/one/many results, boundaries, growth, missing fields/entities, and stable result lifetime; query allocations match the stated contract. |
| V3 | DECIDE/BUILD/PROVE | Define transaction scope and implement atomic multi-page mutation with explicit commit/rollback and writer exclusion; individual page commits are not database transactions. | Fault/crash tests at each commit stage prove all-or-nothing visibility after reopen, exact acknowledgement semantics, and preserved prior state on rejection. |
| V4 | BUILD/PROVE | Design and implement safe WAL checkpoint/recycling so retained embedded redo does not permanently exhaust; preserve the current refusal behavior until safe recycling is proved. | Repeated checkpoint/write/reopen cycles prove no loss or duplicate replay across injected failures and journal wrap/reuse boundaries. |
| V5 | BUILD/PROVE | Complete the R4 Headless security/admin workflow: remove or explicitly replace the default bootstrap credential; prove TOTP/setup-URI behavior; add protected enrollment/recovery, durable replay state, per-client sessions, entity grants, sensitive-field enforcement, step-up, and auditable failures as the first scope requires. Integrate admin state with durable Store only through public Database contracts. | Registered tests exercise bootstrap/login/enrollment/replay/recovery, authorization allow/deny, expiry/step-up, secret redaction, persistence failure and restart. Vexspoke TOTP/OtpAuth code exists, but its checklist owners and the Headless service owner are currently ❌; primitives alone do not complete service security. |
| V6 | DECIDE/BUILD/PROVE | Specify Darkbase's connection descriptor/URI and implement its parser and admission policy. Decide embedded-file versus service endpoint forms; do not treat Vexspoke URL builders or API Haven's REST parser as a Darkbase connection API. | Public contract and owners cover malformed/oversized input, path/endpoint policy, credentials redaction, supported forms, and wrong/missing database identity. |
| V7 | PROVE | Close the end-to-end and backend-trust evidence gaps: wire all owners, exercise exhaustion/recovery, inject allocation/OS failures, and run supported platform/runtime checks without weakening the global ownership ratchet. | Checklist records exact executed scope and gaps; a fresh end-to-end owner passes; macOS 14 and other claimed platforms are separately proven; no production-ready claim exceeds the evidence. |

**V2 progress:** `Database_queryEqual` resolves one reflected Field, validates
its byte span against `Struct.size`, and returns a cold cursor over exact-byte
matches. `Database_storeCatalogEntry` now returns copied persisted name/stride/
row-count metadata by index after validating the committed page chain. Owners
cover match counts, schema/value rejection, out-of-range discovery and cursor
ownership. `Database_indexBuild` now declares and builds the in-memory int32
index for a `REFLECT_FIELD_INDEXED` field; `Database_queryInt32Range` uses it when
present and scans otherwise, and an insert marks it stale for the next query to
rebuild. `Database_saveStore` now persists each declared index after its entity's
row span inside the same catalog payload, so rows and index publish under one
root-page commit; `Database_loadStore` re-validates ordering, `rowIndex` range and
every key against its row, and refuses a same-stride schema whose indexed field
moved. V2 remains partial: no schema
reconstruction, ordering or page-level incremental index exists yet, and named
field resolution is its first projection piece. See the Database owner rows in
`metadata/gists/test-checklist.md`.

**V1 progress:** the Database now uses a dedicated reflected-catalog/row-span
page-chain encoding through the Store, not the legacy M2 snapshot parser. Its
owner test proves save/reopen/load, wrong-stride schema rejection preserving a
pre-existing target row, bounded-journal refusal preserving the prior root/image,
and child-exit recovery after the root redo marker sync. The strict optimized C
ASan/UBSan owner passed on macOS arm64 (checklist timestamp `1792053120`);
the linked Rust archive is not sanitizer-instrumented and its archive reports a
newer macOS deployment target. This closes the V1 scope only: it remains a
whole-image adapter with retained prior pages/WAL, not incremental row storage,
multi-page transactions, query/index support, or Headless integration.

| T1 | FIX | `tools/test_checklist.py run` records ✅ when the command **SKIPs**: `b test` exits 0 on a skip, so a skipped owner (e.g. `keychain_test`, which needs `DARKBASE_KEYCHAIN_TEST=1`) was recorded as passed. The ledger must detect a skip and record ❌, per the Timestamped Test Checklist Law. | ⬜ |

| T2 | DECIDE | Two repositories own the relative include path `oop/type.h` (vexspoke, darkbase-engine; samplerate too). It works only while each repo's own `src` is first for its own translation units — proven by compiling vexspoke's `exception.c` with darkbase's `src` first, which lost `TYPE_EXCEPTION_SINGLETON`. Decide: keep the convention with the per-target rule enforced, or rename the registry file to be repo-qualified (`src/oop/darkbase-type.h`, matching darling's `src/c23/darling-type.h`). | ⬜ |

## How to use this

| Type | Meaning |
| :--- | :--- |
| **DECIDE** | a contract or product choice still needs to be settled. |
| **BUILD** | accepted direction exists, but the user-facing feature is unfinished. |
| **FIX** | inspected code or documents contradict the intended contract. |
| **PROVE** | functionality may exist, but the relevant executed evidence is missing. |
| **RECHECK** | historical concern; do not assume it still reproduces. |

- Set an item's status to ⬜ (open) or ✅ (resolved) only with the associated decision or evidence. Dates/emoji in older
  conversations are not current proof. This document does not supersede
  `preferences/PREFERENCES.md`, repo-local laws, the readiness Gist or `test-checklist.md`.
- Priority means suggested dependency order, not permission to start every item.

### Coverage and limits

Inspected the current repository inventory, READMEs/readiness pages, applicable
lawbooks, selected implementation seams, current checklist, agent bus and the
latest retrievable messages of **50 listed sessions**. Partial API responses were
recovered where possible. This was **not** a full replay of every message or a
fresh runtime/sanitizer/security audit. Deleted sessions, other projects and
repositories outside this checkout are not recoverable from this inventory.
The session register below makes incomplete history explicit. No private lesson
contents, credentials or raw conversation exports are included.

## Start here: highest-leverage unfinished seams

### Scheduled terminal consumer follow-up

| Status | Type | Item | Detail |
| :---: | :--- | :--- | :--- |
| ⬜ | BUILD/PROVE | Primeagen consumes Determinant + CommandLine | The R1 terminal-application kind `CommandLine` (owned TTY, always-honored resize, swappable app seam) and the R3 Determinant toolkit now exist. Next: build the R3 `TerminalApp` + widgets from `_notes/_self/tui.txt`, then migrate Primeagen onto them while preserving host-owned conversation, draft, consent and pipes. Reproduce the reported restart-required `/update` defect before diagnosing it; prove a changed view/command in the same production process, incompatible-candidate preservation, successful retry and resolved rollback. Callback substitution alone is not this integration proof. No live provider call or visual acceptance is implied. |
| ⬜ | BUILD/PROVE | R6 superapp workflows | Anti and Semicolon compose R1–R5 public contracts without lower-tier implementation ownership. Semicolon’s future Language/b/Primeagen integration and Anti’s IDE/DAW/drawing workflows remain blueprints; Primeagen stays standalone R5. |

| Priority | Task | Why it unlocks other work |
| :--- | :--- | :--- |
| P0 | Real string-to-glyph rendering, measurement and a usable Label | Almost every control and all editor/studio interfaces need text. |
| P0 | HTTPS transport, status/error semantics and trusted authentication | Drive backup, remote APIs and real session authentication cannot work on descriptors alone. |
| P0 | Persistence format, failure-safe publication and durability contract | Saving raw rows is not safe persistent identity, crash recovery or transactions. |
| P0 | Resident R2 lifetime and reload pins/exclusion | Hot reload must not unload code or destroy storage still in use. |
| P1 | ScrollPanel attachment/input, focus and keyboard routing | A painted viewport is not yet a ready-to-use interactive UI. |
| P1 | Automatic ordered filter/tree planning and completed scene handoff | Static gallery GPU scopes are not general widget composition. |
| P1 | FileSession/DirectorySession plus real local workflows | Sesh currently admits metadata and schedules snapshots, not directory synchronization. |
| P1 | Owner-test coverage, actual platform runs and truthful status | Broad historical green claims hide missing or differently scoped proof. |
| P2 | One complete R5 workflow before more catalog expansion | A small useful editor/studio loop is more valuable than additional empty feature names. |

## Decisions that still need laying out

| Status | Type | Item | Detail |
| :---: | :--- | :--- | :--- |
| ⬜ | DECIDE | first deliverable | pick one first usable workflow and its acceptance criteria: readable interactive UI, local database, backup/restore, mini editor, drawing loop or audio project. Do not make every roadmap a release gate. |
| ⬜ | DECIDE | identity lifecycle | who creates/persists client, workspace, resource and operation IDs; uniqueness scope; account linking; device reset; name reuse; tombstones; history retention and deduplication epochs. |
| ⬜ | DECIDE | synchronization authority | single-writer first, or a backend enforcing authorization and revision/CAS? Define conflicts, retries, deletion, rename, baseline retention and offline reconciliation. Local counters are not distributed CAS. |
| ⬜ | DECIDE | persistence meaning | when is a save acknowledged, what survives a crash/power loss, what can be recovered, and what is the backup/restore policy? Separate buffered flush, durable sync, atomic publication and transactions. |
| ⬜ | DECIDE | portable schema | format version, byte order, schema hash, field encoding, pointer/reference relocation, functions rebound by name, evolution/rollback and incompatible-version rejection. |
| ⬜ | DECIDE | C/Rust migration boundary | native Memory ABI remains supported; define which collection moves next and its parity gates. Rust pools are not an interchangeable native allocator, and Rust TypeId is not persistent engine identity. |
| ⬜ | DECIDE | mapped storage consumers | fixed-extent Rust FixedMappedFile now separates cold mapped bytes from hot arenas, uses Rust borrows plus unsafe external-file exclusion, and has explicit flush/sync. Resize, mapped C ABI, persistent file identity, enforced hostile-file ownership, database recovery and supported-host proof remain consumer/follow-through work. |
| ⬜ | DECIDE | UI policies | text ownership, editable document model, focus traversal/modal capture, nested-scroll consumption, layout measurement, attachment ownership and accessibility expectations. |
| ⬜ | DECIDE | filter ownership | per-element versus deliberately shared Property stacks; immutable parameter leases/COW; invalidation of every referrer; nested backdrop prefix meaning; explicit unsupported-capability disposition. |
| ⬜ | DECIDE | operational limits | configurable defaults versus justified safety bounds, observable backpressure, deadlines and cancellation disposition. Historical fixed room/queue/FPS targets need review under the No Hardcoding Law. |
| ⬜ | DECIDE | deployment | standalone runtime dependency packaging, application manifests, capability requirements, signing, updates, rollback and supported-host proof. |
| ⬜ | DECIDE | product names | Darkbase library versus executable naming; Samplerate sound engine versus Impedance workstation; create a Darling Editor checkout only when its app scope is authorized. |

## R2: relational-engine

Source: `../host-behavior/relational-engine/README.md`,
`relational-engine-preferences.md`, `src/nio/`, `src/io/`, `src/type/`, `rust/`;
readiness: [relational-engine Gist](https://gist.github.com/vex-graph/6943f92acb931b25dad1073c46da6ce7#file-relational-engine-md).

**Already real:** engine-owned production native IO/NIO, compatible Memory C ABI,
shared type algebra, Rust byte/string publication, stable chunks, named bindings,
TypedChunk/TypedPool and native C span search. Do not redo the ownership migration.

| Status | Type | Item | Detail |
| :---: | :--- | :--- | :--- |
| ✅ | BUILD | fixed-extent Rust FixedMappedFile primitive | Implemented in rust/src/nio/fixed_mapped_file.rs; macOS arm64 debug/release owners and unsafe/arity/type/borrow negatives pass. Application retains the file/mapping until close/drop and reads checked offset/count byte spans. Caller must exclude external mutation/truncation; no resize, mapped C ABI, database format or transaction. Page faults and IO have no hard latency bound. |
| ✅ | BUILD | create-new physical byte-file preallocation | Rust io/PreallocatedFile reserves the caller extent with no sparse fallback and checks allocated OS blocks. Real macOS arm64 debug/release proof covers decimal 1 GB, offset bit changes/sync/reopen, existing-path preservation and reservation failure cleanup/retry. Retained-descriptor mapping avoids reopening the pathname. Caller supplies a trusted/stable parent; no implicit Application Support artifact. APFS COW/snapshots may still require space on later edits. Linux source unproven; Windows Unsupported; OS mapping/sync/cleanup-error injection remains a gap. |
| ⬜ | PROVE/BUILD | mapping follow-through | OS mapping/flush/sync-failure injection, huge-file admission, Rust sanitizer instrumentation, Windows and macOS14 runtime proof remain gaps. Enforced hostile-file ownership, mapped C ABI and resize are not offered; database publication/recovery and persistent file identity belong to consumer integration. |
| ⬜ | BUILD | identity table geometry | TypedChunk/TypedPool now reject stale owner-local generation handles, preserve history across backing release and retire exhaustion; C RowPool adds wrong-owner rejection. Proposed compact identity-table geometry/metadata encoding and persistent cross-restart identity remain unfinished. Raw indices remain reusable locations, not identities. |
| ⬜ | BUILD | object/name integration | connect names to value lifetime and destruction without conflating VariableSlot `[name,value]` with StringSlot `[self,name]`. |
| ⬜ | BUILD | bulk/scratch/VM | contiguous bulk APIs, resettable typed scratch, reserve/commit and mapping are separate contracts; stable chunks are not one giant contiguous array. |
| ⬜ | BUILD | file toolkit | safe directory traversal, buffered/asynchronous operations, indexing/watchers and manifest-backed persistent objects remain future slices. HotFileSys currently has lifecycle proof, not working watching. |
| ⬜ | BUILD | codecs/virtual storage | ZIP/7z, ASTC and GPU storage-transfer references are planned areas, not automatic compression or SSD-to-GPU support. |
| ⬜ | PROVE | resident reload | real two-consumer-module reload retaining engine code/storage; exclude API users before release; test teardown and failed migration rollback. |
| ⬜ | PROVE | Rust/native boundary | Rust instrumentation, allocator/OOM behavior, complete legal concurrency/fault matrix, Windows and performance. C-client ASan/UBSan does not instrument Rust or prove native allocator parity. |
| ⬜ | PROVE | permission-bound clipboard | mutation was skipped without lab permission; do not turn the skip into a pass or mutate the clipboard implicitly. |
| ⬜ | RECHECK | historical native allocator/File concerns | old research raised fallback tracking, stale headers, alignment, scratch arithmetic, stream position and close errors. Some native owners were strengthened later. Reconcile each concern with today's implementation and tests rather than relisting all as live defects. |

## R2: vexspoke

Source: `../host-behavior/vexspoke/src/net/http.c`, `src/relational/symbol_table.c`,
`src/input/`, `src/reactive/`; readiness: [vexspoke Gist](https://gist.github.com/vex-graph/6943f92acb931b25dad1073c46da6ce7#file-vexspoke-md).

| Status | Type | Item | Detail |
| :---: | :--- | :--- | :--- |
| ⬜ | FIX/BUILD | HTTPS admission | Http_perform still returns false for https. Wire verified TLS, hostname/certificate verification, bounded transport operations, cancellation and distinct transport errors. A standalone TLS backend is not HTTP integration. |
| ⬜ | PROVE | hostile transport | DNS/connect/TLS/reset/short-read/timeouts, framing/chunks, overflow, redirect policy and failure preservation at real cold seams. |
| ⬜ | RECHECK | CAS claims | SymbolTable_compareAndSetPointer uses ordinary compare/assignment, not atomic CAS. Confirm its synchronization contract and correct any thread-safe/lock-free roadmap claims; do not infer atomicity from the name. |
| ⬜ | BUILD | reflection convergence | settle remaining identity-cell/shelf/name integration and C/Rust ownership. Keep reflective lookup cold; retain validated pointers for hot consumers. Old reflection plans are not the current ABI. |
| ⬜ | BUILD | event-stream gestures | drag/scroll/zoom bindings need their event-driven resolver; per-frame tap polling alone does not deliver these gestures. |
| ⬜ | BUILD/PROVE | non-Apple audio/input/system seams | distinguish safe fallback stubs from actual native audio behavior and prove supported hosts separately. |
| ⬜ | PROVE | per-file contracts | remaining collection growth/overflow, pointer legitimacy, ring/spin contention and reactive callback-affinity evidence. |
| ⬜ | FIX | readiness drift | reconcile contradictory TLS entries, historical memory/name/header geometry, clipboard ownership and blanket green claims against current owners. |

## R3: graphvex

Source: `../drivers/graphvex/COMPOSITOR.md`, `FILTERS.md`,
`src/graphics/graphics.c`, `src/vulkan/vk_renderer.c`, `src/compositor/`.

**Already real:** numeric CPU reference, Vulkan color/scatter scopes, sampled GPU
Images and GPU-resident gallery-to-Picture bridge. The later sampled bridge
supersedes the earlier gallery readback limitation; do not reintroduce CPU filtering.

| Status | Type | Item | Detail |
| :---: | :--- | :--- | :--- |
| ⬜ | FIX/BUILD | real text | Raster drawText ignores its arguments and returns success; Vulkan drawText ignores the string and submits glyph zero. Implement font/glyph selection, measurement, native-resolution atlas/shaping and clipping; prove different strings produce the correct different pixels. |
| ⬜ | BUILD | automatic filter attachment | connect declared Element stacks to ordered render planning, isolation, all three scopes, rounded masks and dependencies. The explicit static gallery is not that planner. |
| ⬜ | BUILD | support/ROI/damage | ordered output support and backward source requirements; preserve sources outside visible output that scatter inward; invalidate old/new bounds and backdrop dependencies; never resize hit bounds to fit halos. |
| ⬜ | BUILD | complex filter parameters | typed immutable records, generation validation, sharing/COW, migration, retain/release and GPU in-flight leases. A token constructor does not prove effect execution. |
| ⬜ | BUILD | effects beyond proved subset | progressive blur, Gaussian support, HSL/HSV, noise and additional recipes each need defined ranges/color/alpha/edge semantics and numeric owner proof. Source-energy and constant-field normalization differ. |
| ⬜ | BUILD | independent Scene handoff | consume latest completed images without forcing scene ticks; versions need GPU synchronization, safe resize/close and retirement. |
| ⬜ | BUILD/PROVE | pooled steady state | cold preparation, reusable scratch/targets, bounded leases and actual allocation/frame-cost measurements. The allocating CPU reference is not a production hot-path fallback. |
| ⬜ | FIX/DECIDE | presentation contract drift | COMPOSITOR.md describes current CALayer/IOSurface publication, while lawbooks require the one CAMetalLayer seam. Reconcile the actual boundary and approved architecture before another backend rewrite. |
| ⬜ | FIX/PROVE | safety net | the historical vk_guard.h named by the lawbook is absent in the current checkout. Implement/reconcile the canonical health/loss contract, then prove it; annotations alone do not catch device loss. |
| ⬜ | PROVE | backends/failure | Raster/Null/Vulkan conformance, actual device-loss, driver-stage/OOM faults, validation layers, shader failure and retirement tests. Review old one-second-wait findings against current bounded waits before calling them live bugs. |
| ⬜ | PROVE | memory/performance/appearance | process footprint versus GPU memory, retained-texture growth, native drag profiling and user visual approval remain separate from pixel parity. No measured memory saving is inferred from fewer vertices. |
| ⬜ | PROVE | platform floor | macOS 14 runtime with a compatible loader, M1 and other supported hardware/hosts; a newer Apple host passing is not minimum-floor proof. |

## R3: api-haven

Source: `../drivers/api-haven/src/api/rest.c`, `src/storage/snapshot_io.h`,
`src/api/auth.h`, `../../README.md`; proof requirements: `../../tests/test-preferences.md`.

| Status | Type | Item | Detail |
| :---: | :--- | :--- | :--- |
| ✅ | FIX | REST status semantics | Preserve the published resolved record: `api/rest.c` checks Http_perform and returns success only for completed 2xx while retaining the response for inspection. The existing owner is `../../tests/api-haven/api/rest_test.c`; this document migration is not a fresh transport proof. |
| ✅ | FIX | auth failure propagation | Preserve the published resolved record: explicitly required credentials whose ApiAuth_apply fails now reject before a request is sent; nullptr/NONE permits an intentional public request. Existing loopback owner is `../../tests/api-haven/api/rest_test.c`; migration does not upgrade its scope. |
| ⬜ | FIX/BUILD | one URL/trust policy | duplicated parsing, atoi ports and silent path truncation need a canonical policy and adversarial proof. Include IPv6, userinfo, SSRF/private-address controls, redirects and cross-origin credential handling. |
| ⬜ | BUILD | retry/dropout/backpressure | distinct transport results, bounded attempts/jitter, Retry-After, streaming EOF/truncation and observable saturation. |
| ⬜ | BUILD | Drive provider | desktop OAuth/PKCE and refresh/revocation, scopes, issuer-to-principal mapping, upload/download, durable acknowledgement and idempotency. Never treat an API-key/bearer descriptor or fake verifier as completed OAuth. |
| ⬜ | BUILD | real connector behavior | catalogs for AI/DB/assets are not live provider integrations. Keep database execution with Darkbase; normalize responses, enforce license/attribution and cache confinement; no scraping. |
| ⬜ | PROVE | owner/wiring gaps | audit today's registered targets rather than reusing historical missing-test counts; finish transport, retry, SSRF, secret, framing, saturation and loopback batteries with exact cold diagnostics. |
| ⬜ | PROVE | MCP/telemetry safety | bounded serialization, protocol versions, handler permissions, no unintended exec/write, secret redaction and quiet normal flow. |

## R3: darkbase

Source: `../drivers/darkbase-engine/src/database/database.{h,c}`,
`database_result.{h,c}`; readiness: [darkbase Gist](https://gist.github.com/vex-graph/6943f92acb931b25dad1073c46da6ce7#file-darkbase-md).

**Already real:** M1 entity/row binding and M2 native-endian row save/load with
CRC32. Current docs disagree about completion; do not call it source-free anymore.

| Status | Type | Item | Detail |
| :---: | :--- | :--- | :--- |
| ⬜ | FIX | safe save publication | Database_save opens the destination with TRUNCATE and writes directly. A write failure can destroy the previous snapshot. Define temporary-write/verify/replace and durable-sync policy with fault injection. |
| ⬜ | DECIDE/BUILD | field codec | raw row Bytes are not portable object graphs; pointers, padding, endianness and schema evolution need explicit restrictions or encoding. CRC detects corruption, not compatibility, security or crash durability. |
| ⬜ | BUILD | mapped/page store | depends on RE FixedMappedFile; mapping itself is neither a transaction nor bounded-latency hot access. Keep file format policy here. |
| ⬜ | BUILD | queries/indexes | structured field predicates, projection, indexes, cursor boundaries and stable borrowed-result lifetime before advertising full queries. |
| ⬜ | BUILD | transactions/WAL | commit/rollback, crash/torn-write recovery, writer exclusion and backup/restore with actual changed content. |
| ⬜ | BUILD | programs/export/drivers | reactive store events, derived views, descriptor export/rebinding and a quarantined foreign driver are later milestones. |
| ⬜ | PROVE | load failure stages | independently inject allocation/commit-stage failures, hostile metadata, stride/length overflow and rejection recovery; distinguish malformed-file validation from full rollback/durability guarantees. |
| ⬜ | FIX | stale docs | README still says no production source/store behavior; header opening says persistence is future; the readiness entry contradicts its M1/M2 defect log. Update contracts, IDE metadata and readiness to the actual scope. |

## R3: language

Source: `../drivers/language/README.md`, `language-preferences.md`.

| Status | Type | Item | Detail |
| :---: | :--- | :--- | :--- |
| ⬜ | DECIDE/BUILD | first real grammar | reconcile Language/Lang_* vocabulary with Grammar_init/parse/destroy module ABI; implement one grammar and tokenizer before promising the whole language matrix. |
| ⬜ | BUILD | relational AST/highlighting | caller storage, stable node identity, byte/UTF-8 offsets, incremental edit behavior and error recovery. |
| ⬜ | BUILD/PROVE | LSP and reload | bounded external-process supervision, fragmented/malformed JSON-RPC, module ABI/version rejection and rollback. |
| ⬜ | PROVE | CodeField dependency | host compiler adapters in b do not supply parsing/highlighting or an editor document model. |

## R1: hotcwap

Source: `../host-behavior/hotcwap/hot`, `process/`, `kernel/`, `window/`;
contracts: `hotcwap-preferences.md` and `preferences/PREFERENCES.md`.

| Status | Type | Item | Detail |
| :---: | :--- | :--- | :--- |
| ⬜ | BUILD/PROVE | pins and resident ownership | Process hot association is not a generation pin. Keep verifier/callback code loaded during invocation; test active consumer reload and teardown while borrowed R2 storage is live. |
| ⬜ | PROVE | ABI gate completeness | actual version/class-layout/export compatibility before trampoline binding; magic checks alone are not schema compatibility. |
| ⬜ | PROVE | loader trust/retirement | hostile paths, permissions, symlink races, dependency interposition, ring exhaustion, concurrent calls and observable close failure. Existing rollback support must survive these failure stages too. |
| ⬜ | PROVE | integrated reverse teardown | detach R5/R4, retire R3, stop/exclude R2 users, close host resources, arenas last. Exercise cancellation and bounded joins. |
| ⬜ | BUILD/PROVE | supported native hosts | real Windows compilation/input/DPI/ resize/close tests; Linux/Wayland/X11 work has its own scope, not macOS proof. |
| ⬜ | RECHECK | lifecycle/presentation | Application blocking lifetime and Frame starter migration were implemented later; do not reopen the old proposal as an absent feature. Remaining GUI/native interaction approval and cross-platform proof stay open. |

## R4: darling-framework

Source: `../interfaces/darling-framework/STATUS.md`, `SCAFFOLDS.md`,
`src/panel/scroll_panel.c`, `src/label/`, `src/input/`, `src/overlay/`.

| Status | Type | Item | Detail |
| :---: | :--- | :--- | :--- |
| ⬜ | FIX | missing owning lawbook | darling-framework-preferences.md is absent. Recover/review a current remastered contract, not a blind copy of the retired generation; register it in the constitution in the same cycle. |
| ⬜ | BUILD | Label/TextCore | string ownership, fonts/measurement, wrapping, readable paint and typography, after the real Graphvex text path. |
| ⬜ | BUILD | editable text | document buffer, caret, selection, keyboard/IME, clipboard, UTF-8 indexing and undo/redo; CodeField/rich text need these foundations. |
| ⬜ | BUILD | usable ScrollPanel | default wheel/trackpad handler, direction and units, nested consumption/bubbling, momentum/overscroll contract, typed Panel/Frame attachment ownership, ScrollBar and offset API routing. |
| ⬜ | BUILD | focus/input | window-scoped dispatch, Tab/arrow navigation, disabled/hidden behavior, pointer capture, modal trapping, destruction and focus restoration. |
| ⬜ | BUILD | layout vocabulary | List/Grid/Flex/Split and sizing modes with measurement, min/max, padding/gap/margin and live resize, without a second geometry authority. |
| ⬜ | BUILD | OverlayRoot | escape content clips while maintaining modal input; then menus, select/popover/tooltips/dialogs and focus restoration. |
| ⬜ | BUILD | actual controls | Button, Checkbox, Switch, Slider/Knob, pickers, themes and feedback need real API/paint/input, not just the 125 draft file pairs. |
| ⬜ | BUILD | Scene/media/export | completed image handoff, video decode/import, safe process-driven decode, SVG/HTML export and interaction semantics. Picture's sampled GPU bridge already exists; fit/crop/media policy is a separate backlog. |
| ⬜ | DECIDE/BUILD | reactive UI metrics | source-of-truth property updates, owner-thread notifications and coalesced dirty/wake tickets; stale plans naming retired GraphicsComponent paths are not a ready implementation patch. |
| ⬜ | PROVE | user-facing acceptance | named input robot scripts, offscreen pixel oracles, native lifecycle seams and user appearance feedback. Compilation of a draft is not a working control; legacy tests are not remastered widget proof. |
| ⬜ | FIX | documentation precedence | current substrate inventory must override retired completed-widget tables, old color formats/points and outdated readback claims. |

## R4: sesh

Source: `../interfaces/sesh/README.md`, `sesh-preferences.md`, `src/lang/`,
`src/session/`, `src/snapshot/`; runner: `../../tests/sesh/run.py`.

**Already real:** seven-class composition, injected verification, local identity/
revision admission, copied intent versus receipt, replay, growth and snapshot scheduling.

| Status | Type | Item | Detail |
| :---: | :--- | :--- | :--- |
| ⬜ | BUILD | FileSession/DirectorySession | compose Sesh; real local traversal, path/symlink safety, nested content hashes, versioned manifest and state restoration. |
| ⬜ | BUILD | sync/clone/rebase | upload content before publishing manifest; preserve prior published version on failure; clone into new/empty storage; compare baselines and preserve conflicting versions rather than overwrite silently. |
| ⬜ | BUILD | applied data | an applied local revision is not applied file or database content. Bind owner operations with explicit transactional outcomes. |
| ⬜ | BUILD | cloud backup | API Haven Drive plus verified HTTPS, durable provider acknowledgement/idempotency; iCloud needs its own identity/entitlement integration. Use only disposable payloads and separately authorized real cloud smoke tests. |
| ⬜ | BUILD | durable identities/journal | persist IDs, queued intents, receipts and baselines; recovery, retention/epoch reset, deletion/rename and account linking. |
| ⬜ | BUILD/PROVE | distributed security | authoritative principal/ACL/revision checks and retry identity at the backend. Caller-serialized TSan proof is not internal thread safety, remote auth or cross-process atomicity. |
| ⬜ | BUILD | overall deadlines | pending snapshots require caller cancellation; define overall timeout and provider-borrow release before staging reuse. |
| ⬜ | BUILD | later collaboration | ordering/loss/reconnect, presence, merge model, relay deployment, framing/encryption and sanitized crash ingestion are future work, not implied by the local session object. |

## R5 applications and audio scope

Each row is a first workflow to define/build/prove, not a claim of existing product readiness.

| Checkout or concept | Open backlog / first acceptance loop |
| :--- | :--- |
| `../drivers/samplerate` | **BUILD/DECIDE:** sound-engine scope under Impedance; callback ring feeding, CPU DSP/mixer, format/rate/channel policy, latency/underrun handling, realtime no-allocation soak; GPU DSP only through Graphvex completion/fallback seams. Currently a blueprint. |
| `../interactables/impedance` | **BUILD/PROVE:** existing C audio shell is not a DAW; track/mix controls, transport, project/sample loading, save/reopen and realtime safety with usable UI. Decide supported hardware/MIDI and minimum workflow. |
| `../superapp/semicolon` | **BUILD:** real text document/editor, open/type/save, language highlight, supervised build/error output, undo/recovery. Empty/reserved editor directories and compiler adapters are not an IDE. |
| `../interactables/drawling` | **BUILD:** stylus/mouse stroke to pixels to real saved file, layers, undo/redo and reopen; frame timeline/onion skin later. Blueprint, not a painting app. |
| `../superapp/anti` | **BUILD:** launch editor, create scene, manipulate object, save/reopen, play/stop; then mesh/material/physics workflows. Empty-window FPS targets are not useful game-engine acceptance. |
| Darling Editor (no independent checkout found) | **DECIDE/BUILD:** establish app ownership, pan/zoom canvas and one editable persisted item; then layout inspector/export and Sesh integration. Framework/gallery capability is not this app. |
| Darkbase interactive host (future) | **DECIDE/BUILD:** keep R5 executable separate from R3 store; open/inspect/change/save/reopen one database through public contracts. |

## Tooling, tests, documentation and non-code repositories

| Status | Type | Item | Detail |
| :---: | :--- | :--- | :--- |
| ⬜ | PROVE | tests repository | map current owner units to registered runners, enforce assertions/strict warnings, exact negative diagnostics and skips as 77. Historical coverage counts need regeneration, not promotion from remembered green. |
| ⬜ | FIX | semantic readiness | several readiness entries retain legacy green claims or contradictory ownership/format descriptions. Reconcile code, proof, scope and user visual approval independently; do not bulk-promote a whole layer. |
| ⬜ | PROVE | standalone runtime | per-repo IDE CMake configure/no-op/syntax checks do not close b's actual dependency/link/resource/FFI/package contracts. |
| ⬜ | PROVE | platform matrix | supported Windows 10 and Apple Silicon/macOS 14 runtime floors; newer-device capability fallback/refusal; other hosts only where promised. GPU/clipboard/audio/window checks may legitimately need explicit skips. |
| ⬜ | FIX/RECHECK | universal API conformance | inventory constructors/zero, symmetric safe accessors, bounded string projections, blueprint field maps, ownership and exception contracts. The toString Law exists; ecosystem-wide implementation is not proved by Sesh having it. |
| ⬜ | FIX | stale citations/maps | retired law titles/numeric references and old checkout paths remain in historical material. Current docs cite Titles and actual owner paths; review typography substitutions without silently editing private notes. |
| ⬜ | DECIDE | workspace hygiene | generated root b.json, .DS_Store and the untracked Rust helloworld scratch file need explicit ignore/retain/track choices. Do not discard unknown user edits or stage all repositories wholesale. |
| ⬜ | PROVE | personal/b | adapter tests are scoped; TypeScript strip/parse is not type-checking, browser opener success is not rendering, SQL execution is not a sandbox, Cargo/native scripts can perform work, hardware upload is board-specific. Export/packaging and native project discovery remain separate product choices. |
| ⬜ | RECHECK | CLion integration | root/per-repo adapters and run configurations have changed across sessions; verify present settings/real tool paths and user IDE behavior, not the old deleted-CMake story. |
| ⬜ | DECIDE | profiles | `../personal/vex-graph` and `../vexgraph-ecosystem-gitrepo/.github` have artwork/ markup checks, not remote-link longevity or user appearance approval. No runtime blockers inferred. |
| ⬜ | DECIDE | readiness maintenance | the [readiness Gist](https://gist.github.com/vex-graph/6943f92acb931b25dad1073c46da6ce7) is canonical and the retired `../vexgraph-ecosystem-gitrepo/ecosystem` wiki is no longer maintained; correct contradictory legacy claims there while preserving feature scope/history. |
| ✅ | DECIDE | harness repository owner/status | Preserve the published resolved record: `interfaces/harness` is an independent repository with its own README/lawbook and real `src/space` values. Registered offline owners live in `../../tests/harness/space` and `../../tests/harness/run.py`. General agent/provider/server/UI integration remains unfinished; source/metadata and offline values are not live integration proof. |
| ⬜ | PROVE | release publication | inspect current local/remote state when publication is requested. Past one-off push permissions are consumed, not reusable. |
| ⬜ | FIX | `b test <name>` blocked by the coverage ratchet | Verified 2026-10-24: `./tools/b test reflection_test` exits 1 at `compiled units 173 / owned 0` and prints `REGRESSION — unit(s) shipped without an owner test` before running the named binary. The `MISSING` paths exist on disk, so "MISSING" means "no owner test", not "no file". Named-test selection should execute the test and report coverage separately; today no C test runs through the umbrella runner. |
| ⬜ | FIX | test source with no build target | `tests/language/adapters/c/c23_lexer_test.c` is inventoried and was rewritten by the cast-spacing sweep, but no CMake target compiles it; `tests/language/run.py` covers `adapters/c23/c23_adapter_test.c`, not this file. Wire it into a named target or retire it (Executable Evidence and Readiness Law). |

## Other session follow-ups (not ecosystem implementation gates)

| Status | Type | Item | Detail |
| :---: | :--- | :--- | :--- |
| ⬜ | RECHECK | Arduino | confirm current sketch/pin map, active-low LED wiring, common rails/ground, resistors, D12 pull-up/debounce, LDR threshold and potentiometer range/delay. Earlier exact-zero LDR and bad Serial.print advice was superseded by a later threshold/light helper session; inspect today's sketch before fixing it again. |
| ⬜ | PROVE | Arduino hardware | latest behavioral edits were not all compiled/ uploaded/hardware-tested. Native AVR toolchain support, board FQBN/port and physical current/polarity need real confirmation; formatting-only work did not prove behavior. |
| ⬜ | DECIDE | Tinkercad/capstone | recover assignment acceptance criteria and current circuit/sketch; partial history is insufficient to certify completeness. |
| ⬜ | DECIDE | Roblox | select project and trusted Studio/MCP or file-sync integration, permissions and exact task. No connection/game delivery is established here. |
| ⬜ | RECHECK | OpenCode cleanup | a historical pruning script was prepared, not proof of successful cleanup. Locate/review it and back up before any separately authorized deletion; do not stop this session's service or erase history as backlog cleanup. |
| ⬜ | DECIDE | browser automation | the cuadriver/manual-click session lacks a recoverable conclusion here. Restate task, target app and permission boundary. |

## Available session register

These entries account for all 50 sessions returned by the project session list
at review time. Duplicate titles are deliberately retained. **Partial** means
latest text could not be fully decoded/recovered; bus/source evidence supplements
it where available. No claim of complete historical coverage is made.

| Session title | Carry-forward / coverage |
| :--- | :--- |
| Planning Darkbase’s Vertically Integrated Database Architecture | M1/M2, mapping handoff, later path migration; current source beats stale README. |
| Testing Sesh with Google Drive and API Haven | This conversation/checkpoint and current composition sources; API history partial. File/cloud workflows deferred. |
| Large software architecture and developer motivation concerns | Shared type algebra move is completed per bus/source; priorities and remaining storage identity decisions. |
| Relational Engine Storage Design and Build Readiness | Native ownership migration done; TypedPool done; FixedMappedFile handoff not implemented. |
| Update all repositories for R2 relational engine naming | Ownership/docs/IDE fixes and SUGAR_VEX proof completed; downstream doc drift still needs reconciliation. |
| Testing button 12 in writin-phase.ino | D12 wiring/debounce and serial advice; hardware follow-up. |
| Find links to all repositories and projects in GitHub ecosystems | Rust/stable rows/bindings implemented later; persistence/GPU paths remain separate. Latest history partial. |
| Roblox Studio Buddy Check-In | Integration/setup proposal, not an established Studio connection. |
| Making `preferences/PREFERENCES.md` a one-file Gist | Canonical Gist publication/private lesson handling completed; local source now gist/PREFERENCES.md. Do not publish private lessons through this backlog. |
| Diagnosing Filter Gallery memory usage and real vs. private memory | Source/bus confirm later sampled GPU path; process-memory profiling remains open. |
| Reviewing repository structure and separating relational engine | Per-repo IDE adapters done; standalone runtime/IDE appearance not thereby proved. |
| Rust object model lessons | Research partly recovered; Rust type identity/borrowing does not replace canonical reflection/lifetime proof. |
| Portable storage GPU transfers | Research partly recovered; portable host reads plus Graphvex upload, optional capability paths not implemented universally. |
| Allocation and virtual memory | Research partly recovered; mapping/layout/lifetime decisions and historical risks require current-owner reconciliation. |
| Greeting | No substantive recoverable task; failed session is not an implementation blocker. |
| Greeting | Greeting only; no backlog inferred. |
| Greeting | No substantive recoverable task; failed session is not an implementation blocker. |
| Update preferences symlink and assess separated relational engine structure | No recoverable conclusions; newer real-root constitution and engine ownership supersede old path assumptions. |
| Designing pools for Graphvex memory models and filters | GPU scopes delivered; automatic attachment, parameter models and broader proof remain. Partial history. |
| compositor discussion | b/IDE discussion; old engine-removal proposal is not current ownership intent. |
| Update .opencode Git setup and consolidate preferences into one prompt | b adapter/tooling cycle; later gallery changes supersede readback report. |
| Designing a Typed, Stackable UI Filter System | Contracts/static GPU scope work and coordination; general widget planner remains open. |
| Arduino AVR compiler bad CPU type error on macOS | Toolchain issue and later LED/LDR/delay edits; hardware proof incomplete. |
| compositor discussion | Scope/resize/Picture slice completed then superseded in part by sampled path. |
| Assess compute scatter correctness | Normalization/race/capability research; not executed general backend proof. |
| Assess widget compositor scheduling | Independent scene cadence, completed-image handoff and dependency planner backlog. |
| Agent message signatures for identity | Messaging/checklist/IDE/lifecycle tooling completed; historical push claims are time-specific. Partial history. |
| Review scatter compositor architecture | Pool leases, ordering, numeric semantics and target budgets; later explicit scopes partially deliver this. |
| Review absolute filter bounds | Ordered support, reverse ROI, nested masks and layout-versus-paint semantics. |
| Assess opaque window and frame behavior in darling_gallery tests | Later Application/Frame migration exists; native/visual acceptance stays separate. |
| Planning the next focus for the Darling project | Cursor property delivered; readable text, scrolling and controls remain higher leverage. |
| Ensuring Comprehensive Test Coverage in `tests` | Skip-as-pass fixed; current owner/security/backend coverage still needs inventory. |
| Compare two darling-framework generations | Retired widget library is reference, not current remastered capabilities. |
| Map graphvex Element and graphics seams | Historical source inventory partly recovered; current seam/doc drift takes precedence. |
| Deleting chat sessions from the database | Prepared cleanup workflow; no deletion authorized by blockers.md. |
| Darling UI remastered component design | Historical native presentation fix reported; current visual/input proof not inferred. |
| Removing excessive newlines in writing-phase.ino | Formatting completed; not hardware/behavior evidence. |
| Inventory graphvex UI holders (@muse-reporter-a subagent) | Historical generation inventory; no agent spawned for this audit. |
| Inventory darling widgets (@muse-reporter-b subagent) | Historical widget inventory; remastered drafts cannot inherit old readiness. |
| Check language + media deps (@muse-reporter-c subagent) | Language/text/video gaps; later photo/sample-texture bridge supersedes some missing-image claims. |
| Arduino wiring phase 2 completeness check | Partial recovery; screenshot review not complete electrical verification. |
| Tinkercad photoresistor capstone project | Partial history, no recoverable conclusion; recover requirements before changes. |
| Running tasks via cuadriver vs manual clicks | Partial history, no recoverable conclusion; clarify automation goal. |
| New session - 2026-09-21T11:04:28.722Z | Partial historical image orientation/fit-demo fix; not current text/gallery proof. |
| New session - 2026-09-22T05:02:54.554Z | Greeting; no deliverable inferred. |
| New session - 2026-09-21T11:03:35.153Z | No substantive recoverable text; no backlog invented. |
| New session - 2026-09-21T08:05:21.035Z | No substantive recoverable text; no backlog invented. |
| Darling overhaul for component container | Partial history, no recovered conclusion; use current remastered sources/status. |
| Migrate widgets anim scene (@muse-writer subagent) | Partial migration history, no final proof recovered; do not promote historical files. |
| Migrate compositor bridge canvas (@muse-writer subagent) | Partial migration history, no final proof recovered; current build/owner evidence governs. |

## Suggested later work sequence

1. Choose one first workflow and resolve only the decisions it needs.
2. Repair text/Label and scrolling/focus if it is a GUI workflow.
3. Implement/prove storage publication and mapping before promising durable databases.
4. Fix HTTPS/status/auth, then local file sessions, then an explicitly authorized cloud round trip.
5. Prove resident lifetime/reload and failure recovery across the seams actually used.
6. Add one R5 end-to-end workflow and gather user visual/interaction feedback.
7. Expand filters, collaboration, additional grammars/platforms and performance
   work from measured needs, not from completing every roadmap cell at once.

**Audit:** this backlog is published as the [ecosystem blockers Gist](https://gist.github.com/vex-graph/e921fa188eebbd0c68c4e59646109887);
the retired `tests/tools/blockers_test.py` no longer runs. Per-test lab evidence belongs
in the checklist under the Timestamped Test Checklist Law.

---

## Resolved decisions (2026-10-08)

| Status | Type | Item | Detail |
| :---: | :--- | :--- | :--- |
| ✅ | RESOLVED | byte order / endianness (darkbase field codec + portable schema) | NO ENDIANNESS NEEDED. Values are raw `uint8_t[]` written in memory order; no detection, no swapping, no text encoding. Every supported host is little-endian (Apple Silicon arm64 floor; Windows x86_64), so there is no cross-endian peer. Bytes-in-order is more native than a swap layer. `toString` is a cold converter only. Codified as the Byte-Native Persistence Law (`darkbase-preferences.md`) and as an `// INTENTIONAL(vex)` note at the `.vexdb` format definition. |
| ✅ | RESOLVED | canonical variable | `{ uint8_t name[24], void* pointer }`. The engine's canonical `VariableSlot` already matches (Rust `[u8;24]` + `*const u8`; C `uint8_t name[24]` + `const uint8_t*`). Vexspoke's *legacy retained C copy* (`char name[24]` + `uintptr_t`) diverges and is a separate migration item. |
| ⬜ | DEFERRED | darling / ScrollPanel | deprioritized; not a current focus. The P1 ScrollPanel attachment/input/focus item is dropped from near-term priority. |
| ✅ | DONE | blockers.md | moved to `_notes/blockers.md` (local, Git-ignored); root deletion + `/blockers.md` ignore are staged, not committed. Its owner test `tests/tools/blockers_test.py` was retired (the doc is no longer tracked). |
## Session delta: R3 Samplerate + R4 Harness + personal func (2026-10-09)

Newest dangling work from the Samplerate tier correction session. Everything here
is **draft** unless an evidence row says otherwise. No push is authorized by this
section; each item is a suggestion for the next session.

### Samplerate — now R3 native audio driver (tier changed this session)

| Status | Type | Item | Detail |
| :---: | :--- | :--- | :--- |
| ⬜ | BUILD | samplerate owner tests | `AudioFormat`, `AudioBuffer`, `AudioMemory` and the `AudioStream` seam have **no** owner test; `tests/samplerate/` does not exist. Blocked on the shared checklist hold. |
| ⬜ | BUILD | samplerate next classes | `Sample`, `SamplePlayer`, `Audio` (the approved inventory), then graph / synth / filter / effect / io / seq. |
| ⬜ | PROVE | CoreAudio device output | `platform/audio_stream_cocoa.m` compiles but has **never opened or started a real device**. Needs a native output probe, or an explicit `B_TEST_SKIP` with reason. |
| ⬜ | BUILD | non-Apple audio backends | `platform/audio_stream_stub.c` fails closed; WASAPI/ALSA are unimplemented. |
| ⬜ | DECIDE | R1 Kernel supervision | Samplerate runs standalone; adding it to hotcwap's include allowlist is a separate amendment. |
| ⬜ | DECIDE | GPU audio compute | Needs an explicit R3→R3 `graphvex` grant plus measured benchmarks before any claim. |
| ⬜ | DECIDE | vexspoke audio retirement | `vexspoke/src/audio/audio_cocoa.m` (AVAudioEngine) and `audio_hal_mac.m` (CoreAudio) are untested and now overlap samplerate — migrate or retire. |

### Harness — R4 interface (the user's own agent)

| Status | Type | Item | Detail |
| :---: | :--- | :--- | :--- |
| ⬜ | DECIDE | harness tool set + MCP | Choose the built-in tools, the own-MCP surface, and external MCP (Claude/others) support. |
| ⬜ | BUILD | harness first objects | `Model`, `Prompt`, `Conversation`, `Answer`, `Question`, `Tool`/`ToolRegistry`, `HarnessMcp`, `Harness`. Zero source today. |

### func — personal compile-time opcode orchestrator

| Status | Type | Item | Detail |
| :---: | :--- | :--- | :--- |
| ⬜ | BUILD | func Phase 1 | `Opcode`/`OpcodeRegistry`/`Value` → `FuncStream`/`FuncReader`/`FuncProgram` → frontend → compiler/emitter/builder → runtime. First milestone: `1, 34, 7` → `41`. Docs-only blueprint exists; no source. |

### Impedance — R5 DAW

| Status | Type | Item | Detail |
| :---: | :--- | :--- | :--- |
| ⬜ | PROVE | impedance shell owner test | `src/{impedance.c,impedance.h,main.c}` have no owner test; a sibling session is editing the source. Live output, GPU path, UI and persistence do not exist. |

### Cross-cutting

| Status | Type | Item | Detail |
| :---: | :--- | :--- | :--- |
| ⬜ | RECHECK | shared checklist | Contended by sessions; samplerate and tests evidence are pending. |
| ⬜ | PUSH | tests repo | My `docs(tests)` commit is local only; the repo also holds the RE-mapping sibling's unpushed test commit. |
| ⬜ | RECHECK | RE FixedMappedFile + native Memory | RE carries 9 unpushed commits (mapped-file + memory-exhaustion proof). A `mem.h` ABI change would affect samplerate's `core/audio_memory.c`. |

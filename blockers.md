# Vexgraph blockers and deferred decisions

**Reviewed: 2026-10-08.** One place to resume work later, across the workspace,
ecosystem repositories, applications, tooling and available conversations.

This is a backlog, **not a claim that you forgot everything below**. Some items
are deliberate deferrals, some are implementation gaps, some are proof gaps,
and some need your design decision. Nothing here authorizes implementation,
cloud access, hardware uploads, deletion, installation or repository pushes.

## How to use this

- **DECIDE**: a contract or product choice still needs to be settled.
- **BUILD**: accepted direction exists, but the user-facing feature is unfinished.
- **FIX**: inspected code or documents contradict the intended contract.
- **PROVE**: functionality may exist, but the relevant executed evidence is missing.
- **RECHECK**: historical concern; do not assume it still reproduces.
- Check a box only with the associated decision or evidence. Dates/emoji in older
  conversations are not current proof. This document does not supersede
  `preferences.md`, repo-local laws, readiness pages or `tests/test-checklist.md`.
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

- [ ] **DECIDE — first deliverable:** pick one first usable workflow and its
  acceptance criteria: readable interactive UI, local database, backup/restore,
  mini editor, drawing loop or audio project. Do not make every roadmap a release gate.
- [ ] **DECIDE — identity lifecycle:** who creates/persists client, workspace,
  resource and operation IDs; uniqueness scope; account linking; device reset;
  name reuse; tombstones; history retention and deduplication epochs.
- [ ] **DECIDE — synchronization authority:** single-writer first, or a backend
  enforcing authorization and revision/CAS? Define conflicts, retries, deletion,
  rename, baseline retention and offline reconciliation. Local counters are not distributed CAS.
- [ ] **DECIDE — persistence meaning:** when is a save acknowledged, what survives
  a crash/power loss, what can be recovered, and what is the backup/restore policy?
  Separate buffered flush, durable sync, atomic publication and transactions.
- [ ] **DECIDE — portable schema:** format version, byte order, schema hash,
  field encoding, pointer/reference relocation, functions rebound by name,
  evolution/rollback and incompatible-version rejection.
- [ ] **DECIDE — C/Rust migration boundary:** native Memory ABI remains supported;
  define which collection moves next and its parity gates. Rust pools are not an
  interchangeable native allocator, and Rust TypeId is not persistent engine identity.
- [ ] **DECIDE — mapped storage:** mapping versus hot arenas, read/write leases,
  resize exclusion, invalidation, flush semantics, Windows handles and blocking-I/O supervision.
- [ ] **DECIDE — UI policies:** text ownership, editable document model, focus
  traversal/modal capture, nested-scroll consumption, layout measurement,
  attachment ownership and accessibility expectations.
- [ ] **DECIDE — filter ownership:** per-element versus deliberately shared
  Property stacks; immutable parameter leases/COW; invalidation of every referrer;
  nested backdrop prefix meaning; explicit unsupported-capability disposition.
- [ ] **DECIDE — operational limits:** configurable defaults versus justified
  safety bounds, observable backpressure, deadlines and cancellation disposition.
  Historical fixed room/queue/FPS targets need review under the No Hardcoding Law.
- [ ] **DECIDE — deployment:** standalone runtime dependency packaging, application
  manifests, capability requirements, signing, updates, rollback and supported-host proof.
- [ ] **DECIDE — product names:** Darkbase library versus executable naming;
  Samplerate sound engine versus Impedance workstation; create a Darling Editor
  checkout only when its app scope is authorized.

## R2: relational-engine

Source: `ecosystem/repos/relational-engine/README.md`,
`relational-engine-preferences.md`, `src/nio/`, `src/io/`, `src/type/`, `rust/`;
readiness: `ecosystem/ecosystem/relational-engine.md`.

**Already real:** engine-owned production native IO/NIO, compatible Memory C ABI,
shared type algebra, Rust byte/string publication, stable chunks, named bindings,
TypedChunk/TypedPool and native C span search. Do not redo the ownership migration.

- [ ] **BUILD — MappedFile:** agreed next primitive remains a plan/handoff, not a
  delivered mapping API. Prove leases, bounds/alignment, resize failure preservation,
  writable borrows, flush errors and close with active borrowers. Page faults must
  not be treated as bounded hot-path work.
- [ ] **BUILD — identity handles:** reusable pool indices are locations, not
  generation-safe identities. Finish metadata encoding, stale rejection, exhaustion
  and wrap policy before exposing reuse as persistent/live object identity.
- [ ] **BUILD — object/name integration:** connect names to value lifetime and
  destruction without conflating VariableSlot `[name,value]` with StringSlot `[self,name]`.
- [ ] **BUILD — bulk/scratch/VM:** contiguous bulk APIs, resettable typed scratch,
  reserve/commit and mapping are separate contracts; stable chunks are not one giant contiguous array.
- [ ] **BUILD — file toolkit:** safe directory traversal, buffered/asynchronous
  operations, indexing/watchers and manifest-backed persistent objects remain future slices.
  HotFileSys currently has lifecycle proof, not working watching.
- [ ] **BUILD — codecs/virtual storage:** ZIP/7z, ASTC and GPU storage-transfer
  references are planned areas, not automatic compression or SSD-to-GPU support.
- [ ] **PROVE — resident reload:** real two-consumer-module reload retaining engine
  code/storage; exclude API users before release; test teardown and failed migration rollback.
- [ ] **PROVE — Rust/native boundary:** Rust instrumentation, allocator/OOM
  behavior, complete legal concurrency/fault matrix, Windows and performance.
  C-client ASan/UBSan does not instrument Rust or prove native allocator parity.
- [ ] **PROVE — permission-bound clipboard:** mutation was skipped without lab
  permission; do not turn the skip into a pass or mutate the clipboard implicitly.
- [ ] **RECHECK — historical native allocator/File concerns:** old research raised
  fallback tracking, stale headers, alignment, scratch arithmetic, stream position
  and close errors. Some native owners were strengthened later. Reconcile each
  concern with today's implementation and tests rather than relisting all as live defects.

## R2: vexspoke

Source: `ecosystem/repos/vexspoke/src/net/http.c`, `src/relational/symbol_table.c`,
`src/input/`, `src/reactive/`; readiness: `ecosystem/ecosystem/vexspoke.md`.

- [ ] **FIX/BUILD — HTTPS admission:** Http_perform still returns false for https.
  Wire verified TLS, hostname/certificate verification, bounded transport operations,
  cancellation and distinct transport errors. A standalone TLS backend is not HTTP integration.
- [ ] **PROVE — hostile transport:** DNS/connect/TLS/reset/short-read/timeouts,
  framing/chunks, overflow, redirect policy and failure preservation at real cold seams.
- [ ] **RECHECK — CAS claims:** SymbolTable_compareAndSetPointer uses ordinary
  compare/assignment, not atomic CAS. Confirm its synchronization contract and
  correct any thread-safe/lock-free roadmap claims; do not infer atomicity from the name.
- [ ] **BUILD — reflection convergence:** settle remaining identity-cell/shelf/name
  integration and C/Rust ownership. Keep reflective lookup cold; retain validated
  pointers for hot consumers. Old reflection plans are not the current ABI.
- [ ] **BUILD — event-stream gestures:** drag/scroll/zoom bindings need their
  event-driven resolver; per-frame tap polling alone does not deliver these gestures.
- [ ] **BUILD/PROVE — non-Apple audio/input/system seams:** distinguish safe fallback
  stubs from actual native audio behavior and prove supported hosts separately.
- [ ] **PROVE — per-file contracts:** remaining collection growth/overflow,
  pointer legitimacy, ring/spin contention and reactive callback-affinity evidence.
- [ ] **FIX — readiness drift:** reconcile contradictory TLS entries, historical
  memory/name/header geometry, clipboard ownership and blanket green claims against current owners.

## R3: graphvex

Source: `ecosystem/repos/graphvex/COMPOSITOR.md`, `FILTERS.md`,
`src/graphics/graphics.c`, `src/vulkan/vk_renderer.c`, `src/compositor/`.

**Already real:** numeric CPU reference, Vulkan color/scatter scopes, sampled GPU
Images and GPU-resident gallery-to-Picture bridge. The later sampled bridge
supersedes the earlier gallery readback limitation; do not reintroduce CPU filtering.

- [ ] **FIX/BUILD — real text:** Raster drawText ignores its arguments and returns
  success; Vulkan drawText ignores the string and submits glyph zero. Implement
  font/glyph selection, measurement, native-resolution atlas/shaping and clipping;
  prove different strings produce the correct different pixels.
- [ ] **BUILD — automatic filter attachment:** connect declared Element stacks to
  ordered render planning, isolation, all three scopes, rounded masks and dependencies.
  The explicit static gallery is not that planner.
- [ ] **BUILD — support/ROI/damage:** ordered output support and backward source
  requirements; preserve sources outside visible output that scatter inward;
  invalidate old/new bounds and backdrop dependencies; never resize hit bounds to fit halos.
- [ ] **BUILD — complex filter parameters:** typed immutable records, generation
  validation, sharing/COW, migration, retain/release and GPU in-flight leases.
  A token constructor does not prove effect execution.
- [ ] **BUILD — effects beyond proved subset:** progressive blur, Gaussian support,
  HSL/HSV, noise and additional recipes each need defined ranges/color/alpha/edge
  semantics and numeric owner proof. Source-energy and constant-field normalization differ.
- [ ] **BUILD — independent Scene handoff:** consume latest completed images without
  forcing scene ticks; versions need GPU synchronization, safe resize/close and retirement.
- [ ] **BUILD/PROVE — pooled steady state:** cold preparation, reusable scratch/targets,
  bounded leases and actual allocation/frame-cost measurements. The allocating CPU
  reference is not a production hot-path fallback.
- [ ] **FIX/DECIDE — presentation contract drift:** COMPOSITOR.md describes current
  CALayer/IOSurface publication, while lawbooks require the one CAMetalLayer seam.
  Reconcile the actual boundary and approved architecture before another backend rewrite.
- [ ] **FIX/PROVE — safety net:** the historical vk_guard.h named by the lawbook is
  absent in the current checkout. Implement/reconcile the canonical health/loss
  contract, then prove it; annotations alone do not catch device loss.
- [ ] **PROVE — backends/failure:** Raster/Null/Vulkan conformance, actual device-loss,
  driver-stage/OOM faults, validation layers, shader failure and retirement tests.
  Review old one-second-wait findings against current bounded waits before calling them live bugs.
- [ ] **PROVE — memory/performance/appearance:** process footprint versus GPU memory,
  retained-texture growth, native drag profiling and user visual approval remain
  separate from pixel parity. No measured memory saving is inferred from fewer vertices.
- [ ] **PROVE — platform floor:** macOS 14 runtime with a compatible loader, M1 and
  other supported hardware/hosts; a newer Apple host passing is not minimum-floor proof.

## R3: api-haven

Source: `ecosystem/repos/api-haven/src/api/rest.c`, `src/storage/snapshot_io.h`,
`src/api/auth.h`, `README.md`; proof requirements: `tests/test-preferences.md`.

- [ ] **FIX — REST status semantics:** perform returns response.ok without checking
  status; it discards Http_perform's return. Classify 1xx/2xx/3xx/4xx/5xx/429/503,
  reject application failures and preserve/clear outputs as documented.
- [ ] **FIX — auth failure propagation:** failed ApiAuth_apply currently omits the
  header and continues. Define explicit unauthenticated requests versus failed
  required authentication, then prove fail-closed behavior.
- [ ] **FIX/BUILD — one URL/trust policy:** duplicated parsing, atoi ports and silent
  path truncation need a canonical policy and adversarial proof. Include IPv6,
  userinfo, SSRF/private-address controls, redirects and cross-origin credential handling.
- [ ] **BUILD — retry/dropout/backpressure:** distinct transport results, bounded
  attempts/jitter, Retry-After, streaming EOF/truncation and observable saturation.
- [ ] **BUILD — Drive provider:** desktop OAuth/PKCE and refresh/revocation, scopes,
  issuer-to-principal mapping, upload/download, durable acknowledgement and idempotency.
  Never treat an API-key/bearer descriptor or fake verifier as completed OAuth.
- [ ] **BUILD — real connector behavior:** catalogs for AI/DB/assets are not live
  provider integrations. Keep database execution with Darkbase; normalize responses,
  enforce license/attribution and cache confinement; no scraping.
- [ ] **PROVE — owner/wiring gaps:** audit today's registered targets rather than
  reusing historical missing-test counts; finish transport, retry, SSRF, secret,
  framing, saturation and loopback batteries with exact cold diagnostics.
- [ ] **PROVE — MCP/telemetry safety:** bounded serialization, protocol versions,
  handler permissions, no unintended exec/write, secret redaction and quiet normal flow.

## R3: darkbase

Source: `ecosystem/repos/darkbase/src/database/database.{h,c}`,
`database_result.{h,c}`; readiness: `ecosystem/ecosystem/darkbase.md`.

**Already real:** M1 entity/row binding and M2 native-endian row save/load with
CRC32. Current docs disagree about completion; do not call it source-free anymore.

- [ ] **FIX — safe save publication:** Database_save opens the destination with
  TRUNCATE and writes directly. A write failure can destroy the previous snapshot.
  Define temporary-write/verify/replace and durable-sync policy with fault injection.
- [ ] **DECIDE/BUILD — field codec:** raw row Bytes are not portable object graphs;
  pointers, padding, endianness and schema evolution need explicit restrictions or
  encoding. CRC detects corruption, not compatibility, security or crash durability.
- [ ] **BUILD — mapped/page store:** depends on RE MappedFile; mapping itself is
  neither a transaction nor bounded-latency hot access. Keep file format policy here.
- [ ] **BUILD — queries/indexes:** structured field predicates, projection, indexes,
  cursor boundaries and stable borrowed-result lifetime before advertising full queries.
- [ ] **BUILD — transactions/WAL:** commit/rollback, crash/torn-write recovery,
  writer exclusion and backup/restore with actual changed content.
- [ ] **BUILD — programs/export/drivers:** reactive store events, derived views,
  descriptor export/rebinding and a quarantined foreign driver are later milestones.
- [ ] **PROVE — load failure stages:** independently inject allocation/commit-stage
  failures, hostile metadata, stride/length overflow and rejection recovery; distinguish
  malformed-file validation from full rollback/durability guarantees.
- [ ] **FIX — stale docs:** README still says no production source/store behavior;
  header opening says persistence is future; wiki opening contradicts its M1/M2
  defect log. Update contracts, IDE metadata and readiness to the actual scope.

## R3: language

Source: `ecosystem/repos/language/README.md`, `language-preferences.md`.

- [ ] **DECIDE/BUILD — first real grammar:** reconcile Language/Lang_* vocabulary
  with Grammar_init/parse/destroy module ABI; implement one grammar and tokenizer
  before promising the whole language matrix.
- [ ] **BUILD — relational AST/highlighting:** caller storage, stable node identity,
  byte/UTF-8 offsets, incremental edit behavior and error recovery.
- [ ] **BUILD/PROVE — LSP and reload:** bounded external-process supervision,
  fragmented/malformed JSON-RPC, module ABI/version rejection and rollback.
- [ ] **PROVE — CodeField dependency:** host compiler adapters in b do not supply
  parsing/highlighting or an editor document model.

## R1: hotcwap

Source: `ecosystem/repos/hotcwap/hot/`, `process/`, `kernel/`, `window/`;
contracts: `hotcwap-preferences.md` and `preferences.md`.

- [ ] **BUILD/PROVE — pins and resident ownership:** Process hot association is
  not a generation pin. Keep verifier/callback code loaded during invocation;
  test active consumer reload and teardown while borrowed R2 storage is live.
- [ ] **PROVE — ABI gate completeness:** actual version/class-layout/export
  compatibility before trampoline binding; magic checks alone are not schema compatibility.
- [ ] **PROVE — loader trust/retirement:** hostile paths, permissions, symlink races,
  dependency interposition, ring exhaustion, concurrent calls and observable close failure.
  Existing rollback support must survive these failure stages too.
- [ ] **PROVE — integrated reverse teardown:** detach R5/R4, retire R3, stop/exclude
  R2 users, close host resources, arenas last. Exercise cancellation and bounded joins.
- [ ] **BUILD/PROVE — supported native hosts:** real Windows compilation/input/DPI/
  resize/close tests; Linux/Wayland/X11 work has its own scope, not macOS proof.
- [ ] **RECHECK — lifecycle/presentation:** Application blocking lifetime and Frame
  starter migration were implemented later; do not reopen the old proposal as an
  absent feature. Remaining GUI/native interaction approval and cross-platform proof stay open.

## R4: darling-framework

Source: `ecosystem/repos/darling-framework/STATUS.md`, `SCAFFOLDS.md`,
`src/panel/scroll_panel.c`, `src/label/`, `src/input/`, `src/overlay/`.

- [ ] **FIX — missing owning lawbook:** darling-framework-preferences.md is absent.
  Recover/review a current remastered contract, not a blind copy of the retired
  generation; register it in the constitution in the same cycle.
- [ ] **BUILD — Label/TextCore:** string ownership, fonts/measurement, wrapping,
  readable paint and typography, after the real Graphvex text path.
- [ ] **BUILD — editable text:** document buffer, caret, selection, keyboard/IME,
  clipboard, UTF-8 indexing and undo/redo; CodeField/rich text need these foundations.
- [ ] **BUILD — usable ScrollPanel:** default wheel/trackpad handler, direction and
  units, nested consumption/bubbling, momentum/overscroll contract, typed Panel/Frame
  attachment ownership, ScrollBar and offset API routing.
- [ ] **BUILD — focus/input:** window-scoped dispatch, Tab/arrow navigation,
  disabled/hidden behavior, pointer capture, modal trapping, destruction and focus restoration.
- [ ] **BUILD — layout vocabulary:** List/Grid/Flex/Split and sizing modes with
  measurement, min/max, padding/gap/margin and live resize, without a second geometry authority.
- [ ] **BUILD — OverlayRoot:** escape content clips while maintaining modal input;
  then menus, select/popover/tooltips/dialogs and focus restoration.
- [ ] **BUILD — actual controls:** Button, Checkbox, Switch, Slider/Knob, pickers,
  themes and feedback need real API/paint/input, not just the 125 draft file pairs.
- [ ] **BUILD — Scene/media/export:** completed image handoff, video decode/import,
  safe process-driven decode, SVG/HTML export and interaction semantics. Picture's
  sampled GPU bridge already exists; fit/crop/media policy is a separate backlog.
- [ ] **DECIDE/BUILD — reactive UI metrics:** source-of-truth property updates,
  owner-thread notifications and coalesced dirty/wake tickets; stale plans naming
  retired GraphicsComponent paths are not a ready implementation patch.
- [ ] **PROVE — user-facing acceptance:** named input robot scripts, offscreen
  pixel oracles, native lifecycle seams and user appearance feedback. Compilation
  of a draft is not a working control; legacy tests are not remastered widget proof.
- [ ] **FIX — documentation precedence:** current substrate inventory must override
  retired completed-widget tables, old color formats/points and outdated readback claims.

## R4: sesh

Source: `ecosystem/repos/sesh/README.md`, `sesh-preferences.md`, `src/lang/`,
`src/session/`, `src/snapshot/`; runner: `tests/sesh/run.py`.

**Already real:** seven-class composition, injected verification, local identity/
revision admission, copied intent versus receipt, replay, growth and snapshot scheduling.

- [ ] **BUILD — FileSession/DirectorySession:** compose Sesh; real local traversal,
  path/symlink safety, nested content hashes, versioned manifest and state restoration.
- [ ] **BUILD — sync/clone/rebase:** upload content before publishing manifest;
  preserve prior published version on failure; clone into new/empty storage;
  compare baselines and preserve conflicting versions rather than overwrite silently.
- [ ] **BUILD — applied data:** an applied local revision is not applied file or
  database content. Bind owner operations with explicit transactional outcomes.
- [ ] **BUILD — cloud backup:** API Haven Drive plus verified HTTPS, durable provider
  acknowledgement/idempotency; iCloud needs its own identity/entitlement integration.
  Use only disposable payloads and separately authorized real cloud smoke tests.
- [ ] **BUILD — durable identities/journal:** persist IDs, queued intents, receipts
  and baselines; recovery, retention/epoch reset, deletion/rename and account linking.
- [ ] **BUILD/PROVE — distributed security:** authoritative principal/ACL/revision
  checks and retry identity at the backend. Caller-serialized TSan proof is not
  internal thread safety, remote auth or cross-process atomicity.
- [ ] **BUILD — overall deadlines:** pending snapshots require caller cancellation;
  define overall timeout and provider-borrow release before staging reuse.
- [ ] **BUILD — later collaboration:** ordering/loss/reconnect, presence, merge
  model, relay deployment, framing/encryption and sanitized crash ingestion are
  future work, not implied by the local session object.

## R5 applications and audio scope

Each row is a first workflow to define/build/prove, not a claim of existing product readiness.

| Checkout or concept | Open backlog / first acceptance loop |
| :--- | :--- |
| `ecosystem/repos/samplerate` | **BUILD/DECIDE:** sound-engine scope under Impedance; callback ring feeding, CPU DSP/mixer, format/rate/channel policy, latency/underrun handling, realtime no-allocation soak; GPU DSP only through Graphvex completion/fallback seams. Currently a blueprint. |
| `ecosystem/projects/impedance` | **BUILD/PROVE:** existing C audio shell is not a DAW; track/mix controls, transport, project/sample loading, save/reopen and realtime safety with usable UI. Decide supported hardware/MIDI and minimum workflow. |
| `ecosystem/projects/semicolon` | **BUILD:** real text document/editor, open/type/save, language highlight, supervised build/error output, undo/recovery. Empty/reserved editor directories and compiler adapters are not an IDE. |
| `ecosystem/projects/drawling` | **BUILD:** stylus/mouse stroke to pixels to real saved file, layers, undo/redo and reopen; frame timeline/onion skin later. Blueprint, not a painting app. |
| `ecosystem/projects/anti` | **BUILD:** launch editor, create scene, manipulate object, save/reopen, play/stop; then mesh/material/physics workflows. Empty-window FPS targets are not useful game-engine acceptance. |
| Darling Editor (no independent checkout found) | **DECIDE/BUILD:** establish app ownership, pan/zoom canvas and one editable persisted item; then layout inspector/export and Sesh integration. Framework/gallery capability is not this app. |
| Darkbase interactive host (future) | **DECIDE/BUILD:** keep R5 executable separate from R3 store; open/inspect/change/save/reopen one database through public contracts. |

## Tooling, tests, documentation and non-code repositories

- [ ] **PROVE — tests repository:** map current owner units to registered runners,
  enforce assertions/strict warnings, exact negative diagnostics and skips as 77.
  Historical coverage counts need regeneration, not promotion from remembered green.
- [ ] **FIX — semantic readiness:** several wiki sections retain legacy green
  claims or contradictory ownership/format descriptions. Reconcile code, proof,
  scope and user visual approval independently; do not bulk-promote a whole layer.
- [ ] **PROVE — standalone runtime:** per-repo IDE CMake configure/no-op/syntax
  checks do not close b's actual dependency/link/resource/FFI/package contracts.
- [ ] **PROVE — platform matrix:** supported Windows 10 and Apple Silicon/macOS 14
  runtime floors; newer-device capability fallback/refusal; other hosts only where
  promised. GPU/clipboard/audio/window checks may legitimately need explicit skips.
- [ ] **FIX/RECHECK — universal API conformance:** inventory constructors/zero,
  symmetric safe accessors, bounded string projections, blueprint field maps,
  ownership and exception contracts. The toString Law exists; ecosystem-wide
  implementation is not proved by Sesh having it.
- [ ] **FIX — stale citations/maps:** retired law titles/numeric references and old
  checkout paths remain in historical material. Current docs cite Titles and actual
  owner paths; review typography substitutions without silently editing private notes.
- [ ] **DECIDE — workspace hygiene:** generated root b.json, .DS_Store and the
  untracked Rust helloworld scratch file need explicit ignore/retain/track choices.
  Do not discard unknown user edits or stage all repositories wholesale.
- [ ] **PROVE — personal/b:** adapter tests are scoped; TypeScript strip/parse is
  not type-checking, browser opener success is not rendering, SQL execution is not
  a sandbox, Cargo/native scripts can perform work, hardware upload is board-specific.
  Export/packaging and native project discovery remain separate product choices.
- [ ] **RECHECK — CLion integration:** root/per-repo adapters and run configurations
  have changed across sessions; verify present settings/real tool paths and user
  IDE behavior, not the old deleted-CMake story.
- [ ] **DECIDE — profiles:** `personal/vex-graph` and `ecosystem/.github` have artwork/
  markup checks, not remote-link longevity or user appearance approval. No runtime blockers inferred.
- [ ] **DECIDE — wiki maintenance:** `ecosystem/ecosystem` is the readiness owner;
  remove contradictory legacy claims carefully while preserving feature scope/history.
- [ ] **DECIDE — harness directory:** `ecosystem/repos/harness` exists with src but
  no independent .git/root README found. Clarify intended owner/status before
  advertising it as a separately delivered repository or runner.
- [ ] **PROVE — release publication:** inspect current local/remote state when
  publication is requested. Past one-off push permissions are consumed, not reusable.

## Other session follow-ups (not ecosystem implementation gates)

- [ ] **RECHECK — Arduino:** confirm current sketch/pin map, active-low LED wiring,
  common rails/ground, resistors, D12 pull-up/debounce, LDR threshold and potentiometer
  range/delay. Earlier exact-zero LDR and bad Serial.print advice was superseded by
  a later threshold/light helper session; inspect today's sketch before fixing it again.
- [ ] **PROVE — Arduino hardware:** latest behavioral edits were not all compiled/
  uploaded/hardware-tested. Native AVR toolchain support, board FQBN/port and physical
  current/polarity need real confirmation; formatting-only work did not prove behavior.
- [ ] **DECIDE — Tinkercad/capstone:** recover assignment acceptance criteria and
  current circuit/sketch; partial history is insufficient to certify completeness.
- [ ] **DECIDE — Roblox:** select project and trusted Studio/MCP or file-sync
  integration, permissions and exact task. No connection/game delivery is established here.
- [ ] **RECHECK — OpenCode cleanup:** a historical pruning script was prepared,
  not proof of successful cleanup. Locate/review it and back up before any separately
  authorized deletion; do not stop this session's service or erase history as backlog cleanup.
- [ ] **DECIDE — browser automation:** the cuadriver/manual-click session lacks
  a recoverable conclusion here. Restate task, target app and permission boundary.

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
| Relational Engine Storage Design and Build Readiness | Native ownership migration done; TypedPool done; MappedFile handoff not implemented. |
| Update all repositories for R2 relational engine naming | Ownership/docs/IDE fixes and SUGAR_VEX proof completed; downstream doc drift still needs reconciliation. |
| Testing button 12 in writin-phase.ino | D12 wiring/debounce and serial advice; hardware follow-up. |
| Find links to all repositories and projects in GitHub ecosystems | Rust/stable rows/bindings implemented later; persistence/GPU paths remain separate. Latest history partial. |
| Roblox Studio Buddy Check-In | Integration/setup proposal, not an established Studio connection. |
| Making `preferences.md` a one-file Gist | Canonical Gist publication/private lesson handling completed; do not publish private lessons through this backlog. |
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
| Ensuring Comprehensive Test Coverage in `tests/` | Skip-as-pass fixed; current owner/security/backend coverage still needs inventory. |
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

**Audit proof:** `python3 -B tests/tools/blockers_test.py` checks this document's
inventory/structure, source references and known critical seam descriptions. It
does not run or prove the features in this backlog. Per-file lab evidence belongs
in the checklist under the Timestamped Test Checklist Law.

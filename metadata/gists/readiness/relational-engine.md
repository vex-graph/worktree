# relational-engine — R2 Memory, Storage & Native C Search

**Repository:** https://github.com/vexgraph-ecosystem/relational-engine
**Workspace checkout:** `host-behavior/relational-engine`.
**Status:** partial backend, not a finished engine.

## Responsibility and transition

R2 has two cooperating repositories. [vexspoke](#file-vexspoke-md) owns CPU computation, math,
algorithms, synchronization and behavior APIs. Relational Engine owns memory
allocation/storage, stable row chunks, variable bindings and native C search
over Rust-owned spans. Production engine code includes no consumer/host headers;
imported C comparison code is not production dependency closure.

Native IO/NIO has migrated here and is linked by default; Vexspoke has no copies.
The C allocator ABI/semantics are preserved, not rewritten into Rust. Broader
container/Rust migration remains staged. R3 may borrow either R2 contract. R1 owns
code/storage residency and lifetimes; active users must stop before destruction.
GPU shaders, dispatch, capabilities and synchronization remain [graphvex](#file-graphvex-md) R3.
No C/Rust atomic-layout compatibility or automatic record-schema migration is
assumed. Actual Hotcwap live reload integration remains unproved.

## Feature inventory

The current engine README, local preferences and `tests/test-checklist.md` are
the implementation/proof sources. Registered owner proof now covers Rust
targets in debug/release, C row-pool/registry/name-search clients,
C-client ASan/UBSan and intended compile failures on the current macOS host.
Rows stay partial because these are bounded slices, not complete storage/type/
allocator parity. A documentation check does not promote runtime readiness.

| Feature | Scope / proof boundary | Status |
| :--- | :--- | :---: |
| Native Memory / scratch | Production engine-owned C ABI; tests/relational-engine/nio/mem_test.c, mem_exhaustion_test.c and transient_lifetime_test.c; all seven slab exhaustion, bounded bump spill/rejection (no untracked heap fallback), correct spill ownership, bump enumeration/reset, full-byte preservation, cross-owner realloc, injected construction/registry allocation failures and 10000 seeded mixed-size operations. macOS arm64 strict/release-like/ASan-UBSan plus focused TSan disjoint alloc/free and actual umbrella owner pass; synthetic lifetime fixture. Current workers retain at most four live blocks: thousands-live concurrent occupancy under the Deliberate Exhaustion and Backend Trust Law remains unproved, despite serial large-live-set exhaustion. No OS leak certificate, performance, all schedules, first-init/registry/reset concurrency, forged checksum, stale raw-pointer generation, Windows/macOS14 runtime or full readiness proof | 🟨 |
| Native File / Cache / Log / VexHome | Migrated default implementation; tests/relational-engine/io file/cache/writer/log/parser/home owners; scoped round trips, not exhaustive hostile-path/durability proof | 🟨 |
| Native ProcessSpawn / FrameInbox | tests/relational-engine/io/process_spawn_test.c and frame_inbox_test.c; bounded child reap/reuse/cancel and frame boundary owners; no WebSocket protocol implementation exists | 🟨 |
| Clipboard / HotFileSys | Native clipboard built but mutation owner SKIP without permission; HotFileSys lifecycle-only draft no-op, not file watching | 🟧 |
| Rust Memory and C ABI | Byte ownership, copy ABI, atomic byte and retained immutable string snapshots; tests/relational-engine/rust owners; not allocator parity or ecosystem type metadata | 🟧 |
| Stable Chunk / ChunkedList | Implemented Rust-owned stable append-only rows; tests/relational-engine/rust/nio and struct owners; no completed Vexspoke migration claim | 🟧 |
| TypedChunk / TypedPool | Implemented aligned rows, packed bitmap, lazy chunks, exclusive removal/hole reuse and empty backing reclamation; tests/relational-engine/rust/nio/typed_chunk_test.rs and struct/typed_pool_test.rs; fault recovery and seeded model pass, Rust sanitizer/Windows gaps remain | 🟨 |
| Generation handles | tests/relational-engine/rust/nio/handle_test.rs, typed_chunk_test.rs and struct/typed_pool_test.rs; zero rejection, exhaustion retirement and retained reclamation history; Rust typed handles owner-local, not pointer validation | 🟨 |
| C Rust byte-row pool | tests/relational-engine/rust/ffi/row_pool_test.c and mirrored Rust owners; aligned flat copied rows, stable growth, owner-tagged stale rejection, OOM preservation and named-binding teardown; C ASan/UBSan, no R3–R5 migration/automatic build wiring | 🟨 |
| Identity table geometry | Proposed 16-byte identity slots and 2 MiB chunks; separate geometry/metadata encoding unresolved | ⬜ |
| Optional object names / bulk / scratch | Existing bindings remain append-only borrowed pointers; object/name lifetime integration, 1 MiB binding geometry and separate contiguous/resettable APIs not yet implemented | ⬜ |
| VariableSlot / append-only registry | Implemented 32-byte slot, exclusive binding registry and opaque C ABI; tests/relational-engine/rust/variable owners; resolve once for hot access | 🟧 |
| Native C name search | Implemented scan over borrowed Rust-owned spans; tests/relational-engine/search/primitives owner; no C/Rust atomic-layout assumption | 🟧 |
| Type algebra / parent-chain resolver | Engine-owned `type/type.{h,c}`: 64-bit id encoding + masks, form/modifier/wrapper predicates, `Type_arch`, and per-project parent chains with cyclic/self-parent/out-of-range rejection and a bounded `Type_isA`; tests/relational-engine/type/type_algebra_test.c plus the vexspoke registry test pass under strict flags | 🟨 |
| Fixed-extent Rust FixedMappedFile | tests/relational-engine/rust/nio/fixed_mapped_file_test.rs and mapping_error_test.rs; existing regular-file read/shared-write byte views retained until close/drop, checked offset/count access, explicit writeback/sync, shared readers and unsafe/arity/type/borrow negatives pass macOS arm64 debug/release. Caller prevents external mutation/truncation; no resize, mapped C ABI, transactions or crash-durability claim. OS mapping/flush/sync failure injection, huge-file admission, Rust sanitizer and Windows/macOS14 runtime gaps remain | 🟨 |
| Reservation-backed Rust GrowableMappedFile + C ABI | tests/relational-engine/rust/nio/growable_mapped_file_test.rs (Rust owner) plus tests/relational-engine/nio/fixed_mapped_file_abi_test.c and tests/relational-engine/nio/growable_mapped_file_abi_test.c (C clients, strict + ASan/UBSan). Reserve once, grow sparsely inside the reservation, allocate-then-publish; the mapping is never remade, so a pointer taken before a step is byte-identical after it — asserted from Rust and from C. One extern-C surface per mapping (`re_mmap_*`, `re_gmap_*`). Gaps: no free-list reuse of released ranges yet (the committed length only ratchets up), no shrink, and Windows/Linux runtime proof. | 🟩 |
| File indexing / buffered I/O | Planned io responsibilities: buffered readers/writers, FFF-style gathering/indexing; no runtime implied | ⬜ |
| Physical byte-file preallocation | tests/relational-engine/rust/io/{preallocated_file,preallocation,preallocation_error,preallocated_failure}_test.rs; create-new full reservation without sparse fallback, decimal 1 GB allocated-block evidence, offset bit changes/sync/reopen, existing-path preservation, rejection cleanup/retry and same-descriptor mapping transfer. macOS arm64 debug/release owners pass; Linux source unproven, Windows Unsupported. APFS COW may require further space; OS mapping/sync/cleanup-error injection, Rust instrumentation and macOS14 runtime gaps remain | 🟨 |
| Manifest-backed persistent objects | Discussion only; no durable snapshots, journal/checkpoint implementation or concurrent file-commit promise | ⬜ |
| Codecs / virtual GPU-storage references | Planned compress/virtual contracts; never duplicate Graphvex shader/dispatch ownership | ⬜ |
| Consumer reload / schema migration | Resident storage required; live loader integration and rollback-tested schema upgrades remain future proof | ⬜ |

No production-ready, Windows, performance, Rust sanitizer or automatic migration
claim is made by this inventory. See [Home](#file-home-md) for the unfinished ecosystem/R5
application status and the canonical constitution linked from each repository.
Rust ASan currently skips for incompatible installed runtime; macOS 14 runtime
compatibility of the installed Rust standard library remains unproved.

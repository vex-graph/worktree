# darkbase — Native Vex Entity Store

> **Architectural Tier**: R3 Driver — the `Database` interface owner and its
> native vex store (future name `darkbase-db`); the R5 `darkbase` executable is a
> separate future host.
> **Current implementation:** the R3 `Database` registry, borrowed row binding,
> exact-stride owned copy-in, cursor, and legacy flat snapshot compatibility API
> are implemented. `Database_load` stages all owned rows before publishing them.
> This M2 dump is superseded and is not the persistence direction; pages + WAL
> now have a separate single-file page-level Store: real Rust mapping, embedded
> redo, reopen/repair and free-page reuse. Database/Headless adaptation, catalog,
> ordered indexes and journal recycling remain unfinished. Scoped owner evidence
> is recorded in `../test-checklist.md`.
> **Governing Laws**:
> 1. **Entity Model**: one shared reflection vocabulary — `struct` -> `Struct`
>    (entity/table), `field` -> `Field` (column: name + read/set + physical
>    offset/size/typeId/flags), `function` -> `Method`. `Class` = Struct +
>    constructor + Methods. No parallel darkbase schema types. One namespace.
> 2. **Reactive Programs**: named programs bound to store events
>    (`beforeInsert`, `afterInsert`, `onCommit`, ...) fire on the cold admission
>    path only; views are derived Entities; programs rebind by name on load.
> 3. **Not a SQL Engine**: the native query contract is structured; text/SQL is
>    only an optional `cli/` convenience or a foreign driver's translation.
> 4. **License Boundary**: GPL/LGPL client libraries (`libpq`,
>    `mariadb-connector-c`) are quarantined inside their own driver dylibs.
> 5. **Two-Layer Access Cap** and **dest-last** cursor fetches per the Semantic
>    Consistency Law.
> 6. **Per-Connection Isolation**: transactions are connection-scoped; deltas
>    journaled before mutating slots.
> 7. **Store Versus Executable Separation**: the store is a resident library; the
>    R5 executable borrows it via opaque handles and never includes store internals.

---

## Subsystem 1: Entity Model (schema AS C reflection)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 1.1 | `Struct` — entity/table | reflection: ordered `Field` list; `Struct.size` is the entity row stride | 🟧 | Entity = Struct; no DDL text. |
| 1.2 | `Field` — entity field + physical column | reflection: name + read/set + (typeId, offset, size, flags) | 🟧 | Extended in vexspoke; `setTypeId` derives size via `Stride_get`. Keystone for storage + export. |
| 1.3 | `Class` — entity + behavior | reflection: `Struct` + constructor + `Method[]` | 🟧 | |
| 1.4 | `Method` — function | reflection: named callable binding; exports name + signature + module | 🟧 | Rebinds by name on load. |
| 1.5 | `DbTrigger` — reactive program | darkbase: a `Method` + a store event | 🟥 | The one darkbase-owned schema-adjacent type. |
| 1.6 | Class registry `src/oop/type.h` | `PROJ_DARKBASE` + L2/trigger `ID_DB_*` | 🟧 | Registry header landed; reflection types carry their own vexspoke ids. |

## Subsystem 2: L2 `Database` Interface

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 2.1 | `Database` handle + entity registry | registers reflection `Struct` entities and owns per-entity row lists | 🟧 | In-memory switchboard; borrowed and copied row modes. |
| 2.2 | `Database_connect` / `Database_close` | structured connect over a declarative `DbUri`; bounded teardown | 🟥 | `Database_free` releases the registry only. |
| 2.3 | Structured query | typed field predicates + path resolution; returns `DatabaseResult` | 🟥 | `Database_select` cursor landed; predicates not yet. |
| 2.4 | `Database_define` / row insertion | register an entity; borrow or exact-stride copy-in; returns index | 🟧 | `database_test` covers both modes and mode-mixing rejection. |
| 2.5 | Dest-last cursor fetch | `DatabaseResult_next(result, outRow)` writes into caller destination | 🟧 | Landed; zero steady-state malloc. |
| 2.6 | Parameter binding | positional/named bind with `oop/type.h` tags | 🟥 | |
| 2.7 | Column metadata | count/name/type read from `Field` | 🟥 | `Field` now carries the layout. |
| 2.8 | Bounded diagnostics | `Database_lastError(db, buf, cap)`, error code enum | 🟧 | Landed (M1). |

## Subsystem 3: Reactive Programs (triggers, views, stored functions)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 3.1 | `DbTrigger` event binding | beforeInsert/afterInsert/beforeUpdate/beforeDelete/onOpen/onCommit/onRollback | 🟥 | Cold admission path only. |
| 3.2 | Program descriptor + rebind | export as data; code rebinds by name on load | 🟥 | No stored addresses. |
| 3.3 | Derived views | a view's rows computed by a program over the authoritative store | 🟥 | No second synchronized copy. |

## Subsystem 4: Native Paged Store (`.vexdb`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 4.1 | Legacy snapshot header | `VEXDB01` compatibility dump, entity/row counts | 🟧 | Superseded M2 format; not the specified pages + WAL path. |
| 4.2 | Table of contents | paged catalog of scopes, `Entity` schemas, page offsets | 🟥 | Not implemented; legacy snapshot has sequential records. |
| 4.3 | Sealed fixed-size pages | power-of-two frames in [512, 65536]; Page_load admits stored metadata; tests/darkbase-engine/page/page_test.c | 🟨 | Real mapping integration via Store; stored-used verification, corruption and failure preservation proved. Catalog still absent. |
| 4.4 | Value codec | live block <-> stable on-disk byte encoding (endianness-defined) | 🟧 | Flat native-endian row Bytes by `Struct.size`; per-`Field` codec later. |
| 4.5 | Checksums | per-page CRC32/xxHash64 | 🟧 | Per-page CRC32 seal now in `Page` (header + in-use payload, id and size included); WAL records checksummed through the shared `util/crc32`. Hot-path builder/verifier cost unproved. |
| 4.6 | Atomic compaction swap | temp write + atomic rename | 🟥 | |
| 4.7 | Single-file page-level Store | tests/darkbase-engine/store/store_test.c and store_adversarial_test.c through store/run.py; fresh real Rust/native dependencies, optimized and C ASan/UBSan | 🟨 | Create/reopen, full-page durable redo, allocation/release/reuse, two exhaustion bounds, 48 live full pages, three child-exit boundaries, torn-data repair and five injected IO stages. Not a durable Database/Headless adapter; journal is retained, not recycled. Global graph ratchet and Rust runtime-floor proof remain gaps. |

## Subsystem 5: Index & Spotlight Query

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 5.1 | Name index | native `re_name_search` over borrowed rows | 🟥 | Cold, linear; not an index yet. |
| 5.2 | B+ tree | fixed-page range index over field values | 🟥 | See the B-Tree Page Consistency Law. |
| 5.3 | Path resolution | `entity.field` walk via reflection | 🟥 | Cold reflection walk. |
| 5.4 | Raw-byte predicates | comparisons evaluated directly on row memory | 🟥 | No boxing. |
| 5.5 | Reverse usage index | entities referencing a target binding | 🟥 | Powers "find references". |

## Subsystem 6: Transactions & Concurrency

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 6.1 | Connection-scoped tx | begin/commit/rollback per connection | 🟥 | |
| 6.2 | Write-ahead log | standalone + embedded v3 fixed-region redo; tests/darkbase-engine/wal/wal_test.c | 🟨 | Leading commit marker gates bounds/CRC validation, body sync precedes marker, Store syncs marker before apply. Torn tails, committed corruption, capacity, failure preservation and replay proved; Database adaptation and safe embedded checkpoint recycling remain unimplemented. |
| 6.3 | Rollback journal | undo deltas for the active scope | 🟥 | |
| 6.4 | Shared/exclusive locks | multiple readers, single writer | 🟥 | |
| 6.5 | Bounded lock timeout | 100ms acquire with drop-degrade | 🟥 | Bounded Wait Law. |

## Subsystem 7: Export & Hosting

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 7.1 | Schema/type manifest | ids + `EntityField` layouts + `PROJ_DARKBASE` + version | 🟥 | For other repos to read/register. |
| 7.2 | CSV / JSON export | cold reflection walk | 🟥 | `toString`/`toStringStruct` legible form. |
| 7.3 | Generated C headers | emit C types from a registered schema | 🟥 | Output outside source trees. |
| 7.4 | Resident hosting | store loaded once by R1, resident across consumer reloads | 🟥 | Resident Storage Boundary Law. |
| 7.5 | Hot-swap rebind | functions/programs rebind by name after reload | 🟥 | Addresses change; names don't. |

## Subsystem 8: Driver Switchboard & Quarantine

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 8.1 | `DbDriver` vtable | connect/query/exec/next/begin/commit/close | 🟥 | Pure C ABI dylib contract. |
| 8.2 | `DbUri` decomposition | `scheme://user@host/db?params`, zero-copy views | 🟥 | Offline path + online URL. |
| 8.3 | Credential masking | redact passwords in logs/telemetry | 🟥 | |
| 8.4 | Scheme dispatch | `vexdb://` native default; others later | 🟥 | |
| 8.5 | Quarantined drivers | sqlite/postgres/mariadb/cloud as isolated dylibs | ⬜ | License boundary. |

## Subsystem 9: Vector & Embedding Index

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 9.1 | Fixed-dimension vector slot | 128/256/512/1536-dim float slabs | ⬜ | |
| 9.2 | SIMD cosine similarity | NEON/AVX distance | ⬜ | |
| 9.3 | HNSW semantic graph | top-K nearest neighbor search | ⬜ | |

## Subsystem 10: R5 Executable Host (future `darkbase`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 10.1 | Interactive host | opens a `.vexdb` and works with it | ⬜ | R5 app over the R3 store. |
| 10.2 | Query workbench | structured + optional text query surface | ⬜ | Optional `cli/` parser, never core. |
| 10.3 | Migration engine | versioned schema migrations | ⬜ | |
| 10.4 | Dump/export tools | CSV/JSON/`.vexdb` snapshots | ⬜ | |
| 10.5 | Benchmark profiler | query time, cache hits, page faults | ⬜ | |

---

## Defect Log & Seam Status

- **Status**: `Database` registers reflection `Struct` entities, supports borrowed
  rows and exact-stride owned copies, and exposes `DatabaseResult` as a dest-last
  cursor. A legacy `.vexdb` flat snapshot reader/writer remains for compatibility;
  load preflights and stages all owned rows before publication. The format is
   superseded, not the forward persistence design. The separate page-level Store
   now connects embedded Wal, sealed Page and Rust mapping in one file; reopen
   replays before admission and free pages are reused. Database/Headless mutation
   adaptation, catalog/indexes, journal recycling, triggers and durable audit are
   still missing. Current executed owner evidence is in `../test-checklist.md`.
- **Not a SQL engine:** the earlier 13-subsystem SQL/driver matrix is retired in
  intent; this page is the current lens. The API is structured; SQL is optional
  and peripheral.
- **R2 foundation is not blanket readiness:** the engine's stable rows and native
  name search are partial; a historical result does not prove darkbase
  integration or durability.
- **Implementation strategy**:
  1. M1 in-memory struct store — `Database` + reflection `Struct`/`Field` +
     insert/get + dest-last cursor (no disk).
  2. M2 persistence/export — `.vexdb` pages + codec + export.
  3. M3 index + structured query.
  4. M4 transactions/WAL.
  5. M5 switchboard + one quarantined driver.
  6. M6 reactive programs + vectors.

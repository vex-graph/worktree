# Database Switchboard

**Idea (in vexgraph's words):** support MariaDB, Postgres, other databases,
online database APIs — *and* my own database as well, so it all settles.

Not a database engine. A **switchboard**: one interface, many backends.
App code talks to `Database`; behind it sits whichever store fits —
local file offline, Postgres at work, a cloud API on the road, the native
vex store by default.

## Shape (from the whiteboard session)
- **L2 `Database` interface class**: `connect`, `query`, `exec`,
  `begin/commit`, `close`, plus a `DatabaseResult` row type and
  cursor-style fetch (`next(row, dest)`) — fixed buffers, zero
  steady-state malloc, same pattern as `Http_perform`.
- **Each driver = one L3 module dylib** with a HotManifest:
  `postgres`, `mariadb`, `vexdb` (native), `online_api`, ...
  ABI-checked, hot-swappable without restarting the app.
- **Connection strings = L1 metadata**: local path offline, URL online,
  same call. Declarative, swappable with zero code changes.
- **Manifest boundary = license boundary**: client libs (`libpq`,
  `mariadb-connector-c`) and their licenses stay quarantined inside
  their driver module. The core never touches them.

## Constraints (sized honestly)
1. Client libraries are the tax: system / FetchContent C linking +
   version drift, contained per driver.
2. No cross-database transactions. Per-connection only — anyone promising
   MariaDB-to-Postgres atomic commits is selling something.
3. Online API drivers are thin translators: `Database_query` → REST
   (the HTTP client already exists) → rows.

## Sequencing
1. `Database` interface + native local driver (offline works, zero deps).
2. Postgres driver (proves the boundary with a real client lib).
3. MariaDB + online APIs (same pattern, cheaper each time).

## Status
Envisioned, not started. No `Database` class exists yet; raw materials
(`io/file`, `vfs`, `mmap`, `net/http`) are in place.

## Next step
Plan the `Database` interface turn: struct fields, function registry
(constructors/core/setters/getters), driver manifest contract
(exports a driver must provide: `DbDriver_connect/query/exec/...`).

# How sesh Works: Session Sync, VPS Relay, Bug Ingestion

> The architecture doc for R4 Interface. **There is no code yet** —
> everything here is the planned shape. Read this BEFORE writing the
> first `.c` file.
> Answers the fundamental question: **"How do sessions sync across
> machines, and how do bugs get home?"**
> Answer: **thin fixed-slot packets over bounded WebSocket fanout, and
> a sanitized telemetry pipe to a VPS or Cloudflare.**

---

## 1. The Short Answer: It Doesn't Run Code — It Ships State

sesh owns three jobs, all passing fixed-stride packets:

1. **Session sync** — live cursors, whiteboard deltas, wireframe
   edits between participants over `HavenWsFanout` (bounded 16-slot
   fanout, no threads, no owned sockets)
2. **Bug ingestion** — crash dumps, memory-arena health logs, scene
   snapshots forwarded from R5 apps to a self-hosted VPS or Cloudflare
3. **Edge relay** — Cloudflare Workers/Tunnels/Turnstile contracts so
   the VPS is optional

Every packet is fixed-stride `{session_id, user_id, delta_kind,
payload}` on vexspoke ring buffers and arenas. Zero steady-state
allocation. Bounded ≤100ms waits on every network slice (Rule 27).

---

## 2. Where It Sits (Read This Once)

```text
R1 hotcwap   — boots first, owns Kernel/Window, tears down last
R2 vexspoke  — arenas, net/http, threads, WsClient
R3 api-haven — connectors: HavenWsFanout, AiSse, McpServer
R4 sesh      — session sync, VPS relay, bug ingestion. WE ARE HERE (planned).
R5 apps      — darling-editor, semicolon, anti (consume sesh)
```

sesh is R4 — it borrows shapes from R2 vexspoke (WsClient, ring
buffers, arenas) and R3 api-haven (HavenWsFanout only). It never
includes graphics engines or other R4 repos.

---

## 3. The Dependency Contracts (exist TODAY, in sibling repos)

### 3a. HavenWsFanout (api-haven) — the primary connector

16 fixed rows, no allocation. Each row is `{handle, source}` where
`source` is a fn-table:

```c
typedef struct HavenWsSource {
    bool (*connect)(void *handle);
    uint32_t (*poll)(void *handle, uint64_t budgetMs);
    bool (*send)(void *handle, const uint8_t *bytes, uint32_t len);
    void (*close)(void *handle);
} HavenWsSource;
```

`HavenWsFanout_pollStep(fanout, budgetMs)` slices the budget evenly
across live rows (min 1ms each) and returns frames delivered.

### 3b. WsClient (vexspoke) — the R2 leaf driver

Fixed 4096-byte rx buffer, state machine (IDLE → CONNECTING → OPEN →
CLOSING → CLOSED). Bytes are fed in by R1; poll drains with bounded
100ms wait in ~1ms cancel-checked slices. Zero threads, zero
allocation.

---

## 4. The Four Problem Domains (from README)

| Domain | What it does | Backend |
|---|---|---|
| Multiplayer Canvas | notes/whiteboards/wireframes + live cursors | HavenWsFanout |
| Bug Catcher | crash dumps, arena health, scene snapshots | VPS/Cloudflare ingest |
| Edge Relay | reverse proxy, Turnstile, KV/R2 storage | Cloudflare Workers |
| Zero-Alloc Sessions | fixed-stride session records | vexspoke rings + arenas |

Consuming apps: `darling-editor` (sessions), `semicolon` (remote
pairing), `anti` (bug reporting).

---

## 5. The Roadmap (from _checklist/sesh.md)

All 8 core features are unstarted:

| # | Feature | Status |
|---|---|---|
| 1 | Session State Engine — fixed-slot `{session_id, user_id, delta}` | not started |
| 2 | Live Cursor Pairing — 60Hz multi-user cursor + interpolation | not started |
| 3 | Room & Channel Manager — multi-room over bounded fanout | not started |
| 4 | VPS Relay Protocol — lightweight C relay | not started |
| 5 | Cloudflare Worker Bridge — Turnstile, tokens, proxy | not started |
| 6 | Cloudflare Tunnel Hook — local-to-VPS ingress | not started |
| 7 | In-Engine Bug Ingestion — dumps + snapshots endpoint | not started |
| 8 | Telemetry Packet Sanitizer — PII stripping + symbolication | not started |
| 9 | Delta Compression — RLE + XOR | backlog |
| 10 | Offline Sync Queue — local queue + reconnect | backlog |

---

## 6. The Class Shapes (design stubs, conforming to Rule 23)

When `src/sesh/*.c` lands, each file is one class, one problem:

- **Session** (L2) — fixed-slot session state engine. Fields:
  session_id, user_id, delta_kind, payload. Zero allocation.
- **CursorPair** (L2) — 60Hz remote cursor with interpolation.
- **RoomChannel** (L2) — multi-room lifecycle over HavenWsFanout.
  Fixed room slots; fanout attach/detach via WsSource tables.
- **RelayWorker** (L4) — VPS relay protocol. Bounded polls.
- **EdgeBridge** (L4) — Cloudflare Worker/Tunnel/Turnstile contracts.
- **BugIngest** (L4) — crash dump + snapshot endpoint.
- **Sanitizer** (L2) — PII stripping + stack symbolication.

---

## 7. Build Wiring Gaps (must fix when code lands)

1. **CMake** only links `vexspoke` via FetchContent seam — missing
   `if(NOT TARGET api-haven)` FetchContent block for `HavenWsFanout`
2. **Umbrella** `CMakeLists.txt` has no `add_subdirectory(projects/sesh)`
3. **No independent git repo** — sesh is a plain dir inside the
   umbrella; upstream would be `github.com/vexgraph-ecosystem/sesh`

---

## 8. Key Architectural Commitments (non-negotiable)

1. **Fixed-stride packets**: `{session_id, user_id, delta_kind,
   payload}` — no variable-length envelopes on the hot path.
2. **Zero steady-state allocation**: packets live in arenas/rings.
3. **Bounded waits**: every network slice ≤100ms (Rule 27).
4. **HavenWsFanout-style seams**: fixed tables + opaque fn-tables.
5. **PII sanitizer before upload**: never ship raw dumps upstream.
6. **No interface scraping**: verified API contracts only (Rule 34).
7. **Teardown**: `Memory_freeAll` last (Rule 26).
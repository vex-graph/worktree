# Sesh — Living Docs

> The 2am README for R4 Interface. **Greenfield: no code yet.** This is
> the planned shape — read it BEFORE writing the first `src/*.c`.
> See also [`_docs/how-it-works/how sesh works.md`](../how-it-works/how%20sesh%20works.md).

---

## 1. Position

R4 Interface — session sync, VPS relay, in-engine bug ingestion,
Cloudflare edge sync. Borrows shapes from R2 vexspoke (WsClient,
rings, arenas) and R3 api-haven (HavenWsFanout only). Never graphics
engines.

Consumers: `darling-editor` (sessions), `semicolon` (remote pairing),
`anti` (bug reporting).

## 2. What Exists Today

| File | State |
|---|---|
| `CMakeLists.txt` | builds static lib only when `src/*.c` exists; today's branch = bare custom target |
| `CONTRIBUTING.md` | 5 ecosystem invariants |
| `README.md` | planned architecture (N/A for actual code — fix when code lands) |
| `LICENSE` | Boost Software License 1.0 |
| `src/` | does not exist yet |

## 3. The Contracts It Will Bind To

**HavenWsFanout** (api-haven, exists):
- 16 fixed rows `{handle, source}`; zero allocation
- `HavenWsSource` fn-table: `{connect, poll, send, close}`
- `pollStep(fanout, budgetMs)` slices budget evenly across live rows

**WsClient** (vexspoke, exists):
- Fixed 4096B rx buffer, state machine, 100ms max poll (Rule 27)
- Zero threads, zero allocation; bytes fed by R1 driver

## 4. The Roadmap

| # | Feature | Status |
|---|---|---|
| 1 | Session State Engine — fixed-slot `{session_id, user_id, delta}` | not started |
| 2 | Live Cursor Pairing — 60Hz cursor + interpolation | not started |
| 3 | Room & Channel Manager — multi-room over bounded fanout | not started |
| 4 | VPS Relay Protocol — lightweight C relay | not started |
| 5 | Cloudflare Worker Bridge — Turnstile, tokens, proxy | not started |
| 6 | Cloudflare Tunnel Hook — local-to-VPS ingress | not started |
| 7 | In-Engine Bug Ingestion — dumps + snapshots | not started |
| 8 | Telemetry Packet Sanitizer — PII strip + symbolication | not started |
| 9 | Delta Compression — RLE + XOR | backlog |
| 10 | Offline Sync Queue — local queue + reconnect | backlog |

## 5. Planned Class Shapes (Rule 23)

When landing, one class per file under `src/`:

- **Session** (L2) — session state engine
- **CursorPair** (L2) — remote cursor interpolation
- **RoomChannel** (L2) — room lifecycle over fanout
- **RelayWorker** (L4) — VPS relay protocol
- **EdgeBridge** (L4) — Cloudflare Worker/Tunnel/Turnstile
- **BugIngest** (L4) — dump + snapshot endpoint
- **Sanitizer** (L2) — PII stripping

## 6. Build Wiring Gaps (fix when code lands)

1. CMake missing `if(NOT TARGET api-haven)` FetchContent seam for
   HavenWsFanout
2. Umbrella `add_subdirectory(projects/sesh)` missing
3. No independent git repo / remote yet (upstream:
   `https://github.com/vexgraph-ecosystem/sesh`)

## 7. Non-Negotiables

Fixed-stride `{session_id, user_id, delta_kind, payload}` packets;
zero steady-state allocation; ≤100ms bounded waits; HavenWsFanout
seams; PII-strip before upload; verified API contracts only; teardown
`Memory_freeAll` last.
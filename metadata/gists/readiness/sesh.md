# sesh — Session Management, VPS Relay & Cloudflare Edge

> **Session composition and snapshot cores; not implemented distributed sync.** R2 comprises [vexspoke](#file-vexspoke-md) CPU
> computation/behavior and [relational-engine](#file-relational-engine-md) memory/storage/native C search.
> Sesh may borrow both R2 public contracts and api-haven. Native production IO/NIO
> and compatible Memory C semantics are engine-owned by default, not rewritten
> into Rust. Snapshot integration remains staged: proof uses caller buffers, not live engine integration,
> atomic-layout equivalence or schema migration. R1 owns lifetimes/residency; GPU
> shaders/dispatch remain [graphvex](#file-graphvex-md). Cloudflare R2 below is a service name,
> not the ecosystem's runtime rank.

> **Architectural Tier**: R4 Interface (Networked collaboration, telemetry, and session state bridge).
> **Production Standard**: *The Zero-Friction Multiplayer & Telemetry Relay: Zero-Alloc Session Records + Live 120Hz Remote Cursors + Collaborative Whiteboard & Canvas Sync + Standalone C Relay Daemon (`seshd`) + In-Engine Bug Snapshot Ingestion + Cloudflare Edge Bridge*.
> **Governing Laws**:
> 1. **Zero Steady-State Allocation**: Network session packets use fixed-stride `{session_id, user_id, delta_kind, payload}` records on top of `vexspoke` ring buffers and memory arenas.
> 2. **Bounded Network Timeouts**: All poll and socket drain operations enforce a strict 100ms maximum wait with drop-degrade (the Bounded Wait Law).
> 3. **Privacy-First Sanitization**: Crash dumps and telemetry undergo strict PII stripping and credential scrubbing before transmission (the Cold-Strict, Hot-Minimal Validation Law).
> 4. **Dest-Last Packet Writing**: Serialization and packet decoding routines follow `fn(src, dest)` (the Semantic Consistency Law (Argument order)).
> 5. **No Arrow Sugar**: `(*ptr).field` always (the Semantic Consistency Law (Reference form)).

---

## First implemented slice: snapshot backup

| Feature | Scope | Status | Notes |
| :--- | :--- | :--- | :--- |
| SeshSnapshot | Caller-buffer upload admission, pending/retry/cancel and bounded projections; `../../../tests/sesh/snapshot/snapshot_test.c` via `python3 tests/sesh/run.py` | 🟨 | macOS strict + ASan/UBSan offline fake round trip. No durable journal, cloud provider, overall transfer deadline, host integration or collaboration proof. |
| Google Drive backup | API Haven OAuth/HTTPS/upload/download adapter | 🟥 | Proposed first cloud backend; only ignored `../../../tests/sesh/test.txt` intended for explicit smoke test. No account contacted. |
| iCloud backup | Future platform-specific storage adapter | ⬜ | Requires separate identity/entitlement integration. |
| FileSession | Explicit local file save via selected provider | 🟥 | Accepted public API proposal; no implemented class or workflow proof. |
| DirectorySession | Explicit directory sync, new/empty-target clone and baseline-aware conflict detection | 🟥 | Needs real R2 traversal, versioned manifest and API provider integration. Snapshot callback proof does not establish directory sync. |

## Session composition (`lang/`)

| Feature | Scope | Status | Notes |
| :--- | :--- | :--- | :--- |
| AuthService | Borrowed API Haven credentials + injected identity verifier; `../../../tests/sesh/session/auth_service_test.c` | 🟨 | Revocation and secret-free projections proved; real OAuth/issuer mapping/expiry integration absent. |
| SeshClient | Host-assigned installation ID, `lang/client.h`; `../../../tests/sesh/session/client_test.c` | 🟨 | Graphvex Client interop proved; automatic global uniqueness and durable identity not implemented. |
| Workspace | Private principal-owned namespace metadata; `../../../tests/sesh/session/workspace_test.c` | 🟨 | No remote ACL enforcement or shared roles. |
| Resource | Workspace target + local revision; `../../../tests/sesh/session/resource_test.c` | 🟨 | Metadata only, no data storage or remote compare-and-swap. |
| Operation | Client-scoped immutable copied intent; `../../../tests/sesh/session/operation_test.c` | 🟨 | Identity/revision value object, not file/SQL execution. |
| Operations | Growable flat intent/receipt ledger; `../../../tests/sesh/session/operations_test.c` | 🟨 | Host-backed reserve, copied intent, receipt-aware apply/replay, failure preservation; clear/reset needs coordinated epoch/baseline. |
| Sesh | Five-part composition and scoped local revision admission; `../../../tests/sesh/session/sesh_test.c` | 🟨 | Caller serialization required across shared parts; close detaches. No internal thread safety or distributed transaction. |

Registered `python3 tests/sesh/session_run.py` (also in the main Sesh runner)
executes ten independent class/helper/interop owners each strict C23 and ASan/UBSan,
plus the synchronized four-client Sesh owner under TSan. Numeric identities are
host-assigned; matching local IDs does not establish remote authorization. API
Haven owns provider protocol/OAuth; database owners retain transaction semantics.
FileSession/DirectorySession remain proposals composing Sesh, not delivered workflows.

## Subsystem 1: Zero-Allocation Session State Machine (`SessionEngine`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 1.1 | Fixed-Stride Session Record | `[sessionId (64b)][userId (32b)][deltaKind (16b)][seq (32b)][payload (256b)]` | 🟥 | Flat, cache-aligned packet representation. |
| 1.2 | Multi-User Session Room Pool | Fixed array of 16/32 active participant slots per session room | 🟥 | Zero dynamic heap allocation per connected user. |
| 1.3 | Monotonic Sequence Tracking | Per-user monotonic packet sequence counters for loss detection | 🟥 | Detects dropped frames and out-of-order packets. |
| 1.4 | Heartbeat & Liveness State | Ping/pong liveness checks with automatic timeout disconnect | 🟥 | 5-second silence disconnects stale clients. |
| 1.5 | Room Lifecycle Manager | `Session_createRoom`, `Session_joinRoom`, `Session_leaveRoom` | 🟥 | Clean entry/exit state transitions. |

---

## Subsystem 2: Multi-User Realtime Presence & Remote Cursors (`Presence`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 2.1 | 120Hz Remote Cursor Broadcast | High-frequency cursor position packets `{float x, y; uint32_t flags;}` | 🟥 | Sub-8ms latency cursor updates. |
| 2.2 | Dead Reckoning & Lerp Smoothing | Hermite spline / linear interpolation between remote cursor updates | 🟥 | Smooth 120Hz cursor rendering even over jittery network. |
| 2.3 | Remote User Hover Badges | Displays remote user name tag, avatar color, and selection highlight | 🟥 | Renders live remote pointers in `darling-editor` canvas. |
| 2.4 | Active Selection Replication | Broadcasts selected widget/node IDs to all room participants | 🟥 | Shows colored selection bounding boxes for peers. |
| 2.5 | Viewport Pan/Zoom Tracking | Broadcasts camera position for "Follow User" presentation mode | 🟥 | Synchronizes multi-user viewports during reviews. |

---

## Subsystem 3: Collaborative Canvas Sync (`CanvasSync`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 3.1 | Node Create/Move/Delete Sync | Replicates board cards, sticky notes, and shapes for `darling-editor` | 🟥 | Replicated delta events. |
| 3.2 | Mindmap Connector Wire Sync | Real-time orthogonal line re-routing when connected nodes move | 🟥 | Synchronizes line anchors and bezier points. |
| 3.3 | Text & Markdown Live Edits | Character insertion and deletion deltas for collaborative text editing | 🟥 | Micro-deltas for concurrent typing without full string resends. |
| 3.4 | Drawing Brush Stroke Stream | Replicates ink strokes in real-time for `drawling` shared sketchpads | 🟥 | Streams stroke vertex packets `{x, y, pressure}`. |
| 3.5 | Conflict-Free State Merging | Last-Write-Wins (LWW) timestamped state resolution | 🟥 | Deterministic conflict resolution across concurrent edits. |

---

## Subsystem 4: Standalone VPS Relay Daemon (`seshd`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 4.1 | Headless C Relay Server | Standalone binary compiled with pure POSIX BSD sockets / kqueue | 🟥 | Low memory footprint (< 4MB RAM). |
| 4.2 | Room-Based Packet Fanout | Forwards client packets to other participants in the same room | 🟥 | Zero packet inspection; pure low-latency forwarding. |
| 4.3 | Epoll / Kqueue Event Loop | Non-blocking socket I/O multiplexer handling thousands of concurrent conns | 🟥 | High-concurrency event-driven network loop. |
| 4.4 | Rate Limiting & Abuse Prevention | Token bucket rate limiter per IP preventing broadcast flood attacks | 🟥 | Drops abusive connections gracefully. |
| 4.5 | Systemd / Launchd Service Config | Native service descriptors for background deployment on Ubuntu/Debian/macOS | 🟥 | Automated startup and crash restarts. |

---

## Subsystem 5: Cloudflare Edge Integration & Tunnels (`CloudflareEdge`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 5.1 | Cloudflare Worker Edge Handler | Serverless edge script validating session tokens and routing WebSockets | 🟥 | Sub-10ms global edge authentication. |
| 5.2 | Cloudflare Tunnel Ingress | Integrates with `cloudflared` for secure local-to-VPS ingress | 🟥 | Exposes local sessions without opening firewall ports. |
| 5.3 | Turnstile Bot Protection | Verification contract for Cloudflare Turnstile CAPTCHA-free tokens | 🟥 | Secures public room joins against bots. |
| 5.4 | R2 Asset Bucket Ingestion | Direct upload of large scene snapshots and assets to Cloudflare R2 | 🟥 | High-capacity blob storage for engine crash dumps. |

---

## Subsystem 6: In-Engine Bug Catcher & Crash Ingestion (`BugCatcher`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 6.1 | Serialized Crash Snapshot Ingestion | Ingests `.antidump` and `.crash` binary records from `anti` and `semicolon` | 🟥 | Captures register states, memory arena statistics, and stack traces. |
| 6.2 | Scene Graph Snapshot Packager | Packages active 3D/2D scene graph state into diagnostic reproduction file | 🟥 | Allows developers to reproduce bugs by re-opening exact scene state. |
| 6.3 | Low-Overhead Exception Hook | Signal handlers (`SIGSEGV`, `SIGBUS`, `SIGABRT`) capturing crash context | 🟥 | Writes local crash log before process termination. |
| 6.4 | Telemetry Dispatch Queue | Asynchronously uploads bug reports in background via `net/http` | 🟥 | Non-blocking dispatch that does not interrupt normal usage. |

---

## Subsystem 7: Telemetry Packet Sanitizer & Symbolicator (`TelemetrySanitizer`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 7.1 | PII & Secret Scrubbing | Regex-based removal of emails, API keys, passwords, and tokens | 🟥 | Enforces the Cold-Strict, Hot-Minimal Validation Law. |
| 7.2 | Path Normalization | Strips local filesystem user paths (`/Users/vexgraph/...` -> `~/...`) | 🟥 | Protects developer identity in public crash logs. |
| 7.3 | Stack Frame Symbolication | Resolves raw program counters against dSYM / ELF symbol tables | 🟥 | Produces human-readable function names and line numbers. |
| 7.4 | System Profile Embedding | Attaches `HardwareInfo` and `GraphicsInfo` to crash reports | 🟥 | Embeds GPU, VRAM, and OS version for bug triage. |

---

## Subsystem 8: Network Delta Compression & Framing (`WireProtocol`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 8.1 | XOR & Varint Delta Compression | Compresses successive coordinate and state updates | 🟥 | Reduces 120Hz packet size to < 16 Bytes per frame. |
| 8.2 | MTU-Aware Packet Chunking | Chunks large asset and scene transfers to fit standard 1400-byte MTUs | 🟥 | Eliminates IP-level packet fragmentation. |
| 8.3 | Binary Packet Framing | 4-byte length prefix + CRC16 integrity checksum | 🟥 | Framing protocol for TCP/WebSocket byte streams. |
| 8.4 | Compression Benchmarks | Latency and ratio benchmarks over synthetic canvas edit traces | 🟥 | Validates sub-microsecond compression cost. |

---

## Subsystem 9: Offline Sync Queue & Reconnection (`SyncQueue`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 9.1 | Local Journal Ring Buffer | Stores un-acknowledged session mutations in persistent local buffer | 🟥 | Preserves user work during network dropouts. |
| 9.2 | Exponential Backoff Reconnect | Automatic reconnect loop with jitter (100ms -> 500ms -> 2s -> 5s) | 🟥 | Avoids thundering herd on relay server restarts. |
| 9.3 | Reconnection State Reconciliation | Fast-forwards missed room packets on successful reconnect | 🟥 | Restores consistent canvas state upon link re-establishment. |
| 9.4 | Bounded Offline Queue Drop-Degrade | Caps offline mutation queue at 10,000 packets | 🟥 | Protects memory arena from overflow during long disconnects. |

---

## Subsystem 10: Security & Session Encryption (`Security`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 10.1 | Ephemeral Session Passcodes | 6-digit or UUID join tokens validating room access | 🟥 | Prevents unauthorized room eavesdropping. |
| 10.2 | HMAC Frame Signatures | Authenticates packet sender using shared session secret | 🟥 | Prevents packet tampering on untrusted relays. |
| 10.3 | Replay Attack Prevention | Timestamp window + monotonic sequence validation | 🟥 | Discards duplicate or delayed replay packets. |
| 10.4 | End-to-End Encryption Seam | Optional ChaCha20-Poly1305 payload encryption layer | ⬜ | Roadmap: confidential enterprise collaboration rooms. |

---

## Defect Log & Seam Status

- **Status**: Session composition/local identity admission and caller-buffer snapshot scheduling implemented with scoped offline proof; cloud, file/directory workflows and distributed collaboration remain unfinished.
- **Dependencies**: Vexspoke CPU contracts, engine-owned IO/NIO when needed, and API Haven provider vocabulary. Actual network and storage integration remain gaps.
- **Implementation Strategy**:
  1. Build `seshd` standalone relay daemon.
  2. Implement `SessionEngine` packet framing and presence cursor broadcasting.
  3. Wire in-engine bug snapshot capture in `anti` and `semicolon`.
  4. Hook collaborative canvas synchronization into `darling-editor`.

# api-haven — Connector Contracts, Telemetry, MCP & Asset Catalog

> **R2 dependency contract:** R3 may borrow [vexspoke](#file-vexspoke-md) CPU computation/behavior
> and/or [relational-engine](#file-relational-engine-md) memory/storage/native C search public contracts.
> Current Vexspoke memory/container ABI and default allocator remain during staged
> migration. This map claims no engine integration, automatic schema migration or
> C/Rust atomic-layout compatibility. R1 owns lifetimes; GPU dispatch stays R3.

> **Architectural Tier**: R3 Driver (Connectors, AI/DB/Asset catalogs, MCP server, webhooks).
> **Production Standard**: *The Universal Connector & Multi-Model Switchboard: 260+ AI Providers + 25 DB Catalogs + 12 Blessed Asset Sinks + MCP stdio Server + Multi-Model Envelopes (OpenAI/Anthropic/Gemini) + Zero Vendor SDK Weight*.
> **Governing Laws**:
> 1. **Zero Vendor SDK Weight**: Pure C23 contracts over `vexspoke` (`net/http`, `net/json`, `io/file`, `nio/mem`); zero external vendor libraries linked (the Vertical Integration Law).
> 2. **Legal-Sense Asset Sourcing**: Public APIs and licensed catalogs only (the Asset Sourcing Law: no scraping, explicit license on every row).
> 3. **Cold-Strict Input Validation**: Bounded buffers, strict payload length checking, zero buffer overruns (the Cold-Strict, Hot-Minimal Validation Law).
> 4. **Dest-Last Buffer Layout**: Parameter writes follow `fn(src, dest)` (the Semantic Consistency Law (Argument order)).
> 5. **No Arrow Sugar**: `(*ptr).field` always (the Semantic Consistency Law (Reference form)).

---

## Subsystem 1: Model Context Protocol (MCP) Server (`mcp/*`, `../../_trash/main/mcp_main.c`)

### Snapshot storage vocabulary (new, provider-neutral)

| Feature | Scope | Status | Notes |
| :--- | :--- | :--- | :--- |
| Snapshot IO contract | `storage/snapshot_io.h` put/get signatures and result vocabulary; `../../../tests/api-haven/storage/snapshot_io_test.c` via `python3 tests/sesh/run.py` | 🟨 | Real strict C23 header client + ASan/UBSan; Sesh fake round trip. Contract only, not Drive/OAuth/HTTPS, provider idempotency or durable backend proof. |
| Google Drive connector | Desktop OAuth, scoped file upload/download and identity mapping | 🟥 | Proposed; no live account or cloud writes performed. |

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 1.1 | MCP stdio JSON-RPC Framer | Newline-delimited JSON-RPC 2.0 parser over stdin/stdout | 💚 | 64KiB maximum line buffer cap; EOF exits cleanly with code 0. |
| 1.2 | `mcp_server` Standalone Binary | Standalone CLI executable for Claude Desktop, Cursor, and IDEs | 💚 | Compiled and tested; stdout strictly pure JSON-RPC. |
| 1.3 | Protocol Initialization Handshake | Handles `initialize` and `notifications/initialized` requests | 💚 | Declares server name, version, tools, and resources capabilities. |
| 1.4 | 14 Built-In Engine Tools | `tools/list` and `tools/call` for system probes, hardware, and assets | 💚 | Exposes `AppDetect`, `CaptureTool`, `HardwareInfo`, `DisplayInfo`, etc. |
| 1.5 | 7 Built-In Engine Resources | `resources/list` and `resources/read` for catalog inspection | 💚 | URI templates (`ai://providers`, `db://providers`, `asset://providers`, etc.). |
| 1.6 | Tool Parameter Validation | Validates required arguments against tool JSON schema definitions | 💚 | Returns clean JSON-RPC error codes on schema mismatch. |
| 1.7 | Headless Conformance Test | `mcp_server_test` automated test verifying JSON-RPC frames | 💚 | Verifies initialization, tool listing, and resource reads. |

---

## Subsystem 2: AI Provider Catalog & Multi-Region Quotas (`ai/ai_provider`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 2.1 | 260+ AI Provider Catalog | Global, European, and Chinese AI providers (`providers_*.inc`) | 💚 | Verified passing with exactly 260 catalog rows in `ai_provider_test`. |
| 2.2 | Regional Partitioning | Global (`providers_global.inc`), Europe (`providers_europe.inc`), China (`providers_china.inc`) | 💚 | Segregated by data sovereignty and regional network reachability. |
| 2.3 | Quota & Rate Limit Fields | Requests-per-minute (RPM), tokens-per-minute (TPM), daily quotas | 💚 | Enables client-side rate limit throttling before request dispatch. |
| 2.4 | Provider Lookup by Slug | `AiProvider_get(slug)` returning slot record | 💚 | Case-insensitive lookup (e.g. `openai`, `anthropic`, `gemini`, `deepseek`). |
| 2.5 | Free-Tier & Privacy Flags | Metadata flags indicating free availability and zero-data-retention | 💚 | Flags privacy-preserving and open-weights endpoints. |
| 2.6 | Code Generator Script | `gen_providers.py` generating `.inc` tables from source database | 💚 | Automated regeneration keeping endpoints in sync. |

---

## Subsystem 3: Multi-Model AI Chat Envelopes (`ai/ai_chat*`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 3.1 | OpenAI Compatible Envelope | `AiChat_buildRequest` with `{"model":..., "messages":[...]}` | 💚 | Universal standard adopted by OpenAI, DeepSeek, Groq, Together, etc. |
| 3.2 | Anthropic Messages Envelope | `AiChatAnthropic_buildRequest` (`/v1/messages`, `x-api-key`, `anthropic-version`) | 🟩 | Specialized envelope for Claude 3.5 Sonnet / Haiku / Opus models. |
| 3.3 | Google Gemini Envelope | `AiChatGemini_buildRequest` (model in URL path, `x-goog-api-key`, contents) | 🟩 | Specialized envelope for Gemini 1.5 / 2.0 Flash / Pro models. |
| 3.4 | Temperature & Max Tokens Tuning | Encodes temperature, top_p, top_k, max_tokens parameters into payload | 💚 | Parameter serialization directly via `net/json` writer. |
| 3.5 | System Prompt Injection | Formats system instructions into respective provider wire formats | 💚 | Handles Anthropic top-level system field vs OpenAI system message role. |
| 3.6 | Synchronous Chat Execution | `AiChat_complete` executing HTTP request and parsing response | 🟩 | Parses assistant response text view using `JsonDoc`. |
| 3.7 | Sisters Compatibility Test | `ai_chat_sisters_test` verifying Anthropic and Gemini payloads | 💚 | Verified passing headless unit test. |

---

## Subsystem 4: Incremental Server-Sent Events (SSE) Streaming (`ai/ai_sse`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 4.1 | Zero-Alloc SSE Chunk Parser | Incremental line-by-line `data:` and `event:` parser | 🟩 | Caller-fed buffer; zero memory allocations during token stream. |
| 4.2 | Token Delta Extraction | Extracts streaming token deltas across OpenAI/Anthropic chunk shapes | 🟩 | Parses `choices[0].delta.content` views. |
| 4.3 | Stream Completion Sentinel | Detects `data: [DONE]` and `event: message_stop` terminations | 🟩 | Clean end-of-stream signaling to UI consumers. |
| 4.4 | Headless SSE Conformance Test | `ai_sse_test` feeding synthetic multi-packet token chunks | 🟩 | Verified passing unit test. |
| 4.5 | Full SSE-to-Token UI Integration | Streams live token deltas directly into Darling `Label` / `TextPane` | ⬜ | Roadmap: hook SSE callbacks directly to interactive UI redraw ticks. |

---

## Subsystem 5: Asset Catalog & Legal-Sense Sourcing (`asset/*`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 5.1 | 12 Blessed Asset Sinks | Openverse, Poly Haven, AmbientCG, Freesound, Kenney, Wikimedia, NASA, etc. | 🟩 | Verified passing with 12 sources in `asset_test`. |
| 5.2 | Legal-Sense License Attributes | Explicit license tag on every row (CC0, CC-BY, Public Domain) | 🟩 | Enforces the Asset Sourcing Law: catalog verification instead of web scraping. |
| 5.3 | Asset Kind Classification | 3D models, textures/PBR, audio samples/SFX, vector icons, photos | 🟩 | Coarse categorization for engine asset browser. |
| 5.4 | Chunked Download Broker | `AssetBroker` downloading assets into `VexHome_cache` | 🟩 | 100ms per-chunk budget with cancel flag (the Bounded Wait Law). |
| 5.5 | Asset Search Seam | Searches public APIs of blessed asset providers | 🟩 | Formats search query URLs for Openverse, Freesound, Poly Haven. |
| 5.6 | Async Asset Ingestion Pipeline | End-to-end background download with progress percentage callbacks | ⬜ | Roadmap: background worker thread feeding `darling` asset cards. |

---

## Subsystem 6: Database Provider Catalog (`database/*`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 6.1 | 25 Database Provider Descriptors | SQL, NoSQL, Time-Series, and Cloud databases (`db_providers.inc`) | 💚 | Verified passing with 25 rows in `db_provider_test`. |
| 6.2 | Database Category Classification | Relational, Document, Key-Value, Graph, Columnar, Vector | 💚 | Type metadata matching `darkbase` driver categories. |
| 6.3 | Default Connection Templates | Connection URI templates (`postgres://`, `mariadb://`, `sqlite:`, etc.) | 💚 | Pre-fills DSN parameters for `darkbase` connection manager. |
| 6.4 | Catalog-Only SQLite Inspector | `DbSqliteFile` inspecting SQLite file headers without linking `sqlite3.h` | 🟩 | Reads 100-byte SQLite header (page size, change counter, schema version). |
| 6.5 | Generator Script | `gen_db_providers.py` generating C catalog tables | 💚 | Automated source table synchronization. |

---

## Subsystem 7: Developer App & Automation Broker (`app/*`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 7.1 | 29 Developer App Descriptors | IDEs, 3D suites, audio tools, container runtimes, terminals | 💚 | Catalog of external developer environments. |
| 7.2 | Probe Integration | Directly queries `vexspoke`'s `AppDetect` and `ProcessProbe` | 💚 | Verified passing in `probe_consumer_test`. |
| 7.3 | 16-Slot Bounded Action Seam | `AppBroker` managing automation actions with injected vtables | 💚 | Bounded execution slots without memory leaks. |
| 7.4 | CLI Launch Parameter Templates | Command-line arguments to open files/projects in target apps | 💚 | Formats CLI calls for `code <path>`, `cursor <path>`, `blender <path>`. |

---

## Subsystem 8: CLI Toolchain & Build Harness (`harness/*`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 8.1 | 20 CLI Engine Descriptors | Clang, GCC, Rustc, Go, Zig, Swift, Python, CMake, Ninja, Git, etc. | 💚 | Metadata describing compiler and build tool commands. |
| 8.2 | Toolchain Detection | Verifies presence and version via `AppDetect_which` | 💚 | Zero-subprocess path lookup. |
| 8.3 | 16-Slot Bounded Job Harness | `Harness` tracking running build and compile jobs | 💚 | Leverages `vexspoke`'s `ProcessSpawn` bounded table. |
| 8.4 | Non-Blocking Job Slices | `Harness_poll` reaping compiler output with 100ms budget | 💚 | Bounded non-blocking wait loops (the Bounded Wait Law). |

---

## Subsystem 9: Webhook Transmitters & Messaging (`com/*`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 9.1 | Discord Rich Embed Webhook | `Discord_sendEmbed` posting rich colored embeds | 💚 | Custom titles, descriptions, color hexes, and field arrays. |
| 9.2 | Discord File Attachment | Multipart/form-data boundary generation uploading logs and snapshots | 🟩 | Attaches crash dumps and scene screenshots directly to Discord. |
| 9.3 | Slack Webhook Transmitter | `Slack_sendText` posting JSON blocks to incoming webhook URLs | 🟩 | Simple JSON text payloads via REST core. |
| 9.4 | Webhook Loopback Test Suite | `webhook_loopback_test` verifying HTTP request wire serialization | 🟩 | Verifies JSON payloads and headers; network calls mockable. |
| 9.5 | Telegram Bot API Webhook | Bot API POST driver sending messages to chat IDs | 🟥 | Concept spec'd; pending wire serialization. |
| 9.6 | Matrix / Element Client-Server | Matrix `/rooms/{roomId}/send/m.room.message` transmitter | 🟥 | Concept spec'd for decentralized team telemetry. |
| 9.7 | Microsoft Teams Webhook | Connector Card JSON format poster | 🟥 | Concept spec'd for enterprise notifications. |

---

## Subsystem 10: REST Core, Authentication & WebSockets (`api/*`)

| # | Micro-Feature | Scope | Status | Notes |
|---|---------------|-------|--------|-------|
| 10.1 | REST Request Serialization + Status Classification | `Rest_postJson` and `Rest_get` over `vexspoke`'s `net/http` | 💚 | Direct socket exchange into caller-owned response buffers. Returns true only on a completed **2xx** transfer; a 1xx/3xx/4xx/5xx exchange returns false while `resp` keeps status/contentType/body for inspection. Proved by `../../../tests/api-haven/api/rest_test.c` over a loopback server (200/204/302/400/404/429/503/500, refused connection, auth fail-closed). |
| 10.2 | Unified `ApiAuth` Contract | `AUTH_NONE`, `AUTH_API_KEY`, `AUTH_BEARER`, `AUTH_BEARER_FN` | 💚 | Uniform header injection across all outbound HTTP requests. An explicitly required credential that cannot be rendered now fails **closed** (no request sent); a `nullptr`/NONE auth stays an intentional public request. |
| 10.3 | 16-Slot Callback Fanout | `HavenWsFanout` registry over opaque handles and caller-supplied callbacks | 🟨 | No socket adapter is implemented; this registry does not establish or manage WebSocket connections. |
| 10.4 | Engine Telemetry Sender | `APIClient_sendTelemetry` dispatching diagnostic reports | 🟩 | High-throughput telemetry emitter. |
| 10.5 | Bug Telemetry Endpoint | Diagnostic scene snapshot and crash reporter transport to VPS / Cloudflare | 🟥 | Crash report bundle uploader feeding `sesh`. |
| 10.6 | Icon Provider Catalog | Icon sets descriptor catalog (Lucide, Tabler, Material, Iconify API) | 🟩 | Catalog feeding vector baking in `darling-editor`. |

---

## Defect Log & Seam Status

- **Loopback Test in Sandbox**: `webhook_loopback_test` requires standard sandbox network socket bind permission; passes in unsandboxed/native environment.
- **TLS Seam**: `vexspoke/src/objc/tls_apple.m` implements a Network.framework client (bounded ~4s handshake) but is **not wired** into `Http_perform`, and `net/tls_curl.c` is a fail-closed `;;DRAFT` stub. `https://` therefore fails closed today; wiring a proven backend is the open HTTPS blocker.
- **Verified Green**: REST core now has its own loopback owner (`rest_test`) alongside `webhook_loopback_test`, `ai_provider_test`, `ai_chat_sisters_test`, `ai_sse_test`, `asset_test`, `db_provider_test`, `probe_consumer_test` and `mcp_server_test`.

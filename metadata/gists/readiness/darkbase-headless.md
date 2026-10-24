# darkbase-headless — R4 darkbase service

> **Architectural Tier:** R4 interface. The service owns database-file lifetime,
> identity, sessions, request admission and the transport seam; `darkbase-engine`
> remains the R3 store owner.
> **Current state:** an offline `HeadlessService` owns database startup/load, the
> one-time admin bootstrap, password + TOTP login, replay-step persistence, forced
> password replacement and explicit request admission. Its mirrored service owner
> passes on macOS arm64 through the workspace graph with strict C23 assertions.
> This is not network/session/CRUD/audit integration; Keychain, WAL-backed service
> mutation, service failure injection/sanitizers and other platforms remain unproved.
> The separate v1 wire codec now has registered framing and optimized/ASan/UBSan
> owner proof; it does not change the service-level gaps above or open any socket.

| Feature | Evidence and notes | Status |
| :--- | :--- | :--- |
| Service source and lifecycle | `../../../tests/darkbase-headless/service/service_test.c`: startup, DB ownership and restart; macOS arm64 only | 🟧 |
| Startup database load and request admission | Owner proves load, closed-on-restart gate and explicit persisted enable/disable; save-failure injection absent | 🟧 |
| Admin authentication and TOTP | Owner proves one-time bootstrap, password + TOTP, replay rejection and forced password change using a fake secret store; no OS Keychain proof | 🟧 |
| Versioned request/response envelope | `../../../tests/darkbase-headless/protocol/headless_protocol_test.c`, `protocol_run.py`: byte oracle, every split, tail retention, EOF/hostile headers, exact bound/refusal/recovery and redacted projections; strict optimized and ASan/UBSan macOS arm64. No transport or service dispatch | 🟨 |
| Network transport and connection dispatch | No socket/TLS/host pump, partial-send adapter, deadlines or connection authentication; codec accepts bytes only | 🟥 |
| Authenticated CRUD and entity-scoped authorization | No request protocol or execution implementation | 🟥 |
| CRUD triggers and durable audit | Engine WAL exists, but Headless mutation integration and audit are not implemented | 🟥 |
| Build registration | `setup_darkbase_headless` discovers the service and owner; `./tools/b test service_test` passes | 🟩 |

## Scope and Limitations

Headless is the R4 service boundary and the only intended database-file opener.
It must not implement storage, paging or WAL, and clients must never open the
database file. Current owner evidence is a single offline macOS arm64 service
test with a fake in-memory secret store; it is not Keychain, network, CRUD, visual,
service-sanitizer, or other-platform proof. Separate protocol owners prove byte
framing and codec memory safety within their scope, not network execution. The fixed bootstrap credential is used for one-time
setup, with a password change before enabling requests; TOTP is required for
administration. The current replay/gate records still use the legacy flat snapshot.
The required durable audit must use the engine's WAL-backed mutation boundary.

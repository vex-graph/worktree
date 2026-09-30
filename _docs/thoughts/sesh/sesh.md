# sesh (Multiplayer Canvas, VPS Relay & In-Engine Bug Ingestion)

**Idea (in vexgraph's words):** session management, remote multi-user collaboration for notes and whiteboards, VPS hosting, bug catching/reporting, and using Cloudflare edge bypassing/tunnels.

## Shape
- **Multiplayer State Sync**: Real-time cursor broadcasting and canvas delta sync over `HavenWsFanout` (16-slot bounded fan-out).
- **In-Engine Bug Catcher & Reporter**: When an exception, assertion, or GPU error triggers, the engine captures a full diagnostic snapshot (active memory arena stats, backtrace, and serialized scene state) and posts it to a developer-controlled VPS endpoint.
- **Cloudflare Edge Ingress**: Secure ingress via Cloudflare Tunnels (no open public firewall ports) and Turnstile bot protection for public demo pairing.

## Status
Envisioned. `../../projects/sesh` initialized.

## Next step
Draft the session packet schema (`{session_id, user_id, op_type, payload}`) and the VPS HTTP/WS listener.

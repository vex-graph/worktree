# harness — The User's Own Agent (R4 interface)

> **Draft; no runtime exists yet.** R4 interface that consumes [api-haven](#file-api-haven-md)
> connectors **as-is**, borrows [relational-engine](#file-relational-engine-md) memory/IO and
> [vexspoke](#file-vexspoke-md) CPU/behavior, and composes [darling](#file-darling-md) for
> interface. The draft `src/space/` value pairs are tracked source but have **no behavioral
> owner test, no runtime build target and no proven platform**. No connector, session, GPU
> or OS implementation is owned here, and it is never included by R1/R2/R3. Repository:
> `vexgraph-ecosystem/harness`.

> **Architectural Tier**: R4 Interface (the user's own agent, integrated with this ecosystem).
> **Production Standard**: *The Integrated Own Agent: Model/Prompt/Conversation/Answer core + Tool registry + own MCP surface, driving the user's projects, bounded tools (`func`/`b`) and R5 applications through registered seams*.
> **Governing Laws**:
> 1. **Harness Host Boundary Law**: consumes api-haven connector and `harness_run`/`harness_poll` seams unchanged (opaque handles + fn-tables); never a parallel connector, transport, GPU or OS implementation (the Vertical Integration Law).
> 2. **Agent Integration Law**: every external tool is a bounded child (the Bounded Wait Law); orchestration compiles through `func`, never a shipped interpreter; cold input rejects loudly (the THROW Law); `func`/`b` are tools, not includes.

---

| Feature | Scope | Status | Notes |
| :--- | :--- | :--- | :--- |
| Space draft values | `src/space/` `support.h` + ModelUser/Channel/Message/Task pairs; owners `tests/harness/space/*_test.c` + arity battery via `python3 tests/harness/run.py` and `./tools/b test <unit>` | 🟨 | Tracked C23 source with strict + ASan/UBSan behavioral owners: 0..8 arity counter/chooser, 23+1 handle extent, bounded projections and byte-span escaping, construction boundaries, embedded-NUL borrowed spans, task lifecycle/enumeration and permission-narrowed delegation, reject-and-preserve on every invalid path. Still a draft: no runtime build target, provider/server/UI integration or proven platform. |
| Model / Prompt / Conversation / Answer | Planned agent core | ⬜ | Specified only; no implementation. |
| Tool / ToolRegistry | Planned built-ins + `func` + MCP | ⬜ | Specified only; `func` is a bounded child tool, never an embed. |
| HarnessMcp | Agent's own MCP surface over api-haven contracts | ⬜ | Specified only; names prefixed so they do not collide with api-haven's `McpServer`. |
| Harness host | Model + Tools + Conversation + interface | ⬜ | Specified only; no runtime build target. |
| Runtime platforms | — | ⬜ | None proven. Workspace IDE code-model checks are not agent execution or IDE appearance. |

---

## Notes

- The two repo-local laws above are forward contracts with nothing bound yet.
- The `space` values are behaviorally owned offline (strict + ASan/UBSan) but remain a draft slice; message text stays borrowed, not durable history.
- Tests live in the shared `../../../tests/harness` partition (the Test Tree Mirror Law), wired through `setup_harness` in the umbrella graph.

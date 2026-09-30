# How api-haven Works: Phonebook + Thin Talkers, Zero Exec

> 2am README for the R2 connector repo. If you forgot everything, read
> section 1 and 2 and go back to sleep. If it's 2pm and you're adding a
> feature, read the how-tos at the bottom.
> Answers the fundamental question: **"Where does the running happen?"**
> Answer: **not here.**

---

## 1. The Short Answer: We Own the Menu, Not the Kitchen

api-haven is a **phonebook with thin talkers**. It knows *what exists*
(260 AI providers, 25 databases, 20 coding engines, 29 apps), *how to
reach each one* (URL, CLI name, bundle id), and *how to ask* (REST,
JSON-RPC, MCP envelopes) — but it never *does the doing*. No `popen`,
no threads, no SDKs, no `osascript` inside this repo. Execution lives
behind injected driver tables implemented in vexspoke (R1) or the R3
app, and until somebody binds one the tools answer `UNBOUND_DRIVER`
instead of spawning. That sentence is the whole architecture.

| Piece | What it is | Count | Role |
|---|---|---|---|
| `AiProvider` | descriptor table | 260 rows | AI vendors: slug, base URL, auth |
| `DbProvider` | descriptor table | 25 rows | data sources: engine, port, family |
| `EngineProvider` + `Harness` | table + 16 job slots | 20 engines | CLI agents: spawn via driver, poll by job-id |
| `AppProvider` + `AppBroker` | table + 16 action slots | 29 apps | Apple/local/bot targets: bounded actions |
| `SearchProvider` | descriptor table | 3 backends | blessed search APIs: searxng, google-cse, wikimedia |
| `Rest` / `ApiAuth` / `APIClient` | thin talkers | — | HTTPS + credentials (never in the arena) |
| `Discord` / `Slack` | webhook drivers | — | embeds + multipart over `Rest` |
| `McpServer` | stdio JSON-RPC engine | 12 tools + 6 resources | exposes everything above to agents |
| `Json` flex (vexspoke `net/json`) | `Json_path` + `JsonWriter` | — | `_.get` + `JSON.stringify` in C, zero-alloc |

---

## 2. Where It Sits (Read This Once)

Per `../../preferences.md` Rule 17 the stack has ONE order:

```text
R0 hotcwap  → boots first, owns Kernel/Window, tears down last
R1 vexspoke → arenas, net/http, threads, system probes (AppDetect, …)
R1.5 graphvex → GPU only
R2 api-haven / darling → features. WE ARE HERE. Hot-reloads via HotModule.
R3 engines/apps → your IDE, your game, other CLIs registering here
```

Compile rule: api-haven includes **vexspoke only** (`net/*`, `nio/mem.h`,
`system/*` probes — consumed, never re-implemented). No graphics, no
`darling`, no vendor SDKs. If a new file wants any other `#include`,
the design is wrong, not the rule. Runtime rule: MCP hosts **handler
closures over tables** — list/poll read, run/action enqueue bounded
async work and answer a job-id. Nothing on the stdio thread ever blocks.

---

## 3. The Three Laws of the Seam (2am Rules)

**Law 1 — No exec here.** If you want `claude`, `osascript`,
`shortcuts`, or a socket dial, you add a *row describing it* plus a
driver *elsewhere*. `grep -rn "popen\|system(\|fork\|exec" src/` must
stay empty. The one exception-shaped hole is the driver table
(`HarnessDriverTable{spawn/poll/cancel}`, `AppDriverTable{runActionFn}`)
— opaque `void*` + fn pointers, implemented outside.

**Law 2 — Slots, never threads.** Every job gets one of 16 fixed slots
(BitPool discipline, like vexspoke memory). 17th concurrent job gets
`BUSY_FULL`, not a 17th thread. Slots are reused (IDLE/DONE/TIMEOUT).
Teardown joins ≤16 things in bounded time (Rules 26/27) — that's why
the window never ghosts.

**Law 3 — Timeouts on everything, `UNBOUND_DRIVER` until bound.**
Every wait takes `timeoutMs` and degrades (drop frame, mark TIMEOUT).
No driver bound (standalone `mcp_server` binary) → tools resolve the
slug and say `UNBOUND_DRIVER … nothing spawned` as `isError`. An R3
host calls `McpServer_bindHarnessDriver` / `McpServer_bindAppDriver`
before serving and the same tools go live. Apple-only rows
(Notes/Music/Shortcuts/osascript) additionally gate on presence:
no Mac / no helper → `UNAVAILABLE`, never a crash.

---

## 4. Data Flows (The Three Shapes)

**List (sync, read-only):**
`tools/call engine_list` → table scan → text lines → done. Same for
`app_list`, `ai_provider_lookup`, `db_data_source_lookup`.

**Run (async, bounded):**
`tools/call harness_run{engine,prompt,timeoutMs?}` → resolve slug →
`Harness_run` takes a free slot → driver `spawnFn` (vexspoke worker) →
answer `job 3 RUNNING … poll with harness_poll` *immediately*.
Client polls: `tools/call harness_poll{jobId}` → `job 3: DONE …`.
`app_action` is the same shape over `AppBroker` (output text rides
along: `job 1 DONE … outLen=12` + raw bytes; envelope escaping happens
at the MCP layer).

**Resources:** `engines://catalog` and `apps://catalog` render the same
bodies as the bare list calls. `system://apps`, `system://capture`,
`db://data-sources` predate them.

---

## 5. How-Tos (2pm Section)

**Add an engine** (3 lines in `src/harness/engine_provider.c`, then fix
the two count comments + overview): one `{"slug","Name","cli",
FAMILY, AUTH, "note"}` row. Families: CLI / LOCAL / REMOTE. Auth:
NONE / API_KEY / OAUTH / SYSTEM.

**Add an app** (same, in `src/app/app_provider.c`): families OSA_SCRIPT
/ SHORTCUTS_CLI / MUSIC_LOCAL / REST_WEBHOOK / LOCAL_SOCKET /
NATIVE_CLI (`python3 --version`-style probes). Tokens always via
`ApiAuth`, never the arena, never the repo.

**Add an MCP tool:** renderer fn + row in `kMcpTools` (+ resource twin
if it dumps a catalog). Lists read tables; runners enqueue into the
seam statics and never block. Update `src/mcp/tests/mcp_server_test.c`
same-commit (substring asserts, `check(strstr…)` style).

**JSON without pain** (vexspoke, upstream-first): read with
`Json_path(doc, root, "params.engine")`, defaults via
`Json_getBool/Number/String(ref, def)`, build replies with `JsonWriter`
(`beginObject → addKey → stringVal/numberVal/… → endObject`). Trap:
reader key-fn is `Json_key`, builder key-fn is `Json_addKey` (name was
taken). Overflow flips `ok` once; later calls no-op.

**Run the scratch tests** (never committed — `_test/` is gitignored):
```sh
cc -std=gnu23 -Wall -Wextra -Werror -I projects/api-haven/src \
  -I projects/vexspoke/src _test/harness_run_test.c \
  projects/api-haven/src/harness/engine_provider.c \
  projects/api-haven/src/harness/harness.c -o /tmp/harness_run_test
# same shape for app_broker_test, json_flex_test (vexspoke-only)
```
Protocol test builds like CMake does (lib flags `-Werror`, test file
without it — the `r` var pattern warns otherwise), linked against
`mcp_server + harness + app + ai + db + json + app_detect +
capture_tool + process_probe`.

**Commits:** inside `../../projects/api-haven` (its own repo), one class per
commit (`feat(harness): …`, `feat(app): …`), upstream-first
`vexspoke → graphvex → hotcwap → darling → api-haven → vexgraph`.
Vexspoke edits (e.g. `net/json`) commit inside `../../projects/vexspoke`.
Never push unless asked. `git status` must show lib sources only —
no `_test/`, no scratch.

---

## 6. Borrowed Brains (MIT Hygiene)

Hermes Agent (NousResearch, MIT) is our interop reference for the
messaging gateway shape (Telegram/Discord/Slack/WhatsApp/Signal/SMS/
Email/Matrix/… — see `_docs/hermes_text.md`). Rule: docs are reference,
rows are ours. No Hermes code vendored; one `;;INTENTION` line per
borrowing file says so. Facts about public APIs aren't anyone's IP;
our wording is our own. Same deal for any future reference.

## 6.5. Search Is Not Scraping (Basic Computer Science)

Calling a documented search API and parsing its documented JSON is a
client using a contract: request schema in, response schema out,
credentials where the contract says. That's a function call over a
socket. Scraping is the reverse: fetching human HTML meant for browsers
and reverse-engineering it into a fake API — selectors as schema,
layout as versioning, ToS bypass as auth. That's screen-reading someone
else's UI and pretending it's an interface. Rule 34 bans the second;
`SearchProvider` rows are all the first (Google CSE JSON API,
self-hosted SearXNG, MediaWiki API). Fetching a page the user pointed
at and reading its text is also the first — extraction, not scraping.

## 7. What's Next / Parked

* **Next:** vexspoke bounded-spawn primitive (the driver kitchen) —
  upstream Tier-1 commit, then bind + first live end-to-end.
* **Parked for semicolon IDE + `_thoughts/`:** skills system, memory
  providers, cron/scheduler, delegation/kanban, browser/voice/media.
  They get their own tables + brokers when they graduate — not rows
  in this repo's tables.
* **Gotchas file:** stdio loop is single-threaded (renderer `static`
  prompt/params buffers are fine *because* of that — don't thread it
  later without removing them); `handleLine` pools are 256 nodes /
  64KiB scratch (prompts past ~32KiB truncate); `mcp_server` answers
  `UNBOUND_DRIVER` standalone by design.

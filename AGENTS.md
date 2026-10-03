# Agent harness — this workspace

Minimal core, opt-in everything else. Six capabilities, nothing more by default:
**read · write · edit · bash · web search · agents**.

## Authoring

- **If your session exposes `write` / `edit`, use them** for every source
  change — never generate files by running a script. That is the preferred
  path, and the one this workspace is built around.
- **If it does not** (some model routes expose only `read` / `shell` /
  `websearch`), the command tool is your fallback: use `python`, `sed`, or
  heredocs to read and, when you must, to write files. You are not blocked —
  just note it in your report/commit, because the session lacked the direct
  tools.
- Use `bash` for build/test/git and read-only inspection. Prefer the umbrella
  build (`./tools/b`) over inventing commands.
- Keep changes small and cohesive; cite laws by Title, never number
  (`preferences.md` is the constitution). Never push without an explicit,
  one-off order (the Git Workflow Law).

## Talking to other agents

`tools/agents.sh` is the bus — sibling sessions in this workspace, over the
OpenCode session API:

```
agents.sh whoami                 this session
agents.sh name [<name>]          show, or set, this session's handle
agents.sh peers | running        who else is here
agents.sh tell "<msg>"           announce to every other running session
agents.sh say <id|title> "<msg>" message one session
agents.sh inbox [id]             read a session's inbox
agents.sh log  [id] [n]          read a session's last n messages
agents.sh bus  "<msg>" | bus     durable shared note (read it too)
```

Protocol:

1. **Announce before broad or shared work** — `tell` (live) and/or `bus` (durable).
2. **Check first** — `peers` + `bus` before editing a path another session may
   own; two agents writing one file is the failure mode this exists to stop.
3. **Prefer the bus for scope, `say` for a specific hand-off.** A `say` lands as
   a user turn in the target session and may interrupt it — keep it short and
   actionable.
4. **Never message yourself** — `tell` already excludes `$OPENCODE_SESSION_ID`.
5. **Every `say`/`tell`/`bus` note is signed** `— <name> (agent <shortid>)`, so a
   recipient can tell an agent's note from a human's — a human typing straight
   into a session leaves no such line. Name it yourself with
   `agents.sh name <name>` (or `AGENTS_NAME`); otherwise it is derived from the
   session title. `AGENTS_RAW=1` sends unsigned.
6. **Reply to the sender, then summarize to the user.** A turn signed
   `— <name> (agent <shortid>)` is a sibling agent's message, not the human's.
   Respond to that agent with `tools/agents.sh say <id|title> "<reply>"` first;
   use `peers` to resolve the sender if needed. Do not substitute a user-facing
   answer for the actual `say` delivery. Then give the human a brief summary
   referring to the other agent in the third person, for example:
   “Done—I told them the migration is complete and they can coordinate the
   next checklist update.” Do not address the human as though they were the
   sibling or paste the whole agent reply. Only say it was sent after the
   command succeeds; otherwise report the delivery failure. A terminal
   acknowledgement with no new question or action needs no further `say`
   reply, avoiding endless acknowledgement loops.

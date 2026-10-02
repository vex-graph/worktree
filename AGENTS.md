# Agent harness — this workspace

Minimal core, opt-in everything else. Six capabilities, nothing more by default:
**read · write · edit · bash · web search · agents**.

## Authoring

- Write and change source with `write` / `edit`. Do **not** generate code by
  running a script (no `python`, `sed`, heredocs, or template loops that emit
  source). Scripts are for tooling and inspection, never for authoring files.
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

import { Plugin } from "@opencode/plugin"
import { access, readFile } from "node:fs/promises"
import { dirname, join } from "node:path"

// vexgraph.agent-bus
//
// Two jobs, both invisible when they work:
//   1. Hold the model to the minimal tool surface for every request.
//   2. Keep every session aware of its siblings by delivering unread bus notes
//      (tools/agents.sh writes them) into the system prompt exactly once.
//
// The bus itself needs no tool: it rides on the command tool running
// tools/agents.sh. OpenCode registers the command tool as `shell`, and Code
// Mode's `execute` must survive or nothing can be invoked at all.
const ALLOWED_TOOLS = new Set(["read", "write", "edit", "shell", "bash", "websearch", "execute"])

const BUS = join("_notes", "agents", "bus.md")

// The workspace root is whichever ancestor owns tools/agents.sh. The server may
// load this plugin from a different location than the session's directory, so
// never assume ctx.location.directory is the workspace.
async function workspaceRoot(start: string): Promise<string> {
  let dir = start
  for (;;) {
    try {
      await access(join(dir, "tools", "agents.sh"))
      return dir
    } catch {
      const parent = dirname(dir)
      if (parent === dir || parent === "") return start
      dir = parent
    }
  }
}

const REMINDER =
  "Harness (minimal): use read/write/edit/bash/websearch only. Write source " +
  "with write/edit — never emit files by running a script. Before editing a " +
  "path a sibling may own, check `tools/agents.sh peers` and `tools/agents.sh " +
  'bus`; announce scope with `tools/agents.sh tell "…"`.'

type AnyRecord = Record<string, unknown>

export default Plugin.define({
  id: "vexgraph.agent-bus",
  async setup(ctx) {
    const busPath = join(await workspaceRoot(ctx.location.directory), BUS)

    await ctx.session.hook("context", async (event) => {
      const e = event as unknown as AnyRecord

      // 1. Enforce the minimal tool surface for this model call.
      const tools = e.tools as AnyRecord | undefined
      if (tools && typeof tools === "object") {
        for (const name of Object.keys(tools)) {
          if (!ALLOWED_TOOLS.has(name)) delete tools[name]
        }
      }

      // 2. Deliver unread bus notes to this session, once.
      let unread = ""
      try {
        const raw = await readFile(busPath, "utf8")
        const lines = raw.split("\n").filter((line) => line.trim() !== "")
        const key = `bus/${(e.sessionID as string | undefined) ?? "unknown"}`
        const seen = ((await ctx.storage.get(key)) as number | undefined) ?? 0
        if (lines.length > seen) unread = lines.slice(seen).join("\n")
        await ctx.storage.set(key, lines.length)
      } catch {
        // no bus yet — nothing to deliver
      }

      // 3. Keep the reminder (and any fresh notes) in front of the model.
      const system = e.system as Array<{ type: string; text: string }> | undefined
      if (Array.isArray(system)) {
        system.push({
          type: "text",
          text: unread ? `${REMINDER}\n\n<agent-bus>\n${unread}\n</agent-bus>` : REMINDER,
        })
      }
    })
  },
})

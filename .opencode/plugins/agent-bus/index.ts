import { access, readFile } from "node:fs/promises"
import { dirname, join } from "node:path"

// vexgraph.agent-bus
//
// One job: deliver unread bus notes (tools/agents.sh writes them) into every
// session's system prompt, once.
//
// It deliberately does NOT touch the tool set. Filtering tools by name broke
// sibling sessions whose provider names them differently — a session could lose
// write/edit because "write" wasn't the name this list used. The minimal
// surface is a convention (AGENTS.md), not a deletion.

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
  "Harness: if this session exposes write/edit, author source with them. If it " +
  "does not (some routes expose only read/shell/websearch), the command tool " +
  "(python/sed) is the fallback — you are not blocked, just say so. Announce " +
  "scope with `tools/agents.sh tell \"…\"` and check `tools/agents.sh bus`/`peers` " +
  "before editing a path a sibling may own."

type AnyRecord = Record<string, unknown>

// The slice of the plugin context this uses. The published helper's define() is
// an identity wrapper (return plugin), so a dependency-free default export of
// { id, setup } is accepted directly — no node_modules to resolve.
type Ctx = {
  location: { directory: string }
  session: { hook: (name: string, fn: (event: unknown) => unknown) => Promise<unknown> }
  storage: {
    get: (key: string) => Promise<unknown>
    set: (key: string, value: unknown) => Promise<void>
  }
}

export default {
  id: "vexgraph.agent-bus",
  async setup(ctx: Ctx) {
    const busPath = join(await workspaceRoot(ctx.location.directory), BUS)

    await ctx.session.hook("context", async (event) => {
      const e = event as unknown as AnyRecord

      // Deliver unread bus notes to this session, once.
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

      const system = e.system as Array<{ type: string; text: string }> | undefined
      if (Array.isArray(system)) {
        system.push({
          type: "text",
          text: unread ? `${REMINDER}\n\n<agent-bus>\n${unread}\n</agent-bus>` : REMINDER,
        })
      }
    })
  },
}

# Vexgraph — Universal Architecture Preferences

This is the **universal constitution** of the vexgraph ecosystem: the author's own
architectural preferences, maintained live and updated whenever the architecture
changes. It is not an AI system prompt and not a style guide for "vibe coding" —
it is the contract the code must satisfy so the system does not collapse as it
grows: memory layout, ownership, tiering, validation, teardown, security,
documentation, and proof. Every rule here exists because a real failure mode
forced it.

It governs every repository (R1–R6). Repo-local lawbooks
(`*-preferences.md` at each repo root) add only what is exclusive to that repo;
the universal rules here always win on conflict (Tier Map).

## How to read

- `gist.md` — the compressed form of the whole constitution. Shape: `##` is a
  law title, `###` is one sub-section of that law (numbered `LAW.N` so the list
  reads cleanly), and each bullet under it is one atomic clause of the rule.
  Greppable: `grep '^## '` lists the laws, `grep '^### '` lists the sub-sections.
- `overview-template.c` — worked example of a self-contained source file, the
  `;;DEFINITION` + `;;OVERVIEW` blueprint every `.c` carries (Living
  Documentation Law).
- `main-template.c` — worked example of the application entry shape: one
  `create<Object>()` helper per owned object (custom UI and algorithms composed
  from lower tiers), then wire, start, end, `return 0` (Vertical Integration
  Law, Compose down, never rebuild).
- `/PREFERENCES.md` (root, Git-ignored) — the complete monolithic source,
  rationale included; published as `preferences-full-documentation.md`. It is
  reference documentation, not something an agent reads whole: grep the law
  number or title, then print that range.
- `./tools/prefs` — the command that does that reading for a session: `list`,
  `law N`, `section N.M`, `find`, `repo`, `test`, and `check`, always fresh,
  always just the law you asked for. `gist.md` and the full documentation carry
  the same law titles, so a title is the safe way to ask.

The block an agent receives on every request is `./tools/prefs prompt`: this
compressed constitution whole, plus a title index of the proof lawbook and of
every repository lawbook. The bodies are not sent; the agent reads the one it
needs with the command. That is why the per-request cost is ~15 KB instead of the
~220 KB of every lawbook at once, and why the index never goes stale.

This introduction is for humans. Agents read `gist.md`; it tells them everything
they need to grep, and the full text stays one read away.

## How it stays live

`gist.md` and this document sit beside `/PREFERENCES.md` and are updated with it.
When the constitution changes, update both and republish the Gist in the same
cycle (Canonical File & Gist Publication). Nothing here is cached or stale: if a
law changes, the next request reads the new text.

## Citation

Cite laws by **Title** (and clause name in parentheses), never by number
(Law Identity Doctrine). Example: `Semantic Consistency Law (Access depth)`.

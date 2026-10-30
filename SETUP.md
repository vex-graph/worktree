# SETUP.md — The Entry Point

Everything in this workspace has one shape: **setup → preferences → the preferences
inside the preferences.** Three rings, each pointing to the next. This file is the
outermost ring — the map. It is not law; it is the reading order.

## The three rings

- **Ring 0 — this file.** The map you are reading. No rules are stated here; it only
  says where the doors are and in what order to open them.
- **Ring 1 — the universal constitution, in two forms.** `metadata/gists/preferences/gist.md`
  is the compressed form: every law as titled sub-sections whose bullets are the
  clauses. It is small enough to carry whole and is what the plugin injects on every
  request. `metadata/gists/preferences/PREFERENCES.md` (workspace root) is the full documentation — rationale,
  examples, prose — and is **reference material only**: never read it whole, ask
  `./tools/prefs` for the one law you need. `metadata/gists/preferences/PREFERENCES.md` is the single source of
  truth; `metadata/gists/preferences.md` is a symlink to it, never edited, always
  the root file. `metadata/gists/preferences/PREFERENCES.md` is published as
  `preferences-full-documentation.md` in the Gist.
- **Ring 2 — the repo preferences, which live *inside* the preference system.**
  The constitution's reading table (`metadata/gists/preferences/PREFERENCES.md`, the Per-Repo Preferences
  Extension Law section) is the canonical link list: one `<repo>-preferences.md`
  lawbook per repository, sitting at its own repo root. The rule of Ring 2 is that
  the constitution governs everywhere, and the owning lawbook adds what is
  exclusive to that repo. Universal first, local second — never local instead.

## The reading order

1. **First session in this workspace:** read the compressed `gist.md` — it arrives
   injected — then `./tools/prefs list` to see the law map. Depth is on demand:
   `./tools/prefs law 6`, `./tools/prefs section 6.4`, `./tools/prefs find "…"`.
   Opening all 738 lines of `metadata/gists/preferences/PREFERENCES.md` spends context on laws that are not
   in play and is not the reading order.
2. **Before working in a repository:** read *that* repo's lawbook next
   (`./tools/prefs repo <name>`) — it is mandatory chained reading, not optional
   background. The injected block lists the lawbooks; it does not carry them.
3. **Before touching tests or proof:** read the owning law out of
   `tests/test-preferences.md` (`./tools/prefs test "<law>"`) — the injected block
   carries its title index, not its body — then check the current
   `metadata/gists/test-checklist.md`: consult the ledger, never trust a
   remembered green result.

## Where the files are

| Thing | Path |
| :-- | :-- |
| Constitution (compressed, injected) | `metadata/gists/preferences/gist.md` |
| Constitution (full documentation, reference) | `metadata/gists/preferences/PREFERENCES.md` (workspace root, Git-ignored) |
| Constitution (human intro) | `metadata/gists/preferences/_introduction.md` |
| Worked blueprint examples | `metadata/gists/preferences/overview-template.c`, `main-template.c` |
| The law query command | `./tools/prefs` |
| Proof lawbook | `tests/test-preferences.md` |
| Evidence ledger | `metadata/gists/test-checklist.md` |
| Repo lawbooks | each repo root, e.g. `suite/vexspoke` |
| Personal tool lawbooks | `suite/func`, `suite/primeagen` |
| The loader | `.opencode/plugins/preferences/index.ts` |

(The engine lawbook is at
`suite/relational-engine`.)

## Reading one law

`./tools/prefs` reads the files fresh on every call; nothing is cached, indexed or
generated. It never prints a law you did not ask for.

    ./tools/prefs list              law map: number and title
    ./tools/prefs law 6             compressed law 6, every sub-section
    ./tools/prefs law 6 --full      the same law in the full documentation
    ./tools/prefs section 6.3       one compressed sub-section
    ./tools/prefs section 6.4 --full
    ./tools/prefs find "compose"    matching lines with their law/section
    ./tools/prefs repo vexspoke     the owning repo lawbook (complete)
    ./tools/prefs repo vexspoke "pointer"  one law out of that lawbook, by title
    ./tools/prefs repos             every repo lawbook in the tree
    ./tools/prefs test              proof lawbook map: every law title
    ./tools/prefs test "two-dylib swap"    one proof law, by title
    ./tools/prefs prompt            the exact block injected every request
    ./tools/prefs check             shape consistency + injected size
    ./tools/prefs files             the five published files, local -> Gist name
    ./tools/prefs publish [file...] publish to the Gist, then verify each file
    ./tools/prefs verify            download from the Gist and compare bytes

Numbers are slice addresses inside their own file, never identity: the compressed
form splits the same content into more sub-sections than the full documentation, so
`6.3` names different clauses in each. Cite a law by its **Title** — the Law
Identity Doctrine — and use a number only to find it.

## How it loads in a session

The preferences plugin injects this map once on the first agent-loop context
request in each OpenCode session. On every request it runs `./tools/prefs prompt`
and prepends the block that command returns: the whole compressed constitution,
plus a **title index** of the proof lawbook and of every `*-preferences.md` in the
tree (each lawbook by path and its own title). The bodies are not injected — they
stay on disk and are read with `prefs repo`, `prefs test`, `prefs law`. That is
the difference between ~15 KB and ~220 KB on every request; `prefs check` fails if
the block outgrows its 32 KB ceiling. The full documentation is never injected.
Nothing is cached or stale — if a file changes, the next request reads the new
text. The plugin README and `AGENTS.md` carry the operational notes; when the load
structure changes, update those in the same cycle (the Living Documentation Law).

## Publishing the working view

`metadata/gists/preferences/` is maintained by hand (Living Documentation Law).
When any of the five files change, publish and verify in one command:

    ./tools/prefs publish            # all five
    ./tools/prefs publish gist.md    # or just one
    ./tools/prefs verify             # compare every published file to the Gist

`publish` runs the `gh gist edit … --filename <remote> <local>` form (remote name
first, local path second), then downloads each raw file and compares bytes; a
mismatched upload is a failed publication, not a done one, and the command exits
nonzero. `check` additionally proves the local files are shaped correctly and end
with a newline, which is what makes the byte comparison honest.

A fresh clone fetches `metadata/gists/preferences/` from the linked Gist first.

## House rules for this file

- Cite laws by their Title, never by number (the Law Identity Doctrine).
- This map sits under the Living Documentation Law: when a path or ring moves,
  update this file in the same cycle.
- No rules or paths are invented here that the canonical sources do not state.

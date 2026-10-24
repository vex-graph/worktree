# metadata/gists/preferences/ — working view of the universal constitution

- `_introduction.md` — for humans: what this is, how to read, how it stays live.
  Agents do not read it.
- `gist.md` — for agents: the whole preference compressed. Shape: `##` = law
  title, `###` = law sub-section numbered `LAW.N`, `*` = one atomic clause of
  that sub-section. Greppable: `grep '^## '` lists laws, `grep '^### '` lists
  sub-sections.
- `overview-template.c` — worked example of a self-contained `.c` blueprint
  (`;;DEFINITION` + `;;OVERVIEW`), per the Living Documentation Law.
- `main-template.c` — worked example of an application entry: one
  `create<Object>()` per owned object (the bespoke UI/algorithm layer), then
  wire → start → end → return `0`.

Read one law, never the whole document: `./tools/prefs list` is the law map, then
`./tools/prefs law 6`, `./tools/prefs section 6.4`, `./tools/prefs find "compose"`,
`./tools/prefs repo vexspoke`. The command reads the files fresh on every call and
prints only what was asked for.

The plugin injects `./tools/prefs prompt` on every request: `gist.md` whole, plus
a title index of `tests/test-preferences.md` and of every repo lawbook. Bodies are
read on demand (`prefs repo`, `prefs test`); `prefs check` fails if the block
outgrows 32 KB.

Full text + rationale: `/PREFERENCES.md` (root, Git-ignored), published as
`preferences-full-documentation.md` in the Gist. It is reference only — ask the
command for one law; never ingest the whole file. Numbers are slice addresses
inside their own file: the compressed form splits the same content into more
sub-sections than the full documentation, so ask by Title when it matters.
Update `gist.md` when the constitution changes (Living Documentation Law).

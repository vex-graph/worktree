# vexgraph — local-only superbuild workspace

> **LOCAL ONLY. Do not push this repository.**
> It has no remote by design. Each `ecosystem/*` directory is its own
> independent checkout with its own git repo and GitHub remote —
> commit and push there, never here.

## Workspace map

Listed in R order (R1 → R2 → R3 → R4 → R5);

| Path | What it is | Pushed? |
|---|---|---|
| `ecosystem/hotcwap` | R1 kernel host, hotloading, windows · `hotcwap-preferences.md` | yes → `vexgraph-ecosystem/hotcwap` |
| `ecosystem/vexspoke` | R2 behavior core (relational C23 runtime) · `vexspoke-preferences.md` + `preferences.md` | yes → `vexgraph-ecosystem/vexspoke` |
| `ecosystem/graphvex` | R3 GPU driver (Vulkan/WGPU compute, SPIR-V, fonts) · `graphvex-preferences.md` | yes → `vexgraph-ecosystem/graphvex` |
| `ecosystem/api-haven` | R3 API/connector surface (MCP, AI, DB, asset) · `api-haven-preferences.md` | yes → `vexgraph-ecosystem/api-haven` |
| `ecosystem/language` | R3 language grammars (hot-swappable dylibs) · `language-preferences.md` | yes → `vexgraph-ecosystem/language` |
| `ecosystem/darkbase` | R3 database driver (native vex store) · `darkbase-preferences.md` | yes → `vexgraph-ecosystem/darkbase` |
| `ecosystem/darling-framework` (`projects/darling` → symlink) | R4 UI toolkit & compositor · `darling-framework-preferences.md` | yes → `vexgraph-ecosystem/darling-framework` |
| `ecosystem/sesh` | R4 session sync / VPS relay · `sesh-preferences.md` | yes → `vexgraph-ecosystem/sesh` |
| `ecosystem/samplerate` | R4 audio engine / R5 DAW · `samplerate-preferences.md` | yes → `vexgraph-ecosystem/samplerate` |
| `projects/semicolon` | R5 mini IDE | yes → `vexgraph-ecosystem/semicolon` |
| `ecosystem/darling-editor` | R5 spatial studio | yes → `vexgraph-ecosystem/darling` |
| `projects/drawling` | R5 drawing studio | yes → `vexgraph-ecosystem/drawling` |
| `projects/anti` | R5 3D game engine (the name lives here and only here) | yes → `vexgraph-ecosystem/anti` |
| `.ecosystem` | Ecosystem meta / orchestration root | yes → [`vexgraph-ecosystem/ecosystem`](https://github.com/vexgraph-ecosystem/ecosystem) |
| `.github` | Organization profile & global workflow templates | yes → [`vexgraph-ecosystem/.github`](https://github.com/vexgraph-ecosystem/.github) |
| `.vexgraph-dev` | Developer portal & tooling | yes → [`vexgraph-dev/vexgraph-dev`](https://github.com/vexgraph-dev/vexgraph-dev) |
| `_main/`, `CMakeLists.txt`, `*.sh` | Umbrella build + demo harness (this workspace only) | **no — local** |
| `_docs/`, `_lessons/`, `_thoughts/`, `_bugs/`, `_test/`, `_legacy-java/`, `_checklist/` | Personal notes, teaching material, snapshots | **no — local** |

## Read before doing anything

The workspace is governed by a constitution:

- **`preferences.md`** (→ `ecosystem/vexspoke/preferences.md`) — the constitution. Read it in full.
- **`<repo>-preferences.md`** (per-repo root) — repo-local laws (the Per-Repo Preferences Extension Law).
- **`CONTRIBUTING.md`** — workflow, commit granularity, per-repo scope.
- **`GEMINI.md`** — this workspace's own rules: git, and the layer include allowlist.

Cite every law by its canonical Title, never by number (the Law Identity Doctrine).
Never push without an explicit, one-off order (the Git Workflow Law).

Scope discipline — cosmetic edits stay cosmetic; functional identifiers
(header guards, `@…_MAGIC`, `anti://` URIs, `~/anti` paths, `ANTI_*` env vars)
change only via deliberate migration, never a drive-by rename.

`opencode.json` auto-loads the instruction files for opencode agents; the above
is for every other agent — and for humans.

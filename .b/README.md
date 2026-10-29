# `.b` — the serialized target graph

`.b/graph.json` is **the build's source of truth**, not a cache. It declares every
target the workspace builds: 26 library / module / executable / app / external
artifacts and 329 test executables.

A builder reads it and nothing else. `b` receives names, kinds, source paths,
include roots, definition words, compiler-option words, dependency edges, a link
plan, an artifact path and, for an artifact an external tool owns, the argv that
produces it. No repository name, tier, layout rule or output convention lives in
`b`.

## Schema

Top level:

```json
{ "byproducts": [".b/…"], "targets": [record…], "tests": [record…] }
```

A record:

| Field | Meaning |
|---|---|
| `name` | target identity |
| `kind` | `lib`, `mod`, `exe`, `app`, `ext` |
| `sources` | repo-relative source files |
| `includes` | repo-relative include roots |
| `definitions` | preprocessor words, without `-D` |
| `options` | compiler words, verbatim |
| `links` | `{ "targets": [names], "flags": [words] }` — the link plan |
| `deps` | build-order edges, explicit (no sentinels) |
| `output` | the artifact this target produces |
| `generator` | present on `ext`: the argv that produces it |

Paths are repo-relative, and build state is written under `.b/`. The file is
identical on every machine checkout, which is why it is tracked while the rest of
`.b/` is ignored.

## Format

One target (or test, or generated step) per line, and each `sources` / `includes`
list one path per line, so a change to one target diffs as a change to that
target — not as a change to a single 442 KB line. It is ordinary JSON: any
formatter may rewrite it, and the next export rewrites it again.

## Regenerating

```
./tools/b ide > .b/graph.json
```

`ide` is the exporter inside `tools/workspace.c`; it emits the graph directly in
this normalized form. Hand edits are lost on the next export — change the
exporter, not the JSON.

## Known limitation

Options and framework flags are emitted for the machine that generated the file
(`-arch arm64`, `-mmacosx-version-min=14.0`, `-framework …`, Homebrew include
roots). A graph exported on darwin-arm64 describes a darwin-arm64 build; another
platform needs its own export until per-platform records exist.

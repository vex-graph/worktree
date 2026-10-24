 # vexgraph Code Cookbook

This is a per-file call reference. Every section is titled for one class and
its implementation file, such as `## Random class (random.c)`. Each section
contains one C example with exactly one `int main()` and direct calls covering
the public functions declared for that file. A matching public header is
included where needed to make the call surface clear.

Keep examples to declarations, minimal argument storage, constructors, and API
calls. Do not write recipes, helper functions, test assertions, loops, or
expected-result narratives. Add a short comment only when a callback signature
or unusual call shape needs context. Use constructor macros such as `Object()`
and setters for changes; never show numbered constructor arms, `_init`, `_create`,
or aggregate field literals. Use descriptive sample parameters such as
`"api-token-goes-here"`.

Capture every non-void return value in a typed variable at the call site;
boolean predicates use `bool`, and getters follow `T value = Object_getValue(x);`.
Call void operations directly. Never discard a return with `(void)` casts or
demonstrate caller-provided destination parameters. Mark any existing
destination-based public API as a migration gap; do not invent a signature
that differs from its checked-in header.

Include only files with callable public APIs. Annotation-only examples are
separate and explicitly marked `;;ANNOTATION`. Keep R5/R6 project cookbooks out
of this library/framework index. These examples show how to call APIs; the
owning headers and tests define contracts and prove behavior.

## Repository index

Where each repository's records live. `Cookbook` is the file in this Gist;
`Readiness` is that repository's own file in the
[ecosystem readiness matrix](https://gist.github.com/vex-graph/6943f92acb931b25dad1073c46da6ce7).
R5 applications, R6 superapps and personal tools are **end products, not
libraries**, so they carry no cookbook — their interface is the product surface
itself, and only their readiness row is maintained.

| Repository | Cookbook (this Gist) | Readiness (`<repo>.md`) |
| :--- | :--- | :--- |
| `vexspoke` | `vexspoke_functions.md` | `vexspoke.md` |
| `relational-engine` | `relational-engine_functions.md` | `relational-engine.md` |
| `graphvex` | `graphvex_functions.md` | `graphvex.md` |
| `api-haven` | `api-haven_functions.md` | `api-haven.md` |
| `language` | `language_functions.md` | `language.md` |
| `darkbase` | `darkbase_functions.md` | `darkbase.md` |
| `samplerate` | `samplerate_functions.md` | `samplerate.md` |
| `hotcwap` | `hotcwap_functions.md` | `hotcwap.md` |
| `darling-framework` | `darling-framework_functions.md` | `darling.md` |
| `sesh` | `sesh_functions.md` | `sesh.md` |
| `harness` | `harness_functions.md` | `harness.md` |
| `darkbase-headless` | `darkbase-headless_functions.md` | `darkbase-headless.md` |
| `determinant` | `determinant_functions.md` | `determinant.md` |
| `darling-editor` | — end product (R5) | `darling-editor.md` |
| `impedance` | — end product (R5) | `impedance.md` |
| `drawling` | — end product (R5) | `drawling.md` |
| `primeagen` | — end product (personal R5) | `primeagen.md` |
| `anti` | — superapp (R6) | `anti.md` |
| `semicolon` | — superapp (R6) | `semicolon.md` |
| `func` | — personal tool | `func.md` |
| `b` | — build tool (not a library) | — no readiness row |

Records that cover the whole ecosystem, one file each:

- [Blockers and deferred decisions](https://gist.github.com/vex-graph/e921fa188eebbd0c68c4e59646109887)
- [Timestamped test evidence ledger](https://gist.github.com/vex-graph/26f556f1a3a57b09d5c991d5ef9ef5ab)
- [Universal constitution / preferences](https://gist.github.com/vex-graph/4132a6c45cb6d3797c3e8eff2e94035a)

Each repository also keeps its own `SECURITY.md` and `<repo>-preferences.md`
in-tree; those are not Gists.

# Source-aware editor and data inspection

**Owner:** R5 semicolon. Tokenization belongs to R3 language; reusable chart and
diagram widgets belong to R4 darling-framework. Semicolon connects these to the
current project, documents and tools.

## What the user wants

Look at code as meaningful pieces without losing the original formatting:
#define, identifiers, punctuation, parameters and exact whitespace. Use the
language appropriate to the file and project, including C or Java workspaces.

## Plain-language editor behavior

A token view could show "identifier: variableName" and "two spaces" beside the
original text. Highlighting reads token kinds; navigation and rename need symbol
resolution. Neither should rewrite the user's spacing just to display it.
Maintain a document version so delayed worker results cannot recolor old offsets
in a newer document. Diagnostics and selections need the same version discipline.

The spelling dictionary answers "where is this text used?" The semantic index
answers "which declaration is this use connected to?" They are different views.

## Optional future inspection tools

Plots or diagrams could visualize project/tool output using the shared widgets.
Hover should reveal the underlying record and units. Filtering should select
records without deleting them; zoom changes the view, not the data. These are
possible consumers of the shared contracts, not a requirement to build charts
inside the tokenizer.

## Links to the owning contracts and original vision

- /Users/vexgraph/CLionProjects/vexgraph/_docs/_thoughts/language/lossless-tokenization.md
- /Users/vexgraph/CLionProjects/vexgraph/_docs/_thoughts/darling-framework/interactive-charts-and-diagrams.md
- /Users/vexgraph/CLionProjects/vexgraph/_docs/_thoughts/semicolon/mini-ide.md

**Status:** Parked editor plan; no UI or language code changes.
**Next step:** expose one file's lossless token stream in a simple inspection
view after language's round-trip tests pass. Preserve text editing responsiveness.

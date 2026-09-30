# Lossless language tokenization

**Owner:** R3 language. Semicolon consumes this contract as an editor.
**User intent:** identify every source piece: directives such as #define,
identifiers, braces, dot, arrow operator, minus, parentheses, parameters and
whitespace such as <spacecount=2>. Support C, Java and mixed-language workspaces.

## Three different IDs

- **Kind:** what sort of token? Identifier, number, operator, whitespace.
- **Spelling:** which text? Two names may share one interned spelling entry.
- **Symbol:** which declaration does this occurrence refer to? Scope matters.

A lexer splits text into pieces. A parser understands their arrangement. Symbol
resolution identifies what a name refers to. Class_functionName starts as an
identifier; its spelling alone does not prove it is a function call.

## Preserve the original source

Keep an immutable source snapshot plus token kind and byte range. That avoids
copying a string for every token and permits exact reconstruction. Ranges belong
to a particular snapshot/version; after an edit, old offsets are not current.

Example source:

```c
#define SIZE  10
```

Possible raw pieces: hash, identifier `define`, one space, identifier `SIZE`,
two spaces, number `10`, original newline. A higher-level directive record can
group hash and define as the logical #define operation. Preserve spacing even
when the directive has whitespace between those pieces. Language-specific rules
such as longest-match operators must be implemented by each lexer.

<spacecount=2> is a helpful display label, not a replacement for exact text.
Tabs, spaces, CRLF/LF line endings, comments and escaped newlines must survive.
Byte offsets are not screen columns: Unicode and tabs require separate mapping.
Unknown or incomplete input needs error tokens, not a stopped editor.
The No Arrow Sugar Law governs our code; a C lexer must still recognize the
arrow operator in user input without rewriting it.

## Project awareness without mixing responsibilities

A lexer depends on language and dialect. Include paths, macro definitions and
build options additionally inform preprocessing and semantic interpretation.
A workspace may contain C and Java at once: choose the appropriate driver per
source file instead of inventing one token dictionary that parses everything.
A codebase spelling map supplements the grammar; it never replaces it.

## First tests, in plain words

- Join every original token span: get exactly the original bytes back.
- Recognize adjacent operators, strings, comments and whitespace correctly.
- Handle half-written code, Unicode and both newline conventions.
- Editing a token updates the relevant region without stale version results.
- Incremental output matches a full re-tokenization of the same snapshot.

Incremental lexing may extend beyond one line (multiline comments/strings and
preprocessor continuations carry state). Re-scan until lexer state stabilizes.

**Status:** Proposal only. No tokenizer added in this documentation task.
**Next step:** one lossless C lexer and round-trip tests, then incremental edits;
Java and semantic indexing follow after the first contract is proven.

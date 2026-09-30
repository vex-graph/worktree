# Session Lesson 2: Reading Any File in Two Minutes

You don't read code top-to-bottom anymore. Every `.c` file now opens with a cheat sheet. This lesson is how to read it.

## The analogy
A textbook chapter starts with a summary box: what you'll learn, key terms, page numbers. The `;;OVERVIEW` block is that box. A developer (or future-you at 2am) learns the whole file from its first ~100 lines without tabbing to the header.

## Anatomy of the box (top to bottom)
1. **`CLASS: Name`** — who lives in this locker. Exactly one (rule from Lesson 1).
2. **`STRUCT FIELDS`** — the class's memory, field by field, *mirroring the real struct exactly*. If the struct changes and this list doesn't, that's a bug — same as a bug in code.
4. **`PRIVATE HELPERS` / `SLOT RECORD`** — roommates that were allowed to stay, with their fields listed. No behavior, just storage.
5. **`FUNCTION REGISTRY`** — everything the class can do, sorted into four drawers:
   - **Constructors** — birth certificates (`Application_0`, `Application_1`…). Different numbers = different amounts of info, like ordering "a burger" vs "a burger with cheese and no pickles."
   - **Core Functions** — the actual job (`Hot_poll`, `Application_addWindow`).
   - **Setters** — change something (`setName`). Always `void`, always null-safe.
   - **Getters** — ask something (`getName`). Never crash on NULL; return a safe default instead.

## What you actually did
- Rewrote `hot.c`'s overview from `MODULE: Hot` (a vague blob hiding 4 structs) to `CLASS: HotModule` with fields, helpers, and the *full* function list — including `save/restore/migrate` that the old version never mentioned.
- Banned `MODULE:` headers except for true procedural files (`../../../main`, `tests/`). Everything else says `CLASS:`.

## Try it (2 minutes, no coding)
Open `../../../projects/hotcwap/app/application.c`, read only lines 1–45, then close it. Quiz yourself: what are the 6 fields? What are the 3 constructors? If you can answer, the box works.

## Note to self
"The Living Overview Law": when you change a struct, update the box *in the same commit*. An outdated summary box is worse than none — it's a map that lies.

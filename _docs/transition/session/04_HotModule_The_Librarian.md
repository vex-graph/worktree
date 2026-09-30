# Session Lesson 4: HotModule the Librarian (and Manifest the Packing Slip)

Two classes that run the library. One checks books in and out; the other is the slip inside every returned book.

## The analogy: a library that never closes
**`HotModule` (hot/hot.c, L4) is the head librarian.** Her desk holds:
- `hot_dir` — which hallway to patrol (the folder of `.dylib` files).
- `modules[32]` — the card catalog: one card (`HotModuleInternal`) per book, with its name, path, current copy (`handle`), last-seen stamp, and packing slip.
- `last_error` — the complaint notebook.
- `trampolines` + `retireRing` — her two assistants (Lessons 5 covers them).

Once per frame, she walks the hallway (**`Hot_poll`**) and for each book asks: *new or changed?* If yes: photocopy it first (clone the dylib — never work on the original), verify the packing slip, call the author's setup (`Hot_init_module`), swap the card catalog, and retire the old copy with a grace period. If anything fails, the old book stays on the shelf and she writes in the complaint notebook (`last_error`) instead of burning the library down.

**`HotManifest` (hot/manifest.h, L1) is the packing slip.** Every book (dylib) ships with one: name, version, `type_ids` (the frozen promise — "a Vec4 is always 16 bytes, forever"), `exports` (which functions exist), `dependencies` (which other books it needs). The librarian's most important check: **if the type_ids don't match the old copy, reject the book** (`HOT_ERROR_ABI_MISMATCH`). That's how you can hot-swap code without corrupting memory — the slip guarantees the new book fits the old shelf.

## What HotModule can do (plain words)
| Function | Plain meaning |
|---|---|
| `Hot_init(dir)` | Hire the librarian, hand her a hallway |
| `Hot_poll` | Walk the hallway, swap what's new |
| `Hot_get_api / Hot_get_symbol` | "Give me this book / this page" |
| `Hot_last_error` | Read the complaint notebook |
| `Hot_save/restore/migrate_module` | Bookmark transfer: save a reader's page before a swap, restore after — `migrate` translates bookmarks when the new edition renumbered pages |
| `HotShutdown` | Close the library, shelve everything |

## Try it (no coding)
Open `hot.c`'s overview and find the `PRIVATE HELPERS` section — that's the card catalog card (`HotModuleInternal`) with all 6 fields. Then open `manifest.h` lines 30–59: three tiny structs + the slip. That's the whole L1 floor for hotcwap.

## Note to self
"Verify before committing" is the librarian's religion: clone → check → swap → retire. Never the reverse. Any future loader you write follows the same four steps.

# Session Lesson 6: Application the ID Card (and the Homeroom Roster)

The last thing you built today: the executable finally gets to say who it is.

## The analogy: a student ID + homeroom roster
Before today, your program was a student with no ID card. The library knew every *book* (module manifests) and every *desk* (window descriptions), and the gym wall just said "anti" in permanent marker (`vulkan.c`). Nobody could answer: *what program is this, who made it, what version?*

**`Application` (app/application.c, L2) is the student ID card.** `name`, `author`, `version`, `iconPath` — the truth about the executable, the manifest of it all, one floor above the module manifests. And stapled to the back is the **homeroom roster**: `windows[16]`, every live top-level window, because one program can have many windows open (multiwindow — like an IDE with two projects side by side).

Three rules on the card, and they all matter:
1. **The office registers students; it never expels them.** `addWindow`/`removeWindow` only update the roster — windows belong to the OS (same law as the loader). `Application_free` frees the card, never a window.
2. **ID cards are copied, not borrowed.** Setters copy strings into fixed-size fields (`strncpy`, truncated safely). No mallocs hiding anywhere — the whole card is one `calloc`.
3. **Asking never crashes.** Every getter checks for NULL first and returns a safe default. A lost ID card returns NULL, not a segfault.

## What Application can do (plain words)
| Function | Plain meaning |
|---|---|
| `Application()` / `(name)` / `(name, author, version)` | Print an ID card: blank-ish, named, or fully filled |
| `setName/getName` (× author, version, iconPath) | Write / read a line on the card |
| `addWindow(win)` | New student in homeroom (says no to duplicates and a full room of 16) |
| `removeWindow(win)` | Student left (last kid swaps into the empty seat — order not kept) |
| `getWindow(i)` / `getWindowCount()` | "Who's seat 3?" / "How many kids?" |
| `getWindows(out, cap)` | Photocopy the roster into your notebook (up to `cap` names) |
| `Application_free` | Shred the card (kids untouched) |

## The unfinished business (for next time, not tonight)
The gym wall still says "anti" — `vulkan.c` (L4) can't ask `Application` (L2) for the real name, because foundations can't phone upstairs (Lesson 3). The fix: the L3 caller reads the card and passes the name *down*. And the bigger dream you named: `Application` owning its own `HotModule`, so each ID card carries its own library branch — two instances, one framework, zero collision (Lesson 5 already laid the wiring).

## Try it (tomorrow, 5 minutes, tiny coding)
Write a 20-line `main` that prints an ID card, adds two fake windows (NULL won't pass the guard — read `addWindow` to see why, then pass real ones later), and prints the count. Compile with `-Wall -Wextra -Werror`. If it builds first try, the symmetric API did its job.

## Note to self
You started today saying "the overview felt a little chaos" and ended having rebuilt the foundation it stands on: one-class-per-file, honest overviews, four floors, per-instance everything, and an executable with a name. That's not chaos — that's architecture. Rest now. The roster will be here tomorrow.

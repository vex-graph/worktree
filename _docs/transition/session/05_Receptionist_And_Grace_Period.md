# Session Lesson 5: The Receptionist and the Grace Period

The librarian's two assistants. One forwards phone calls so callers never hear construction noise; the other lets people finish leaving before locking the doors. Today you gave each assistant their own office *per branch* — that's the big finale of the session.

## The analogy, part 1: the receptionist
**`HotTrampolineTable` (hot/hot_trampoline.c, L4) is a office receptionist.** Callers dial one stable number (the symbol name, like `"Memory_alloc"`). The receptionist looks at her desk chart (`rows[]`, found by `find`) and forwards the call to today's actual extension (`ptr`).

Why not call the extension directly? Because during a reload, the extension *moves*. The old code is being wheeled out and the new code wheeled in. The receptionist swaps her chart entry atomically (`set`) — one instant, no half-written number. And if a call arrives in that exact instant and gets a dead line, she has yesterday's number on a sticky note (`fallback_ptr`) and retries there instead of dropping the call (`get` with fallback cover). Callers never hear construction noise.

## The analogy, part 2: the grace period
**`HotRetireRing` (hot/hot_retire.c, L4) is the "everyone out before we lock" rule.** When a new book edition arrives, the old copy can't be thrown away instantly — some reader mid-sentence is still holding it. So old handles park in a ring of 16 slots for 4 poll-generations (`retire`), the generation counter ticks each frame (`advance`), and only entries past their grace period get `dlclose`d. Full ring? The oldest gets evicted first. Shutdown? `drainAll` empties everything. (In Java terms: this is the garbage collector you had to hand-build, because C has no GC — Lesson 6 in the main series covers that pain.)

## The big finale: every branch gets its own staff
The old design had **one global receptionist and one global door-locker for the whole company**. Two library branches (two loader instances — your IDE dream: two projects open, same framework) would fight over one chart: same symbol name, wrong forwarding.

Now each `HotModule` embeds its **own** table and ring (`trampolines` + `retireRing` fields, zeroed free by `calloc`). Same code, separate desks. Two instances, zero collision. Before doing it you checked the one real danger — nobody `memcpy`s a `HotModule` (atomics can't be photocopied) — and only then converted all 15 call sites.

## What they can do (plain words)
| Function | Plain meaning |
|---|---|
| `Table_register(name)` | Add a new speed-dial entry, get its slot number |
| `Table_get(idx)` | Forward the call (with sticky-note retry) |
| `Table_set(idx, ptr)` | Rewrite a speed-dial entry, keep yesterday's as backup |
| `Table_find(name)` | Slot number for a name, −1 if unknown |
| `Ring_retire(handle)` | "Finish up, we're closing this copy soon" |
| `Ring_advance()` | Next day; lock up copies everyone left |
| `Ring_drainAll()` | Closing time: everybody out (shutdown) |

## Try it (no coding)
Open `hot_trampoline.h`: find the row (`HotTrampoline`, the sticky-note card) and the table (`HotTrampolineTable`, the desk). Two structs, one file — the slot-record exception from Lesson 1, now with a name.

## Note to self
"Share code, not desks" is the whole lesson. Globals are one shared desk. Instances are separate desks with the same training manual. Whenever two things must not collide, look for the global first.

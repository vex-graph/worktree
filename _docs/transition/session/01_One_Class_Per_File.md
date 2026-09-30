# Session Lesson 1: One Locker Per Student

Today you made a rule: **one struct = one class = one file pair.** Here's why, the simple way.

## The analogy
Imagine a school where 4 students share 1 locker. If one student's milk spills, everyone's homework is ruined — and nobody knows whose milk it was. That was `hot.c`: four structs (`HotModule`, `HotModuleInternal`, `HotTrampoline`, `HotRetiredHandle`) crammed in one file. One bug could touch the whole hotloader, and the blame landed everywhere.

Now every student gets their own locker. Milk spills in `hot_retire.c`? Only the retirement ring gets wiped down. `hot.c` never even smells it.

## What you actually did
- `hot/hot.c` went from **4 structs → 2** (it kept `HotModule` plus its dumb slot `HotModuleInternal`, which has no behavior of its own — like a locker keeping its own shelf).
- `hot/hot_trampoline.h/.c` and `hot/hot_retire.h/.c` were born as real classes with real files.
- Rule 3 in `../../../preferences.md` now says it plainly: *a second public struct in the same file is a defect.*

## The one exception (slot records)
A class may keep its **slot record** — a behaviorless row it fully owns, like a locker keeping its shelf. `HotTrampoline` (the row) lives with `HotTrampolineTable` (the owner) because the row *does nothing on its own*. Rule of thumb: **if it has no functions with its name on them, it can stay. If it does things, it moves out.**

## Try it (2 minutes, no coding)
Open `../../../projects/hotcwap/hot/hot.c` and count `typedef struct`. You should find exactly 2. Then open `hot_trampoline.h` and find the row + the table living together — that's the slot-record exception, working as intended.

## Note to self
You felt the chaos ("the overview felt a little... chaos") *before* you could name it. That feeling was real signal: undocumented roommates in one file. Trust that feeling next time — then count the structs.

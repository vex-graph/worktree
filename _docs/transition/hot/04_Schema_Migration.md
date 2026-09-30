# Lesson 4: Schema Migration (The "Port System")

The holy grail of hot-reloading is **Struct Migration**. If you add `float stamina;` to a `Player` struct in conventional C, the memory layout shifts by 4 bytes. When the DLL reloads, it misreads the old memory, and the engine crashes.

`anti` solves this by treating C structs the way Unity treats C# classes—by reflecting on them at runtime and automating the data migration.

## The Infrastructure (`oop/Class.h`)
In `anti`, you register your struct layouts with the engine:
```c
Class *Player_v1 = Class(TYPE_INT, "health", TYPE_INT, "ammo");
```
The engine internally stores an array of `Field` objects, noting that `health` is at offset 0, and `ammo` is at offset 4.

## The Migration Loop
When you edit your code and compile a new DLL, the struct definition changes:
```c
Class *Player_v2 = Class(TYPE_INT, "health", TYPE_INT, "ammo", TYPE_FLOAT, "stamina");
```

Upon reloading, the `anti` engine executes the "Port System":
1. It uses `Memory_findAll(TYPE_PLAYER)` to locate every old player block in memory.
2. It allocates a new block of memory for `Player_v2`.
3. **The Reflection Magic:** It loops through the `Field`s of `Player_v2` and asks `Player_v1`, *"Do you have a field named 'health'?"* 
4. Because the names match, it dynamically copies the bytes from the old offset to the new offset.
5. When it gets to `stamina`, `Player_v1` says "No", so the engine simply leaves `stamina` at its default value (0.0f).
6. It swaps the memory pointers and frees the old block.

## Why this is Unconventional
In AAA C++ engines (like Unreal), they often force you to restart the editor when you change header files because their hotloaders cannot do this byte-level schema mapping. `anti` uses its `mem.c` type-tagging system to achieve the automated serialization power of a managed language (like C# or Java), but without the crippling performance cost of actually running inside a virtual machine.

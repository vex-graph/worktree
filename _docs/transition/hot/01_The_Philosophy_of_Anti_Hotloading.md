# Lesson 1: The Philosophy of Anti Hotloading

## The Core Problem
In conventional C/C++ engine development (like Unreal Engine), hotloading is notoriously difficult. If you change a struct's layout or a function signature, the memory layout shifts. Because C uses raw memory pointers (`void*`), the newly loaded code will read the old memory incorrectly, resulting in immediate crashes. 

Most engines solve this by forcing a complete editor restart (Unreal C++), or by serializing the entire game state to disk, destroying the environment, and deserializing it into the new environment (Unity C#), which causes massive lag spikes.

## The Anti Solution: A Managed C Engine
The `anti` engine approaches this uniquely by porting the introspection capabilities of Java (its `legacy-java` roots) into native C, without the overhead of a Garbage Collector.

This is achieved through two core principles:

### 1. The "Lens of All Things" (`mem.c`)
In `anti`, you never just call `malloc()`. Every single allocation goes through `Memory_alloc(typeId, size)`. Under the hood, the engine allocates an extra 32 bytes to stamp a `typeId` and `length` header onto the block, and links it into a global registry (`s_head`).

Because of this, **there are no blind pointers in the anti engine**. The host can look at any pointer and instantly know what it is and how big it is.

### 2. Runtime Reflection (`oop/Class.h`)
Instead of raw structs, `anti` registers data structures as a `Class` schema. The engine knows the name, size, and byte offset of every field (e.g., `health`, `ammo`). 

### Why this is Unconventional
In AAA C++ engines, memory is purely data, and types are erased at compile time. In `anti`, type data persists at runtime. This allows the engine to heal its own memory. When a DLL hotloads with a new struct layout, the engine can iterate over all old memory blocks, compare the old schema to the new schema by field name, and automatically migrate the data over. 

This gives `anti` the hotloading flexibility of Unity's C# scripts, but at the raw execution speed of native C.

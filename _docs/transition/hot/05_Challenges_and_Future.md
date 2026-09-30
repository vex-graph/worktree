# Lesson 5: Challenges and Future Architecture

While the `anti` engine's hotloading architecture is robust, it presents specific challenges that must be addressed in future releases to ensure absolute stability.

## Challenge 1: The FSEvents File Watcher
Currently, `hot.c` relies on polling `stat()` or `file_mtime()` every frame to detect if a DLL has changed. While functional for small projects, this burns unnecessary CPU cycles and doesn't scale to massive project directories.
**Future Adaptation:** The polling loop must be replaced with the native macOS `FSEvents` API (or `inotify` on Linux). This allows the OS to wake the engine thread *only* when a file is actively written to disk, achieving zero-overhead hotload detection.

## Challenge 2: Pointer Fixup inside Structs
The Schema Migration (Port System) elegantly handles primitive data types (int, float) by matching names and copying bytes. However, if a struct contains a raw C pointer (e.g., `Entity *parent`), and the `Entity` struct is also being migrated to a new memory location, that pointer becomes a dangling reference.
**Future Adaptation:** The engine must enforce the "Lens of All Things" strictly. Instead of raw pointers inside structs, entities must store **Handles** or **Type IDs + Indices**. If pointers are absolutely required, the Schema system (`oop/field.h`) must be updated to explicitly flag a field as `isPointer`, allowing the Migration loop to update the memory address to the newly migrated target block.

## Challenge 3: Function Pointer Deduplication
In `vk_test.c`, the initial hotloader attempt suffered from a bug where the texture was reloaded every single frame because the path string comparison lacked `#include <string.h>`. 
**Future Adaptation:** The engine should provide a unified macro or utility in `hot.h` for state deduplication, such as `HOT_ONCE(condition)` or automatic symbol hashing, so gameplay programmers don't have to manually write `strcmp` caching blocks every time they want to fetch a hotloaded string or state.

## Conclusion
The `anti` engine proves that native C is not inherently rigid. By combining a globally tracked memory allocator (`mem.c`) with a runtime reflection schema (`oop/Class.h`) and a strict Host/Module boundary, it achieves the elusive "Managed C" dream: the iteration speed of a script-driven engine with the execution speed of bare-metal C.

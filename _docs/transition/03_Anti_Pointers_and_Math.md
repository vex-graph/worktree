# Lesson 3: Pointers, Memory, and the `anti_mem` Pattern

Based on `pointer_exercises.c`, your engine relies heavily on advanced pointer arithmetic. Let's break down exactly how pointers work in the context of `anti`.

## 1. Negative Pointer Math (The Header Pattern)
As seen in your `recover_header` exercise, `anti` allocations place metadata *before* the pointer given to the user.

```c
// How anti sees memory:
// 0x1000: [ magic (4 bytes) ]
// 0x1004: [ size  (4 bytes) ]
// 0x1008: [ PAYLOAD START   ] <- This is the pointer passed around!

static BlockHeader *recover_header(void *payload_ptr) {
    uint8_t *byte_ptr = (uint8_t *)payload_ptr;
    // We step backwards exactly 8 bytes to find the header
    return (BlockHeader *)(byte_ptr - sizeof(BlockHeader));
}
```
**Why this matters:** You must *never* perform this negative math on a pointer that wasn't allocated by your specific `Memory` subsystem, or you will read garbage data.

## 2. Bit-Packed Pointers (Tagging)
Modern 64-bit CPUs require pointers to be aligned to 8-byte boundaries. This means the last 3 bits of any valid pointer are always `000`. 
`anti` exploits this (as seen in `pack_pointer_tag`) to store extra information (like a 3-bit variant or state flag) directly inside the pointer's memory address!

```c
uintptr_t raw = (uintptr_t)ptr;
// Store a tag (0-7) in the empty bottom 3 bits!
uintptr_t tagged = raw | (tag & 0x7); 
```
**Auditing Tip:** Before you dereference a tagged pointer, you *must* clear the tag by masking it (`tagged_ptr & ~0x7`), otherwise the CPU will trigger a segmentation fault (`EXC_BAD_ACCESS`) because the address is invalid.

## 3. Pointer-to-Pointer (Reallocation and Handles)
In `reallocate_buffer`, you use `int32_t **buf_ptr`. 
You do this so the function can modify the caller's *original* variable. In `anti`, since slots are recycled, double pointers are often used as "Handles" to update exactly where a subsystem is pointing if data moves or is swapped.

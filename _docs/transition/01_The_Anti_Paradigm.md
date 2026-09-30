# Lesson 1: The Anti Paradigm - C23 Without Abstractions

You are building `anti`, a lock-free, cache-coherent engine where everything is a pointer. You've stripped away garbage collection, object graphs, and hidden allocations. This lesson bridges your Java/FFM background to the raw reality of `anti`.

## 1. Zero Steady-State Allocation (The Arena Doctrine)
In standard C programs, you `malloc` and `free` constantly. In `anti`, you **do not**. 
The engine carves out one massive region from the OS when it starts. From then on, memory is managed via lockless subsystems (`BitPool`, `RingBuffer`). You don't allocate objects; you claim slots.

When you read the code, look for:
- Pre-allocated pools where items are recycled using ABA-tagged freelists.
- When an object is "freed", it comes back at the same address.

## 2. Self-Describing Pointers
A normal C pointer is just a dumb memory address. In `anti`, pointers are self-describing values. 

Every pointer in `anti` carries a header immediately preceding its address in memory:
`[type_id (32-bit)][length (32-bit)][payload (your pointer)]`

This is why your engine doesn't need a registry lookup to know what a pointer is. By doing **negative pointer math** (stepping backward 8 bytes), you can read the `Type` and `Length` of any allocation instantly.

## 3. The Relational Registry
Instead of objects owning other objects (`player->inventory->item`), `anti` uses a relational symbol registry (`Variable`). 
Names map to `(classId, targetPointer)`. Pointers are joined dynamically, similar to a database table, completely eliminating standard Object-Oriented object graphs.

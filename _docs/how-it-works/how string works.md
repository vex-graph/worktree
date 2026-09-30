# How String Works in vexspoke

> Answers: **"How are strings stored?"**
> Answer: **Memory-allocated blocks with length in the header.**

---

## 1. Strings Are Arena Blocks

Every string is a `Memory_alloc`'d block with type `TYPE_STRING_ARRAY`.
The length is stored in the `MemoryHeader` (32 bytes before the
payload pointer), not computed from NUL.

```c
string_length(ptr) → Memory_length(ptr) - 1   // subtract NUL
string_capacity(ptr) → Memory_length(ptr)      // includes NUL
```

This means `string_length` is O(1) with no scanning, no caching, no
branch prediction miss.

---

## 2. Creating Strings

```c
char *s = string_allocate("hello");         // alloc + copy + NUL
uint8_t *s = string_allocateBytes(bytes, len);  // alloc + copy
uint8_t *s = string_allocateUninitialized(len); // alloc only
```

All return arena-allocated pointers. The caller owns the result.

---

## 3. Operations

| Operation | What it does | Allocation? |
|---|---|---|
| `string_copy(ptr)` | duplicate | yes (new block) |
| `string_equals(a, b)` | comparison | no |
| `String_compare(a, b)` | comparison | no |
| `String_contains(h, n)` | substring search | no |
| `String_indexOf(h, n)` | find position | no |
| `String_substring(s, start, len)` | slice | yes (new block) |
| `String_append(a, b)` | concatenate | yes (new block) |
| `String_appendInto(a, b, dest)` | concatenate into dest | no (caller owns dest) |
| `string_free(ptr)` | free | Memory_free |

**Convention**: lowercase `string_*` = base primitives (allocate, free,
length). Capitalized `String_*` = higher-level ops (contains, indexOf,
append). Both operate on arena-allocated blocks.

---

## 4. Key Insight

Because strings live in the arena and have typed headers, the system
can introspect any pointer:

```c
Memory_type(somePtr) → TYPE_STRING_ARRAY  // it's a string
Memory_length(somePtr) → 6                // "hello" + NUL
string_get(somePtr) → "hello"             // the raw bytes
```

This is what "everything is a pointer with a type ID" means in
practice. A string is not special — it's just another arena block with
a known type.

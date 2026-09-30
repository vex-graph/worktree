# Lesson 10: Strings (Java `String` → `char*` Minefield)

Java `String` is immutable, length-tracked, UTF-16, bounds-checked, and never null without telling you. C `char*` is a hope and a NUL byte. Every string habit you have is wrong here; this lesson lists the replacements.

## 1. Length Is Not Stored — Track It or Scan for It
Java: `s.length()` is O(1). C: `strlen` walks to NUL every call — O(n) per call, and a missing NUL reads off the end of the world.
- Your `primitive/string.c` + length-stamped allocator blocks exist so hot paths never `strlen`. Use them: store `(ptr, len)` pairs, pass lengths alongside pointers (dest-last: `(src, len, dest)`), and treat bare `char*` as a display-only type for `printf`/Cocoa bridges.
- Watch for: `strlen`/`strcpy` in loops or per-frame code. One `strcpy` without bounds is a stack smash; prefer `snprintf`/`strncpy` with explicit sizes (see `vk_test.c` path handling).

## 2. UTF-8 vs UTF-16 vs Bytes
Java: everything is UTF-16 chars. C + macOS: UTF-8 `char*` in your code, UTF-16 inside `NSString`, RGBA bytes in textures. Your label pipeline crosses all three (`Label` text → CoreText `NSString` → raster bytes → `Texture_loadRaw`).
- The manifest parser lesson applies everywhere: `\"`, `\\`, `\uXXXX` escapes must be decoded at exactly one layer, with surrogate-pair combining for non-BMP characters (emoji in your test label: `\xF0\x9F\x8C\xBB`). Double-decode or zero-decode and text corrupts.
- Watch for: `char` signedness. Plain `char` is signed on ARM — byte values ≥ 0x80 go negative. Use `uint8_t*` for byte buffers, `char*` only for NUL-terminated text.

## 3. Ownership: Who Frees the String?
Java: strings are GC'd. C: every `strdup`/formatted buffer needs an owner (Lesson 6 applies double here because strings are allocated constantly).
- Prefer: string views (pointer + length, no ownership) for parsing; slab-allocated buffers for building; `snprintf` into fixed stack buffers (`char pathBuf[1024]`, `titleBuf[256]`) for formatting. Heap-allocate a string only when it must outlive the frame/function.
- Watch for: returning pointers to stack buffers (use-after-return), and `strdup` without a matching free on every path.

## 4. Comparison Is Not `==` and Not `.equals()`
`==` on `char*` compares addresses (Lesson 9). `strcmp` compares bytes — but stops at NUL, so embedded NULs truncate; and it is locale-blind. For engine strings (paths, identifiers, telemetry keys), `strcmp`/`strncmp` on NUL-terminated buffers is correct. For text content with lengths, compare `(len, memcmp)`.
- Watch for: `strcmp` on non-NUL-terminated buffers (reads out of bounds) and `==` on strings (always wrong except for interned constants).

## Watch-out Summary
| Java habit | C consequence | Defense |
|---|---|---|
| `s.length()` | O(n) scan, or overrun | `(ptr, len)` pairs; never bare-scan hot paths |
| UTF-16 everywhere | 3 encodings in one pipeline | Decode escapes once; `uint8_t` for bytes |
| GC'd strings | Leak or use-after-return | Views > slabs > stack buffers > heap |
| `.equals()` | `==` compares addresses | `strcmp` for NUL text, `(len, memcmp)` else |

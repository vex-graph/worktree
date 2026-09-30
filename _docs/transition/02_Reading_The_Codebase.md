# Lesson 2: Reading the Anti Codebase & `../../code.txt`

Your codebase (represented in `../../code.txt`) is highly generated or heavily concatenated C code. Reading it requires a different strategy than reading a typical Java project.

## 1. How to Audit Your Files
Since `anti` doesn't have classes, look for **Structs and Function Pointers**. 

### The Core Subsystems
If you open `../../code.txt`, don't read from top to bottom. Search for the core primitives you built:
- `Type`: Search for `Type_` functions. This handles the bit-packed typing system.
- `Memory`: Search for `Memory_`. This is the lens that extracts `type_id` and `length` from raw pointers.
- `BitPool` & `RingBuffer`: These are the lockless concurrency primitives. The MPMC ring buffer is how your threads communicate without locking mutexes.

### Identifying "Methods" in C
In Java, a method is bound to an object. In `anti`, you achieve this via function pointers or explicitly passing the struct pointer as the first argument (often called `self` or the subsystem name).

```c
// This is the C equivalent of Window.setTitle(String title)
Window_setTitle(Window *w, const char *title);
```
When auditing, always check the **first parameter** of a function to understand what "Object" it is operating on.

## 2. Dealing with Varargs and Symbols
You asked about parameters and varargs. 
In a relational engine, varargs (`...`) are often used to pass a dynamic number of arguments to initialization functions or logging (like `printf`). 

**Auditing Tip for Varargs:** The C compiler does not type-check varargs. If your function expects an `int` but you pass a `float`, it will silently corrupt data. When auditing `anti`'s registry or relational table joins, double-check that the types pushed into varargs match the format string or expected type IDs.

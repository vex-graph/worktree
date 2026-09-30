# Lesson 4: Objective-C and the macOS Window Backend

`anti` handles windowing on macOS entirely natively via AppKit, without external dependencies like GLFW. This requires interfacing C23 with Objective-C (`src/window/`).

## How Objective-C works in `anti`
Objective-C is a strict superset of C. The files handling the window (often `.m` files, though sometimes wrapped in C headers) are where the magic happens.

While your C code uses `Window_setTitle(w, "Title")`, under the hood, the implementation must speak to Apple's AppKit objects.

### The Message Send
In standard C, functions jump to a fixed memory address. In Objective-C, you send a message:
```objc
[nsWindow setTitle:nsStringTitle];
```
At runtime, this translates to:
```c
objc_msgSend(nsWindow, @selector(setTitle:), nsStringTitle);
```

### Auditing the Bridge
When auditing the bridge between your raw C23 engine and the Objective-C window:
1. **Thread 0 Requirement:** Apple requires UI operations to occur on the main thread (Thread 0). Ensure your `Window_` C functions either dispatch to the main thread or are only called from it. Your engine loop (the `Loop` ring buffer consumer) runs on its own thread, which is the correct architecture!
2. **Memory Management:** `anti` is zero-allocation, but AppKit is not. When you pass strings or data into `Window_` functions, check if the Objective-C side is properly managing the ARC (Automatic Reference Counting) or explicitly releasing Apple's objects to prevent memory leaks in the window layer.

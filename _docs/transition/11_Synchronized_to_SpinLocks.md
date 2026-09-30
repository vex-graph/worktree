# Lesson 11: `synchronized` → SpinLocks and Memory Order (Threads Without a Net)

Java gave you `synchronized`, `volatile` with real semantics, `java.util.concurrent`, and a memory model course in every textbook. C gives you `_Atomic`, pthreads, and a manual that assumes you already know what acquire-release means. Your engine is threaded everywhere (draw worker, present loop, producers, hot-watch) — this lesson is the minimum to not corrupt it.

## 1. `SpinLock`, Not `synchronized`
Java: `synchronized` blocks, admits waiting, releases on exception. Your `SpinLock` (`atomic/spin.h`) busy-waits — it burns CPU until the lock frees. Correct usage: hold it for nanoseconds (pointer swaps, freelist pop/push), never across I/O, allocation, logging, or anything that can block.
- Watch for: calling `printf`, `malloc`, file I/O, or Vulkan calls while holding a spinlock. On a contended core this becomes a deadlock-shaped stall. If the critical section can block, you need a mutex, not a spinlock.

## 2. `volatile` Is Not Synchronization
Java `volatile` has acquire-release semantics. C `volatile` means "don't optimize this access" — it orders NOTHING across threads. For cross-thread flags, use `_Atomic` with explicit orders (your `running`, FPS telemetry) or atomics via `stdatomic.h`. Never `volatile bool` as a stop flag.
- Watch for: plain-`bool` or `volatile` flags shared between your draw worker and Thread 0. They work until the optimizer or the ARM store buffer says otherwise — i.e., in Release, on device, demo day.

## 3. Memory Order: Default to `seq_cst`, Relax Deliberately
Java: `volatile`/`synchronized` actions have defined ordering. C: `memory_order_relaxed` guarantees atomicity only — no ordering. Your telemetry uses `memory_order_relaxed` correctly (single counters, nobody depends on order). Anything that publishes a pointer (retirement rings, freelist heads, surface swaps) needs `release` on the writer and `acquire` on the reader, or the reader can see the pointer before the data it points to.
- Rule of thumb: `relaxed` for counters/stats; `release/acquire` for handoff (pointer, flag-then-data); `seq_cst` when unsure. Getting this wrong produces bugs that vanish under debuggers and appear at 60fps.
- Watch for: the window struct's `atomic_*` fields (`contentPanel`, `nativeContainer`, generations) — every cross-thread read must be `acquire`, every publish `release`. Audit these before multi-window work.

## 4. Thread 0 Is Sacred (AppKit Law)
Java: Swing/FX thread rules, but forgiving. AppKit: layer-tree mutation off Thread 0 is undefined — your `dispatch_async(dispatch_get_main_queue())` in `Window_compositeIOSurfaceChildren` is not style, it is law. Vulkan recording may happen on workers; `CALayer`/`NSWindow` calls may not.
- Watch for: any new ObjC call from the draw/present workers. If it touches `CALayer`, `NSView`, or `NSWindow`, dispatch it. No exceptions, ever.

## Watch-out Summary
| Java habit | C consequence | Defense |
|---|---|---|
| `synchronized` anything | Spinlock stalls on blocking calls | Spinlocks for ns-sections only |
| `volatile` flag | No cross-thread ordering | `_Atomic` + explicit memory orders |
| Implicit JMM ordering | Reader sees pointer before data | release-publish / acquire-consume |
| Background UI work | AppKit undefined behavior | Main-queue dispatch for all layer calls |

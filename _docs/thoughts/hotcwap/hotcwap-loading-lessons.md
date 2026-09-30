# Hotcwap loading lessons — replacing functions, making opcodes

**What this is:** paced notes for the human half of the pair — how hotcwap's
loading system actually swaps code, what "replacing a function" really
means, and how that grows into opcodes/actions (the Shortcuts idea).
Analogies are load-bearing: they are the pacing device. Local notes only.

---

## 1. The one distinction that unlocks everything

**A function pointer is a phone number; the code is the person answering.**

```c
typedef int (*ProcessEntry)(void *context);  // the phone number
int status = (*entry)(context);              // the call
```

Replacing the pointer changes who answers the NEXT call. It does NOT
re-route a call already in progress. A C call in flight is a stack frame
with a return address burned into it — the old code stays on the line until
it hangs up. This is why every swap rule in hotcwap is really a rule about
**when a call can end**:

- Current call finishes on the OLD code (always).
- Next call reaches the NEW code.
- The old library unloads only when nothing can dial it again.

Java analogy: assigning a new `Runnable` to a field. The task object is
stable; `run()` is whatever the field points at *when invoked*.

## 2. Why an `extern` is a doorbell, not a swap mechanism

An `extern` symbol gives a KNOWN address to call — a doorbell wired at
build time. Loading a new dylib that defines the same symbol does NOT
rewire the doorbell; the process already resolved that address once.

The rewirable version is one indirection deeper:

```
stable name  →  dispatch slot (atomic pointer)  →  this generation's code
"game.damage"      HotTrampoline row                  dylib gen 7's fn
```

hotcwap already has the middle layer — `HotTrampolineTable`
(`hot/hot_trampoline.h`): one atomic `ptr` per named export, `fallback_ptr`
covering the instant of a swap so nobody ever dials NULL. What it grows
next: generation pins so "call in flight" keeps the old dylib loaded.

Analogy: the trampoline is a **receptionist who transfers calls**. The
receptionist never changes; the extension numbers get re-plumbed during
lunch, and anyone mid-call keeps their line.

## 3. What we actually built: Process = one replaceable entry

The contract (hotcwap `kernel/process.{h,c}`):

```c
typedef int (*ProcessEntry)(void *context);
typedef struct Process {
    _Atomic(ProcessEntry) entry;   // current phone number
    _Atomic(void*) context;        // what we hand the call
} Process;

ProcessResult Process_run(Process *self, int *exitStatus);   // call it
ProcessResult Process_replace(Process *self, ProcessEntry e, void *ctx, void *hot);
```

Rules worth internalizing:

- **Replacement is an operation, not a field.** There is no
  `replacement` slot — you swap the binding at a safe boundary or get
  `PROCESS_BUSY`.
- **Admission status ≠ function result.** "Busy" is not `-1`; the callback's
  exit code travels through the dest-last out-param. Conflating them was
  the original design smell.
- **Run and replace share one gate.** A CAS on `occupied` admits exactly
  one of {run, replace, free}. No spinning, no waiting — lose and retry.
- **One entry ≠ one operation.** `main` is one entry that runs a whole
  game. A script is one entry that calls many registered functions.

## 4. Two replacement speeds (pick per situation)

| Design | Swap boundary | Trade-off |
|---|---|---|
| **Stable loop, replaceable operations** | between frame/work callbacks | simplest; 90% of hot reload value |
| **Replaceable loop itself** | old loop yields at a safe point | needs state handoff + restart semantics |

## 5. From function pointers to opcodes (the Shortcuts shape)

The unit is a **named action with a contract**, not a raw pointer:

```
action   = { stable id, in/out types, current gen, immediate-or-yields, contract version }
workflow = ids + data connections (NEVER raw addresses)
```

Register `game.jump`, `game.damage`, `game.spawn`; the workflow graph stores
IDENTITIES; execution resolves them through the trampoline at call time.

- Native C, script, and composite actions all look identical to the graph.
- Hot swap replaces implementations; the graph never notices.
- R5 (game) registers domain actions; R2 provides the registry primitive;
  the existing project-scoped type system (the One Type Registry Law)
  types the arguments — no parallel type registry.

Analogy: Shortcuts actions are **menu items, not recipes**. The recipe
(implementation) can be rewritten and reprinted nightly; the menu item
"Damage" keeps its seat number.

**Generation policy default:** an in-flight invocation keeps its selected
generation; new invocations get the newest. A suspended script resumes
under its existing contract or migrates explicitly. A workflow MAY pin a
consistent generation set when mixed generations would be incoherent.

## 6. The loading-system rules, compressed

1. **Stage, verify, then publish.** A bad candidate rolls back; the stamp
   never advances; the next poll self-heals (the manifest ladder already
   does this — `MANIFEST_UPDATE` → verify → `MANIFEST_PROMOTE`).
2. **Never unload a generation that can still be dialed.** Retire rings
   give grace periods, but elapsed polls are NOT proof of quiescence —
   real pins (call in flight = hold) are the missing piece.
3. **State snapshot → rehydrate BEFORE commit → rollback on reject.** The
   loader rehydrates into STAGED images first; a rejected restore keeps the
   old generation live.
4. **Swap pointers atomically, cover the gap.** `ptr`/`fallback_ptr` means
   nobody ever calls into a half-swapped table.
5. **R1 owns lifetimes; R3+ owns work.** The loader trusts the ladder's
   placement; it never builds the artifacts.

## 7. Pacing checklist (when returning to this)

- [ ] Process loader pin: `hot` becomes a real retire handle held across
      `Process_run` (the `;;INTENTION` in process.c).
- [ ] Action registry primitive in vexspoke (ids, types, generation).
- [ ] Workflow composition consuming the registry (R4/R5).
- [ ] CDP puppeteering experiment (if ever) — behind a `;;DRAFT`.


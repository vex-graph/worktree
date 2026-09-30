# Typed Signal and UI bindings

**Status:** `;;DRAFT` contract only. Signal is not implemented. Dispatch is a
separate, uncommitted mailbox implementation tested on macOS. Existing Reactive
is still the scalar synchronous wrapper; this proposal does not change it.

## The user's intent

Multiple listeners, typed pointer payloads, and deferred UI-thread delivery.
A name changes once; all bound labels show the latest name without polling or
repainting unchanged content. Java analogy: an observable property feeding
listeners via an executor (not a new thread for every property).

## Proposed payload contract

- `void *value` plus a project-scoped `uint64_t typeId`. A void pointer alone
  erases type; it does not provide runtime type validation.
- Fix the expected type at Signal creation and reject incompatible sets.
  Use vexspoke's existing type identity, not a second type registry.
- Pointer equality cannot detect in-place changes. Prefer immutable snapshots;
  allow an explicit change/version operation when the pointer stays the same.
- A type tag is a contract, not proof that an arbitrary address is valid.

## Ownership must come before convenience

For an initial borrowed-value API, values must remain valid and immutable while
stored, queued or being delivered. Stack strings from returning worker functions
are invalid. Replacing a value does not prove nobody still reads the old one.
Before general async text binding, choose copying or explicit retain/release
operations per payload type. No hidden GC and no automatic free of arbitrary
void pointers. This is an open design decision, not an implemented promise.

## Deferred change delivery

1. A setter validates and publishes a new version under Signal synchronization.
2. At most one delivery job is queued per Signal. Repeated sets coalesce to the
   latest value; events where every occurrence matters use a queue instead.
3. The designated consumer drains Dispatch and Signal snapshots its subscribers
   and current payload without holding a lock across user callbacks.
4. A callback that sets again schedules a later pass, never recursive delivery.
5. A failed Dispatch_post must NOT leave a permanently set queued flag. The
   implementation needs a race-safe rollback/retry policy and explicit failure
   reporting. A dirty value without a queued job needs a guaranteed retry path.

Dispatch currently has no OS wakeup hook, deadline budget or coalescing. The host
must schedule drains on its owner thread; R2 must never import Window/Panel.
A sleeping on-demand UI will additionally need wake-on-post integration.

## Listener and binding lifetime

Use stable subscription identities, not vector indices that move on deletion.
Unsubscribe must invalidate pending delivery before a widget is freed. Define
self-unsubscribe and unsubscribe-of-another-listener during delivery explicitly.
Do not retain raw pointers into a subscriber array across callback-driven growth.
Signal shutdown must account for queued jobs referencing it, even if it has no
listeners. Hotloaded listener code also needs module lifetime protection.

## Darling boundary (proposed, not current API)

A binding in R4 observes a text Signal. On the UI thread it validates/converts
the payload, calls the widget's normal text setter, and invalidates the affected
layout/paint state only when necessary. Two labels can share one Signal.
Unbinding precedes destruction. Two-way editing is a later feature: define
feedback suppression before connecting edits back into the same Signal.

Analogy: Signal is the latest notice on a board; Dispatch delivers a notification
that the board changed; a binding reads the notice and updates its label.
Random/Probable are producers of values, not reasons to reroll on every paint.
Passive computation needs explicit invalidation; laziness alone is not caching.

## Acceptance checklist

- [ ] Two subscribers receive one coalesced latest-value delivery.
- [ ] Worker sets never execute widget callbacks on the worker.
- [ ] Type mismatch is rejected without modifying value/version.
- [ ] Posting failure cannot strand a dirty Signal forever.
- [ ] Callback sets defer; unsubscribe during callback is safe.
- [ ] Queued delivery cannot touch a destroyed widget or Signal.
- [ ] Payload lifetime survives replacement and concurrent delivery.
- [ ] Unchanged text avoids redundant layout/paint; idle UI can sleep and wake.

**Next step:** settle payload ownership and subscription teardown, then implement
Signal independently of darling. This is not yet a production UI binding layer.

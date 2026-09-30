# Test Preferences Restructure — Design Plan

**Status:** `;;COMPLETE` — approved and executed this cycle. `tests/test-preferences.md` was rewritten
to this structure (820 lines: Part I 15 universal laws, Part II 5 subsystem law sets with Seams-to-Prove
ledgers, Part III 4 blueprint repos).
**Target document:** `tests/test-preferences.md` (in the `vexgraph-ecosystem/tests` repo).
**Universal architecture:** `ecosystem/vexspoke/preferences.md` stays authoritative; this document
governs proof and readiness only. Cite laws by Title, never by number.

---

## 1. Why the current file is wrong

Today `tests/test-preferences.md` is a flat list of 12 generic laws. It is well-written but
**repo-blind**: it cannot say what a hot-swap test actually proves, what an api failure code must be,
or which darling variants must exist. The ecosystem is too large and too varied for one flat list.

The inventories (below, section 6) found the real shape of the risk:

- **Every subsystem has unowned surfaces.** vexspoke has whole families with no owner test
  (`bit`, `atomic`, `struct/*`, `net/*`); graphvex's GPU lifecycle exists only in a gitignored
  `_old/` tree; darling has parked test targets; language/darkbase/sesh/samplerate have **zero source
  and zero tests**.
- **Security is the biggest hole.** Unbounded `dlopen`/TOCTOU in hotcwap, no TLS/SSRF policy in
  api-haven, arithmetic-overflow seams in vexspoke, tag/generation gaps in darling, `VkGuard`
  unported in graphvex.
- **Failures are silent.** `Rest_*` returns success on HTTP 5xx; `Http_perform` has no timeout code;
  hotcwap discards `dlclose` results; darling's dirty flags are stubs.

The fix is not more generic laws. It is **universal law (Part I) + per-subsystem law (Part II)**,
each subsystem section carrying its own table of contents and its own concrete proof obligations.

---

## 2. Proposed structure (the new TOC)

```
# vexgraph — Test Preferences (Ecosystem Test Laws)
;;EDITION("2026.09-testing")

> Proof lawbook for the whole ecosystem, per file, battled.
> Universal architecture: preferences.md (vexspoke) — cited by Title.

## Table of Contents

Part I — Universal Test Laws (bind every repo and every file)
  1. Per-File Battle Test Law
  2. Contract Before Cases Law
  3. Public Surface Proof Law
  4. Value Boundary Matrix Law
  5. Pointer, Identity, and Dereference Safety Law
  6. Arity and Variadic Dispatch Law
  7. Failure Atomicity and Recovery Law
  8. Failure Observability Law                 (new)
  9. Determinism and Reproducibility Law       (new)
 10. Resource and Lifetime Law
 11. Concurrency and Bounded Progress Law
 12. Adversarial and Hostile-Input Proof Law   (new — security)
 13. Executable Evidence and Readiness Law

Part II — Subsystem Test Laws
 14. hotcwap Test Laws        (R1 host)
 15. vexspoke Test Laws       (R2 substrate)
 16. graphvex Test Laws       (R3 GPU)
 17. api-haven Test Laws      (R3 API)
 18. darling Test Laws        (R4 UI)

Part III — Blueprint Repos (stub-stage; rules provisional)
 19. language Test Laws
 20. darkbase Test Laws
 21. sesh Test Laws
 22. samplerate Test Laws
```

Order follows R-level (host → substrate → drivers → UI), matching the *Vertical Integration Law*.

---

## 3. Part I — Universal Test Laws

The existing 12 laws are kept verbatim (they are sound): Per-File Battle Test Law, Contract Before
Cases Law, Public Surface Proof Law, Value Boundary Matrix Law, Pointer, Identity, and Dereference
Safety Law, Arity and Variadic Dispatch Law, Failure Atomicity and Recovery Law, Resource and
Lifetime Law, Concurrency and Bounded Progress Law, Executable Evidence and Readiness Law; plus the
Darling Component Narrative and Focus Law and the Runtime-Level Seam Law fold into Part II.

Three new universal laws:

### Failure Observability Law
- **Definition:** A rejection the contract promises must be **observable**: a return code, and — on
  cold paths — a log to stderr/stdout that the test can assert. Failure is never silent where the
  contract says it rejects.
- **The Why:** A crash, a silent no-op, and a correct rejection are indistinguishable if nothing
  reports which happened. `Rest_*` returning true on a 5xx, and hotcwap ignoring a `dlclose` failure,
  are exactly this class.
- **The Rule:** every promised rejection has an asserted observable channel; log-once determinism is
  testable; hot paths stay quiet per the Cold-Strict, Hot-Minimal Validation Law.

### Determinism and Reproducibility Law
- **Definition:** A passing test asserts the **same result for the same input** every run. No test
  outcome depends on clock, scheduler luck, address layout, or an unseeded RNG.
- **The Why:** Flaky green is worse than red — it hides regressions and erodes the readiness claim.
- **The Rule:** seed all randomness and record the seed; never synchronize with sleeps; property and
  metamorphic tests where an oracle is not exact; a nondeterministic test is a defect, not a rerun.

### Adversarial and Hostile-Input Proof Law (security)
- **Definition:** Every public seam that consumes **untrusted input** — bytes, sizes, indices,
  pointers, paths, URLs, filenames, binary modules, network frames, serialized data — has an
  adversarial test that feeds malformed, oversized, truncated, and hostile values on the **cold
  seam**.
- **The Why:** Untrusted input is how crashes, overflows, traversal, injection, SSRF, and
  decompression bombs enter the system. The inventories found these unproven across every repo.
- **The Rule:**
  1. Enumerate the untrusted seams per file; each has an adversarial battery.
  2. Cover overflow (`len + 1`, `count * sizeof`, capacity doubling), underflow, `UINT*_MAX`
     boundary, negative-where-unsigned, embedded NUL, invalid UTF-8, and hostile sizes.
  3. Cover path/URL/redirect/CRLF injection, symlink/hardlink, and TOCTOU where a check precedes a
     privileged use.
  4. Cover resource exhaustion: deep nesting, huge counts, decompression/expansion bombs, exact-cap
     and one-over-cap, each with a bounded-wait watchdog so a test can never hang the suite.
  5. A sanitizer finding (ASAN/UBSAN/TSAN) fails the proof.

---

## 4. Part II — Subsystem Test Laws

Each subsystem section opens with a one-line purpose and its own law list. Titles below are the
proposed laws; each carries concrete proof obligations grounded in the inventory.

### hotcwap Test Laws (R1 host)
- **Two-Dylib Swap Law** — every swap is exercised with **two real dylibs**: boot dylib A, swap to
  dylib B, assert state preserved (`Hot_save`/`Hot_restore`/`Hot_migrate`), generation advanced, and
  A retired but still mapped in the retire ring.
- **Stale and Wrong Binary Law** — a dylib missing `VkModuleGetTrampolines`, a foreign-magic dylib, a
  wrong-ABI/version dylib, and a stale generation are each rejected fail-closed with rollback and a
  later self-heal; asserts `HOT_ERROR_*` and preserved caller state.
- **Manifest Resilience Law** — missing manifest is **created**; empty/truncated/duplicate-key/corrupt
  manifests clear the mount without overwriting the existing file; unvalidated section stems; the
  ladder (`bin/current`, `.generation`) is asserted at each stage.
- **Loader Trust Boundary Law (security)** — symlink and TOCTOU between verify and `dlopen`; `DYLD_*`
  and search-path hijack; permissions/ownership of `bin/current` and `manifest.json`; path traversal
  via `VEX_MANIFEST`/`HOME`; unsigned-binary adoption must be a **stated** decision, not silent.
- **Retire-Ring Overflow Law** — 17+ swaps drive the 16-slot ring, asserting the oldest handle is
  closed only when quiescent, and that a `dlclose` failure is observed, not discarded.
- **Teardown and Bounded Wait Law** — the save worker is joined before handles are torn down; a save
  in flight during shutdown is safe; `HotShutdown` obeys the Teardown Order Law.

### vexspoke Test Laws (R2 substrate)
- **Deterministic Calculation Law** — the *Determinism and Reproducibility Law* applied: identical
  input yields identical output for math, calc, hash, and sort; property/metamorphic oracles.
- **Boundary Value Law** — zero, negative, empty (`{}`, `''`, `""`), and `nullptr` for every
  collection and primitive: `Array/List/Map/Set/SparseSet/MinHeap/Queue/Deque/Stack` at
  empty / one / size / size+1 / overflow.
- **Pointer Legitimacy Law** — `Memory_*`, `BitPool_*`, `StringPool_*`, `SymbolTable_*`, `Cell_*`,
  `Shelf_*`: wrong pointer, misaligned/interior pointer, foreign-arena pointer, freed/stale pointer,
  forged type/project ID, and sugar-tampered header (`ha[-4]`, `ha[-16]`) each rejected fail-closed
  with unrelated state intact.
- **Failure Observability Law (substrate)** — where it catches, assert what the caller observes
  (`false` / `0` / `nullptr` / safe default) and the stderr line on cold rejections
  (`SymbolTable_instant/rename` already log).
- **Overflow Guard Law (security)** — the specific seams found: `Transient_alloc` missing the
  `UINT32_MAX` guard, `StringPool_isSlot` deref-before-range-check, `Url_base64` `4*((len+2)/3)`
  overflow, `ProbableObjects_add` `totalWeight + weight`, `primitive/string` `len + 1`, and
  `count * sizeof` in radix sort / BVH.
- **Lifetime and Arena Law** — double-init, post-shutdown reuse, failed-construction cleanup,
  `MemoryArena_destroy` with blocks outstanding, `MemoryArena_realloc` cross-arena routing.
- **Concurrent Substrate Law** — `atomic/ring` (MPMC), `atomic/spin` (ticket locks), `bit` ABA tags
  under contention, each with a bounded external watchdog and TSAN.

### graphvex Test Laws (R3 GPU)
- **Backend Conformance Law** — the same contract suite passes for the Vulkan, Raster, and Null rows;
  a headless mock is never presented as hardware-valid.
- **Native Pixel and Present-On-Demand Law** — `Device_resize`/`present` operate in native hardware
  pixels; exactly one present entry; present only on change; asserted against the raster reference.
- **Resource Retirement Law** — port and run the retire/swapchain/sync suites (`texture_retire`,
  `raster_graphics`, `graphics_layer`) against the active tree: fence-signal vs retire-guard vs
  two-frame lag, timeout strikes, `VK_ERROR_OUT_OF_DATE`/`SUBOPTIMAL` rebuild, device-loss latch.
- **Safety-Net Law** — `VkGuard_check`/`checkResource` ported to the active tree and tested for
  debug-on vs `NDEBUG` tree-shake and log-once determinism; bindless texId clamped to `Texture_maxBoundId`.
- **Stride Overflow Law (security)** — `shadowAlloc`, `Image_upload` `width*height*4`, and
  `textureBytesOk` at `UINT32_MAX` dimensions; reject, never wrap.
- **Shader Fallback Law** — `loadSpvAny` precedence (`ANTI_SPV_DIR`/`VEX_SPV_DIR` → exe/spv →
  Resources/spv → CWD) and compile-failure fallback for missing/corrupt `.spv`.
- **Device Fuzz Law** — no loader, missing GPA/symbols, no queue family, instance/device create
  failure each rejected with `nullptr` and partial state freed.

### api-haven Test Laws (R3 API)
- **Transport Failure-Code Law** — a deterministic, distinct outcome for DNS failure, connect
  refused, TLS failure, timeout, reset mid-headers, reset mid-body, and short read; today
  `Http_perform` collapses these to a bare `false`.
- **Status Taxonomy Law** — 1xx/2xx/3xx/4xx/5xx, 429 with `Retry-After`, and 503 classified
  explicitly; **`Rest_*` must not report success on a 5xx** (currently a defect).
- **Retry and Recovery Law** — retry is a **process**, not a hope: bounded attempts, capped
  exponential backoff with jitter, idempotency, cancellation, and an asserted outcome of
  succeeds / stays-safely-rejected / needs-explicit-reset. (No retry exists today — this law drives
  new code and tests.)
- **Dropout Law** — across **all** situations: partial headers, truncated body, stream EOF without
  `[DONE]`, mid-line 2048-byte SSE flush, and reconnection absence, each with an asserted result; a
  dead stream must be an observable negative, not silence.
- **Volume and Saturation Law** — “if it is too much, create a test”: oversized `Content-Length`,
  chunked overflow, decompression bomb, JSON depth 24, exact-cap body without NUL, 64 KiB MCP line,
  256 KiB response — one test per limit, each with a bounded watchdog.
- **Offline-Proof Law** — no test requires the live internet; a loopback fault-injection server
  drives DNS/refused/timeout/reset/short-read deterministically; a blocked loopback is an explicit,
  recorded skip, never a pass.
- **Endpoint Trust and SSRF Law (security)** — allowlist/scheme policy over the three duplicated
  `parseUrl` copies; reject metadata IP (`169.254.169.254`), localhost/LAN, `file://`, `[::1]`, and
  userinfo abuse; MCP `web_search base` override constrained.
- **Secret Handling Law (security)** — TLS verification asserted (and its current unreachability
  documented), no cleartext API key in URL query strings, bearer/token redaction in errors and logs.
- **Framing and Escaping Law** — control-byte escaping in MCP JSON, `rawIdExtract` `"id"` spoofing
  and truncation, and JSON-RPC `-32700` on malformed input.

### darling Test Laws (R4 UI)
- **Window-First Law** — component tests run inside a **real window**; everything renders inside that
  window; a headless mock is never presented as proof of hardware behavior.
- **ScrollPanel Habitat Law** — containers are mounted inside a scrollable **ScrollPanel**; nested
  scroll chaining (consume-then-bubble via `scrollByChained`), clip, and paint-skip asserted.
- **Variation Matrix Law** — every element is exercised across a **matrix of the same element**:
  - size: large, small, thin, thick;
  - state: focusable, highlightable, hovered, pressed, disabled, checked, selected, open;
  - appearance: background, color, foreground, style, opacity, radius mode, z, margin;
  - capability: renderable, clickable, logic-based, scrollable, overlay.
  Each row is one asserted case; the matrix is the acceptance surface.
- **Focus and Input Reality Law** — initial focus, keyboard traversal (Tab/arrows — must be added),
  focus gain/loss/restoration, destruction of the focused element, pointer capture across
  destruction and re-parenting, and the cross-window focus divergence (`s_focusedPanel` vs the
  bridge store); callbacks fire exactly once.
- **Present-On-Demand and Dirty Law** — `Panel_isTreeDirty`/`clearTreeDirty` are real (today stubs),
  so dirty propagation, retained targets, and present-on-change are actually proven.
- **Layout Robustness Law (security)** — container growth overflow (`capacity * 2u`,
  `sizeof(Component) * capacity`), deep-tree recursion in dispatch/paint, and NaN/Inf/negative
  geometry into `GraphicsComponent` and the scroll clamp.
- **Untrusted Text Law (security)** — Markdown/RichText scanners, Input/InputOTP, and
  `Label_charIndexAt` against malformed UTF-8, embedded NUL, and capacity boundaries.

---

## 5. Part III — Blueprint Repos (provisional)

language, darkbase, sesh, and samplerate have **zero source and zero tests**. They get sections now
so the first real commit lands with its rules, not after. Each section lists its top three holes
(from the inventory) as the initial obligation:

- **language** — tokenizer boundary matrix; grammar-dylib hot-swap rollback; malformed/partial LSP
  frame and external-process death.
- **darkbase** — persistence durability (WAL replay, torn-write, backup/restore with a real change);
  zero-copy cursor boundary/lifetime; `DbUri` malformed input plus credential redaction.
- **sesh** — session ordering and reconnect reconciliation (bounded backoff); adversarial wire-protocol
  fuzz (length, CRC, MTU chunking, varint); sanitizer proof that PII/secrets are removed before transmit.
- **samplerate** — long-run glitch/underrun soak with an allocation watchdog (zero malloc on the audio
  callback); SPSC ring concurrency with overflow/underflow drop-degrade; malformed WAV/MIDI parse.

---

## 6. Cross-cutting notes the sections depend on

- **Testing locus:** the *Test Segregation Law* says `_tests/`; the tree is `tests/`. The sections
  assume `tests/<subsystem>/` and this plan flags the wording drift for a one-line fix.
- **Wiring:** `tests/CMakeLists.txt` currently wires only graphvex. Each section's laws are unprovable
  until its targets are named and wired (`-Wall -Wextra -Werror`, nonzero exit on failure).
- **Token disambiguation (still required):** the 34 stale `test-preferences.md` references that mean
  the supreme constitution must become `preferences.md` (tracked in
  `test-preferences-charter-plan.md`), independent of this content restructure.
- **No meta-laws:** per the authorial decision, no law governs this document's own existence,
  precedence, or synchronization; no `;;SYNC`.

---

## 7. Decisions taken

1. **Blueprint repos:** included. Part III carries language/darkbase/sesh/samplerate now.
2. **Universal laws:** kept the 12 in Part I **and** added the 3 new ones (13–15), **and** specialized
   the Focus law (into the darling Variation Matrix / Focus and Input Reality laws) and the
   Runtime-Level Seam law (into each subsystem's Seam obligations). Nothing removed; Part II holds the
   concrete restatements.
3. **Scope:** rewrite the document only, shaped for incremental fixing (the Seams-to-Prove ledgers name
   one target test per row). Wiring targets and executing the adversarial batteries are the next cycle.

## 8. Next cycle (not this one)

- Retoken the 34 stale `test-preferences.md` → `preferences.md` references
  (`test-preferences-charter-plan.md`).
- Wire `tests/CMakeLists.txt` for every subsystem (`-Wall -Wextra -Werror`, nonzero exit on failure).
- Begin the highest-severity batteries: hotcwap Loader Trust Boundary, api-haven Endpoint Trust and
  SSRF, vexspoke Overflow Guard.

---

## 8. Inventory basis (evidence)

Performed read-only across `ecosystem/*` and `tests/*`:

| Repo | Source state | Owner tests | Worst holes |
| :--- | :--- | :--- | :--- |
| hotcwap | real (`kernel`, `hot`, `window`) | 11 harnesses | no ABI/trust check around `dlopen`; TOCTOU; manifest adversarial cases |
| vexspoke | real (332 files, 39 dirs) | 33 harnesses | `Transient_alloc` truncation; `StringPool_isSlot` deref-before-check; whole `struct/`,`bit/`,`atomic/`,`net/` families unowned; no sanitizers |
| graphvex | active CPU/Vulkan-device + gitignored `_old/` | 11 headless | GPU lifecycle only in `_old/`; `VkGuard` unported; stride overflow edges |
| api-haven | real (`api`,`ai`,`mcp`) | 13 harnesses | no retry; no TLS/SSRF policy; `Rest_*` success on 5xx; size limits unproven |
| darling-framework | real (large widget set) | 13 wired, rest parked | `isTreeDirty` stub; no focus traversal; container overflow; no window-based CI |
| language/darkbase/sesh/samplerate | **stub** (0 source) | none | everything |

---

*Deliverable of this cycle: this design plan. Approval required before rewriting the document or
wiring targets.*

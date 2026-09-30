# Anti — Game Engine R&D

**What this is:** `anti` was the engine core that once lived inside
vexspoke. It now has its own space. This file is the full R&D dump —
every feature, philosophy call, and explicit non-goal — parked verbatim
so nothing evaporates. Organized, not trimmed.

Base rule: **first developed on a base-model Mac.** No-bloat baseline;
if it flies there, it flies anywhere. Empty-window loop (nothing
rendered, just the loop) is the zero-overhead proof — target 6-digit
fps. Templates ship in three flavors: **nothing / regular / cutting
edge**, showing which features are on by default.

---

## 1. Editor workflow
- **Universal undo tree, persisted** across focuses and trees. An undo
  list on each scene, item, script, modification — everything.
- **Multiple scene viewports**: different perspectives of the *same*
  scene, side by side in the editor.
- **Hierarchical focus workflow** + **breadcrumbs (and breadcrumb
  focuses)** — always know where you are and how you got there.
- **Isolate in new tab**: pop any object/scene into its own tab.
- **Multiple tabs, peekable, detachable**: tabs can peek or move to a
  different window over any tab/scene.
- **Editor renders 2× the viewport** (1/3 ratio fallback if heavy) so
  exploring stays smooth while the game view stays honest.

## 2. UI design (the 5-column law)
- Columns: **left icons | left sidebar | main scene/canvas |
  right sidebar | right icons**.
- Left sidebar has exactly **5** things: files/directory, toolbox,
  exports, game hierarchy, find assets (textures/objects/audio/inspo
  across sectors + online marketplace via object/image APIs, e.g.
  Openverse). Scour 4–5 items, the info is there.
- Right sidebar has exactly **4**, dynamically switching on what you're
  holding: game properties → scene properties → group properties →
  object properties. No manual switching unless you want it.
- **Two play buttons**: simulate (current scene, in place) vs play (the
  real game in a new window, with built-in profiling preview).
- Bottom bar: git icon + breadcrumbs left; **AI-look** icon + help right.
  The AI looks at your hierarchy and tells you what's wrong with the
  visuals — advice only, **no autonomy** (you keep fine control), and it
  never generates images/video/audio. Help opens docs.
- Game-property combobox (consistent window, 10 items): application,
  window, renderer, structures, variables, events, database, server,
  bugs, export (as game or project).
- Niche-but-necessary UIs ship anyway: lyrics, empty states,
  progressive-blur scroll panels, layered panels, grids, console, code
  text areas.
- Prebuilt UIs for UI design, stackable inside each other (hybrid UI
  for specific actions), tab-navigable for accessibility. Blur-any-object
  hotkey + rectangle border helpers for optical balancing (the Apple
  philosophy) — no manual Photoshop trips.

## 3. Rendering (bindless or bust)
- **Bindless architecture (objects AND textures) is a must.**
- **Stackable per-object filters via render graphs**: 150+ built-in
  filters, stacked any time, any order — and order matters
  (`box blur > contrast > cel shade` ≠ `cel shade > contrast > box blur`).
- Users **can't write their own shaders** (the known disadvantage).
  The philosophy: more filters × config is 20× easier to modify than
  hand-rolled GLSL/HLSL. Choice over code.
- **Stackable lighting, 4 levels**: baked (path-traced once) →
  deferred → global illumination (maybe surfel cache) → full path
  tracing (for the stubborn). Lights and shadows bleed across levels,
  4 down to 1.
- **Golyporphism** (glass polymorphism): OIT via tiled compute shaders,
  no linked lists.
- **Per-object dedicated canvas**: draw on top of objects Procreate-style,
  with layers — a filter stack (canvas) inside a filter stack (object
  textures) inside a filter stack (render loop).
- **Virtualized geometry, FOSS** (free, open source — but solo dev, no
  PRs, full control). Deliberately *not* Nanite: no distance-automatic
  LOD. The whole mesh swaps when the object shrinks on screen (full
  object → 1/4 → 1/8 → 1/16 …), 128-triangle meshlets, max 8 cooked
  models per model (128 → 2). Meshlet culling on terrains for good
  measure, no per-geometry LODs — uniformity over cleverness.
- **Tesseract folding coordinates / portal scenes on day 1.**
- **Secure-enclave-flavored GPU work** for security/random/PRNG the user
  can't read or cheat on.
- **DMA is a non-goal**: not in your face, not in the philosophy, no
  feature. Stays out.

## 4. Relational engine + Darkbase
- The **"relational engine"**: DOD relational database over `int[]`
  buses of `{pool id, pool index, …}` — alternating pairs that *are*
  pointers. Object pools are struct pools; holding a pointer means
  reactive O(1) updates across everything when it moves. Different from
  Mass and DOTS: pools free/reuse by index, pointers stay live.
- **Create-your-own-struct**: user defines mob/player/anything and it
  reflects into the relational engine seamlessly — hoops of pointers,
  still O(1).
- **Darkbase**: built-in DBMS powered by the relational engine. Pairs
  with the built-in server on trivial settings (ip, port, data, params).
- **Built-in server**: P2P *or* centralized, observable, reports errors
  and retries on cut connections. Same simple settings.
- **Built-in RAGs** on the same relational engine.
- **Serialization**: easy, secure, backwards-compatible — index bus,
  paged file, table of contents.
- **SEARCH EVERYTHING + QUERY EVERYTHING**: searching "speed" finds
  `player.speed`, its definition, *and* related settings, across all
  parts. And the search bar initializes values directly.

## 5. Physics: reversible until disturbed
- **Deterministic physics** (reversible — with a scrubber) *and*
  **non-deterministic physics** (baked per scene, or mixed).
- The rule: when a deterministic object gets disturbed, it flips to
  non-deterministic **instantly** and leaves the scrubber (the scrubber
  can't show what was never determined). A **bake button** re-syncs
  everything.

## 6. Threads you can touch
- Threads can be **added, removed, or re-behaved**; prebuilt engine
  threads can't be deleted.
- 4 thread levels: **unused / sleep / dynamic / busy-wait** — good for
  rhythm games and anything timing-critical. When scripting threads are
  fully booked, add more.

## 7. Memory & streaming
- **mmap baked in**, resizable pages for discrete GPUs — UMA gets its
  (slightly unfair) Mac-fps advantage on purpose.
- Streaming as pages: **SSD → RAM → VRAM**, plus **SSD → VRAM** direct.

## 8. Coordinates & precision
- **Built-in switchable coordinate precision**: fp32 ↔ fp64 ↔
  int32fp32 / int64fp64 / int64fp32 and back. The type is a setting,
  not a rewrite.

## 9. Scripting without boilerplate
- **Apple-Shortcuts-type scripting**: one-liners, no boilerplate.
- Users can reshape constructs (`for(Object = setObject(); …)`).
- A single shortcut acts as a reusable method *and* multiplies as an ID
  into the relational engine.
- Built-in editor data structures for scripting/variables/procedural
  generation — **observable**, event-triggering.
- Engine lifecycle script hooks: run **BEFORE the engine starts** and
  **AFTER the window closes / app terminates**. All events (every
  listener/adapter) visible in game properties.

## 10. Input, devices, humans
- Tablets, controllers, custom keyboards. **Per-device profiles saved
  into the game**; the engine remembers what hardware you have.
- **Haptics on.** **Speech-to-text and back** (voice chat ready).
- **System event detection**: USB plug/unplug, app install/launch/quit,
  what the machine is running or doing.

## 11. Trust & shipping
- **Built-in bug catcher/reader**: devs get a bug-report API to their
  own site, with **scene snapshots** showing what went wrong.
- **One-click export to mobile/console**: a C `.class`-file compiler
  (or AOT path) so porting through SDKs is easy.

## Status
R&D parked, not scheduled. Substrate exists (relational types, pools,
hot-swap, windows, compositor); engine-editor work not started.

## Next step
When the mini IDE (`/Users/vexgraph/CLionProjects/vexgraph/_docs/_thoughts/semicolon/mini-ide.md`) reaches a working editor shell,
revisit #2/#5 here first — viewport + physics determinism are the two
load-bearing bets. Everything else fans out from those.

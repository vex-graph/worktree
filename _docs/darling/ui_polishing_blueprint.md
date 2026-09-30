# UI Polishing Blueprint — Implemented → Polishing via Live Events

> Execution plan for promoting the 9 interactive controls from `Implemented`
> to `Implemented and Polishing` (see `_docs/ui_checklist.md` audit law).
> Rule: a row is promoted ONLY by landing live events + fired callbacks,
> verified by a headless test, in the same commit. Never by argument.
> Sources: `projects/darling/event/dispatch.h/.c`, `event/pointer.h`
> (`PTR_DOWN/MOVE/UP/DRAG/HOVER/ENTER/LEAVE/CANCEL`), `event/bridge.h`,
> `darling/container.h` (`Container_hitTest`, `Container_resolve`).

---

## 1. Frozen contracts (no worker may renegotiate these)

**Contract A — callbacks:** `void (*fn)(void *ctx)` everywhere. Callbacks are
notifications, not data carriers. State is pulled via symmetric getters
(`Checkbox_isChecked`, `Slider_getValue`, `Input_getText`). Rich data rides
the existing `ValueEvent`/`ActionEvent`/`UIKeyEvent` pipeline, never ad-hoc
signatures. Zero API breakage: headers already type this way.

**Contract B — pointer:** every interactive widget exposes

```c
void <Widget>_handlePointer(<Widget> *self, int kind, float localX, float localY);
```

`kind` is the `PTR_*` enum, coords are target-local (dispatch translates),
`void` return, null-safe no-op on null `self`. Widgets never walk the tree.

**Contract C — keys:** `void <Widget>_handleKey(<Widget> *self, const UIKeyEvent *ev)`
for focusable widgets (Input, Textarea). Dispatch delivers to the focused
panel only.

Style (all workers): `(*p).field` never `->`; `T *name`; `(T*) var` casts;
dest-last outs; single-line braceless `if`s; `;;OVERVIEW` registry updated;
one class per commit inside `../../projects/darling` (Rules 6/20/25); no push.

---

## 2. Work split (doubled throughput)

| Owner | Scope | Files |
|---|---|---|
| opencode (this side) | #3 Blueprint (this file) + Pkg 1 dispatch + Pkg 4 text | `event/dispatch.c`, `field/input.h/.c`, `field/textarea.h/.c`, tests |
| antigravity (other side) | Pkg 2 click + Pkg 3 drag | `button/button.h/.c`, `field/checkbox.h/.c`, `button/switch.h/.c`, `field/radiogroup.h/.c`, `field/slider.h/.c`, `field/knob.h/.c`, `field/scrollbar.h/.c`, tests |

Packages run FULLY parallel — Contract B decouples widgets from dispatch.

---

## 3. Pkg 1 — central dispatch (`event/dispatch.c`, procedural MODULE)

1. `Darling_firePointer(root, ev)`: recursive reverse-child-order walk
   (top-most first) with `Container_hitTest`; first hit wins. Translate to
   local coords (`screen - resolved origin`); call the target's
   `handlePointer` (type dispatch via `Memory_type`, no cross-includes of
   widget headers — use extern decls or a handler table).
2. Capture: `s_activePanel` set on `PTR_DOWN`, receives all `PTR_DRAG`
   until `PTR_UP` (sliders/knobs keep scrubbing outside bounds).
3. Hover: `s_hoveredPanel` tracking, `PTR_ENTER`/`PTR_LEAVE` pairs
   (Label hover/cursor path rides this).
4. Focus: `s_focusedPanel` set on `PTR_DOWN` for focusable kinds;
   `Darling_fireKey` forwards there. `consumed` flag short-circuits bubble.
5. `bridge.c` already attaches OS listeners — dispatch consumes its events,
   no bridge changes.

## 4. Pkg 2 — click controls (antigravity)

* **Button**: `Button_press` honors `disabled`, invokes `onPress(ctx)`.
  `handlePointer`: ENTER/HOVER→`hovered=1`, LEAVE→clear hover+pressed,
  DOWN→`pressed=1`, UP-inside→clear+`press()` (click-on-release). Paint
  selects `bg/bgHover/bgPressed` (painter work may follow separately).
* **Checkbox**: `toggle` clears `indeterminate`, dirties, fires
  `onChange(ctx)` (getter reveals state). `handlePointer`: UP-inside→toggle.
* **Switch**: `handlePointer`: UP-inside→`Switch_setOn(!on)` (firing comes
  free via existing `setOn`). Thumb glide animation optional follow-up.
* **RadioGroup**: real option store (owned labels, `List*` exists),
  `select(index)` enforces mutual exclusion + fires `onSelect(ctx)`,
  row-click→index→select. `addOption`/`clear` stop being stubs.

## 5. Pkg 3 — drag controls (antigravity)

* **Slider**: DOWN/DRAG→`ratio=(lx-pad)/trackW` clamp `0..1`,
  `val=min+ratio*(max-min)`, step-snap if `step>0`, fire `onChange(ctx)`
  only on actual change. Capture keeps scrubbing alive outside bounds.
* **Knob**: `setNormalized` clamps + fires; vertical-drag scrub
  (`Δy`→value) or `atan2` rotary tracking; fires on change.
* **ScrollBar**: thumb DOWN tracks grab offset, DRAG repositions value;
  track-click pages; both directions sync with `ScrollContainer`
  (`syncFromBar`/`syncToBar` already exist).

## 6. Pkg 4 — text fields (opencode)

* **Input**: `insertChar` (byte-wise UTF-8 append at cursor, cap-truncate
  like `setText`, re-measure caret target, fire `onChange`),
  `eraseChar` (backspace before caret, fire `onChange`), `handleKey`
  (printable→insert, backspace→erase, left/right→`goTo`, enter→fire
  `onSubmit`), `handlePointer` DOWN→focus + caret-to-click (measurer hook,
  best-effort index). Multibyte-cursor precision is follow-up, not blocker.
* **Textarea**: multiline insert (enter→`\n`), up/down across line
  boundaries, caret-follow scroll (`scrollY` clamp), fire `onChange`.

## 7. Tests + promotion (both sides, same pattern)

One `<widget>_test.c` per class beside its source (mirror
`darling/label/label_test.c`), wired in `projects/darling/CMakeLists.txt`:

```c
static bool s_fired = false;
static void onFire(void *ctx) { (*(bool*) ctx) = true; }
/* DOWN+UP inside bounds → pressed cleared + fired==true; UP outside → !fired */
```

Checklist row promotes in the SAME commit as its green test. Gallery
behavior unchanged (no painter changes in this wave unless trivial).

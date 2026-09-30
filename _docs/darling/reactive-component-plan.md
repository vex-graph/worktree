# Reactive Component Plan (darling) — every metric observable

Status: **DRAFT for review.** Spans R3 (`graphvex` GraphicsComponent) + R4 (`darling` widgets).

## Goal

Every component metric is a reactive, so setting one auto-updates and repaints with
no extra wiring:

```c
Reactive(Float)  x, y, w, h, cornerRadius, opacity;
Reactive(String) text;
...
Reactive_set(panel->x, 12.0f);   // recompute + repaint, no manual dirty call
```

## Findings

- `Component` **is** graphvex's `GraphicsComponent` (`lang/graphics_component.h`),
  embedded **by value** in every widget (`Panel { Container base; Component component; ... }`).
- The struct carries ~20 float metrics: `x, y, w, h, scaleX/Y, min*/max*, measured*,
  margin*, padding*, borderWidth, cornerRadius, opacity` + ints/enums + the resolved
  currencies (`Transform local`, `abs*`).
- **78 accessors**; the impl lives in `src/component/graphics_component.c`.
- **Every setter already ends in `GraphicsComponent_recompute(self)`** — so the
  recompute point exists; what is missing is the *notification* (a change channel)
  and reactive *storage*.
- Fields are read/written **directly** (`(*self).x`) throughout the impl — that is the
  invasive part.

## Design

A metric is `ReactiveFloat` (the engine + typed channels). Two storage choices:

| | storage | cost | change |
|---|---|---|---|
| **(a) pointer** | `ReactiveFloat *x;` (heap) | one small alloc per metric | `Reactive_set((*self).x, v)` |
| **(b) embedded** | `ReactiveFloat x;` (inline) | ~64 B per metric inline (~1.3 KB/component) | same API |

Recommend **(a)** — `ReactiveFloat *` per metric — because `GraphicsComponent` is
copied by value (view model) and a pointer keeps the struct small; a view can share a
metric or own it knowingly. Recompute-change repaint comes free through the channels.

The accessors stay the public API and become thin reactive wrappers:

```c
float GraphicsComponent_getX(const GraphicsComponent *self) { return Reactive_get((*self).x); }
void  GraphicsComponent_setX(GraphicsComponent *self, float x) {
    if (!self) return;
    if ((*self).minX != 0.0f && x < (*self).minX) x = (*self).minX;
    if ((*self).maxX != 0.0f && x > (*self).maxX) x = (*self).maxX;
    Reactive_set((*self).x, x);          // fires onChanged -> mark tree dirty
    GraphicsComponent_recompute(self);
}
```

The **repaint wiring**: bind `onChanged` on each metric to a per-component
`markDirty(self)` (one line at construction), which fans the parent-ref set — the
existing dirty mechanism — so the compositor re-renders on the next present
(Present-On-Demand Law preserved: a change marks dirty, the owner drains/presents).

**Text** lives on the widget (Label), not the layout record, so `Reactive(String) text`
is a widget-level metric (e.g. `Label { ...; Reactive(String) *text; }`), same pattern.

## Open decisions

1. **Storage: (a) pointer or (b) embedded?** (recommend a)
2. **Scope of the first pass:** the geometry metrics (`x y w h cornerRadius`) only, or
   *all* floats (margins/padding/border/min/max/opacity/scale)?
3. **Resolved currencies stay plain** (`Transform local`, `abs*` are outputs, not
   authored metrics — they should NOT be reactive; they are recompute products).
4. **Colors/enums** (`backgroundColor`, `origin`, `anchor`, ...) — reactive too, or
   plain? (they change rarely; a `Reactive(Double)`/tagged word is possible).

## Slices

1. **Proof** (this cycle): a darling `ReactiveComponent` with `Reactive(Float)` metrics
   + `Reactive(String)` text, proving get/set/observe end-to-end against the repaint
   dirty-flag. No graphvex change yet.
2. **GraphicsComponent storage swap** — metrics become `ReactiveFloat *`; 78 accessors
   rewired to reactive get/set; recompute reads through them. graphvex-first (R3).
3. **Repaint binding** — each component binds its metrics' `onChanged` to `markDirty`.
4. **Widgets** — `Label.text`, `Panel` background/radius, every widget's metrics.
5. **Living docs** — preferences + readiness.

## Risks

- Direct `(*self).x` reads across the impl/tree must ALL move to `Reactive_get` — a
  missed one reads the pointer, not the value (a silent bug), so this wants a
  mechanical sweep + tests.
- The view model aliases payloads by pointer; two views sharing a metric must be
  deliberate (shared reactive = shared observable).

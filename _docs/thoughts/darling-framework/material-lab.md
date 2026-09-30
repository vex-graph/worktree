# Material lab (material viewer/tweaker)

**Idea ("material mover"):** a darling panel set that shows what a material
looks like and lets you move its parameters — albedo, roughness, metallic
(and later emissive/clearcoat) — live on the viewed object. Think:
`ColorPicker` + `Slider` rows bound to a graphvex material, previewed on
the `Object3D`/`Viewer3D` cube. Narrowest useful version: one material,
one preview object, three controls.

## Why separate from the viewer

- **Material state has a different owner.** The viewer owns camera + model
  path; the object owns rotation; the *material* (how light interacts with
  surfaces) belongs to graphvex's future PBR path. A dedicated panel owns
  the material values so viewer/object files never grow lighting fields —
  same part-segregation instinct as Rule 29 (`Class_part_verb`; the
  material is a part with its own verbs, not stray floats on the viewer).
- **Controls already exist as shells.** Albedo is a `ColorSwatch`/
  `ColorPicker`; roughness/metallic are `Slider`s on `[0,1]`; toggles are
  `Switch`es. The lab is mostly *binding* existing widgets to a material,
  not inventing widgets.

## API sketch (not final)

```c
typedef struct MaterialPanel {
    Panel base;
    void *material;      // BORROWED graphvex material handle (null = default gray)
    Object3D *preview;   // BORROWED preview target (usually the viewer cube); detach-only
} MaterialPanel;
// setMaterial (borrowed + dirty) / setPreviewTarget
// Convenience part verbs over the bound material:
//   material_setAlbedo(panel, color) / material_getAlbedo
//   material_setRoughness(panel, v)  // clamped 0..1, Slider law
//   material_setMetallic(panel, v)   // clamped 0..1
```

## Constraints (sized honestly)

1. **No material system exists anywhere yet.** graphvex has no material
   type, no uniform layout, no lit pipeline; darling renders unlit
   (`solid_quad`, `texture_quad`, SDF text). The lab's first version must
   target a *minimal* graphvex material (albedo + roughness + metallic,
   single directional light) — full PBR is explicitly out of scope.
2. **Preview before editor.** An unlit→minimal-lit cube toggle proves the
   pipeline; the slider rows come second. Sliders bound to nothing are
   decoration.
3. **Values are live, not applied-on-OK.** Dragging roughness re-renders
   the preview the same frame (dirty + present-on-demand). Modal apply
   buttons are a later desktop nicety, not the core.

## Sequencing

1. graphvex minimal lit material + one light (cube goes from flat to shaded).
2. `MaterialPanel` shell bound to the preview cube (albedo only).
3. Roughness/metallic `Slider` rows (clamp laws from `Slider`).
4. Preset row (a `ColorSwatch` of 4–6 canned materials) + gallery section.

## Status

Envisioned, not started. Blocked on a graphvex lit path; darling side is
binding work over existing widget shells.

## Next step

Decide the minimal graphvex material struct (albedo + roughness + metallic
+ one light) — everything in this thought hangs off that struct's fields.

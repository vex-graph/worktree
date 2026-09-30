# Drawing app (the input-loop prover)

**Idea (in vexgraph's words):** a drawing application — canvas, brushes,
layers, and strokes on the darling tree. The first full vertical slice:
real input → real pixels → real file.

## Why this one goes first
- **Zero new engine needed.** Everything it touches exists: `Canvas`
  (projection), `Raster`/`Surface` (software pixels), `Picture` (image
  node), `Panel` tree (layers panel, toolbar), `Input`/`Slider`/
  `ColorPicker` shells (brush size, color), `io/file` + `io/bake`
  (save/load).
- **Proves the input loop.** Stylus/mouse down-move-up through
  `Key/Mouse/Touch` pipelines into retained-mode nodes is the exact
  path every later app (DAW automation, IDE caret) reuses. If drawing
  feels right, the loop is right.
- **Layers are Panels.** A layer stack is a `LayeredPanel` with one
  `Picture` child per layer — the new shell earns its keep on day one.
  Undo is a stroke ring (`RingBuffer` with a 50-stroke cap).

## Constraints (sized honestly)
1. Software raster first (`Raster` exists). GPU canvas (`VkSceneCanvas`)
   only when a brush stroke can outrun 60 fps on CPU.
2. Brush engine stays tiny: round stamp + spacing + opacity. Custom
   engines are hotcwap modules later, not now.
3. Formats: PNG via shell-out first, native `.antibake` second
   (`io/bake.c` already writes triangles; teach it quads).

## Sequencing
1. One window + one canvas + one round brush + stroke ring undo.
2. Layers via `LayeredPanel`, color via `ColorPicker` behavior.
3. Save/load (shell-out, then native).
4. Brush modules as hotcwap drivers.

## Status
Envisioned, not started. All substrate present; no stroke path wired.

## Next step
Implement `Button_press` + `Slider` drag behavior (the two input
primitives drawing needs), then open the canvas window.

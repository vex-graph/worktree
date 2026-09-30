# darling-editor (the Figma + Miro spatial whiteboard)

**Idea (in vexgraph's words):** an interactive tool inspired by Figma and Miro — an infinite 2D canvas where you can take notes, draw diagrams, sketch mindmaps, design user interfaces interactively, and export them directly to C code, HTML/CSS, SVGs, or high-res images.

## Why this belongs on the Darling substrate
- **darling-framework is already a scene graph.** It has containers, 9-grid anchors, text, cards, buttons, and custom painters. Building an editor on it dogfoods every widget in the tree.
- **Infinite pan/zoom on Vulkan**: Software canvases hitch when zooming into complex boards. A Vulkan 120Hz canvas with SDF text and baked vector paths zooms infinitely without losing sharpness.
- **SVG baking via Jump Flooding Algorithm (JFA)**: Vector icons and SVG shapes are baked into Signed Distance Fields on the GPU (`sdf_jfa`), allowing infinite non-pixelated scaling at 120fps.
- **Multi-format export**:
  - Export to C23 (`Class(...)` with 9-grid anchors for in-engine UI).
  - Export to HTML/CSS for web wireframes.
  - Export to SVG for vector assets.
  - Export to PNG for presentations and documentation.

## Status
Envisioned. `darling-framework` substrate is live; `../../projects/darling-editor` initialized.

## Next step
Wire the infinite pan/zoom canvas and the icon palette browser (Lucide/Tabler via `api-haven`).

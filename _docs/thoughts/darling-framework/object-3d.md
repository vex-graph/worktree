# Object3D (turntable object node)

**Idea:** a `Panel`-inherited darling node that displays one 3D object.
It can be **rotated but not moved**. Its framing derives from the panel
bounds: the object **fits, never stretches** — uniform scale from
`min(panelW, panelH)`, centered, letterboxed. Aspect is preserved under
any resize with zero re-upload.

## Why a separate node (not just a Scene)

- **Transform separation.** Object rotation (turntable) and scene/camera
  motion (orbit/pan in the viewer) are different operations with different
  owners. Mixing them into one node is how you get 2am bugs where dragging
  the object flings the camera. `Object3D` owns *object* rotation only;
  `Viewer3D` (sibling thought) owns the *scene/camera*.
- **Bounds law.** Like `Picture` (`crop` + fit modes) and `Scene`
  (`STRETCH`/`FIT`/`PIXEL`), the node must survive arbitrary panel sizes
  without distortion. Fit-not-stretch is the contract: compute
  `s = min(w, h) / objectRadius`, scale uniformly, center. Stretch is a
  defect, same as a squished `Picture`.
- **Borrowed mesh.** The GPU mesh lives in graphvex (vertex/index buffers);
  darling holds a borrowed handle, never copies it — same rule as
  `Picture.image` and `Plot.xs/ys`. Caller keeps the mesh alive while
  attached; detach never frees.

## API sketch (darling-idiomatic, not final)

```c
typedef struct Object3D {
    Panel base;          // layout/tree/bg; size = framing input
    void *mesh;          // BORROWED graphvex mesh handle (null = nothing to draw)
    float rotX, rotY;    // object rotation, radians (the ONLY transform)
    bool autoFit;        // true = refit on every resize (default true)
    float fitPadding;    // margin inside panel, 0..1 (default ~0.1)
} Object3D;
// Object3D_0() detached; Object3D_1(parent) attached
// setMesh (borrowed assign + dirty) / setRotation(x, y) / setAutoFit / setFitPadding
// getMesh / getRotation(outX, outY) / isAutoFit / getFitPadding
// No setPosition, no setScale — absent on purpose. Position/scale belong to framing.
```

## Constraints (sized honestly)

1. **Rotate-only is the contract.** No position, no scale, no camera.
   If you need the camera moved, you need `Viewer3D`, not this node.
2. **graphvex owns the mesh first.** Today graphvex has buffers, `Texture`,
   `SdfGpu`, `VkSceneCanvas` — no mesh type, no loader, no draw pipeline
   for indexed geometry. `Object3D` cannot land before a minimal graphvex
   `Mesh` (vertex+index buffers + draw call) exists.
3. **One unlit placeholder path first.** Flat-shaded cube before PBR. The
   material thought (`/Users/vexgraph/CLionProjects/vexgraph/_docs/_thoughts/darling-framework/material-lab.md`) layers lighting on top later.

## Sequencing

1. graphvex minimal `Mesh` + single draw (unlit, one hardcoded cube).
2. `Object3D` shell: struct + accessors + fit framing + rotation.
3. Mesh handle wiring (borrowed) + dirty on rotation/resize.
4. Fit-law proof in gallery (wide/tall/square panels, no stretch).

## Status

Envisioned, not started. Blocked on graphvex `Mesh`; no loader needed yet
(hardcoded cube is enough for the framing proof).

## Next step

Define the graphvex `Mesh` handle (vertex/index buffer ownership + draw
entry) — then `Object3D` becomes a thin framing + rotation shell over it.

# Viewer3D (Blender-style scene shell)

**Idea:** a `Panel`-inherited darling node that hosts a small 3D scene:
a **floor grid at the origin** (the Blender-on-open feeling), a **cube
placeholder** until a model loads, and a model loaded from **`.obj` first,
`.gltf` second** via VFS. It renders through graphvex. Interaction
**rotates and moves only the SCENE (camera/orbit), never the object** —
object posing belongs to `Object3D` (`/Users/vexgraph/CLionProjects/vexgraph/_docs/_thoughts/darling-framework/object-3d.md`).

## Why this shape

- **Grid + cube is the orientation contract.** A lone floating model with
  no ground reference is unreadable at 2am. The grid at `y = 0` answers
  "which way is down, where is the floor" for free; the cube proves the
  pipeline works before any file parsing exists.
- **Camera-vs-object split.** The viewer owns orbit/yaw/pitch/pan/zoom
  (scene transform). The contained object keeps its own rotation
  (`Object3D`). Two transforms, two owners, zero fights.
- **`.obj` before `.gltf` — deliberately.** OBJ is text, single-digit
  parser, no binary chunks, no JSON, no accessors. It proves mesh upload +
  framing + camera with minimum risk. glTF is the real format (binary,
  materials, scenes) and lands second, reusing the same mesh handle.

## API sketch (not final)

```c
typedef struct Viewer3D {
    Panel base;            // viewport; children paint inside (no nested layers)
    Object3D *object;      // BORROWED content slot (null = cube placeholder); detach-only
    char path[...];        // inline model path (VFS uri); empty = placeholder
    bool showGrid;         // floor grid at y=0 (default true)
    float camYaw, camPitch;// scene orbit, radians
    float camDist;         // dolly distance (> 0)
    float panX, panY;      // scene pan in world units
} Viewer3D;
// Viewer3D_0() (grid + cube) / Viewer3D_1(parent)
// setModelPath (VFS resolve + async load + dirty) / clearModel (back to cube)
// setShowGrid / setOrbit(yaw, pitch) / setDistance / setPan
// getModelPath / isShowingGrid / getOrbit / getDistance / getPan
```

## Constraints (sized honestly)

1. **graphvex does the heavy lifting.** Needs: `Mesh` type, OBJ loader
   (graphvex-side, CPU), grid-line pipeline, orbit camera math, placeholder
   cube mesh. darling only owns framing + camera state + dirty.
2. **VFS paths, not raw paths.** Model references go through
   `Vfs_resolve` (`anti://`, `project://`) like fonts — never bare
   filesystem strings baked into the node.
3. **Placeholder is permanent.** Even after loaders land, empty-path must
   still show grid + cube. The placeholder is the loading state, the error
   state, and the test fixture.

## Sequencing

1. `Object3D` framing proof first (sibling thought) — viewer reuses it.
2. Viewer shell: grid + cube + orbit camera, no files.
3. OBJ load via VFS (graphvex parser, borrowed mesh into `object` slot).
4. glTF load (same slot, richer path). Materials arrive via `/Users/vexgraph/CLionProjects/vexgraph/_docs/_thoughts/darling-framework/material-lab.md`.

## Status

Envisioned, not started. Depends on `/Users/vexgraph/CLionProjects/vexgraph/_docs/_thoughts/darling-framework/object-3d.md` framing + graphvex
`Mesh`/camera/grid pipelines, none of which exist yet.

## Next step

Build the grid + cube + orbit shell with no file IO. If orbiting an empty
grid with a cube feels like Blender-on-open, the shell is right — then
teach it OBJ.

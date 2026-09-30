# Depth-driven effects and editor visualizations

**Owner:** R5 anti, consuming shared darling-framework UI and graphvex execution.
**User intent:** blur whose value comes from a scene depth map, such as depth of
field; masks from textures; complex scene/filter composition in the future.

## Simple explanation

Ordinary blur says "blur every pixel by this much." Depth-driven blur says
"look up how far away this pixel is, then decide how much blur it needs."

Pseudocode only, not an API or shader:

```text
blurAmount = mapDepthToBlur(depthImage, focusDistance, maximumBlur)
result = blur(sceneColor, radiusImage = blurAmount)
```

The color image and depth image are different inputs. Define their coordinate
alignment, depth units and camera/depth encoding. Nonlinear hardware depth is
not automatically distance. A channel is data with meaning, not just a number.
Depth-dependent blur is an approximation, not automatically correct depth of
field: foreground/background boundaries can create halos or bleed. Those are
future graphics questions, not reasons to begin 3D work now.

## Editor applications (suggested, not committed features)

Shared plots could inspect frame timings or other numeric diagnostics. Shared
diagrams could edit action/workflow connections. Anti supplies the meanings and
data; darling-framework supplies reusable inspection and interaction behavior.
Do not make the generic chart or filter classes depend on game-specific types.

This extends the existing game vision at:
/Users/vexgraph/CLionProjects/vexgraph/_docs/_thoughts/anti/anti-engine.md

Shared filter scope is recorded at:
/Users/vexgraph/CLionProjects/vexgraph/_docs/_thoughts/darling-framework/element-filter-stacks.md

**Status:** Future R5 use case. No 3D or graphics implementation yet.
**Next step:** revisit only after the UI framework is polished and on-demand;
start with a clearly defined image-input contract rather than many effects.

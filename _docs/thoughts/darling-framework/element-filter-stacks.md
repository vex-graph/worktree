# Element filter stacks

**Owner:** R4 darling-framework (scope and composition contracts).
**User intent:** background filter = stack; text filter = stack; foreground
filter = stack for the WHOLE element. Support blur, texture masks and parameters
whose values come from image pixels. This is a design note, not renderer work.

## Names that say what gets changed

| Suggested scope | Plain meaning |
|---|---|
| Backdrop | Content already behind this element |
| Background | This element's own background |
| Text | This element's text output |
| Element/composite | The assembled element; explicitly decide whether children are included |

The user's "foreground = whole element" intention is preserved as the proposed
**element/composite** scope. Foreground alone can sound like only the top content.
Final names remain open. A backdrop blur and blurring your own background are
not the same operation.

## Stack to the user, dependencies to the implementation

Pseudocode only:

```text
element.backgroundFilters = [blur(radius = 4), mask(texture)]
element.textFilters = [shadow(offset = [1, 1])]
element.elementFilters = [opacity(0.8)]
```

Order matters: blur then mask differs from mask then blur. Define whether mask
uses alpha or a color channel, how sizes/coordinates align, and what happens at
edges. Define color space and premultiplied-alpha handling before visual tests.

Each filter describes its input, output, parameters and extra image inputs.
A parameter can be a constant, an animated/reactive value, or a sampled image
channel. "Use pixel data" must specify which channel, units, mapping and limits.

A list is easy to edit, but auxiliary images create a dependency graph underneath.
Validate missing inputs and cycles. Intermediate filter images are offscreen
resources, NOT extra native window layers. Keep the window's existing layer
contract intact. R3 graphvex owns eventual execution; R4 names UI intent.

## Keep the immediate-on-demand feel

Cache unchanged results. A changed mask invalidates effects that read it, not
all siblings. Blur can affect pixels outside the original dirty rectangle, so
filters declare their read radius/output extent. Backdrop effects also depend on
changes behind the element. Explicit dependencies prevent stale cached results.
Bound work and resource use; an unrestricted stack can be very expensive.

See the game-specific depth-map example in
/Users/vexgraph/CLionProjects/vexgraph/_docs/_thoughts/anti/depth-driven-effects.md.

**Status:** Parked contract; no graphics or shader implementation authorized here.
**Next step:** settle scope, child inclusion, effect order and invalidation rules
on paper after ordinary UI layout/focus/text behavior is dependable.

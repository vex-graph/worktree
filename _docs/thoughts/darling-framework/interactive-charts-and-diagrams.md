# Interactive plots, graphs and diagrams

**Owner:** R4 darling-framework (shared UI toolkit), not the darling editor app.
**User intent:** line graphs, scatter plots, histograms, bar graphs and diagrams;
hover a cursor to see data, and simple ways to filter what is shown.
**Status:** Thoughts only. API names below are pseudocode, not existing functions.
Graphics implementation waits until the ordinary UI feels polished and on-demand.

## Plain-language model

- **Data:** the values we have.
- **Series:** one group of related values, such as temperature over time.
- **Scale:** how a value becomes a position on an axis.
- **View range:** the part of the data space we are looking at.
- **Selection:** the points the user chose.
- **Data filter:** a rule deciding which records participate.

A chart is axes + scales + series + labels + interaction. Prefer composition:
a chart can hold a line series and scatter points together. Public convenience
classes such as LineGraph and ScatterPlot remain possible; do not settle an
inheritance tree before mixed-series behavior is understood.

| View | Meaning |
|---|---|
| Line graph | Ordered samples joined together; define whether input order or sorted X wins |
| Scatter plot | Independent points, optionally with size or color values |
| Histogram | Measurements counted into numeric bins |
| Bar graph | Categories and their values; categories are not histogram bins |
| Diagram | Nodes, ports and connections; a different data model from a chart |

## Hover: "what am I looking at?"

Hover should return a small hit result: series identity, stable item identity,
source values, units and screen anchor for the tooltip. No hit means no tooltip.
Examples: a scatter point's X/Y, a bar's category/value, a histogram bin's range
and count. A line may show the nearest sample or an interpolated value; label
interpolation clearly instead of presenting it as a measured sample.

Best practices:
- Use a small screen-space hit radius, not an exact pixel match.
- Convert coordinates through the scale, including log scales, pan and zoom.
- Define overlap rules for coincident points and show which series was picked.
- Preserve stable data identities when filtering/reordering, not array positions.
- Define whether masked-out points can be hit; default to visible points only.
- Support keyboard focus and an inspectable data table; hover cannot be the only
  way to read values. Touch needs tap/selection rather than hover.
- Tooltips normally repaint only their overlay, not recalculate all chart data.

## Three different "filters"

These are illustrative pseudocode, not C or promised APIs:

```text
chart.setDataFilter(x between 0 and 10 AND y >= 5)
chart.setViewRange(x = [0, 10], y = [0, 100])
chart.setVisualFilters(blur(radius = 2))
```

The first chooses records. The second changes the camera on the chart without
removing records. The third changes appearance. They must not share one vague
setFilter(x, y) operation.

For simple numeric cases, offer explicit X/Y ranges. For more complex cases,
use a filter description that names the field, operation and value. Decide if
multiple rules combine with AND or OR; do not guess from argument order.

```text
filter = allOf(range("time", 0, 10), atLeast("temperature", 5))
chart.setDataFilter(filter)
chart.clearDataFilter()
```

This description is easier to inspect, save and edit than an opaque callback.
A callback predicate may still be useful for advanced local use, with explicit
lifetime/thread rules. Do not mutate source data just to hide a point.

Specify inclusive/exclusive range ends, missing values and NaN behavior. Reject
invalid ranges and report an empty result clearly. Choose whether axes stay
fixed or auto-fit filtered values; make it a setting to avoid surprise jumps.
For histograms decide whether bin edges remain fixed after filtering. Filtering
before aggregation and filtering the displayed bins are different operations.

## Interaction beyond hover

Pan, zoom, reset view, select one item, drag a selection rectangle, and optional
linked selection between views. Keep hover, selection and data filtering separate:
hovering should not silently change which rows count. Provide clear-selection
and reset-filter actions. Changing a filter should not destroy the selection's
source identities; define how hidden selected items are represented.

For large datasets, cache suitable hit-test indexes and invalidate them with data
or view changes. Downsample only the drawing when necessary; preserve truthful
inspection of original samples or explicitly label aggregates. Cancel stale
background filter work so old results cannot overwrite a newer request.

## Diagrams

Share node/edge/port selection, dragging, connection hit testing and labels.
Workflow/opcode editors consume this model; the diagram widget does not execute
scripts. Domain validation belongs to the application or language subsystem.

## On-demand behavior

A pointer move may change a hover overlay, not the dataset. New samples update
the series; range changes update transforms; filter changes update derived data.
Coalesce notifications, but do not drop real samples merely because only the
latest UI notification is needed. UI changes happen on the UI owner thread.

**Status:** Parked proposal; no charts or diagram APIs added.
**Next step:** choose one small scatter plot with hover, range filtering and
reset, and write data/interaction tests before a rendering implementation.

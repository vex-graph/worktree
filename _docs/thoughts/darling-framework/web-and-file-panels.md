# Web panels + native file dialogs — parked design

**Status:** `;;DRAFT` — R4 (darling-framework) work, parked until the R2
primitives layer (signal/coalesced change, deferred queue, action registry)
lands. Nothing here is built. Picked from a conversation; parked verbatim
so nothing evaporates.

Core instinct: **the OS does the heavy lifting, we compose.** No bundling
by default. Panels are pixels inside OUR window; dialogs ride the existing
modal glue.

---

## 1. The core tension: "headless browser as a panel"

A browser is only a *panel* (pixels composited inside our window) if the
OS exposes an **embedding API**. You cannot grab an arbitrary installed
Chrome and composite its pixels — Chrome does not expose its renderer.
So the three subclasses split into two capability classes:

| Subclass | Backing | Embeds in our window? | Ships with OS? |
|---|---|---|---|
| **NativeWebPanel** | WKWebView (macOS), WebView2 (Windows), WebKitGTK (Linux) | Yes — true compositing layer | Effectively yes |
| **WebKitPanel** | System WebKit directly | Yes | Apple only |
| **ChromiumPanel** | Bundled CEF/Chromium | Yes | No (heavy) |

Verdict: **NativeWebPanel is the prize** — a system web view exists on
all three majors, so zero bundling covers ~all real demand.

"Use the user's installed browser instance" has only two weaker modes:

- **External handoff** — open the URI in their browser. A launcher, not a panel.
- **CDP puppeteering** — launch their Chrome headless, drive it over the
  DevTools protocol (api-haven's WS stack), blit frames into a panel.
  Possible, but high-latency, fragile across versions, painful input.
  Park as a research experiment, NOT a pillar.

## 2. R-rank placement (the Vertical Integration Law)

| Piece | Rank | Why |
|---|---|---|
| `BrowserProbe` / `BrowserBroker` — installed-browser discovery (bundle IDs on macOS, registry `App Paths` on Windows, `.desktop` scan on Linux) | **R3 api-haven** | Pure connector/catalog surface, same shape as `AppBroker`/`DbProvider`. Reports kind/version/path as DATA; never windows |
| `WebPanel` contract + `NativeWebPanel` OS backends | **R4 darling-framework** | Panel-derived; under the Window Board Root Lock Law it locks to the window as contentPane and the web content fills the board |
| `ChromiumPanel` (CEF) | R4, deferred | Bundling is a packaging decision. Keep the slot, defer the dependency |
| `FileDialog` / `NativeFileDialog` | **R4 darling-framework** | NSOpenPanel / IFileOpenDialog / GTK chooser |

R5 consumes both (semicolon xlsx viewer, anti UI). The probe result is a
descriptor struct, never a live handle — same pattern as `DbSqliteFile`.

## 3. Design notes (save-pain list)

1. **WebPanel as a slot registry, not an API soup** — mirror the
   `WindowEvent` pattern: nullable event slots (`onNavigate`,
   `onTitleChanged`, `onLoadFinished`, `onCrashed`), fire dispatchers on
   Thread 0, null slot = no-op. A web panel is ANOTHER compositing layer in
   the 2-VkImage board system (the Window Compositing Layer Order Law);
   keyboard focus routes through the key gate, never straight to the web view.
2. **FileDialog is async with callbacks, never blocking** — a modal that
   blocks Thread 0 freezes the pump (the Bounded Wait Law).
   `FileDialog_open(dialog, onChosen, userdata)` shape, dest-last.
   Sheet/parented modal on macOS, owned dialog on Windows; anchors to the
   existing child-window + key-gate modal glue.
3. **Single Class Per File Law** — WebPanel, NativeWebPanel, ChromiumPanel,
   FileDialog, NativeFileDialog: one `.h/.c` pair each, backend selected at
   build time per OS (exactly like the window backends), never runtime swap.

## 4. Build order when unparked

1. `FileDialog`/`NativeFileDialog` — small, self-contained, no compositor
   entanglement, modal glue already exists. First R4 win.
2. `WebPanel` contract + `NativeWebPanel` macOS backend — the lift is a new
   layer type in the compositing order, so it waits for the R2 dispatch
   layer (dirty flags + coalescing) to exist.
3. `BrowserProbe` in api-haven whenever (pure catalog, no coupling).
4. `ChromiumPanel` + CDP mode — only when something truly needs it.

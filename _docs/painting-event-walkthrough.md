# Coalesced painting event — walkthrough

## What changed

- `graphvex`: added a per-client `Repaint` ticket, consumed before presentation. Multiple requests ahead of a paint become one pass; requests during the present hook remain for one further pass. Failed presents re-arm the ticket. The demand loop still owns the bounded park and its thread-safe wake.
- `darling-framework`: each `Frame` owns its ticket. `Frame_requestRepaint(frame)` is the producer-facing, thread-safe request **and** wake; `Frame_markDirty` routes mouse/window/content changes through that path. Producers must stop or join before `Frame_free`.
- `vk_test`: the existing reactive worker now requests a frame repaint directly after writing its value, without a worker-side registry lookup or a polling probe. `scroll_probe` remains a separate executable, using `Frame_markDirty` for input.
- AppKit's synchronous resize paint queues a retry only if the immediate paint fails, rather than queuing an extra paint after success.
- Live rendering follow-up: the seam's `CAMetalLayer` now uses `presentsWithTransaction = NO`. With `YES`, wheel input advanced ScrollScene and Vulkan reported successful presents, but the on-screen drawable stayed stale until a window-state/resize transaction. Vulkan `vkQueuePresentKHR` must publish the on-demand drawable without requiring a Core Animation property-change transaction.

## Verification

- Built `graphics_loop_test`, `frame_test`, `vk_test`, and `scroll_probe` with their `-Wall -Wextra -Werror` targets in `build-verify`.
- Passed `graphics_loop_test` (batching, mid-paint request, failed-present retry, worker wake), `frame_test` (Frame-to-event wiring), `scroll_panel_test`, `scroll_scene_tick_test`, `scroll_scene_cull_test`, and `scroll_scene_vulkan_test`.
- `git diff --check` passed in `graphvex` and `darling-framework`. No commits or pushes.
- Reproduced the live issue by posting macOS wheel events: `PROBE_INPUT_TRACE` showed page offsets moving while captured ScrollPanel pixels stayed unchanged. After removing transaction gating, a captured content-only scroll visibly changed the ScrollPanel rows. This was a local live-window check, not a claim about every display configuration.

## Boundary / follow-up

This adds the scheduling event, not automatic widget-to-Frame subscription. A reactive producer must request a repaint from its live Frame after updating state. The previously deferred question of **visible text-label refresh** is not claimed resolved here; it needs a separate assessment. The loop's bounded park still services OS events periodically when no producer fires.

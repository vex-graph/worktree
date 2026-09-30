# Preferences contract cleanup — walkthrough

## Changed

- Consolidated Git workflow and hardcoding/scalability ownership in the canonical preferences; a named default is user/application-adjustable unless an inherently fixed value has a stated reason. Reconciled the shipped M1 baseline with runtime-gated newer capabilities and aligned test placement with `tests/`.
- Kept `;;OVERVIEW` and `;;DEFINITION` as readable, current class maps; retired mandatory empty registry categories and exact source-banner templates, without deleting existing overviews.
- Clarified that `;;CHECKER` and `;;HOTCODE` are compile-time markers, not runtime validation or proof. Recoverable Vexspoke `THROW` remains loud and safe-returning; Hotcwap's fatal macro is now named `FATAL_THROW` (no production macro callers were found). Synchronous stderr may block and cannot diagnose a segfault preceding the check.
- Wired a bounded diagnostic/container CTest slice in the independent tests checkout, added a Vexspoke test that captures stderr and checks a normal no-report path, and made the Hotcwap test assert its fatal banner and exit status in a child with a timeout. Updated test-repo README and lawbook. All other existing test sources and worktree changes remain untouched.

## Verification

- Isolated macOS Debug and Release configurations, both with `-Wall -Wextra -Werror`: `throw_test`, `throwable_test`, `array_test`, and `collection_test` compiled and passed (4/4 CTest cases in each configuration).
- Canonical Index: 27 titles match 27 full-law headings; changed repository diffs passed `git diff --check`.
- This is **not** a release-wide proof gate: current root CTest discovers 18 named tests, while numerous test-repo sources remain unwired or untracked and sanitizer/platform/concurrency coverage is incomplete. No claim of full green status or production-wide absence of THROW is made.
- No commits or pushes were made. The independent repositories already had substantial user work in progress before this slice.

# Preferences contract cleanup — implementation plan

## Background

The canonical preferences repeat Git and hardcoding rules, disagree about the portable CPU baseline and test source location, and require a full eight-part blueprint few active files use. The independent `tests/` repository has many test sources but its aggregate runs only nine Graphvex tests; umbrella CTest discovers none. Vexspoke's recoverable `THROW` and Hotcwap's fatal same-named `THROW` have different contracts.

## Changes by component

- **Canonical Vexspoke preferences:** make Git Workflow the single owner of commit scope and push permission; merge hardcoding/scalability around named, adjustable defaults and explicit immutable exceptions; retain flat storage + OO APIs without repeating their owning rules; make Living Documentation the single owner of freshness. Preserve `;;OVERVIEW` and `;;DEFINITION` as navigational aids, while removing the rarely-used mandatory eight-way registry/body template. State a portable build minimum separate from gated newer features. Align test placement with tracked `tests/` sources. Specify that production rejects unsafe inputs safely and reports detected cold failures; tests and sanitizers catch failures that do not reach diagnostics.
- **Tests repository + umbrella CMake:** register a small, explicit diagnostic smoke set as actual tests before claiming broader coverage. Assert Vexspoke reporting and no-report normal path; test Hotcwap fatal behavior separately. Keep all pre-existing staged/unstaged tests untouched. Do not treat missing or unwired cases as passing.
- **Hotcwap:** give its process-terminating diagnostic a distinct public spelling from Vexspoke's recoverable `THROW`. Update its owning test and explanatory overview; preserve its existing fatal behavior until separately redesigned.
- **Repo-local docs / workspace guidance:** update only references affected by the changed universal titles or test contract. No broad source-tree migration.

## Trade-offs and open boundaries

- Tests cannot replace runtime validation of untrusted input or guard against a segfault that precedes `THROW`. Release strips optional debug instrumentation, not the minimum safety checks.
- `;;CHECKER`/`;;HOTCODE` are compile-time no-op markers today; deleting them is not a release optimization. Their future use is separate from the runtime diagnostic contract.
- The Hotcwap fatal API is a distinct operation, not an implementation of recoverable `THROW`. Avoid a mechanical rename of untraced clients.
- Do not claim all ~174 test sources run until each has a wired target and executable evidence. Do not stage the already-dirty tests checkout wholesale.

## Verification

1. Validate the canonical Markdown index matches its law headings and that retired titles appear only in historical maps.
2. Configure an isolated build; compile changed diagnostic and test targets with `-Wall -Wextra -Werror`.
3. Run the registered diagnostic smoke tests and verify explicit counts; check both Debug and Release paths where feasible.
4. Run `git diff --check` per changed independent repository and report any missing build/test coverage honestly. Do not push.

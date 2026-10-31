# Ecosystem test checklist

Generated test report maintained by `python3 tools/test_checklist.py`.
Governed by the **Timestamped Test Checklist Law** in `PREFERENCES.md`.

- ✅ = an automated lab check passed for this exact file hash, in its stated scope.
- ❌ = untested, failed, skipped, or stale; see evidence. This is not a battle-tested claim.
- Last checked is actual Unix time: integer seconds since 1970-01-01T00:00:00Z.
  `—` means never checked. Estimates must never be recorded as executed evidence.
- The hash identifies the tested content. A file change invalidates a previous ✅;
  the old timestamp/evidence remains visible until the next executed check.
- The ledger tracks **executable tests only**: compilable/runnable test sources
  (`*_test.c/.m/.rs/.py/.ts`), registered runner scripts (`run.py`, `*_run.py`) and
  the shared test harness (`test_support.h`). Markdown, documentation, images,
  configuration and production source are deliberately excluded — a row exists
  to record a test that can actually run, not a file that never executes.
  This report alone is excluded to avoid a self-referential hash. A subsystem
  with no inventoried test is untested, not exempt.
- An integration pass only applies to explicitly named subjects and scope.
  Neither test-file presence nor a passing build proves every framework file.
- Platform gaps and omitted cases must be stated in the evidence/scope column.
- Visual appearance, interactive demos, and subjective approval are not tested
  by this ledger. The user performs visual checks and reports what is broken.
  Automated assertions (including numeric/pixel oracles) are lab evidence only,
  never visual approval. Do not launch galleries or manual demos to earn ✅.
- Descriptions explain the check; no author, agent name, or session ID is stored.

## Commands

```sh
python3 tools/test_checklist.py sync   # inventory executable tests; invalidate stale greens
python3 tools/test_checklist.py check  # reject missing rows or stale results
# Execute the test first, then record its executed test file:
python3 tools/test_checklist.py run --file tests/tools/test_checklist_test.py -- python3 -B tests/tools/test_checklist_test.py
```

`run` records only inventoried executable test files; naming a documented or
production file is rejected because those are not runnable tests.

`run` propagates failures; exit 77 is recorded as skipped, never green.
Add repeated `--file` arguments only for files actually exercised by the command.
Use `--scope` to describe proof limits, platform and gaps. A syntax check is only
syntax evidence, not runtime or full contract verification. Agents must read this
report before working and update affected rows in the same work cycle.
Use `--description` for a short explanation. Only `--kind lab` is recordable;
`--kind visual` is rejected before execution. Visual reports belong to the user.
Do not hand-edit generated tables; add files/tests and use `sync` or `run`.

## vexgraph-ecosystem/anti

No inventoried files yet; not verified.

## vexgraph-ecosystem/darkbase/darkbase-engine

No inventoried files yet; not verified.

## vexgraph-ecosystem/darkbase/darkbase-headless

No inventoried files yet; not verified.

## vexgraph-ecosystem/darling-framework

No inventoried files yet; not verified.

## vexgraph-ecosystem/determinant

No inventoried files yet; not verified.

## vexgraph-ecosystem/drawling

No inventoried files yet; not verified.

## vexgraph-ecosystem/graphvex

No inventoried files yet; not verified.

## vexgraph-ecosystem/impedance

No inventoried files yet; not verified.

## vexgraph-ecosystem/language

No inventoried files yet; not verified.

## vexgraph-ecosystem/lifetime

No inventoried files yet; not verified.

## vexgraph-ecosystem/relational-engine

No inventoried files yet; not verified.

## vexgraph-ecosystem/samplerate

No inventoried files yet; not verified.

## vexgraph-ecosystem/semicolon

No inventoried files yet; not verified.

## vexgraph-ecosystem/sesh

No inventoried files yet; not verified.

## vexgraph-ecosystem/tests

### `vexgraph-ecosystem/tests`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/test_support.h` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/api-haven`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/api-haven/ai_chat_sisters_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/api-haven/ai_provider_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/api-haven/ai_sse_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/api-haven/app_broker_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/api-haven/asset_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/api-haven/db_provider_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/api-haven/db_sqlite_file_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/api-haven/harness_run_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/api-haven/haven_ws_fanout_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/api-haven/json_flex_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/api-haven/mcp_server_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/api-haven/probe_consumer_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/api-haven/webhook_loopback_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/api-haven/ws_binding_run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/api-haven/ws_source_binding_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/api-haven/api`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/api-haven/api/rest_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/api-haven/storage`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/api-haven/storage/snapshot_io_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/b`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/b/arduino_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/b/blueprint_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/b/box_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/b/box_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/b/cli_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/b/cmake_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/b/cpp_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/b/html_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/b/inspect_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/b/javascript_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/b/npm_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/b/objc_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/b/php_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/b/preferences_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/b/readme_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/b/shell_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/b/sql_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/b/swift_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/b/typescript_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/b/util_test.c` | ✅ | 1793373060 | f8df889116da29449e5fff70292bbe16c6068656f3b48839b647c8c5a633dde9 | ['sh', '-c', 'python3 vexgraph-ecosystem/tests/b/util_test.py']; darwin-arm64, debug, ASan+UBSan; standalone b utility owner via its Python harness; other targets not exercised | Repaired the harness to the two-root layout: owner source util/util.c and the b/util plus R0 platform include roots | passed |
| `vexgraph-ecosystem/tests/b/util_test.py` | ✅ | 1793373060 | b87dd2ff6c8b01228422ef94e251f7c093307b4512161c3a2d82faea4624ebb5 | ['sh', '-c', 'python3 vexgraph-ecosystem/tests/b/util_test.py']; darwin-arm64, debug, ASan+UBSan; standalone b utility owner via its Python harness; other targets not exercised | Repaired the harness to the two-root layout: owner source util/util.c and the b/util plus R0 platform include roots | passed |
| `vexgraph-ecosystem/tests/b/workspace_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/b/adapters`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/b/adapters/adapter_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/b/adapters/cargo_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/b/adapters/glsl_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/b/adapters/go_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/b/adapters/lua_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/b/adapters/metal_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/b/adapters/workspace_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/b/adapters/zig_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/darkbase-engine`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/darkbase-engine/run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/darkbase-engine/database`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/darkbase-engine/database/database_result_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/darkbase-engine/database/database_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/darkbase-engine/database/run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/darkbase-engine/oop`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/darkbase-engine/oop/modifier_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/darkbase-engine/page`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/darkbase-engine/page/page_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/darkbase-engine/store`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/darkbase-engine/store/run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/darkbase-engine/store/store_adversarial_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/darkbase-engine/store/store_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/darkbase-engine/util`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/darkbase-engine/util/crc32_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/darkbase-engine/wal`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/darkbase-engine/wal/wal_test.c` | ✅ | 1793370538 | e32076f05fe9c098a0338c58e026066eac0411a84f7674ddc0aaf5dbac8bb271 | ['sh', '-c', './tools/b build wal_test && ./.b/out/debug/bin/wal_test']; darwin-arm64, debug; WAL owner behavior on current host | Runs the WAL owner test after normalizing its Windows branches; other targets remain untested here. | passed |

### `vexgraph-ecosystem/tests/darkbase-headless`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/darkbase-headless/protocol_run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/darkbase-headless/protocol`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/darkbase-headless/protocol/headless_protocol_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/darkbase-headless/service`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/darkbase-headless/service/service_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/darling/capture`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/darling/capture/ui_clip_restore_battle_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/darling/capture/ui_clip_scope_battle_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/darling/capture/ui_multiple_masks_pixels_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/darling/capture/ui_nested_clip_battle_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/darling/capture/ui_rounded_clip_battle_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/darling/capture/ui_rounded_hit_battle_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/darling/color`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/darling/color/ui_border_pixels_battle_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/darling/color/ui_visual_state_pixels_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/darling/compositor`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/darling/compositor/gallery_photo_test.c` | ✅ | 1793370496 | a6fcb60cdc47fb341fea3892e73e6424d6759183af0e341d202c56564198ab96 | ['sh', '-c', './tools/b build gallery_photo_test && ./.b/out/debug/bin/gallery_photo_test']; darwin-arm64, debug; Darwin image decode and resource lookup | Darwin image decode and resource lookup; current host only | passed |

### `vexgraph-ecosystem/tests/darling/cursor`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/darling/cursor/set_cursor_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/darling/drawable`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/darling/drawable/picture_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/darling/event`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/darling/event/event_invoke_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/darling/event/event_kinds_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/darling/frame`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/darling/frame/borderless_frame_test.c` | ✅ | 1793371073 | 84ea715faece544e9608ce92e03ffb3bd8ffaff1dc038be5bddc382c1a9341fa | ['sh', '-c', './tools/b build borderless_frame_test &gt;/dev/null 2&gt;&1 && ./.b/out/debug/bin/borderless_frame_test']; darwin-arm64, debug; re-executed after the delegate hand-back; other targets not exercised | Darwin borderless chrome; re-run passes | passed |
| `vexgraph-ecosystem/tests/darling/frame/frame_application_lifecycle_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/darling/frame/frame_fps_focus_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/darling/frame/frame_live_resize_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/darling/frame/frame_resize_test.c` | ✅ | 1793371070 | 8b61908ed5baa1f6339723621b3290b2016afc424e0eba41d142b88b0998cd0a | ['sh', '-c', './tools/b build frame_resize_test &gt;/dev/null 2&gt;&1 && ./.b/out/debug/bin/frame_resize_test']; darwin-arm64, debug; re-executed after the delegate hand-back; other targets not exercised | Darwin resize behavior; re-run passes | passed |
| `vexgraph-ecosystem/tests/darling/frame/frame_test.c` | ✅ | 1793371068 | 3f9ab7e5a162d167bbcbd4c5a4123752720ee7262117757c7a336c0242d471b8 | ['sh', '-c', './tools/b build frame_test &gt;/dev/null 2&gt;&1 && ./.b/out/debug/bin/frame_test']; darwin-arm64, debug; re-executed after the delegate hand-back; other targets not exercised | Darwin frame behavior; re-run passes | passed |
| `vexgraph-ecosystem/tests/darling/frame/liquid_glass_frame_test.c` | ✅ | 1793370484 | f3da27a639420a8b06e93dff4b506ece6bef6f51ec26817ad1d836370011f620 | ['sh', '-c', './tools/b build liquid_glass_frame_test && ./.b/out/debug/bin/liquid_glass_frame_test']; darwin-arm64, debug; Darwin liquid glass chrome; OS support and GUI surface are host-limited | Darwin liquid glass chrome; OS support and GUI surface are host-limited; current host only | passed |
| `vexgraph-ecosystem/tests/darling/frame/naked_frame_test.c` | ✅ | 1793371077 | 2222125adfcc4ffac4ac19efce46f92c0b8647bb2ca09354c0a44266277aa2e1 | ['sh', '-c', './tools/b build naked_frame_test &gt;/dev/null 2&gt;&1 && ./.b/out/debug/bin/naked_frame_test']; darwin-arm64, debug; re-executed after the delegate hand-back; other targets not exercised | Darwin naked frame chrome; re-run passes | passed |
| `vexgraph-ecosystem/tests/darling/frame/traffic_light_frame_test.c` | ✅ | 1793371080 | ace0304f864f61e6eb3b65a9f8550eb180abfd7f5a9a72c843e800662403125c | ['sh', '-c', './tools/b build traffic_light_frame_test &gt;/dev/null 2&gt;&1 && ./.b/out/debug/bin/traffic_light_frame_test']; darwin-arm64, debug; re-executed after the delegate hand-back; other targets not exercised | Darwin traffic light chrome; re-run passes | passed |
| `vexgraph-ecosystem/tests/darling/frame/ui_matryoshka_battle_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/darling/frame/ui_revalidate_cascade_battle_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/darling/frame/ui_wide_tree_battle_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/darling/kinematics/anchor`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/darling/kinematics/anchor/ui_anchor_pivot_pixels_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/darling/kinematics/pivot`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/darling/kinematics/pivot/ui_size_limits_pixels_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/darling/panel/panel`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/darling/panel/panel/panel_add_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/darling/panel/panel/panel_anchor_corner_radius_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/darling/panel/panel/panel_corner_radius_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/darling/panel/panel/panel_events_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/darling/panel/panel/panel_matryoshka_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/darling/panel/panel/panel_shadow_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/darling/panel/panel/panel_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/darling/panel/scrollpanel`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/darling/panel/scrollpanel/scroll_panel_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/darling/panel/scrollpanel/ui_scroll_capture_battle_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/darling/panel/shared`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/darling/panel/shared/ui_element_contract_battle_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/darling/properties`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/darling/properties/properties_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/darling/scaffold`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/darling/scaffold/scaffold_lab_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/determinant`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/determinant/run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/determinant/cli`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/determinant/cli/command_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/determinant/cli/commandparser_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/determinant/cli/commandregistry_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/determinant/cli/logcommands_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/determinant/cli/output_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/determinant/cli/scanner_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/determinant/events`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/determinant/events/terminal_input_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/determinant/format`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/determinant/format/terminal_color_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/determinant/ui/app`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/determinant/ui/app/terminal_app_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/determinant/ui/button`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/determinant/ui/button/terminal_button_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/determinant/ui/code`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/determinant/ui/code/terminal_code_editor_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/determinant/ui/code/terminal_code_view_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/determinant/ui/compositor`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/determinant/ui/compositor/terminal_compositor_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/determinant/ui/field`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/determinant/ui/field/terminal_input_line_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/determinant/ui/field/terminal_text_area_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/determinant/ui/image`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/determinant/ui/image/terminal_image_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/determinant/ui/list`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/determinant/ui/list/terminal_list_view_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/determinant/ui/markdown`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/determinant/ui/markdown/markdown_action_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/determinant/ui/markdown/markdown_callout_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/determinant/ui/markdown/markdown_code_block_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/determinant/ui/markdown/markdown_inline_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/determinant/ui/markdown/markdown_table_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/determinant/ui/markdown/markdown_text_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/determinant/ui/markdown/markdown_theme_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/determinant/ui/markdown/terminal_markdown_view_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/determinant/ui/panel`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/determinant/ui/panel/terminal_anchor_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/determinant/ui/panel/terminal_frame_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/determinant/ui/panel/terminal_panel_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/determinant/ui/scroll`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/determinant/ui/scroll/terminal_scroll_glide_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/determinant/ui/surface`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/determinant/ui/surface/terminal_canvas_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/determinant/ui/surface/terminal_reload_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/determinant/ui/surface/terminal_surface_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/determinant/ui/surface/terminal_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/determinant/ui/text`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/determinant/ui/text/terminal_breadcrumb_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/determinant/ui/text/terminal_status_bar_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/determinant/ui/text/terminal_text_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/determinant/ui/text/terminal_text_view_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/determinant/ui/theme`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/determinant/ui/theme/terminal_appearance_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/determinant/ui/tree`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/determinant/ui/tree/terminal_tree_view_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/func`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/func/readme_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/func/run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/func/src`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/func/src/func_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/graphvex`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/graphvex/board_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/graphvex/element_property_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/graphvex/element_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/graphvex/image_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/graphvex/compositor`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/graphvex/compositor/color_pass_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/graphvex/compositor/compositor_image_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/graphvex/compositor/compositor_scope_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/graphvex/compositor/compositor_submit_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/graphvex/compositor/compositor_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/graphvex/compositor/filter_gallery_fixture_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/graphvex/compositor/filter_pool_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/graphvex/compositor/gpu_scope_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/graphvex/filter`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/graphvex/filter/filter_functions_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/graphvex/filter/filter_type_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/graphvex/graphics`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/graphvex/graphics/capture_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/graphvex/graphics/graphics_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/graphvex/graphics/image_runs_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/graphvex/graphics/render_loop_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/graphvex/graphics/viewport_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/graphvex/lang`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/graphvex/lang/filter_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/graphvex/nio`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/graphvex/nio/pool_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/graphvex/nio/property_pool_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/graphvex/ui`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/graphvex/ui/element_bounds_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/graphvex/ui/element_image_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/graphvex/vulkan`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/graphvex/vulkan/clip_rounded_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/graphvex/vulkan/gpu_render_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/graphvex/vulkan/pipeline_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/graphvex/vulkan/resize_clip_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/graphvex/vulkan/sampled_image_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/graphvex/vulkan/surface_gpu_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/graphvex/vulkan/surface_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/graphvex/vulkan/vk_batch_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/graphvex/vulkan/vk_renderer_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/harness`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/harness/run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/harness/space`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/harness/space/channel_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/harness/space/message_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/harness/space/model_user_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/harness/space/space_arity_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/harness/space/support_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/harness/space/task_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/hotcwap/hot`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/hotcwap/hot/cold_update_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/hotcwap/hot/cold_update_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/hotcwap/hot/hot_behavior_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/hotcwap/hot/hot_retire_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/hotcwap/hot/hot_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/hotcwap/hot/hot_trampoline_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/hotcwap/hot/ledger_test.c` | ✅ | 1793370499 | 7588d62d0b6134c503669afd658ecf5c1aed88f900522ec0e1cf4dd6e5f05d65 | ['sh', '-c', './tools/b build ledger_test && ./.b/out/debug/bin/ledger_test']; darwin-arm64, debug; Install ledger behavior on Darwin arm64 | Install ledger behavior on Darwin arm64; current host only | passed |
| `vexgraph-ecosystem/tests/hotcwap/hot/loader_trust_test.c` | ✅ | 1793370502 | e0967e266f5f71589cefd1e04e8b01586e416981c5ca3d44a173d23dd160958d | ['sh', '-c', './tools/b build loader_trust_test && ./.b/out/debug/bin/loader_trust_test']; darwin-arm64, debug; Loader path trust boundary on Darwin arm64 | Loader path trust boundary on Darwin arm64; current host only | passed |
| `vexgraph-ecosystem/tests/hotcwap/hot/manifest_adversarial_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/hotcwap/hot/manifest_hot_test.c` | ✅ | 1793370505 | b07b1f9f8cb449d868ab3287ecf27f0ddb7271c34d5cb21491ede6b08de494f0 | ['sh', '-c', './tools/b build manifest_hot_test && ./.b/out/debug/bin/manifest_hot_test']; darwin-arm64, debug; Manifest reload lifecycle on Darwin arm64 | Manifest reload lifecycle on Darwin arm64; current host only | passed |
| `vexgraph-ecosystem/tests/hotcwap/hot/manifest_rollback_test.c` | ✅ | 1793370508 | 117470f2f699f866f4f2e5e6069ac19215f3d7fe237f486d1dd7022a20e3c5fa | ['sh', '-c', './tools/b build manifest_rollback_test && ./.b/out/debug/bin/manifest_rollback_test']; darwin-arm64, debug; Manifest rollback on Darwin arm64 | Manifest rollback on Darwin arm64; current host only | passed |
| `vexgraph-ecosystem/tests/hotcwap/hot/manifest_uninstall_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/hotcwap/hot/retire_ring_overflow_test.c` | ✅ | 1793370515 | 9ef2efad357087fd4054609738ca09ed436c810c8c08ec112120a7cf0147cd45 | ['sh', '-c', './tools/b build retire_ring_overflow_test && ./.b/out/debug/bin/retire_ring_overflow_test']; darwin-arm64, debug; Retire ring behavior on Darwin arm64 | Retire ring behavior on Darwin arm64; current host only | passed |
| `vexgraph-ecosystem/tests/hotcwap/hot/shutdown_order_test.c` | ✅ | 1793370520 | 32c3a3395f7c1ae8fae24bb9b33efaf4cc895cf91c2796725185606da89cdec5 | ['sh', '-c', './tools/b build shutdown_order_test && ./.b/out/debug/bin/shutdown_order_test']; darwin-arm64, debug; Shutdown ordering on Darwin arm64 | Shutdown ordering on Darwin arm64; current host only | passed |
| `vexgraph-ecosystem/tests/hotcwap/hot/throwable_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/hotcwap/hot/two_dylib_swap_test.c` | ✅ | 1793370523 | 1a226ac88343ccd97eb537607c0494ae179ce64a6fc82ce733a7cbacb9ce91b5 | ['sh', '-c', './tools/b build two_dylib_swap_test && ./.b/out/debug/bin/two_dylib_swap_test']; darwin-arm64, debug; Two-dylib swap on Darwin arm64 | Two-dylib swap on Darwin arm64; current host only | passed |
| `vexgraph-ecosystem/tests/hotcwap/hot/uninstall_guard_test.c` | ✅ | 1793370526 | 3c8d8e44fb2e98275cbc9ec35fd772f17ce98517b7c44bf92503d1e52cac0ec8 | ['sh', '-c', './tools/b build uninstall_guard_test && ./.b/out/debug/bin/uninstall_guard_test']; darwin-arm64, debug; Uninstall path guard on Darwin arm64 | Uninstall path guard on Darwin arm64; current host only | passed |
| `vexgraph-ecosystem/tests/hotcwap/hot/wrong_binary_test.c` | ✅ | 1793370528 | 1fcc5ec383a342d4bb5e55fec626bf6317921b80ee2ecd2fa3bdb384d02ded3c | ['sh', '-c', './tools/b build wrong_binary_test && ./.b/out/debug/bin/wrong_binary_test']; darwin-arm64, debug; Wrong module rejection on Darwin arm64 | Wrong module rejection on Darwin arm64; current host only | passed |

### `vexgraph-ecosystem/tests/language`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/language/run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/language/adapters/c`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/language/adapters/c/c23_highlights_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/language/adapters/c/c23_inlay_hints_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/language/adapters/c/c23_lex_step_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/language/adapters/c/c23_lexer_run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/language/adapters/c/c23_lexer_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/language/adapters/c23`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/language/adapters/c23/c23_adapter_run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/language/adapters/c23/c23_adapter_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/language/adapters/diff`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/language/adapters/diff/diff_adapter_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/language/analysis`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/language/analysis/diagnostic_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/language/analysis/syntax_span_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/language/document`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/language/document/line_index_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/language/document/source_range_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/language/document/text_document_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/language/document/text_snapshot_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/language/index`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/language/index/dependency_graph_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/language/index/file_analysis_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/language/index/project_index_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/language/lang`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/language/lang/language_adapter_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/language/lang/language_engine_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/language/lang/language_lex_result_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/language/lang/language_registry_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/language/project`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/language/project/build_target_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/language/project/language_project_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/language/project/project_configuration_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/language/project/project_file_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/language/semantic`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/language/semantic/reference_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/language/semantic/symbol_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/language/style`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/language/style/style_key_registry_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/language/style/text_style_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/language/syntax`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/language/syntax/role_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/language/syntax/token_stream_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/language/text`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/language/text/bounded_text_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/language/token`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/language/token/token_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/lifetime/capability`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/lifetime/capability/capability_test.c` | ✅ | 1793370414 | 3e85d667910e5080274e2970cc5ebb0578658d70bad65db5302d04255e658af3 | ['sh', '-c', './tools/b build capability_test && ./.b/out/debug/bin/capability_test']; darwin-arm64, debug; Capability cache and names on Darwin arm64 | Capability cache and names on Darwin arm64; current host only | passed |

### `vexgraph-ecosystem/tests/lifetime/kernel`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/lifetime/kernel/application_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/lifetime/kernel/commandline_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/lifetime/kernel/console_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/lifetime/kernel/kernel_function_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/lifetime/kernel/kernel_lifecycle_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/lifetime/kernel/process_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/lifetime/permission`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/lifetime/permission/permission_test.c` | ✅ | 1793370416 | 85fa18fd61ada0699b2231adcad9599fa8b70eabafbcfe990096a475042bd353 | ['sh', '-c', './tools/b build permission_test && ./.b/out/debug/bin/permission_test']; darwin-arm64, debug; Permission names and supported-host status on Darwin arm64 | Permission names and supported-host status on Darwin arm64; current host only | passed |

### `vexgraph-ecosystem/tests/lifetime/platform`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/lifetime/platform/platform_test.c` | ✅ | 1793370384 | aad43309462ae28af35e574c82d3c61fd30d1dd2ed4973ac5edbcc7210cc4c67 | ['sh', '-c', './tools/b build platform_test && ./.b/out/debug/bin/platform_test']; darwin-arm64, debug; six-target compile-time branches and current host identity only | Asserts the exact target, derived platform/architecture axes, target names, and raw compiler macro resolution for the host build. | passed |

### `vexgraph-ecosystem/tests/lifetime/spoke`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/lifetime/spoke/spoke_test.c` | ✅ | 1793370446 | c5559f2db0ad32b53f9bc289c3a855dbca83f25bb595317212288d01ebf329e0 | ['sh', '-c', './tools/b build spoke_test && ./.b/out/debug/bin/spoke_test']; darwin-arm64, debug; Bespoke bridge state on Darwin arm64 | Bespoke bridge state on Darwin arm64; current host only | passed |

### `vexgraph-ecosystem/tests/lifetime/window`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/lifetime/window/bridge_seam_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/lifetime/window/present_surface_test.c` | ✅ | 1793371065 | 362e8f353c796a05dcec90456da6851d69d082e8835d9d0df11da2d36211cc8a | ['sh', '-c', './tools/b build present_surface_test &gt;/dev/null 2&gt;&1 && ./.b/out/debug/bin/present_surface_test']; darwin-arm64, debug; re-executed after the delegate hand-back; other targets not exercised | Cocoa surface seam; re-run passes where the delegate recorded a failure | passed |
| `vexgraph-ecosystem/tests/lifetime/window/traffic_light_test.c` | ✅ | 1793370428 | adac7b364990cd28974257511d04e0f8d4ffd8a1fef318cde950ef81da25f79b | ['sh', '-c', './tools/b build traffic_light_test && ./.b/out/debug/bin/traffic_light_test']; darwin-arm64, debug; Cocoa traffic light seam on Darwin arm64 | Cocoa traffic light seam on Darwin arm64; current host only | passed |
| `vexgraph-ecosystem/tests/lifetime/window/window_event_test.c` | ✅ | 1793370425 | 1b5b7545e60611eef9ea43c93b6d0411e206ed87608831bb6bb1454d40b338b3 | ['sh', '-c', './tools/b build window_event_test && ./.b/out/debug/bin/window_event_test']; darwin-arm64, debug; Window event seam on Darwin arm64; C branches not exercised | Window event seam on Darwin arm64; C branches not exercised; current host only | passed |
| `vexgraph-ecosystem/tests/lifetime/window/window_test.c` | ✅ | 1793371063 | d5e0f38c43630155d29bbb39056685f85190f52466686ade0e613c4bb32a8e0f | ['sh', '-c', './tools/b build window_test &gt;/dev/null 2&gt;&1 && ./.b/out/debug/bin/window_test']; darwin-arm64, debug; re-executed after the delegate hand-back; other targets not exercised | Window lifecycle and contract; re-run passes where the delegate recorded a failure | passed |

### `vexgraph-ecosystem/tests/primeagen`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/primeagen/launcher_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/readme_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/primeagen/cli`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/primeagen/cli/appearance_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/cli/main_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/cli/preview_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/cli/screen_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/cli/tui_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/cli/update_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/cli/update_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/cli/view_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/primeagen/native`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/primeagen/native/request_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/primeagen/personality`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/primeagen/personality/owo_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/primeagen/session`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/primeagen/session/controlled_consent_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/session/session_answer_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/session/session_answer_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/session/session_bridge_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/session/session_consent_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/primeagen/src`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/primeagen/src/agent_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/src/controlled_session_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/src/env_file_native_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/src/env_file_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/src/env_file_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/src/json_admit_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/src/json_admit_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/src/json_input_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/src/process_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/src/provider_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/src/session_host_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/src/settings_native_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/src/settings_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/src/tools_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/src/transport_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/primeagen/tools`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/primeagen/tools/bash_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/tools/create_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/tools/delete_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/tools/edit_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/tools/fs_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/tools/fs_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/tools/list_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/tools/main_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/tools/read_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/tools/websearch_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/tools/write_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/primeagen/tui`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/primeagen/tui/markdown_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/tui/tui_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/primeagen/tui/utf8_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/primeagen/tui/event`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/primeagen/tui/event/mouse_event_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/relational-engine`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/relational-engine/native_memory_doc_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/native_run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/preferences_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/primer_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/scaffold_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/relational-engine/io`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/relational-engine/io/cache_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/io/clipboard_test.c` | ❌ | 1793371090 | fdeb3a49022200c49accf19255d75310ebfe8e0f5479bfbe1b9c972c656fbd50 | ['sh', '-c', './tools/b build clipboard_test &gt;/dev/null 2&gt;&1 && ./.b/out/debug/bin/clipboard_test']; darwin-arm64, debug; system clipboard mutation requires RE_TEST_SYSTEM_CLIPBOARD=1 | Clipboard stub/API proof; skips by design without the env opt-in (recorded as skipped, not failed) | skipped (exit 77) |
| `vexgraph-ecosystem/tests/relational-engine/io/file_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/io/filewriter_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/io/frame_inbox_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/io/hot_file_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/io/log_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/io/logparser_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/io/process_spawn_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/io/vexhome_test.c` | ✅ | 1793370453 | e35716d966290e3bc245423a2cf9863146d941673c7cab7c1598f2632c98a8f5 | ['sh', '-c', './tools/b build vexhome_test && ./.b/out/debug/bin/vexhome_test']; darwin-arm64, debug; VexHome path resolution on Darwin arm64 | VexHome path resolution on Darwin arm64; current host only | passed |

### `vexgraph-ecosystem/tests/relational-engine/nio`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/relational-engine/nio/fixed_mapped_file_abi_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/nio/growable_mapped_file_abi_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/nio/mem_exhaustion_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/nio/mem_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/nio/relational_memory_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/nio/transient_lifetime_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/relational-engine/relational`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/relational-engine/relational/cell_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/relational/class_relational_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/relational/shelf_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/relational/symbol_table_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/relational/variable_hash_map_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/relational/variable_mini_map_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/relational/variable_pool_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/relational/variable_slot_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/relational/variable_strict_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/relational-engine/rust`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/relational-engine/rust/run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/rust/sanitizer_run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/relational-engine/rust/ffi`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/relational-engine/rust/ffi/memory_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/rust/ffi/memory_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/rust/ffi/row_pool_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/rust/ffi/row_pool_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/rust/ffi/variable_registry_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/rust/ffi/variable_registry_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/relational-engine/rust/io`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/relational-engine/rust/io/preallocated_failure_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/rust/io/preallocated_file_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/rust/io/preallocation_error_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/rust/io/preallocation_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/relational-engine/rust/nio`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/relational-engine/rust/nio/chunk_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/rust/nio/fixed_mapped_file_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/rust/nio/growable_mapped_file_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/rust/nio/handle_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/rust/nio/mapping_error_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/rust/nio/mem_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/rust/nio/row_chunk_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/rust/nio/row_handle_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/rust/nio/typed_chunk_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/relational-engine/rust/primitives`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/relational-engine/rust/primitives/atomic_string_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/rust/primitives/string_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/relational-engine/rust/struct`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/relational-engine/rust/struct/chunked_list_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/rust/struct/row_pool_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/rust/struct/typed_pool_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/relational-engine/rust/variable`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/relational-engine/rust/variable/variable_registry_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/relational-engine/rust/variable/variable_slot_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/relational-engine/search/primitives`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/relational-engine/search/primitives/name_search_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/relational-engine/type`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/relational-engine/type/type_algebra_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/repos`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/repos/artwork_headers_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/repos/vex-graph`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/repos/vex-graph/readme_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/semicolon`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/semicolon/gitignore_rail_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/semicolon/gutter_alignment_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/semicolon/icon_catalog_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/semicolon/install_command_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/semicolon/launcher_language_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/semicolon/mouse_capture_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/semicolon/rail_format_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/semicolon/rail_interaction_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/semicolon/readme_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/semicolon/run_console_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/semicolon/tui_main_test.py` | ✅ | 1793373371 | 1345893dbe66c0d69f722f8b0fa8861f65f3ebdfdf39eb2c70bf0092189682ae | ['sh', '-c', 'python3 vexgraph-ecosystem/tests/semicolon/tui_main_test.py']; darwin-arm64, debug, real pty and real pasteboard; standalone semicolon build via its own build.py; other targets not exercised | Repaired the harness to the two-root layout, gave its own build.py the R0 platform include, and replaced the pasteboard race with a bounded wait; 3/3 green | passed |

### `vexgraph-ecosystem/tests/semicolon/editor`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/semicolon/editor/language_bridge_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/semicolon/editor/run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/semicolon/editor/semicolon_syntax_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/sesh`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/sesh/docs_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/sesh/run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/sesh/session_run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/sesh/lang`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/sesh/lang/arity_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/sesh/lang/interop_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/sesh/session`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/sesh/session/auth_service_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/sesh/session/client_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/sesh/session/operation_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/sesh/session/operations_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/sesh/session/resource_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/sesh/session/sesh_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/sesh/session/text_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/sesh/session/workspace_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/sesh/snapshot`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/sesh/snapshot/snapshot_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/tools`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/tools/agent_tool_contract_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/tools/agents_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/tools/arrange_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/tools/c23_migration_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/tools/ci_repos_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/tools/clion_adapter_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/tools/compositor_contract_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/tools/compositor_shader_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/tools/darling_lifecycle_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/tools/ecosystem_docs_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/tools/exhaustion_law_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/tools/filter_gallery_resources_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/tools/harness_ide_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/tools/linter_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/tools/migration_contract_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/tools/opencode_preferences_test.ts` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/tools/per_repo_ide_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/tools/prefs_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/tools/readiness_test.py` | ✅ | 1793381558 | 141cb7d93ab8714fe2ecaaec44273259502ccaf4504129d11a95e43b67a52600 | ['python3', '-B', 'vexgraph-ecosystem/tests/tools/readiness_test.py']; Command-only evidence; no broader readiness claim | Automated lab check; visual approval not recorded | passed |
| `vexgraph-ecosystem/tests/tools/run_current_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/tools/sampled_texture_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/tools/test_checklist_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/vexspoke`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/vexspoke/backend_contract_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/vexspoke/algo`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/vexspoke/algo/algo_suite_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/algo/bvh_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/algo/dijkstra_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/algo/kd_tree_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/algo/radix_sort_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/algo/segment_index_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/algo/sort_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/algo/spatial_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/algo/tree_sit_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/vexspoke/atomic`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/vexspoke/atomic/registry_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/atomic/ring_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/atomic/spin_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/vexspoke/audio`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/vexspoke/audio/audio_hal_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/vexspoke/bit`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/vexspoke/bit/bit_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/vexspoke/c23`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/vexspoke/c23/equals_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/c23/fn_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/c23/free_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/vexspoke/cli`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/vexspoke/cli/console_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/vexspoke/deferred`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/vexspoke/deferred/dispatch_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/vexspoke/exception`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/vexspoke/exception/exception_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/exception/throw_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/exception/try_code_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/exception/try_ptr_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/exception/try_value_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/vexspoke/image`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/vexspoke/image/png_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/vexspoke/input`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/vexspoke/input/hardware_input_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/input/input_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/input/key_map_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/vexspoke/lang`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/vexspoke/lang/mat4_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/lang/vec2_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/lang/vec3_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/lang/vec4_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/vexspoke/math`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/vexspoke/math/coord_frame_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/math/fast_math_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/math/math_coord_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/math/math_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/math/strict_math_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/vexspoke/misc`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/vexspoke/misc/header_veto_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/vexspoke/net`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/vexspoke/net/net_test.c` | ✅ | 1793371082 | bd94a331a89b4923a568c18a3cceea645003ba2ba1a18dff270a4a01060b52f1 | ['sh', '-c', './tools/b build net_test &gt;/dev/null 2&gt;&1 && ./.b/out/debug/bin/net_test']; darwin-arm64, debug; re-executed after the delegate hand-back; other targets not exercised | HTTP/network seam; re-run passes | passed |
| `vexgraph-ecosystem/tests/vexspoke/net/run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/net/tls_apple_run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/net/tls_apple_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/net/url_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/net/websocket_smoke_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/net/websocket_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/net/ws_smoke_run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/vexspoke/objects`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/vexspoke/objects/choice_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/objects/future_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/objects/global_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/objects/local_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/objects/passive_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/objects/probable_objects_test.c` | ✅ | 1793370430 | f9d78f8bc680cab78947adbbde48bd9c7312125bd2c98d102f5b253b8f772fb8 | ['sh', '-c', './tools/b build probable_objects_test && ./.b/out/debug/bin/probable_objects_test']; darwin-arm64, debug; ProbableObjects value and boundary behavior on Darwin arm64 | ProbableObjects value and boundary behavior on Darwin arm64; current host only | passed |
| `vexgraph-ecosystem/tests/vexspoke/objects/probable_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/vexspoke/oop`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/vexspoke/oop/stride_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/oop/type_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/vexspoke/primitive`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/vexspoke/primitive/bool_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/primitive/brain_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/primitive/byte_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/primitive/double_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/primitive/fixed32_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/primitive/fixed64_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/primitive/float_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/primitive/int_double_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/primitive/int_float_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/primitive/int_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/primitive/long_double_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/primitive/long_float_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/primitive/long_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/primitive/pack_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/primitive/short_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/primitive/string_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/vexspoke/reactive`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/vexspoke/reactive/reactive_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/reactive/reactive_typed_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/vexspoke/reflection`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/vexspoke/reflection/reflection_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/vexspoke/regex`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/vexspoke/regex/charclass_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/regex/nodelist_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/regex/parser_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/regex/program_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/regex/regex_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/regex/run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/regex/span_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/regex/vm_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/vexspoke/search`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/vexspoke/search/find_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/search/search_calc_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/search/spotlight_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/vexspoke/security`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/vexspoke/security/argon2_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/security/base32_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/security/blake2b_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/security/chacha20_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/security/chacha20poly1305_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/security/crypto_security_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/security/crypto_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/security/hkdf_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/security/hmac_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/security/keychain_test.c` | ❌ | 1793371088 | 7db27b4dc0b6c19099d7200b0cd6668dad240d8f0da9d36b62fec4fc5afe4f0d | ['sh', '-c', './tools/b build keychain_test &gt;/dev/null 2&gt;&1 && ./.b/out/debug/bin/keychain_test']; darwin-arm64, debug; requires DARKBASE_KEYCHAIN_TEST=1 and writes the real login keychain | Keychain API proof; skips by design without the env opt-in (recorded as skipped, not failed) | skipped (exit 77) |
| `vexgraph-ecosystem/tests/vexspoke/security/otpauth_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/security/password_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/security/password_verifier_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/security/poly1305_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/security/secure_random_test.c` | ✅ | 1793370435 | 59dda4e92f16c6d43a1c791e429ccf690cde856fe2ce6fdf2243b63c19701dfe | ['sh', '-c', './tools/b build secure_random_test && ./.b/out/debug/bin/secure_random_test']; darwin-arm64, debug; OS random backend behavior on Darwin arm64 | OS random backend behavior on Darwin arm64; current host only | passed |
| `vexgraph-ecosystem/tests/vexspoke/security/sha1_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/security/totp_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/vexspoke/struct`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/vexspoke/struct/array_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/struct/chunked_list_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/struct/chunked_paged_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/struct/circle_array_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/struct/collection_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/struct/deque_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/struct/exhaustion_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/struct/list_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/struct/map_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/struct/minheap_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/struct/octree_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/struct/queue_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/struct/set_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/struct/sparseset_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/struct/spatial_struct_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/struct/sphere_array_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/struct/stack_observability_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/struct/stack_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/vexspoke/system`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/vexspoke/system/app_detect_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/system/capture_tool_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/system/display_info_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/system/display_monitor_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/system/graphics_info_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/system/hardware_info_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/system/process_probe_test.c` | ✅ | 1793370438 | d5e9678a4f60a12a5a506bc3663457018d3f62f18cb4b2c145fca01a9f09a9c4 | ['sh', '-c', './tools/b build process_probe_test && ./.b/out/debug/bin/process_probe_test']; darwin-arm64, debug; Process probe behavior on Darwin arm64 | Process probe behavior on Darwin arm64; current host only | passed |
| `vexgraph-ecosystem/tests/vexspoke/system/system_test.c` | ✅ | 1793370449 | 621024ae0517e82c7cef22c937a3de63a8a22784c18b9466b00649a562e77a5d | ['sh', '-c', './tools/b build system_test && ./.b/out/debug/bin/system_test']; darwin-arm64, debug; System discovery surface on Darwin arm64 | System discovery surface on Darwin arm64; current host only | passed |

### `vexgraph-ecosystem/tests/vexspoke/thread`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/vexspoke/thread/compute_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/thread/thread_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/vexspoke/time`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/vexspoke/time/calendar_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/time/clock_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/time/datetime_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/time/nanotime_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/time/time_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `vexgraph-ecosystem/tests/vexspoke/util`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-ecosystem/tests/vexspoke/util/arrays_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/util/hash_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `vexgraph-ecosystem/tests/vexspoke/util/random_test.c` | ✅ | 1793370440 | 16180fd928d0057e8b52e83512c6926d21044b025e5e2ac171260840f69ff519 | ['sh', '-c', './tools/b build random_test && ./.b/out/debug/bin/random_test']; darwin-arm64, debug; Seeded random behavior on Darwin arm64 | Seeded random behavior on Darwin arm64; current host only | passed |

## vexgraph-ecosystem/vexspoke

No inventoried files yet; not verified.

## vexgraph-hobby-projects/api-haven

No inventoried files yet; not verified.

## vexgraph-hobby-projects/b

### `vexgraph-hobby-projects/b/tests`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `vexgraph-hobby-projects/b/tests/ci_smoke_test.py` | ✅ | 1793451239 | 0391b5653dc5fe80b473f1254d21ec626464a0e209e7df1bb5c52eca96cd148b | ['sh', '-c', 'set -e; cd vexgraph-hobby-projects/b; export B_HOME=$(mktemp -d); export B_TARGET=darwin-arm64; ./b --help &gt;/dev/null; export B_BINARY="$HOME/Library/Application Support/b/cli"; exec python3 -B tests/ci_smoke_test.py', '--timeout', '300']; test | b claims a territory with generate, writes .b/workspace.json with units, refuses a nested claim, run/breeze resolve upward to the territory and refuse outside one, self-box and install round-trip pass. | passed |

## vexgraph-hobby-projects/func

No inventoried files yet; not verified.

## vexgraph-hobby-projects/harness

No inventoried files yet; not verified.

## vexgraph-hobby-projects/hotcwap

No inventoried files yet; not verified.

## vexgraph-hobby-projects/primeagen

No inventoried files yet; not verified.

## workspace

### `tools/python`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tools/python/test_checklist.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

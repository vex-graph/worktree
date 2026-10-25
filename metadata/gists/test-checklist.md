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

## tests

### `tests`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/test_support.h` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/api-haven`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/api-haven/ai_chat_sisters_test.c` | ✅ | 1792852616 | b955b3879428fdabbba25994ac7aed7010efa9d9b658fafee86217e1abf27f65 | ['./cmake-build-debug/bin/ai_chat_sisters_test']; macOS arm64; C23; debug build; direct owner binary from cmake-build-debug; no live network | API Haven constructor chooser APIs and call sites | passed |
| `tests/api-haven/ai_provider_test.c` | ✅ | 1792852616 | c105bfe624cccb9f8d05f8b80c2d70e4ba5ae17bfb0d1b9cb7c78f572e64ab63 | ['./cmake-build-debug/bin/ai_provider_test']; macOS arm64; C23; debug build; direct owner binary from cmake-build-debug; no live network | API Haven constructor chooser APIs and call sites | passed |
| `tests/api-haven/ai_sse_test.c` | ✅ | 1792052698 | 255abedaa92ebdc7ef4d5b6b13cc42f58d5e347cc96a1d080cc5129bff80cce0 | ['cmake-build-debug/bin/ai_sse_test']; macOS native executable | AiSse event getter returns borrowed value | passed |
| `tests/api-haven/app_broker_test.c` | ✅ | 1792852616 | 015712a20c8373ad4b9af47abeb5fea20529135b71d47db10d3a2baf5235d837 | ['./cmake-build-debug/bin/app_broker_test']; macOS arm64; C23; debug build; direct owner binary from cmake-build-debug; no live network | API Haven constructor chooser APIs and call sites | passed |
| `tests/api-haven/asset_test.c` | ✅ | 1792852616 | c934946a5f35dc0d03cf6474e7bd699af7bd9908a794f882e4486f269942843f | ['./cmake-build-debug/bin/asset_test']; macOS arm64; C23; debug build; direct owner binary from cmake-build-debug; no live network | AssetBroker cache-sub getter returns borrowed value | passed |
| `tests/api-haven/db_provider_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/api-haven/db_sqlite_file_test.c` | ✅ | 1792852617 | a1149dc4a217a33489d153d19d2272e63d0a9047eba866a765426efb73f7263b | ['./cmake-build-debug/bin/db_sqlite_file_test']; macOS arm64; C23; debug build; direct owner binary from cmake-build-debug; no live network | API Haven constructor chooser APIs and call sites | passed |
| `tests/api-haven/harness_run_test.c` | ✅ | 1792852617 | 1e9593cf2f005e95070c12912c9d6db89d4a6db2f4a766889b2d74aaa41cb5c8 | ['./cmake-build-debug/bin/harness_run_test']; macOS arm64; C23; debug build; direct owner binary from cmake-build-debug; no live network | API Haven constructor chooser APIs and call sites | passed |
| `tests/api-haven/haven_ws_fanout_test.c` | ✅ | 1792024270 | 0ec06704d56fb664de8a2eda19c328b15aab7a7b010ce122dc090549cfb958b3 | ['ctest', '--test-dir', '/private/tmp/vexgraph-cmake-check-cmake', '--output-on-failure', '-R', '^(ai_chat_sisters_test&#124;ai_provider_test&#124;ai_sse_test&#124;app_broker_test&#124;asset_test&#124;db_sqlite_file_test&#124;harness_run_test&#124;haven_ws_fanout_test&#124;mcp_server_test)$']; macOS arm64; C23; debug CTest; no live network | API Haven constructor chooser APIs and call sites | passed |
| `tests/api-haven/json_flex_test.c` | ✅ | 1792053379 | b483ebc7cecaf560457b34156cc30c6d373b5883a5f69c13be787ffd7c568256 | ['./cmake-build-debug/bin/json_flex_test']; Command-only evidence; no broader readiness claim | Direct-return length-delimited JsonStringView getter, wrong-type handling, and writer/parser round trip | passed |
| `tests/api-haven/mcp_server_test.c` | ✅ | 1792852617 | 5cd453a5d2df1b1c9021f3556b38c64241c36ab0f91ef72a7aec3801a04dc38a | ['./cmake-build-debug/bin/mcp_server_test']; macOS arm64; C23; debug build; direct owner binary from cmake-build-debug; no live network | API Haven constructor chooser APIs and call sites | passed |
| `tests/api-haven/probe_consumer_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/api-haven/webhook_loopback_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/api-haven/ws_binding_run.py` | ✅ | 1792074371 | 414e3e90b2cc29501d75e07db555edb355f56f17d1060c0b9192ad9832c5574a | ['python3', '-B', 'tests/vexspoke/net/run.py']; macOS arm64; strict + ASan/UBSan; ws:// loopback peer only -- the wss:// path is proven by the smoke owner | WebSocket protocol and binding owners re-verified after the transport-guard fix that let writes reach the TLS session (writeText/writeBinary/writePing/writeClose/wsSendFrame had all required a socket fd, so every wss:// write was dead): the offline owners stay green and the live smoke is what caught it | passed |
| `tests/api-haven/ws_source_binding_test.c` | ✅ | 1792852681 | 283f72c0742222cc3c1e7aab3f1f20b4c2025968d8a92c6f0381290647cc1e31 | ['python3', '-B', 'tests/vexspoke/net/run.py']; macOS arm64; strict + ASan/UBSan WebSocket owner through the vexspoke net runner; no live network | API Haven WebSocket source binding | passed |

### `tests/api-haven/api`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/api-haven/api/rest_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/api-haven/storage`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/api-haven/storage/snapshot_io_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/b`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/b/arduino_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/b/blueprint_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/b/box_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/b/box_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/b/cli_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/b/cmake_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/b/cpp_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/b/html_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/b/inspect_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/b/javascript_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/b/npm_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/b/objc_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/b/php_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/b/preferences_test.py` | ❌ | 1792060065 | eb020a53ae84a567cf3596e1f2235fe702e2e5309521baa6fbbe12264f8f71c6 | ['python3', '-B', 'tests/b/preferences_test.py']; macOS arm64; source-level preferences checks; fails because expected personal/b/b.h and personal/b C sources are absent from this checkout | Workspace preference source checks after Value Return Law clarification | failed (exit 1) |
| `tests/b/readme_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/b/shell_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/b/sql_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/b/swift_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/b/typescript_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/b/util_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/b/util_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/b/workspace_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/b/adapters`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/b/adapters/adapter_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/b/adapters/cargo_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/b/adapters/glsl_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/b/adapters/go_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/b/adapters/lua_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/b/adapters/metal_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/b/adapters/workspace_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/b/adapters/zig_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/darkbase-engine`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/darkbase-engine/run.py` | ❌ | 1792049336 | 13c2b614af5cd41d50cb7c994b9cdf7f71993733d8238947c5271b1ac8fe9cee | ['python3', '-B', 'tests/darkbase-engine/run.py']; Workspace graph attempt only; no graph runtime coverage credited; no baseline changes | Graph owner runner registration exercised; currently blocked before execution by global post-migration Vexspoke ownership ratchet, independent Store runner remains separate passing proof | failed (exit 1) |

### `tests/darkbase-engine/database`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/darkbase-engine/database/database_result_test.c` | ✅ | 1792852617 | ab9eef91bcec27601b71ca00be76fabb5d79dff5bcb8106ac67975015f849a05 | ['./cmake-build-debug/bin/database_result_test']; macOS arm64; C23; debug build; direct owner binary from cmake-build-debug; no live network | Darkbase Database and cursor owners, now including named field resolution: Database_fieldSpan returns a copied {code, offset, size} for a folded field name, a generic caller reads a row's Bytes through the span, and a null argument, unknown entity, unknown field, ambiguous name and out-of-row span each reject explicitly rather than returning a span a reader could not safely use | passed |
| `tests/darkbase-engine/database/database_test.c` | ✅ | 1792852617 | ff2d55ed7d1d8ba630a31e30fcdccea95320fb32219ff17cf877683d96a05f59 | ['./cmake-build-debug/bin/database_test']; macOS arm64; C23; debug build; direct owner binary from cmake-build-debug; no live network | Darkbase Database and cursor owners, now including named field resolution: Database_fieldSpan returns a copied {code, offset, size} for a folded field name, a generic caller reads a row's Bytes through the span, and a null argument, unknown entity, unknown field, ambiguous name and out-of-row span each reject explicitly rather than returning a span a reader could not safely use | passed |
| `tests/darkbase-engine/database/run.py` | ✅ | 1792116783 | d9ff57f8d811384f74997d2fea027e86668e2a83022df25ca9c59e86182eb1cf | ['python3', '-B', 'tests/darkbase-engine/database/run.py']; macOS arm64; strict optimized C ASan/UBSan; linked Rust archive not sanitizer-instrumented and reports macOS 27 deployment metadata; workspace graph still blocked by the Vexspoke ownership ratchet | Darkbase Database and cursor owners, now including named field resolution: Database_fieldSpan returns a copied {code, offset, size} for a folded field name, a generic caller reads a row's Bytes through the span, and a null argument, unknown entity, unknown field, ambiguous name and out-of-row span each reject explicitly rather than returning a span a reader could not safely use | passed |

### `tests/darkbase-engine/oop`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/darkbase-engine/oop/modifier_test.c` | ✅ | 1792377427 | 52f223e9260b61c189e637929757befd465ca4b42279eb2256acdeb2ef9ecda6 | ['sh', '-c', 'DB=suite/ecosystem/darkbase-engine; CPU=suite/ecosystem/vexspoke; clang -std=gnu23 -Wall -Wextra -Werror -O2 -UNDEBUG -mcpu=apple-m1 -mmacosx-version-min=14.0 -I $DB/src -I $CPU/src tests/darkbase-engine/oop/modifier_test.c $DB/src/oop/modifier.c -o /tmp/modifier_test && /tmp/modifier_test && clang -std=gnu23 -Wall -Wextra -Werror -O2 -UNDEBUG -mcpu=apple-m1 -mmacosx-version-min=14.0 -I $DB/src -I $CPU/src -fsanitize=address,undefined tests/darkbase-engine/oop/modifier_test.c $DB/src/oop/modifier.c -o /tmp/modifier_test_san && /tmp/modifier_test_san']; macOS arm64 lab; clang -std=gnu23 -Wall -Wextra -Werror -O2 -UNDEBUG -mcpu=apple-m1 -mmacosx-version-min=14.0; optimized and ASan/UBSan runs | Modifier value record: orthogonal axes + validation, 80 declaration presets and short forms, free-order parser with unknown/duplicate/overlong rejection (one THROW each), predicates, warnings, and bounded projections | passed |

### `tests/darkbase-engine/page`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/darkbase-engine/page/page_test.c` | ✅ | 1792049307 | e74e3eede6a4672ac5d07fbf43ce1c88dc99ef51928462bb753e3ee84e1f9258 | ['python3', '-B', 'tests/darkbase-engine/store/run.py']; macOS arm64 local host; fresh native strict C23 -O2 assertions and ASan/UBSan; real Rust debug staticlib, Rust not sanitizer-instrumented; leaks 0/0 on non-fork lifetime/fault paths only; Rust std macOS27 deployment warning and global graph ownership-ratchet failure remain gaps | Single-file Store/Page/Wal owners: retained redo and free-page reuse/reopen; 48 live full pages, two exhaustion bounds, exact Store/adversarial diagnostics, three actual child-exit boundaries, torn-data repair, five injected IO stages, unsupported constructor arities, non-fork OS leak check | passed |

### `tests/darkbase-engine/store`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/darkbase-engine/store/run.py` | ✅ | 1792049307 | c893ccb57718049772741a73039bc43a983c517ffcf7de344551453bc067e194 | ['python3', '-B', 'tests/darkbase-engine/store/run.py']; macOS arm64 local host; fresh native strict C23 -O2 assertions and ASan/UBSan; real Rust debug staticlib, Rust not sanitizer-instrumented; leaks 0/0 on non-fork lifetime/fault paths only; Rust std macOS27 deployment warning and global graph ownership-ratchet failure remain gaps | Single-file Store/Page/Wal owners: retained redo and free-page reuse/reopen; 48 live full pages, two exhaustion bounds, exact Store/adversarial diagnostics, three actual child-exit boundaries, torn-data repair, five injected IO stages, unsupported constructor arities, non-fork OS leak check | passed |
| `tests/darkbase-engine/store/store_adversarial_test.c` | ✅ | 1792049307 | cdeca2b43bdd0cd575156dae3240b18caa42da71b967f0aeab65465c9ae7b521 | ['python3', '-B', 'tests/darkbase-engine/store/run.py']; macOS arm64 local host; fresh native strict C23 -O2 assertions and ASan/UBSan; real Rust debug staticlib, Rust not sanitizer-instrumented; leaks 0/0 on non-fork lifetime/fault paths only; Rust std macOS27 deployment warning and global graph ownership-ratchet failure remain gaps | Single-file Store/Page/Wal owners: retained redo and free-page reuse/reopen; 48 live full pages, two exhaustion bounds, exact Store/adversarial diagnostics, three actual child-exit boundaries, torn-data repair, five injected IO stages, unsupported constructor arities, non-fork OS leak check | passed |
| `tests/darkbase-engine/store/store_test.c` | ✅ | 1792049307 | a33b4092c5aa16feb7bc0d0ff0cfdf44216060ee516e83270b05355dcd68ed22 | ['python3', '-B', 'tests/darkbase-engine/store/run.py']; macOS arm64 local host; fresh native strict C23 -O2 assertions and ASan/UBSan; real Rust debug staticlib, Rust not sanitizer-instrumented; leaks 0/0 on non-fork lifetime/fault paths only; Rust std macOS27 deployment warning and global graph ownership-ratchet failure remain gaps | Single-file Store/Page/Wal owners: retained redo and free-page reuse/reopen; 48 live full pages, two exhaustion bounds, exact Store/adversarial diagnostics, three actual child-exit boundaries, torn-data repair, five injected IO stages, unsupported constructor arities, non-fork OS leak check | passed |

### `tests/darkbase-engine/util`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/darkbase-engine/util/crc32_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/darkbase-engine/wal`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/darkbase-engine/wal/wal_test.c` | ✅ | 1792049307 | e32076f05fe9c098a0338c58e026066eac0411a84f7674ddc0aaf5dbac8bb271 | ['python3', '-B', 'tests/darkbase-engine/store/run.py']; macOS arm64 local host; fresh native strict C23 -O2 assertions and ASan/UBSan; real Rust debug staticlib, Rust not sanitizer-instrumented; leaks 0/0 on non-fork lifetime/fault paths only; Rust std macOS27 deployment warning and global graph ownership-ratchet failure remain gaps | Single-file Store/Page/Wal owners: retained redo and free-page reuse/reopen; 48 live full pages, two exhaustion bounds, exact Store/adversarial diagnostics, three actual child-exit boundaries, torn-data repair, five injected IO stages, unsupported constructor arities, non-fork OS leak check | passed |

### `tests/darkbase-headless`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/darkbase-headless/protocol_run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/darkbase-headless/protocol`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/darkbase-headless/protocol/headless_protocol_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/darkbase-headless/service`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/darkbase-headless/service/service_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/darling/capture`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/darling/capture/ui_clip_restore_battle_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/darling/capture/ui_clip_scope_battle_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/darling/capture/ui_multiple_masks_pixels_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/darling/capture/ui_nested_clip_battle_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/darling/capture/ui_rounded_clip_battle_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/darling/capture/ui_rounded_hit_battle_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/darling/color`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/darling/color/ui_border_pixels_battle_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/darling/color/ui_visual_state_pixels_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/darling/compositor`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/darling/compositor/gallery_photo_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/darling/cursor`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/darling/cursor/set_cursor_test.c` | ✅ | 1792069421 | f5b99ea4749904d187afc64d3d84081426154a37967037ad32ab521fc18a7be3 | ['sh', '-c', './cmake-build-debug/bin/panel_add_test && ./cmake-build-debug/bin/set_cursor_test']; macOS arm64; deterministic panel ownership and cursor preference lab owners; no user visual acceptance claimed | Add and cursor APIs while adding per-file call examples | passed |

### `tests/darling/drawable`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/darling/drawable/picture_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/darling/event`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/darling/event/event_invoke_test.c` | ✅ | 1792852619 | 7da656c9e4ff56aff4f5f34b51c346bb8bf38fca58c6a61b25e93336fdf45739 | ['./cmake-build-debug/bin/event_invoke_test']; macOS arm64; C23; debug build; direct owner binary from cmake-build-debug; no live network | Event registry contract while adding its per-file call example | passed |
| `tests/darling/event/event_kinds_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/darling/frame`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/darling/frame/borderless_frame_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/darling/frame/frame_application_lifecycle_test.c` | ✅ | 1792852621 | ccee27dc1acd39068efbc9e063531fec4a823256bc9de93a758798dd799b96d6 | ['./cmake-build-debug/bin/frame_application_lifecycle_test']; macOS arm64; C23; debug build; direct owner binary from cmake-build-debug; no live network | Frame application lifecycle owner while adding its per-file call example | passed |
| `tests/darling/frame/frame_fps_focus_test.c` | ❌ | 1792069699 | ecdef0bcb5573a61418f276b61cff29c418aed34e7391c89cf4142635e572f3a | ['./cmake-build-debug/bin/frame_fps_focus_test']; darling-frame-fps-focus | Frame FPS and focus assertions on current host | failed (exit 1) |
| `tests/darling/frame/frame_live_resize_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/darling/frame/frame_resize_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/darling/frame/frame_test.c` | ❌ | 1792069618 | 27ac1494b95211961a6057c26a419f627fc37ab5e989f28a7b4142f05b988516 | ['sh', '-c', './cmake-build-debug/bin/frame_test && ./cmake-build-debug/bin/frame_application_lifecycle_test && ./cmake-build-debug/bin/frame_fps_focus_test']; macOS arm64; deterministic Frame rendering, application attachment/lifetime, and FPS focus policy owners; no visual approval claimed | Frame API owner suite while adding its per-file call example | failed (exit 1) |
| `tests/darling/frame/liquid_glass_frame_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/darling/frame/naked_frame_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/darling/frame/traffic_light_frame_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/darling/frame/ui_matryoshka_battle_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/darling/frame/ui_revalidate_cascade_battle_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/darling/frame/ui_wide_tree_battle_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/darling/kinematics/anchor`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/darling/kinematics/anchor/ui_anchor_pivot_pixels_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/darling/kinematics/pivot`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/darling/kinematics/pivot/ui_size_limits_pixels_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/darling/panel/panel`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/darling/panel/panel/panel_add_test.c` | ✅ | 1792069421 | cf9a5f754b3a0009764d8980403c698be56e8b8cdda0db100a088b407683c030 | ['sh', '-c', './cmake-build-debug/bin/panel_add_test && ./cmake-build-debug/bin/set_cursor_test']; macOS arm64; deterministic panel ownership and cursor preference lab owners; no user visual acceptance claimed | Add and cursor APIs while adding per-file call examples | passed |
| `tests/darling/panel/panel/panel_anchor_corner_radius_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/darling/panel/panel/panel_corner_radius_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/darling/panel/panel/panel_events_test.c` | ✅ | 1792852622 | ccc53dfadfa86281d1455d4a457a1c37929712be23c91cfec9efa564bacfd26c | ['./cmake-build-debug/bin/panel_events_test']; macOS arm64; C23; debug build; direct owner binary from cmake-build-debug; no live network | ScrollPanel scalar offset getters in panel event path | passed |
| `tests/darling/panel/panel/panel_matryoshka_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/darling/panel/panel/panel_shadow_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/darling/panel/panel/panel_test.c` | ✅ | 1792069459 | e753dbd316b46b4d0ce024855876845bff2d04871d2ab23748230dd09c0eec22 | ['./cmake-build-debug/bin/panel_test']; macOS arm64; deterministic Panel construction, setters, queries, ownership and paint lab owner; no visual approval claimed | Panel public API while adding its per-file call example | passed |

### `tests/darling/panel/scrollpanel`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/darling/panel/scrollpanel/scroll_panel_test.c` | ✅ | 1792069246 | 233616bd7d2c34ef42eead98c699d95b747e1d76e07ddfc5c4ecc522e05bd32a | ['./cmake-build-debug/bin/scroll_panel_test']; macOS arm64; ScrollPanel deterministic lab owner; not a real-window visual or compositor test | ScrollPanel habitat behavior while adding its per-file call example | passed |
| `tests/darling/panel/scrollpanel/ui_scroll_capture_battle_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/darling/panel/shared`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/darling/panel/shared/ui_element_contract_battle_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/darling/properties`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/darling/properties/properties_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/darling/scaffold`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/darling/scaffold/scaffold_lab_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/determinant`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/determinant/run.py` | ❌ | 1792744061 | 4f87848c00e0e638fd9dd3200409ae9e26f3cb158103fd39acb4fbd24d662bc8 | ['python3', 'tests/determinant/run.py']; macOS arm64; clang strict C23 -Wall -Wextra -Werror with assertions active plus ASan/UBSan via tests/determinant/run.py; all mirrored Determinant owners compiled per mode; no host terminal, downloads or visual acceptance | TerminalScrollGlide per-axis scroll motion: defaults and configured construction, invalid ease/epsilon rejection with preserved state, impulse/target/position/halt/clamp, frame-by-frame easing and snap, saturated SIZE_MAX conversion, safe null defaults, projections, and a settled hot-loop guard. The runner also proves the intended unsupported-arity rejection for TerminalScrollGlide(1) and now compiles 27 terminal owners in both modes. | stale — content changed; rerun required |

### `tests/determinant/cli`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/determinant/cli/command_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/determinant/cli/commandparser_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/determinant/cli/commandregistry_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/determinant/cli/logcommands_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/determinant/cli/output_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/determinant/cli/scanner_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/determinant/events`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/determinant/events/terminal_input_test.c` | ✅ | 1792940728 | bb7698ac082fc7b98ac11a526a9c7172b1aaadee40c449eae94f26a9d6df6474 | ['python3', 'tests/determinant/run.py']; macOS arm64 local lab; clang strict optimized C23 assertions and ASan/UBSan via tests/determinant/run.py; no live host terminal, no physical device or visual acceptance; Linux/Windows unproved | Determinant ui/ taxonomy: surface, image, scroll, panel, text, list, tree, field, code, markdown, button, events, theme and format owners after the directory move | passed |

### `tests/determinant/format`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/determinant/format/terminal_color_test.c` | ✅ | 1792940728 | 158c169b74f2d757e64e80b3b4984aec10cb63311a1d1c2480af7de2987229cd | ['python3', 'tests/determinant/run.py']; macOS arm64 local lab; clang strict optimized C23 assertions and ASan/UBSan via tests/determinant/run.py; no live host terminal, no physical device or visual acceptance; Linux/Windows unproved | Determinant ui/ taxonomy: surface, image, scroll, panel, text, list, tree, field, code, markdown, button, events, theme and format owners after the directory move | passed |

### `tests/determinant/ui/button`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/determinant/ui/button/terminal_button_test.c` | ✅ | 1792940728 | 1006debfd05f355c8b8928c36e37f3a976d2e5e53d8e75ee29126f71b3e0bb5e | ['python3', 'tests/determinant/run.py']; macOS arm64 local lab; clang strict optimized C23 assertions and ASan/UBSan via tests/determinant/run.py; no live host terminal, no physical device or visual acceptance; Linux/Windows unproved | Determinant ui/ taxonomy: surface, image, scroll, panel, text, list, tree, field, code, markdown, button, events, theme and format owners after the directory move | passed |

### `tests/determinant/ui/code`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/determinant/ui/code/terminal_code_view_test.c` | ✅ | 1792940728 | 3f780a4408b13354dc94cfc0d45487ac85b285735b21fff09e775704dccba801 | ['python3', 'tests/determinant/run.py']; macOS arm64 local lab; clang strict optimized C23 assertions and ASan/UBSan via tests/determinant/run.py; no live host terminal, no physical device or visual acceptance; Linux/Windows unproved | Determinant ui/ taxonomy: surface, image, scroll, panel, text, list, tree, field, code, markdown, button, events, theme and format owners after the directory move | passed |

### `tests/determinant/ui/field`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/determinant/ui/field/terminal_input_line_test.c` | ✅ | 1792940728 | e67d0b6d330c526a0614cb665aef741b551b6e608fbb7c0543639fcb0db202e2 | ['python3', 'tests/determinant/run.py']; macOS arm64 local lab; clang strict optimized C23 assertions and ASan/UBSan via tests/determinant/run.py; no live host terminal, no physical device or visual acceptance; Linux/Windows unproved | Determinant ui/ taxonomy: surface, image, scroll, panel, text, list, tree, field, code, markdown, button, events, theme and format owners after the directory move | passed |

### `tests/determinant/ui/image`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/determinant/ui/image/terminal_image_test.c` | ✅ | 1792940728 | 0b2ada1f50906113358055dff5d14585f78b12d0c65e37e034cff8d8e9a36541 | ['python3', 'tests/determinant/run.py']; macOS arm64 local lab; clang strict optimized C23 assertions and ASan/UBSan via tests/determinant/run.py; no live host terminal, no physical device or visual acceptance; Linux/Windows unproved | Determinant ui/ taxonomy: surface, image, scroll, panel, text, list, tree, field, code, markdown, button, events, theme and format owners after the directory move | passed |

### `tests/determinant/ui/list`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/determinant/ui/list/terminal_list_view_test.c` | ✅ | 1792940728 | 151d4840f23dd4e4fad5da18ff2466027df223b7fcc6482051359d4b76bf0f68 | ['python3', 'tests/determinant/run.py']; macOS arm64 local lab; clang strict optimized C23 assertions and ASan/UBSan via tests/determinant/run.py; no live host terminal, no physical device or visual acceptance; Linux/Windows unproved | Determinant ui/ taxonomy: surface, image, scroll, panel, text, list, tree, field, code, markdown, button, events, theme and format owners after the directory move | passed |

### `tests/determinant/ui/markdown`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/determinant/ui/markdown/terminal_markdown_view_test.c` | ✅ | 1792940728 | fdc6a8f317d440141c500c2828ff79b67ae6394acb91914b69678e7931f9ef19 | ['python3', 'tests/determinant/run.py']; macOS arm64 local lab; clang strict optimized C23 assertions and ASan/UBSan via tests/determinant/run.py; no live host terminal, no physical device or visual acceptance; Linux/Windows unproved | Determinant ui/ taxonomy: surface, image, scroll, panel, text, list, tree, field, code, markdown, button, events, theme and format owners after the directory move | passed |

### `tests/determinant/ui/panel`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/determinant/ui/panel/terminal_anchor_test.c` | ✅ | 1792940728 | 51a1ccd56ac214fd59e89519d1d9fcd39de80eb52c1fdab984cc6cdcab7f0504 | ['python3', 'tests/determinant/run.py']; macOS arm64 local lab; clang strict optimized C23 assertions and ASan/UBSan via tests/determinant/run.py; no live host terminal, no physical device or visual acceptance; Linux/Windows unproved | Determinant ui/ taxonomy: surface, image, scroll, panel, text, list, tree, field, code, markdown, button, events, theme and format owners after the directory move | passed |
| `tests/determinant/ui/panel/terminal_frame_test.c` | ✅ | 1792940728 | 0a32138aaf8bce1c4de73b7c484dd8321d5fd2851928de08f9df0120c276dd01 | ['python3', 'tests/determinant/run.py']; macOS arm64 local lab; clang strict optimized C23 assertions and ASan/UBSan via tests/determinant/run.py; no live host terminal, no physical device or visual acceptance; Linux/Windows unproved | Determinant ui/ taxonomy: surface, image, scroll, panel, text, list, tree, field, code, markdown, button, events, theme and format owners after the directory move | passed |
| `tests/determinant/ui/panel/terminal_panel_test.c` | ✅ | 1792940728 | 4b89d121f7b530a4bee6208517590b8c42a15301b2f6c3489a9d6f3abbe9c180 | ['python3', 'tests/determinant/run.py']; macOS arm64 local lab; clang strict optimized C23 assertions and ASan/UBSan via tests/determinant/run.py; no live host terminal, no physical device or visual acceptance; Linux/Windows unproved | Determinant ui/ taxonomy: surface, image, scroll, panel, text, list, tree, field, code, markdown, button, events, theme and format owners after the directory move | passed |

### `tests/determinant/ui/scroll`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/determinant/ui/scroll/terminal_scroll_glide_test.c` | ✅ | 1792940728 | 1a1432802a09cd2180a8811edbe1c0d516429e4dd7f1986f275d505383976bcb | ['python3', 'tests/determinant/run.py']; macOS arm64 local lab; clang strict optimized C23 assertions and ASan/UBSan via tests/determinant/run.py; no live host terminal, no physical device or visual acceptance; Linux/Windows unproved | Determinant ui/ taxonomy: surface, image, scroll, panel, text, list, tree, field, code, markdown, button, events, theme and format owners after the directory move | passed |

### `tests/determinant/ui/surface`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/determinant/ui/surface/terminal_canvas_test.c` | ✅ | 1792940728 | 320138c1919c73ef597bcc049ccc28a8142ddb4aaf90a0c4e0cc9a07de40b46e | ['python3', 'tests/determinant/run.py']; macOS arm64 local lab; clang strict optimized C23 assertions and ASan/UBSan via tests/determinant/run.py; no live host terminal, no physical device or visual acceptance; Linux/Windows unproved | Determinant ui/ taxonomy: surface, image, scroll, panel, text, list, tree, field, code, markdown, button, events, theme and format owners after the directory move | passed |
| `tests/determinant/ui/surface/terminal_reload_test.c` | ✅ | 1792940728 | 3eb156c226ba8ddd510dadd556320fb55d4ffbed49f489f620b2945d61c9cf29 | ['python3', 'tests/determinant/run.py']; macOS arm64 local lab; clang strict optimized C23 assertions and ASan/UBSan via tests/determinant/run.py; no live host terminal, no physical device or visual acceptance; Linux/Windows unproved | Determinant ui/ taxonomy: surface, image, scroll, panel, text, list, tree, field, code, markdown, button, events, theme and format owners after the directory move | passed |
| `tests/determinant/ui/surface/terminal_surface_test.c` | ✅ | 1792940728 | 2725072257a4717d3629026c925498ebb0ff0f45204ef94a1532bc783b5046b1 | ['python3', 'tests/determinant/run.py']; macOS arm64 local lab; clang strict optimized C23 assertions and ASan/UBSan via tests/determinant/run.py; no live host terminal, no physical device or visual acceptance; Linux/Windows unproved | Determinant ui/ taxonomy: surface, image, scroll, panel, text, list, tree, field, code, markdown, button, events, theme and format owners after the directory move | passed |
| `tests/determinant/ui/surface/terminal_test.c` | ✅ | 1792940728 | d02f9c710ec51afed67da2104268da49fd58a7de215201d32400852dc2062666 | ['python3', 'tests/determinant/run.py']; macOS arm64 local lab; clang strict optimized C23 assertions and ASan/UBSan via tests/determinant/run.py; no live host terminal, no physical device or visual acceptance; Linux/Windows unproved | Determinant ui/ taxonomy: surface, image, scroll, panel, text, list, tree, field, code, markdown, button, events, theme and format owners after the directory move | passed |

### `tests/determinant/ui/text`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/determinant/ui/text/terminal_status_bar_test.c` | ✅ | 1792940728 | 2a74be839cf2d2654aeb345fb137e5d2bc87b79b11c83fd07c7d86aad55373b5 | ['python3', 'tests/determinant/run.py']; macOS arm64 local lab; clang strict optimized C23 assertions and ASan/UBSan via tests/determinant/run.py; no live host terminal, no physical device or visual acceptance; Linux/Windows unproved | Determinant ui/ taxonomy: surface, image, scroll, panel, text, list, tree, field, code, markdown, button, events, theme and format owners after the directory move | passed |
| `tests/determinant/ui/text/terminal_text_test.c` | ✅ | 1792940728 | ebd13ab8d77783bb8eca6e1fef299794d856d39820fcc3f311fbca51ab5ce50e | ['python3', 'tests/determinant/run.py']; macOS arm64 local lab; clang strict optimized C23 assertions and ASan/UBSan via tests/determinant/run.py; no live host terminal, no physical device or visual acceptance; Linux/Windows unproved | Determinant ui/ taxonomy: surface, image, scroll, panel, text, list, tree, field, code, markdown, button, events, theme and format owners after the directory move | passed |
| `tests/determinant/ui/text/terminal_text_view_test.c` | ✅ | 1792940728 | 586448659aaeed555aa96be059e386853b9d29ac17a80d6e7e814a39ad0ed527 | ['python3', 'tests/determinant/run.py']; macOS arm64 local lab; clang strict optimized C23 assertions and ASan/UBSan via tests/determinant/run.py; no live host terminal, no physical device or visual acceptance; Linux/Windows unproved | Determinant ui/ taxonomy: surface, image, scroll, panel, text, list, tree, field, code, markdown, button, events, theme and format owners after the directory move | passed |

### `tests/determinant/ui/theme`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/determinant/ui/theme/terminal_appearance_test.c` | ✅ | 1792940728 | ac4c81f6a1a4157c7f45ad39249b7d2b69c86a82d6670450f2e98a927e095cc9 | ['python3', 'tests/determinant/run.py']; macOS arm64 local lab; clang strict optimized C23 assertions and ASan/UBSan via tests/determinant/run.py; no live host terminal, no physical device or visual acceptance; Linux/Windows unproved | Determinant ui/ taxonomy: surface, image, scroll, panel, text, list, tree, field, code, markdown, button, events, theme and format owners after the directory move | passed |

### `tests/determinant/ui/tree`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/determinant/ui/tree/terminal_tree_view_test.c` | ✅ | 1792940728 | 84de68d0927f3f977fab3244dc87e4a6288bfaeda882bd6295507a5a952079fe | ['python3', 'tests/determinant/run.py']; macOS arm64 local lab; clang strict optimized C23 assertions and ASan/UBSan via tests/determinant/run.py; no live host terminal, no physical device or visual acceptance; Linux/Windows unproved | Determinant ui/ taxonomy: surface, image, scroll, panel, text, list, tree, field, code, markdown, button, events, theme and format owners after the directory move | passed |

### `tests/func`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/func/readme_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/func/run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/func/src`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/func/src/func_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/graphvex`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/graphvex/board_test.c` | ✅ | 1792024894 | a6c39d861c59a6b6d6f420f90a586fe16cd4cc2e1e7f345bd54739d4d9a1d589 | ['/bin/sh', '-c', '/private/tmp/vexgraph-cmake-check-cmake/bin/board_test && /private/tmp/vexgraph-cmake-check-cmake/bin/graphics_test && /private/tmp/vexgraph-cmake-check-cmake/bin/vk_batch_test && /private/tmp/vexgraph-cmake-check-cmake/bin/property_pool_test && /private/tmp/vexgraph-cmake-check-cmake/bin/surface_test && /private/tmp/vexgraph-cmake-check-cmake/bin/render_loop_test && /private/tmp/vexgraph-cmake-check-cmake/bin/viewport_test']; macOS arm64 C23 debug; temporary CMake build; direct headless binaries; CTest marks these cases window-opt-in and disabled. | Graphvex constructor chooser owner tests run as headless unit binaries. | passed |
| `tests/graphvex/element_property_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/graphvex/element_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/graphvex/image_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/graphvex/compositor`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/graphvex/compositor/color_pass_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/graphvex/compositor/compositor_image_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/graphvex/compositor/compositor_scope_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/graphvex/compositor/compositor_submit_test.c` | ✅ | 1792853245 | 4085b65d7762f1871573e4bf85882df8b063e8a2e1397dd9c9e247b469adbdd7 | ['./cmake-build-debug/bin/compositor_submit_test']; macOS arm64; C23; debug build; direct owner binary rebuilt from the current test source in cmake-build-debug; no GPU or end-to-end presentation proof | Compositor submission recording, exact placement, borrowed output lifetime and preserved-state failures | passed |
| `tests/graphvex/compositor/compositor_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/graphvex/compositor/filter_gallery_fixture_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/graphvex/compositor/filter_pool_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/graphvex/compositor/gpu_scope_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/graphvex/filter`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/graphvex/filter/filter_functions_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/graphvex/filter/filter_type_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/graphvex/graphics`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/graphvex/graphics/capture_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/graphvex/graphics/graphics_test.c` | ✅ | 1792024894 | 92b2fa30f6030525b06372e676e58b9ad4cbdf9ff0ab5417931a862229b7b4c3 | ['/bin/sh', '-c', '/private/tmp/vexgraph-cmake-check-cmake/bin/board_test && /private/tmp/vexgraph-cmake-check-cmake/bin/graphics_test && /private/tmp/vexgraph-cmake-check-cmake/bin/vk_batch_test && /private/tmp/vexgraph-cmake-check-cmake/bin/property_pool_test && /private/tmp/vexgraph-cmake-check-cmake/bin/surface_test && /private/tmp/vexgraph-cmake-check-cmake/bin/render_loop_test && /private/tmp/vexgraph-cmake-check-cmake/bin/viewport_test']; macOS arm64 C23 debug; temporary CMake build; direct headless binaries; CTest marks these cases window-opt-in and disabled. | Graphvex constructor chooser owner tests run as headless unit binaries. | passed |
| `tests/graphvex/graphics/image_runs_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/graphvex/graphics/render_loop_test.c` | ✅ | 1792024894 | 9dec898a03702055c29028362bfa023ae772cc265f72e410a01272c7e69e468e | ['/bin/sh', '-c', '/private/tmp/vexgraph-cmake-check-cmake/bin/board_test && /private/tmp/vexgraph-cmake-check-cmake/bin/graphics_test && /private/tmp/vexgraph-cmake-check-cmake/bin/vk_batch_test && /private/tmp/vexgraph-cmake-check-cmake/bin/property_pool_test && /private/tmp/vexgraph-cmake-check-cmake/bin/surface_test && /private/tmp/vexgraph-cmake-check-cmake/bin/render_loop_test && /private/tmp/vexgraph-cmake-check-cmake/bin/viewport_test']; macOS arm64 C23 debug; temporary CMake build; direct headless binaries; CTest marks these cases window-opt-in and disabled. | Graphvex constructor chooser owner tests run as headless unit binaries. | passed |
| `tests/graphvex/graphics/viewport_test.c` | ✅ | 1792053557 | 66755a00b39b2a8755cd7748a21bb440ffdbaa68333d34c41098f11b3ef576c2 | ['./cmake-build-debug/bin/viewport_test']; Command-only evidence; no broader readiness claim | Viewport coordinate conversion and logical size return named values | passed |

### `tests/graphvex/lang`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/graphvex/lang/filter_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/graphvex/nio`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/graphvex/nio/pool_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/graphvex/nio/property_pool_test.c` | ✅ | 1792852622 | 2ba0f20c343a507f4912a5f21400057c5bf789f1fab841a69bcb42131535eeeb | ['./cmake-build-debug/bin/property_pool_test']; macOS arm64; C23; debug build; direct owner binary from cmake-build-debug; no live network | Graphvex constructor chooser owner tests run as headless unit binaries. | passed |

### `tests/graphvex/ui`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/graphvex/ui/element_bounds_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/graphvex/ui/element_image_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/graphvex/vulkan`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/graphvex/vulkan/clip_rounded_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/graphvex/vulkan/gpu_render_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/graphvex/vulkan/pipeline_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/graphvex/vulkan/resize_clip_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/graphvex/vulkan/sampled_image_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/graphvex/vulkan/surface_gpu_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/graphvex/vulkan/surface_test.c` | ✅ | 1792852622 | 4e300871b73285c59e139c4455da992455d51c7da1932202f42cdbd32c3d6a59 | ['./cmake-build-debug/bin/surface_test']; macOS arm64; C23; debug build; direct owner binary from cmake-build-debug; no live network | Graphvex constructor chooser owner tests run as headless unit binaries. | passed |
| `tests/graphvex/vulkan/vk_batch_test.c` | ✅ | 1792024894 | 53fdbb4d9ddb45b847ae62d1e3c946dac257c8a193f187225e6fc63bb49275e4 | ['/bin/sh', '-c', '/private/tmp/vexgraph-cmake-check-cmake/bin/board_test && /private/tmp/vexgraph-cmake-check-cmake/bin/graphics_test && /private/tmp/vexgraph-cmake-check-cmake/bin/vk_batch_test && /private/tmp/vexgraph-cmake-check-cmake/bin/property_pool_test && /private/tmp/vexgraph-cmake-check-cmake/bin/surface_test && /private/tmp/vexgraph-cmake-check-cmake/bin/render_loop_test && /private/tmp/vexgraph-cmake-check-cmake/bin/viewport_test']; macOS arm64 C23 debug; temporary CMake build; direct headless binaries; CTest marks these cases window-opt-in and disabled. | Graphvex constructor chooser owner tests run as headless unit binaries. | passed |
| `tests/graphvex/vulkan/vk_renderer_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/harness`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/harness/run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/harness/space`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/harness/space/channel_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/harness/space/message_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/harness/space/model_user_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/harness/space/space_arity_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/harness/space/support_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/harness/space/task_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/hotcwap/capability`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/hotcwap/capability/capability_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/hotcwap/hot`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/hotcwap/hot/cold_update_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/hotcwap/hot/cold_update_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/hotcwap/hot/hot_behavior_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/hotcwap/hot/hot_retire_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/hotcwap/hot/hot_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/hotcwap/hot/hot_trampoline_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/hotcwap/hot/ledger_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/hotcwap/hot/loader_trust_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/hotcwap/hot/manifest_adversarial_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/hotcwap/hot/manifest_hot_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/hotcwap/hot/manifest_rollback_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/hotcwap/hot/manifest_uninstall_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/hotcwap/hot/retire_ring_overflow_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/hotcwap/hot/shutdown_order_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/hotcwap/hot/throwable_test.c` | ✅ | 1792029656 | 2ff43cc0216dce0a5cdb2d25f626434efa910f6247094d2e6780d8cd67138de6 | ['cmake-build-debug/bin/throwable_test']; hotcwap | Hotcwap Throwable consumes the Exception(...) constructor and preserves fatal/reporting behavior | passed |
| `tests/hotcwap/hot/two_dylib_swap_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/hotcwap/hot/uninstall_guard_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/hotcwap/hot/wrong_binary_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/hotcwap/kernel`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/hotcwap/kernel/application_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/hotcwap/kernel/commandline_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/hotcwap/kernel/console_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/hotcwap/kernel/kernel_function_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/hotcwap/kernel/kernel_lifecycle_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/hotcwap/kernel/process_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/hotcwap/permission`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/hotcwap/permission/permission_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/hotcwap/spoke`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/hotcwap/spoke/spoke_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/hotcwap/window`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/hotcwap/window/bridge_seam_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/hotcwap/window/present_surface_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/hotcwap/window/traffic_light_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/hotcwap/window/window_event_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/hotcwap/window/window_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/language`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/language/run.py` | ✅ | 1792595983 | 83206939520e28cc09b3ae08d780784ebe85f16aa6e2621721bd2976e41ca904 | ['python3', 'tests/language/run.py']; macOS arm64 local lab; strict C23 -Wall -Wextra -Werror with assertions active; ASan/UBSan; lexical subset only, no parser/discovery/Semicolon UI or non-macOS proof | Language value owners, explicit C23 adapter, snapshot engine, scalable registry and project/index contracts | passed |

### `tests/language/adapters/c`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/language/adapters/c/c23_highlights_test.c` | ✅ | 1792741059 | a7187dc1843f3b2c569b03ef399288f8c73e685451bc32eeab05ad45ede149eb | ['python3', 'tests/language/run.py']; macOS arm64 local lab; strict C23 -Wall -Wextra -Werror with assertions active; ASan/UBSan; no parser, preprocessor, Semicolon appearance or non-macOS proof | C23 highlight roles: include-header &lt;...&gt; as one string span after #include, quoted include string, ordinary &lt; as operator, ordered coverage, bounded projections | passed |
| `tests/language/adapters/c/c23_inlay_hints_test.c` | ✅ | 1792595983 | 537e2c531f91ac9a3d4d5c471242afea38e33b35ddb51aac14c0a2d94703e594 | ['python3', 'tests/language/run.py']; macOS arm64 local lab; strict C23 -Wall -Wextra -Werror with assertions active; ASan/UBSan; lexical subset only, no parser/discovery/Semicolon UI or non-macOS proof | Language value owners, explicit C23 adapter, snapshot engine, scalable registry and project/index contracts | passed |
| `tests/language/adapters/c/c23_lex_step_test.c` | ✅ | 1792595983 | 8de48a2caf10d96e4c86fae0db970e3f9f7627847c31eb645899c1e5e1327f1d | ['python3', 'tests/language/run.py']; macOS arm64 local lab; strict C23 -Wall -Wextra -Werror with assertions active; ASan/UBSan; lexical subset only, no parser/discovery/Semicolon UI or non-macOS proof | Language value owners, explicit C23 adapter, snapshot engine, scalable registry and project/index contracts | passed |
| `tests/language/adapters/c/c23_lexer_run.py` | ✅ | 1792739887 | b6798da5281a9127df8f484969a1879c3efa0f196bccc0c3577766a4a189b84e | ['python3', 'tests/language/run.py']; macOS arm64 local lab; strict C23 -Wall -Wextra -Werror with assertions active; ASan/UBSan; lexical presentation classification only, no parser/preprocessor/semantic resolution, Semicolon appearance or non-macOS proof | Language C23 lexical owners: ordered keyword/literal/comment spans, distinct regular/doc comments, heuristic type/function/variable/member/macro roles, line-start #include/#define marker and directive roles with in-code # remaining punctuation, Unicode boundaries, constructor arity/recovery, growable output and bounded projections | passed |
| `tests/language/adapters/c/c23_lexer_test.c` | ❌ | 1792595983 | 6ae6c4924ec68a8224676e00d670e8c1f318dd39c1ab8cd0b0e94590b92d0691 | ['python3', 'tests/language/run.py']; macOS arm64 local lab; strict C23 -Wall -Wextra -Werror with assertions active; ASan/UBSan; lexical subset only, no parser/discovery/Semicolon UI or non-macOS proof | Language value owners, explicit C23 adapter, snapshot engine, scalable registry and project/index contracts | stale — content changed; rerun required |

### `tests/language/adapters/c23`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/language/adapters/c23/c23_adapter_run.py` | ✅ | 1792595983 | 353fc86efd6fcd614c7c4c26f940144a5110cbfb2fa602ea25b17276476fd6b6 | ['python3', 'tests/language/run.py']; macOS arm64 local lab; strict C23 -Wall -Wextra -Werror with assertions active; ASan/UBSan; lexical subset only, no parser/discovery/Semicolon UI or non-macOS proof | Language value owners, explicit C23 adapter, snapshot engine, scalable registry and project/index contracts | passed |
| `tests/language/adapters/c23/c23_adapter_test.c` | ✅ | 1792853263 | 2f6c0d1243a6d07e9dc2172a5baabbdb46b17fd25f96fffed9fccc8892213888 | ['python3', 'tests/language/run.py']; macOS arm64 local lab; strict C23 -Wall -Wextra -Werror with assertions active; ASan/UBSan; lexical subset only, no parser/discovery/Semicolon UI or non-macOS proof | Language value, engine and C23 adapter owners | passed |

### `tests/language/adapters/diff`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/language/adapters/diff/diff_adapter_test.c` | ✅ | 1792558284 | e5a27320c9726aadeac1036300489c1d746cd639a3991ed1fdd75fa1ab5f4937 | ['python3', 'tests/language/run.py']; macOS arm64; strict C23 -Wall -Wextra -Werror; ASan/UBSan; offline value/adapter layer only; no parser, preprocessor or host integration | Language value owners plus delegated C23 adapter owners: construction/accessor/role/span/diagnostic/diff proof, lexer and inlay strict/ASan owners, and eight constructor-arity negatives | passed |

### `tests/language/analysis`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/language/analysis/diagnostic_test.c` | ✅ | 1792558284 | 35992ba7441a5f2c5bcf0484c0cf16dcbb474f6cede42357126b5a206497cb52 | ['python3', 'tests/language/run.py']; macOS arm64; strict C23 -Wall -Wextra -Werror; ASan/UBSan; offline value/adapter layer only; no parser, preprocessor or host integration | Language value owners plus delegated C23 adapter owners: construction/accessor/role/span/diagnostic/diff proof, lexer and inlay strict/ASan owners, and eight constructor-arity negatives | passed |
| `tests/language/analysis/syntax_span_test.c` | ✅ | 1792558284 | df884b68c2373041c023516151f41cd020a1c91ddfa57b822562a40353930aa1 | ['python3', 'tests/language/run.py']; macOS arm64; strict C23 -Wall -Wextra -Werror; ASan/UBSan; offline value/adapter layer only; no parser, preprocessor or host integration | Language value owners plus delegated C23 adapter owners: construction/accessor/role/span/diagnostic/diff proof, lexer and inlay strict/ASan owners, and eight constructor-arity negatives | passed |

### `tests/language/document`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/language/document/line_index_test.c` | ✅ | 1792595983 | 81714a547bb64fccb244a4ee81587b7a680a5d21e3ab9536a6b3c25ba4130b72 | ['python3', 'tests/language/run.py']; macOS arm64 local lab; strict C23 -Wall -Wextra -Werror with assertions active; ASan/UBSan; lexical subset only, no parser/discovery/Semicolon UI or non-macOS proof | Language value owners, explicit C23 adapter, snapshot engine, scalable registry and project/index contracts | passed |
| `tests/language/document/source_range_test.c` | ✅ | 1792558284 | a33756531a18cb31b8bef1706b1b9a72789b867fbca5abb34e70853ecde065e4 | ['python3', 'tests/language/run.py']; macOS arm64; strict C23 -Wall -Wextra -Werror; ASan/UBSan; offline value/adapter layer only; no parser, preprocessor or host integration | Language value owners plus delegated C23 adapter owners: construction/accessor/role/span/diagnostic/diff proof, lexer and inlay strict/ASan owners, and eight constructor-arity negatives | passed |
| `tests/language/document/text_document_test.c` | ✅ | 1792595983 | 61f173e20d259d302ed60ac312f5f6d6975ccfc17f26d25b4f4a83fbc70ae06b | ['python3', 'tests/language/run.py']; macOS arm64 local lab; strict C23 -Wall -Wextra -Werror with assertions active; ASan/UBSan; lexical subset only, no parser/discovery/Semicolon UI or non-macOS proof | Language value owners, explicit C23 adapter, snapshot engine, scalable registry and project/index contracts | passed |
| `tests/language/document/text_snapshot_test.c` | ✅ | 1792595983 | afba38b745c7289c12fc7c3ef47604c1a1c5d42090ac9dbeb866e23a4185c410 | ['python3', 'tests/language/run.py']; macOS arm64 local lab; strict C23 -Wall -Wextra -Werror with assertions active; ASan/UBSan; lexical subset only, no parser/discovery/Semicolon UI or non-macOS proof | Language value owners, explicit C23 adapter, snapshot engine, scalable registry and project/index contracts | passed |

### `tests/language/index`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/language/index/dependency_graph_test.c` | ✅ | 1792595983 | 3befdc8f1d38390f0becc5087c85cf9ac98e3421a4c690ebb6ebab91cd944738 | ['python3', 'tests/language/run.py']; macOS arm64 local lab; strict C23 -Wall -Wextra -Werror with assertions active; ASan/UBSan; lexical subset only, no parser/discovery/Semicolon UI or non-macOS proof | Language value owners, explicit C23 adapter, snapshot engine, scalable registry and project/index contracts | passed |
| `tests/language/index/file_analysis_test.c` | ✅ | 1792595983 | 2d63742544f224c7bd4703e089af259e9758315582e04768c001d13e1a6e5a2f | ['python3', 'tests/language/run.py']; macOS arm64 local lab; strict C23 -Wall -Wextra -Werror with assertions active; ASan/UBSan; lexical subset only, no parser/discovery/Semicolon UI or non-macOS proof | Language value owners, explicit C23 adapter, snapshot engine, scalable registry and project/index contracts | passed |
| `tests/language/index/project_index_test.c` | ✅ | 1792595983 | 72543c45cf7a41646f6724d69f938d001d14b81df7f334981bd1ecb2af7e73a9 | ['python3', 'tests/language/run.py']; macOS arm64 local lab; strict C23 -Wall -Wextra -Werror with assertions active; ASan/UBSan; lexical subset only, no parser/discovery/Semicolon UI or non-macOS proof | Language value owners, explicit C23 adapter, snapshot engine, scalable registry and project/index contracts | passed |

### `tests/language/lang`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/language/lang/language_adapter_test.c` | ✅ | 1792595983 | ce0eab1dc271b896edf1972f00eefe6cd8455460f89057f5b912a4fb5edc5d7b | ['python3', 'tests/language/run.py']; macOS arm64 local lab; strict C23 -Wall -Wextra -Werror with assertions active; ASan/UBSan; lexical subset only, no parser/discovery/Semicolon UI or non-macOS proof | Language value owners, explicit C23 adapter, snapshot engine, scalable registry and project/index contracts | passed |
| `tests/language/lang/language_engine_test.c` | ✅ | 1792853263 | 6cee3da005c638d2af66c28d9eec55d03a5606d0eb910f9f57fa41e8b9ace9d0 | ['python3', 'tests/language/run.py']; macOS arm64 local lab; strict C23 -Wall -Wextra -Werror with assertions active; ASan/UBSan; lexical subset only, no parser/discovery/Semicolon UI or non-macOS proof | Language value, engine and C23 adapter owners | passed |
| `tests/language/lang/language_lex_result_test.c` | ✅ | 1792853263 | 44797374e0df7fbef4c25999ab72e2e5329c86b89d763ca0d85e35af0cc3dee6 | ['python3', 'tests/language/run.py']; macOS arm64 local lab; strict C23 -Wall -Wextra -Werror with assertions active; ASan/UBSan; lexical subset only, no parser/discovery/Semicolon UI or non-macOS proof | Language value, engine and C23 adapter owners | passed |
| `tests/language/lang/language_registry_test.c` | ✅ | 1792595983 | ca9f6f2ed22fb95f0cd436dab21ec7454dc9cc7d9c19230f95652cec6c998e9f | ['python3', 'tests/language/run.py']; macOS arm64 local lab; strict C23 -Wall -Wextra -Werror with assertions active; ASan/UBSan; lexical subset only, no parser/discovery/Semicolon UI or non-macOS proof | Language value owners, explicit C23 adapter, snapshot engine, scalable registry and project/index contracts | passed |

### `tests/language/project`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/language/project/build_target_test.c` | ✅ | 1792595983 | 154cbceddc1a92ad328aca05bb5255d703d6f026d7da016c9635281e30c349c4 | ['python3', 'tests/language/run.py']; macOS arm64 local lab; strict C23 -Wall -Wextra -Werror with assertions active; ASan/UBSan; lexical subset only, no parser/discovery/Semicolon UI or non-macOS proof | Language value owners, explicit C23 adapter, snapshot engine, scalable registry and project/index contracts | passed |
| `tests/language/project/language_project_test.c` | ✅ | 1792595983 | 41d4ccdce3b2ad497ee8d5de6e836e6f20bc9736586d3949ce897db1f0842ec1 | ['python3', 'tests/language/run.py']; macOS arm64 local lab; strict C23 -Wall -Wextra -Werror with assertions active; ASan/UBSan; lexical subset only, no parser/discovery/Semicolon UI or non-macOS proof | Language value owners, explicit C23 adapter, snapshot engine, scalable registry and project/index contracts | passed |
| `tests/language/project/project_configuration_test.c` | ✅ | 1792595983 | 3f82d1419e119d227fb1a05eda09553b67e311b421a68c4a50cb710bc38a8bfd | ['python3', 'tests/language/run.py']; macOS arm64 local lab; strict C23 -Wall -Wextra -Werror with assertions active; ASan/UBSan; lexical subset only, no parser/discovery/Semicolon UI or non-macOS proof | Language value owners, explicit C23 adapter, snapshot engine, scalable registry and project/index contracts | passed |
| `tests/language/project/project_file_test.c` | ✅ | 1792595983 | 3faf9a520bf39823ea3d284b7ff68c5767f8d61c1948daf174da4c4f4ec5db5e | ['python3', 'tests/language/run.py']; macOS arm64 local lab; strict C23 -Wall -Wextra -Werror with assertions active; ASan/UBSan; lexical subset only, no parser/discovery/Semicolon UI or non-macOS proof | Language value owners, explicit C23 adapter, snapshot engine, scalable registry and project/index contracts | passed |

### `tests/language/semantic`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/language/semantic/reference_test.c` | ✅ | 1792558284 | 07ced5a5449366a03b1a98908caf54457153a4010118a5525dcfacaae5cbe2c6 | ['python3', 'tests/language/run.py']; macOS arm64; strict C23 -Wall -Wextra -Werror; ASan/UBSan; offline value/adapter layer only; no parser, preprocessor or host integration | Language value owners plus delegated C23 adapter owners: construction/accessor/role/span/diagnostic/diff proof, lexer and inlay strict/ASan owners, and eight constructor-arity negatives | passed |
| `tests/language/semantic/symbol_test.c` | ✅ | 1792558284 | 506fe7cf58d390790c90db57b8e283392cf2977105b4d668e38e121b61e125bb | ['python3', 'tests/language/run.py']; macOS arm64; strict C23 -Wall -Wextra -Werror; ASan/UBSan; offline value/adapter layer only; no parser, preprocessor or host integration | Language value owners plus delegated C23 adapter owners: construction/accessor/role/span/diagnostic/diff proof, lexer and inlay strict/ASan owners, and eight constructor-arity negatives | passed |

### `tests/language/style`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/language/style/style_key_registry_test.c` | ✅ | 1792558284 | ab2b30f418c171bf6132fa847b3f618ed7cc8112d9de14a786a243e546f9703f | ['python3', 'tests/language/run.py']; macOS arm64; strict C23 -Wall -Wextra -Werror; ASan/UBSan; offline value/adapter layer only; no parser, preprocessor or host integration | Language value owners plus delegated C23 adapter owners: construction/accessor/role/span/diagnostic/diff proof, lexer and inlay strict/ASan owners, and eight constructor-arity negatives | passed |
| `tests/language/style/text_style_test.c` | ✅ | 1792558284 | f0afe718a2b8cd609e00a082d32a79b94ffaad45e69348f8ad8ff331690a4662 | ['python3', 'tests/language/run.py']; macOS arm64; strict C23 -Wall -Wextra -Werror; ASan/UBSan; offline value/adapter layer only; no parser, preprocessor or host integration | Language value owners plus delegated C23 adapter owners: construction/accessor/role/span/diagnostic/diff proof, lexer and inlay strict/ASan owners, and eight constructor-arity negatives | passed |

### `tests/language/syntax`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/language/syntax/role_test.c` | ✅ | 1792595983 | a51199f098a81f480c32464bdcc7b71f6c6ec8225c4726aebb8e1571152ee3f7 | ['python3', 'tests/language/run.py']; macOS arm64 local lab; strict C23 -Wall -Wextra -Werror with assertions active; ASan/UBSan; lexical subset only, no parser/discovery/Semicolon UI or non-macOS proof | Language value owners, explicit C23 adapter, snapshot engine, scalable registry and project/index contracts | passed |
| `tests/language/syntax/token_stream_test.c` | ✅ | 1792595983 | 0cc8c0fe6befd8bd2b8ef45d68777e7e9a773ab32fc24c7cf9d328ced03c09a5 | ['python3', 'tests/language/run.py']; macOS arm64 local lab; strict C23 -Wall -Wextra -Werror with assertions active; ASan/UBSan; lexical subset only, no parser/discovery/Semicolon UI or non-macOS proof | Language value owners, explicit C23 adapter, snapshot engine, scalable registry and project/index contracts | passed |

### `tests/language/text`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/language/text/bounded_text_test.c` | ✅ | 1792558284 | 17516a4d81b6eb0036c1f35da609d177382e070f0bae4f1f7e1d410ef34d366a | ['python3', 'tests/language/run.py']; macOS arm64; strict C23 -Wall -Wextra -Werror; ASan/UBSan; offline value/adapter layer only; no parser, preprocessor or host integration | Language value owners plus delegated C23 adapter owners: construction/accessor/role/span/diagnostic/diff proof, lexer and inlay strict/ASan owners, and eight constructor-arity negatives | passed |

### `tests/language/token`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/language/token/token_test.c` | ✅ | 1792558284 | 6f09989108f1fb454d3eeb7339e7d433f126c29d9964d420f2cc4f987e95e261 | ['python3', 'tests/language/run.py']; macOS arm64; strict C23 -Wall -Wextra -Werror; ASan/UBSan; offline value/adapter layer only; no parser, preprocessor or host integration | Language value owners plus delegated C23 adapter owners: construction/accessor/role/span/diagnostic/diff proof, lexer and inlay strict/ASan owners, and eight constructor-arity negatives | passed |

### `tests/primeagen`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/primeagen/launcher_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/readme_test.py` | ✅ | 1792852513 | c8f7632a992832c4bbcc31c7c01dca8e8b2c1ca1db0c3656e07741ce9405a63a | ['python3', '-B', 'tests/primeagen/readme_test.py']; macOS arm64; source/document contract and explicit dependency-root build; no appearance or provider integration proof | Primeagen workspace-tree, Nerd Font, collapse controls and standalone competency documentation | passed |
| `tests/primeagen/run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/primeagen/cli`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/primeagen/cli/appearance_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/cli/main_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/cli/preview_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/cli/screen_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/cli/tui_test.py` | ❌ | 1792677171 | 5b3891b6d507e993887faf477ea4ed89a0e57e54b5ca2ab3af0e4ee95f4c12a2 | ['python3', '-B', 'tests/primeagen/cli/tui_test.py']; macOS arm64; strict C23 and ASan/UBSan; headless ncurses; appearance/physical terminal acceptance unproved | Primeagen explorer rendering, selection, folding, scroll and hidden-tree behavior | stale — content changed; rerun required |
| `tests/primeagen/cli/update_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/cli/update_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/cli/view_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/primeagen/native`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/primeagen/native/request_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/primeagen/personality`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/primeagen/personality/owo_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/primeagen/session`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/primeagen/session/controlled_consent_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/session/session_answer_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/session/session_answer_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/session/session_bridge_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/session/session_consent_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/primeagen/src`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/primeagen/src/agent_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/src/controlled_session_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/src/env_file_native_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/src/env_file_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/src/env_file_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/src/json_admit_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/src/json_admit_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/src/json_input_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/src/process_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/src/provider_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/src/session_host_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/src/settings_native_test.py` | ✅ | 1792024904 | a1af6148750b42a332e509842ba834b32737330447c9f3a1207c01987c8eb66f | ['python3', '-B', 'tests/primeagen/src/settings_native_test.py']; macOS arm64; clang C23 strict plus ASan/UBSan via settings_native_test.py; disposable VEX_MANIFEST directory; current suite/ source roots. | Primeagen settings constructor owner run in strict and sanitized native builds. | passed |
| `tests/primeagen/src/settings_test.c` | ✅ | 1792024904 | 8b312e676e30f26b5e1b229c93a47175459e8c726b13a1ccc92f7667ebb7849a | ['python3', '-B', 'tests/primeagen/src/settings_native_test.py']; macOS arm64; clang C23 strict plus ASan/UBSan via settings_native_test.py; disposable VEX_MANIFEST directory; current suite/ source roots. | Primeagen settings constructor owner run in strict and sanitized native builds. | passed |
| `tests/primeagen/src/tools_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/src/transport_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/primeagen/tools`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/primeagen/tools/bash_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/tools/create_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/tools/delete_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/tools/edit_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/tools/fs_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/tools/fs_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/tools/list_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/tools/main_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/tools/read_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/tools/websearch_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/tools/write_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/primeagen/tui`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/primeagen/tui/markdown_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/tui/tui_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/primeagen/tui/utf8_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/primeagen/tui/event`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/primeagen/tui/event/mouse_event_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/relational-engine`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/relational-engine/native_memory_doc_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/native_run.py` | ✅ | 1792059834 | 40c2b0bc698afa1efd8823441715aa39884175b64e69e3a974920f13d7d2a811 | ['python3', '-B', 'tests/relational-engine/native_run.py']; macOS arm64; strict+release+sanitized (ASan/UBSan) modes; io/clipboard owners SKIP without RE_TEST_SYSTEM_CLIPBOARD=1; TSan mode not run | Engine native Memory owners for the final 32-byte header: id+BE6C, hash veto, u64 length and the object/primitive redirect; slab+bump exhaustion, realloc preservation, refusal counting, hash tamper rejection, transient lifetime | passed |
| `tests/relational-engine/preferences_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/primer_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/scaffold_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/relational-engine/io`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/relational-engine/io/cache_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/io/clipboard_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/io/file_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/io/filewriter_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/io/frame_inbox_test.c` | ✅ | 1792070544 | 39bf87d2c88abb3ab1c32e24e922a81d4516f83ce9f44052d1b6995689ef1649 | ['clang', '-std=gnu23', '-Wall', '-Wextra', '-Werror', '-DUNDEBUG', '-I', 'suite/ecosystem/relational-engine/src', '-I', 'suite/ecosystem/vexspoke/src', '-I', 'tests', 'tests/relational-engine/io/frame_inbox_test.c', 'suite/ecosystem/relational-engine/src/io/frame_inbox.c', 'suite/ecosystem/relational-engine/src/nio/mem.c', 'suite/ecosystem/relational-engine/src/type/type.c', 'suite/ecosystem/vexspoke/src/atomic/spin.c', '-o', '/tmp/frame_inbox_test']; Current macOS arm64 host; strict warning build and runtime inbox behavior. No WebSocket protocol or socket adapter coverage. | FrameInbox strict C23 owner test | passed |
| `tests/relational-engine/io/hot_file_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/io/log_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/io/logparser_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/io/process_spawn_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/io/vexhome_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/relational-engine/nio`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/relational-engine/nio/fixed_mapped_file_abi_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/nio/growable_mapped_file_abi_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/nio/mem_exhaustion_test.c` | ✅ | 1792059834 | d04601a8a4852e96629453ffa1bdb04740b9d511ce5acaea212bae8357719aef | ['python3', '-B', 'tests/relational-engine/native_run.py']; macOS arm64; strict+release+sanitized (ASan/UBSan) modes; io/clipboard owners SKIP without RE_TEST_SYSTEM_CLIPBOARD=1; TSan mode not run | Engine native Memory owners for the final 32-byte header: id+BE6C, hash veto, u64 length and the object/primitive redirect; slab+bump exhaustion, realloc preservation, refusal counting, hash tamper rejection, transient lifetime | passed |
| `tests/relational-engine/nio/mem_test.c` | ✅ | 1792059834 | 51a278683f801b30cc0ae04df3b0789d10237615b531aa33d564ba12bee49bd4 | ['python3', '-B', 'tests/relational-engine/native_run.py']; macOS arm64; strict+release+sanitized (ASan/UBSan) modes; io/clipboard owners SKIP without RE_TEST_SYSTEM_CLIPBOARD=1; TSan mode not run | Engine native Memory owners for the final 32-byte header: id+BE6C, hash veto, u64 length and the object/primitive redirect; slab+bump exhaustion, realloc preservation, refusal counting, hash tamper rejection, transient lifetime | passed |
| `tests/relational-engine/nio/relational_memory_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/nio/transient_lifetime_test.c` | ✅ | 1792059834 | 42054833b99d8dfe8f4909ea7bb040b80cd71a5188f8243d2fad939cfcf350d4 | ['python3', '-B', 'tests/relational-engine/native_run.py']; macOS arm64; strict+release+sanitized (ASan/UBSan) modes; io/clipboard owners SKIP without RE_TEST_SYSTEM_CLIPBOARD=1; TSan mode not run | Engine native Memory owners for the final 32-byte header: id+BE6C, hash veto, u64 length and the object/primitive redirect; slab+bump exhaustion, realloc preservation, refusal counting, hash tamper rejection, transient lifetime | passed |

### `tests/relational-engine/rust`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/relational-engine/rust/run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/rust/sanitizer_run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/relational-engine/rust/ffi`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/relational-engine/rust/ffi/memory_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/rust/ffi/memory_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/rust/ffi/row_pool_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/rust/ffi/row_pool_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/rust/ffi/variable_registry_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/rust/ffi/variable_registry_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/relational-engine/rust/io`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/relational-engine/rust/io/preallocated_failure_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/rust/io/preallocated_file_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/rust/io/preallocation_error_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/rust/io/preallocation_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/relational-engine/rust/nio`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/relational-engine/rust/nio/chunk_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/rust/nio/fixed_mapped_file_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/rust/nio/growable_mapped_file_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/rust/nio/handle_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/rust/nio/mapping_error_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/rust/nio/mem_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/rust/nio/row_chunk_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/rust/nio/row_handle_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/rust/nio/typed_chunk_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/relational-engine/rust/primitives`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/relational-engine/rust/primitives/atomic_string_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/rust/primitives/string_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/relational-engine/rust/struct`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/relational-engine/rust/struct/chunked_list_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/rust/struct/row_pool_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/rust/struct/typed_pool_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/relational-engine/rust/variable`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/relational-engine/rust/variable/variable_registry_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/relational-engine/rust/variable/variable_slot_test.rs` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/relational-engine/search/primitives`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/relational-engine/search/primitives/name_search_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/relational-engine/type`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/relational-engine/type/type_algebra_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/repos`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/repos/artwork_headers_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/repos/vex-graph`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/repos/vex-graph/readme_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/semicolon`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/semicolon/gitignore_rail_test.py` | ❌ | 1792853525 | 10a472ba9e0f1aa5a805f0fc9936fcaf57ed9dc7635fb163085445a3e412820e | ['python3', '-c', 'import subprocess,sys; names=["readme_test.py","tui_main_test.py","rail_interaction_test.py","rail_format_test.py","run_console_test.py","gitignore_rail_test.py","gutter_alignment_test.py","mouse_capture_test.py","icon_catalog_test.py","install_command_test.py"]; [subprocess.run([sys.executable,"tests/semicolon/"+name],check=True,timeout=240) for name in names]']; macOS arm64 local lab; strict native C23 build, scripted PTY xterm-256color and disposable fixture paths; aggregate watchdog 900s, each owner 240s; no physical-terminal visual acceptance, windowed launch or non-macOS runtime proof; Linux stat nanosecond branch is guarded source and awaits CI | Semicolon TUI regression aggregate after the portable stat-nanosecond fix: tabs/tree/caret/autosave, exact bounded undo/redo autosaved bytes, gutter alignment, wheel and divider scrolling, mouse capture, console, icons, launcher/install and mechanical README boundary all pass through the current tui-main.c | failed (exit 124) |
| `tests/semicolon/gutter_alignment_test.py` | ❌ | 1792853525 | 4a599b1309fa00c39fb3e5763f105792a69326ee64b839bb5eb75eee9e63dde1 | ['python3', '-c', 'import subprocess,sys; names=["readme_test.py","tui_main_test.py","rail_interaction_test.py","rail_format_test.py","run_console_test.py","gitignore_rail_test.py","gutter_alignment_test.py","mouse_capture_test.py","icon_catalog_test.py","install_command_test.py"]; [subprocess.run([sys.executable,"tests/semicolon/"+name],check=True,timeout=240) for name in names]']; macOS arm64 local lab; strict native C23 build, scripted PTY xterm-256color and disposable fixture paths; aggregate watchdog 900s, each owner 240s; no physical-terminal visual acceptance, windowed launch or non-macOS runtime proof; Linux stat nanosecond branch is guarded source and awaits CI | Semicolon TUI regression aggregate after the portable stat-nanosecond fix: tabs/tree/caret/autosave, exact bounded undo/redo autosaved bytes, gutter alignment, wheel and divider scrolling, mouse capture, console, icons, launcher/install and mechanical README boundary all pass through the current tui-main.c | failed (exit 124) |
| `tests/semicolon/icon_catalog_test.py` | ❌ | 1792853525 | 55e7bff04ecb750a4437074c9d784c55c983f4868ce105ceb92762724f69934f | ['python3', '-c', 'import subprocess,sys; names=["readme_test.py","tui_main_test.py","rail_interaction_test.py","rail_format_test.py","run_console_test.py","gitignore_rail_test.py","gutter_alignment_test.py","mouse_capture_test.py","icon_catalog_test.py","install_command_test.py"]; [subprocess.run([sys.executable,"tests/semicolon/"+name],check=True,timeout=240) for name in names]']; macOS arm64 local lab; strict native C23 build, scripted PTY xterm-256color and disposable fixture paths; aggregate watchdog 900s, each owner 240s; no physical-terminal visual acceptance, windowed launch or non-macOS runtime proof; Linux stat nanosecond branch is guarded source and awaits CI | Semicolon TUI regression aggregate after the portable stat-nanosecond fix: tabs/tree/caret/autosave, exact bounded undo/redo autosaved bytes, gutter alignment, wheel and divider scrolling, mouse capture, console, icons, launcher/install and mechanical README boundary all pass through the current tui-main.c | failed (exit 124) |
| `tests/semicolon/install_command_test.py` | ❌ | 1792853525 | 7f6de64f5c3bf91ec2d49aa84a3e43ceecfef9033236c8628d18a60fb2dd2914 | ['python3', '-c', 'import subprocess,sys; names=["readme_test.py","tui_main_test.py","rail_interaction_test.py","rail_format_test.py","run_console_test.py","gitignore_rail_test.py","gutter_alignment_test.py","mouse_capture_test.py","icon_catalog_test.py","install_command_test.py"]; [subprocess.run([sys.executable,"tests/semicolon/"+name],check=True,timeout=240) for name in names]']; macOS arm64 local lab; strict native C23 build, scripted PTY xterm-256color and disposable fixture paths; aggregate watchdog 900s, each owner 240s; no physical-terminal visual acceptance, windowed launch or non-macOS runtime proof; Linux stat nanosecond branch is guarded source and awaits CI | Semicolon TUI regression aggregate after the portable stat-nanosecond fix: tabs/tree/caret/autosave, exact bounded undo/redo autosaved bytes, gutter alignment, wheel and divider scrolling, mouse capture, console, icons, launcher/install and mechanical README boundary all pass through the current tui-main.c | failed (exit 124) |
| `tests/semicolon/launcher_language_test.py` | ✅ | 1792740145 | 925b5ba1062e3d5c688a594b35feca0933f5a07e6470c5bf7083c89d59e475aa | ['python3', 'tests/semicolon/launcher_language_test.py']; macOS arm64 local lab; strict optimized C23 assertions; disposable fake builder/artifact; no real compiler or physical-terminal visual proof | Semicolon Language launcher invalidation after the C23Highlights directive-role change: real Language header/source dependency tracking, mtime invalidation and unchanged-build reuse | passed |
| `tests/semicolon/mouse_capture_test.py` | ❌ | 1792853525 | a615e78b592564869642309751bcd5d31747c0f72efa6264c6cec55d6b1657ba | ['python3', '-c', 'import subprocess,sys; names=["readme_test.py","tui_main_test.py","rail_interaction_test.py","rail_format_test.py","run_console_test.py","gitignore_rail_test.py","gutter_alignment_test.py","mouse_capture_test.py","icon_catalog_test.py","install_command_test.py"]; [subprocess.run([sys.executable,"tests/semicolon/"+name],check=True,timeout=240) for name in names]']; macOS arm64 local lab; strict native C23 build, scripted PTY xterm-256color and disposable fixture paths; aggregate watchdog 900s, each owner 240s; no physical-terminal visual acceptance, windowed launch or non-macOS runtime proof; Linux stat nanosecond branch is guarded source and awaits CI | Semicolon TUI regression aggregate after the portable stat-nanosecond fix: tabs/tree/caret/autosave, exact bounded undo/redo autosaved bytes, gutter alignment, wheel and divider scrolling, mouse capture, console, icons, launcher/install and mechanical README boundary all pass through the current tui-main.c | failed (exit 124) |
| `tests/semicolon/rail_format_test.py` | ❌ | 1792853525 | 7af7390ea756c80eb1ac9289c2caef5e20e6fc7b79360abfba428a002a80dce1 | ['python3', '-c', 'import subprocess,sys; names=["readme_test.py","tui_main_test.py","rail_interaction_test.py","rail_format_test.py","run_console_test.py","gitignore_rail_test.py","gutter_alignment_test.py","mouse_capture_test.py","icon_catalog_test.py","install_command_test.py"]; [subprocess.run([sys.executable,"tests/semicolon/"+name],check=True,timeout=240) for name in names]']; macOS arm64 local lab; strict native C23 build, scripted PTY xterm-256color and disposable fixture paths; aggregate watchdog 900s, each owner 240s; no physical-terminal visual acceptance, windowed launch or non-macOS runtime proof; Linux stat nanosecond branch is guarded source and awaits CI | Semicolon TUI regression aggregate after the portable stat-nanosecond fix: tabs/tree/caret/autosave, exact bounded undo/redo autosaved bytes, gutter alignment, wheel and divider scrolling, mouse capture, console, icons, launcher/install and mechanical README boundary all pass through the current tui-main.c | failed (exit 124) |
| `tests/semicolon/rail_interaction_test.py` | ❌ | 1792853525 | 0d306f3cafb16f0d538055978a01445f3f1c94e6cbdcce6ce5f9c097b3e92a83 | ['python3', '-c', 'import subprocess,sys; names=["readme_test.py","tui_main_test.py","rail_interaction_test.py","rail_format_test.py","run_console_test.py","gitignore_rail_test.py","gutter_alignment_test.py","mouse_capture_test.py","icon_catalog_test.py","install_command_test.py"]; [subprocess.run([sys.executable,"tests/semicolon/"+name],check=True,timeout=240) for name in names]']; macOS arm64 local lab; strict native C23 build, scripted PTY xterm-256color and disposable fixture paths; aggregate watchdog 900s, each owner 240s; no physical-terminal visual acceptance, windowed launch or non-macOS runtime proof; Linux stat nanosecond branch is guarded source and awaits CI | Semicolon TUI regression aggregate after the portable stat-nanosecond fix: tabs/tree/caret/autosave, exact bounded undo/redo autosaved bytes, gutter alignment, wheel and divider scrolling, mouse capture, console, icons, launcher/install and mechanical README boundary all pass through the current tui-main.c | failed (exit 124) |
| `tests/semicolon/readme_test.py` | ❌ | 1792853525 | 243fa9ff9d808e9f43029414e628d38804cca88bd2e515eadf9ca3cc627b429d | ['python3', '-c', 'import subprocess,sys; names=["readme_test.py","tui_main_test.py","rail_interaction_test.py","rail_format_test.py","run_console_test.py","gitignore_rail_test.py","gutter_alignment_test.py","mouse_capture_test.py","icon_catalog_test.py","install_command_test.py"]; [subprocess.run([sys.executable,"tests/semicolon/"+name],check=True,timeout=240) for name in names]']; macOS arm64 local lab; strict native C23 build, scripted PTY xterm-256color and disposable fixture paths; aggregate watchdog 900s, each owner 240s; no physical-terminal visual acceptance, windowed launch or non-macOS runtime proof; Linux stat nanosecond branch is guarded source and awaits CI | Semicolon TUI regression aggregate after the portable stat-nanosecond fix: tabs/tree/caret/autosave, exact bounded undo/redo autosaved bytes, gutter alignment, wheel and divider scrolling, mouse capture, console, icons, launcher/install and mechanical README boundary all pass through the current tui-main.c | failed (exit 124) |
| `tests/semicolon/run_console_test.py` | ❌ | 1792853525 | 575f3f78efa1a7eccba17940ce92ea227006ce6b468330b13cc3220510feed25 | ['python3', '-c', 'import subprocess,sys; names=["readme_test.py","tui_main_test.py","rail_interaction_test.py","rail_format_test.py","run_console_test.py","gitignore_rail_test.py","gutter_alignment_test.py","mouse_capture_test.py","icon_catalog_test.py","install_command_test.py"]; [subprocess.run([sys.executable,"tests/semicolon/"+name],check=True,timeout=240) for name in names]']; macOS arm64 local lab; strict native C23 build, scripted PTY xterm-256color and disposable fixture paths; aggregate watchdog 900s, each owner 240s; no physical-terminal visual acceptance, windowed launch or non-macOS runtime proof; Linux stat nanosecond branch is guarded source and awaits CI | Semicolon TUI regression aggregate after the portable stat-nanosecond fix: tabs/tree/caret/autosave, exact bounded undo/redo autosaved bytes, gutter alignment, wheel and divider scrolling, mouse capture, console, icons, launcher/install and mechanical README boundary all pass through the current tui-main.c | failed (exit 124) |
| `tests/semicolon/tui_main_test.py` | ❌ | 1792853525 | ebef728dfedaf628f1bb762a2323568f9a8c8722d11c9329cecfe256e7a3d7fe | ['python3', '-c', 'import subprocess,sys; names=["readme_test.py","tui_main_test.py","rail_interaction_test.py","rail_format_test.py","run_console_test.py","gitignore_rail_test.py","gutter_alignment_test.py","mouse_capture_test.py","icon_catalog_test.py","install_command_test.py"]; [subprocess.run([sys.executable,"tests/semicolon/"+name],check=True,timeout=240) for name in names]']; macOS arm64 local lab; strict native C23 build, scripted PTY xterm-256color and disposable fixture paths; aggregate watchdog 900s, each owner 240s; no physical-terminal visual acceptance, windowed launch or non-macOS runtime proof; Linux stat nanosecond branch is guarded source and awaits CI | Semicolon TUI regression aggregate after the portable stat-nanosecond fix: tabs/tree/caret/autosave, exact bounded undo/redo autosaved bytes, gutter alignment, wheel and divider scrolling, mouse capture, console, icons, launcher/install and mechanical README boundary all pass through the current tui-main.c | failed (exit 124) |

### `tests/semicolon/editor`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/semicolon/editor/language_bridge_test.c` | ✅ | 1792746726 | 7129d08d6f5ebf0ed0eb438cd8c75aa6f1044b4168f437b12b68a8839ce6ceb6 | ['python3', 'tests/semicolon/editor/run.py']; macOS arm64 local lab; strict optimized C23 assertions; C ASan/UBSan for both the SemicolonSyntax bridge and the production tui-main snapshot history; injected bridge allocation failures; real static Language C23Highlights link and Determinant TerminalScrollGlide link; scripted xterm-256color PTY; no physical-terminal visual approval, leak-sanitizer claim on macOS, or non-macOS proof | Semicolon C23 editor ink and live editor route after adding bounded snapshot undo/redo: lexical colors, include-header string spans, multiline context, exact autosave bytes/caret/scroll preservation, allocation-refusal recovery, scripted PTY recoloring, and ASan/UBSan multibyte undo/redo with exact autosaved bytes | passed |
| `tests/semicolon/editor/run.py` | ❌ | 1792746726 | 90cfbbca4a62a600b261574c0346490fc705cd721a7ab887bdd6068c18f41ab6 | ['python3', 'tests/semicolon/editor/run.py']; macOS arm64 local lab; strict optimized C23 assertions; C ASan/UBSan for both the SemicolonSyntax bridge and the production tui-main snapshot history; injected bridge allocation failures; real static Language C23Highlights link and Determinant TerminalScrollGlide link; scripted xterm-256color PTY; no physical-terminal visual approval, leak-sanitizer claim on macOS, or non-macOS proof | Semicolon C23 editor ink and live editor route after adding bounded snapshot undo/redo: lexical colors, include-header string spans, multiline context, exact autosave bytes/caret/scroll preservation, allocation-refusal recovery, scripted PTY recoloring, and ASan/UBSan multibyte undo/redo with exact autosaved bytes | stale — content changed; rerun required |
| `tests/semicolon/editor/semicolon_syntax_test.c` | ✅ | 1792746726 | b177b490ad901edfa843445a14adbc841a3245b5f2928da1f08a226c83ff8ae8 | ['python3', 'tests/semicolon/editor/run.py']; macOS arm64 local lab; strict optimized C23 assertions; C ASan/UBSan for both the SemicolonSyntax bridge and the production tui-main snapshot history; injected bridge allocation failures; real static Language C23Highlights link and Determinant TerminalScrollGlide link; scripted xterm-256color PTY; no physical-terminal visual approval, leak-sanitizer claim on macOS, or non-macOS proof | Semicolon C23 editor ink and live editor route after adding bounded snapshot undo/redo: lexical colors, include-header string spans, multiline context, exact autosave bytes/caret/scroll preservation, allocation-refusal recovery, scripted PTY recoloring, and ASan/UBSan multibyte undo/redo with exact autosaved bytes | passed |

### `tests/sesh`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/sesh/docs_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/sesh/run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/sesh/session_run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/sesh/lang`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/sesh/lang/arity_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/sesh/lang/interop_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/sesh/session`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/sesh/session/auth_service_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/sesh/session/client_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/sesh/session/operation_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/sesh/session/operations_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/sesh/session/resource_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/sesh/session/sesh_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/sesh/session/text_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/sesh/session/workspace_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/sesh/snapshot`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/sesh/snapshot/snapshot_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/tools`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/tools/agent_tool_contract_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/tools/agents_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/tools/arrange_test.py` | ✅ | 1792851572 | 4b7c975f30b89a70ec02c828eec9a015882842158f899fb7eb30091033a0f8ac | ['python3', '-B', 'tests/tools/arrange_test.py']; Fixture .c files; no build, no network; control-flow layout rules, conservative exclusions, check/diff/write, ratchet baseline | Layout arranger: 20 unit tests pass | passed |
| `tests/tools/c23_migration_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/tools/ci_repos_test.py` | ✅ | 1792850992 | 913dd73e45cb97955aa23efa482f59850bd143e55f67d8ae50139878fc15c9bc | ['python3', '-B', 'tests/tools/ci_repos_test.py']; Fixture-based; no network, no build; manifest validation, clone dry-run, caller gating, lint+layout baselines, require-ready | CI repo tooling: 21 unit tests pass | passed |
| `tests/tools/clion_adapter_test.py` | ✅ | 1792903150 | 2423dad052be4ed2c3781e6ba388335a0ad000339d7a874b8f92dd5dfcde8f63 | ['sh', '-c', 'python3 -B tests/tools/run_current_test.py && python3 -B tests/tools/clion_adapter_test.py']; Command-only evidence; no broader readiness claim | Verify moved suite paths through b and CMake | passed |
| `tests/tools/compositor_contract_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/tools/compositor_shader_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/tools/darling_lifecycle_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/tools/ecosystem_docs_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/tools/exhaustion_law_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/tools/filter_gallery_resources_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/tools/harness_ide_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/tools/linter_test.py` | ✅ | 1792852172 | d0934f7ea3769f9522b0f1f1d725a19a0c9f2ccc938357605e12516742234d2e | ['python3', '-B', 'tests/tools/linter_test.py']; Fixture-based; throwaway .c files; no build; lint rules, fixers, ratchet baseline | Linter and ratchet baseline: 17 unit tests pass | passed |
| `tests/tools/migration_contract_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/tools/opencode_preferences_test.ts` | ✅ | 1792886375 | 6d4238467ce4a89173e7952164b70fb35d5e37ee6fdbe41a85ac43e62a5ea097 | ['bun', 'test', 'tests/tools/opencode_preferences_test.ts']; Preferences plugin assembly + tools/prefs CLI on macOS arm64; no other platform claimed | Injected block is compressed constitution (37 laws, incl. Relational Memory) + proof/repo title index under 32 KB; on-demand law/section/test/repo slices by Title; fallback and loud-missing paths; setup-once hook | passed |
| `tests/tools/per_repo_ide_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/tools/prefs_test.py` | ✅ | 1792851803 | 00992eef91f8568f9a807a38d3c4b43fa2ed9b4ee57f418372f54c9e885b30e0 | ['python3', '-B', 'tests/tools/prefs_test.py']; Throwaway trees; no network, no gh; compressed-only check, full-document parity, publish/verify refusal | Preferences CLI: 7 unit tests pass | passed |
| `tests/tools/readiness_test.py` | ❌ | 1792851324 | 2775bec43a570c903c51636cfaa8bf52a3eb23c8f6e3f2211e38641f7c90272b | ['python3', '-B', 'tests/tools/readiness_test.py']; Fixture git checkouts; no build or network; attribution, ledger green/stale, lint+layout debt, platform declaration, text/markdown/JSON | Readiness scoreboard: 10 unit tests pass | stale — content changed; rerun required |
| `tests/tools/run_current_test.py` | ✅ | 1792886444 | a20353017e41804546eccd9f598fe8c053ee93afb0fb022baa3ad251551122e2 | ['python3', '-B', 'tests/tools/run_current_test.py']; macOS arm64; current-file launcher path and routing in tools/scripts/run-current; headless tests only | Verify moved suite paths through b and CLion run-current runner | passed |
| `tests/tools/sampled_texture_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/tools/test_checklist_test.py` | ❌ | 1792022726 | 1279295ead35806ed5459814353de41d6f5f0471b28817245d161bee3c37a133 | ['sh', '-c', 'bun test tests/tools/opencode_preferences_test.ts && python3 -B tests/tools/test_checklist_test.py && python3 -B tests/tools/clion_adapter_test.py']; macOS arm64; b graph path resolution, preferences tooling tests through b and CTest, native CMake adapter regression; focused targets only | Build wiring for suite paths and preferences tooling tests | stale — content changed; rerun required |

### `tests/vexspoke`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/vexspoke/backend_contract_test.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/vexspoke/algo`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/vexspoke/algo/algo_suite_test.c` | ✅ | 1792048700 | 7b29713d0077afb54a11030fcc189fec4369e101cbbc898dcb92d53ab1d87644 | ['cmake-build-debug/bin/algo_suite_test']; macOS arm64; C23 CMake debug target; algorithm integration, 64 MiB default Relational Engine memory arena | Vexspoke algorithm suite with Sort radix API | passed |
| `tests/vexspoke/algo/bvh_test.c` | ✅ | 1792029426 | c5b36a971e26345794de8047140176dd0ae8e549d691b939f0bdcd16bf9229f8 | ['cmake-build-debug/bin/bvh_test']; vexspoke | BvhTree constructors, allocation lifecycle, rebuild preconditions, ray hits, and AABB queries | passed |
| `tests/vexspoke/algo/dijkstra_test.c` | ✅ | 1792024900 | 1b60837dc082a69e062a65e35f307a1c1bf6557d760f759f240b154a4e8254ee | ['ctest', '--test-dir', '/private/tmp/vexgraph-cmake-check-cmake', '--output-on-failure', '-R', '^(terminal_appearance_test&#124;vec2_test&#124;vec3_test&#124;vec4_test&#124;secure_random_test&#124;algo_suite_test&#124;dijkstra_test)$']; macOS arm64 C23 debug; CMake build /private/tmp/vexgraph-cmake-check-cmake; headless owner tests. | Constructor chooser C23 owner tests, including geometry and precision-vector overloads. | passed |
| `tests/vexspoke/algo/kd_tree_test.c` | ✅ | 1792031936 | 97c2a6393385481b6e872593ea97aa8794c1d741abce4fc0d858919972231470 | ['ctest', '--test-dir', 'cmake-build-debug', '--output-on-failure', '-R', '^(kd_tree_test&#124;octree_test&#124;compute_test&#124;datetime_test&#124;sha1_test&#124;vm_test)$']; macOS arm64; C23 CMake debug targets; offline deterministic owner tests; no live network or visual checks | Vexspoke value constructor macros in geometry, compute, time, SHA-1, and regex VM owners | passed |
| `tests/vexspoke/algo/radix_sort_test.c` | ✅ | 1792048697 | 8202accc914537c45a2f9b74384a8f96f65ad1c68b930b35ff968e1903299686 | ['cmake-build-debug/bin/radix_sort_test']; macOS arm64; C23 CMake debug target; deterministic qsort oracles, unsigned extrema, duplicates, paired values, arena allocation | Sort unsigned radix owner test | passed |
| `tests/vexspoke/algo/segment_index_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/algo/sort_test.c` | ✅ | 1792048689 | ac6a2653c0563b1bab66ee45a72ad8081e7b596843f58178411fb043cee95b1c | ['cmake-build-debug/bin/sort_test']; macOS arm64; C23 CMake debug target; comparison sorts, stability, quicksort adversarial patterns, merge scratch rejection, partition boundaries | Sort comparison algorithms owner test | passed |
| `tests/vexspoke/algo/spatial_test.c` | ✅ | 1792048693 | d9702f8c190ea66b2512c0f5aff22406f32e97d3c53a8b78a8c97bc1406e3533 | ['cmake-build-debug/bin/spatial_test']; macOS arm64; C23 CMake debug target; Morton encoding axis bits, 21-bit bounds, truncation | Spatial Morton encoding owner test | passed |
| `tests/vexspoke/algo/tree_sit_test.c` | ✅ | 1792852622 | e6466807bf94fc323eac407a9b53e8a79e9f61d8db09d47257d77800bd808ee7 | ['./cmake-build-debug/bin/tree_sit_test']; macOS arm64; C23; debug build; direct owner binary from cmake-build-debug; no live network | TreeSit constructors, node relationships, traversal, and byte lookup | passed |

### `tests/vexspoke/atomic`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/vexspoke/atomic/registry_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/atomic/ring_test.c` | ✅ | 1792029286 | 4d0cc5e8aec37a84334e7bd25eb42e31694a92a4f52ccb46ba7ab35e29957155 | ['sh', '-c', 'cmake-build-debug/bin/ring_test && cmake-build-debug/bin/bit_test && cmake-build-debug/bin/bool_test && cmake-build-debug/bin/byte_test && cmake-build-debug/bin/short_test && cmake-build-debug/bin/int_test && cmake-build-debug/bin/long_test && cmake-build-debug/bin/float_test && cmake-build-debug/bin/double_test && cmake-build-debug/bin/brain_test && cmake-build-debug/bin/fixed32_test && cmake-build-debug/bin/fixed64_test && cmake-build-debug/bin/int_float_test && cmake-build-debug/bin/int_double_test && cmake-build-debug/bin/long_float_test && cmake-build-debug/bin/long_double_test']; vexspoke | RingBuffer and BitPool constructors plus primitive pool allocation lifecycle | passed |
| `tests/vexspoke/atomic/spin_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/vexspoke/audio`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/vexspoke/audio/audio_hal_test.c` | ✅ | 1792030289 | e1598b3146d2e2a35b01f4135751543a57c962882eb00e25a3121eea9bd3186a | ['cmake-build-debug/bin/audio_hal_test']; vexspoke | AudioHalConfig constructors and setter validation | passed |

### `tests/vexspoke/bit`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/vexspoke/bit/bit_test.c` | ✅ | 1792029286 | 9ffd12a6c52faf6a3eb990d350a0614236d1623e6f1cb04802929fc462f961d2 | ['sh', '-c', 'cmake-build-debug/bin/ring_test && cmake-build-debug/bin/bit_test && cmake-build-debug/bin/bool_test && cmake-build-debug/bin/byte_test && cmake-build-debug/bin/short_test && cmake-build-debug/bin/int_test && cmake-build-debug/bin/long_test && cmake-build-debug/bin/float_test && cmake-build-debug/bin/double_test && cmake-build-debug/bin/brain_test && cmake-build-debug/bin/fixed32_test && cmake-build-debug/bin/fixed64_test && cmake-build-debug/bin/int_float_test && cmake-build-debug/bin/int_double_test && cmake-build-debug/bin/long_float_test && cmake-build-debug/bin/long_double_test']; vexspoke | RingBuffer and BitPool constructors plus primitive pool allocation lifecycle | passed |

### `tests/vexspoke/c23`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/vexspoke/c23/equals_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/c23/fn_test.c` | ✅ | 1792030712 | 261d6dd5c854b187448c0ebbb5e0e377d35d4f8b8d05b9978714935f6bf79a1d | ['env', 'B_HOME=/Users/vexgraph/vexgraph/cmake-build-debug/b-state', './tools/b', 'run', 'fn_test']; vexspoke | Function constructor arities, callback/context binding, and null-safe execution | passed |
| `tests/vexspoke/c23/free_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/vexspoke/cli`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/vexspoke/cli/console_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/vexspoke/deferred`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/vexspoke/deferred/dispatch_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/vexspoke/exception`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/vexspoke/exception/exception_test.c` | ✅ | 1792029621 | 93f7124ee770041a372a9b1f97258105fba07b728eaa80db33dad008597d69b0 | ['sh', '-c', 'cmake-build-debug/bin/exception_test && cmake-build-debug/bin/throwable_test']; vexspoke | Exception constructor formatting, owned diagnostic lifecycle, and Hotcwap throwable integration | passed |
| `tests/vexspoke/exception/throw_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/exception/try_code_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/exception/try_ptr_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/exception/try_value_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/vexspoke/image`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/vexspoke/image/png_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/vexspoke/input`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/vexspoke/input/hardware_input_test.c` | ✅ | 1792853242 | c508bc9e2ff7df22d0306e8186546dc792890d27b9ec21b5c0acc25ac3d8e75e | ['./cmake-build-debug/bin/hardware_input_test']; macOS arm64; C23; debug build; direct owner binary rebuilt from the current test source in cmake-build-debug; no live input hardware | Gamepad and Turntable calculations return named value records | passed |
| `tests/vexspoke/input/input_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/input/key_map_test.c` | ✅ | 1792030970 | 71e9d4c1db5a577735943844c5dd201df2291c20081177bdbe3cf5253c76b6b6 | ['env', 'B_HOME=/Users/vexgraph/vexgraph/cmake-build-debug/b-state', './tools/b', 'run', 'key_map_test']; vexspoke | KeyMap recipe using the borrowed default MemoryArena | passed |

### `tests/vexspoke/lang`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/vexspoke/lang/mat4_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/lang/vec2_test.c` | ✅ | 1792024900 | e2b1c562c39908f281417ded4b5c81faecdf259c7d91d7c482c4488aab643af1 | ['ctest', '--test-dir', '/private/tmp/vexgraph-cmake-check-cmake', '--output-on-failure', '-R', '^(terminal_appearance_test&#124;vec2_test&#124;vec3_test&#124;vec4_test&#124;secure_random_test&#124;algo_suite_test&#124;dijkstra_test)$']; macOS arm64 C23 debug; CMake build /private/tmp/vexgraph-cmake-check-cmake; headless owner tests. | Constructor chooser C23 owner tests, including geometry and precision-vector overloads. | passed |
| `tests/vexspoke/lang/vec3_test.c` | ✅ | 1792853241 | 2ca73e644bada9a8f5d643a39b9864fc0a3508d64a4993b88409c53a6a2b7073 | ['./cmake-build-debug/bin/vec3_test']; macOS arm64; C23; debug build; direct owner binary rebuilt from the current test source in cmake-build-debug; headless | Constructor chooser C23 owner tests, including geometry and precision-vector overloads | passed |
| `tests/vexspoke/lang/vec4_test.c` | ✅ | 1792024900 | 55d30e611a5ffec1808876879d74388422ff8d08185732c06cdab2e6aba7ebf2 | ['ctest', '--test-dir', '/private/tmp/vexgraph-cmake-check-cmake', '--output-on-failure', '-R', '^(terminal_appearance_test&#124;vec2_test&#124;vec3_test&#124;vec4_test&#124;secure_random_test&#124;algo_suite_test&#124;dijkstra_test)$']; macOS arm64 C23 debug; CMake build /private/tmp/vexgraph-cmake-check-cmake; headless owner tests. | Constructor chooser C23 owner tests, including geometry and precision-vector overloads. | passed |

### `tests/vexspoke/math`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/vexspoke/math/coord_frame_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/math/fast_math_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/math/math_coord_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/math/math_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/math/strict_math_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/vexspoke/misc`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/vexspoke/misc/header_veto_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/vexspoke/net`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/vexspoke/net/net_test.c` | ✅ | 1792032250 | bd94a331a89b4923a568c18a3cceea645003ba2ba1a18dff270a4a01060b52f1 | ['cmake-build-debug/bin/net_test', '--constructors-only']; macOS arm64; strict C23 CMake debug executable; exercises constructor defaults and one setter; full net_test loopback path fails because HttpServer_start cannot bind in this sandbox | Vexspoke constructor-only owner path for DownloadOptions and Bespoke | passed |
| `tests/vexspoke/net/run.py` | ✅ | 1792074371 | 5c747f24c2d393254fb5b2e60444432c13966fea92994b345af9752ef68618f2 | ['python3', '-B', 'tests/vexspoke/net/run.py']; macOS arm64; strict + ASan/UBSan; ws:// loopback peer only -- the wss:// path is proven by the smoke owner | WebSocket protocol and binding owners re-verified after the transport-guard fix that let writes reach the TLS session (writeText/writeBinary/writePing/writeClose/wsSendFrame had all required a socket fd, so every wss:// write was dead): the offline owners stay green and the live smoke is what caught it | passed |
| `tests/vexspoke/net/tls_apple_run.py` | ✅ | 1792117824 | 09a3ebb89fe1c68be43574ad2fcbce35452023a23d48dd9229a7c2034d8277bd | ['python3', '-B', 'tests/vexspoke/net/tls_apple_run.py']; macOS arm64; strict and sanitized; ARC + Network.framework; refusal paths only -- the completed handshake, heartbeat ACK and close-code reporting are proved by the WebSocket smoke's live tiers; tls_curl.c is a fail-closed stub | Apple TLS backend refusal paths re-verified after the receive-slot rewrite: the session now owns ONE outstanding nw_connection_receive shared by Tls_readable and Tls_recv, a timed-out wait leaves it armed with its Bytes intact instead of abandoning it, and a consume offset prevents a partial read from discarding buffered Bytes. Refusals, null-safety and the bounded connect budget are unchanged. | passed |
| `tests/vexspoke/net/tls_apple_test.c` | ✅ | 1792117824 | 2f3b44a60d2e2e6d2ff15048ccb2b0ee80883bd147dfdc0236f418a460476df6 | ['python3', '-B', 'tests/vexspoke/net/tls_apple_run.py']; macOS arm64; strict and sanitized; ARC + Network.framework; refusal paths only -- the completed handshake, heartbeat ACK and close-code reporting are proved by the WebSocket smoke's live tiers; tls_curl.c is a fail-closed stub | Apple TLS backend refusal paths re-verified after the receive-slot rewrite: the session now owns ONE outstanding nw_connection_receive shared by Tls_readable and Tls_recv, a timed-out wait leaves it armed with its Bytes intact instead of abandoning it, and a consume offset prevents a partial read from discarding buffered Bytes. Refusals, null-safety and the bounded connect budget are unchanged. | passed |
| `tests/vexspoke/net/url_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/net/websocket_smoke_test.c` | ✅ | 1792117802 | 2596116aefe22f2c4f6a36045baec18484e2e3aa712cf814bd3f3afa5750239c | ['python3', '-B', 'tests/vexspoke/net/ws_smoke_run.py']; macOS arm64; strict C23; ARC + Foundation/Network; idle tier offline and always runs; live tiers are opt-in so the shared suite never needs the internet. A previous revision of this scope blamed wss://ws.postman-echo.com/raw for sending nothing: that was WRONG and was caused by a defect in the TLS adapter (a timed-out readiness probe abandoned its nw_connection_receive and left it armed, so the next read stacked a second receive and aborted the connection). The single-outstanding-receive fix landed and postman now echoes. No Discord token was used, stored or needed; no Discord auth/session/REST is implied; tls_curl.c remains a fail-closed stub so Linux/Windows have no transport security | WebSocket smoke, three tiers: idle cost (~3000 ms idle for ~1 ms CPU, asserted); an opt-in live round-trip that now ECHOES correctly against wss://ws.postman-echo.com/raw (24-Byte probe returned); and an opt-in Discord gateway tier with NO token -- TLS handshake, HELLO (op 10, heartbeat_interval), heartbeat acked (op 11), and a deliberately invalid IDENTIFY refused with close code 4004 'Authentication failed.', which also proves the close code and reason reach the caller | passed |
| `tests/vexspoke/net/websocket_test.c` | ✅ | 1792074371 | 65d41647abdffc468349bd9861ab4cec6d502d14b6a9810d045495ca07bf1087 | ['python3', '-B', 'tests/vexspoke/net/run.py']; macOS arm64; strict + ASan/UBSan; ws:// loopback peer only -- the wss:// path is proven by the smoke owner | WebSocket protocol and binding owners re-verified after the transport-guard fix that let writes reach the TLS session (writeText/writeBinary/writePing/writeClose/wsSendFrame had all required a socket fd, so every wss:// write was dead): the offline owners stay green and the live smoke is what caught it | passed |
| `tests/vexspoke/net/ws_smoke_run.py` | ✅ | 1792117802 | 77bfbe5ff5fd41996ab0d6972981612e6b60c97456cfb58e47655befc3ea6b7a | ['python3', '-B', 'tests/vexspoke/net/ws_smoke_run.py']; macOS arm64; strict C23; ARC + Foundation/Network; idle tier offline and always runs; live tiers are opt-in so the shared suite never needs the internet. A previous revision of this scope blamed wss://ws.postman-echo.com/raw for sending nothing: that was WRONG and was caused by a defect in the TLS adapter (a timed-out readiness probe abandoned its nw_connection_receive and left it armed, so the next read stacked a second receive and aborted the connection). The single-outstanding-receive fix landed and postman now echoes. No Discord token was used, stored or needed; no Discord auth/session/REST is implied; tls_curl.c remains a fail-closed stub so Linux/Windows have no transport security | WebSocket smoke, three tiers: idle cost (~3000 ms idle for ~1 ms CPU, asserted); an opt-in live round-trip that now ECHOES correctly against wss://ws.postman-echo.com/raw (24-Byte probe returned); and an opt-in Discord gateway tier with NO token -- TLS handshake, HELLO (op 10, heartbeat_interval), heartbeat acked (op 11), and a deliberately invalid IDENTIFY refused with close code 4004 'Authentication failed.', which also proves the close code and reason reach the caller | passed |

### `tests/vexspoke/objects`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/vexspoke/objects/choice_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/objects/future_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/objects/global_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/objects/local_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/objects/passive_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/objects/probable_objects_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/objects/probable_test.c` | ✅ | 1792031060 | a5fdf64ed1db2cfefea16d50c283b94ec4ddde045d32ec999173178b28444350 | ['env', 'B_HOME=/Users/vexgraph/vexgraph/cmake-build-debug/b-state', './tools/b', 'run', 'probable_test']; vexspoke | Probable constructor macro and weighted-pool recipe | passed |

### `tests/vexspoke/oop`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/vexspoke/oop/stride_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/oop/type_test.c` | ✅ | 1792510080 | 05e9b7da823fc739421540fb35d60220a28e0675cb9b0387d910f01cfd3ebdc3 | ['python3', '/private/var/folders/z7/x7y_f3fd7vnchzxx7gmwkhp40000gn/T/opencode/type_owner.py']; macOS arm64; strict optimized C23 with -Wall -Wextra -Werror and assertions active; compiles and executes the real engine Type resolver and migrated native Memory implementation. | Vexspoke class registry and engine Type algebra owner | passed |

### `tests/vexspoke/primitive`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/vexspoke/primitive/bool_test.c` | ✅ | 1792029286 | 6f07cbf0a35401414b6740caf3b63ea7edee47ac9f690ac6960979bef96a513b | ['sh', '-c', 'cmake-build-debug/bin/ring_test && cmake-build-debug/bin/bit_test && cmake-build-debug/bin/bool_test && cmake-build-debug/bin/byte_test && cmake-build-debug/bin/short_test && cmake-build-debug/bin/int_test && cmake-build-debug/bin/long_test && cmake-build-debug/bin/float_test && cmake-build-debug/bin/double_test && cmake-build-debug/bin/brain_test && cmake-build-debug/bin/fixed32_test && cmake-build-debug/bin/fixed64_test && cmake-build-debug/bin/int_float_test && cmake-build-debug/bin/int_double_test && cmake-build-debug/bin/long_float_test && cmake-build-debug/bin/long_double_test']; vexspoke | RingBuffer and BitPool constructors plus primitive pool allocation lifecycle | passed |
| `tests/vexspoke/primitive/brain_test.c` | ✅ | 1792029286 | 7ab5823c9ae3f8a27a2af2c90a807969b7e35cc0975e0d25e9292edaba26e9f0 | ['sh', '-c', 'cmake-build-debug/bin/ring_test && cmake-build-debug/bin/bit_test && cmake-build-debug/bin/bool_test && cmake-build-debug/bin/byte_test && cmake-build-debug/bin/short_test && cmake-build-debug/bin/int_test && cmake-build-debug/bin/long_test && cmake-build-debug/bin/float_test && cmake-build-debug/bin/double_test && cmake-build-debug/bin/brain_test && cmake-build-debug/bin/fixed32_test && cmake-build-debug/bin/fixed64_test && cmake-build-debug/bin/int_float_test && cmake-build-debug/bin/int_double_test && cmake-build-debug/bin/long_float_test && cmake-build-debug/bin/long_double_test']; vexspoke | RingBuffer and BitPool constructors plus primitive pool allocation lifecycle | passed |
| `tests/vexspoke/primitive/byte_test.c` | ✅ | 1792029286 | 932dae16377213c1243d4606c135be58eef239c912940a5260f006d67a2d15ac | ['sh', '-c', 'cmake-build-debug/bin/ring_test && cmake-build-debug/bin/bit_test && cmake-build-debug/bin/bool_test && cmake-build-debug/bin/byte_test && cmake-build-debug/bin/short_test && cmake-build-debug/bin/int_test && cmake-build-debug/bin/long_test && cmake-build-debug/bin/float_test && cmake-build-debug/bin/double_test && cmake-build-debug/bin/brain_test && cmake-build-debug/bin/fixed32_test && cmake-build-debug/bin/fixed64_test && cmake-build-debug/bin/int_float_test && cmake-build-debug/bin/int_double_test && cmake-build-debug/bin/long_float_test && cmake-build-debug/bin/long_double_test']; vexspoke | RingBuffer and BitPool constructors plus primitive pool allocation lifecycle | passed |
| `tests/vexspoke/primitive/double_test.c` | ✅ | 1792029286 | e2e0753046019e9686906bf70a716a88f066c240eb708ff634f22da97c95c79b | ['sh', '-c', 'cmake-build-debug/bin/ring_test && cmake-build-debug/bin/bit_test && cmake-build-debug/bin/bool_test && cmake-build-debug/bin/byte_test && cmake-build-debug/bin/short_test && cmake-build-debug/bin/int_test && cmake-build-debug/bin/long_test && cmake-build-debug/bin/float_test && cmake-build-debug/bin/double_test && cmake-build-debug/bin/brain_test && cmake-build-debug/bin/fixed32_test && cmake-build-debug/bin/fixed64_test && cmake-build-debug/bin/int_float_test && cmake-build-debug/bin/int_double_test && cmake-build-debug/bin/long_float_test && cmake-build-debug/bin/long_double_test']; vexspoke | RingBuffer and BitPool constructors plus primitive pool allocation lifecycle | passed |
| `tests/vexspoke/primitive/fixed32_test.c` | ✅ | 1792029286 | a1542bd6837caa15904aeb758be9a33cb79be65e9a9ac602d76c0c4cc28b7a37 | ['sh', '-c', 'cmake-build-debug/bin/ring_test && cmake-build-debug/bin/bit_test && cmake-build-debug/bin/bool_test && cmake-build-debug/bin/byte_test && cmake-build-debug/bin/short_test && cmake-build-debug/bin/int_test && cmake-build-debug/bin/long_test && cmake-build-debug/bin/float_test && cmake-build-debug/bin/double_test && cmake-build-debug/bin/brain_test && cmake-build-debug/bin/fixed32_test && cmake-build-debug/bin/fixed64_test && cmake-build-debug/bin/int_float_test && cmake-build-debug/bin/int_double_test && cmake-build-debug/bin/long_float_test && cmake-build-debug/bin/long_double_test']; vexspoke | RingBuffer and BitPool constructors plus primitive pool allocation lifecycle | passed |
| `tests/vexspoke/primitive/fixed64_test.c` | ✅ | 1792029286 | 68fa0a3690263a2132ea8185340fbfc643fbb1d3bef9d8965dac6f90ab23a250 | ['sh', '-c', 'cmake-build-debug/bin/ring_test && cmake-build-debug/bin/bit_test && cmake-build-debug/bin/bool_test && cmake-build-debug/bin/byte_test && cmake-build-debug/bin/short_test && cmake-build-debug/bin/int_test && cmake-build-debug/bin/long_test && cmake-build-debug/bin/float_test && cmake-build-debug/bin/double_test && cmake-build-debug/bin/brain_test && cmake-build-debug/bin/fixed32_test && cmake-build-debug/bin/fixed64_test && cmake-build-debug/bin/int_float_test && cmake-build-debug/bin/int_double_test && cmake-build-debug/bin/long_float_test && cmake-build-debug/bin/long_double_test']; vexspoke | RingBuffer and BitPool constructors plus primitive pool allocation lifecycle | passed |
| `tests/vexspoke/primitive/float_test.c` | ✅ | 1792029286 | 5abfbd6be607bb367b5012f237675987a32d43cba65df9d9c725d76b8ef14aeb | ['sh', '-c', 'cmake-build-debug/bin/ring_test && cmake-build-debug/bin/bit_test && cmake-build-debug/bin/bool_test && cmake-build-debug/bin/byte_test && cmake-build-debug/bin/short_test && cmake-build-debug/bin/int_test && cmake-build-debug/bin/long_test && cmake-build-debug/bin/float_test && cmake-build-debug/bin/double_test && cmake-build-debug/bin/brain_test && cmake-build-debug/bin/fixed32_test && cmake-build-debug/bin/fixed64_test && cmake-build-debug/bin/int_float_test && cmake-build-debug/bin/int_double_test && cmake-build-debug/bin/long_float_test && cmake-build-debug/bin/long_double_test']; vexspoke | RingBuffer and BitPool constructors plus primitive pool allocation lifecycle | passed |
| `tests/vexspoke/primitive/int_double_test.c` | ✅ | 1792029286 | 1795fddefd82aeffb4cdf4b0fee10105de192189511759d19b6057948dcd8695 | ['sh', '-c', 'cmake-build-debug/bin/ring_test && cmake-build-debug/bin/bit_test && cmake-build-debug/bin/bool_test && cmake-build-debug/bin/byte_test && cmake-build-debug/bin/short_test && cmake-build-debug/bin/int_test && cmake-build-debug/bin/long_test && cmake-build-debug/bin/float_test && cmake-build-debug/bin/double_test && cmake-build-debug/bin/brain_test && cmake-build-debug/bin/fixed32_test && cmake-build-debug/bin/fixed64_test && cmake-build-debug/bin/int_float_test && cmake-build-debug/bin/int_double_test && cmake-build-debug/bin/long_float_test && cmake-build-debug/bin/long_double_test']; vexspoke | RingBuffer and BitPool constructors plus primitive pool allocation lifecycle | passed |
| `tests/vexspoke/primitive/int_float_test.c` | ✅ | 1792029286 | d1972969716cc55cb33dc46cc7dc17298aa104e3e2e0ba3506baf069c05450e9 | ['sh', '-c', 'cmake-build-debug/bin/ring_test && cmake-build-debug/bin/bit_test && cmake-build-debug/bin/bool_test && cmake-build-debug/bin/byte_test && cmake-build-debug/bin/short_test && cmake-build-debug/bin/int_test && cmake-build-debug/bin/long_test && cmake-build-debug/bin/float_test && cmake-build-debug/bin/double_test && cmake-build-debug/bin/brain_test && cmake-build-debug/bin/fixed32_test && cmake-build-debug/bin/fixed64_test && cmake-build-debug/bin/int_float_test && cmake-build-debug/bin/int_double_test && cmake-build-debug/bin/long_float_test && cmake-build-debug/bin/long_double_test']; vexspoke | RingBuffer and BitPool constructors plus primitive pool allocation lifecycle | passed |
| `tests/vexspoke/primitive/int_test.c` | ✅ | 1792029286 | 7a460a6f3c7c06a951566917ffebf0fc29173a99b25fad8dbefdd03be420ef8a | ['sh', '-c', 'cmake-build-debug/bin/ring_test && cmake-build-debug/bin/bit_test && cmake-build-debug/bin/bool_test && cmake-build-debug/bin/byte_test && cmake-build-debug/bin/short_test && cmake-build-debug/bin/int_test && cmake-build-debug/bin/long_test && cmake-build-debug/bin/float_test && cmake-build-debug/bin/double_test && cmake-build-debug/bin/brain_test && cmake-build-debug/bin/fixed32_test && cmake-build-debug/bin/fixed64_test && cmake-build-debug/bin/int_float_test && cmake-build-debug/bin/int_double_test && cmake-build-debug/bin/long_float_test && cmake-build-debug/bin/long_double_test']; vexspoke | RingBuffer and BitPool constructors plus primitive pool allocation lifecycle | passed |
| `tests/vexspoke/primitive/long_double_test.c` | ✅ | 1792029286 | d43a59a80fdb0fc3b4ae02a8658034a631854c0c2e1fb0567dea4eab2443ae50 | ['sh', '-c', 'cmake-build-debug/bin/ring_test && cmake-build-debug/bin/bit_test && cmake-build-debug/bin/bool_test && cmake-build-debug/bin/byte_test && cmake-build-debug/bin/short_test && cmake-build-debug/bin/int_test && cmake-build-debug/bin/long_test && cmake-build-debug/bin/float_test && cmake-build-debug/bin/double_test && cmake-build-debug/bin/brain_test && cmake-build-debug/bin/fixed32_test && cmake-build-debug/bin/fixed64_test && cmake-build-debug/bin/int_float_test && cmake-build-debug/bin/int_double_test && cmake-build-debug/bin/long_float_test && cmake-build-debug/bin/long_double_test']; vexspoke | RingBuffer and BitPool constructors plus primitive pool allocation lifecycle | passed |
| `tests/vexspoke/primitive/long_float_test.c` | ✅ | 1792029286 | 6645530681cc42188760a6bef2886941f1300d3e93f7957b0380b3157abb1650 | ['sh', '-c', 'cmake-build-debug/bin/ring_test && cmake-build-debug/bin/bit_test && cmake-build-debug/bin/bool_test && cmake-build-debug/bin/byte_test && cmake-build-debug/bin/short_test && cmake-build-debug/bin/int_test && cmake-build-debug/bin/long_test && cmake-build-debug/bin/float_test && cmake-build-debug/bin/double_test && cmake-build-debug/bin/brain_test && cmake-build-debug/bin/fixed32_test && cmake-build-debug/bin/fixed64_test && cmake-build-debug/bin/int_float_test && cmake-build-debug/bin/int_double_test && cmake-build-debug/bin/long_float_test && cmake-build-debug/bin/long_double_test']; vexspoke | RingBuffer and BitPool constructors plus primitive pool allocation lifecycle | passed |
| `tests/vexspoke/primitive/long_test.c` | ✅ | 1792029286 | 2d295ae377594778211663b232e588e4f9770bc43ba6c0363edfbab2420bd240 | ['sh', '-c', 'cmake-build-debug/bin/ring_test && cmake-build-debug/bin/bit_test && cmake-build-debug/bin/bool_test && cmake-build-debug/bin/byte_test && cmake-build-debug/bin/short_test && cmake-build-debug/bin/int_test && cmake-build-debug/bin/long_test && cmake-build-debug/bin/float_test && cmake-build-debug/bin/double_test && cmake-build-debug/bin/brain_test && cmake-build-debug/bin/fixed32_test && cmake-build-debug/bin/fixed64_test && cmake-build-debug/bin/int_float_test && cmake-build-debug/bin/int_double_test && cmake-build-debug/bin/long_float_test && cmake-build-debug/bin/long_double_test']; vexspoke | RingBuffer and BitPool constructors plus primitive pool allocation lifecycle | passed |
| `tests/vexspoke/primitive/pack_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/primitive/short_test.c` | ✅ | 1792029286 | 9610712e01e577b568461357cae134c27ab3db200c67abe62196a28ef8f4746e | ['sh', '-c', 'cmake-build-debug/bin/ring_test && cmake-build-debug/bin/bit_test && cmake-build-debug/bin/bool_test && cmake-build-debug/bin/byte_test && cmake-build-debug/bin/short_test && cmake-build-debug/bin/int_test && cmake-build-debug/bin/long_test && cmake-build-debug/bin/float_test && cmake-build-debug/bin/double_test && cmake-build-debug/bin/brain_test && cmake-build-debug/bin/fixed32_test && cmake-build-debug/bin/fixed64_test && cmake-build-debug/bin/int_float_test && cmake-build-debug/bin/int_double_test && cmake-build-debug/bin/long_float_test && cmake-build-debug/bin/long_double_test']; vexspoke | RingBuffer and BitPool constructors plus primitive pool allocation lifecycle | passed |
| `tests/vexspoke/primitive/string_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/vexspoke/reactive`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/vexspoke/reactive/reactive_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/reactive/reactive_typed_test.c` | ✅ | 1792028152 | b2c49ac884d806dfe58b49c206dce1c10c3794e83f43edd5704d364191e62431 | ['cmake-build-debug/bin/reactive_typed_test']; macOS debug build; scalar constructors plus all seven object-family chooser macros, generic object operations, and probable constructors | Reactive typed suite: constructor choosers, object rebinding, probable update/read, observer delivery | passed |

### `tests/vexspoke/reflection`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/vexspoke/reflection/reflection_test.c` | ✅ | 1792852623 | 1bc0c0bad33dc917666b8acb54b28ec4d346ea1922137fdbf9980d9d155e3a5d | ['./cmake-build-debug/bin/reflection_test']; macOS arm64; C23; debug build; direct owner binary from cmake-build-debug; no live network | Output-first reflection getter callers | passed |

### `tests/vexspoke/regex`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/vexspoke/regex/charclass_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/regex/nodelist_test.c` | ✅ | 1792028364 | 38e0d781e8db71338d82a18bd28300df7770389d5cc32ee72081182c45bbfe39 | ['cmake-build-debug/bin/nodelist_test']; macOS debug build; regex stage constructor, parsing, compilation, VM execution, and cleanup | Regex nodelist owner suite after replacing stage initializer examples with constructors | passed |
| `tests/vexspoke/regex/parser_test.c` | ✅ | 1792028364 | 026adcb5178dff440da64b4fa292c4ec9680624dd863a587e1070ba7082170ee | ['cmake-build-debug/bin/parser_test']; macOS debug build; regex stage constructor, parsing, compilation, VM execution, and cleanup | Regex parser owner suite after replacing stage initializer examples with constructors | passed |
| `tests/vexspoke/regex/program_test.c` | ✅ | 1792028364 | f6401975724bee90438ee6be2fac4cb03951814d2ea3c85d425231fd3308b278 | ['cmake-build-debug/bin/program_test']; macOS debug build; regex stage constructor, parsing, compilation, VM execution, and cleanup | Regex program owner suite after replacing stage initializer examples with constructors | passed |
| `tests/vexspoke/regex/regex_test.c` | ✅ | 1792031459 | 59c51a62bc8be4d703caf9d7621cf7a314ad7bd8d33d30b94e01fa46e412f36d | ['ctest', '--test-dir', 'cmake-build-debug', '--output-on-failure', '-R', '^(algo_suite_test&#124;kd_tree_test&#124;regex_test&#124;crypto_test&#124;octree_test&#124;thread_test&#124;datetime_test)$']; macOS arm64; focused rebuilt CMake owner tests for constructor and value-record APIs | Vexspoke cookbook constructor/value API regression coverage | passed |
| `tests/vexspoke/regex/run.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/regex/span_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/regex/vm_test.c` | ✅ | 1792031936 | 7dbdacbe585e777e0af067bc25ca2cd491877c1b9c1719d3272a159f6b30f1be | ['ctest', '--test-dir', 'cmake-build-debug', '--output-on-failure', '-R', '^(kd_tree_test&#124;octree_test&#124;compute_test&#124;datetime_test&#124;sha1_test&#124;vm_test)$']; macOS arm64; C23 CMake debug targets; offline deterministic owner tests; no live network or visual checks | Vexspoke value constructor macros in geometry, compute, time, SHA-1, and regex VM owners | passed |

### `tests/vexspoke/relational`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/vexspoke/relational/cell_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/relational/class_relational_test.c` | ✅ | 1792053060 | fcd16c0d100831511a377d81a1ca33978005593f6a8e5b6cf7cfb790a8c6dcea | ['./cmake-build-debug/bin/class_relational_test']; Command-only evidence; no broader readiness claim | Direct-return symbol getter in relational spotlight/search integration | passed |
| `tests/vexspoke/relational/shelf_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/relational/symbol_table_test.c` | ✅ | 1792053060 | ea61f4a4b24fe4651581df820ff5d5418499d34649247218efce73da912c31d7 | ['./cmake-build-debug/bin/symbol_table_test']; Command-only evidence; no broader readiness claim | Borrowed direct-return symbol name getter, invalid ids, rename and pointer registry cases | passed |
| `tests/vexspoke/relational/variable_hash_map_test.c` | ✅ | 1792053059 | a2a43c83f3cc8c12efd0da6d02f44825021e84d8e2c319bc9fdbe0d927e5501b | ['./cmake-build-debug/bin/variable_hash_map_test']; Command-only evidence; no broader readiness claim | Direct-return map getter API, collision chain, 3000-key volume, and public lookup callers | passed |
| `tests/vexspoke/relational/variable_mini_map_test.c` | ✅ | 1792053059 | ff6677bbf82f88275442942e1fa0353697a7bc8b92f990f49b529d058a64586f | ['./cmake-build-debug/bin/variable_mini_map_test']; Command-only evidence; no broader readiness claim | Direct-return scoped map getter API, bucket coverage, and SegmentIndex integration | passed |
| `tests/vexspoke/relational/variable_pool_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/relational/variable_slot_test.c` | ✅ | 1792852623 | dadb6d61d9a85adc73e12b59bc0c02342c90108dc2662f05839e7c54d48eb397 | ['./cmake-build-debug/bin/variable_slot_test']; macOS arm64; C23; debug build; direct owner binary from cmake-build-debug; no live network | Output-first VariableSlot_getName callers | passed |
| `tests/vexspoke/relational/variable_strict_test.c` | ✅ | 1792053060 | 895fb1e643940ff8353ef3d5e623adef6a181f7996a86c18ea82a6c4878bdda9 | ['./cmake-build-debug/bin/variable_strict_test']; Command-only evidence; no broader readiness claim | Borrowed direct-return dotted symbol name and strict relational behavior | passed |

### `tests/vexspoke/search`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/vexspoke/search/find_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/search/search_calc_test.c` | ✅ | 1792048703 | d33a55c16ee2c7c5f758894f682e0703a7b6fa291be05e178c0337c1282b0894 | ['cmake-build-debug/bin/search_calc_test']; macOS arm64; C23 CMake debug target; search calculator, matching, spotlight regression after removing obsolete DraftSort coupling | Search calculator and ranking owner test | passed |
| `tests/vexspoke/search/spotlight_test.c` | ✅ | 1792030498 | 30a573b99cc2369acbfc4721ce1e8304bd6278afb612002caacf7e645e7315d5 | ['env', 'B_HOME=/Users/vexgraph/vexgraph/cmake-build-debug/b-state', './tools/b', 'run', 'spotlight_test']; vexspoke | Spotlight ranking and calculator task recipe | passed |

### `tests/vexspoke/security`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/vexspoke/security/argon2_test.c` | ✅ | 1792385295 | c1da208b58e0f84824be9cfe99a62ef1edb817d63a8dddeb98346cde41f63bb3 | ['sh', '-c', 'CPU=suite/ecosystem/vexspoke; clang -std=gnu23 -Wall -Wextra -Werror -O2 -UNDEBUG -mcpu=apple-m1 -mmacosx-version-min=14.0 -I $CPU/src tests/vexspoke/security/blake2b_test.c $CPU/src/security/blake2b.c -o /tmp/blake2b_test && /tmp/blake2b_test && clang -std=gnu23 -Wall -Wextra -Werror -O2 -UNDEBUG -mcpu=apple-m1 -mmacosx-version-min=14.0 -I $CPU/src tests/vexspoke/security/argon2_test.c $CPU/src/security/argon2.c $CPU/src/security/blake2b.c -o /tmp/argon2_test && /tmp/argon2_test && clang -std=gnu23 -Wall -Wextra -Werror -O2 -UNDEBUG -mcpu=apple-m1 -mmacosx-version-min=14.0 -I $CPU/src -fsanitize=address,undefined tests/vexspoke/security/argon2_test.c $CPU/src/security/argon2.c $CPU/src/security/blake2b.c -o /tmp/argon2_test_san && /tmp/argon2_test_san']; macOS arm64 lab; clang -std=gnu23 -Wall -Wextra -Werror -O2 -UNDEBUG -mcpu=apple-m1 -mmacosx-version-min=14.0; optimized and ASan/UBSan runs | BLAKE2b against RFC 7693 and the official BLAKE2 KATs; Argon2id against the RFC 9106 Section 5.3 vector (pre-hash, all passes, final tag) with determinism, salt sensitivity and parameter refusal | passed |
| `tests/vexspoke/security/base32_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/security/blake2b_test.c` | ✅ | 1792385295 | dae2bcff8ccd338d46a25ba00fb626f31d41b3ab8d87fc730180d5ef4cbe8510 | ['sh', '-c', 'CPU=suite/ecosystem/vexspoke; clang -std=gnu23 -Wall -Wextra -Werror -O2 -UNDEBUG -mcpu=apple-m1 -mmacosx-version-min=14.0 -I $CPU/src tests/vexspoke/security/blake2b_test.c $CPU/src/security/blake2b.c -o /tmp/blake2b_test && /tmp/blake2b_test && clang -std=gnu23 -Wall -Wextra -Werror -O2 -UNDEBUG -mcpu=apple-m1 -mmacosx-version-min=14.0 -I $CPU/src tests/vexspoke/security/argon2_test.c $CPU/src/security/argon2.c $CPU/src/security/blake2b.c -o /tmp/argon2_test && /tmp/argon2_test && clang -std=gnu23 -Wall -Wextra -Werror -O2 -UNDEBUG -mcpu=apple-m1 -mmacosx-version-min=14.0 -I $CPU/src -fsanitize=address,undefined tests/vexspoke/security/argon2_test.c $CPU/src/security/argon2.c $CPU/src/security/blake2b.c -o /tmp/argon2_test_san && /tmp/argon2_test_san']; macOS arm64 lab; clang -std=gnu23 -Wall -Wextra -Werror -O2 -UNDEBUG -mcpu=apple-m1 -mmacosx-version-min=14.0; optimized and ASan/UBSan runs | BLAKE2b against RFC 7693 and the official BLAKE2 KATs; Argon2id against the RFC 9106 Section 5.3 vector (pre-hash, all passes, final tag) with determinism, salt sensitivity and parameter refusal | passed |
| `tests/vexspoke/security/chacha20_test.c` | ✅ | 1792387789 | 826f9841fbe4cd67339869d8f2b788bc5cd2dbb2e10a74f05566d993063ea1ae | ['sh', '-c', 'CPU=suite/ecosystem/vexspoke; CF="-std=gnu23 -Wall -Wextra -Werror -O2 -UNDEBUG -mcpu=apple-m1 -mmacosx-version-min=14.0"; clang $CF -I $CPU/src tests/vexspoke/security/chacha20_test.c $CPU/src/security/chacha20.c -o /tmp/c1 && /tmp/c1 && clang $CF -I $CPU/src tests/vexspoke/security/poly1305_test.c $CPU/src/security/poly1305.c -o /tmp/c2 && /tmp/c2 && clang $CF -I $CPU/src tests/vexspoke/security/chacha20poly1305_test.c $CPU/src/security/chacha20poly1305.c $CPU/src/security/chacha20.c $CPU/src/security/poly1305.c $CPU/src/security/crypto.c -o /tmp/c3 && /tmp/c3 && clang $CF -I $CPU/src tests/vexspoke/security/hkdf_test.c $CPU/src/security/hkdf.c $CPU/src/security/hmac.c $CPU/src/security/sha1.c $CPU/src/security/crypto.c -o /tmp/c4 && /tmp/c4 && clang $CF -fsanitize=address,undefined -I $CPU/src tests/vexspoke/security/chacha20poly1305_test.c $CPU/src/security/chacha20poly1305.c $CPU/src/security/chacha20.c $CPU/src/security/poly1305.c $CPU/src/security/crypto.c -o /tmp/c5 && /tmp/c5']; macOS arm64 lab; clang -std=gnu23 -Wall -Wextra -Werror -O2 -UNDEBUG -mcpu=apple-m1 -mmacosx-version-min=14.0; optimized and ASan/UBSan runs | ChaCha20 (RFC 8439 2.3.2/2.4.2), Poly1305 (2.5.2), ChaCha20-Poly1305 AEAD (2.8.2 plus forged-tag/flipped-bit/changed-AAD refusals), HKDF (RFC 5869 A.1/A.2/A.3) | passed |
| `tests/vexspoke/security/chacha20poly1305_test.c` | ✅ | 1792387789 | 4d3b9a211f06299f8c578a335f3fe3dda64623ca7302d4edcbfdad087af128e1 | ['sh', '-c', 'CPU=suite/ecosystem/vexspoke; CF="-std=gnu23 -Wall -Wextra -Werror -O2 -UNDEBUG -mcpu=apple-m1 -mmacosx-version-min=14.0"; clang $CF -I $CPU/src tests/vexspoke/security/chacha20_test.c $CPU/src/security/chacha20.c -o /tmp/c1 && /tmp/c1 && clang $CF -I $CPU/src tests/vexspoke/security/poly1305_test.c $CPU/src/security/poly1305.c -o /tmp/c2 && /tmp/c2 && clang $CF -I $CPU/src tests/vexspoke/security/chacha20poly1305_test.c $CPU/src/security/chacha20poly1305.c $CPU/src/security/chacha20.c $CPU/src/security/poly1305.c $CPU/src/security/crypto.c -o /tmp/c3 && /tmp/c3 && clang $CF -I $CPU/src tests/vexspoke/security/hkdf_test.c $CPU/src/security/hkdf.c $CPU/src/security/hmac.c $CPU/src/security/sha1.c $CPU/src/security/crypto.c -o /tmp/c4 && /tmp/c4 && clang $CF -fsanitize=address,undefined -I $CPU/src tests/vexspoke/security/chacha20poly1305_test.c $CPU/src/security/chacha20poly1305.c $CPU/src/security/chacha20.c $CPU/src/security/poly1305.c $CPU/src/security/crypto.c -o /tmp/c5 && /tmp/c5']; macOS arm64 lab; clang -std=gnu23 -Wall -Wextra -Werror -O2 -UNDEBUG -mcpu=apple-m1 -mmacosx-version-min=14.0; optimized and ASan/UBSan runs | ChaCha20 (RFC 8439 2.3.2/2.4.2), Poly1305 (2.5.2), ChaCha20-Poly1305 AEAD (2.8.2 plus forged-tag/flipped-bit/changed-AAD refusals), HKDF (RFC 5869 A.1/A.2/A.3) | passed |
| `tests/vexspoke/security/crypto_security_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/security/crypto_test.c` | ✅ | 1792031459 | d82348976f79fe2c7b35d0fb7a990594dab6eec1c5c4d92df298dd554c326721 | ['ctest', '--test-dir', 'cmake-build-debug', '--output-on-failure', '-R', '^(algo_suite_test&#124;kd_tree_test&#124;regex_test&#124;crypto_test&#124;octree_test&#124;thread_test&#124;datetime_test)$']; macOS arm64; focused rebuilt CMake owner tests for constructor and value-record APIs | Vexspoke cookbook constructor/value API regression coverage | passed |
| `tests/vexspoke/security/hkdf_test.c` | ✅ | 1792387789 | a4c4a6717db1bc9c6ae5b56fbfc87a65c1b3a1d2d7365d03ba7b380a22bd49d6 | ['sh', '-c', 'CPU=suite/ecosystem/vexspoke; CF="-std=gnu23 -Wall -Wextra -Werror -O2 -UNDEBUG -mcpu=apple-m1 -mmacosx-version-min=14.0"; clang $CF -I $CPU/src tests/vexspoke/security/chacha20_test.c $CPU/src/security/chacha20.c -o /tmp/c1 && /tmp/c1 && clang $CF -I $CPU/src tests/vexspoke/security/poly1305_test.c $CPU/src/security/poly1305.c -o /tmp/c2 && /tmp/c2 && clang $CF -I $CPU/src tests/vexspoke/security/chacha20poly1305_test.c $CPU/src/security/chacha20poly1305.c $CPU/src/security/chacha20.c $CPU/src/security/poly1305.c $CPU/src/security/crypto.c -o /tmp/c3 && /tmp/c3 && clang $CF -I $CPU/src tests/vexspoke/security/hkdf_test.c $CPU/src/security/hkdf.c $CPU/src/security/hmac.c $CPU/src/security/sha1.c $CPU/src/security/crypto.c -o /tmp/c4 && /tmp/c4 && clang $CF -fsanitize=address,undefined -I $CPU/src tests/vexspoke/security/chacha20poly1305_test.c $CPU/src/security/chacha20poly1305.c $CPU/src/security/chacha20.c $CPU/src/security/poly1305.c $CPU/src/security/crypto.c -o /tmp/c5 && /tmp/c5']; macOS arm64 lab; clang -std=gnu23 -Wall -Wextra -Werror -O2 -UNDEBUG -mcpu=apple-m1 -mmacosx-version-min=14.0; optimized and ASan/UBSan runs | ChaCha20 (RFC 8439 2.3.2/2.4.2), Poly1305 (2.5.2), ChaCha20-Poly1305 AEAD (2.8.2 plus forged-tag/flipped-bit/changed-AAD refusals), HKDF (RFC 5869 A.1/A.2/A.3) | passed |
| `tests/vexspoke/security/hmac_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/security/keychain_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/security/otpauth_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/security/password_test.c` | ✅ | 1792483531 | 180bf0683e5c1262e5c00449a966acc4cc755f49b2807e0dba6c2ef39ba2c153 | ['sh', '-c', 'CPU=suite/ecosystem/vexspoke; CFLAGS="-std=gnu23 -Wall -Wextra -Werror -O2 -UNDEBUG -mcpu=apple-m1 -mmacosx-version-min=14.0"; COMMON="$CPU/src/security/argon2.c $CPU/src/security/blake2b.c $CPU/src/security/hmac.c $CPU/src/security/sha1.c $CPU/src/security/crypto.c $CPU/src/security/secure_random.c"; clang $CFLAGS -I "$CPU/src" tests/vexspoke/security/password_test.c "$CPU/src/security/password.c" $COMMON -o /tmp/password_owner && /tmp/password_owner; clang $CFLAGS -I "$CPU/src" tests/vexspoke/security/password_verifier_test.c "$CPU/src/security/password.c" $COMMON -o /tmp/password_verifier_owner && /tmp/password_verifier_owner; clang $CFLAGS -fsanitize=address,undefined -I "$CPU/src" tests/vexspoke/security/password_verifier_test.c "$CPU/src/security/password.c" $COMMON -o /tmp/password_verifier_owner_san && /tmp/password_verifier_owner_san']; macOS arm64 lab; strict C23 clang with -Wall -Wextra -Werror -O2 and ASan/UBSan; OS CSPRNG | Legacy PBKDF2 vectors and versioned PBKDF2/Argon2id verifier creation, verification, malformed-parameter refusal, and KDF dispatch | passed |
| `tests/vexspoke/security/password_verifier_test.c` | ✅ | 1792483531 | 581bf4bdd60b963fc151200a824ce941456d5f8471b614239bdbd1f9157d3687 | ['sh', '-c', 'CPU=suite/ecosystem/vexspoke; CFLAGS="-std=gnu23 -Wall -Wextra -Werror -O2 -UNDEBUG -mcpu=apple-m1 -mmacosx-version-min=14.0"; COMMON="$CPU/src/security/argon2.c $CPU/src/security/blake2b.c $CPU/src/security/hmac.c $CPU/src/security/sha1.c $CPU/src/security/crypto.c $CPU/src/security/secure_random.c"; clang $CFLAGS -I "$CPU/src" tests/vexspoke/security/password_test.c "$CPU/src/security/password.c" $COMMON -o /tmp/password_owner && /tmp/password_owner; clang $CFLAGS -I "$CPU/src" tests/vexspoke/security/password_verifier_test.c "$CPU/src/security/password.c" $COMMON -o /tmp/password_verifier_owner && /tmp/password_verifier_owner; clang $CFLAGS -fsanitize=address,undefined -I "$CPU/src" tests/vexspoke/security/password_verifier_test.c "$CPU/src/security/password.c" $COMMON -o /tmp/password_verifier_owner_san && /tmp/password_verifier_owner_san']; macOS arm64 lab; strict C23 clang with -Wall -Wextra -Werror -O2 and ASan/UBSan; OS CSPRNG | Legacy PBKDF2 vectors and versioned PBKDF2/Argon2id verifier creation, verification, malformed-parameter refusal, and KDF dispatch | passed |
| `tests/vexspoke/security/poly1305_test.c` | ✅ | 1792387789 | 5a24cf2f2fca9ee80968b853dcbe279ab65369f2cda2463368e79a4ad342d75d | ['sh', '-c', 'CPU=suite/ecosystem/vexspoke; CF="-std=gnu23 -Wall -Wextra -Werror -O2 -UNDEBUG -mcpu=apple-m1 -mmacosx-version-min=14.0"; clang $CF -I $CPU/src tests/vexspoke/security/chacha20_test.c $CPU/src/security/chacha20.c -o /tmp/c1 && /tmp/c1 && clang $CF -I $CPU/src tests/vexspoke/security/poly1305_test.c $CPU/src/security/poly1305.c -o /tmp/c2 && /tmp/c2 && clang $CF -I $CPU/src tests/vexspoke/security/chacha20poly1305_test.c $CPU/src/security/chacha20poly1305.c $CPU/src/security/chacha20.c $CPU/src/security/poly1305.c $CPU/src/security/crypto.c -o /tmp/c3 && /tmp/c3 && clang $CF -I $CPU/src tests/vexspoke/security/hkdf_test.c $CPU/src/security/hkdf.c $CPU/src/security/hmac.c $CPU/src/security/sha1.c $CPU/src/security/crypto.c -o /tmp/c4 && /tmp/c4 && clang $CF -fsanitize=address,undefined -I $CPU/src tests/vexspoke/security/chacha20poly1305_test.c $CPU/src/security/chacha20poly1305.c $CPU/src/security/chacha20.c $CPU/src/security/poly1305.c $CPU/src/security/crypto.c -o /tmp/c5 && /tmp/c5']; macOS arm64 lab; clang -std=gnu23 -Wall -Wextra -Werror -O2 -UNDEBUG -mcpu=apple-m1 -mmacosx-version-min=14.0; optimized and ASan/UBSan runs | ChaCha20 (RFC 8439 2.3.2/2.4.2), Poly1305 (2.5.2), ChaCha20-Poly1305 AEAD (2.8.2 plus forged-tag/flipped-bit/changed-AAD refusals), HKDF (RFC 5869 A.1/A.2/A.3) | passed |
| `tests/vexspoke/security/secure_random_test.c` | ✅ | 1792024900 | 59dda4e92f16c6d43a1c791e429ccf690cde856fe2ce6fdf2243b63c19701dfe | ['ctest', '--test-dir', '/private/tmp/vexgraph-cmake-check-cmake', '--output-on-failure', '-R', '^(terminal_appearance_test&#124;vec2_test&#124;vec3_test&#124;vec4_test&#124;secure_random_test&#124;algo_suite_test&#124;dijkstra_test)$']; macOS arm64 C23 debug; CMake build /private/tmp/vexgraph-cmake-check-cmake; headless owner tests. | Constructor chooser C23 owner tests, including geometry and precision-vector overloads. | passed |
| `tests/vexspoke/security/sha1_test.c` | ✅ | 1792031936 | dedbd6ca9288652ca410401449a6fa47174b922e38f115c1deed4914a927a5b5 | ['ctest', '--test-dir', 'cmake-build-debug', '--output-on-failure', '-R', '^(kd_tree_test&#124;octree_test&#124;compute_test&#124;datetime_test&#124;sha1_test&#124;vm_test)$']; macOS arm64; C23 CMake debug targets; offline deterministic owner tests; no live network or visual checks | Vexspoke value constructor macros in geometry, compute, time, SHA-1, and regex VM owners | passed |
| `tests/vexspoke/security/totp_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/vexspoke/struct`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/vexspoke/struct/array_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/struct/chunked_list_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/struct/chunked_paged_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/struct/circle_array_test.c` | ✅ | 1792852623 | 816c716863251570a1f3699966199ffb6ad2243fde25cd9e5c8317584f83e626 | ['./cmake-build-debug/bin/circle_array_test']; macOS arm64; C23; debug build; direct owner binary from cmake-build-debug; no live network | Output-first CircleArray cell getters | passed |
| `tests/vexspoke/struct/collection_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/struct/deque_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/struct/exhaustion_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/struct/list_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/struct/map_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/struct/minheap_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/struct/octree_test.c` | ✅ | 1792032243 | 6d26916caaf41fe8e7eaea87265b2d9a9633f0a3ff07a72eace5ff33b2fccf28 | ['ctest', '--test-dir', 'cmake-build-debug', '--output-on-failure', '-R', '^octree_test$']; macOS arm64; C23 CMake debug owner test; in-process deterministic coverage; no visual checks | Octree public value constructors after internal node constructor rename | passed |
| `tests/vexspoke/struct/queue_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/struct/set_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/struct/sparseset_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/struct/spatial_struct_test.c` | ✅ | 1792052257 | 72236f5b1109665eadee9d3fa3c15a3ae3e594709eb7604dcd75e3ea69b709e9 | ['cmake-build-debug/bin/spatial_struct_test']; macOS native executable | Output-first spatial cell getter callers | passed |
| `tests/vexspoke/struct/sphere_array_test.c` | ✅ | 1792852623 | 98169990a518b68f4a9d6f8e5334b583a5416743939b0050f008280aec3de043 | ['./cmake-build-debug/bin/sphere_array_test']; macOS arm64; C23; debug build; direct owner binary from cmake-build-debug; no live network | Output-first SphereArray cell getters | passed |
| `tests/vexspoke/struct/stack_observability_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/struct/stack_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/vexspoke/system`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/vexspoke/system/app_detect_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/system/capture_tool_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/system/display_info_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/system/display_monitor_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/system/graphics_info_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/system/hardware_info_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/system/process_probe_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/system/system_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/vexspoke/thread`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/vexspoke/thread/compute_test.c` | ✅ | 1792031936 | 2f88d1be139e0f1ecf40a7493335f9b22cb993f63da87db1cf728e336d06e930 | ['ctest', '--test-dir', 'cmake-build-debug', '--output-on-failure', '-R', '^(kd_tree_test&#124;octree_test&#124;compute_test&#124;datetime_test&#124;sha1_test&#124;vm_test)$']; macOS arm64; C23 CMake debug targets; offline deterministic owner tests; no live network or visual checks | Vexspoke value constructor macros in geometry, compute, time, SHA-1, and regex VM owners | passed |
| `tests/vexspoke/thread/thread_test.c` | ✅ | 1792031459 | c500ff606e29eb0d46cc712311f0507bc3ba8c569ef6b6b405f96db7ee2dd0c9 | ['ctest', '--test-dir', 'cmake-build-debug', '--output-on-failure', '-R', '^(algo_suite_test&#124;kd_tree_test&#124;regex_test&#124;crypto_test&#124;octree_test&#124;thread_test&#124;datetime_test)$']; macOS arm64; focused rebuilt CMake owner tests for constructor and value-record APIs | Vexspoke cookbook constructor/value API regression coverage | passed |

### `tests/vexspoke/time`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/vexspoke/time/calendar_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/time/clock_test.c` | ✅ | 1792027315 | b304ab6e1a3bbd96c2dd08acc38f52af44f3fd978f013b3faedebf9e4bfc154c | ['sh', '-c', 'cmake-build-debug/b-state/out/debug/bin/hardware_input_test && cmake-build-debug/b-state/out/debug/bin/key_map_test && cmake-build-debug/b-state/out/debug/bin/circle_array_test && cmake-build-debug/b-state/out/debug/bin/sphere_array_test && cmake-build-debug/b-state/out/debug/bin/octree_test && cmake-build-debug/b-state/out/debug/bin/clock_test']; macOS arm64; C23; debug; constructor macro migrations in input, containers, and clock | Run owners after replacing init/create APIs with public constructor chooser macros | passed |
| `tests/vexspoke/time/datetime_test.c` | ✅ | 1792031936 | 722ade3acd63cdea20081f236ad4857ccbcc4cdb949fe05e279ee27d88a97465 | ['ctest', '--test-dir', 'cmake-build-debug', '--output-on-failure', '-R', '^(kd_tree_test&#124;octree_test&#124;compute_test&#124;datetime_test&#124;sha1_test&#124;vm_test)$']; macOS arm64; C23 CMake debug targets; offline deterministic owner tests; no live network or visual checks | Vexspoke value constructor macros in geometry, compute, time, SHA-1, and regex VM owners | passed |
| `tests/vexspoke/time/nanotime_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/time/time_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tests/vexspoke/util`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tests/vexspoke/util/arrays_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/util/hash_test.c` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |
| `tests/vexspoke/util/random_test.c` | ✅ | 1792025807 | 16180fd928d0057e8b52e83512c6926d21044b025e5e2ac171260840f69ff519 | ['/private/tmp/vexgraph-cmake-check-cmake/bin/random_test']; Command-only evidence; no broader readiness claim | Verify default and seeded Random constructor behavior | passed |

## workspace

### `tools`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tools/test_checklist.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

### `tools/python`

| Filename | Lab tested? | Last checked (Unix seconds) | SHA-256 at check | Evidence / scope | Description | Result |
| :--- | :---: | ---: | :--- | :--- | :--- | :--- |
| `tools/python/test_checklist.py` | ❌ | — | — | No executed evidence | Awaiting automated lab check | untested |

# Hotloading: the two-file application

> Proposal, not law yet. Everything below rests on the machinery that already
> exists in `vex-graph/hotcwap` (the loader, the trampoline table, the manifest
> ladder) and `vex-lib/lifetime` (Application/Window lifetime). Nothing here
> invents a second reloader.

## 1. The one idea

Every R5-R6 application is **two files**:

| file | role | rebuilt? |
| :--- | :--- | :--- |
| `main.c` | the **host** / opener | no, ever |
| `app-main.c` | the **application** | yes, every swap |

The host is a frozen `.app`/executable. It owns the process, the OS window, and
the lifetime. The application is compiled to a `.dylib` and lives in the
manifest ladder. When you rebuild the application, the host swaps it in place
and nothing you can see flickers.

That is the whole model. The rest of this document is just naming the pieces so
they stop feeling like "so many processes".

## 2. Why it feels like so many processes

There are **four layers** and only the first one is a process. Keep them apart
and the overwhelm goes away:

| layer | what it is | how many |
| :--- | :--- | :--- |
| 1. OS process | the `.app` / `main()` you launch | exactly one |
| 2. R1 lifetime | `Application` + `Window` (owned by the host) | one each |
| 3. the loader | one `HotModule` + a trampoline table | one |
| 4. the ladder | `bin/{backward,previous,current,new}/<lib>/` + `<lib>.generation` | on disk |

The "application process" you were thinking of is layer 4 -- a `.dylib` in
`bin/current/<lib>/`. It is **not** a second OS process. It is code the one
process loads and unloads.

## 3. What each file owns

**Host (`main.c`) -- boot only, no business logic (Law 6.4):**

1. mount the install ladder: `MANIFEST` -> `MANIFEST_LIBRARY` -> `MANIFEST_ENSURE`
   -> `MANIFEST_REFLECT` on first run
2. bind the loader: `Hot_init(library)`
3. create the OS window: `Frame(...)`
4. create the lifetime: `Application(...)` + `Frame_attachApplication`
5. hand the app to the reloader: `Application_setHot(app, hot)`
6. resolve the module's entry points with `Hot_get_symbol`
7. run: `Application_start(app)` (it polls `Hot_poll` for you)
8. tear down top-down: `HotShutdown` -> `Frame_destroy` -> `Application_free`

**Application (`app-main.c`) -- everything visible:**

- builds the panel tree into the borrowed `Frame` (`App_attach`)
- ticks one frame (`App_frame`)
- forgets its panels before unload (`App_detach`)
- saves/restores its logical state across a swap (`Hot_save`/`Hot_restore`)
- exports the loader table (`Hot_getExports`)

The host never draws. The application never owns the window, and it never owns
the panels either: `Frame_add` makes the Frame the owner. `App_detach` drops the
module's borrowed references only; `Frame_removePanels` is what frees them, and
it runs on the host side after detach. Freeing in both places is a d64 free.

The loader itself never calls `Hot_init_module` on load -- `dlopen` is the init.
It calls `Hot_shutdown_module` on `HotShutdown`, and nothing else on unload
(retired images leave through the grace ring). So `App_attach` is the module's
real initialization point, and `Hot_init_module` exists for module self-tests.

## 4. The swap, step by step

`Application_run` calls `Application_pollHot` roughly every 250 ms. That calls
`Hot_poll`, which compares `MANIFEST_GENERATION(library)` against the
generation it last saw. When the stamp moves:

1. **snapshot** -- a worker thread calls the old module's `Hot_save` (state blob)
2. **stage** -- `dlopen` the new `bin/current/<lib>/*.dylib`, verify each
   exports `Hot_getExports` (fail-closed: any bad section aborts all)
3. **restore** -- call the new module's `Hot_restore` with the old blob
   *before* anything is committed; a rejection rolls the whole swap back
4. **commit** -- swap the trampoline targets, retire the old handles into the
   grace ring (they stay mapped 4 polls so in-flight calls drain)
5. **notify** -- `hotReloadFn` fires on the host

`Hot_get_symbol` returns the row's current target, not a thunk: the host's
cached `App_frame` is a direct pointer into the image it was resolved from. That
is why the old image must stay mapped through the notification -- the host calls
the old `App_detach` (captured before the swap) and only then re-resolves.

The host's job in step 5 is small and is the only place the app tree is
rebuilt:

```c
static fn onReload(Application *app, u32 loaded, any userdata) {
    Host *host = userdata;
    if (host->detach) host->detach(host->scene);   // old module still mapped
    Frame_removePanels(host->frame);               // belt and braces
    host->attach = (AppAttachFn) Hot_get_symbol(host->hot, "App_attach");
    host->frameFn = (AppFrameFn) Hot_get_symbol(host->hot, "App_frame");
    host->detach  = (AppDetachFn) Hot_get_symbol(host->hot, "App_detach");
    host->scene   = host->attach ? host->attach(host->frame) : nullptr;
}
```

## 5. State across a swap

`app-main.c` ships one schema: a fixed 16-byte blob.

| offset | field | type |
| :--- | :--- | :--- |
| 0 | magic `VEXA` | `u32` |
| 4 | schema version (2) | `u32` |
| 8 | `pulseBias` | `f32` |
| 12 | `selected` | `i32` |

- What survives: what `Hot_save` writes and `Hot_restore` reads -- plain values
  only.
- What does not survive: any pointer into the module's own image, and any
  `Panel*` the module created. Panels belong to the `Frame` (host-owned, R4);
  the module rewrites them in `App_attach` after every swap.
- Schema changes: `Hot_restore` accepts the old layout by length (a 12-byte v1
  blob is promoted in place), and `Hot_migrate` converts a labelled legacy
  version to the current one. The loader tries `Hot_restore`, then
  `Hot_migrate` + `Hot_restore`, then rolls the whole swap back.

## 6. Build shape

The host is a normal `app` unit. The application is a new `module` unit --
a `.dylib` built with `-dynamiclib -fPIC -undefined dynamic_lookup` so it
resolves `Frame_*`/`Panel_*` from the host instead of linking a second copy of
R1-R4 (Law 6.3: no shadow owners -- one darling registry per process).

```json
"gallery_host": {
  "type": "app",
  "sources": ["vex-test/main.c"],
  "include_roots": ["vex-test"],
  "deps": ["darling_framework", "graphvex", "vexspoke", "lifetime",
           "relational_engine", "hotcwap"],
  "frameworks": ["IOSurface", "Vulkan"]
},
"gallery_app": {
  "type": "module",
  "sources": ["vex-test/app-main.c"],
  "include_roots": ["vex-test", "vex-lib/darling-framework",
                    "vex-lib/graphvex/src", "vex-lib/vexspoke"],
  "deps": []
}
```

The module declares no `deps` on purpose. Linking an archive would put a second
copy of R3/R4 objects in the image; `-undefined dynamic_lookup` makes the host's
already-loaded symbols the only ones.

`b` already has `lib` / `app` / `executable`; `module` is the one new branch:

```c
if (strcmp(unit_type, "module") == 0) {
    snprintf(out_path, sizeof out_path, "%s/%s.dylib", out_dir, unit_name);
    snprintf(link_cmd, sizeof link_cmd,
             "clang -dynamiclib -fPIC -undefined dynamic_lookup %s -o %s",
             obj_files, out_path);
    rc = system(link_cmd);
}
```

## 7. The dev loop

```
b build gallery_host        # the frozen shell (once)
b build gallery_app         # the reloadable part (every edit)
cp .b/out/gallery_app.dylib <root>/bin/new/gallery/     # stage
MANIFEST_PROMOTE()          # or the app's own update verb
# the running host's next poll swaps it in
```

During development you can skip the ladder and point the host at
`.b/out/` via `$VEX_MANIFEST`, but the shipped path is always the ladder.

## 8. The rule, stated

> **Two-file application rule.** Every R5-R6 application ships at least a
> host (`main.c`) and a reloadable application module (`app-main.c`). The host
> holds boot, window, and lifetime; the module holds behavior and state. The
> host is never rebuilt to change behavior.

A third shared `app_contract.h` is allowed -- it is the seam both files agree
on, not app logic.

## 9. What this does not do (honest scope)

- It does **not** make the app a separate OS process. It is an in-process
  dylib, exactly as `hotcwap` already ships it.
- It does **not** preserve `Panel*` across a swap. The module rebuilds its tree
  from `Hot_restore` state.
- It does **not** sandbox the module. Module code is trusted local build output,
  never model output.
- It does **not** prove the GPU path yet. `filter_gallery` builds and runs, but
  window/GPU activation needs a real GUI session to verify end to end.

## 10. Status, and what blocks a real build

Written and syntax-verified with `clang -fsyntax-only -std=gnu23 -Wall -Wextra
-Werror`:

| file | role | verified |
| :--- | :--- | :--- |
| `app_contract.h` | the seam | yes |
| `main.c` | host / opener | yes |
| `app-main.c` | reloadable module | yes |

Three pre-existing problems block `b build gallery_host` / `b build gallery_app`
today, plus one missing build unit. None of them are caused by these files, and
none should be papered over inside the module:

1. **`annotation/` is missing from the worktree root.** Every repo now includes
   `../../../annotation/*.h`, which resolves to `vexgraph/annotation/`, and that
   directory does not exist. The syntax check above used a throwaway copy at that
   relative depth; the real one has to be restored before anything compiles.
2. **The flattening is not reflected in the build files.** The repos no longer
   have a `src/` level (`vex-lib/lifetime/core`, `vex-lib/vexspoke/algo`, ...),
   but `b.assembly.json` still globs `vex-lib/lifetime/src/**/*.c` and
   `vex-lib/vexspoke/src/**/*.c` -- both currently match zero files -- and
   `CMakeLists.txt` still maps `suite/ecosystem/...`. `vexspoke` and `lifetime`
   therefore contribute no sources to any link.
3. **Include namespaces no longer exist as directories.** `frame.h` includes
   `"kernel/application.h"` and `"window/window.h"`; the files are
   `vex-lib/lifetime/core/application.h` and
   `vex-lib/lifetime/window/window.h`. `manifest.h` includes
   `"platform/platform.h"`, which is `vex-lib/lifetime/lifetime/platform.h`.
   Either those directories get renamed to the names the includes use, or the
   includes change to `core/`, `window/`, `lifetime/` with the matching roots
   declared once in `b.assembly.json`.
4. **`hotcwap` has no unit in `b.assembly.json`.** The loader and manifest
   (`vex-graph/hotcwap/*.c`) are not part of any `lib` entry, so `Hot_init`,
   `MANIFEST_*` and `Hot_get_symbol` are unresolved for every host that uses
   them. It needs a `lib` unit with `vex-graph/hotcwap` as its only include
   root before `gallery_host` can link.

The `module` build branch (section 6) is in `vex-graph/b/build.c`: a `module`
unit links a `.dylib` with `-dynamiclib -fPIC -undefined dynamic_lookup` and no
dep archives. `gallery_host` / `gallery_app` are **not** in `b.assembly.json`
yet, because that manifest itself still points at the pre-flattening `src/`
layout and has to be re-derived first.

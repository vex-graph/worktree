#ifndef VEX_APP_CONTRACT_H
#define VEX_APP_CONTRACT_H

#include "vex.h"

// app_contract.h — the seam between an application's HOST and its RELOADABLE
// MODULE.
//
// following the directory going forward:
// worktree > organization > repository > <directory tree> > file
//
// Two files, one seam:
//   main.c      (host)   includes this and CALLS the module through it.
//   app-main.c  (module) includes this and IMPLEMENTS every function below,
//                        shipping as a .dylib.
//
// The host owns the process, the OS Window/Frame, and the Application lifetime.
// The module owns the app's behavior and is unloaded/reloaded by hotcwap.
// Nothing here may own a pointer that outlives one module generation: the only
// things that cross a swap are plain values carried by Hot_save/Hot_restore.

typedef struct Frame Frame;

// Opaque per-generation scene handle returned by App_attach. The module decides
// what it means; the host only hands it back to App_frame and App_detach.
typedef struct AppScene AppScene;

// --- The module's app entry points (resolved via Hot_getSymbol) -------------

// Build the module's UI into the host-owned frame. Called once after the first
// load and again after every successful swap. Returns nullptr on failure.
typedef AppScene *(*AppAttachFn)(Frame *frame);

// Advance the scene one frame on the owner thread. `nowSeconds` is the host
// clock (never a frame count).
typedef fn (*AppFrameFn)(AppScene *scene, d64 nowSeconds);

// Drop the module's references and release anything the MODULE owns. Panels
// attached with Frame_add are owned by the Frame; the host clears them with
// Frame_removePanels, so this must never free them. Called before a swap and at
// shutdown, while the outgoing image is still mapped.
typedef fn (*AppDetachFn)(AppScene *scene);

#endif // VEX_APP_CONTRACT_H

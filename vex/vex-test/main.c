//
// Created by Vex on 11/2/26.
// this is for hotcwap designing process
//
// ============================================================================
// THE HOST / OPENER (main.c)
// ============================================================================
// The frozen shell. It boots, owns the OS window and the Application lifetime,
// binds the reloader, and never draws a pixel. Everything visible lives in the
// reloadable module (app-main.c) and is resolved through app_contract.h.
//
// Boot order (bottom-up):  manifest -> loader -> window -> application -> run.
// Teardown order (top-down): module detach -> frame -> application -> loader.
// ============================================================================

#include "app_contract.h"

#include "hotcwap/hot.h"
#include "hotcwap/manifest.h"
#include "darling/frame/frame.h"
#include "lifetime/core/application.h"

#include <stdint.h>
#include <stdio.h>
#include <time.h>

// The manifest library key this host hosts, and the bundled first-run payload.
#define APP_LIBRARY "gallery"
#define APP_TITLE "Gallery"
#define APP_WIDTH 1160
#define APP_HEIGHT 430
#define APP_BUNDLED "bundled/" APP_LIBRARY

// Everything the host keeps between frames. One struct, no file-scope globals.
typedef struct Host {
    HotModule *hot;
    Frame *frame;
    Application *app;
    AppScene *scene;
    AppAttachFn attach;
    AppFrameFn frameFn;
    AppDetachFn detach;
} Host;

// Monotonic seconds for the module's per-frame clock (never a frame count).
static double hostNow() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double) ts.tv_sec + (double) ts.tv_nsec / 1e9;
}

// Re-resolve the module's entry points and rebuild the scene. Runs after the
// first load and again after every successful swap.
static void hostAttach(Host *host) {
    (*host).attach = (AppAttachFn) Hot_getSymbol((*host).hot, "App_attach");
    (*host).frameFn = (AppFrameFn) Hot_getSymbol((*host).hot, "App_frame");
    (*host).detach = (AppDetachFn) Hot_getSymbol((*host).hot, "App_detach");
    if ((*host).attach)
        (*host).scene = (*host).attach((*host).frame);
}

// Hot-reload notification. The outgoing image is still mapped in the retire
// ring, so calling the OLD detach here is safe; then the new image rebuilds.
static void hostReload(Application *app, uint32_t loaded, void *userdata) {
    (void) app;
    (void) loaded;
    Host *host = userdata;
    if ((*host).detach)
        (*host).detach((*host).scene);
    Frame_removePanels((*host).frame);
    (*host).scene = nullptr;
    hostAttach(host);
}

// One frame: hand the clock to the module, which owns all drawing.
static void hostTick(Application *app, void *userdata) {
    (void) app;
    Host *host = userdata;
    if ((*host).frameFn && (*host).scene)
        (*host).frameFn((*host).scene, hostNow());
}

int main(void) {
    // 1. mount the install ladder (fail-closed, one-shot).
    if (!MANIFEST(MANIFEST_APP_DATA, "vexgraph", APP_LIBRARY))
        return 1;
    if (!MANIFEST_LIBRARY(APP_LIBRARY, (const char*) nullptr) || !MANIFEST_ENSURE())
        return 1;
    if (MANIFEST_IS_FIRST_RUN() && !MANIFEST_REFLECT(APP_LIBRARY, APP_BUNDLED))
        return 1;

    // 2. bind the reloader to this library's current/ set.
    Host host = {0};
    host.hot = Hot_init(APP_LIBRARY);
    if (!host.hot)
        return 1;

    // 3. the OS window: owned here, never reloaded.
    host.frame = Frame(APP_TITLE, APP_WIDTH, APP_HEIGHT);
    if (!host.frame) {
        Hot_shutdown(host.hot);
        return 1;
    }

    // 4. the lifetime: Application registers the window and services frames.
    host.app = Application(APP_TITLE);
    if (!host.app || !Frame_attachApplication(host.frame, host.app)) {
        Frame_destroy(host.frame);
        Hot_shutdown(host.hot);
        return 1;
    }

    // 5. hand the app to the reloader; Application_run polls Hot_poll for us.
    // R0 holds the watcher opaque; hotcwap provides the poll seam.
    Application_setHot(host.app, host.hot);
    Application_setHotPoll(host.app, (AppHotPollFn) Hot_poll);
    Application_onHotReload(host.app, hostReload, &host);

    // 6. first load, then resolve the module's entry points.
    uint32_t loaded = 0;
    if (Hot_poll(host.hot, &loaded) != HOT_OK) {
        Frame_destroy(host.frame);
        Hot_shutdown(host.hot);
        return 1;
    }
    hostAttach(&host);
    if (!host.attach || !host.frameFn) {
        Frame_destroy(host.frame);
        Hot_shutdown(host.hot);
        return 1;
    }
    if (!Application_addPollEvent(host.app, hostTick, &host)) {
        Frame_destroy(host.frame);
        Hot_shutdown(host.hot);
        return 1;
    }

    // 7. run: blocks until every window closes.
    Application_start(host.app);

    // 8. teardown, top-down: module, window, lifetime, loader.
    if (host.detach)
        host.detach(host.scene);
    Frame_destroy(host.frame);
    Application_free(host.app);
    Hot_shutdown(host.hot);
    return 0;
}

//
// Created by Vex on 11/2/26.
// this is another main for hotloading process that needs to be inserted into an executable to be replaced easily
//
// ============================================================================
// THE RELOADABLE APPLICATION (app-main.c)
// ============================================================================
// Compiled to a `.dylib` (type: "module") and swapped in place by hotcwap.
// It owns the app's BEHAVIOR and its small logical state; it never owns the
// process, the OS window, or the Frame. The host (main.c) calls into this file
// only through app_contract.h:
//
//     App_attach(frame)  -> build the panel tree into the host's frame
//     App_frame(scene, t)-> advance one frame (draw is the frame's job)
//     App_detach(scene)  -> drop references before the image is unloaded
//
// Panels attached with Frame_addPanel are OWNED by the Frame (darling R4).
// App_detach therefore never frees them: it only forgets them, and the host's
// Frame_removePanels is what actually releases them.
//
// The swap contract hotcwap reads off this image:
//     Hot_getExports  -> export table (the loader adopts it on dlopen)
//     Hot_save/Hot_restore    -> carry logical state across a generation
//     Hot_migrate             -> convert an older blob to this schema
//     Hot_shutdown_module     -> last call before dlclose
// ============================================================================

#include "app_contract.h"

#include "c23/overload.h"
#include "frame/frame.h"
#include "panel/panel.h"
#include "graphics/graphics.h"
#include "ui/element.h"

#include <math.h>
#include <stdint.h>
#include <string.h>

// following the directory going forward:
// worktree > organization > repository > <directory tree> > file
//
// This module may include downward only (R4 darling, R3 graphvex). It must not
// include lifetime/hotcwap headers: the host owns those, and the module is
// linked with -undefined dynamic_lookup so it borrows them at load time rather
// than building a second copy (Compose down, never rebuild / no shadow owners).

// ── state schema ────────────────────────────────────────────────────────────
// v2: magic + schema + pulseBias + selected. 16 bytes, fixed, POD only.
// No pointer ever enters this blob: a pointer into the old image is exactly what
// a swap must not preserve.
#define APP_SCHEMA_MAGIC 0x56455841u // "VEXA"
#define APP_SCHEMA_VERSION 2u
#define APP_STATE_SIZE 16u
#define APP_STATE_V1_SIZE 12u
#define APP_LEGACY_VERSION "1.0.0"

#define APP_CARD_COUNT 3
#define APP_CARD_WIDTH 320.0f
#define APP_CARD_HEIGHT 200.0f
#define APP_CARD_GAP 24.0f

// ── the scene: module-owned, one per generation ─────────────────────────────
// Static storage keeps the hot path allocation-free (Root Law 37). The host
// holds this pointer only between App_attach and App_detach.
struct AppScene {
    Frame *frame;                    // borrowed (host-owned)
    Panel *cards[APP_CARD_COUNT];    // borrowed after Frame_add (frame owns)
    u32 cardCount;
    f32 pulseBias;                 // survives a swap
    i32 selected;                // survives a swap
    f32 phase;                     // frame-local; resets on swap
};

static struct AppScene s_scene;

// ── palette ─────────────────────────────────────────────────────────────────
static const Color s_cardColor[APP_CARD_COUNT] = {
    COLOR_RGBA(94, 160, 220, 255),
    COLOR_RGBA(220, 140, 96, 255),
    COLOR_RGBA(120, 200, 150, 255),
};

// CORE FUNCTIONS (PUBLIC & PRIVATE)

// Drops the module's references to panels the host frame owns. Never frees.
static void sceneForget(struct AppScene *scene) {
    for (u32 i = 0; i < APP_CARD_COUNT; i++)
        (*scene).cards[i] = nullptr;
    (*scene).cardCount = 0;
    (*scene).frame = nullptr;
}

// ── the app contract ────────────────────────────────────────────────────────

/** Builds the card row into the host-owned frame and returns the scene. */
AppScene *App_attach(Frame *frame) {
    if (!frame) 
        return nullptr;

    struct AppScene *self = &s_scene;

    sceneForget(self);

    (*self).frame = frame;

    Rect root = Frame_root(frame);

    f32 rowWidth = APP_CARD_COUNT * APP_CARD_WIDTH + (APP_CARD_COUNT - 1) * APP_CARD_GAP;

    f32 startX = (root.w - rowWidth) * 0.5f;

    f32 y = (root.h - APP_CARD_HEIGHT) * 0.5f;

    for (u32 i = 0; i < APP_CARD_COUNT; i++) {
        Panel *card = Panel(APP_CARD_WIDTH, APP_CARD_HEIGHT);

        if (!card) {
            sceneForget(self);

            return nullptr;
        }

        Panel_setAnchor(card, PART_TOP_LEFT);

        Panel_setOffset(card, startX + (f32) i * (APP_CARD_WIDTH + APP_CARD_GAP), y);

        Panel_setRadius(card, 18.0f);

        Panel_setBackground(card, s_cardColor[i]);

        Panel_setShadow(card, 0.0f, 8.0f, 24.0f);

        Panel_setShadowColor(card, COLOR_RGBA(0, 0, 0, 90));

        if (!Frame_add(frame, card)) {
            Panel_destroy(card);

            sceneForget(self);

            return nullptr;
        }
        // Frame_add made the Frame the owner; this is a borrowed view.
        (*self).cards[i] = card;
    }

    (*self).cardCount = APP_CARD_COUNT;

    Frame_invalidate(frame);

    return &s_scene;
}

/** Advances one frame: the card row breathes, the selected card lifts. */
void App_frame(AppScene *scene, d64 nowSeconds) {
    if (!scene || !(*scene).frame) 
        return;

    (*scene).phase = (f32) nowSeconds + (*scene).pulseBias;

    f32 pulse = 0.5f + 0.5f * sinf((*scene).phase * 6.28318530718f);

    for (u32 i = 0; i < (*scene).cardCount; i++) {
        Panel *card = (*scene).cards[i];

        if (!card) 
            continue;

        bool selected = (i32) i == (*scene).selected;

        f32 grow = selected ? 1.0f + 0.06f * pulse : 1.0f;

        Panel_setSize(card, APP_CARD_WIDTH * grow, APP_CARD_HEIGHT * grow);
    }

    Frame_invalidate((*scene).frame);
}

/** Drops module references; the frame still owns (and later frees) the panels. */
void App_detach(AppScene *scene) {
    if (!scene) 
        return;

    sceneForget(scene);
}

// ── loader exports ──────────────────────────────────────────────────────────

/** Module initialization export (the loader reaches App_attach for real work). */
bool Hot_init_module(void) {
    s_scene.pulseBias = 0.0f;

    s_scene.selected = 0;

    s_scene.phase = 0.0f;

    sceneForget(&s_scene);

    return true;
}

/** Last call before dlclose: the frame has already released its own panels. */
void Hot_shutdown_module(void) {
    sceneForget(&s_scene);
}

/** Writes the v2 logical state blob. Plain values only. */
bool Hot_save(void *buf, bytes cap, bytes *outLen) {
    if (!buf || !outLen || cap < APP_STATE_SIZE) 
        return false;

    u8 *b = buf;

    const u32 magic = APP_SCHEMA_MAGIC;

    const u32 schema = APP_SCHEMA_VERSION;

    memcpy(b, &magic, 4);

    memcpy(b + 4, &schema, 4);

    memcpy(b + 8, &s_scene.pulseBias, 4);

    memcpy(b + 12, &s_scene.selected, 4);

    (*outLen) = APP_STATE_SIZE;

    return true;
}

/** Restores a v2 blob, or a v1 legacy blob promoted in place. */
bool Hot_restore(const void *buf, bytes len) {
    if (!buf) 
        return false;

    const u8 *b = buf;

    if (len == APP_STATE_V1_SIZE) {
        memcpy(&s_scene.pulseBias, b, 4);

        memcpy(&s_scene.selected, b + 4, 4);

        return true;
    }

    if (len != APP_STATE_SIZE) 
        return false;

    u32 magic = 0;

    u32 schema = 0;

    memcpy(&magic, b, 4);

    memcpy(&schema, b + 4, 4);

    if (magic != APP_SCHEMA_MAGIC || schema != APP_SCHEMA_VERSION) 
        return false;

    memcpy(&s_scene.pulseBias, b + 8, 4);

    memcpy(&s_scene.selected, b + 12, 4);

    return true;
}

/** Converts a supported legacy blob to the v2 layout, or copies a fitting one. */
bool Hot_migrate(const char *oldVersion, const void *oldBuf, bytes oldLen,
                 void *newBuf, bytes newCap, bytes *outLen) {
    if (!oldVersion || !oldBuf || !newBuf || !outLen || newCap < APP_STATE_SIZE) 
        return false;

    const u32 magic = APP_SCHEMA_MAGIC;

    const u32 schema = APP_SCHEMA_VERSION;

    if (strcmp(oldVersion, APP_LEGACY_VERSION) == 0 && oldLen == APP_STATE_V1_SIZE) {
        memcpy(newBuf, &magic, 4);

        memcpy((u8*) newBuf + 4, &schema, 4);

        memcpy((u8*) newBuf + 8, oldBuf, APP_STATE_V1_SIZE);

        (*outLen) = APP_STATE_SIZE;

        return true;
    }

    if (oldLen > newCap) 
        return false;

    memcpy(newBuf, oldBuf, oldLen);

    (*outLen) = oldLen;

    return true;
}

/** Static descriptor of this module (name, schema, exports, dependencies). */
const char *Hot_manifest(void) {
    return "{\"name\": \"gallery_app\", \"version\": \"2.0.0\", "
           "\"type_ids\": [{\"name\": \"GalleryState\", \"value\": 3}], "
           "\"exports\": [\"App_attach\", \"App_frame\", \"App_detach\", "
           "\"Hot_init_module\", \"Hot_shutdown_module\", "
           "\"Hot_save\", \"Hot_restore\", \"Hot_migrate\", "
           "\"Hot_getExports\"], "
           "\"dependencies\": []}";
}

// LOADER ABI EXPORT — row layout must match hot/hot.c:
//   { const char *name; void *fn; } entries[], count via Hot_getExports.
typedef struct HotModuleExport {
    const char *name;
    void *fn;
} HotModuleExport;

static const HotModuleExport s_exports[] = {
    { "App_attach",           (void*) App_attach },
    { "App_frame",            (void*) App_frame },
    { "App_detach",           (void*) App_detach },
    { "Hot_init_module",      (void*) Hot_init_module },
    { "Hot_shutdown_module",  (void*) Hot_shutdown_module },
    { "Hot_save",             (void*) Hot_save },
    { "Hot_restore",          (void*) Hot_restore },
    { "Hot_migrate",          (void*) Hot_migrate },
};

/** Returns this module's static trampoline export table and optional row count. */
const void *Hot_getExports(u32 *outCount) {
    if (outCount) 
        (*outCount) = (u32) (sizeof s_exports / sizeof s_exports[0]);

    return s_exports;
}

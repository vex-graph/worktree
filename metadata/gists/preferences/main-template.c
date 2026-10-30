/* main-template.c — the application entry shape (Vertical Integration Law) */

#include "annotation/definition.h"
#include "annotation/overview.h"

;;DEFINITION
/**
 * ============================================================================
 * DEFINITION: main
 * ============================================================================
 * The top of an application: build each owned object, wire it, start it, end
 * it, return 0. Composition only — no business logic lives here, and nothing
 * is re-implemented that a lower tier already owns (the Vertical Integration
 * Law, Compose down, never rebuild).
 * ============================================================================
 */

;;OVERVIEW
/**
 * ============================================================================
 * TEMPLATE: main (main.c)
 * ============================================================================
 * App/Window/Board are placeholders for whatever this interactable or superapp
 * actually owns; the shape is the law, the names follow their owning repo.
 *
 *   create<Object>   one file-local helper per owned object, returning it
 *   main             create -> wire -> start -> end -> release -> return 0
 * ============================================================================
 */

#include "app/app.h"

/* These helpers are the bespoke layer: the custom UI, the custom algorithms,
   the thing this interactable or superapp exists to be — assembled FROM the
   lower-tier contracts. They compose those contracts; they never re-implement
   them. Each returns the object it built; nothing is a destination parameter
   (Value Return Law). */
static App *createApp(void)
{
   return App(...);
}

static Window *createWindow(void)
{
   return Window(...);
}

static Board *createBoard(void)
{
   return Board(...);
}

int main(void)
{
   /* 1. build every owned object first, so each failure point is one line */
   App *app = createApp();
   Window *window = createWindow();
   Board *board = createBoard();

   /* 2. wire them: lower-tier objects are referenced, never rebuilt here */
   App_attachWindow(app, window);
   Window_attachBoard(window, board);

   /* 3. run: start blocks until the application ends */
   App_start(app);

   /* 4. end top-down: detach before free, in reverse creation order */
   App_stop(app);

   Board_free(board);
   Window_free(window);
   App_free(app);

   /* 5. the host's arena reset is the last teardown step, never this file */
   return 0;
}

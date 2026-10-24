# Hotcwap — public call reference

`Window_new` and `Window_create` remain legacy public constructor functions in
the header; the requested constructor-macro API is `Window(...)`. This example
uses that macro and covers the non-constructor public `Window_*` calls.
`WindowEvent_init` remains an initializer function without the requested
constructor macro.

## Kernel class (kernel.c)

`Kernel(...)` is the constructor macro. Registry-copy getters
(`Kernel_getApplications`, `Kernel_getProcesses`, `Kernel_getConsoles`, and
`Kernel_getCommandLines`) still write caller-provided arrays, so they remain
Value Return Law migration gaps. `Kernel_run` is called below after the
registries are empty; the kind-specific `Kernel_runProcess`,
`Kernel_runConsole`, `Kernel_runApplication`, and `Kernel_runCommandLine` calls
need live executable objects and remain runtime gaps. `Kernel_addRunFunction`
and `Kernel_addEndFunction`
require callback definitions, which this one-main format cannot provide, so
those registration calls remain callback gaps.

```c
#include "kernel/kernel.h"
#include "kernel/application.h"
#include "kernel/commandline.h"
#include "kernel/console.h"
#include "kernel/process.h"

int main(void)
{
    Kernel *kernel = Kernel();
    Kernel *sizedKernel = Kernel(67108864u);
    Kernel *boundedKernel = Kernel(33554432u, 67108864u);
    Kernel *legacyKernel = Kernel();
    Application *application = Application("application-name-goes-here");
    Process *process = Process(nullptr);
    Console *console = Console();
    CommandLine *commandLine = CommandLine();

    KernelPhase phase = Kernel_getPhase(kernel);
    bool isRunning = Kernel_isRunning(kernel);
    Application *registeredApplication = Kernel_getApplication(kernel, 0u);
    uint32_t applicationCount = Kernel_getApplicationCount(kernel);
    Process *registeredProcess = Kernel_getProcess(kernel, 0u);
    uint32_t processCount = Kernel_getProcessCount(kernel);
    Console *registeredConsole = Kernel_getConsole(kernel, 0u);
    uint32_t consoleCount = Kernel_getConsoleCount(kernel);
    CommandLine *registeredCommandLine = Kernel_getCommandLine(kernel, 0u);
    uint32_t commandLineCount = Kernel_getCommandLineCount(kernel);
    uint32_t runFunctionCount = Kernel_getRunFunctionCount(kernel);
    uint32_t endFunctionCount = Kernel_getEndFunctionCount(kernel);
    void *arena = Kernel_getArena(kernel);
    void *transientArena = Kernel_getTransientArena(kernel);
    Lifetime *lifetime = Kernel_getLifetime(kernel);
    const Lifetime *lifetimeView = Kernel_lifetime(kernel);

    Kernel_setGfxAppRunner(kernel, nullptr);
    int (*gfxAppRunner)(void *, bool (*)(void *), bool (*)(void)) = Kernel_getGfxAppRunner(kernel);
    Kernel_addApplication(kernel, application);
    bool removedApplication = Kernel_removeApplication(kernel, application);
    bool addedProcess = Kernel_addProcess(kernel, process);
    bool removedProcess = Kernel_removeProcess(kernel, process);
    bool addedConsole = Kernel_addConsole(kernel, console);
    bool removedConsole = Kernel_removeConsole(kernel, console);
    bool addedCommandLine = Kernel_addCommandLine(kernel, commandLine);
    bool removedCommandLine = Kernel_removeCommandLine(kernel, commandLine);
    int emptyRunStatus = Kernel_run(kernel);
    Kernel_stop(kernel);


    Kernel_free(kernel);
    Kernel_free(sizedKernel);
    Kernel_free(boundedKernel);
    Kernel_destroy(legacyKernel);
    bool processFreed = Process_free(process);
    Console_free(console);
    CommandLine_free(commandLine);
    Application_free(application);
    return 0;
}
```

## Window class (window_cocoa.m)

`Window_getLocation`, `Window_getContentOrigin`, `Window_getSizePoints`,
`Window_readPresentSurface`, `Window_macOS_getTrafficLightHeaderPosition`, and
`Window_macOS_getLiquidGlass` still require caller-provided output destinations.
They are migration gaps under the value-return rule and are omitted here.
`Window_writePNG` and
`Window_presentRGBA` needs actual pixel storage, which this example does not
create. The retired pane-compositor calls are inert stubs, so they are omitted
as non-usage.

```c
#include "window/window.h"

int main(void)
{
    Window *window = Window();
    bool shouldClose = Window_shouldClose(window);
    Window_setShouldClose(window, false);
    Window_close(window);
    Window_pollEvents();
    bool hasMoreEvents = Window_pollEventStep();
    Window_waitEvents(window, 0);
    Window_setTitle(window, "window-title-goes-here");
    int width = Window_width(window);
    int height = Window_height(window);
    Window_setSize(window, 800, 600);
    Window_setLocation(window, 20, 30);
    Window_center(window);
    Window_show(window);
    Window_hide(window);
    Window_setVisible(window, true);
    float scale = Window_getScale(window);
    Window_revalidate(window);
    Window_setSizePoints(window, 800.0f, 600.0f);
    float widthPoints = Window_widthPoints(window);
    float heightPoints = Window_heightPoints(window);
    int viewportWidth = Window_viewportWidth(window);
    int viewportHeight = Window_viewportHeight(window);
    float viewportWidthPoints = Window_viewportWidthPoints(window);
    float viewportHeightPoints = Window_viewportHeightPoints(window);
    int windowWidth = Window_windowWidth(window);
    int windowHeight = Window_windowHeight(window);
    float windowWidthPoints = Window_windowWidthPoints(window);
    float windowHeightPoints = Window_windowHeightPoints(window);
    Window_setBottomLayer(window, nullptr);
    void *bottomLayer = Window_getBottomLayer(window);
    Window_setTopLayer(window, nullptr);
    void *topLayer = Window_getTopLayer(window);
    Window_orderLayers(window);
    Window_compositeBoards(window);
    Window_setPresentMode(window, WINDOW_PRESENT_FIFO);
    int presentMode = Window_getPresentMode(window);
    Window_setTransparent(window, true);
    bool isTransparent = Window_isTransparent(window);
    void *surface = Window_createPresentSurface(window, 800, 600);
    Window_presentSurface(window, surface);
    Window_presentSurfaceContents(window);
    Window_destroyPresentSurface(window, surface);
    uint64_t renderGeneration = Window_renderGeneration(window);
    Window_setEnabled(window, true);
    bool isEnabled = Window_isEnabled(window);
    bool isLiveResizing = Window_isLiveResizing(window);
    bool isResizable = Window_isResizable(window);
    Window_setResizable(window, true);
    bool isClosable = Window_isClosable(window);
    Window_setClosable(window, true);
    bool isMiniaturizable = Window_isMiniaturizable(window);
    Window_setMiniaturizable(window, true);
    Window_setFullscreenButton(window, true);
    Window_setUndecorated(window, WINDOW_DECORATED);
    Window_setDecorated(window, true);
    bool isDecorated = Window_isDecorated(window);
    Window_setNaked(window, false);
    bool isNaked = Window_isNaked(window);
    Window_setBorderless(window, false);
    bool isBorderless = Window_isBorderless(window);
    Window_setViewportFlushToTop(window, false);
    bool isViewportFlushToTop = Window_isViewportFlushToTop(window);
    Window_setFloatingTrafficLights(window, false);
    Window_macOS_setTrafficLightButtonVisible(window, WINDOW_TRAFFIC_LIGHT_CLOSE, true);
    bool isCloseButtonVisible = Window_macOS_isTrafficLightButtonVisible(window, WINDOW_TRAFFIC_LIGHT_CLOSE);
    Window_macOS_setTrafficLightHeaderPosition(window, 12.0f, 8.0f);
    bool hasLiquidGlass = Window_macOS_hasLiquidGlass();
    Window_macOS_setLiquidGlass(window, nullptr);
    Window_setOpacity(window, 1.0f);
    Window_setTransparentBackground(window, false);
    Window_setBackdropBlur(window, 0.0f);
    Window_setAlwaysOnTop(window, false);
    Window_setClickThrough(window, false);
    Window_setShadow(window, true);
    Window_setMovableByBackground(window, false);
    Window_bringToFront(window);
    Window_attachChild(window, nullptr);
    Window_detachChild(window, nullptr);
    Window_minimize(window);
    Window_restore(window);
    bool isMinimized = Window_isMinimized(window);
    bool isFullscreen = Window_isFullscreen(window);
    Window_setFullscreen(window, false);
    Window_toggleFullscreen(window);
    Window_setDRM(window, false);
    Window_setMinSize(window, 320, 240);
    Window_setMaxSize(window, 1920, 1080);
    Window_setCursorType(window, WINDOW_CURSOR_DEFAULT);
    WindowCursorType cursorType = Window_getCursorType(window);
    Window_setCursorLocked(window, false);
    void *contentView = Window_contentView(window);
    void *nativeHandle = Window_nativeHandle(window);
    void *metalLayer = Window_metalLayer(window);
    Window_setGravityTopLeft(window);
    Window_workerPresentBegin();
    Window_workerPresentEnd();
    bool framePresented = Window_present(window, nullptr);
    Window_addKeyAdapter(window, nullptr);
    bool keyAdapterRemoved = Window_removeKeyAdapter(window, nullptr);
    Window_addMouseAdapter(window, nullptr);
    bool mouseAdapterRemoved = Window_removeMouseAdapter(window, nullptr);
    Window_addTouchAdapter(window, nullptr);
    bool touchAdapterRemoved = Window_removeTouchAdapter(window, nullptr);
    WindowEvent *lifecycle = Window_getLifecycle(window);
    Window_dispatchEvents(window);
    uint32_t windowId = Window_id(window);
    Window_focus(window);
    bool isFocused = Window_isFocused(window);
    Window_setKeyEnabled(window, true);
    bool isKeyEnabled = Window_isKeyEnabled(window);
    uint32_t monitorId = Window_getMonitorId(window);
    uint64_t sizeGeneration = Window_sizeGeneration(window);
    WindowResizeRenderFn resizeRenderHook = Window_getResizeRenderHook(window);
    Window_destroy(window);











































    Window_destroyAll();
    return 0;
}
```

## Window class (window.c)

This Win32 fallback defines `Window_create` but does not define the
`Window(...)` constructor macro arms; the macro is a construction gap for this
implementation. The output-pointer getters (`Window_getSizePoints`,
`Window_getContentOrigin`, `Window_getLocation`, and
`Window_macOS_getTrafficLightHeaderPosition`) remain Value Return Law gaps and
are omitted. The remaining functions are safe-default stubs in this file and
are shown with a null handle because it has no available constructor macro.

```c
#include "window/window.h"

int main(void)
{
    Window *window = nullptr;
    Window_destroy(window);
    Window_destroyAll();
    bool shouldClose = Window_shouldClose(window);
    Window_setShouldClose(window, false);
    Window_pollEvents();
    bool hasMoreEvents = Window_pollEventStep();
    Window_setPresentMode(window, WINDOW_PRESENT_FIFO);
    int presentMode = Window_getPresentMode(window);
    Window_setTransparent(window, true);
    bool transparent = Window_isTransparent(window);
    uint64_t renderGeneration = Window_renderGeneration(window);
    Window_setEnabled(window, true);
    bool enabled = Window_isEnabled(window);
    Window_setTitle(window, "window-title-goes-here");
    Window_setSize(window, 800, 600);
    float scale = Window_getScale(window);
    Window_revalidate(window);
    Window_setSizePoints(window, 800.0f, 600.0f);
    float widthPoints = Window_widthPoints(window);
    float heightPoints = Window_heightPoints(window);
    int viewportWidth = Window_viewportWidth(window);
    int viewportHeight = Window_viewportHeight(window);
    float viewportWidthPoints = Window_viewportWidthPoints(window);
    float viewportHeightPoints = Window_viewportHeightPoints(window);
    int windowWidth = Window_windowWidth(window);
    int windowHeight = Window_windowHeight(window);
    float windowWidthPoints = Window_windowWidthPoints(window);
    float windowHeightPoints = Window_windowHeightPoints(window);
    Window_setLocation(window, 24, 32);
    WindowResizeRenderFn resizeHook = Window_getResizeRenderHook(window);
    uint32_t monitorId = Window_getMonitorId(window);
    Window_center(window);
    Window_setVisible(window, true);
    bool resizable = Window_isResizable(window);
    Window_setResizable(window, true);
    bool closable = Window_isClosable(window);
    Window_setClosable(window, true);
    bool miniaturizable = Window_isMiniaturizable(window);
    Window_setMiniaturizable(window, true);
    Window_setFullscreenButton(window, true);
    Window_setUndecorated(window, WINDOW_DECORATED);
    Window_setDecorated(window, true);
    bool decorated = Window_isDecorated(window);
    Window_setNaked(window, false);
    bool naked = Window_isNaked(window);
    Window_setBorderless(window, false);
    bool borderless = Window_isBorderless(window);
    Window_setViewportFlushToTop(window, false);
    bool flushToTop = Window_isViewportFlushToTop(window);
    Window_setFloatingTrafficLights(window, false);
    Window_macOS_setTrafficLightButtonVisible(window, WINDOW_TRAFFIC_LIGHT_CLOSE, true);
    bool trafficLightVisible = Window_macOS_isTrafficLightButtonVisible(window, WINDOW_TRAFFIC_LIGHT_CLOSE);
    Window_macOS_setTrafficLightHeaderPosition(window, 12.0f, 8.0f);
    Window_minimize(window);
    Window_restore(window);
    bool minimized = Window_isMinimized(window);
    bool fullscreen = Window_isFullscreen(window);
    Window_setFullscreen(window, false);
    Window_toggleFullscreen(window);
    Window_setDRM(window, false);
    Window_setMinSize(window, 320, 240);
    Window_setMaxSize(window, 1920, 1080);
    Window_setCursorType(window, WINDOW_CURSOR_DEFAULT);
    WindowCursorType cursorType = Window_getCursorType(window);
    Window_compositeBoards(window);
    void *contentView = Window_contentView(window);
    void *nativeHandle = Window_nativeHandle(window);
    return 0;
}
```

## WindowEvent class (window_event.c)

`WindowEvent_init` is a lower-level initializer, not a preferred constructor;
the `Window(...)` macro creates and initializes its embedded lifecycle record.
The example uses `Window_getLifecycle` and setter calls instead.

```c
#include "window/window.h"
#include "window/window_event.h"

int main(void)
{
    Window *window = Window();
    WindowEvent *events = Window_getLifecycle(window);
    WindowEvent_setSelf(events, nullptr);
    void *owner = WindowEvent_getSelf(events);
    WindowEvent_setOnQuitRequested(events, nullptr);
    WindowQuitRequestedFn onQuitRequested = WindowEvent_getOnQuitRequested(events);
    WindowEvent_setOnAfterQuit(events, nullptr);
    WindowNoArgFn onAfterQuit = WindowEvent_getOnAfterQuit(events);
    WindowEvent_setOnResized(events, nullptr);
    WindowResizedFn onResized = WindowEvent_getOnResized(events);
    WindowEvent_setOnMoved(events, nullptr);
    WindowMovedFn onMoved = WindowEvent_getOnMoved(events);
    WindowEvent_setOnFullscreen(events, nullptr);
    WindowNoArgFn onFullscreen = WindowEvent_getOnFullscreen(events);
    WindowEvent_setOnMinimized(events, nullptr);
    WindowNoArgFn onMinimized = WindowEvent_getOnMinimized(events);
    WindowEvent_setOnRestored(events, nullptr);
    WindowNoArgFn onRestored = WindowEvent_getOnRestored(events);
    WindowEvent_setOnPressed(events, nullptr);
    WindowNoArgFn onPressed = WindowEvent_getOnPressed(events);
    WindowEvent_setOnFocusGained(events, nullptr);
    WindowNoArgFn onFocusGained = WindowEvent_getOnFocusGained(events);
    WindowEvent_setOnFocusLost(events, nullptr);
    WindowNoArgFn onFocusLost = WindowEvent_getOnFocusLost(events);
    WindowEvent_setOnZoomFilled(events, nullptr);
    WindowNoArgFn onZoomFilled = WindowEvent_getOnZoomFilled(events);
    WindowEvent_setOnZoomBack(events, nullptr);
    WindowNoArgFn onZoomBack = WindowEvent_getOnZoomBack(events);
    WindowEvent_setOnOcclusionChanged(events, nullptr);
    WindowOcclusionFn onOcclusionChanged = WindowEvent_getOnOcclusionChanged(events);
    bool quitRequested = WindowEvent_fireQuitRequested(events, window);
    WindowEvent_fireAfterQuit(events, window);
    WindowEvent_fireResized(events, window, 800, 600);
    WindowEvent_fireMoved(events, window, 20, 30);
    WindowEvent_fireFullscreen(events, window);
    WindowEvent_fireMinimized(events, window);
    WindowEvent_fireRestored(events, window);
    WindowEvent_firePressed(events, window);
    WindowEvent_fireFocusGained(events, window);
    WindowEvent_fireFocusLost(events, window);
    WindowEvent_fireZoomFilled(events, window);
    WindowEvent_fireZoomBack(events, window);
    WindowEvent_fireOcclusionChanged(events, window, true);
    Window_destroy(window);














    return 0;
}
```

## Capability class (capability.c)

```c
#include "capability/capability.h"

int main(void)
{
    Capability_probe();
    bool hasDotProduct = Capability_has(CAPABILITY_CPU_DOTPROD);
    const char *capabilityName = Capability_kindName(CAPABILITY_CPU_DOTPROD);
    int osMajor = Capability_osMajor();



    return 0;
}
```

## HotTrampolineTable class (hot_trampoline.c)

`HotTrampolineTable_toString` and `HotTrampolineTable_toStringStruct` still
require caller-provided buffers and are API migration gaps.

```c
#include "hot/hot_trampoline.h"

int main(void)
{
    HotTrampolineTable table = HotTrampolineTable();
    bool reserved = HotTrampolineTable_reserve(&table, 16u);
    int functionIndex = HotTrampolineTable_register(&table, "function-name-goes-here");
    int foundIndex = HotTrampolineTable_find(&table, "function-name-goes-here");
    HotTrampolineTable_set(&table, functionIndex, nullptr);
    void *functionPointer = HotTrampolineTable_get(&table, functionIndex);
    uint64_t exhaustionCount = HotTrampolineTable_exhaustionCount(&table);
    HotTrampolineTable_free(&table);




    return 0;
}
```

## HotRetireRing class (hot_retire.c)

`HotRetireRing` has no constructor macro or public setters. Its API expects an
initialized owner embedded in `HotModule`; a standalone example cannot create
that state without aggregate initialization. `HotRetireRing_retire`,
`HotRetireRing_advance`, and `HotRetireRing_drainAll` remain constructor/API
gaps.

```c
int main(void)
{
    return 0;
}
```

## Throwable functions (throwable.c)

`Throwable_throw` terminates the process. `Throwable_registerTeardown` and
`Throwable_unregisterTeardown` require a real callback, which this one-main
cookbook format cannot define; the nonfatal try/catch check and teardown runner
are shown directly.

```c
#include "hot/throwable.h"

int main(void)
{
    bool conditionPassed = Throwable_tryCatch(true, EXCEPTION_RUNTIME,
        "site-name-goes-here", __FILE__, __LINE__, "message-goes-here", "");
    Throwable_runTeardown();

    return 0;
}
```

## Lifetime class (lifetime.c)

The class has value-returning `Lifetime_bind` but no preferred `Lifetime(...)`
constructor macro; `Lifetime_create` is the current legacy factory and remains
a constructor-macro gap.

```c
#include "spoke/lifetime.h"

int main(void)
{
    Lifetime lifetime = Lifetime_bind(nullptr, nullptr, 0u, 0u, nullptr);
    bool persistentArenaIsLegit = Lifetime_isLegit(nullptr);
    bool lifetimeIsValid = Lifetime_isValid(&lifetime);
    void *persistentBlock = Lifetime_allocPersistent(&lifetime, VEXSPOKE_TYPE_ARENA, 64u);
    void *transientBlock = Lifetime_allocTransient(&lifetime, VEXSPOKE_TYPE_ARENA, 64u);
    Lifetime_freePersistent(&lifetime, persistentBlock);
    Lifetime_resetTransient(&lifetime);
    Lifetime_destroy(&lifetime);



    return 0;
}
```

## Ledger class (ledger.c)

`Ledger_lastVersion` still writes into a caller-provided destination buffer and
is an API migration gap.

```c
#include "hot/ledger.h"

int main(void)
{
    Ledger *ledger = Ledger_open("organization-name-goes-here", "application-name-goes-here");
    bool recorded = Ledger_recordInstall(ledger, "version-goes-here");
    bool hasRecord = Ledger_hasRecord(ledger);
    LedgerState state = Ledger_state(ledger);
    const char *lastError = Ledger_lastError(ledger);
    bool markedUninstalled = Ledger_markUninstalled(ledger);
    bool forgotten = Ledger_forget(ledger);
    Ledger_free(ledger);






    return 0;
}
```

## Permission class (permission.c)

The platform backends, including `permission/objc/permission_cocoa.m`, implement
internal `permissionBackend*` hooks; the public call surface is declared in
`permission.h` and shown here. The backend hooks are not public cookbook APIs.

```c
#include "permission/permission.h"

int main(void)
{
    PermissionKind kind = PERMISSION_SCREEN_CAPTURE;
    PermissionStatus status = Permission_status(kind);
    bool requested = Permission_request(kind);
    bool requiresRestart = Permission_requiresRestart(kind);
    bool openedSettings = Permission_openSettings(kind);
    const char *kindName = Permission_kindName(kind);
    const char *statusName = Permission_statusName(status);





    return 0;
}
```

## Hot behavior module functions (hot_behavior.c)

`Hot_save`, `Hot_migrate`, `hot_behavior_bar`, and `VkModuleGetTrampolines`
still require caller-owned output buffers or pointers and remain API migration
gaps. `Hot_restore` consumes a caller-owned byte span directly.

```c
#include <stddef.h>

bool Hot_init_module(void);
void Hot_shutdown_module(void);
bool Hot_restore(const void *buffer, size_t length);
const char *Hot_manifest(void);
float hot_behavior_pulse(double nowSeconds);
const char *hot_texture_path(void);
void hot_behavior_set_phase_bias(float value);
float hot_behavior_get_phase_bias(void);

int main(void)
{
    bool initialized = Hot_init_module();
    bool restored = Hot_restore(nullptr, 0u);
    const char *manifest = Hot_manifest();
    float pulse = hot_behavior_pulse(0.0);
    const char *texturePath = hot_texture_path();
    hot_behavior_set_phase_bias(0.25f);
    float phaseBias = hot_behavior_get_phase_bias();
    Hot_shutdown_module();






    return 0;
}
```

## Console class (console.c)

`Console_poll` returns output through its buffer and length arguments, so it is
an API migration gap. `ConsoleIo` is a raw function-pointer table with no
constructor macro or per-entry setters, so the example does not initialize or
expose its callbacks. Passing `nullptr` leaves execution disconnected;
`Console_run` then demonstrates its direct boolean result.

```c
#include "kernel/console.h"

int main(void)
{
    Console *console = Console("shell-command-goes-here");
    Console_setShell(console, "shell-command-goes-here");
    Console_setWorkDir(console, "working-directory-goes-here");
    const ConsoleIo *configuredIo = Console_getIo(console);
    Console_setIo(console, nullptr, nullptr);
    const char *shell = Console_getShell(console);
    const char *workDir = Console_getWorkDir(console);
    bool started = Console_run(console);
    bool wroteInput = Console_writeInput(console, "input-line-goes-here", 20u);
    bool isRunning = Console_isRunning(console);
    int exitStatus = Console_getExitStatus(console);
    Console_cancel(console);
    Console_free(console);







    return 0;
}
```

## Process class (process.c)

`Process` requires an entry callback, and `Process_run` requires a caller-owned
exit-status destination. The one-main cookbook format cannot define a callback
helper, so construction, execution, replacement, and all instance queries are
gaps: `Process`, `Process_run`, `Process_replace`, `Process_setName`,
`Process_free`, `Process_isRunning`, `Process_getInvocationCount`,
`Process_getEntry`, `Process_getContext`, `Process_getHot`, and
`Process_getName`.

```c
int main(void)
{
    return 0;
}
```

## CommandLine class (commandline.c)

`CommandLine_poll` writes the event into a caller-owned output record, and
`CommandLine_toString` / `CommandLine_toStringStruct` write to destination
buffers; those APIs are migration gaps. The application seam requires callback
functions, which this cookbook format does not define; `CommandLine_setApp`,
`CommandLine_tick`, and `CommandLine_run` are consequently callback callability
gaps. `CommandLine_open` needs a real backend implementation and cannot be
shown with the null backend used by this no-helper example.

```c
#include "kernel/commandline.h"

int main(void)
{
    CommandLine *line = CommandLine("terminal-title-goes-here");
    const CommandLineIo *io = CommandLine_getIo(line);
    bool resetBackend = CommandLine_setIo(line, nullptr);
    bool revalidated = CommandLine_revalidate(line);
    bool presented = CommandLine_present(line);
    bool cleared = CommandLine_clear(line);
    bool mouseReporting = CommandLine_setMouseReporting(line, false);
    bool hasApp = CommandLine_hasApp(line);
    bool detached = CommandLine_detachApp(line);
    CommandLine_stop(line);
    CommandLine_requestCancel(line);
    bool isRunning = CommandLine_isRunning(line);
    size_t width = CommandLine_getWidth(line);
    size_t height = CommandLine_getHeight(line);
    size_t capacity = CommandLine_getCapacity(line);
    char *cells = CommandLine_getCells(line);
    const char *constCells = CommandLine_getCellsConst(line);
    CommandLine_setTitle(line, "updated-terminal-title-goes-here");
    const char *title = CommandLine_getTitle(line);
    uint64_t generation = CommandLine_getGeneration(line);
    size_t exhaustionCount = CommandLine_exhaustionCount(line);
    bool isOpen = CommandLine_isOpen(line);
    bool isActive = CommandLine_isActive(line);
    bool isCancelled = CommandLine_isCancelled(line);
    CommandLine_close(line);
    CommandLine_free(line);






















    return 0;
}
```

## CommandLine default backend functions (commandline_ncurses.c)

```c
#include "kernel/commandline.h"

int main(void)
{
    CommandLineIo defaultIo = CommandLine_defaultIo();

    return 0;
}
```

## TrafficLight class (traffic_light_cocoa.m)

The class has only `TrafficLight_create`, not the preferred
`TrafficLight(...)` constructor macro, so its instance methods are blocked:
`TrafficLight_destroy`, `TrafficLight_setButtonVisible`,
`TrafficLight_isButtonVisible`, `TrafficLight_setHeaderPosition`,
`TrafficLight_resetBase`, `TrafficLight_refresh`, and
`TrafficLight_setFloating`. `TrafficLight_getHeaderPosition` additionally
requires output pointers.

```c
int main(void)
{
    return 0;
}
```

## Application class (application.c)

`Application_getWindows` writes its registry into a caller-owned array and is
an API migration gap. Callback registration, removal, invocation, and clearing
are shown with null callbacks; this demonstrates those call shapes without
defining helper functions. `Application(...)` performs the one-shot bootstrap;
the separate `Application_init()` lifecycle call is not shown as a constructor.

```c
#include "kernel/application.h"

int main(void)
{
    Application *application = Application("application-name-goes-here",
        "author-name-goes-here", "1.0.0");
    Application_setName(application, "updated-application-name-goes-here");
    Application_setAuthor(application, "updated-author-name-goes-here");
    Application_setVersion(application, "1.1.0");
    Application_setIconPath(application, "icon-path-goes-here");
    const char *name = Application_getName(application);
    const char *author = Application_getAuthor(application);
    const char *version = Application_getVersion(application);
    const char *iconPath = Application_getIconPath(application);
    uint32_t fps = Application_getFps(application);
    uint32_t frameTimeUs = Application_getFrametimeUs(application);
    HotModule *hot = Application_getHot(application);
    Application_setHot(application, hot);
    Application_poll(application);
    bool began = Application_begin(application);
    bool isRunning = Application_isRunning(application);
    bool isFinished = Application_isFinished(application);
    bool startCallbackAdded = Application_addStartEvent(application, nullptr, nullptr);
    bool pollCallbackAdded = Application_addPollEvent(application, nullptr, nullptr);
    bool pollCallbackRemoved = Application_removePollEvent(application, nullptr, nullptr);
    bool invocationAccepted = Application_invoke(application, nullptr, nullptr);
    Application_onHotReload(application, nullptr, nullptr);
    Application_pollHot(application);
    Application_start(application);
    Application_run(application);
    Application_close(application);
    Application_stop(application);
    Application_finish(application);
    Application *current = Application_current();
    uint32_t windowCount = Application_getWindowCount(application);
    Window *window = Application_getWindow(application, 0u);
    bool addedWindow = Application_addWindow(application, window);
    bool removedWindow = Application_removeWindow(application, window);
    Application_free(application);
    Application_shutdown();


















    return 0;
}
```

## Manifest module functions (manifest.c)

`UNINSTALL(...)` calls `Manifest_uninstall` and intentionally deletes the
selected install tree, so it is documented as a destructive-operation gap and
omitted. `Manifest_init` is reached through the preferred `MANIFEST(...)`
macro. `ManifestPath` still
has no preferred destination-free constructor macro. `ManifestPath_begin`,
`ManifestPath_push`, `ManifestPath_get`, `ManifestPath_len`,
`ManifestPath_ladderDir`, `ManifestPath_libraryDir`,
`ManifestPath_generationFile`, `ManifestPath_cacheDir`, and
`ManifestPath_manifestJson` remain constructor or caller-buffer API gaps.

```c
#include "hot/manifest.h"

int main(void)
{
    bool mounted = MANIFEST(MANIFEST_APP_DATA,
        "organization-name-goes-here", "application-name-goes-here");
    bool libraryRegistered = MANIFEST_LIBRARY("library-name-goes-here", (const char*) nullptr);
    const char *root = MANIFEST_ROOT();
    bool ensured = MANIFEST_ENSURE();
    bool reflected = MANIFEST_REFLECT("library-name-goes-here", "payload-directory-goes-here");
    bool updated = MANIFEST_UPDATE("library-name-goes-here", "staged-payload-directory-goes-here");
    bool allowed = MANIFEST_ALLOWS("library-name-goes-here", "section-filename-goes-here");
    uint32_t sectionCount = MANIFEST_SECTION_COUNT("library-name-goes-here");
    uint64_t generation = MANIFEST_GENERATION("library-name-goes-here");
    bool requiresRecovery = MANIFEST_REQUIRES_RECOVERY();
    bool firstRun = MANIFEST_IS_FIRST_RUN();
    bool promotedLibrary = MANIFEST_PROMOTE_LIBRARY("library-name-goes-here");
    bool revertedLibrary = MANIFEST_REVERT_LIBRARY("library-name-goes-here", generation);
    bool promoted = MANIFEST_PROMOTE();













    return 0;
}
```

## HotModule class (hot.c)

`Hot_init` is the current legacy factory; `HotModule(...)` does not yet exist.
The public `Hot_get_symbol`, `Hot_get_generation`, and `Hot_last_error` getters
also need a constructible module. `Hot_updateCold`, `Hot_poll`,
`Hot_requiresRecovery`,
`Hot_shutdown_module`, `Hot_save_module`, `Hot_restore_module`, and
`Hot_migrate_module` operations need a constructible module; update, poll, save,
and migrate also use caller-provided result buffers or counts. They remain
constructor and value-return API gaps.

```c
int main(void)
{
    return 0;
}
```

## Window class (window_linux.c)

This backend exposes legacy `Window_create` but no `Window(...)` constructor
macro implementation. The `Window_getLocation`, `Window_getContentOrigin`, and
`Window_macOS_getTrafficLightHeaderPosition` APIs still write caller-owned
output pointers. These constructor/value APIs are explicit gaps; null-safe
public calls are shown without fabricating a Window object.

```c
#include "window/window.h"

int main(void)
{
    Window *window = nullptr;
    bool shouldClose = Window_shouldClose(window);
    Window_setShouldClose(window, false);
    Window_pollEvents();
    bool moreEvents = Window_pollEventStep();
    Window_setPresentMode(window, WINDOW_PRESENT_FIFO);
    int presentMode = Window_getPresentMode(window);
    Window_setTransparent(window, true);
    bool isTransparent = Window_isTransparent(window);
    uint64_t renderGeneration = Window_renderGeneration(window);
    Window_setEnabled(window, true);
    bool isEnabled = Window_isEnabled(window);
    Window_setTitle(window, "window-title-goes-here");
    Window_setSize(window, 800, 600);
    Window_setLocation(window, 20, 30);
    WindowResizeRenderFn resizeHook = Window_getResizeRenderHook(window);
    uint32_t monitorId = Window_getMonitorId(window);
    Window_center(window);
    Window_setVisible(window, true);
    bool isResizable = Window_isResizable(window);
    Window_setResizable(window, true);
    bool isClosable = Window_isClosable(window);
    Window_setClosable(window, true);
    bool isMiniaturizable = Window_isMiniaturizable(window);
    Window_setMiniaturizable(window, true);
    Window_setFullscreenButton(window, true);
    Window_setUndecorated(window, WINDOW_DECORATED);
    Window_setDecorated(window, true);
    bool isDecorated = Window_isDecorated(window);
    Window_setNaked(window, false);
    bool isNaked = Window_isNaked(window);
    Window_setBorderless(window, false);
    bool isBorderless = Window_isBorderless(window);
    Window_setViewportFlushToTop(window, false);
    bool flushesToTop = Window_isViewportFlushToTop(window);
    Window_setFloatingTrafficLights(window, false);
    Window_macOS_setTrafficLightButtonVisible(window, WINDOW_TRAFFIC_LIGHT_CLOSE, true);
    bool trafficLightVisible = Window_macOS_isTrafficLightButtonVisible(window, WINDOW_TRAFFIC_LIGHT_CLOSE);
    Window_macOS_setTrafficLightHeaderPosition(window, 12.0f, 8.0f);
    Window_minimize(window);
    Window_restore(window);
    bool isMinimized = Window_isMinimized(window);
    bool isFullscreen = Window_isFullscreen(window);
    Window_setFullscreen(window, false);
    Window_toggleFullscreen(window);
    Window_setDRM(window, false);
    Window_setMinSize(window, 320, 240);
    Window_setMaxSize(window, 1920, 1080);


















    return 0;
}
```

## Window class (window_win32.c)

`Window_getLocation`, `Window_getContentOrigin`, `Window_getSizePoints`, and
`Window_macOS_getTrafficLightHeaderPosition` still require output destinations
and are migration gaps. `Window_create` remains a legacy constructor function;
this implementation provides the requested `Window(...)` constructor macro.

```c
#include "window/window.h"

int main(void)
{
    Window *window = Window();
    bool shouldClose = Window_shouldClose(window);
    Window_setShouldClose(window, false);
    Window_close(window);
    Window_pollEvents();
    bool moreEvents = Window_pollEventStep();
    Window_setPresentMode(window, WINDOW_PRESENT_FIFO);
    int presentMode = Window_getPresentMode(window);
    Window_setTransparent(window, true);
    bool isTransparent = Window_isTransparent(window);
    uint64_t renderGeneration = Window_renderGeneration(window);
    Window_orderLayers(window);
    Window_setBottomLayer(window, nullptr);
    void *bottomLayer = Window_getBottomLayer(window);
    Window_setTopLayer(window, nullptr);
    void *topLayer = Window_getTopLayer(window);
    Window_compositeBoards(window);
    Window_setEnabled(window, true);
    bool isEnabled = Window_isEnabled(window);
    bool isLiveResizing = Window_isLiveResizing(window);
    Window_setTitle(window, "window-title-goes-here");
    int width = Window_width(window);
    int height = Window_height(window);
    float scale = Window_getScale(window);
    Window_revalidate(window);
    Window_setSizePoints(window, 800.0f, 600.0f);
    float widthPoints = Window_widthPoints(window);
    float heightPoints = Window_heightPoints(window);
    int viewportWidth = Window_viewportWidth(window);
    int viewportHeight = Window_viewportHeight(window);
    float viewportWidthPoints = Window_viewportWidthPoints(window);
    float viewportHeightPoints = Window_viewportHeightPoints(window);
    int windowWidth = Window_windowWidth(window);
    int windowHeight = Window_windowHeight(window);
    float windowWidthPoints = Window_windowWidthPoints(window);
    float windowHeightPoints = Window_windowHeightPoints(window);
    Window_setSize(window, 800, 600);
    Window_setLocation(window, 20, 30);
    Window_center(window);
    Window_show(window);
    Window_hide(window);
    Window_setVisible(window, true);
    Window_setEnabled(window, true);
    WindowResizeRenderFn resizeHook = Window_getResizeRenderHook(window);
    uint32_t monitorId = Window_getMonitorId(window);
    bool isResizable = Window_isResizable(window);
    Window_setResizable(window, true);
    bool isClosable = Window_isClosable(window);
    Window_setClosable(window, true);
    bool isMiniaturizable = Window_isMiniaturizable(window);
    Window_setMiniaturizable(window, true);
    Window_setFullscreenButton(window, true);
    Window_setUndecorated(window, WINDOW_DECORATED);
    Window_setDecorated(window, true);
    bool isDecorated = Window_isDecorated(window);
    Window_setNaked(window, false);
    bool isNaked = Window_isNaked(window);
    Window_setBorderless(window, false);
    bool isBorderless = Window_isBorderless(window);
    Window_setViewportFlushToTop(window, false);
    bool flushesToTop = Window_isViewportFlushToTop(window);
    Window_setFloatingTrafficLights(window, false);
    Window_macOS_setTrafficLightButtonVisible(window, WINDOW_TRAFFIC_LIGHT_CLOSE, true);
    bool trafficLightVisible = Window_macOS_isTrafficLightButtonVisible(window, WINDOW_TRAFFIC_LIGHT_CLOSE);
    Window_macOS_setTrafficLightHeaderPosition(window, 12.0f, 8.0f);
    Window_setOpacity(window, 1.0f);
    Window_setTransparentBackground(window, false);
    Window_setAlwaysOnTop(window, false);
    Window_setClickThrough(window, false);
    Window_setShadow(window, true);
    Window_setMovableByBackground(window, false);
    Window_bringToFront(window);
    Window_attachChild(window, nullptr);
    Window_detachChild(window, nullptr);
    Window_minimize(window);
    Window_restore(window);
    bool isMinimized = Window_isMinimized(window);
    bool isFullscreen = Window_isFullscreen(window);
    Window_setFullscreen(window, false);
    Window_toggleFullscreen(window);
    Window_setDRM(window, false);
    Window_setMinSize(window, 320, 240);
    Window_setMaxSize(window, 1920, 1080);
    Window_setCursorLocked(window, false);
    Window_setCursorType(window, WINDOW_CURSOR_DEFAULT);
    WindowCursorType cursorType = Window_getCursorType(window);
    bool presented = Window_present(window, nullptr);
    void *contentView = Window_contentView(window);
    void *nativeHandle = Window_nativeHandle(window);
    void *metalLayer = Window_metalLayer(window);
    Window_setGravityTopLeft(window);
    Window_workerPresentBegin();
    Window_workerPresentEnd();
    Window_addKeyAdapter(window, nullptr);
    bool removedKeyAdapter = Window_removeKeyAdapter(window, nullptr);
    Window_addMouseAdapter(window, nullptr);
    bool removedMouseAdapter = Window_removeMouseAdapter(window, nullptr);
    Window_addTouchAdapter(window, nullptr);
    bool removedTouchAdapter = Window_removeTouchAdapter(window, nullptr);
    Window_dispatchEvents(window);
    uint32_t windowId = Window_id(window);
    Window_focus(window);
    bool isFocused = Window_isFocused(window);
    Window_setKeyEnabled(window, true);
    bool isKeyEnabled = Window_isKeyEnabled(window);
    WindowEvent *lifecycle = Window_getLifecycle(window);
    uint32_t monitorIdAgain = Window_getMonitorId(window);
    uint64_t sizeGeneration = Window_sizeGeneration(window);
    Window_destroy(window);


















































    return 0;
}
```

## Window class (window_wayland.c)

This Wayland backend is a draft translation unit and is not wired into the
build. The `Window(...)` macro constructs the class. `Window_getLocation`,
`Window_getContentOrigin`, `Window_getSizePoints`,
`Window_macOS_getTrafficLightHeaderPosition`, and the `Window_new(desc)`
constructor are documented gaps here: output-pointer getters violate the
value-return preference and `Window_new` has no `Window(desc)` macro arm.

```c
#include "window/window.h"

int main(void)
{
    Window *window = Window();
    bool shouldClose = Window_shouldClose(window);
    Window_setShouldClose(window, false);
    Window_close(window);
    Window_pollEvents();
    bool moreEvents = Window_pollEventStep();
    Window_setPresentMode(window, WINDOW_PRESENT_FIFO);
    int presentMode = Window_getPresentMode(window);
    Window_setTransparent(window, true);
    bool isTransparent = Window_isTransparent(window);
    uint64_t renderGeneration = Window_renderGeneration(window);
    Window_orderLayers(window);
    Window_setBottomLayer(window, nullptr);
    void *bottomLayer = Window_getBottomLayer(window);
    Window_setTopLayer(window, nullptr);
    void *topLayer = Window_getTopLayer(window);
    Window_compositeBoards(window);
    Window_setEnabled(window, true);
    bool isEnabled = Window_isEnabled(window);
    bool isLiveResizing = Window_isLiveResizing(window);
    Window_setTitle(window, "window-title-goes-here");
    int width = Window_width(window);
    int height = Window_height(window);
    float scale = Window_getScale(window);
    Window_revalidate(window);
    Window_setSizePoints(window, 800.0f, 600.0f);
    float widthPoints = Window_widthPoints(window);
    float heightPoints = Window_heightPoints(window);
    int viewportWidth = Window_viewportWidth(window);
    int viewportHeight = Window_viewportHeight(window);
    float viewportWidthPoints = Window_viewportWidthPoints(window);
    float viewportHeightPoints = Window_viewportHeightPoints(window);
    int windowWidth = Window_windowWidth(window);
    int windowHeight = Window_windowHeight(window);
    float windowWidthPoints = Window_windowWidthPoints(window);
    float windowHeightPoints = Window_windowHeightPoints(window);
    Window_setSize(window, 800, 600);
    Window_setLocation(window, 20, 30);
    Window_center(window);
    Window_show(window);
    Window_hide(window);
    Window_setVisible(window, true);
    WindowResizeRenderFn resizeHook = Window_getResizeRenderHook(window);
    uint32_t monitorId = Window_getMonitorId(window);
    bool isResizable = Window_isResizable(window);
    Window_setResizable(window, true);
    bool isClosable = Window_isClosable(window);
    Window_setClosable(window, true);
    bool isMiniaturizable = Window_isMiniaturizable(window);
    Window_setMiniaturizable(window, true);
    Window_setFullscreenButton(window, true);
    Window_setUndecorated(window, WINDOW_DECORATED);
    Window_setDecorated(window, true);
    bool isDecorated = Window_isDecorated(window);
    Window_setNaked(window, false);
    bool isNaked = Window_isNaked(window);
    Window_setBorderless(window, false);
    bool isBorderless = Window_isBorderless(window);
    Window_setViewportFlushToTop(window, false);
    bool flushesToTop = Window_isViewportFlushToTop(window);
    Window_setFloatingTrafficLights(window, false);
    Window_macOS_setTrafficLightButtonVisible(window, WINDOW_TRAFFIC_LIGHT_CLOSE, true);
    bool trafficLightVisible = Window_macOS_isTrafficLightButtonVisible(window, WINDOW_TRAFFIC_LIGHT_CLOSE);
    Window_macOS_setTrafficLightHeaderPosition(window, 12.0f, 8.0f);
    Window_setOpacity(window, 1.0f);
    Window_setTransparentBackground(window, false);
    Window_setAlwaysOnTop(window, false);
    Window_setClickThrough(window, false);
    Window_setShadow(window, true);
    Window_setMovableByBackground(window, false);
    Window_bringToFront(window);
    Window_attachChild(window, nullptr);
    Window_detachChild(window, nullptr);
    Window_minimize(window);
    Window_restore(window);
    bool isMinimized = Window_isMinimized(window);
    bool isFullscreen = Window_isFullscreen(window);
    Window_setFullscreen(window, false);
    Window_toggleFullscreen(window);
    Window_setDRM(window, false);
    Window_setMinSize(window, 320, 240);
    Window_setMaxSize(window, 1920, 1080);
    Window_setCursorLocked(window, false);
    Window_setCursorType(window, WINDOW_CURSOR_DEFAULT);
    WindowCursorType cursorType = Window_getCursorType(window);
    bool presented = Window_present(window, nullptr);
    void *contentView = Window_contentView(window);
    void *nativeHandle = Window_nativeHandle(window);
    void *metalLayer = Window_metalLayer(window);
    Window_setGravityTopLeft(window);
    Window_workerPresentBegin();
    Window_workerPresentEnd();
    Window_addKeyAdapter(window, nullptr);
    bool removedKeyAdapter = Window_removeKeyAdapter(window, nullptr);
    Window_addMouseAdapter(window, nullptr);
    bool removedMouseAdapter = Window_removeMouseAdapter(window, nullptr);
    Window_addTouchAdapter(window, nullptr);
    bool removedTouchAdapter = Window_removeTouchAdapter(window, nullptr);
    Window_dispatchEvents(window);
    uint32_t windowId = Window_id(window);
    Window_focus(window);
    bool isFocused = Window_isFocused(window);
    Window_setKeyEnabled(window, true);
    bool isKeyEnabled = Window_isKeyEnabled(window);
    WindowEvent *lifecycle = Window_getLifecycle(window);
    uint64_t sizeGeneration = Window_sizeGeneration(window);
    Window_destroy(window);

















































    return 0;
}
```

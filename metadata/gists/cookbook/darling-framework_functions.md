# Darling Framework — public call reference

Darling Framework has no local preferences file in this checkout. The
implementation and test laws were read; this missing lawbook remains a
documented reading gap. The example covers the retained `Picture` class.

## Picture class (picture.c)

`Picture_toString` and `Picture_toStringStruct` require caller-owned output
buffers and remain Value Return Law migration gaps.

```c
#include "drawable/picture.h"

int main(void)
{
    Image *borrowedImage = nullptr;
    Picture *picture = Picture(borrowedImage);
    Picture_setImage(picture, borrowedImage);
    Picture_setSize(picture, 128.0f, 96.0f);
    Picture_setLocation(picture, 24.0f, 32.0f);
    Element *graphics = Picture_graphics(picture);
    const Image *image = Picture_image(picture);
    float width = Picture_width(picture);
    float height = Picture_height(picture);
    Point location = Picture_location(picture);
    Picture_destroy(picture);
    return 0;
}
```

## ScrollPanel class (scroll_panel.c)

`ScrollPanel(...)` is the constructor macro. The viewport owns the content
element. Getter results are returned directly and stored in local values.
`ScrollPanel_addMouseEvent`, `ScrollPanel_addScrollEvent`,
`ScrollPanel_addZoomEvent`, `ScrollPanel_addKeyEvent`,
`ScrollPanel_addTouchEvent`, and `ScrollPanel_addDocumentEvent` need handler
records with callback fields; those records have no constructor macro or
setters, and real handlers need definitions outside `main()`. Those callback
registration calls remain API ergonomics gaps.

```c
#include "panel/scroll_panel.h"
#include "ui/element.h"

int main(void)
{
    ScrollPanel *emptyScrollPanel = ScrollPanel();
    ScrollPanel *squareScrollPanel = ScrollPanel(160.0f);
    ScrollPanel *scrollPanel = ScrollPanel(320.0f, 240.0f);
    Element *content = Element();
    Element *sizedContent = Element_setSize(content, 640.0f, 960.0f);
    ScrollPanel_setContent(scrollPanel, content);
    ScrollPanel_setViewportSize(scrollPanel, 320.0f, 240.0f);
    ScrollPanel_setContentSize(scrollPanel, 640.0f, 960.0f);
    float viewportWidth = ScrollPanel_viewportWidth(scrollPanel);
    float viewportHeight = ScrollPanel_viewportHeight(scrollPanel);
    float contentWidth = ScrollPanel_contentWidth(scrollPanel);
    float contentHeight = ScrollPanel_contentHeight(scrollPanel);
    Element *viewport = ScrollPanel_graphics(scrollPanel);
    Element *attachedContent = ScrollPanel_content(scrollPanel);
    bool canScrollX = ScrollPanel_canScrollX(scrollPanel);
    bool canScrollY = ScrollPanel_canScrollY(scrollPanel);
    float maxX = ScrollPanel_maxX(scrollPanel);
    float maxY = ScrollPanel_maxY(scrollPanel);
    ScrollPanel_setOffset(scrollPanel, maxX, maxY);
    float offsetX = ScrollPanel_getOffsetX(scrollPanel);
    float offsetY = ScrollPanel_getOffsetY(scrollPanel);
    ScrollPanel_scrollBy(scrollPanel, -offsetX, -offsetY);
    ScrollPanel_revalidate(scrollPanel);
    ScrollPanel_destroy(scrollPanel);
    ScrollPanel_destroy(emptyScrollPanel);
    ScrollPanel_destroy(squareScrollPanel);
    return 0;
}
```

## Hit module (hit.c)

`Hit_resolve` is the only public function in this file, but its current
signature requires a caller-provided `Hit *out`. That API is a Value Return
Law migration blocker, so this example does not demonstrate a nonconforming
call. The function has no constructor macro.

```c
#include "event/hit.h"

int main(void)
{
    return 0;
}
```

## Element event module (event_invoke.c)

`Event` has no preferred constructor macro or setters, so
`Element_dispatchEvent` cannot be demonstrated without writing its fields
directly. `Element_addMouseEvent`, `Element_addScrollEvent`,
`Element_addZoomEvent`, `Element_addKeyEvent`, `Element_addTouchEvent`, and
`Element_addDocumentEvent` require handler records with callback fields; those
records have no constructor macros or setters, and real handlers need
definitions outside `main()`. Those dispatch and registration calls remain
API ergonomics gaps.

```c
#include "c23/event_invoke.h"
#include "ui/element.h"

int main(void)
{
    Element *root = Element();
    Element_clearEvents(root);
    int bindingCount = Element_eventBindingCount();
    Element_destroy(root);
    return 0;
}
```

## Frame class (revalidate.c)

`Frame_revalidate(...)` is the public arity macro for the frame-wide
revalidation operation.

```c
#include "c23/overload.h"
#include "frame/frame.h"

int main(void)
{
    Frame *frame = Frame("window-title-goes-here", 640, 480);
    Frame_revalidate(frame);
    Frame_destroy(frame);
    return 0;
}
```

## Panel and Frame classes (remove.c)

`Panel_remove(...)` returns the detached child; the caller then owns and
destroys it. `Frame_removePanels(...)` destroys every panel owned by the frame.

```c
#include "c23/overload.h"
#include "frame/frame.h"
#include "panel/panel.h"

int main(void)
{
    Frame *frame = Frame("window-title-goes-here", 640, 480);
    Panel *parent = Panel();
    Panel *child = Panel();
    Panel_add(parent, child);
    Panel *detachedChild = Panel_remove(child);
    Panel_destroy(detachedChild);
    Panel_destroy(parent);
    Frame_removePanels(frame);
    Frame_destroy(frame);
    return 0;
}
```

## Panel and Frame classes (set_size.c)

Both operations use their public arity macros. Frame dimensions are native
pixels.

```c
#include "c23/overload.h"
#include "frame/frame.h"
#include "panel/panel.h"

int main(void)
{
    Panel *panel = Panel();
    Panel_setSize(panel, 320.0f, 240.0f);
    Panel_destroy(panel);
    Frame *frame = Frame("window-title-goes-here", 640, 480);
    Frame_setSize(frame, 800, 600);
    Frame_destroy(frame);
    return 0;
}
```

## Panel class (set_location.c)

`Panel_setLocation(...)` supports offset-only, offset plus parent anchor, and
offset plus anchor and pivot forms.

```c
#include "c23/overload.h"
#include "panel/panel.h"

int main(void)
{
    Panel *panel = Panel(120.0f, 80.0f);
    Panel_setLocation(panel, 24.0f, 32.0f);
    Panel_setLocation(panel, 24.0f, 32.0f, PART_CENTER);
    Panel_setLocation(panel, 24.0f, 32.0f, PART_CENTER, PART_CENTER);
    Panel_destroy(panel);
    return 0;
}
```

## Panel and Frame classes (add.c)

`Panel_add(...)` and `Frame_add(...)` select their public arities. `Frame_addPanel`
currently requires an `ElementDesc` caller record, which has no constructor or
setter API, so it remains an explicit API ergonomics gap and is not fabricated
here.

```c
#include "c23/overload.h"
#include "frame/frame.h"
#include "panel/panel.h"

int main(void)
{
    Panel *parent = Panel();
    Panel *firstChild = Panel();
    Panel *secondChild = Panel();
    Panel_add(parent, firstChild);
    Panel_add(parent, secondChild, 0);
    Panel_destroy(parent);
    Frame *frame = Frame("window-title-goes-here", 640, 480);
    Panel *firstFramePanel = Panel();
    Panel *secondFramePanel = Panel();
    Frame_add(frame, firstFramePanel);
    Frame_add(frame, secondFramePanel, 0);
    Frame_destroy(frame);
    return 0;
}
```

## Element and class cursor operations (set_cursor.c)

Cursor preferences are set on an Element, Panel, ScrollPanel, or Frame. The
resolved cursor is returned as a `CursorType` value.

```c
#include "c23/overload.h"
#include "frame/frame.h"
#include "panel/panel.h"
#include "panel/scroll_panel.h"

int main(void)
{
    Element *element = Element();
    Element *cursorElement = Element_setCursor(element, CURSOR_TEXT);
    CursorType elementCursor = Element_cursorAt(element, 0.0f, 0.0f);
    Panel *panel = Panel();
    Panel *cursorPanel = Panel_setCursor(panel, CURSOR_POINTER);
    ScrollPanel *scrollPanel = ScrollPanel(240.0f, 160.0f);
    ScrollPanel *cursorScrollPanel = ScrollPanel_setCursor(scrollPanel, CURSOR_CROSSHAIR);
    Frame *frame = Frame("window-title-goes-here", 640, 480);
    Frame_setCursor(frame, CURSOR_RESIZE_EW);
    Frame_destroy(frame);
    ScrollPanel_destroy(scrollPanel);
    Panel_destroy(panel);
    Element_destroy(element);
    return 0;
}
```

## Panel class (panel.c)

The `Panel(...)` macro covers the zero-argument and width/height constructors.
The descriptor constructor needs an `ElementDesc`, which currently has no
constructor or setter API; that form is an ergonomics gap. The ownership helpers
declared only in `panel_internal.h` are internal seams, not public calls.
`Panel_addMouseEvent`, `Panel_addScrollEvent`, `Panel_addZoomEvent`,
`Panel_addKeyEvent`, `Panel_addTouchEvent`, and `Panel_addDocumentEvent` need
handler records with callback fields; those records have no constructor macros
or setters, and real handlers need definitions outside `main()`. Those
registration calls remain API ergonomics gaps.

```c
#include "c23/overload.h"
#include "panel/panel.h"

int main(void)
{
    Panel *parent = Panel();
    Panel *panel = Panel(120.0f, 80.0f);
    Panel_add(parent, panel);
    Panel_setOffset(panel, 12.0f, 18.0f);
    Panel_setAnchor(panel, PART_CENTER);
    Panel_setPivot(panel, PART_CENTER);
    Panel_setTag(panel, "panel-tag-goes-here");
    Panel_setRadius(panel, 8.0f);
    Panel_setBackground(panel, COLOR_RGBA(40, 80, 120, 255));
    Panel_setBorder(panel, COLOR_RGBA(255, 255, 255, 255), 1.0f);
    Panel_setShadow(panel, 0.0f, 2.0f, 4.0f);
    Panel_setShadowColor(panel, COLOR_RGBA(0, 0, 0, 128));
    Panel_setVisible(panel, true);
    Element *graphics = Panel_graphics(panel);
    int childCount = Panel_childCount(parent);
    Element *childElement = Panel_childElement(parent, 0);
    Panel *owner = Panel_parent(panel);
    float width = Panel_width(panel);
    float height = Panel_height(panel);
    float radius = Panel_radius(panel);
    int anchor = Panel_anchor(panel);
    int pivot = Panel_pivot(panel);
    const char *tag = Panel_tag(panel);
    bool visible = Panel_isVisible(panel);
    Panel_destroy(parent);
    return 0;
}
```

## Pointer module (pointer.c)

The module has no object constructor. `Pointer_addButton` currently requires
an `ElementDesc` with no constructor or setter API, so it is documented as a
gap. `Pointer_onClick` needs a real callback definition, which the one-main
cookbook format does not provide; it remains an API ergonomics gap.

```c
#include "c23/overload.h"
#include "frame/frame.h"
#include "input/pointer.h"
#include "panel/panel.h"

int main(void)
{
    Frame *frame = Frame("window-title-goes-here", 640, 480);
    Panel *panel = Panel(120.0f, 80.0f);
    Frame_add(frame, panel);
    Element *root = Frame_element(frame);
    Panel *hoveredPanel = Pointer_hover(root, 24.0f, 32.0f);
    Pointer_move(root, 24.0f, 32.0f);
    Pointer_press(root, 24.0f, 32.0f);
    Pointer_release(root, 24.0f, 32.0f);
    Pointer_click(root, 24.0f, 32.0f);
    Pointer_hold(root, 24.0f, 32.0f, 0.0);
    Pointer_drag(root, 24.0f, 32.0f, 48.0f, 64.0f, 0.0);
    Pointer_track(frame);
    Frame_destroy(frame);
    return 0;
}
```

## Panel class (set_corner_radius.c)

`Panel_setCornerRadius(...)` is the public macro for this file’s radius
setter. It returns the panel pointer after applying the radius.

```c
#include "c23/overload.h"
#include "panel/panel.h"

int main(void)
{
    Panel *panel = Panel();
    Panel_setCornerRadius(panel, 12.0f);
    Panel_destroy(panel);
    return 0;
}
```

## Panel class (set_maximum_size.c)

`Panel_setMaximumSize(...)` is the public macro for this file’s maximum-size
setter. Non-positive extents clear that axis’s maximum.

```c
#include "c23/overload.h"
#include "panel/panel.h"

int main(void)
{
    Panel *panel = Panel();
    Panel_setMaximumSize(panel, 1280.0f, 720.0f);
    Panel_destroy(panel);
    return 0;
}
```

## Panel class (set_minimum_size.c)

`Panel_setMinimumSize(...)` is the public macro for this file’s minimum-size
setter. Non-positive extents clear that axis’s minimum.

```c
#include "c23/overload.h"
#include "panel/panel.h"

int main(void)
{
    Panel *panel = Panel();
    Panel_setMinimumSize(panel, 80.0f, 24.0f);
    Panel_destroy(panel);
    return 0;
}
```

## Frame class (frame.c)

The `Frame(...)` macro provides the zero-argument, title-only, and
title-plus-size constructors. `Frame_macOS_getLiquidGlass` still requires a
caller-provided output record, so it is a Value Return Law blocker and is
omitted. `Frame_paint` uses a `DisplayList` constructor and returned root
bounds. `Frame_onClose(frame, nullptr, nullptr)` is shown with a null callback;
a non-null callback requires a helper function, which this one-main example
format excludes. `Frame_runAll` and `Frame_run` are blocking alternatives and
remain application-loop call gaps in this call-only example.

```c
#include "c23/overload.h"
#include "frame/frame.h"

int main(void)
{
    Frame *frame = Frame("window-title-goes-here", 640, 480);
    Frame *defaultFrame = Frame();
    Frame *titledFrame = Frame("another-window-title-goes-here");
    Frame_setTitle(frame, "updated-window-title-goes-here");
    Frame_onClose(frame, nullptr, nullptr);
    Frame_setBackground(frame, COLOR_RGBA(24, 32, 48, 255));
    Frame_setBackgroundColor(frame, COLOR_RGBA(32, 40, 56, 255));
    Color background = Frame_background(frame);
    Frame_setTransparent(frame, false);
    Frame_setBlur(frame, 0.0f);
    bool liquidGlassAvailable = Frame_macOS_hasLiquidGlass();
    Frame_macOS_setLiquidGlass(frame, nullptr);
    Window *window = Frame_window(frame);
    Surface *surface = Frame_surface(frame);
    Board *contentBoard = Frame_contentBoard(frame);
    Element *root = Frame_element(frame);
    Rect rootBounds = Frame_root(frame);
    Panel *panel = Panel();
    Frame_add(frame, panel);
    int panelCount = Frame_count(frame);
    Panel *attachedPanel = Frame_panel(frame, 0);
    Frame_setOwner(titledFrame, frame);
    Frame *owner = Frame_owner(titledFrame);
    Frame_show(frame);
    Frame_hide(frame);
    bool isClosed = Frame_isClosed(frame);
    Frame_setFPSCap(frame, 60);
    Frame_setFPSCapWhenFocusGain(frame, 120);
    Frame_setFPSCapWhenFocusLost(frame, 1);
    int fpsCap = Frame_getFPSCap(frame);
    int focusGainCap = Frame_getFPSCapWhenFocusGain(frame);
    int focusLostCap = Frame_getFPSCapWhenFocusLost(frame);
    int effectiveFpsCap = Frame_getEffectiveFPSCap(frame);
    DisplayList *displayList = DisplayList();
    Frame_paint(frame, displayList);
    DisplayList_free(displayList);
    Frame_render(frame);
    Frame_invalidate(frame);
    Frame_invalidateElement(root);
    Frame *activeFrame = Frame_active();
    Image *capture = Frame_capture(frame);
    bool saved = Frame_savePNG(frame, "frame-capture-path-goes-here.png");
    Frame_close(Frame("frame-to-close"));
    Application *application = Application("application-name-goes-here");
    Frame *applicationFrame = Frame("application-window-title-goes-here");
    bool attached = Frame_attachApplication(applicationFrame, application);
    Application *attachedApplication = Frame_application(applicationFrame);
    Frame_destroyApplicationFrames(application);
    Application_free(application);
    Frame_destroy(defaultFrame);
    Frame_destroy(frame);
    return 0;
}
```

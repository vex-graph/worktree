# graphvex — Public API Calls

Per-file call reference. These snippets expose call spellings only; they
do not claim rendered pixels, a window, or swapchain integration.

## Board class (board.c)

`Board_new` accepts a `BoardDesc *`, but `BoardDesc` has no preferred
constructor macro or setters. It remains a constructor ergonomics gap; the
example uses the public `Board(...)` constructor forms instead.

```c
#include "board.h"

int main(void)
{
    Board *board = Board(640u, 360u);
    Board *defaultBoard = Board();
    bool resized = Board_resize(board, 800u, 600u);
    Board_publish(board);
    Board_fill(board, COLOR_BLACK);
    uint32_t width = Board_width(board);
    uint32_t height = Board_height(board);
    uint64_t generation = Board_generation(board);
    bool valid = Board_isValid(board);
    Image *image = Board_image(board);
    void *native = Board_native(board);
    Board_clearRevalidators(board);
    Board_revalidate(board);






    Board_destroy(defaultBoard);
    Board_destroy(board);
    return 0;
}
```

`Board_addRevalidator` requires a real callback; defining one would add a helper
function outside the single-main cookbook format, so its callback path remains
an example gap.

## Viewport class (viewport.c)

```c
#include "graphics/viewport.h"

int main(void)
{
    Viewport viewport = Viewport();
    Viewport_resize(&viewport, 1600.0f, 900.0f, 2.0f);
    float x = Viewport_x(&viewport, 20.0f);
    float y = Viewport_y(&viewport, 30.0f);
    float width = Viewport_w(&viewport, 100.0f);
    float height = Viewport_h(&viewport, 50.0f);
    Rect rect = Viewport_rect(&viewport, 20.0f, 30.0f, 100.0f, 50.0f);
    ViewportPoint point = Viewport_toPoints(&viewport, 40.0f, 60.0f);
    ViewportSize logicalSize = Viewport_logicalSize(&viewport);
    bool empty = Viewport_isEmpty(&viewport);








    return 0;
}
```

## Image class (image.c)

`Image_new` accepts an `ImageDesc *`, but `ImageDesc` has no preferred
constructor macro or setters; that factory form remains a constructor gap.

```c
#include "image.h"

int main(void)
{
    Image *image = Image(1u, 1u, IMAGE_FORMAT_RGBA8, IMAGE_USAGE_SAMPLED);
    bool resized = Image_resize(image, 2u, 2u);
    bool shadowReady = Image_ensureShadow(image, 2u, 2u);
    Image_fill(image, COLOR_BLACK);
    uint32_t width = Image_width(image);
    uint32_t height = Image_height(image);
    uint32_t format = Image_format(image);
    uint32_t usage = Image_usage(image);
    size_t stride = Image_stride(image);
    uint8_t *pixels = Image_pixels(image);
    bool valid = Image_isValid(image);
    void *native = Image_native(image);
    void *ioSurface = Image_iosurface(image);
    Image_setNative(image, nullptr);
    Image_setIOSurface(image, nullptr);
    uint32_t layer = Image_layer(image);
    Image_setLayer(image, 0u);
    bool gpuCleared = Image_clearGpu(image);
    void *gpuResource = Image_gpuResource(image);
    void *gpuDevice = Image_gpuDevice(image);
    void *gpuDescriptor = Image_gpuDescriptor(image);
    bool drawable = Image_isDrawable(image);














    Image_destroy(image);
    return 0;
}
```

`Image_upload(rgba, width, height, image)` writes through a dest-last image
argument, so it is omitted as a Value Return Law migration gap.
`Image_bindGpu` needs valid GPU handles and paired retain/release callbacks;
that callback-backed binding call is also omitted from this one-main example.

## Property class (property.c)

`Property` has no preferred `Property(...)` constructor macro; its only
constructor-like function is `Property_default()`. The example obtains a live
property from `Element_property` and demonstrates the available setters and
value getters without using that legacy constructor call.

```c
#include "ui/property.h"
#include "ui/element.h"

int main(void)
{
    Element *element = Element();
    Property *property = Element_property(element);
    Property_setMinSize(property, 24.0f, 16.0f);
    Property_setMaxSize(property, 320.0f, 240.0f);
    float effectiveWidth = Property_width(property);
    float effectiveHeight = Property_height(property);

    Element_destroy(element);

    return 0;
}
```

## Element class (element.c)

```c
#include "ui/element.h"
#include "image.h"
#include "graphics/viewport.h"

int main(void)
{
    Element *root = Element();
    Element *child = Element();
    Element *insertedChild = Element();
    Image *image = Image(1u, 1u, IMAGE_FORMAT_RGBA8, IMAGE_USAGE_SAMPLED);
    Viewport viewport = Viewport();
    Viewport_resize(&viewport, 640.0f, 360.0f, 1.0f);
    Rect parentBounds = Viewport_rect(&viewport, 0.0f, 0.0f, 640.0f, 360.0f);

    Property *sharedProperty = Element_property(root);
    child = Element_setProperty(child, sharedProperty);
    child = Element_ownProperty(child);
    root = Element_setSize(root, 640.0f, 360.0f);
    root = Element_setMinimumSize(root, 80.0f, 60.0f);
    root = Element_setMaximumSize(root, 1280.0f, 720.0f);
    root = Element_setOffset(root, 12.0f, 18.0f);
    root = Element_setAnchor(root, PART_TOP_LEFT);
    root = Element_setPivot(root, PART_TOP_LEFT);
    root = Element_setTag(root, "root-element");
    root = Element_setRadius(root, 12.0f);
    root = Element_setBackground(root, COLOR_RGBA(24u, 32u, 48u, 255u));
    root = Element_setBorder(root, COLOR_RGBA(96u, 112u, 128u, 255u), 2.0f);
    root = Element_setShadow(root, 0.0f, 4.0f, 8.0f);
    root = Element_setShadowColor(root, COLOR_RGBA(0u, 0u, 0u, 96u));
    root = Element_setBlur(root, 1.0f);
    root = Element_setClip(root, true);
    root = Element_setPressed(root, false);
    root = Element_setVisible(root, true);
    root = Element_setImage(root, image);
    root = Element_setCursorPreference(root, 3);

    Point center = Part_point(parentBounds, PART_CENTER);
    Rect eventBound = Element_eventBound(root, parentBounds);
    Rect absoluteBound = Element_absoluteBound(root, parentBounds);
    Rect resolved = Element_resolve(root, parentBounds);
    Rect bounds = Element_bounds(root, parentBounds);
    DisplayList *displayList = DisplayList();
    Element_paint(root, eventBound, displayList);
    DisplayList_free(displayList);

    child = Element_add(root, child);
    insertedChild = Element_addAt(root, insertedChild, 0);
    bool firstRemovalSucceeded = Element_remove(insertedChild);
    insertedChild = Element_addAt(root, insertedChild, 0);
    Element_markDirty(root);
    Element_revalidate(root);

    Property *bound = Element_property(child);
    bool dirty = Element_isDirty(root);
    int childCount = Element_count(root);
    Element *firstChild = Element_child(root, 0);
    Element *parent = Element_parent(child);
    Element *treeRoot = Element_root(child);
    Element *tagged = Element_find(root, "root-element");
    Element *hit = Element_hit(root, 20.0f, 24.0f);
    const Image *borrowedImage = Element_image(root);
    float width = Element_width(root);
    float height = Element_height(root);
    float radius = Element_radius(root);
    int anchor = Element_anchor(root);
    int pivot = Element_pivot(root);
    bool valid = Element_isValid(root);
    bool visible = Element_isVisible(root);
    bool pressed = Element_isPressed(root);
    const char *tag = Element_tag(root);
    int cursor = Element_cursorPreference(root);























    bool secondRemovalSucceeded = Element_remove(insertedChild);
    Element_destroy(root);
    Element_destroy(insertedChild);
    Image_destroy(image);
    return 0;
}
```

The `Element(desc)` constructor overload takes an `ElementDesc`, but that
descriptor has no setters; this example uses `Element()` and the available
element setters. The Rect-based calls use `Viewport_rect` to obtain a value
without aggregate initialization.

## Graphics class (graphics.c)

```c
#include "graphics/graphics.h"
#include "graphics/viewport.h"
#include "image.h"

int main(void)
{
    const Backend *rasterBackend = RasterGraphics_row();
    bool backendRegistered = Graphics_register(rasterBackend);
    bool backendSelected = Graphics_use(BACKEND_RASTER);
    bool rasterConfigured = Raster_configure(640u, 360u);

    Viewport viewport = Viewport();
    Viewport_resize(&viewport, 640.0f, 360.0f, 1.0f);
    Rect source = Viewport_rect(&viewport, 0.0f, 0.0f, 1.0f, 1.0f);
    Rect destination = Viewport_rect(&viewport, 16.0f, 24.0f, 240.0f, 120.0f);
    bool sourceEmpty = Rect_isEmpty(source);
    bool destinationContainsOrigin = Rect_contains(destination, 0.0f, 0.0f);
    Rect overlap = Rect_intersect(source, destination);
    Color sampleColor = COLOR_RGBA(24u, 48u, 96u, 255u);
    uint8_t red = Color_red(sampleColor);
    uint8_t green = Color_green(sampleColor);
    uint8_t blue = Color_blue(sampleColor);
    uint8_t alpha = Color_alpha(sampleColor);
    Image *image = Image(1u, 1u, IMAGE_FORMAT_RGBA8, IMAGE_USAGE_SAMPLED);
    DisplayList *displayList = DisplayList();

    bool began = Graphics_begin();
    bool cleared = Graphics_clear(COLOR_BLACK);
    bool clipped = Graphics_clip(&destination);
    bool roundedClipSet = Graphics_clipRounded(&destination, 8.0f);
    bool clipCleared = Graphics_clip(nullptr);
    bool imageDrawn = Graphics_drawImage(image, &destination);
    DisplayList_image(displayList, image, source, destination);
    DisplayList_text(displayList, destination, "label-text-goes-here", COLOR_WHITE);
    DisplayList_clip(displayList, destination);
    DisplayList_clipRounded(displayList, destination, 8.0f);
    DisplayList_unclip(displayList);
    bool submitted = Graphics_submit(displayList);
    bool ended = Graphics_end();
    bool presented = Graphics_present();
    bool resized = Graphics_resize(640u, 360u);

    uint32_t backendId = Graphics_backendId();
    const Backend *activeBackend = Graphics_current();
    const uint32_t *pixels = Raster_pixels();
    uint32_t pixel = Raster_pixelAt(0u, 0u);
    size_t commandCount = DisplayList_count(displayList);
    const DrawCmd *commands = DisplayList_cmds(displayList);






    DisplayList_clear(displayList);
    DisplayList_free(displayList);
    Image_destroy(image);
    return 0;
}
```

`Graphics_capture` writes into a caller-provided Image and is a Value Return Law
gap. `Graphics_fillRect`, `Graphics_drawText`, and `DisplayList_rect` require a
`Brush`, but Graphvex currently has no Brush constructor or setters; those calls
are omitted until the value can be built without aggregate field initialization.

## Filter token functions (filter_functions.h)

The lower-case `filterScalar` and `filterReference` helpers are private
encoders. These public `Filter_*` functions construct and inspect compact
filter tokens; token encoding does not allocate or execute a filter.

```c
#include "filter/filter_functions.h"

int main(void)
{
    FilterToken identity = Filter_identity();
    uint16_t identityId = Filter_id(identity);
    uint64_t identityPayload = Filter_payload(identity);
    FilterToken gain = Filter_gain(1.25f);
    FilterToken scatterBlur = Filter_scatterBlur(4u);
    FilterToken brightness = Filter_brightness(0.15f);
    FilterToken contrast = Filter_contrast(1.2f);
    FilterToken blackAndWhite = Filter_blackAndWhite(0.5f);
    FilterToken monocolor = Filter_monocolor(0x336699FFu);
    FilterToken grayscale = Filter_grayscale();
    FilterToken grayscaleRed = Filter_grayscaleRed();
    FilterToken grayscaleGreen = Filter_grayscaleGreen();
    FilterToken grayscaleBlue = Filter_grayscaleBlue();
    FilterToken invert = Filter_invert();
    FilterToken toneCurve = Filter_toneCurve(1u, 1u);
    FilterToken hsl = Filter_hsl(1u, 1u);
    FilterToken hsv = Filter_hsv(1u, 1u);
    FilterToken colorBalance = Filter_colorBalance(1u, 1u);
    FilterToken edges = Filter_edges(1u, 1u);
    FilterToken dropShadow = Filter_dropShadow(1u, 1u);
    FilterToken gradientMap = Filter_gradientMap(1u, 1u);
    FilterToken replaceColor = Filter_replaceColor(1u, 1u);
    FilterToken gaussianBlur = Filter_gaussianBlur(1u, 1u);
    FilterToken boxBlur = Filter_boxBlur(1u, 1u);
    FilterToken zoomingBlur = Filter_zoomingBlur(1u, 1u);
    FilterToken movingBlur = Filter_movingBlur(1u, 1u);
    FilterToken spinBlur = Filter_spinBlur(1u, 1u);
    FilterToken lensBlur = Filter_lensBlur(1u, 1u);
    FilterToken mosaic = Filter_mosaic(1u, 1u);
    FilterToken unsharpMask = Filter_unsharpMask(1u, 1u);
    FilterToken frostedGlass = Filter_frostedGlass(1u, 1u);
    FilterToken stroke = Filter_stroke(1u, 1u);
    FilterToken stainedGlass = Filter_stainedGlass(1u, 1u);
    FilterToken outerGlow = Filter_outerGlow(1u, 1u);
    FilterToken innerGlow = Filter_innerGlow(1u, 1u);
    FilterToken emboss = Filter_emboss(1u, 1u);
    FilterToken relief = Filter_relief(1u, 1u);
    FilterToken waterdrop = Filter_waterdrop(1u, 1u);
    FilterToken extrude = Filter_extrude(1u, 1u);
    FilterToken godRays = Filter_godRays(1u, 1u);
    FilterToken chromaticAberration = Filter_chromaticAberration(1u, 1u);
    FilterToken glitch = Filter_glitch(1u, 1u);
    FilterToken noise = Filter_noise(1u, 1u);
    FilterToken dithering = Filter_dithering(1u, 1u);
    FilterToken chrome = Filter_chrome(1u, 1u);
    FilterToken bloom = Filter_bloom(1u, 1u);
    FilterToken sheer = Filter_sheer(1u, 1u);
    FilterToken pixelate = Filter_pixelate(1u, 1u);
    FilterToken pointillize = Filter_pointillize(1u, 1u);
    FilterToken expansion = Filter_expansion(1u, 1u);
    FilterToken fisheye = Filter_fisheye(1u, 1u);
    FilterToken sphere = Filter_sphere(1u, 1u);
    FilterToken wave = Filter_wave(1u, 1u);
    FilterToken dots = Filter_dots(1u, 1u);

    return 0;
}
```

## ColorPass class (color_pass.c)

```c
#include "compositor/color_pass.h"

int main(void)
{
    ColorPass *pass = ColorPass();
    FilterToken grayscaleToken = Filter_grayscale();
    bool tokenValid = ColorPass_validateToken(grayscaleToken);
    void *descriptorLayout = ColorPass_getDescriptorLayout(pass);

    ColorPass_destroy(pass);
    return 0;
}
```

The zero-argument constructor produces a null identity. Creating a usable
pipeline requires a live Vulkan Device, render pass, and SPIR-V inputs, so that
constructor form and `ColorPass_record` remain runtime-resource gaps.
`ColorPass_toString` and `ColorPass_toStringStruct` require caller-provided
buffers and remain Value Return Law gaps.

## CompositorSurface class (compositor.c)

```c
#include "compositor/compositor.h"

int main(void)
{
    CompositorSurface *empty = CompositorSurface_zero();
    CompositorBounds bounds = CompositorSurface_bounds(empty);
    CompositorSurface *surface = CompositorSurface(bounds);
    float *pixels = CompositorSurface_pixels(surface);
    const float *readOnlyPixels = CompositorSurface_constPixels(surface);
    CompositorStatus validationStatus = CompositorSurface_validate(surface);


    CompositorSurface_destroy(surface);
    CompositorSurface_destroy(empty);
    return 0;
}
```

`CompositorSurface_create`, `Compositor_filterBounds`, and
`Compositor_compose` write results through caller-provided output parameters;
`Compositor_sourceOver` takes its mutated destination surface separately.
Those operations are Value Return Law migration gaps.
`CompositorSurface_toString` and `CompositorSurface_toStringStruct` also
require caller buffers and are omitted.

## CompositorImage class (compositor_image.c)

```c
int main(void)
{
    return 0;
}
```

Both `CompositorSurface_fromImage` and `CompositorSurface_toImage` return
status while writing the produced object through an output pointer. They remain
Value Return Law gaps until the APIs return their owned result directly.

## CompositorScope class (compositor_scope.c)

```c
int main(void)
{
    return 0;
}
```

`Compositor_crop` and `Compositor_scopedScene` write their owned results through
output pointers, and the scene call also requires a `CompositorScopeDesc` with
no public setters. These APIs remain example gaps.

## CompositorSubmit class (compositor_submit.c)

```c
int main(void)
{
    return 0;
}
```

`Compositor_record` writes its newly created Image through `Image **outImage`;
it remains a Value Return Law gap.

## FilterPool class (filter_pool.c)

The destination-based constructor and recipe methods remain gaps. Null-safe
value/status operations can still be called directly to show their call shape.

```c
#include "compositor/filter_pool.h"

int main(void)
{
    FilterPoolStatus destroyStatus = FilterPool_destroy(nullptr);
    FilterPoolStatus retainStatus = FilterPool_retain(nullptr, 0u);
    FilterPoolStatus releaseStatus = FilterPool_release(nullptr, 0u);
    uint32_t capacity = FilterPool_capacity(nullptr);
    uint32_t maxRecipeFilters = FilterPool_maxRecipeFilters(nullptr);
    uint32_t live = FilterPool_live(nullptr);
    return 0;
}
```

`FilterPool(config, out)` dispatches to a constructor that writes through an
output pointer, and `FilterPool_insert`, `FilterPool_snapshot`, and
`FilterPool_compose` also use caller destinations. There is no destination-free
constructor or result-returning form yet. `FilterPool_toString` and
`FilterPool_toStringStruct` require caller buffers.

## GpuScope class (gpu_scope.c)

```c
#include "compositor/gpu_scope.h"

int main(void)
{
    GpuScope *scope = GpuScope_zero();
    bool pending = GpuScope_isPending(scope);

    bool destroyed = GpuScope_destroy(scope);
    return 0;
}
```

The zero-argument constructor is a null identity. A usable `GpuScope` needs a
live Device, but Graphvex exposes no Device constructor macro; that construction
path is a gap. `GpuScope_render` and `GpuScope_renderSampled` use output Images,
and `GpuScope_toString` / `GpuScope_toStringStruct` use caller buffers, so they
remain Value Return Law gaps.

## RenderLoop class (render_loop.c)

```c
#include "graphics/render_loop.h"

int main(void)
{
    int windowIdentity = 0;
    void *window = &windowIdentity;
    RenderLoop *loop = RenderLoop();
    RenderLoop *defaultLoop = RenderLoop_default();

    RenderLoop_markDirty(loop, window);
    RenderLoop_setContentGen(loop, window, 7u);
    RenderLoop_notify(loop);
    RenderLoop_notify(defaultLoop);
    bool stepped = RenderLoop_step(loop);
    Client *client = RenderLoop_findClient(loop, window);
    bool removed = RenderLoop_removeClient(loop, window);


    RenderLoop_free(loop);
    return 0;
}
```

`RenderLoop_addClient` needs a `Client` value containing callback functions;
there are no Client setters, and defining callbacks would add non-main helper
functions. That call remains an example gap. The one-argument constructor
`RenderLoop_fps` is declared, but `RenderLoop(...)` dispatches its one-argument
form to the absent `RenderLoop_1`; that constructor macro form is also a gap.

## Pool class (pool.c)

```c
#include "nio/pool.h"

int main(void)
{
    Pool *emptyPool = nullptr;
    Pool_destroy(emptyPool);
    void *emptyItem = Pool_alloc(emptyPool);
    Pool_release(emptyPool, emptyItem);
    bool belongsToPool = Pool_contains(emptyPool, emptyItem);
    uint32_t live = Pool_live(emptyPool);
    size_t stride = Pool_stride(emptyPool);
    return 0;
}
```

`Pool` has no constructor macro or setters; its only constructor is
`Pool_new(stride, blockCap)`. Per the constructor preference, that factory call
is not shown. The null-safe operations are shown on the null identity; a usable
pool remains blocked on a constructor macro.

## PropertyPool class (property_pool.c)

```c
#include "nio/property_pool.h"

int main(void)
{
    PropertyPool *pool = PropertyPool();
    Property *property = PropertyPool_alloc(pool, nullptr);
    uint32_t live = PropertyPool_live(pool);
    PropertyPool_release(pool, property);
    PropertyPool_destroy(pool);

    PropertyPool *defaultPool = PropertyPool_default();
    uint32_t defaultLive = PropertyPool_live(defaultPool);


    return 0;
}
```

`PropertyPool_default()` returns a borrowed process-wide pool; this example
does not destroy it. `PropertyPool_alloc`'s input points to initial property
state, not to a caller-provided result destination.

## ImageRuns class (image_runs.c)

```c
int main(void)
{
    return 0;
}
```

`ImageRuns_visit` requires an `ImageRunsFn` callback for a useful call. A valid
callback needs a separate function definition, which the per-file cookbook
format intentionally excludes; passing `nullptr` would only demonstrate the
rejection path, so the call remains a documented example gap.

## Device class (device.c)

```c
#include "vulkan/device.h"

int main(void)
{
    bool valid = Device_isValid(nullptr);
    const char *lastError = Device_lastError(nullptr);
    const char *name = Device_name(nullptr);
    void *native = Device_native(nullptr);
    void *instance = Device_instance(nullptr);
    void *physical = Device_physical(nullptr);
    void *queue = Device_queue(nullptr);
    uint32_t queueFamily = Device_queueFamily(nullptr);
    bool hasMetalObjects = Device_hasMetalObjects(nullptr);









    Device_destroy(nullptr);
    return 0;
}
```

`Device_create` is the only constructor, and there is no `Device(...)` macro;
usable Device creation remains a constructor gap.

## Pipeline class (pipeline.c)

```c
#include "vulkan/pipeline.h"

int main(void)
{
    Pipeline *pipeline = nullptr;
    bool valid = Pipeline_isValid(pipeline);
    uint32_t vertexStride = Pipeline_vertexStride(pipeline);
    void *native = Pipeline_native(pipeline);



    Pipeline_destroy(pipeline);
    return 0;
}
```

`Pipeline_new` and `Pipeline_fromFiles` are function constructors, and
`PipelineDesc` has no setters or constructor macro. The usable Pipeline API
remains a constructor gap.

## SampledImage class (sampled_image.c)

```c
#include "vulkan/sampled_image.h"

int main(void)
{
    SampledImage *sampledImage = SampledImage();
    bool ready = SampledImage_isReady(sampledImage);
    uint32_t width = SampledImage_width(sampledImage);
    uint32_t height = SampledImage_height(sampledImage);
    Device *device = SampledImage_device(sampledImage);
    void *descriptor = SampledImage_descriptor(sampledImage);
    bool polled = SampledImage_poll(sampledImage);
    bool retained = SampledImage_retain(sampledImage);
    bool bound = SampledImage_bindImage(sampledImage, nullptr);
    bool released = SampledImage_release(sampledImage);

    return 0;
}
```

The zero-argument constructor is a null identity, so lifecycle calls are shown
on that null instance to demonstrate their signatures. A usable sampled image
needs a live Device, for which no constructor macro exists. The useful image
binding path is therefore a constructor gap. `SampledImage_toString` and
`SampledImage_toStringStruct` remain output-buffer gaps.

## Surface class (surface.c)

`Surface_onPresent` and `Surface_setClock` require callback definitions that
the one-main-only example format does not provide. `Surface_present` has no
host callback until that seam is installed, so these APIs remain a cookbook
ergonomics gap.

```c
#include "vulkan/surface.h"

int main(void)
{
    Surface *surface = Surface();
    Board *board = Board();
    bool resized = Surface_resize(surface, 640u, 360u);
    Surface_setFPSCap(surface, 30);
    Surface_addBoard(surface, board);
    Surface_revalidateNow(surface);
    Surface_revalidate(surface);
    Surface_poll(surface);
    Surface_removeBoard(surface, board);

    uint32_t width = Surface_width(surface);
    uint32_t height = Surface_height(surface);
    bool valid = Surface_isValid(surface);
    void *handle = Surface_handle(surface);
    Image *presentImage = Surface_presentImage(surface);
    int fpsCap = Surface_getFPSCap(surface);
    uint64_t presentCount = Surface_getPresentCount(surface);







    Surface_destroy(surface);
    Board_destroy(board);
    return 0;
}
```

`Surface_present` requires a host callback, and `Surface_onPresent` and
`Surface_setClock` require callback definitions. Those call paths remain gaps
because the per-file cookbook format excludes helper functions.

## VkBatch class (vk_batch.c)

```c
#include "vulkan/vk_batch.h"
#include "graphics/viewport.h"

int main(void)
{
    VkBatch *batch = VkBatch();
    Viewport viewport = Viewport();
    Viewport_resize(&viewport, 640.0f, 360.0f, 1.0f);
    Rect clip = Viewport_rect(&viewport, 0.0f, 0.0f, 640.0f, 360.0f);
    Rect source = Viewport_rect(&viewport, 0.0f, 0.0f, 1.0f, 1.0f);
    Rect destination = Viewport_rect(&viewport, 12.0f, 18.0f, 120.0f, 80.0f);
    Image *image = Image(1u, 1u, IMAGE_FORMAT_RGBA8, IMAGE_USAGE_SAMPLED);
    VkBatch_setClip(batch, clip);
    VkBatch_setClipRadius(batch, 8.0f);
    VkBatch_image(batch, image, source, destination);
    VkBatch_glyph(batch, destination, 2u, COLOR_WHITE);
    VkBatch_clear(batch);
    Image_destroy(image);
    VkBatch_free(batch);
    return 0;
}
```

`VkBatch_rect` needs a `Brush`, but Graphvex exposes no Brush constructor or
setters. `VkBatch_vertices` writes into caller-provided vertex storage and
remains a Value Return Law gap.

## VulkanBackend class (vk_renderer.c)

```c
#include "vulkan/vulkan_backend.h"

int main(void)
{
    const Backend *backend = VulkanBackend_row();
    const VkBatch *batch = VulkanBackend_batch();
    const char *lastError = VulkanBackend_lastError();
    Device *device = VulkanBackend_device();
    size_t vertexBytes = VulkanBackend_vertexBytes();





    VulkanBackend_unbindSurface();
    VulkanBackend_cleanupSurfaces();
    bool surfaceSelected = VulkanBackend_useSurface(-1);
    VulkanBackend_removeSurface(-1);
    VulkanBackend_unbind();
    return 0;
}
```

Binding a native host surface or IOSurface needs live platform/GPU handles;
`VulkanBackend_bind`, `VulkanBackend_bindSurface`, `VulkanBackend_addSurface`,
and `VulkanBackend_prepareImage` remain runtime-resource gaps.

# Determinant — public call reference

Each titled section models one implementation file. Constructor arms such as
`Class_0()`/`Class_1(...)` are implementation details; examples use the class
constructor macro. The Value Return Law also forbids caller-provided output
destinations. Sections whose current APIs still expose those parameters are
explicit migration gaps until their source and tests are updated.

The current terminal cookbook sections cover ten terminal implementation
files. Callable CLI implementation files `command.c`, `commandregistry.c`,
`logcommands.c`, and `scanner.c` still need their own sections; they are
documented below where their current public declarations permit a meaningful
call example.

## CommandParser class (commandparser.c)

```c
#include "cli/commandparser.h"

int main(void)
{
    Command *fromLine = CommandParser_parse("open notes.txt");
    Command *fromBytes = CommandParser_parseBytes("open notes.txt", 15u);
    Command_free(fromLine);
    Command_free(fromBytes);
    return 0;
}
```

## Command class (command.c)

`Command_toString` and `Command_toStringStruct` still take a destination buffer
and truncation output pointer, which violates the Value Return Law. These
legacy signatures remain a migration gap and are omitted from the call example.

```c
#include "cli/command.h"
#include "primitive/string.h"

int main(void)
{
    uint8_t *name = String("command-name-goes-here");
    uint8_t *arguments[] = { String("argument-goes-here") };
    Command *command = Command(name, arguments, 1u);
    Command *emptyCommand = Command();
    const uint8_t *commandName = Command_name(command);
    size_t argumentCount = Command_argumentCount(command);
    const uint8_t *argument = Command_argument(command, 0u);
    Command_free(command);
    Command_free(emptyCommand);



    return 0;
}
```

## CommandRegistry class (commandregistry.c)

`CommandRegistry_toString` and `CommandRegistry_toStringStruct` still take a
destination buffer and truncation output pointer; they remain migration gaps
and are omitted. `CommandRegistry_register` and `CommandRegistry_execute`
require a callback function. The cookbook forbids local helper definitions, so
those callback-dependent calls are documented as gaps here.

```c
#include "cli/commandregistry.h"

int main(void)
{
    CommandRegistry registry = CommandRegistry();
    CommandRegistryRow rows[8];
    bool rowsReserved = CommandRegistry_reserve(&registry, rows, 8u);
    bool outputCleared = CommandRegistry_setOutput(&registry, nullptr, nullptr);
    DeterminantOutputFn output = CommandRegistry_getOutput(&registry);
    void *hostContext = CommandRegistry_getHostContext(&registry);
    size_t count = CommandRegistry_getCount(&registry);
    size_t capacity = CommandRegistry_getCapacity(&registry);
    size_t exhaustionCount = CommandRegistry_exhaustionCount(&registry);
    const CommandRegistryRow *registeredRows = CommandRegistry_getRows(&registry);
    bool isActive = CommandRegistry_isActive(&registry);
    bool isFreed = CommandRegistry_free(&registry);







    return 0;
}
```

## LogCommands class (logcommands.c)

`LogCommands_stat` and `LogCommands_cat` need a live log path and output
callback. This standalone example has no callback definition or stable log
fixture, so both public calls are documented gaps.

```c
int main(void)
{
    return 0;
}
```

## Scanner class (scanner.c)

`Scanner_toString` and `Scanner_toStringStruct` still take a destination buffer
and truncation output pointer, which violates the Value Return Law. They remain
migration gaps and are omitted from this call example.

```c
#include "cli/scanner.h"
#include "primitive/string.h"

int main(void)
{
    char input[128];
    char largerInput[256];
    Scanner scanner = Scanner(input, sizeof input);
    bool hasInput = Scanner_feed(&scanner, "first-line\nsecond-word", sizeof "first-line\nsecond-word" - 1u, true);
    bool isReserved = Scanner_reserve(&scanner, largerInput, sizeof largerInput);
    bool hasNextLine = Scanner_hasNextLine(&scanner);
    uint8_t *line = Scanner_nextLine(&scanner);
    uint8_t *word = Scanner_nextWord(&scanner);
    size_t length = Scanner_getLength(&scanner);
    size_t capacity = Scanner_getCapacity(&scanner);
    size_t position = Scanner_getPosition(&scanner);
    bool isEnded = Scanner_isEnded(&scanner);
    size_t exhaustionCount = Scanner_exhaustionCount(&scanner);
    const char *bytes = Scanner_getBytes(&scanner);
    Scanner_reset(&scanner);
    string_free(line);
    string_free(word);







    return 0;
}
```

## TerminalButton class (terminal_button.c)

```c
#include "terminal/terminal_button.h"

int main(void)
{
    TerminalButton defaultButton = TerminalButton();
    Terminal terminal = Terminal();
    TerminalButton button = TerminalButton("button-label-goes-here", 2u, 3u);
    bool labelSet = TerminalButton_setLabel(&button, "renamed-button-label-goes-here");
    const char *label = TerminalButton_getLabel(&button);
    bool positionSet = TerminalButton_setPosition(&button, 4u, 5u);
    TerminalButtonPosition position = TerminalButton_getPosition(&button);
    TerminalButton_setFocused(&button, true);
    bool isFocused = TerminalButton_isFocused(&button);
    TerminalButton_setEnabled(&button, true);
    bool isEnabled = TerminalButton_isEnabled(&button);
    bool keyHandled = TerminalButton_key(&button, TERMINAL_KEY_ENTER);
    bool clickHandled = TerminalButton_click(&button, 4u, 5u);
    bool rendered = TerminalButton_render(&button, &terminal);
    TerminalProjection text = TerminalButton_toString(&button);
    TerminalProjection structuredText = TerminalButton_toStringStruct(&button);








    return 0;
}
```

## Terminal class (terminal.c)

The constructor starts paused. Operations that need caller-owned cell storage
or module callbacks are omitted because this API has no matching constructors
or setters. The gap list names those public calls explicitly.

```c
#include "terminal/terminal.h"

int main(void)
{
    Terminal terminal = Terminal();
    size_t width = Terminal_getWidth(&terminal);
    size_t height = Terminal_getHeight(&terminal);
    size_t capacity = Terminal_getCapacity(&terminal);
    uint64_t generation = Terminal_getGeneration(&terminal);
    size_t exhaustionCount = Terminal_exhaustionCount(&terminal);
    bool isPaused = Terminal_isPaused(&terminal);
    bool isActive = Terminal_isActive(&terminal);
    DeterminantOutputFn output = Terminal_getOutput(&terminal);
    void *hostContext = Terminal_getHostContext(&terminal);
    const char *cells = Terminal_getCells(&terminal);
    void *residentState = Terminal_getResidentState(&terminal);
    TerminalModule module = Terminal_getModule(&terminal);
    TerminalProjection text = Terminal_toString(&terminal);
    TerminalProjection structuredText = Terminal_toStringStruct(&terminal);
    bool paused = Terminal_pause(&terminal);
    bool freed = Terminal_free(&terminal);






    return 0;
}
```

`Terminal_bind` requires caller-owned cell storage and a valid output callback;
`Terminal_setOutput` requires a callback; `Terminal_swap` requires a module
with callbacks. `Terminal_resume`, `Terminal_render`, `Terminal_command`,
`Terminal_text`, `Terminal_clear`, and `Terminal_present` require those
resources, but the class exposes no constructor or setters for supplying them.

## TerminalFrame class (terminal_frame.c)

```c
#include "terminal/terminal_frame.h"

int main(void)
{
    TerminalFrame emptyFrame = TerminalFrame();
    TerminalRule defaultRule = TerminalRule();
    TerminalRule customRule = TerminalRule(0x2500u, 0x2502u);
    TerminalRule stripedRule = TerminalRule(0x2500u, 0x2502u, 0x2591u, 4u);
    TerminalFrame frame = TerminalFrame(8u, 8u);
    TerminalRule rule = TerminalRule('-', '|');
    TerminalCanvas root = TerminalCanvas(nullptr, nullptr, 40u, 12u);
    bool railsSet = TerminalFrame_setRails(&frame, 8u, 8u);
    TerminalFramePair rails = TerminalFrame_getRails(&frame);
    bool bandsSet = TerminalFrame_setBands(&frame, 2u, 1u);
    TerminalFramePair bands = TerminalFrame_getBands(&frame);
    bool backgroundSet = TerminalFrame_setBackground(&frame, nullptr);
    const TerminalImage *background = TerminalFrame_getBackground(&frame);
    TerminalFrameLayout layout = TerminalFrame_getLayout(&frame, &root);
    TerminalFrame_paintBackground(&frame, &root);
    TerminalCanvas headerCanvas = TerminalFrame_header(&frame, &root);
    TerminalCanvas leftCanvas = TerminalFrame_left(&frame, &root);
    TerminalCanvas centerCanvas = TerminalFrame_center(&frame, &root);
    TerminalCanvas rightCanvas = TerminalFrame_right(&frame, &root);
    TerminalCanvas footerCanvas = TerminalFrame_footer(&frame, &root);
    TerminalFrame_drawRules(&frame, &root, TerminalPen());
    bool ruleSet = TerminalFrame_setRule(&frame, rule);
    TerminalRule currentRule = TerminalFrame_getRule(&frame);
    TerminalRule_draw(&rule, &root, 1u, TerminalPen());
    TerminalRule_drawCut(&rule, &root, 2u, 1u, TerminalPen());
    TerminalRule_drawBox(&rule, &root, TerminalPen());
    TerminalProjection text = TerminalFrame_toString(&frame);
    TerminalProjection structuredText = TerminalFrame_toStringStruct(&frame);












    return 0;
}
```

## TerminalAppearance class (terminal_appearance.c)

```c
#include "terminal/terminal_appearance.h"

int main(void)
{
    TerminalAppearance appearance = TerminalAppearance();
    size_t presetCount = TerminalAppearance_presetCount();
    const char *presetName = TerminalAppearance_presetName(0u);
    TerminalAppearance preset = TerminalAppearance_preset(0u);
    TerminalAppearance namedAppearance = TerminalAppearance_named("appearance-name-goes-here");
    bool ruleSet = TerminalAppearance_setRule(&appearance, TerminalRule());
    TerminalRule rule = TerminalAppearance_getRule(&appearance);
    TerminalAppearanceColors colors = TerminalAppearance_getColors(&appearance);
    bool colorsSet = TerminalAppearance_setColors(&appearance, colors.accent, colors.muted, colors.text, colors.error);
    TerminalFrame frame = TerminalFrame();
    TerminalCanvas canvas = TerminalCanvas(nullptr, nullptr, 32u, 4u);
    TerminalAppearance_applyTo(&appearance, &frame);
    TerminalAppearance_drawRule(&appearance, &canvas, 0u, TerminalPen());
    TerminalProjection text = TerminalAppearance_toString(&appearance);
    TerminalProjection structuredText = TerminalAppearance_toStringStruct(&appearance);







    return 0;
}
```

## TerminalTextView class (terminal_text_view.c)

```c
#include "terminal/terminal_text_view.h"

int main(void)
{
    TerminalTextView emptyView = TerminalTextView();
    TerminalTextView zeroView = TerminalTextView();
    const char *lines[] = { "first-line-goes-here", "second-line-goes-here" };
    TerminalTextView view = TerminalTextView(lines, 2u);
    bool linesSet = TerminalTextView_setLines(&view, lines, 2u);
    TerminalTextViewLines borrowedLines = TerminalTextView_getLines(&view);
    bool scrollSet = TerminalTextView_setScroll(&view, 1u);
    size_t scroll = TerminalTextView_getScroll(&view);
    TerminalTextView_setTail(&view, true);
    bool isTail = TerminalTextView_isTail(&view);
    TerminalTextView_setPen(&view, TerminalPen());
    TerminalPen pen = TerminalTextView_getPen(&view);
    bool scrollMoved = TerminalTextView_scrollBy(&view, -1, 3u);
    TerminalCanvas canvas = TerminalCanvas();
    TerminalTextView_render(&view, &canvas);
    TerminalProjection text = TerminalTextView_toString(&view);
    TerminalProjection structuredText = TerminalTextView_toStringStruct(&view);








    return 0;
}
```

## TerminalListView class (terminal_list_view.c)

```c
#include "terminal/terminal_list_view.h"

int main(void)
{
    TerminalListView emptyView = TerminalListView();
    TerminalListView zeroView = TerminalListView();
    const char *labels[] = { "first-label-goes-here", "second-label-goes-here" };
    TerminalListView view = TerminalListView(labels, 2u);
    bool labelsSet = TerminalListView_setLabels(&view, labels, 2u);
    TerminalListViewLabels borrowedLabels = TerminalListView_getLabels(&view);
    bool selectionSet = TerminalListView_setSelection(&view, 1u);
    size_t selection = TerminalListView_getSelection(&view);
    bool scrollSet = TerminalListView_setScroll(&view, 0u);
    size_t scroll = TerminalListView_getScroll(&view);
    bool markerSet = TerminalListView_setMarker(&view, "selected-marker-goes-here");
    const char *marker = TerminalListView_getMarker(&view);
    TerminalListView_setPens(&view, TerminalPen(), TerminalPen());
    TerminalListViewPens pens = TerminalListView_getPens(&view);
    bool selectionMoved = TerminalListView_move(&view, 1, 3u);
    TerminalCanvas canvas = TerminalCanvas();
    TerminalListView_render(&view, &canvas);
    TerminalProjection text = TerminalListView_toString(&view);
    TerminalProjection structuredText = TerminalListView_toStringStruct(&view);









    return 0;
}
```

## TerminalInputLine class (terminal_input_line.c)

```c
#include "terminal/terminal_input_line.h"

int main(void)
{
    TerminalInputLine emptyInput = TerminalInputLine();
    TerminalInputLine zeroInput = TerminalInputLine();
    char inputText[128];
    TerminalInputLine input = TerminalInputLine(inputText, sizeof inputText);
    bool bufferBound = TerminalInputLine_bind(&input, inputText, sizeof inputText);
    const char *buffer = TerminalInputLine_getBuffer(&input);
    size_t capacity = TerminalInputLine_getCapacity(&input);
    size_t length = TerminalInputLine_length(&input);
    bool isBound = TerminalInputLine_isBound(&input);
    bool prefixSet = TerminalInputLine_setPrefix(&input, "input-prefix-goes-here");
    const char *prefix = TerminalInputLine_getPrefix(&input);
    TerminalInputLine_setPens(&input, TerminalPen(), TerminalPen());
    TerminalInputLinePens pens = TerminalInputLine_getPens(&input);
    bool characterAdded = TerminalInputLine_add(&input, 'x');
    bool characterRemoved = TerminalInputLine_backspace(&input);
    TerminalInputLine_clear(&input);
    TerminalCanvas canvas = TerminalCanvas();
    TerminalInputLine_render(&input, &canvas);
    TerminalProjection text = TerminalInputLine_toString(&input);
    TerminalProjection structuredText = TerminalInputLine_toStringStruct(&input);










    return 0;
}
```

## TerminalStatusBar class (terminal_status_bar.c)

```c
#include "terminal/terminal_status_bar.h"

int main(void)
{
    TerminalStatusBar emptyBar = TerminalStatusBar();
    TerminalStatusBar bar = TerminalStatusBar("left-status-goes-here");
    bool leftSet = TerminalStatusBar_setLeft(&bar, "updated-left-status-goes-here");
    const char *left = TerminalStatusBar_getLeft(&bar);
    bool rightSet = TerminalStatusBar_setRight(&bar, "right-status-goes-here");
    const char *right = TerminalStatusBar_getRight(&bar);
    TerminalStatusBar_setPens(&bar, TerminalPen(), TerminalPen());
    TerminalStatusBarPens pens = TerminalStatusBar_getPens(&bar);
    TerminalCanvas canvas = TerminalCanvas();
    TerminalStatusBar_render(&bar, &canvas);
    TerminalProjection text = TerminalStatusBar_toString(&bar);
    TerminalProjection structuredText = TerminalStatusBar_toStringStruct(&bar);







    return 0;
}
```

## TerminalImage class (terminal_image.c)

```c
#include "terminal/terminal_image.h"

int main(void)
{
    TerminalImage emptyImage = TerminalImage();
    const uint8_t rgbaPixels[] = { 255u, 0u, 0u, 255u };
    TerminalImage image = TerminalImage(rgbaPixels, 1u, 1u);
    bool pixelsSet = TerminalImage_setPixels(&image, rgbaPixels, 1u, 1u);
    const uint8_t *pixels = TerminalImage_getPixels(&image);
    size_t imageWidth = TerminalImage_getWidth(&image);
    size_t imageHeight = TerminalImage_getHeight(&image);
    bool isValid = TerminalImage_isValid(&image);
    bool rampSet = TerminalImage_setRamp(&image, "glyph-ramp-goes-here");
    const char *ramp = TerminalImage_getRamp(&image);
    TerminalImage_setStyle(&image, TERMINAL_STYLE_DIM);
    uint8_t style = TerminalImage_getStyle(&image);
    TerminalImage_setColor(&image, true);
    bool hasColor = TerminalImage_hasColor(&image);
    TerminalImageColorRamp purple = TerminalImage_rampPurple();
    bool colorRampSet = TerminalImage_setColorRamp(&image, purple.data, purple.count);
    TerminalImageColorRamp colorRamp = TerminalImage_getColorRamp(&image);
    TerminalImage_setJitter(&image, 4u, 123u);
    uint8_t jitter = TerminalImage_getJitter(&image);
    uint32_t jitterSeed = TerminalImage_getJitterSeed(&image);
    TerminalImage_setPaletteScatter(&image, 2u);
    uint8_t paletteScatter = TerminalImage_getPaletteScatter(&image);
    TerminalImage_setSkipTransparent(&image, true);
    bool skipsTransparent = TerminalImage_skipsTransparent(&image);
    TerminalImage_setInvert(&image, false);
    bool inverted = TerminalImage_inverted(&image);
    TerminalImage_setCellAspect(&image, 1.0);
    double cellAspect = TerminalImage_getCellAspect(&image);
    bool noiseSet = TerminalImage_setNoise(&image, "noise-glyphs-go-here", TERMINAL_COLOR_DEFAULT);
    const char *noise = TerminalImage_getNoise(&image);
    TerminalImage_setNoiseSeed(&image, 456u);
    uint32_t noiseSeed = TerminalImage_getNoiseSeed(&image);
    TerminalImage_setNoiseStyle(&image, TERMINAL_STYLE_DIM);
    uint8_t noiseStyle = TerminalImage_getNoiseStyle(&image);
    TerminalImage_setNoiseDensity(&image, 50u);
    uint8_t noiseDensity = TerminalImage_getNoiseDensity(&image);
    uint8_t luminance = TerminalImage_luminance(255u, 0u, 0u);
    char glyph = TerminalImage_glyph(&image, 128u);
    TerminalImageSample sample = TerminalImage_sampleCell(&image, 0u, 0u, 1u, 1u);
    TerminalCanvas canvas = TerminalCanvas();
    TerminalImage_render(&image, &canvas, 0u, 0u);
    TerminalProjection text = TerminalImage_toString(&image);
    TerminalProjection structuredText = TerminalImage_toStringStruct(&image);
    TerminalImage_renderFit(&image, &canvas);
    TerminalImage_renderContain(&image, &canvas);























    return 0;
}
```

## TerminalProjection class (terminal_projection.h)

```c
#include "terminal/terminal_projection.h"

int main(void)
{
    TerminalProjection projection = TerminalProjection_format(
        "terminal-label-goes-here: %u", 42u);
    return 0;
}
```

## TerminalCanvas class (terminal_canvas.c)

```c
#include "terminal/terminal_canvas.h"

int main(void)
{
    TerminalCanvas emptyCanvas = TerminalCanvas();
    TerminalPen zeroPen = TerminalPen();
    TerminalPen stylePen = TerminalPen(TERMINAL_STYLE_DIM);
    TerminalPen foregroundPen = TerminalPen(TERMINAL_STYLE_BOLD, TERMINAL_COLOR_DEFAULT);
    TerminalPen backgroundPen = TerminalPen(TERMINAL_STYLE_REVERSE,
                                            0x336699FFu, 0x101010FFu);
    uint32_t cells[64];
    uint8_t styles[64];
    uint32_t foreground[64];
    uint32_t background[64];
    TerminalCanvas styleCanvas = TerminalCanvas(cells, styles, 8u, 8u);
    TerminalPen pen = TerminalPen(TERMINAL_STYLE_BOLD, 0xFFFFFFFFu, 0x202020FFu);
    TerminalCanvas canvas = TerminalCanvas(cells, styles, foreground, background, 8u, 8u);
    bool isValid = TerminalCanvas_isValid(&canvas);
    TerminalCanvas subcanvas = TerminalCanvas_sub(&canvas, 1u, 1u, 4u, 4u);
    TerminalCanvas_fill(&canvas, ' ', pen);
    TerminalCanvas_fill(&styleCanvas, '.', stylePen);
    TerminalCanvas_text(&canvas, 0u, 0u, "text-goes-here", 14u, pen);
    TerminalCanvas_hline(&canvas, 1u, '-', pen);
    TerminalCanvas_vline(&canvas, 1u, '|', pen);
    TerminalCanvas_box(&canvas, pen);
    TerminalCanvasDecodedScalar decoded = TerminalCanvas_utf8Decode("A", 1u);
    TerminalCanvas_glyph(&canvas, 2u, 2u, decoded.codepoint, pen);
    size_t glyphWidth = TerminalCanvas_widthOf(0x6F22u);
    uint32_t glyph = TerminalCanvas_glyphAt(&canvas, 0u, 0u);
    uint8_t style = TerminalCanvas_styleAt(&canvas, 0u, 0u);
    uint32_t foregroundColor = TerminalCanvas_fgAt(&canvas, 0u, 0u);
    uint32_t backgroundColor = TerminalCanvas_bgAt(&canvas, 0u, 0u);
    size_t width = TerminalCanvas_getWidth(&canvas);
    size_t height = TerminalCanvas_getHeight(&canvas);
    bool hasStylePlane = TerminalCanvas_hasStylePlane(&canvas);
    bool hasColorPlane = TerminalCanvas_hasColorPlane(&canvas);
    TerminalCanvasTextRow row = TerminalCanvas_copyRow(&canvas, 0u);
    bool styleCanvasIsValid = TerminalCanvas_isValid(&styleCanvas);
    TerminalProjection text = TerminalCanvas_toString(&canvas);
    TerminalProjection structuredText = TerminalCanvas_toStringStruct(&canvas);

    return 0;
}
```

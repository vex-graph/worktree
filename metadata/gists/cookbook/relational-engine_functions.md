# Relational Engine — public call reference

Each section names one implementation file and demonstrates its public call
surface from one `main()`. These are API call references, not runnable recipes;
platform I/O and callback effects depend on the host. Constructor-shaped legacy
functions (`*_0`, `*_1`, etc.) are reached only through their constructor
macros. Where this API has no preferred constructor macro, the gap is called
out instead of inventing an object or initializing fields directly.

The workspace constitution abolishes caller-provided destinations. Getters and
calculations return values; multi-value results use named value records.
Examples below must match current headers. Every caller-provided destination,
output pointer, output buffer, output length, or output flag is prohibited; each
legacy signature of that shape is migration debt, not a cookbook example.
The identity-cell projections `Cell_toString` / `Cell_toStringStruct`,
`Shelf_toString` / `Shelf_toStringStruct`,
`VariableSlot_toString` / `VariableSlot_toStringStruct`,
`VariableHashMap_toString` / `VariableHashMap_toStringStruct`, and
`VariableMiniMap_toString` / `VariableMiniMap_toStringStruct` require output
buffers. The reflection name getters (`Class_getName`, `Field_getName`,
`Method_getName`, `Struct_getName`, and `Variable_getName`) fill caller buffers.
The reflection projections `Class_toString` / `Class_toStringStruct`,
`Field_toString` / `Field_toStringStruct`, `Method_toString` /
`Method_toStringStruct`, `Struct_toString` / `Struct_toStringStruct`,
`Variable_toString` / `Variable_toStringStruct` require output buffers.
`Memory_findAll`, `VariableSlot_foldName`, and the C and Rust APIs
listed in their gap notes write caller-owned outputs and are omitted.

## Memory class (mem.c)

`MemoryArena_create` has no preferred `MemoryArena(...)` constructor macro, and
the borrowed process default returned by `Memory_defaultArena()` must not be
destroyed with `MemoryArena_destroy`. Those creation/destruction forms remain
gaps. `MemoryArena_findAll` and `Memory_findAll` write into caller-provided
output arrays and are Value Return Law gaps. `Memory_init` and
`Memory_initTransient` remain
process lifecycle gaps; this example uses the default arena directly.

```c
#include "nio/mem.h"

int main(void)
{
    uint64_t typeId = 42u;
    const char payload[] = "memory-payload-goes-here";
    void *first = Memory_alloc(typeId, sizeof payload);
    void *second = Memory_alloc(typeId, sizeof payload);
    first = Memory_realloc(first, sizeof payload + 16u);
    size_t allocationLength = Memory_length(first);
    uint64_t allocationType = Memory_type(first);
    bool similarAllocations = Memory_similar(first, second);
    MemoryArena *defaultArena = Memory_defaultArena();
    void *arenaBlock = MemoryArena_alloc(defaultArena, typeId, sizeof payload);
    arenaBlock = MemoryArena_realloc(defaultArena, arenaBlock, sizeof payload + 16u);
    size_t arenaActiveBytes = MemoryArena_activeBytes(defaultArena);
    size_t arenaCapacity = MemoryArena_capacity(defaultArena);
    uint64_t arenaExhaustionCount = MemoryArena_exhaustionCount(defaultArena);
    MemoryArena_free(defaultArena, arenaBlock);
    uint64_t exhaustionCount = Memory_exhaustionCount();
    Memory_free(second);
    Memory_free(first);
    Memory_freeAll();
    MemoryArena_freeAll(defaultArena);

    void *temporary = Transient_alloc(typeId, sizeof payload);
    bool isTransient = Transient_contains(temporary);
    uint64_t transientGeneration = Transient_getGeneration();
    uint64_t transientExhaustionCount = Transient_exhaustionCount();
#if defined(DEBUG_BORROW_CHECK)
    const uint8_t *transientBuffer = Transient_getBuffer();
#endif
    MemoryLifetime lifetime = Memory_getLifetime(temporary);
    Transient_reset();
    return 0;
}
```

## Cache class (cache.c)

This interface has no constructor macro, and `Cache_open` returns its handle
through a caller-provided output pointer. `Cache_get_path` and `Cache_get_data`
also write caller-owned outputs. The remaining instance methods (`Cache_close`,
`Cache_has`, `Cache_put_data`, `Cache_put_file`, `Cache_evict`, `Cache_clear`,
and `Cache_get_dir`) cannot be called on a preferredly constructed cache yet.

```c
int main(void)
{
    return 0;
}
```

## Clipboard class (clipboard_mac.m)

`Clipboard_getText` and `Clipboard_getImage` fill caller-provided destinations
and remain migration gaps. Setter calls below pass input data.

```c
#include "io/clipboard.h"

int main(void)
{
    bool hasText = Clipboard_hasText();
    bool hasImage = Clipboard_hasImage();
    bool textWasSet = Clipboard_setText("clipboard-text-goes-here");
    unsigned char pixels[4u * 4u * 4u] = {0};
    bool imageWasSet = Clipboard_setImage(pixels, 4, 4);
    Clipboard_clear();




    return 0;
}
```

## Clipboard class (clipboard_stub.c)

This platform-exclusive implementation shares `io/clipboard.h` with the
macOS implementation. `Clipboard_getText` and `Clipboard_getImage` still
write caller-owned output buffers and dimensions, so they remain API migration
gaps.

```c
#include "io/clipboard.h"

int main(void)
{
    bool hasText = Clipboard_hasText();
    bool hasImage = Clipboard_hasImage();
    bool textWasSet = Clipboard_setText("clipboard-text-goes-here");
    bool imageWasSet = Clipboard_setImage(nullptr, 4, 4);
    Clipboard_clear();




    return 0;
}
```

## File class (file.c)

`File_open()` is the public allocation/opening entry point; there is no
`File(...)` constructor macro in `io/file.h` yet. `File_close`, `File_read`,
`File_write`, `File_seek`, `File_refreshSize`, `File_flush`, `File_handle`,
`File_name`, `File_size`, `File_pos`, `File_mode`, and `File_eof` all require a
successfully opened handle. The one-main call-only format has no failure branch
to prove `File_open()` produced one, so these handle-bound operations remain
constructor/callability gaps. The independent path operations are shown below.

```c
#include "io/file.h"

int main(void)
{
    const char path[] = "file-path-goes-here";
    File *file = File_open(path, FILE_MODE_READ | FILE_MODE_WRITE | FILE_MODE_CREATE);
    /* File_open may fail; handle-dependent calls need a non-null handle. */
    bool pathExists = File_exists(path);
    bool isDirectory = File_isDirectory("directory-path-goes-here");
    bool directoriesCreated = File_mkdirs("directory-path-goes-here");
    bool fileDeleted = File_delete("file-path-to-delete-goes-here");

    return 0;
}
```

## FileWriter class (filewriter.c)

There is no `FileWriter(...)` constructor macro. `FileWriter_open` requires
initialized caller-owned storage, and zeroing its fields directly would violate
the requested construction style. `FileWriter_write`, `FileWriter_flush`,
`FileWriter_close`, and `FileWriter_bytesWritten` also require that unavailable
instance; all of them remain constructor gaps.

```c
#include "io/filewriter.h"

int main(void)
{
    /* Add FileWriter(...) before demonstrating this caller-owned API. */
    return 0;
}
```

## HotFileSys class (hot_file.c)

This subsystem exposes `HotFileSys_init` and `HotFileSys_shutdown` but has no
object constructor macro. Those lifecycle functions conflict with the
requested construction style, so they are omitted. `HotFileSys_pumpEvents()`
is a standalone function and is called directly below.

```c
#include "io/hot_file.h"

int main(void)
{
    HotFileSys_pumpEvents();
    return 0;
}
```

## Log class (log.c)

`Log` is caller-owned storage and currently has no `Log(...)` constructor
macro. Its public initializer remains visible in the API but is not presented
as a constructor pattern. `Log_init`, `Log_initDefault`, `Log_shutdown`,
`Log_isEnabled`, `Log_isActive`, `Log_setActive`, `Log_path`,
`Log_appended`, `Log_dropped`, `Log_written`, `Log_append`, and
`Log_appendKind` all require that unavailable instance; demonstrating them
would require a field aggregate or use of `_init` as construction.

```c
#include "io/log.h"

int main(void)
{
    /* Add Log(...) before demonstrating this caller-owned API. */
    return 0;
}
```

## LogParser class (logparser.c)

`LogParser_parse` requires a record callback, which this one-main-only format
cannot define. `LogParser_formatRecord` fills a caller-provided character
buffer and is a Value Return Law migration gap; both calls are omitted.

```c
#include "io/logparser.h"
#include "io/logkind.h"

int main(void)
{
    const char path[] = "log-path-goes-here";
    bool isLogFile = LogParser_isLogFile(path);
    int64_t recordCount = LogParser_count(path);
    const char *kindName = LogParser_kindName(LOG_KIND_RENDER_PRESENT);
    return 0;
}
```

## ProcessSpawn class (process_spawn.c)

`ProcessSpawn(...)` is available as the constructor macro; the numbered
constructor arms are intentionally not shown. `ProcessSpawn_spawn` returns
its job through a caller-provided `ProcessSpawn *` output argument, so that
operation is omitted until its API returns a value or mutates an explicitly
selected job on the object.

```c
#include "io/process_spawn.h"

int main(void)
{
    ProcessSpawn *process = ProcessSpawn();
    const char *arguments[] = {"program-name-goes-here", nullptr};
    ProcessSpawn_setPid(process, 0);
    ProcessSpawn_setTimeoutMs(process, 1000u);
    ProcessSpawn_setExitCode(process, 0);
    ProcessSpawn_setCancelFlag(process, false);
    int32_t pid = ProcessSpawn_getPid(process);
    uint64_t timeoutMs = ProcessSpawn_getTimeoutMs(process);
    int32_t exitCode = ProcessSpawn_getExitCode(process);
    bool cancelRequested = ProcessSpawn_isCancelFlag(process);
    bool hasPendingJobs = ProcessSpawn_poll(process, 1000000u);
    ProcessSpawn_cancel(process);
    uint32_t jobCount = ProcessSpawn_getCount(process);
    int32_t jobPid = ProcessSpawn_getJobPid(process, 0u);
    int32_t jobExitCode = ProcessSpawn_getJobExitCode(process, 0u);
    bool isJobDone = ProcessSpawn_isJobDone(process, 0u);
    ProcessSpawn_free(process);
    return 0;
}
```

## VexHome class (vexhome.c)

```c
#include "io/vexhome.h"

int main(void)
{
    const char *root = VexHome_root();
    const char *projects = VexHome_projects();
    const char *logs = VexHome_logs();
    const char *fonts = VexHome_fonts();
    const char *placeholder = VexHome_placeholder();
    const char *cache = VexHome_cache("subsystem-name-goes-here");
    const char *cacheIndex = VexHome_cacheIndex("subsystem-name-goes-here");
    bool cacheReady = VexHome_cacheEnsure("subsystem-name-goes-here");
    bool homeReady = VexHome_ensure();
    const char *defaultLogPath = VexHome_defaultLogPath();

    return 0;
}
```

## FrameInbox class (frame_inbox.c)

A bounded caller-fed frame inbox. It is not a WebSocket
client: it opens no connection and implements no WebSocket protocol. The
caller feeds bytes into this R2-owned storage slot. No socket adapter is
currently wired to it in the workspace.

`FrameInbox(...)` is the constructor macro; numbered constructor arms are not
used. `FrameInbox_poll` writes bytes and length through caller-provided outputs,
so it is omitted until the API returns a value record. The remaining calls
show the legacy inbox API without a destination argument.

```c
#include "io/frame_inbox.h"

int main(void)
{
    FrameInbox *client = FrameInbox();
    const uint8_t frame[] = "frame-bytes-go-here";
    bool frameFed = FrameInbox_feed(client, frame, (uint32_t)sizeof frame);
    FrameInbox_cancel(client);
    FrameInbox_clear(client);
    FrameInbox_setState(client, FRAME_INBOX_CLOSED);
    FrameInboxState state = FrameInbox_getState(client);
    FrameInbox_setTimeoutNs(client, 1000000u);
    uint64_t timeoutNs = FrameInbox_getTimeoutNs(client);
    FrameInbox_setCancelled(client, false);
    bool cancelled = FrameInbox_isCancelled(client);
    uint32_t pendingBytes = FrameInbox_getPending(client);




    FrameInbox_free(client);
    return 0;
}
```

## Class class (class.c)

`Class(...)` is the constructor macro. `Class_construct` and
`Class_setConstruct` require a real constructor callback, and
`Class_forEachMethod` requires a visitor callback; the one-main example cannot
define those helpers, so those calls remain callback gaps. `Class_getName`
writes into a caller-provided character buffer, so it remains a getter
migration gap under the value-return rule. `Class_toString` and
`Class_toStringStruct` also require caller-provided output buffers.

```c
#include "reflection/class.h"

int main(void)
{
    Struct *layout = Struct("class-layout-goes-here");
    Class *type = Class("class-name-goes-here", layout);
    uint64_t classKind = Class_kind(type);
    bool classHasType = Class_check(type, 1u);
    Struct *classLayout = Class_getLayout(type);
    Class_setLayout(type, classLayout);
    ClassConstructFn construct = Class_getConstruct(type);
    Method *method = Method("method-name-goes-here");
    uint32_t methodIndex = Class_addMethod(type, method);
    Method *firstMethod = Class_getMethod(type, 0u);
    uint32_t methodCount = Class_methodCount(type);
    bool classNameSet = Class_setName(type, "renamed-class-goes-here");
    Method_free(method);
    Class_free(type);
    Struct_free(layout);
    return 0;
}
```

## Field class (field.c)

`Field_getName` writes into a caller-provided character buffer, so it remains a
getter migration gap under the value-return rule. `Field_read`, `Field_write`,
`Field_setRead`, and `Field_setSet` need real reader and writer callbacks, which
this one-main cookbook format cannot define. `Field_toString` and
`Field_toStringStruct` also require caller-provided output buffers.

```c
#include "reflection/field.h"

int main(void)
{
    Field *field = Field("field-name-goes-here");
    uint64_t fieldKind = Field_kind(field);
    bool fieldHasType = Field_check(field, 1u);
    Variable *embeddedVariable = Field_getVariable(field);
    bool fieldNameSet = Field_setName(field, "renamed-field-goes-here");
    VariableReadFn readFunction = Field_getRead(field);
    FieldSetFn setFunction = Field_getSet(field);
    Field_setTarget(field, nullptr);
    void *target = Field_getTarget(field);
    Field_free(field);
    return 0;
}
```

## Method class (method.c)

`Method_call` and `Method_setInvoke` need a real `MethodFn`, which this one-main
cookbook format cannot define. `Method_getName` writes into a caller-provided
character buffer. `Method_toString` and `Method_toStringStruct` require
caller-provided output buffers and remain Value Return Law gaps.

```c
#include "reflection/method.h"

int main(void)
{
    Method *method = Method("method-name-goes-here");
    uint64_t methodKind = Method_kind(method);
    bool methodHasType = Method_check(method, 1u);
    bool methodNameSet = Method_setName(method, "renamed-method-goes-here");
    MethodFn invoke = Method_getInvoke(method);
    Method_setTarget(method, nullptr);
    void *target = Method_getTarget(method);
    Method_free(method);
    return 0;
}
```

## Struct class (struct.c)

`Struct_forEach` requires a visitor callback, so it remains a callback gap in
the one-main format. `Struct_getName`, `Struct_toString`, and
`Struct_toStringStruct` write into caller-provided buffers and remain Value
Return Law gaps.

```c
#include "reflection/struct.h"

int main(void)
{
    Struct *layout = Struct("record-name-goes-here");
    uint64_t structKind = Struct_kind(layout);
    bool structHasType = Struct_check(layout, 1u);
    Field *field = Field("field-name-goes-here");
    uint32_t fieldIndex = Struct_add(layout, field);
    Field *firstField = Struct_get(layout, 0u);
    bool structNameSet = Struct_setName(layout, "renamed-record-goes-here");
    uint32_t fieldCount = Struct_count(layout);
    bool isEmpty = Struct_isEmpty(layout);
    Struct_free(layout);
    Field_free(field);
    return 0;
}
```

## Variable class (variable.c)

`Variable_read` and `Variable_setRead` need a real `VariableReadFn`, which this
one-main cookbook format cannot define. `Variable_toString` and
`Variable_toStringStruct` require caller-provided output buffers and remain
Value Return Law migration gaps. `Variable_getName` also writes into a
caller-provided character buffer.

```c
#include "reflection/variable.h"

int main(void)
{
    Variable *variable = Variable("variable-name-goes-here");
    uint64_t variableKind = Variable_kind(variable);
    bool variableHasType = Variable_check(variable, 1u);
    bool variableNameSet = Variable_setName(variable, "renamed-variable-goes-here");
    VariableReadFn readFunction = Variable_getRead(variable);
    Variable_setTarget(variable, nullptr);
    void *target = Variable_getTarget(variable);
    Variable_free(variable);
    return 0;
}
```

## Cell class (cell.c)

```c
#include "relational/cell.h"

int main(void)
{
    Cell *cell = Cell(42u, 0u);
    uint64_t cellType = Cell_typeId(cell);
    bool typeMatches = Cell_check(cell, 42u);
    Cell_setValue(cell, 123u);
    uintptr_t value = Cell_getValue(cell);
    Cell_free(cell);
    return 0;
}
```

## Shelf class (shelf.c)

`Shelf(...)` is the constructor macro; this class's methods also expose the
current initialize/shutdown lifecycle directly.

```c
#include "relational/shelf.h"

int main(void)
{
    Shelf *shelf = Shelf();
    uint32_t cellIndex = Shelf_addCell(shelf, 1u, 100u);
    uint32_t firstNode = Shelf_addNode(shelf, cellIndex);
    uint32_t secondNode = Shelf_addNode(shelf, cellIndex);
    uintptr_t cellValue = Shelf_getCell(shelf, cellIndex);
    uint32_t nextNode = Shelf_getNext(shelf, firstNode);
    bool nextSet = Shelf_setNext(shelf, firstNode, secondNode);
    bool nodesLinked = Shelf_link(shelf, firstNode, secondNode);
    bool headSet = Shelf_setHead(shelf, firstNode);
    uint32_t head = Shelf_getHead(shelf);
    uint32_t nodeCount = Shelf_count(shelf);
    bool isEmpty = Shelf_isEmpty(shelf);
    Shelf_shutdown(shelf);
    Shelf_free(shelf);
    return 0;
}
```

## SymbolTable class (symbol_table.c)

`SymbolTable(...)` has no constructor macro in this header. The cookbook cannot
show a valid call sequence until one is added. `SymbolTable_init`,
`SymbolTable_shutdown`, `SymbolTable_instant`, `SymbolTable_rename`,
`SymbolTable_getId`, `SymbolTable_getPointer`, `SymbolTable_setPointer`,
`SymbolTable_compareAndSetPointer`, `SymbolTable_getClassId`,
`SymbolTable_getName`, and `SymbolTable_getActiveCount` all require that
instance; `SymbolTable_findByClass` additionally writes into a caller-owned
array. Direct field initialization and the legacy initializer as construction
are excluded by the requested style.

```c
#include "relational/symbol_table.h"

int main(void)
{
    /* Add SymbolTable(...) before demonstrating this caller-owned API. */
    return 0;
}
```

## VariableHashMap class (variable_hash_map.c)

`VariableHashMap_forEach` requires a visitor callback and remains a one-main
callback gap.

```c
#include "relational/variable_hash_map.h"

int main(void)
{
    VariableHashMap *map = VariableHashMap();
    bool valueAdded = VariableHashMap_add(map, "hash-map-name-goes-here", 1u);
    uintptr_t pointer = VariableHashMap_get(map, "hash-map-name-goes-here");
    bool containsName = VariableHashMap_contains(map, "hash-map-name-goes-here");
    uint32_t entryCount = VariableHashMap_count(map);
    bool isEmpty = VariableHashMap_isEmpty(map);

    VariableHashMap_free(map);
    return 0;
}
```

## VariableMiniMap class (variable_mini_map.c)

`VariableMiniMap_forEach` requires a visitor callback and remains a one-main
callback gap.

```c
#include "relational/variable_mini_map.h"

int main(void)
{
    VariableMiniMap *map = VariableMiniMap();
    bool valueAdded = VariableMiniMap_add(map, "mini-map-name-goes-here", 1u);
    uintptr_t pointer = VariableMiniMap_get(map, "mini-map-name-goes-here");
    bool containsName = VariableMiniMap_contains(map, "mini-map-name-goes-here");
    uint32_t entryCount = VariableMiniMap_count(map);
    bool isEmpty = VariableMiniMap_isEmpty(map);

    VariableMiniMap_free(map);
    return 0;
}
```

## StringPool class (variable_pool.c)

This process-wide pool has no object constructor macro and requires
`StringPool_init()` with a live `MemoryArena`, which currently has no preferred
constructor macro either. `StringPool_count()` safely returns zero before
initialization, and `StringPool_shutdown()` is safe and idempotent before it, so
both direct calls are shown. `StringPool_intern`, `StringPool_find`,
`StringPool_isSlot`, `StringPool_slot`, and `StringPool_name` require the missing
initialized pool and remain lifecycle gaps.

```c
#include "relational/variable_pool.h"

int main(void)
{
    uint32_t slotCount = StringPool_count();
    StringPool_shutdown();
    return 0;
}
```

## VariableSlot class (variable_slot.c)

`VariableSlot(...)` is the constructor macro. Its inline initializer and
numbered allocation arms are intentionally not used as construction examples;
the direct `VariableSlot_init` form is an initializer gap.

```c
#include "relational/variable_slot.h"

int main(void)
{
    VariableSlot *slot = VariableSlot("variable.name-goes-here", 0u);
    uint32_t bucket = VariableSlot_bucketOf('v');
    bool nameSet = VariableSlot_setName(slot, "renamed.variable-goes-here");
    VariableSlot_setPointer(slot, 123u);
    const char *name = VariableSlot_getName(slot);
    uintptr_t pointer = VariableSlot_getPointer(slot);
    bool isEmpty = VariableSlot_isEmpty(slot);
    bool nameMatches = VariableSlot_nameEquals(slot, "renamed.variable-goes-here");
    VariableSlot_free(slot);
    return 0;
}
```

## Relational class (relational.c)

`Relational_*` operates on `SymbolTable`, which currently has no constructor
macro. `Relational_getId`, `Relational_getName`, `Relational_setName`,
`Relational_getValue`, `Relational_getValueById`, `Relational_setValue`,
`Relational_setValueById`, `Relational_getString`, `Relational_setString`,
`Relational_getFunction`, and `Relational_setFunction` need that scope.
`Relational_search` and `Relational_searchAll` also write matches through
caller-provided output arrays. A null scope is not a meaningful example; add
`SymbolTable(...)` before documenting direct facade calls.

```c
#include "relational/relational.h"

int main(void)
{
    /* Add SymbolTable(...) before demonstrating these scope-bound calls. */
    return 0;
}
```

## Type class (type.c)

The `Type_*` predicates and encoders are inline public functions in `type.h`;
the registry and inheritance functions are implemented in `type.c`.

```c
#include "type/type.h"

int main(void)
{
    uint64_t typeId = Type_make(PROJ_RELATIONAL_ENGINE, FORM_STRUCT_SINGLETON, 2u);
    uint64_t classId = Type_class(typeId);
    uint64_t form = Type_form(typeId);
    uint64_t project = Type_project(typeId);
    bool isStructForm = Type_isStruct(FORM_STRUCT_SINGLETON);
    bool isSingleton = Type_isSingleton(typeId);
    bool isArray = Type_isArray(typeId);
    bool isPointer = Type_isPointer(typeId);
    bool isStructSingleton = Type_isStructSingleton(typeId);
    bool isStructArray = Type_isStructArray(typeId);
    bool isStructSOA = Type_isStructSOA(typeId);
    bool isStructAOS = Type_isStructAOS(typeId);
    bool isStructCoexistent = Type_isStructCoexistent(typeId);
    bool isStructPointer = Type_isStructPointer(typeId);
    bool isPrimitive = Type_isPrimitive(typeId);
    bool isGlobal = Type_isGlobal(typeId);
    bool isLocale = Type_isLocale(typeId);
    bool isTransient = Type_isTransient(typeId);
    bool isProactive = Type_isProactive(typeId);
    bool isReactive = Type_isReactive(typeId);
    bool isProbable = Type_isProbable(typeId);
    bool isProbableObjects = Type_isProbableObjects(typeId);
    bool isFuture = Type_isFuture(typeId);
    bool isChoice = Type_isChoice(typeId);
    uint64_t architecture = Type_arch(2u);
    bool isVexspoke = Type_isVexspoke(2u);
    bool isHotcwap = Type_isHotcwap(2u);
    bool isDarling = Type_isDarling(2u);
    bool isDarkbase = Type_isDarkbase(2u);
    const uint32_t parents[] = {1u, 2u};
    bool parentsRegistered = Type_registerParents(PROJ_GRAPHVEX, parents, 2u);
    bool bareParentsRegistered = Type_registerBareParents(parents, 2u);
    uint64_t parentClass = Type_getParentClass(2u);
    bool isDerived = Type_isA(2u, 1u);
    return 0;
}
```

## NameSearch class (name_search.c)

This C primitive uses a non-prefixed exported name in its header. Its only
public operation writes the found row index through a caller-provided pointer,
so it is a migration gap.

```c
int main(void)
{
    return 0;
}
```

## String byte/text helpers (string.rs)

These functions are Rust APIs and have no C ABI, so a C `int main()` cannot
call them. This native Rust example shows both borrowed conversions directly.

```rust
use relational_engine_scratchpad::primitives::string::{as_text, to_byte_array};

fn main() {
    let bytes = to_byte_array("utf8-text-goes-here");
    let text = as_text(bytes);
}
```

## PreallocatedFile class (preallocated_file.rs)

The preferred `PreallocatedFile!` macro constructs this owner. Creation touches
the filesystem and can fail if physical reservation is unavailable. Its bounded
`to_string` and `to_string_struct` take caller-owned output buffers, so those
methods remain gaps under the workspace value-return rule.

```rust
fn main() {
    let closed_file = relational_engine_scratchpad::PreallocatedFile!();
    let mut file = relational_engine_scratchpad::PreallocatedFile!("trusted-existing-parent/file-bytes-go-here", 4096u64).expect("file reservation");
    let length = file.len();
    let is_empty = file.is_empty();
    let is_open = file.is_open();
    let path = file.path();
    let allocated_bytes = file.allocated_bytes();
    let synced = file.sync();
    file.close();
}
```

## Chunk class (chunk.rs)

`Chunk!(T, capacity)` is the preferred constructor. `get_mut` takes an exclusive
Rust borrow of the selected value; no caller-provided destination is involved.
`to_string` and `to_string_struct` remain output-buffer API gaps.

```rust
fn main() {
    let default_chunk = relational_engine_scratchpad::Chunk!(u64).expect("default chunk allocation");
    let mut chunk = relational_engine_scratchpad::Chunk!(u64, 4usize).expect("chunk allocation");
    let index = chunk.add(73u64).expect("append row");
    let value = chunk.get(index).copied();
    if let Some(value) = chunk.get_mut(index) { *value += 1; }
    let rows = chunk.as_slice();
    let row_count = chunk.len();
    let is_empty = chunk.is_empty();
    let capacity = chunk.get_capacity();
}
```

## Handle class (handle.rs)

`to_string` and `to_string_struct` write into caller-owned buffers and remain
output-buffer API gaps. `new` and `zero` are reached through `Handle!`.

```rust
fn main() {
    let handle = relational_engine_scratchpad::Handle!(7usize, 3u32);
    let index = handle.index();
    let generation = handle.generation();
    let is_zero = handle.is_zero();
    let zero_handle = relational_engine_scratchpad::Handle!();
}
```

## RowHandle class (nio/row_handle.rs)

The owner-issued identity is constructed with the canonical `RowHandle!`
macro. Its fixed ABI validation is crate-private. `to_string` and
`to_string_struct` write caller-owned buffers and remain output-buffer gaps.

```rust
fn main() {
    let handle = relational_engine_scratchpad::RowHandle!(17u64, 4usize, 2u32);
    let owner = handle.owner();
    let index = handle.index();
    let generation = handle.generation();
    let is_zero = handle.is_zero();
    let zero_handle = relational_engine_scratchpad::RowHandle!();
}
```

## Memory class (mem.rs)

`Memory!()` is the canonical constructor. Handles are local to this store and
must not be confused with ecosystem type IDs. Value-returning borrows and
mutations are shown; the API has no output-buffer getters.

```rust
fn main() {
    let mut memory = relational_engine_scratchpad::Memory!();
    let bytes_handle = memory.copy_bytes(relational_engine_scratchpad::Bytes!("payload-bytes-go-here")).expect("copy bytes");
    let bytes = memory.get(bytes_handle);
    let first_byte = memory.get_byte(bytes_handle, 0);
    let atomic_byte = memory.new_atomic_byte(7u8).expect("register atomic byte");
    let loaded_byte = memory.get_atomic_byte(atomic_byte);
    let stored_byte = memory.set_atomic_byte(atomic_byte, 8u8);
    let atomic_text = memory.new_atomic_string(b"initial-text-goes-here", 256usize).expect("register atomic text");
    let text = memory.get_atomic_string(atomic_text);
    let stored_text = memory.set_atomic_string(atomic_text, b"updated-text-goes-here");
    let updated_text = memory.get_atomic_string(atomic_text);
    let block_count = memory.len();
    let is_empty = memory.is_empty();
    let released = memory.release(bytes_handle);
    memory.clear();
}
```

## RowChunk class (row_chunk.rs)

The canonical macro selects byte size, alignment, and capacity. Borrowed row
slices are Rust return values. `get_mut` is an exclusive object borrow, not a
caller-provided output destination. `to_string` and `to_string_struct` are
output-buffer gaps.

```rust
fn main() {
    let mut rows = relational_engine_scratchpad::RowChunk!(8usize, 8usize, 4usize).expect("row chunk allocation");
    let row = rows.add(b"row-data").expect("append row");
    let bytes = rows.get(row);
    if let Some(bytes) = rows.get_mut(row) { bytes[0] = b'R'; }
    let is_empty = rows.is_empty();
    let has_backing = rows.has_backing();
    let is_full = rows.is_full();
    let removed = rows.remove(row);
    let released = rows.release_empty();
}
```

## TypedChunk class (typed_chunk.rs)

The macro is the preferred constructor. `generation_at` and the get methods
return values or borrows directly; `to_string` and `to_string_struct` remain
gaps because they write caller-owned buffers. `new_with_generation_limit` currently has no
constructor macro arm, so that configurable constructor remains a macro gap.

```rust
fn main() {
    let mut rows = relational_engine_scratchpad::TypedChunk!(u64, 4usize).expect("typed chunk allocation");
    let default_rows = relational_engine_scratchpad::TypedChunk!(u64).expect("default typed chunk allocation");
    let index = rows.add(73u64).expect("insert row");
    let value = rows.get(index).copied();
    let generation = rows.generation_at(index);
    let handle = rows.add_handle(91u64).expect("insert handled row");
    let by_handle = rows.get_handle(handle).copied();
    if let Some(value) = rows.get_mut(index) { *value += 1; }
    if let Some(value) = rows.get_handle_mut(handle) { *value += 1; }
    let count = rows.len();
    let is_empty = rows.is_empty();
    let capacity = rows.get_capacity();
    let is_full = rows.is_full();
    let removed_handle_value = rows.remove_handle(handle);
    let removed_index_value = rows.remove(index);
}
```

## ChunkedList class (chunked_list.rs)

`to_string` and `to_string_struct` write into caller-owned buffers and remain
output-buffer API gaps. `new` and `zero` are reached through `ChunkedList!`.

```rust
fn main() {
    let mut rows = relational_engine_scratchpad::ChunkedList!(u64, 4usize).expect("chunked list allocation");
    let default_rows = relational_engine_scratchpad::ChunkedList!(u64).expect("default chunked list allocation");
    let index = rows.add(73u64).expect("append row");
    let value = rows.get(index).copied();
    if let Some(value) = rows.get_mut(index) { *value += 1; }
    let first_chunk = rows.get_chunk(0);
    let chunk_count = rows.get_chunk_count();
    let rows_per_chunk = rows.get_rows_per_chunk();
    let row_count = rows.len();
    let is_empty = rows.is_empty();
}
```

## TypedPool class (typed_pool.rs)

`to_string` and `to_string_struct` write into caller-owned buffers and remain
output-buffer API gaps. `new` and `zero` are reached through `TypedPool!`.

```rust
fn main() {
    let mut values = relational_engine_scratchpad::TypedPool!(u64, 4usize).expect("typed pool allocation");
    let default_values = relational_engine_scratchpad::TypedPool!(u64).expect("default typed pool allocation");
    let index = values.add(73u64).expect("insert value");
    let value = values.get(index).copied();
    if let Some(value) = values.get_mut(index) { *value += 1; }
    let handle = values.add_handle(91u64).expect("insert handled value");
    let by_handle = values.get_handle(handle).copied();
    if let Some(value) = values.get_handle_mut(handle) { *value += 1; }
    let count = values.len();
    let is_empty = values.is_empty();
    let chunk_count = values.get_chunk_count();
    let rows_per_chunk = values.get_rows_per_chunk();
    let removed_by_handle = values.remove_handle(handle);
    let removed_by_index = values.remove(index);
    let released_chunks = values.release_empty_chunks();
}
```

## AtomicString class (atomic_string.rs)

There is no `AtomicString!()` constructor macro yet, so this section records the
construction gap and does not demonstrate the ordinary `AtomicString::new()`
method as a substitute. `AtomicString::get` and `AtomicString::set` also need
that instance; they return values and do not use caller-owned destinations.

```rust
fn main() {
    // Add AtomicString!(...) before demonstrating this public value API.
}
```

## VariableSlot class (variable_slot.rs)

`VariableSlot!` constructs a named slot. Name and pointer accessors return their
values directly. `to_string` and `to_string_struct` remain output-buffer gaps.

```rust
fn main() {
    let mut slot = relational_engine_scratchpad::VariableSlot!(b"user.profile", std::ptr::null()).expect("valid slot name");
    let empty_slot = relational_engine_scratchpad::VariableSlot!();
    let unbound_named_slot = relational_engine_scratchpad::VariableSlot!(b"session.token").expect("valid slot name");
    let is_empty = slot.is_empty();
    let renamed = slot.set_name(b"account.session");
    let name = slot.get_name();
    let padded_name = slot.get_name_bytes();
    slot.set_pointer(std::ptr::NonNull::<u8>::dangling().as_ptr());
    let pointer = slot.get_pointer();
}
```

## FixedMappedFile class (nio/fixed_mapped_file.rs)

The canonical macro supplies closed, read-only-open, and writable-open
construction. These calls are shown without executing filesystem access. The
unsafe open macros require the external-file exclusion contract stated in the
implementation. `from_preallocated` has no matching constructor macro yet;
`to_string` and `to_string_struct` retain caller-owned output buffers.

```rust
fn main() {
    let mut mapping = relational_engine_scratchpad::FixedMappedFile!();
    let read_only = unsafe { relational_engine_scratchpad::FixedMappedFile!("existing-file-path-goes-here") };
    let writable = unsafe { relational_engine_scratchpad::FixedMappedFile!("existing-file-path-goes-here", true) };
    let length = mapping.len();
    let is_empty = mapping.is_empty();
    let is_open = mapping.is_open();
    let is_writable = mapping.is_writable();
    let bytes = mapping.as_slice();
    let writable_bytes = mapping.as_mut_slice();
    let range = mapping.read(0usize, 8usize);
    let write = mapping.write(0usize, b"bytes-go");
    let flushed = mapping.flush();
    let synced = mapping.sync();
    mapping.close();
}
```

## GrowableMappedFile class (nio/growable_mapped_file.rs)

`GrowableMappedFile` has public `zero`, `create`, and `open` constructors but
no canonical constructor macro, so object operations are not demonstrated
through those ordinary constructor methods. Only `supported` is callable as a
standalone value. Instance methods `len`, `reserved`, `is_empty`, `is_open`,
`allocated_bytes`, `as_slice`, `as_mut_slice`, `read`, `write`, `grow_to`,
`flush`, `sync`, and `close` remain blocked on the constructor macro.
`to_string` and `to_string_struct` additionally require output buffers.

```rust
fn main() {
    let supported = relational_engine_scratchpad::GrowableMappedFile::supported();
}
```

## RowPool class (struct/row_pool.rs)

The preferred constructor macro accepts row geometry and optionally a per-chunk
capacity. Mutating borrows are ordinary exclusive Rust borrows; they do not use
caller-provided output destinations. `to_string` and `to_string_struct` remain
output-buffer gaps.

```rust
fn main() {
    let mut rows = relational_engine_scratchpad::RowPool!(8usize, 8usize, 4usize).expect("row pool allocation");
    let default_rows = relational_engine_scratchpad::RowPool!(8usize, 8usize).expect("default row pool allocation");
    let handle = rows.add(b"row-data").expect("append row");
    let bytes = rows.get(handle);
    if let Some(bytes) = rows.get_mut(handle) { bytes[0] = b'R'; }
    let count = rows.len();
    let is_empty = rows.is_empty();
    let row_size = rows.row_size();
    let alignment = rows.alignment();
    let rows_per_chunk = rows.rows_per_chunk();
    let owner = rows.owner();
    let removed = rows.remove(handle);
    let released_chunks = rows.release_empty_chunks();
}
```

## VariableRegistry class (variable/variable_registry.rs)

`to_string` and `to_string_struct` write caller-owned output buffers and remain
projection gaps. `new` and `zero` are reached through `VariableRegistry!`.

```rust
fn main() {
    let value = 73u64;
    let value_pointer = &value as *const u64 as *const u8;
    let mut variables = relational_engine_scratchpad::VariableRegistry!(4usize).expect("registry allocation");
    let default_variables = relational_engine_scratchpad::VariableRegistry!().expect("default registry allocation");
    let index = variables.add(b"account.balance", value_pointer).expect("register variable");
    let found = variables.find(b"account.balance");
    let slot = variables.get(index);
    let pointer_updated = variables.set_pointer(index, value_pointer);
    let count = variables.len();
    let is_empty = variables.is_empty();
}
```

## FixedMappedFile FFI class (fixed_mapped_file.rs)

This is the C ABI for the Rust-owned mapping. Its owner is created only through
`re_mmap_open`, which writes the handle through an output pointer. The public
read, borrow, metadata, and string projection functions also write outputs, and
there is no value-returning constructor macro. These are migration gaps.

```c
int main(void)
{
    return 0;
}
```

## GrowableMappedFile FFI class (growable_mapped_file.rs)

The C ABI constructs its owner through output-pointer functions and exposes
output-pointer getters and read projections. No value-returning constructor
macro is available, so this section remains an API gap.

```c
int main(void)
{
    return 0;
}
```

## StorageError class (storage_error.rs)

`StorageError` is a public value enum with no constructor helper. Construct its
variant directly and inspect it through standard Rust pattern matching.

```rust
use relational_engine_scratchpad::StorageError;

fn main() {
    let error = StorageError::Bounds;
    let is_bounds = matches!(error, StorageError::Bounds);
}
```

## ReMemory FFI class (memory.rs)

The C ABI exposes `re_memory_new()` rather than a `ReMemory(...)` constructor
macro, and its copy/read/get operations use caller-provided outputs. These are
migration gaps under the constructor and value-return rules.

```c
int main(void)
{
    return 0;
}
```

## ReRowPool FFI class (row_pool.rs)

Both C ABI constructors return handles through output pointers; the other
lookup/read/metadata functions use output pointers or output buffers. There is
no compliant value-returning construction and call sequence yet.

```c
int main(void)
{
    return 0;
}
```

## ReVariableRegistry FFI class (variable_registry.rs)

The C ABI constructor, insertion, lookup, and slot access all require caller
output pointers, so they are migration gaps under the value-return rule.

```c
int main(void)
{
    return 0;
}
```

# Darkbase Engine — public call reference

Each section covers one implementation file with callable public functions.
Constructor calls use class macros; numbered arms are never shown. Existing
caller-provided destinations are documented as migration gaps and omitted from
the examples per the Value Return Law.

## Database class (database.c)

`Database_lastError`, `Database_toString`, and `Database_toStringStruct` still
take output destinations. They remain migration gaps and are omitted.

```c
#include "database/database.h"
#include "database/database_result.h"
#include "reflection/struct.h"
#include "store/store.h"
#include "oop/type.h"

int main(void)
{
    Database *database = Database();
    Struct *schema = Struct("entity-name-goes-here");
    Store *store = Store();
    uint32_t borrowedRow = 42u;
    uint32_t ownedRow = 84u;
    int32_t fieldValue = 42;
    uint64_t databaseKind = Database_kind(database);
    bool correctDatabaseType = Database_check(database, TYPE_DB_DATABASE_SINGLETON);
    int32_t entityIndex = Database_define(database, schema);
    int32_t registeredEntityIndex = Database_entityIndex(database, "entity-name-goes-here");
    uint32_t entityCount = Database_entityCount(database);
    Struct *registeredSchema = Database_schema(database, "entity-name-goes-here");
    int32_t borrowedRowIndex = Database_insert(database, "entity-name-goes-here", &borrowedRow);
    int32_t ownedRowIndex = Database_insertOwned(database, "entity-name-goes-here", &ownedRow, sizeof ownedRow);
    void *storedRow = Database_row(database, "entity-name-goes-here", 0u);
    uint32_t rowCount = Database_count(database, "entity-name-goes-here");
    DatabaseResult *rows = Database_select(database, "entity-name-goes-here");
    DatabaseResult *equalRows = Database_queryEqual(database, "entity-name-goes-here",
        "field-name-goes-here", &fieldValue, sizeof fieldValue);
    DatabaseResult *rangeRows = Database_queryInt32Range(database, "entity-name-goes-here",
        "field-name-goes-here", 0, 100);
    int32_t indexBuildCode = Database_indexBuild(database, "entity-name-goes-here",
        "indexed-int32-field-name-goes-here");
    bool hasDeclaredIndex = Database_indexed(database, "entity-name-goes-here",
        "indexed-int32-field-name-goes-here");
    DatabaseFieldSpan fieldSpan = Database_fieldSpan(database,
        "entity-name-goes-here", "field-name-goes-here");
    int32_t saveCode = Database_save(database, "database-path-goes-here");
    int32_t loadCode = Database_load(database, "database-path-goes-here");
    int32_t saveStoreCode = Database_saveStore(database, store);
    int32_t loadStoreCode = Database_loadStore(database, store);
    DatabaseCatalogEntry catalog = Database_storeCatalogEntry(store, 0u);
    int32_t errorCode = Database_errorCode(database);
    const char *errorText = Database_errorText(DATABASE_OK);
    DatabaseResult_free(rows);
    DatabaseResult_free(equalRows);
    DatabaseResult_free(rangeRows);
    Database_free(database);
    Struct_free(schema);
    Store_free(store);

    return 0;
}
```

## DatabaseResult class (database_result.c)

`DatabaseResult_next` writes the row to `outRow`.
`DatabaseResult_toString` and `DatabaseResult_toStringStruct` write to
destination buffers. Those APIs remain migration gaps and are omitted.

```c
#include "database/database_result.h"
#include "oop/type.h"

int main(void)
{
    DatabaseResult *empty = DatabaseResult();
    uint64_t resultKind = DatabaseResult_kind(empty);
    bool correctResultType = DatabaseResult_check(empty, TYPE_DB_DATABASE_RESULT_SINGLETON);
    uint32_t rowCount = DatabaseResult_count(empty);
    uint32_t position = DatabaseResult_position(empty);
    DatabaseResult_rewind(empty);
    DatabaseResult_free(empty);




    return 0;
}
```

The nonempty constructors require a `ChunkedList` source, and `next` requires
an output pointer; the current public API has no value-returning row accessor.

## Page class (page.c)

`Page_toString` and `Page_toStringStruct` still require destination buffers and
truncation output pointers. They remain migration gaps and are omitted.

```c
#include "page/page.h"
#include "c23/constructor.h"

int main(void)
{
    uint8_t pageBytes[PAGE_SIZE_DEFAULT];
    bool validPageSize = Page_sizeValid(PAGE_SIZE_DEFAULT);
    Page *emptyPage = Page();
    Page *page = Page(pageBytes, sizeof pageBytes);
    PageCode formatCode = Page_format(page, 1u, PAGE_KIND_LEAF);
    PageCode appendCode = Page_append(page, (const uint8_t*) "payload-goes-here", 17u);
    PageCode sealCode = Page_seal(page);
    PageCode verifyCode = Page_verify(page);
    PageCode currentCode = Page_code(page);
    PageCode loadCode = Page_load(page);
    uint8_t *payload = Page_payload(page);
    const uint8_t *payloadView = Page_payloadOf(page);
    uint32_t used = Page_used(page);
    uint32_t capacity = Page_capacity(page);
    uint32_t freeSpace = Page_freeSpace(page);
    uint32_t pageId = Page_id(page);
    uint32_t pageKind = Page_kind(page);
    uint32_t size = Page_size(page);
    uint32_t sealValue = Page_sealValue(page);
    bool isSealed = Page_isSealed(page);
    bool isDirty = Page_isDirty(page);
    Page_markClean(page);
    PageCode resetCode = Page_reset(page, PAGE_KIND_LEAF);
    const char *pageCodeName = Page_codeName(PAGE_OK);
    const char *pageKindName = Page_kindName(PAGE_KIND_LEAF);
    Page_free(page);
    Page_free(emptyPage);




    return 0;
}
```

## Store class (store.c)

`Store_add` returns its page ID through `outPageId`; `Store_page_read` writes
the bytes, length, kind, and truncation state to output arguments. Both violate
the Value Return Law and are omitted. `Store_setCommitObserver` requires a
callback and cannot be shown without defining a helper in this cookbook format;
`Store_getCommitObserver` and `Store_getObserverContext` are shown below.

```c
#include "store/store.h"

int main(void)
{
    Store *closedStore = Store();
    Store *store = Store("database-path-goes-here", 65536u, PAGE_SIZE_DEFAULT, 8192u);
    StoreCode writeCode = Store_page_write(store, 1u, PAGE_KIND_LEAF, (const uint8_t*) "payload-goes-here", 17u);
    StoreCode releaseCode = Store_page_release(store, 1u);
    StoreCode syncCode = Store_sync(store);
    bool isOpen = Store_isOpen(store);
    bool isBlocked = Store_isBlocked(store);
    StoreCode storeCode = Store_code(store);
    uint32_t pageSize = Store_pageSize(store);
    uint32_t pageCount = Store_pageCount(store);
    uint32_t freeHead = Store_freeHead(store);
    size_t reservedBytes = Store_reserved(store);
    size_t journalBytes = Store_journalBytes(store);
    uint64_t sequence = Store_sequence(store);
    uint64_t exhaustionCount = Store_exhaustionCount(store);
    StoreCommitObserver commitObserver = Store_getCommitObserver(store);
    void *observerContext = Store_getObserverContext(store);
    const char *storeCodeName = Store_codeName(STORE_OK);
    Store_free(store);
    Store_free(closedStore);
    return 0;
}
```

`Store_toString` and `Store_toStringStruct` also require output destinations;
they remain migration gaps and are omitted.

## Wal class (wal.c)

`Wal_append` returns its sequence through an output pointer, `Wal_replay`
requires caller scratch plus a visitor callback, and `Wal_toString` and
`Wal_toStringStruct` require output destinations. These APIs remain migration
gaps. The callback and destination forms are omitted here.

```c
#include "wal/wal.h"

int main(void)
{
    Wal *closedWal = Wal();
    Wal *wal = Wal("journal-path-goes-here");
    bool isOpen = Wal_isOpen(wal);
    const char *path = Wal_path(wal);
    WalCode walCode = Wal_code(wal);
    uint64_t sequence = Wal_sequence(wal);
    uint64_t baseSequence = Wal_baseSequence(wal);
    uint32_t recordCount = Wal_count(wal);
    uint32_t recoveredRecords = Wal_recovered(wal);
    bool tailTorn = Wal_tailTorn(wal);
    uint64_t remainingBytes = Wal_remaining(wal);
    uint64_t exhaustionCount = Wal_exhaustionCount(wal);
    WalCode syncCode = Wal_sync(wal);
    WalCode checkpointCode = Wal_checkpoint(wal);
    const char *walCodeName = Wal_codeName(WAL_OK);
    Wal_free(wal);
    Wal_free(closedWal);


    return 0;
}
```

`Wal_append` and `Wal_replay` are deliberately not called until their
destination/callback contracts have a cookbook-compatible value-return form.

## Crc32 class (crc32.c)

```c
#include "util/crc32.h"

int main(void)
{
    const char checksumInput[] = "checksum-input-goes-here";
    uint32_t checksum = Crc32_update(CRC32_SEED, checksumInput, sizeof checksumInput - 1u);
    uint32_t finalChecksum = Crc32_finalize(checksum);
    uint32_t oneShotChecksum = Crc32_of(checksumInput, sizeof checksumInput - 1u);


    return 0;
}
```

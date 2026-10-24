# api-haven — Function Calls

Each section is one implementation file and its public header. This page shows
the call surface only; contracts remain in the headers and tests.

api-haven is R3: pure connector contracts. Transports are injected; this repo
does not own sockets, threads, exec, or vendor SDKs.

## AiChat class (ai_chat.c)

`AiChat_buildRequest` and `AiChat_complete` still take caller-owned output
buffers and response records. They are API migration gaps and are omitted from
this value-return cookbook example.

```c
#include "ai/ai_chat.h"
#include "ai/ai_provider.h"

int main(void)
{
    AiChat chat = AiChat("model-name-goes-here", "api-token-goes-here");
    AiProvider *providers = AiProvider_shared();
    const AiProviderSlot *peer = AiProvider_get(providers, "provider-name-goes-here");
    AiChat_setProvider(&chat, providers);
    AiChat_setPeer(&chat, peer);
    AiChat_setModel(&chat, "model-name-goes-here");
    AiChat_setApiKey(&chat, "api-token-goes-here");
    AiChat_setBaseUrl(&chat, "https://api.example.test");
    const AiProvider *selectedProvider = AiChat_getProvider(&chat);
    const AiProviderSlot *selectedPeer = AiChat_getPeer(&chat);
    const char *model = AiChat_getModel(&chat);
    const char *apiKey = AiChat_getApiKey(&chat);
    const char *baseUrl = AiChat_getBaseUrl(&chat);





    return 0;
}
```

## AiChatAnthropic class (ai_chat_anthropic.c)

`AiChatAnthropic_buildRequest` and `AiChatAnthropic_complete` still take
caller-owned output buffers and response records. They are API migration gaps.

```c
#include "ai/ai_chat_anthropic.h"

int main(void)
{
    AiChatAnthropic chat = AiChatAnthropic("model-name-goes-here", "api-token-goes-here");
    AiProvider *providers = AiProvider_shared();
    const AiProviderSlot *peer = AiProvider_get(providers, "provider-name-goes-here");
    AiChatAnthropic_setProvider(&chat, providers);
    AiChatAnthropic_setPeer(&chat, peer);
    AiChatAnthropic_setModel(&chat, "model-name-goes-here");
    AiChatAnthropic_setApiKey(&chat, "api-token-goes-here");
    AiChatAnthropic_setBaseUrl(&chat, "https://api.example.test");
    AiChatAnthropic_setMaxTokens(&chat, 2048u);
    const AiProvider *selectedProvider = AiChatAnthropic_getProvider(&chat);
    const AiProviderSlot *selectedPeer = AiChatAnthropic_getPeer(&chat);
    const char *model = AiChatAnthropic_getModel(&chat);
    const char *apiKey = AiChatAnthropic_getApiKey(&chat);
    const char *baseUrl = AiChatAnthropic_getBaseUrl(&chat);
    uint32_t maxTokens = AiChatAnthropic_getMaxTokens(&chat);






    return 0;
}
```

## AiChatGemini class (ai_chat_gemini.c)

`AiChatGemini_buildRequest` and `AiChatGemini_complete` still take
caller-owned output buffers and response records. They are API migration gaps.

```c
#include "ai/ai_chat_gemini.h"

int main(void)
{
    AiChatGemini chat = AiChatGemini("model-name-goes-here", "api-token-goes-here");
    AiProvider *providers = AiProvider_shared();
    const AiProviderSlot *peer = AiProvider_get(providers, "provider-name-goes-here");
    AiChatGemini_setProvider(&chat, providers);
    AiChatGemini_setPeer(&chat, peer);
    AiChatGemini_setModel(&chat, "model-name-goes-here");
    AiChatGemini_setApiKey(&chat, "api-token-goes-here");
    AiChatGemini_setBaseUrl(&chat, "https://api.example.test");
    const AiProvider *selectedProvider = AiChatGemini_getProvider(&chat);
    const AiProviderSlot *selectedPeer = AiChatGemini_getPeer(&chat);
    const char *model = AiChatGemini_getModel(&chat);
    const char *apiKey = AiChatGemini_getApiKey(&chat);
    const char *baseUrl = AiChatGemini_getBaseUrl(&chat);





    return 0;
}
```

## AiSse class (ai_sse.c)

`AiSse_feed` still writes decoded event text to a caller-provided buffer and
truncation flag. `HavenWsSource` has no constructor macro or setters, so
`AiSse_bind` is also a construction gap; the remaining lifecycle and getter
calls are shown directly.

```c
#include "ai/ai_sse.h"

int main(void)
{
    AiSse stream = AiSse();
    AiSse_setTimeout(&stream, 100u);
    AiSse_setCancelled(&stream, false);
    AiSse_setDone(&stream, false);
    void *slotHandle = AiSse_getSlotHandle(&stream);
    const HavenWsSource *slotSource = AiSse_getSlotSource(&stream);
    uint64_t timeoutMs = AiSse_getTimeout(&stream);
    bool isCancelled = AiSse_isCancelled(&stream);
    bool isDone = AiSse_isDone(&stream);
    uint32_t lineLength = AiSse_getLineLen(&stream);
    const char *eventName = AiSse_getEvent(&stream);
    AiSse_cancel(&stream);
    AiSse_reset(&stream);
    AiSse_unbind(&stream);







    return 0;
}
```

## AiProvider class (ai_provider.c)

Provider records are immutable static rows. `AiProvider_shared()` is the
existing singleton accessor; the class does not yet expose the preferred
`AiProvider(...)` constructor macro. The legacy base-URL projection returns a
borrowed string directly; there are no caller-provided destinations.

```c
#include "ai/ai_provider.h"

int main(void)
{
    AiProvider *providers = AiProvider_shared();
    uint32_t count = AiProvider_count(providers);
    const AiProviderSlot *firstProvider = AiProvider_at(providers, 0u);
    const AiProviderSlot *selectedProvider = AiProvider_get(providers, "provider-slug-goes-here");
    const char *resolvedBaseUrl = AiProvider_resolveBaseUrl(providers, selectedProvider);
    const char *slug = AiProvider_getSlug(providers, selectedProvider);
    const char *displayName = AiProvider_getDisplayName(providers, selectedProvider);
    const char *baseUrl = AiProvider_getBaseUrl(providers, selectedProvider);
    AiProviderFamily family = AiProvider_getFamily(providers, selectedProvider);
    AiProviderAuth auth = AiProvider_getAuth(providers, selectedProvider);
    AiProviderRegion region = AiProvider_getRegion(providers, selectedProvider);
    const char *note = AiProvider_getNote(providers, selectedProvider);
    uint32_t quotaPerDay = AiProvider_getQuotaPerDay(providers, selectedProvider);
    uint32_t quotaRemaining = AiProvider_getQuotaRemaining(providers, selectedProvider);
    int64_t resetUnix = AiProvider_getResetUnix(providers, selectedProvider);
    const char *authKind = AiProvider_getAuthKind(providers, selectedProvider);
    const char *licenseFamily = AiProvider_getLicenseFamily(providers, selectedProvider);















    return 0;
}
```

## AppProvider class (app_provider.c)

`AppProvider_shared()` is the existing singleton accessor; the class does not
yet expose the preferred `AppProvider(...)` constructor macro.
`AppProvider_resolveTarget` still writes into a caller buffer, so that public
operation is an API migration gap and is omitted here.

```c
#include "app/app_provider.h"

int main(void)
{
    AppProvider *providers = AppProvider_shared();
    uint32_t count = AppProvider_count(providers);
    const AppProviderSlot *firstProvider = AppProvider_at(providers, 0u);
    const AppProviderSlot *selectedProvider = AppProvider_get(providers, "provider-slug-goes-here");
    const char *slug = AppProvider_getSlug(providers, selectedProvider);
    const char *displayName = AppProvider_getDisplayName(providers, selectedProvider);
    AppProviderFamily family = AppProvider_getFamily(providers, selectedProvider);
    AppProviderAuth auth = AppProvider_getAuth(providers, selectedProvider);
    const char *bundleIdOrScheme = AppProvider_getBundleIdOrScheme(providers, selectedProvider);
    const char *note = AppProvider_getNote(providers, selectedProvider);








    return 0;
}
```

## AssetProvider class (asset_provider.c)

`AssetProvider_shared()` is the existing singleton accessor; the class does
not yet expose the preferred `AssetProvider(...)` constructor macro.

```c
#include "asset/asset_provider.h"

int main(void)
{
    AssetProvider *providers = AssetProvider_shared();
    uint32_t count = AssetProvider_count(providers);
    const AssetProviderSlot *firstProvider = AssetProvider_at(providers, 0u);
    const AssetProviderSlot *selectedProvider = AssetProvider_get(providers, "provider-slug-goes-here");
    const char *slug = AssetProvider_getSlug(providers, selectedProvider);
    const char *displayName = AssetProvider_getDisplayName(providers, selectedProvider);
    const char *apiBase = AssetProvider_getApiBase(providers, selectedProvider);
    const char *licenseFamily = AssetProvider_getLicenseFamily(providers, selectedProvider);
    const char *sampleTitle = AssetProvider_getSampleTitle(providers, selectedProvider);
    const char *sampleAuthor = AssetProvider_getSampleAuthor(providers, selectedProvider);
    const char *samplePreview = AssetProvider_getSamplePreview(providers, selectedProvider);
    const char *sampleDownload = AssetProvider_getSampleDownload(providers, selectedProvider);
    const char *note = AssetProvider_getNote(providers, selectedProvider);











    return 0;
}
```

## DbProvider class (db_provider.c)

`DbProvider_shared()` is the existing singleton accessor; the class does not
yet expose the preferred `DbProvider(...)` constructor macro.

```c
#include "database/db_provider.h"

int main(void)
{
    DbProvider *providers = DbProvider_shared();
    uint32_t count = DbProvider_count(providers);
    const DbProviderSlot *firstProvider = DbProvider_at(providers, 0u);
    const DbProviderSlot *selectedProvider = DbProvider_get(providers, "provider-slug-goes-here");
    const DbProviderSlot *engineProvider = DbProvider_findByEngine(providers, "engine-name-goes-here");
    const char *slug = DbProvider_getSlug(providers, selectedProvider);
    const char *displayName = DbProvider_getDisplayName(providers, selectedProvider);
    const char *engine = DbProvider_getEngine(providers, selectedProvider);
    uint16_t defaultPort = DbProvider_getDefaultPort(providers, selectedProvider);
    DbProviderFamily family = DbProvider_getFamily(providers, selectedProvider);
    const char *note = DbProvider_getNote(providers, selectedProvider);









    return 0;
}
```

## EngineProvider class (engine_provider.c)

`EngineProvider_shared()` is the existing singleton accessor; the class does
not yet expose the preferred `EngineProvider(...)` constructor macro.
`EngineProvider_resolveCli` still requires a caller-provided output buffer and
is documented as an API migration gap.

```c
#include "harness/engine_provider.h"

int main(void)
{
    EngineProvider *providers = EngineProvider_shared();
    uint32_t count = EngineProvider_count(providers);
    const EngineProviderSlot *firstProvider = EngineProvider_at(providers, 0u);
    const EngineProviderSlot *selectedProvider = EngineProvider_get(providers, "provider-slug-goes-here");
    const char *slug = EngineProvider_getSlug(providers, selectedProvider);
    const char *displayName = EngineProvider_getDisplayName(providers, selectedProvider);
    const char *cliName = EngineProvider_getCliName(providers, selectedProvider);
    EngineProviderFamily family = EngineProvider_getFamily(providers, selectedProvider);
    EngineProviderAuth auth = EngineProvider_getAuth(providers, selectedProvider);
    const char *note = EngineProvider_getNote(providers, selectedProvider);








    return 0;
}
```

## SearchProvider class (search_provider.c)

`SearchProvider_shared()` is the existing singleton accessor; the class does
not yet expose the preferred `SearchProvider(...)` constructor macro.
`SearchProvider_resolveEndpoint` still requires a caller-provided output
buffer and is documented as an API migration gap.

```c
#include "search/search_provider.h"

int main(void)
{
    SearchProvider *providers = SearchProvider_shared();
    uint32_t count = SearchProvider_count(providers);
    const SearchProviderSlot *firstProvider = SearchProvider_at(providers, 0u);
    const SearchProviderSlot *selectedProvider = SearchProvider_get(providers, "provider-slug-goes-here");
    const char *slug = SearchProvider_getSlug(providers, selectedProvider);
    const char *displayName = SearchProvider_getDisplayName(providers, selectedProvider);
    SearchProviderFamily family = SearchProvider_getFamily(providers, selectedProvider);
    SearchProviderAuth auth = SearchProvider_getAuth(providers, selectedProvider);
    const char *endpoint = SearchProvider_getEndpoint(providers, selectedProvider);
    const char *note = SearchProvider_getNote(providers, selectedProvider);
    uint32_t quotaPerDay = SearchProvider_getQuotaPerDay(providers, selectedProvider);
    uint32_t quotaRemaining = SearchProvider_getQuotaRemaining(providers, selectedProvider);
    int64_t resetUnix = SearchProvider_getResetUnix(providers, selectedProvider);
    const char *authKind = SearchProvider_getAuthKind(providers, selectedProvider);
    const char *licenseFamily = SearchProvider_getLicenseFamily(providers, selectedProvider);













    return 0;
}
```

## ApiAuth functions (auth.c)

`ApiAuth` has named legacy construction functions rather than the preferred
`ApiAuth(...)` constructor macro: `ApiAuth_none`, `ApiAuth_apiKey`,
`ApiAuth_bearer`, and `ApiAuth_bearerFn` are therefore constructor gaps.
`ApiAuth_apply` also requires a caller-owned buffer and output pointer, so it is
a Value Return Law gap.

```c
int main(void)
{
    return 0;
}
```

## APIClient functions (client.c)

`APIClient_sendTelemetry` needs an `APIClientTelemetry` value, but that record
has no constructor macro or setters. The example does not initialize its fields
directly; construction of the telemetry value is an API ergonomics gap.

```c
#include "api/client.h"

int main(void)
{
    return 0;
}
```

## HavenWsFanout class (haven_ws_fanout.c)

The registry has `HavenWsFanout(...)`, but `HavenWsSource` is a callback table
with no constructor macro or setters. `HavenWsFanout_attach` and a valid
detach sequence therefore remain API gaps; the example does not use an
aggregate literal or assign callback fields directly. The null-safe detach
rejection path is still shown as a direct call.

```c
#include "api/haven_ws_fanout.h"

int main(void)
{
    HavenWsFanout *fanout = HavenWsFanout();
    bool detached = HavenWsFanout_detach(fanout, nullptr);
    uint32_t deliveredFrames = HavenWsFanout_pollStep(fanout, 100u);
    uint32_t slotCount = HavenWsFanout_getCount(fanout);
    void *slotHandle = HavenWsFanout_getHandle(fanout, 0u);
    HavenWsFanout_free(fanout);



    return 0;
}
```

## Rest functions (rest.c)

`Rest_get` and `Rest_postJson` require an `HttpResponse` with a caller-provided
response body buffer. These APIs are migration gaps under the Value Return Law.

```c
int main(void)
{
    return 0;
}
```

## AppBroker class (app_broker.c)

`AppBroker_action` requires caller-provided output buffers and a driver callback,
so it is a Value Return Law gap and has no no-helper cookbook form. The
`AppDriverTable` value also has no constructor macro or setters, so
`AppBroker_setDriver` cannot be shown without aggregate/direct-field setup. The
broker has no public `free` operation; it is constructed with `AppBroker(...)`.

```c
#include "app/app_broker.h"

int main(void)
{
    AppBroker broker = AppBroker();
    AppProvider *providers = AppProvider_shared();
    const AppProviderSlot *target = AppProvider_get(providers, "app-slug-goes-here");
    AppBroker_setTarget(&broker, target);
    AppBroker_setTimeout(&broker, 100u);
    const AppProviderSlot *selectedTarget = AppBroker_getTarget(&broker);
    void *driver = AppBroker_getDriver(&broker);
    uint64_t timeoutMs = AppBroker_getTimeout(&broker);
    bool isRunning = AppBroker_isRunning(&broker);
    uint32_t jobCount = AppBroker_getJobCount(&broker);
    const AppJob *job = AppBroker_getJobAt(&broker, 0u);
    AppStatus jobStatus = AppBroker_getJobStatus(&broker, 0u);
    AppStatus lastStatus = AppBroker_getLastStatus(&broker);
    AppStatus polledStatus = AppBroker_poll(&broker, 0u);
    bool cancelled = AppBroker_cancel(&broker, 0u);








    return 0;
}
```

## AssetBroker class (asset_broker.c)

`AssetBroker_copyChunk`, `AssetBroker_cachePath`, and `AssetBroker_setCacheSub`
still require caller-owned output buffers/flags, so they remain API migration
gaps and are omitted.

```c
#include "asset/asset_broker.h"

int main(void)
{
    AssetBroker broker = AssetBroker("asset-cache-slot-goes-here");
    AssetBroker_setChunkBudget(&broker, 100u);
    AssetBroker_setCancelled(&broker, false);
    AssetBroker_setBytesCopied(&broker, 0u);
    const char *cacheSub = AssetBroker_getCacheSub(&broker);
    uint64_t chunkBudgetMs = AssetBroker_getChunkBudget(&broker);
    bool isCancelled = AssetBroker_isCancelled(&broker);
    uint32_t bytesCopied = AssetBroker_getBytesCopied(&broker);
    AssetBroker_cancel(&broker);
    AssetBroker_reset(&broker);




    return 0;
}
```

## DbSqliteFile class (db_sqlite_file.c)

`DbSqliteFile_describe` and `DbSqliteFile_exec` still write caller-owned output
buffers. `DbSqliteFile_bind` also needs a `DbSqliteExec` callback table, which
has no constructor macro or setters; binding is an API gap. The example keeps
the slot unbound without initializing the callback field directly.

```c
#include "database/db_sqlite_file.h"

int main(void)
{
    DbSqliteFile file = DbSqliteFile("database-path-goes-here");
    DbSqliteFile_setPath(&file, "database-path-goes-here");
    DbSqliteFile_setCaps(&file, DB_SQLITE_CAP_READ);
    DbSqliteFile_setMaxBytes(&file, 1048576u);
    DbSqliteFile_setReadOnly(&file, true);
    const char *path = DbSqliteFile_getPath(&file);
    uint32_t caps = DbSqliteFile_getCaps(&file);
    uint64_t maxBytes = DbSqliteFile_getMaxBytes(&file);
    bool isReadOnly = DbSqliteFile_isReadOnly(&file);
    void *boundHandle = DbSqliteFile_getExecHandle(&file);
    const DbSqliteExec *boundTable = DbSqliteFile_getExecTable(&file);
    DbSqliteFile_unbind(&file);






    return 0;
}
```

## DiscordWebhook functions (discord.c)

`DiscordEmbed` has no constructor macro or setters, so
`DiscordWebhook_sendEmbed` remains a value-construction gap. The text webhook
call accepts its arguments directly.

```c
#include "com/discord/discord.h"

int main(void)
{
    bool sentText = DiscordWebhook_sendText(
        "https://discord.example.test/webhook-token-goes-here",
        "message-goes-here", "bot-name-goes-here", "avatar-url-goes-here");

    return 0;
}
```

## SlackWebhook functions (slack.c)

```c
#include "com/slack/slack.h"

int main(void)
{
    bool sent = SlackWebhook_sendText(
        "https://slack.example.test/webhook-token-goes-here",
        "message-goes-here", "bot-name-goes-here", "icon-url-goes-here");

    return 0;
}
```

## Harness class (harness.c)

`Harness_run` still returns the job ID through an output pointer, so that API
is an explicit migration gap. `HarnessDriverTable` has no constructor macro or
setters, so `Harness_setDriver` cannot be shown without direct field setup.

```c
#include "harness/harness.h"

int main(void)
{
    Harness harness = Harness();
    EngineProvider *providers = EngineProvider_shared();
    const EngineProviderSlot *engine = EngineProvider_get(providers, "engine-slug-goes-here");
    Harness_setEngine(&harness, engine);
    Harness_setTimeout(&harness, 100u);
    const EngineProviderSlot *selectedEngine = Harness_getEngine(&harness);
    void *driver = Harness_getDriver(&harness);
    uint64_t timeoutMs = Harness_getTimeout(&harness);
    bool isRunning = Harness_isRunning(&harness);
    uint32_t jobCount = Harness_getJobCount(&harness);
    const HarnessJob *job = Harness_getJobAt(&harness, 0u);
    HarnessStatus jobStatus = Harness_getJobStatus(&harness, 0u);
    HarnessStatus lastStatus = Harness_getLastStatus(&harness);
    HarnessStatus polledStatus = Harness_poll(&harness, 0u);
    bool cancelled = Harness_cancel(&harness, 0u);








    return 0;
}
```

## McpServer class (mcp_server.c)

`McpServer_shared()` is the existing singleton accessor; the class does not
yet expose the preferred `McpServer(...)` constructor macro.
`McpServer_handleLine` still renders into a caller-provided output buffer. It
remains an API migration gap. `McpServer_bindHarnessDriver` and
`McpServer_bindAppDriver` require `HarnessDriverTable` and `AppDriverTable`
values, which have no constructor macros or setters; those calls remain
constructor gaps rather than using direct field initialization.

```c
#include "mcp/mcp_server.h"

int main(void)
{
    McpServer *server = McpServer_shared();
    const char *name = McpServer_getName(server);
    const char *version = McpServer_getVersion(server);
    const char *protocolVersion = McpServer_getProtocolVersion(server);
    bool isInitialized = McpServer_isInitialized(server);




    return 0;
}
```

## MCP stdio entry point (mcp_main.c)

This implementation file is the executable's `main` itself, not a class API
that another example can call. Its interactive stdin/stdout loop is therefore
represented by this standalone entry-point example rather than a recursive
call to `main`.

```c
#include "mcp/mcp_server.h"

int main(void)
{
    McpServer *server = McpServer_shared();

    return 0;
}
```

`AiChat_buildRequest` and `AiChat_complete` require caller-provided output
buffers/response records, so they remain Value Return Law gaps. Their message
input is also the `AiMessage` record, which currently has no constructor macro
or setters; direct field initialization is omitted.

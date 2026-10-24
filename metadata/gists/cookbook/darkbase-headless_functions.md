# darkbase-headless — Function Calls

Each section names one implementation file and shows its
public functions inside one `main`. This is not a claim of transport, TLS,
authorization, or UI integration.

## HeadlessProtocol class (headless_protocol.c)

`HeadlessProtocol_feed` and `HeadlessProtocol_encode` take caller-provided
outputs. `HeadlessProtocol_toString` and `HeadlessProtocol_toStringStruct` also
write into caller buffers. They are migration gaps under the value-return rule
and are omitted from the calls.

```c
#include "protocol/headless_protocol.h"

int main(void)
{
    uint8_t storage[128];
    HeadlessProtocol frame = HeadlessProtocol(storage, sizeof storage);
    bool frameFinished = HeadlessProtocol_finish(&frame);
    bool ready = HeadlessProtocol_isReady(&frame);
    bool failed = HeadlessProtocol_isFailed(&frame);
    uint32_t code = HeadlessProtocol_getCode(&frame);
    uint64_t exhaustionCount = HeadlessProtocol_getExhaustionCount(&frame);
    size_t capacity = HeadlessProtocol_getCapacity(&frame);
    size_t used = HeadlessProtocol_getUsed(&frame);
    size_t expected = HeadlessProtocol_getExpected(&frame);
    uint16_t kind = HeadlessProtocol_getKind(&frame);
    uint16_t operation = HeadlessProtocol_getOperation(&frame);
    uint16_t status = HeadlessProtocol_getStatus(&frame);
    uint32_t requestId = HeadlessProtocol_getRequestId(&frame);
    const uint8_t *payload = HeadlessProtocol_getPayload(&frame);
    size_t payloadLength = HeadlessProtocol_getPayloadLength(&frame);
    bool frameReleased = HeadlessProtocol_release(&frame);
    HeadlessProtocol_reset(&frame);













    return 0;
}
```

## HeadlessService class (service.c)

`HeadlessService_start` requires callback implementations and caller-owned
bootstrap output buffers. `HeadlessService_toString` and
`HeadlessService_toStringStruct` also require destinations. These APIs are
migration gaps under the value-return and one-main call-example rules.

```c
#include "service/service.h"

int main(void)
{
    HeadlessService *service = HeadlessService("database-file-path-goes-here");
    bool iterationsSet = HeadlessService_setPasswordIterations(service, 210000u);
    uint32_t passwordIterations = HeadlessService_getPasswordIterations(service);
    bool loggedIn = HeadlessService_adminLogin(service, "admin-user-goes-here", "current-password-goes-here", 123456u);
    bool loggedInAt = HeadlessService_adminLoginAt(service, "admin-user-goes-here", "current-password-goes-here", 123456u, 1760000000u);
    bool passwordChanged = HeadlessService_changeAdminPassword(service, "current-password-goes-here", "new-password-goes-here", 123456u);
    bool passwordChangedAt = HeadlessService_changeAdminPasswordAt(service, "current-password-goes-here", "new-password-goes-here", 123456u, 1760000000u);
    bool requestGateSet = HeadlessService_setAcceptRequests(service, true);
    bool acceptingRequests = HeadlessService_isAcceptingRequests(service);
    bool requestAllowed = HeadlessService_isRequestAllowed(service);
    HeadlessService_free(service);



    return 0;
}
```

# Sesh — public call reference

The public projections `Operation_toString` / `Operation_toStringStruct`,
`SeshClient_toString` / `SeshClient_toStringStruct`,
`Workspace_toString` / `Workspace_toStringStruct`,
`Resource_toString` / `Resource_toStringStruct`,
`AuthService_toString` / `AuthService_toStringStruct`,
`Operations_toString` / `Operations_toStringStruct`,
`SeshSnapshot_toString` / `SeshSnapshot_toStringStruct`, and
`Sesh_toString` / `Sesh_toStringStruct` require caller-provided destinations.
`SeshText_format` also writes to a caller buffer, and `Operations_find` writes
a found operation through an output pointer. Those APIs are migration gaps
under the value-return rule and are omitted below.
`AuthService_setAuth`, `AuthService_setVerifier`, and
`AuthService_authenticate` also need configured inputs: API Haven `ApiAuth`
constructors have no chooser macro, and the verifier must be a real non-null
callback. This one-main call reference does not define a callback helper, so
those configured calls are an explicit constructor/API gap rather than a
misleading null-input example.

## Operation class (operation.c)

```c
#include "lang/operation.h"

int main(void)
{
    Operation operation = Operation();
    bool idSet = Operation_setId(&operation, 9u);
    bool clientIdSet = Operation_setClientId(&operation, 7u);
    bool workspaceIdSet = Operation_setWorkspaceId(&operation, 22u);
    bool resourceIdSet = Operation_setResourceId(&operation, 31u);
    bool expectedRevisionSet = Operation_setExpectedRevision(&operation, 0u);
    uint64_t id = Operation_getId(&operation);
    uint64_t clientId = Operation_getClientId(&operation);
    uint64_t workspaceId = Operation_getWorkspaceId(&operation);
    uint64_t resourceId = Operation_getResourceId(&operation);
    uint64_t expectedRevision = Operation_getExpectedRevision(&operation);
    bool valid = Operation_isValid(&operation);
    bool equal = Operation_equals(&operation, &operation);







    return 0;
}
```

## SeshClient class (client.c)

```c
#include "lang/client.h"

int main(void)
{
    SeshClient client = SeshClient();
    bool idSet = SeshClient_setId(&client, 7u);
    uint64_t id = SeshClient_getId(&client);

    return 0;
}
```

## Workspace class (workspace.c)

```c
#include "lang/workspace.h"

int main(void)
{
    Workspace workspace = Workspace();
    bool idSet = Workspace_setId(&workspace, 22u);
    bool principalIdSet = Workspace_setPrincipalId(&workspace, 7u);
    uint64_t id = Workspace_getId(&workspace);
    uint64_t principalId = Workspace_getPrincipalId(&workspace);


    return 0;
}
```

## Resource class (resource.c)

```c
#include "lang/resource.h"

int main(void)
{
    Resource resource = Resource();
    bool idSet = Resource_setId(&resource, 31u);
    bool workspaceIdSet = Resource_setWorkspaceId(&resource, 22u);
    bool revisionSet = Resource_setRevision(&resource, 0u);
    uint64_t id = Resource_getId(&resource);
    uint64_t workspaceId = Resource_getWorkspaceId(&resource);
    uint64_t revision = Resource_getRevision(&resource);



    return 0;
}
```

## AuthService class (auth_service.c)

```c
#include "lang/auth_service.h"

int main(void)
{
    AuthService service = AuthService();
    bool contextSet = AuthService_setContext(&service, nullptr);
    const ApiAuth *authView = AuthService_getAuth(&service);
    AuthServiceVerifyFn verifier = AuthService_getVerifier(&service);
    void *context = AuthService_getContext(&service);
    uint64_t principalId = AuthService_getPrincipalId(&service);
    bool authenticated = AuthService_isAuthenticated(&service);
    AuthService_revoke(&service);





    return 0;
}
```

## Operations class (operations.c)

```c
#include "lang/operations.h"

int main(void)
{
    OperationsSlot slots[8];
    Operations ledger = Operations(slots, 8u);
    Operation operation = Operation();
    Resource resource = Resource();
    bool storageReserved = Operations_reserve(&ledger, slots, 8u);
    int addStatus = Operations_add(&ledger, &operation);
    bool applied = Operations_isApplied(&ledger, 7u, 9u);
    int applyStatus = Operations_apply(&ledger, &operation, &resource);
    size_t count = Operations_getCount(&ledger);
    size_t capacity = Operations_getCapacity(&ledger);
    Operations_clear(&ledger);



    return 0;
}
```

## SeshSnapshot class (snapshot.c)

`SeshSnapshot_setProvider`, `SeshSnapshot_queue`, and `SeshSnapshot_step`
require a non-null provider callback. The one-main call example does not define
a callback helper, so those calls are an explicit callback-shape gap; passing
`nullptr` would only demonstrate rejection. The bounded string projections
remain destination-based migration gaps.

```c
#include "snapshot/snapshot.h"

int main(void)
{
    uint8_t storage[256];
    SeshSnapshot snapshot = SeshSnapshot();
    bool bufferSet = SeshSnapshot_setBuffer(&snapshot, storage, sizeof storage);
    bool retryPolicySet = SeshSnapshot_setRetryPolicy(&snapshot, 1000u, 3u);
    const uint8_t *buffer = SeshSnapshot_getBuffer(&snapshot);
    size_t capacity = SeshSnapshot_getCapacity(&snapshot);
    size_t length = SeshSnapshot_getLength(&snapshot);
    HavenSnapshotPutFn provider = SeshSnapshot_getProvider(&snapshot);
    void *context = SeshSnapshot_getContext(&snapshot);
    uint64_t key = SeshSnapshot_getKey(&snapshot);
    uint64_t nextAttemptMs = SeshSnapshot_getNextAttemptMs(&snapshot);
    uint64_t retryDelayMs = SeshSnapshot_getRetryDelayMs(&snapshot);
    uint32_t attempts = SeshSnapshot_getAttempts(&snapshot);
    uint32_t maxAttempts = SeshSnapshot_getMaxAttempts(&snapshot);
    int state = SeshSnapshot_getState(&snapshot);
    SeshSnapshot_cancel(&snapshot);











    return 0;
}
```

## Sesh class (sesh.c)

The two bounded string projections still require caller-provided output
destinations, so they are migration gaps under the value-return rule.
`Sesh_submit` requires a configured API Haven credential and a non-null trusted
verifier callback before the operation can be meaningfully admitted. Since the
`ApiAuth(...)` constructor macro is missing and this one-main call reference
does not define a callback helper, submit remains an explicit configuration
gap; this example only shows valid composition and binding calls.

```c
#include "lang/sesh.h"

int main(void)
{
    OperationsSlot slots[8];
    AuthService auth = AuthService();
    SeshClient client = SeshClient();
    Workspace workspace = Workspace();
    Resource resource = Resource();
    Operations operations = Operations(slots, 8u);
    Sesh session = Sesh();
    bool authServiceSet = Sesh_setAuthService(&session, &auth);
    bool clientSet = Sesh_setClient(&session, &client);
    bool workspaceSet = Sesh_setWorkspace(&session, &workspace);
    bool resourceSet = Sesh_setResource(&session, &resource);
    bool operationsSet = Sesh_setOperations(&session, &operations);
    AuthService *authService = Sesh_getAuthService(&session);
    SeshClient *clientView = Sesh_getClient(&session);
    Workspace *workspaceView = Sesh_getWorkspace(&session);
    Resource *resourceView = Sesh_getResource(&session);
    Operations *operationsView = Sesh_getOperations(&session);
    Sesh_close(&session);






    return 0;
}
```

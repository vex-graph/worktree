# harness — Function Calls

Grounded per-file call reference for the implemented local metadata classes.
Callbacks and model/provider execution are outside these examples.

## Space helper functions (support.h)

`Space_nameValid` returns its value directly. `Space_format` and `Space_quote`
write into caller-provided destination buffers, so they remain Value Return Law
migration gaps.

```c
#include "space/support.h"

int main(void)
{
    bool validName = Space_nameValid("developer-handle-goes-here");
    return 0;
}
```

## Task class (task.c)

`Task_delegate` currently writes a second `Task` through an output pointer.
`Task_toString` and `Task_toStringStruct` fill caller-owned buffers. These are
Value Return Law migration gaps.

```c
#include "space/task.h"

int main(void)
{
    Task task = Task(101u, 22u, 7u, 7u, 0u);
    bool started = Task_start(&task, 7u);
    bool finished = Task_finish(&task, 7u);
    bool cancelled = Task_cancel(&task);
    uint64_t id = Task_getId(&task);
    uint64_t channelId = Task_getChannelId(&task);
    uint64_t requesterId = Task_getRequesterId(&task);
    uint64_t assigneeId = Task_getAssigneeId(&task);
    uint64_t parentId = Task_getParentId(&task);
    uint64_t permissions = Task_getPermissions(&task);
    uint32_t state = Task_getState(&task);







    return 0;
}
```

## Message class (message.c)

`Message_toString` and `Message_toStringStruct` fill caller-owned buffers and
are Value Return Law migration gaps.

```c
#include "space/message.h"

int main(void)
{
    const char messageText[] = "message-text-goes-here";
    Message message = Message(501u, 22u, 7u, 101u,
        messageText, sizeof messageText - 1u);
    uint64_t id = Message_getId(&message);
    uint64_t channelId = Message_getChannelId(&message);
    uint64_t authorId = Message_getAuthorId(&message);
    uint64_t taskId = Message_getTaskId(&message);
    const char *text = Message_getText(&message);
    size_t length = Message_getLength(&message);






    return 0;
}
```

## ModelUser class (model_user.c)

`ModelUser_toString` and `ModelUser_toStringStruct` require caller-provided
output buffers and are Value Return Law migration gaps.

```c
#include "space/model_user.h"

int main(void)
{
    ModelUser empty = ModelUser();
    ModelUser persona = ModelUser(9001u, "assistant-handle-goes-here", 42u);
    bool nameSet = ModelUser_setName(&persona, "renamed-assistant-handle");
    bool modelIdSet = ModelUser_setModelId(&persona, 43u);
    uint64_t id = ModelUser_getId(&persona);
    const char *name = ModelUser_getName(&persona);
    uint64_t modelId = ModelUser_getModelId(&persona);




    return 0;
}
```

## Channel class (channel.c)

`Channel_toString` and `Channel_toStringStruct` require caller-provided output
buffers and are Value Return Law migration gaps.

```c
#include "space/channel.h"

int main(void)
{
    Channel empty = Channel();
    Channel channel = Channel(17u, 9001u);
    uint64_t id = Channel_getId(&channel);
    uint64_t serverId = Channel_getServerId(&channel);
    uint64_t modelUserId = Channel_getModelUserId(&channel);




    return 0;
}
```

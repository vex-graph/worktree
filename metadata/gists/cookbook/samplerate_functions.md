# Samplerate — public call reference

## AudioBuffer class (audio_buffer.c)

`AudioBuffer_toString` and `AudioBuffer_toStringStruct` still fill
caller-provided buffers; they are Value Return Law migration gaps.

```c
#include "audio/audio_buffer.h"
#include "audio/audio_format.h"

int main(void)
{
    AudioBuffer *buffer = AudioBuffer(512u, AUDIO_CHANNELS_STEREO, 48000.0);
    bool resized = AudioBuffer_resize(buffer, 256u);
    AudioBuffer_clear(buffer);
    const float *constData = AudioBuffer_getConstData(buffer);
    float *data = AudioBuffer_getData(buffer);
    uint32_t frames = AudioBuffer_getFrames(buffer);
    uint32_t capacity = AudioBuffer_getCapacity(buffer);
    uint32_t channels = AudioBuffer_getChannels(buffer);
    double sampleRate = AudioBuffer_getSampleRate(buffer);
    AudioBuffer_setChannels(buffer, AUDIO_CHANNELS_MONO);
    AudioBuffer_setSampleRate(buffer, 44100.0);
    bool isValid = AudioBuffer_isValid(buffer);







    AudioBuffer_free(buffer);
    return 0;
}
```

## AudioFormat class (audio_format.c)

`AudioFormat_toString` and `AudioFormat_toStringStruct` still fill
caller-provided buffers; they are Value Return Law migration gaps.

```c
#include "audio/audio_format.h"

int main(void)
{
    AudioFormat *format = AudioFormat(48000.0, AUDIO_CHANNELS_STEREO);
    AudioFormat_setSampleRate(format, 44100.0);
    AudioFormat_setChannels(format, AUDIO_CHANNELS_MONO);
    AudioFormat_setFramesPerBlock(format, 256u);
    AudioFormat_setSampleType(format, AUDIO_SAMPLE_F32);
    double sampleRate = AudioFormat_getSampleRate(format);
    uint32_t channels = AudioFormat_getChannels(format);
    uint32_t framesPerBlock = AudioFormat_getFramesPerBlock(format);
    uint32_t sampleType = AudioFormat_getSampleType(format);
    bool isValid = AudioFormat_isValid(format);





    AudioFormat_free(format);
    return 0;
}
```

## AudioMemory functions (audio_memory.c)

```c
#include "core/audio_memory.h"
#include "oop/type.h"

int main(void)
{
    MemoryArena *arena = AudioMemory_arena();
    void *block = AudioMemory_alloc(TYPE_AUDIO_BUFFER, 256u);
    block = AudioMemory_realloc(block, 512u);
    AudioMemory_free(block);
    void *scratch = AudioMemory_scratch(TYPE_AUDIO_BUFFER, 128u);
    AudioMemory_resetScratch();


    AudioMemory_shutdown();
    return 0;
}
```

## AudioStream functions (audio_stream_stub.c)

The stub backend always rejects opening the stream. `AudioStream_toString` and
`AudioStream_toStringStruct` still take caller-provided output buffers, so they
are Value Return Law migration gaps. `AudioStreamConfig` has no preferred
`AudioStreamConfig(...)` constructor macro; its configured
`AudioStream(&config)` overload and the legacy `AudioStreamConfig_default()`
factory remain constructor ergonomics gaps.

```c
#include "stream/audio_stream.h"

int main(void)
{
    AudioStream *stream = AudioStream();
    bool opened = AudioStream_open(stream);
    bool started = AudioStream_start(stream);
    bool stopped = AudioStream_stop(stream);
    bool isRunning = AudioStream_isRunning(stream);
    double sampleRate = AudioStream_getSampleRate(stream);
    uint32_t channels = AudioStream_getChannels(stream);
    uint32_t framesPerBlock = AudioStream_getFramesPerBlock(stream);
    double latencyMs = AudioStream_getLatencyMs(stream);





    AudioStream_free(stream);
    return 0;
}
```

## AudioStream functions (audio_stream_cocoa.m)

`AudioStream_toString` and `AudioStream_toStringStruct` still take
caller-provided output buffers, so they are Value Return Law migration gaps.
The remaining stream operations are shown with direct value-returning getters.
The configured constructor overload and legacy `AudioStreamConfig_default()`
factory remain gaps because `AudioStreamConfig` has no
`AudioStreamConfig(...)` constructor macro.

```c
#include "stream/audio_stream.h"

int main(void)
{
    AudioStream *stream = AudioStream();
    bool opened = AudioStream_open(stream);
    bool started = AudioStream_start(stream);
    bool stopped = AudioStream_stop(stream);
    bool isRunning = AudioStream_isRunning(stream);
    double sampleRate = AudioStream_getSampleRate(stream);
    uint32_t channels = AudioStream_getChannels(stream);
    uint32_t framesPerBlock = AudioStream_getFramesPerBlock(stream);
    double latencyMs = AudioStream_getLatencyMs(stream);





    AudioStream_free(stream);
    return 0;
}
```

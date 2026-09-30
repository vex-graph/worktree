# How JSON Works in vexspoke

> Answers: **"How do we parse JSON without allocating?"**
> Answer: **Caller provides a fixed node pool + scratch arena. Parser
> fills them. No malloc, no failure to allocate.**

---

## 1. The Contract

`Json_parse` takes:
- A `JsonDoc` (the document handle)
- A `JsonNode[]` pool (caller-owned, fixed size)
- A `char[]` scratch (caller-owned, for decoded escape sequences)
- The input text

If the document doesn't fit (too many nodes, scratch overflow), the
parse reports `ok = false` and stops. It never allocates, never
reallocates, never fails silently.

---

## 2. The Node Pool

Each `JsonNode` is 32 bytes:
```c
JsonNode {
    JsonType type;      // NULL/FALSE/TRUE/NUMBER/STRING/ARRAY/OBJECT
    JsonRef child;      // first element/member (index into pool)
    JsonRef next;       // next sibling
    uint32_t offset;    // string/key start (in src, or scratch)
    uint32_t length;    // string/key length (decoded)
    bool inScratch;     // true when offset points into decode arena
    double number;      // JSON_NUMBER payload
}
```

Unescaped strings are views into the input text (pointer-stable).
Escaped strings decode into the scratch arena.

---

## 3. Navigation

```c
JsonRef root = Json_root(&doc);
JsonRef val = Json_member(&doc, root, "key");     // object lookup
JsonRef item = Json_at(&doc, arrayRef, 0);        // array index
double num = Json_number(&doc, val);               // number value
const char *str = Json_string(&doc, val, &len);    // string value
bool exists = Json_has(&doc, root, "key");         // existence check
JsonRef deep = Json_path(&doc, root, "a.b[0].c"); // dotted path
```

`Json_path` provides lodash-like dotted path lookup. Max parse
depth: 24.

---

## 4. The Writer

```c
char buf[4096];
JsonWriter w;
JsonWriter_init(&w, buf, 4096);
Json_beginObject(&w);
Json_addKey(&w, "name");
Json_stringVal(&w, "vex");
Json_addKey(&w, "version");
Json_numberVal(&w, 1.0);
Json_endObject(&w);
// buf now contains: {"name":"vex","version":1}
```

The writer builds into a caller byte buffer. Overflow flips `ok` once
and later calls no-op. The caller checks `JsonWriter_ok(&w)` after
building.

---

## 5. Key Insight

JSON in vexspoke is the same pattern as everything else: caller owns
the memory, parser fills it, no hidden allocation. This is critical
for hot-loading (manifests), network protocols (REST/MCP), and
configuration — all paths where allocation failure is not an option.

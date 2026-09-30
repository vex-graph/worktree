# The toString Law — Implementation Plan

> Status: DRAFT (`;;DRAFT`). Universal law (#37). This is the plan; no code yet.
> Binds: the Dest-Last Law, the Cold-Strict, Hot-Minimal Validation Law
> (Truncation-Never-Silent clause), the Living `;;OVERVIEW` & `;;DEFINITION`
> Blueprint Law, the Symmetric Getter/Setter Completeness Law, the Living
> Preferences Law, the Arity and Constructive Convenience Law.

---

## 1. Purpose

Every object in the ecosystem must be able to render itself as a string — for
debugging, logs, telemetry, and **AI-readable state** (an agent dumps any object
and reads its fields). The law gives every class two bounded string projections
with one uniform signature.

---

## 2. The law (text for `preferences.md` #37)

### Definition:
Every class across the ecosystem ships **two bounded string projections**:

1. **`Class_toString(self, dest, cap, outTruncated)`** — the **VALUE** string: a
   concise, class-specific summary of the object's state.
2. **`Class_toStringStruct(self, dest, cap, outTruncated)`** — the **STRUCTURE**
   string: a recursive, by-name dump of the object's fields.

Both are bounded (dest-last + a truncation flag) and cold-path only.

### The Why:
Every object has a string, and today each subsystem invents its own ad-hoc
printing — un-greppable, un-cappable, and unusable by an agent. A single uniform
pair makes state legible everywhere (a debugger's `po`, a log line, an agent's
context). And the struct dump **mirrors the `;;OVERVIEW` STRUCT FIELDS** block, so
the two enforce each other: a field added without updating the dump is a defect,
exactly like a stale overview.

### The Rule:
1. **Every public class ships both.** No class is string-blind.
2. **Signature is fixed:** `(const Class *self, char *dest, size_t cap, bool *outTruncated)` — dest-last (the Dest-Last Law), bounded, truncation flagged (the Cold-Strict, Hot-Minimal Validation Law).
3. **Null-safe:** a null `self` writes a safe default (`"(null)"`), never crashes.
4. **Cold-path only:** never called on a frame — it formats (and may allocate).
5. **`toStringStruct` mirrors the `;;OVERVIEW` STRUCT FIELDS** — same fields, same declaration order.
6. **Nesting recurses:** a parent's dump calls each child's `toStringStruct`.
7. **The formatter fuses here:** the `{object}` placeholder of the Label formatter calls `toString`.

---

## 3. The signature (fixed, both verbs)

```c
void Class_toString(const Class *self, char *dest, size_t cap, bool *outTruncated);
void Class_toStringStruct(const Class *self, char *dest, size_t cap, bool *outTruncated);
```

- `dest` / `cap`: the bounded destination (dest-last per the Dest-Last Law).
- `outTruncated`: set true when the output was cut (the Truncation-Never-Silent
  clause) — the caller degrades loudly.
- Return `void`: the result is the written buffer; failure is a truncation flag,
  not an error code (a string is best-effort).

---

## 4. The helper — a bounded string builder (vexspoke R2)

Hand-rolling bounds checks in every class is the defect this law would create.
So a tiny **bounded builder** carries the bound once:

```c
// vexspoke lang/str.h (R2) — the bounded string builder
typedef struct Str {
    char  *dest;       // the destination buffer (borrowed)
    size_t cap;        // total capacity
    size_t len;        // bytes written so far
    bool   truncated;  // a write was cut
} Str;

void Str_init(Str *s, char *dest, size_t cap);
void Str_put(Str *s, const char *text);              // append, bounded
void Str_putc(Str *s, char c);
void Str_printf(Str *s, const char *fmt, ...);       // bounded printf (cold)
bool Str_isTruncated(const Str *s);
```

Every class's `toStringStruct` builds through one `Str`, then reports
`Str_isTruncated` into `outTruncated`. One bound, one truncation flag.

---

## 5. The class template (what every class writes)

```c
;;OVERVIEW
// ... STRUCT FIELDS:
//   float x, y, w, h;      // ...
//   uint32_t color;        // ...

void Panel_toStringStruct(const Panel *self, char *dest, size_t cap, bool *outTruncated) {
    Str s;
    Str_init(&s, dest, cap);
    if (self == nullptr) {
        Str_put(&s, "(null)");
        if (outTruncated) *outTruncated = false;
        return;
    }
    Str_put(&s, "Panel { ");
    Str_printf(&s, "name: \"%s\", ", Component_getName(&(*self).component));
    Str_printf(&s, "color: 0x%08X, ", Panel_getColor(self));
    Str_printf(&s, "abs: (%.1f, %.1f, %.1f, %.1f)", Panel_getAbsX(self), ...);
    Str_put(&s, " }");
    if (outTruncated) *outTruncated = Str_isTruncated(&s);
}
```

The field list here **is** the overview's STRUCT FIELDS — same order, same names.

---

## 6. The two projections — value vs structure

- **`toString`** = the VALUE — concise, class-specific: `Panel("root")`,
  `Image(64x64)`, `Vec4(1, 2, 3, 4)`.
- **`toStringStruct`** = the STRUCTURE — the full recursive field dump:
  `Window { title: "…", panels: { Panel { … }, Panel { … } } }`.

`toString` is what a log line wants; `toStringStruct` is what a debugger/agent
wants. A class may implement `toString` in terms of its key fields and
`toStringStruct` as the complete dump.

---

## 7. Migration — class-by-class, same-cycle (not a big-bang sweep)

Per the Living Preferences Law, a class gains both verbs **in the commit that
next touches it** (the Per-Repo Preferences Extension Law keeps each repo's
mirror current). The law lands in the constitution now; the classes follow as
they are touched, plus a **first batch** to prove the pattern.

**First batch (graphvex — the classes we just built):**
1. `Transform` (2×3 affine — the simplest; proves the pattern).
2. `GraphicsComponent` (many fields; proves the dump mirrors the overview).
3. `Component` (recurses into children — proves nesting).
4. `Panel` (wraps Component — proves the wrapper forwards).
5. `Image`, `Device`, `Filter` (the rest of the language).

**Then:** vexspoke primitives (`Vec2/3/4`, `Mat4`, arenas), hotcwap (`Window`,
`Kernel`), darling (`Frame`, widgets), api-haven.

---

## 8. Relationship to the Label formatter (the fusion)

The Label's `{variableName}` / `%d` formatter (planned next) has a `{object}`
placeholder that resolves by calling the object's **`toString`**. So the toString
Law is the substrate the formatter stands on — which is why it lands first.

---

## 9. Resolved decisions

1. **Null self** writes `"nullptr"`.
2. **ONE LAYER, no recursion.** `toStringStruct` dumps only THIS class's fields. A
   nested object field renders via that object's **`toString`** (the value), never
   its `toStringStruct` — so depth is bounded by design and no recursion guard is
   needed. (A class that *wants* a deeper view calls the child's `toStringStruct`
   itself.)
3. **Escape** — strings are emitted quoted + escaped (`\n`, `\t`, `\"`, `\\`) via
   a `Str_putQuoted` helper.
4. **Builder home:** vexspoke `lang/str.h` (R2, shared).
5. **Buffer only** — no heap `toStringAlloc`; the bounded form is the law.
6. **Law #37, Tier 2** (Semantics/Contracts).

## 10. The one-layer rule (rule 6, revised)

```c
// Component_toStringStruct — ONE LAYER: this component's fields only.
// A child element renders via its own toString (a one-line value), never by
// recursing into the child's toStringStruct.
Component { name: "root", type: 0x…, parent: nullptr, graphics: 2, children: 1 }
```


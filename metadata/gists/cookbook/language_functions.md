# Language — public call reference

## SourceRange class (source_range.c)

```c
#include "document/source_range.h"

int main(void)
{
    SourceRange empty = SourceRange_zero();
    SourceRange document = SourceRange(42u);
    SourceRange range = SourceRange(42u, 120u, 160u);
    SourceRange zeroRange = SourceRange();
    SourceRange_setDocumentId(&range, 43u);
    SourceRange_setStartByte(&range, 121u);
    SourceRange_setEndByte(&range, 161u);
    bool isValid = SourceRange_isValid(&range);
    uint32_t documentId = SourceRange_getDocumentId(&range);
    uint64_t startByte = SourceRange_getStartByte(&range);
    uint64_t endByte = SourceRange_getEndByte(&range);






    return 0;
}
```

## Token class (token.c)

```c
#include "token/token.h"

int main(void)
{
    SourceRange range = SourceRange(7u, 24u, 32u);
    Token empty = Token_zero();
    Token identifier = Token(TOKEN_KIND_IDENTIFIER);
    Token token = Token(TOKEN_KIND_KEYWORD, range);
    Token zeroToken = Token();
    Token_setKind(&token, TOKEN_KIND_OPERATOR);
    Token_setRange(&token, range);
    TokenKind kind = Token_getKind(&token);
    SourceRange tokenRange = Token_getRange(&token);




    return 0;
}
```

## Reference class (reference.c)

```c
#include "semantic/reference.h"

int main(void)
{
    SourceRange range = SourceRange(7u, 40u, 48u);
    Reference empty = Reference_zero();
    Reference identity = Reference(9001u);
    Reference reference = Reference(9001u, range, REFERENCE_ROLE_CALL, true);
    Reference zeroReference = Reference();
    Reference_setTargetSymbolId(&reference, 9002u);
    Reference_setRange(&reference, range);
    Reference_setRole(&reference, REFERENCE_ROLE_READ_WRITE);
    Reference_setResolved(&reference, false);
    uint64_t targetSymbolId = Reference_getTargetSymbolId(&reference);
    SourceRange referenceRange = Reference_getRange(&reference);
    ReferenceRole role = Reference_getRole(&reference);
    bool isResolved = Reference_isResolved(&reference);






    return 0;
}
```

## Symbol class (symbol.c)

```c
#include "semantic/symbol.h"

int main(void)
{
    SourceRange range = SourceRange(7u, 12u, 22u);
    Symbol empty = Symbol_zero();
    Symbol identity = Symbol(9001u);
    Symbol symbol = Symbol(9001u, 77u, SYMBOL_KIND_FUNCTION, "function-name-goes-here", range);
    Symbol zeroSymbol = Symbol();
    Symbol_setId(&symbol, 9002u);
    Symbol_setScopeId(&symbol, 78u);
    Symbol_setKind(&symbol, SYMBOL_KIND_METHOD);
    Symbol_setName(&symbol, "method-name-goes-here");
    Symbol_setDeclarationRange(&symbol, range);
    uint64_t symbolId = Symbol_getId(&symbol);
    uint64_t scopeId = Symbol_getScopeId(&symbol);
    SymbolKind kind = Symbol_getKind(&symbol);
    const char *name = Symbol_getName(&symbol);
    SourceRange declarationRange = Symbol_getDeclarationRange(&symbol);







    return 0;
}
```

## DiffAdapter functions (diff_adapter.c)

`DiffAdapter_classifyLine` requires caller-provided state and token output
destinations. It is a migration gap under the value-return rule, so this file
has no compliant API call to show yet.

```c
int main(void)
{
    return 0;
}
```

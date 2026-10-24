# Func — Personal Standalone Compile-Time Tool

Not an extra R tier. This checkout borrows no ecosystem headers/runtime. The
first literal compiler is implemented; general orchestration remains unfinished.
Current evidence is scoped in the shared `tests/test-checklist.md`, not a blanket
production-readiness claim. No repository push is implied by this matrix.

| Feature | Status | Scope / proof / gaps |
| :--- | :---: | :--- |
| Literal opcode decoder and native source emitter | 🟧 | `src/func.c`; numeric/surface add=1/arity2, mul=2/arity2, print=3/arity1; flat growable rows, int64 literal checks and checked native arithmetic. `../../../tests/func/src/func_test.py`: actual native output/order, invalid arity/IDs/ranges/NUL, growth/recovery, C ASan/UBSan. OOM fault injection/leak accounting/non-host runtimes remain unproved. |
| Build-only launcher | 🟧 | `func`; explicit Clang invocation, caller stage deadlines, simultaneous capped pipes, kill/reap, private cleanup and prior-artifact preservation. Real build and failure/timeout/output tests above; never implicitly runs. Trusted compiler/parent, no malicious detached-process sandbox proof. |
| Extensible opcode registry / references / control flow / general orchestration | ⬜ | Vital future work; current three literal IDs are not an extensible registry or general tool language. No public FuncProgram/FuncRuntime classes are implemented. |

Platform scope: macOS arm64 lab, strict C23 `-Wall -Wextra -Werror`; C decoder
ASan/UBSan with leak detection disabled. macOS 14 runtime, Linux/Windows and full
backend-trust/exhaustion instrumentation remain gaps. `../../../tests/func/readme_test.py`
mechanically reviews competency against current source; it is not runtime proof.

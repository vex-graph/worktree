# Test Preferences Charter — Implementation Plan

**Status:** `;;RESOLVED` — no retoken needed. The 34 stale `test-preferences.md` references were
**uncommitted working-tree edits** (the mangled reverts), never part of any commit. Discarding them
removed the drift: `ecosystem/` now references `preferences.md` everywhere and zero times references
`test-preferences.md`. The token disambiguation this plan proposed is therefore already satisfied by
the committed state.
**Scope:** keep the tests repo's `test-preferences.md` as the home of its substantive testing
laws; disambiguate references that incorrectly use that name for the universal constitution.
**Universal architecture:** `ecosystem/vexspoke/preferences.md` remains authoritative.

---

## 1. Background — what was actually butchered

The current documents contain an unresolved naming collision (see
[`per-repo-preferences-overhaul-plan.md`](per-repo-preferences-overhaul-plan.md)):

1. The constitution lives at `ecosystem/vexspoke/preferences.md`, but some prose still calls it
   `test-preferences.md`.
2. `tests/test-preferences.md` is a separate document of substantive testing laws.

The result: the token `test-preferences.md` now denotes **two different documents** depending on
the file. This is a live *Zero Drift* violation of the **Living Preferences Law** — the
constitution's own text calls a file by the wrong name.

### The user's decision

- **Keep the name** `test-preferences.md` in the existing `vexgraph-ecosystem/tests` repository.
- **Keep the testing laws in that document.** “Laws” means its multiple substantive test laws,
  not laws about the existence, precedence, citation, or synchronization of that document.
- **Do not add meta-laws** to the constitution or a `;;SYNC` annotation to the tests document.

Because the name stays, the only way to remove the ambiguity is to make the token mean exactly one
thing: **scrub every stale use that means the supreme law.** That is the spine of this plan.

---

## 2. Evidence — the 34 stale references

Grep-provable: `grep -rn "test-preferences" .` currently returns **34** hits that mean *the supreme
constitution* and must become `preferences.md`:

| Location | Count | Lines | Meaning today | Action |
| :--- | :-- | :--- | :--- | :--- |
| `ecosystem/vexspoke/preferences.md` | 7 | Living Preferences Law (defn + rule 1), Conflict Triage Law (protocol 4), No Section Sign Law (rule 3), Per-Repo Preferences Extension Law (defn + rules 1, 5) | supreme law | retoken to `preferences.md` |
| `ecosystem/*/<repo>-preferences.md` | 9 | line 9 each: "All universal laws in `test-preferences.md` are mandatory" | supreme law | retoken to `preferences.md` |
| `ecosystem/*/CONTRIBUTING.md` | 18 | heading "Supreme Living Document: `test-preferences.md` ..." + the same-cycle "Whenever preferences..." line | supreme law | retoken to `preferences.md` |

The single genuine use of the token — the charter itself at `tests/test-preferences.md` — stays.

### The tell

`ecosystem/vexspoke/CONTRIBUTING.md` line 47 is the fingerprint of the half-done rename:

```md
Whenever preferences or conventions evolve, [`test-preferences.md`](preferences.md) ...
```

Link **text** says `test-preferences.md`; link **target** says `preferences.md`. The rename moved the
target and forgot the label. (The No Section Sign Law warning about `->` applies to the C in these
docs; the markdown link is safe, the *word* is the defect.)

---

## 3. Goal — distinct documents, distinct roles

Keep these documents distinct without inventing a new governance layer:

| Document | Role | Repository |
| :--- | :--- | :--- |
| `preferences.md` | universal architectural preferences | `vexspoke` |
| `<repo>-preferences.md` | existing repo-specific preferences | individual repos |
| `test-preferences.md` | substantive laws for test proof | `vexgraph-ecosystem/tests` |

### End-state contract

- Every `test-preferences.md` in the ecosystem means **the Test Proof Charter** — nothing else.
- Every reference to the supreme law says **`preferences.md`** — nothing else.
- The tests document retains its substantive testing laws. No new Law Index, synchronization
  annotation, or meta-law is required. Its existing introduction already points to
  `ecosystem/vexspoke/preferences.md` for universal architecture.

---

## 4. Exact edits (per repo, upstream-first)

If the cross-repo cleanup is approved, perform it upstream-first (**vexspoke →
graphvex/api-haven/language/darkbase → hotcwap → darling-framework/sesh → samplerate**).
`tests/` is now its own repo; the umbrella root has no remote. Never push without instruction.

### Phase 0 — preparation
- [x] Write this plan at `_docs/misc/test-preferences-charter-plan.md`.
- [x] Clone `vexgraph-ecosystem/tests` into the existing `tests/` non-destructively;
  remote scaffold tracked and existing local suite content still untracked.

### Phase 1 — vexspoke (constitution; the model)
1. Retoken the 7 stale `test-preferences.md` → `preferences.md` in `preferences.md`
   (Living Preferences Law, Conflict Triage Law, No Section Sign Law, Per-Repo Preferences Extension Law).
2. Update `ecosystem/vexspoke/CONTRIBUTING.md`: retoken heading + same-cycle line
   (`test-preferences.md` → `preferences.md`). Do not add new constitutional laws.
3. Verify changes; consider a repo-local commit only after approval.

### Phase 2 — R3 drivers (4 repos, upstream order)
- [ ] `graphvex`, `api-haven`, `language`, `darkbase`: retoken `<repo>-preferences.md` line 9 and
  the two `CONTRIBUTING.md` refs each; commit per repo.

### Phase 3 — R1 host + R4 (3 repos)
- [ ] `hotcwap`, `darling-framework`, `sesh`: same retoken + per-repo commit.

### Phase 4 — R5 (1 repo)
- [ ] `samplerate`: same retoken + per-repo commit.

### Phase 5 — tests repo (separate scope)
- [ ] Preserve `tests/test-preferences.md` as the tests repo's root preferences document.
  Its opening already links the universal architecture; leave its laws intact for a separate,
  substantive review. Do not add `;;SYNC`, a Law Index, or meta-laws.
- [ ] Decide separately whether/when to track the currently untracked suite and charter in the
  tests repo. Do not silently add or commit the entire test tree as part of a docs-reference fix.

### Phase 6 — verify & report
- [ ] Review `test-preferences.md` references: none calls it the supreme constitution.
- [ ] Inspect each touched repo's diff and status; no `git push` (the No Auto-Pushing Law).

---

## 5. Deferred decisions

- Should `tests/test-preferences.md` itself be revised for tone or scope? That is a separate
  review of the substantive test laws, not a reason to add laws about laws.
- The **Test Segregation Law** currently says `_tests/` while the tree is `tests/`.
  Check build wiring and repository expectations before changing that law.
- Decide whether to commit the pre-existing untracked suite into the tests repo, and in what
  cohesive units. This plan does not authorize bulk staging or a push.

---

## 7. Verification

- Docs-only: no `cmake --build` wiring changes; `-Wall -Wextra -Werror` builds stay green per repo.
- Grep-provable: zero stale `test-preferences.md` tokens that mean the supreme law; surviving
  uses refer to the tests repo's preferences.
- Style: zero `->` in C snippets, zero section-sign glyphs, correct cast/decl spacing in embedded code,
  Titles only (the **No Arrow Sugar Law**, **No Section Sign Law**, **Law Identity Doctrine**).
- The tests document retains its existing architecture link and carries no `;;SYNC` token.

---

*Deliverable of this cycle: this plan artifact only. Approval required before Phase 1 execution.*

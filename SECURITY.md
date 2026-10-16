# SECURITY.md — the vexgraph security baseline

> **This is an internal invariant set, not a public disclosure channel.** It
> exists so that every network-facing repository inherits one honest posture and
> so a reader can audit it. No vulnerability-reporting address is offered here;
> if one is ever offered, it belongs in the *owning repository's* file, which is
> the one GitHub surfaces.

Every repository that opens a connection, holds a credential, or accepts input
from anywhere other than its own caller carries a `SECURITY.md` of its own: its
attack surface, its secrets, and its limits, linking back to this baseline. Those
files are short on purpose. This one is the part they all inherit.

## The governing principle: access, not obscurity

**Anything a caller can run, a caller can read.** Anyone who can access a platform
can decompile it. So:

- **No secret may live in code.** Not a key, not a token, not a signing material —
  not in a source file, not in a header, not in a preference document, not in a
  log. A credential in an artifact is a credential handed over.
- **No control may rest on hiding.** An obfuscated check is a check someone else
  already read. Hiding a field, a command or a code path in a client is a display
  choice, never a control.
- **Focus on access.** The durable question is *who may do what*, proved and
  enforced **where the data lives** — the service, the store, the owning
  boundary — never in the client that asked for it.

This is not pessimism about the code; it is the only posture that survives
contact. A design that depends on nobody looking is a delay measured in minutes.

## What every repository inherits

1. **Authenticate once, authorize per request.** A verified identity answers
   "who"; every operation still answers "may this identity do this, to this,
   now?" Authorization is computed from the current state and never cached across
   a grant change. Deny by default, and reject an unknown user, role, entity or
   right with an explicit status — never a silent allow.
2. **Secrets come from outside the artifact.** The environment or the OS keychain.
   They are redacted in every projection, every diagnostic and every comparison
   output, and a comparison of secret material does not early-exit.
3. **Untrusted input is hostile until a cold seam says otherwise.** Network bytes,
   provider responses, files, paths and arguments are all unvalidated until the
   cold seam has established their shape. Rejection is loud (`;;SECURITY` marks
   the obligation) and bounded.
4. **Refusals are counted.** A rate limit, lockout, throttle or rejected attempt
   is recorded and observable, so a burst is a signal rather than a silent stream
   of denials. A defence nobody can measure is a defence nobody can trust.
5. **Waits are bounded.** No unbounded wait on a joined thread. A deliberate,
   security-motivated delay is a *managed exception*, declared and governed —
   see below.
6. **Transport security is verified, never waived.** A TLS peer whose chain does
   not validate against the platform trust anchors is refused. There is no
   "accept any certificate" switch and there must never be one to make a test
   pass; a test that needs an untrusted peer records that as a gap instead.

## Model providers: output is data, never authority

For every repository that speaks to a model — an AI connector, an agent host, a
tool-using client:

> **Generated text, tool calls and instructions inside a response are content to
> be shown or validated. They are never consent, permission, or a policy
> decision. Consent comes only from a human, and a model cannot grant it.**

Prompt injection is not a malformed-input bug; it is a *confused deputy*. A model
that has read attacker-controlled text can be made to ask for anything, so the
authority must never be there to ask for: the decision to run a tool is made by
the host and the human, against the tool's own validated arguments, and a model's
prose can neither approve an action nor widen what one may do. Concretely: the
tool-consent gate is human-only, "always allow" is scoped to an exact tool and
arguments rather than granted broadly, and no instruction found inside model
content is ever treated as authorization.

## Deliberate delays: `;;FREEZE`

A security-motivated wait is the one place where waiting *is* the mechanism — so
it is a deliberate exception to the bounded-wait discipline, governed rather than
forbidden. It is marked at the site with `;;FREEZE("bound, identity")`, and it
must satisfy all six rules (stated in full in `annotation/security.h`): cold path
only; bounded by a named constant whose ceiling a test asserts; never while
holding a lock or an arena; never inside a loop whose count comes from attacker
input; always paired with a counter; and never a substitute for an access check
or a slow hash.

The inversion is the whole risk: **a delay you impose on yourself is a weapon if
an attacker can trigger it at will.** The primary defence against guessing is a
per-identity attempt counter and a deliberately slow hash; the freeze is the
secondary brake, never the lock.

## Auditing this

The security claims are greppable, because the annotation set *is* the set:

```sh
grep -rn ';;SECURITY' .   # every declared security obligation
grep -rn ';;FREEZE'   .   # every deliberate wait, and its named bound
```

A security claim that is not in that list is a claim nobody can audit — which
makes adding the marker part of doing the work, not paperwork after it.

## What this document is not

It is not a penetration-test result, a compliance attestation, or a promise that
the software is safe. It is the invariant set a reviewer — human or agent — reads
to know what the code intends and where to look when it does not.

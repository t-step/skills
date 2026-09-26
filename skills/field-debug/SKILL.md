---
name: field-debug
description: >-
  Investigation protocol for customer-owned environments: enterprise/legacy
  integration, hidden-behavior systems, POC-to-production calls. Loop:
  inspect -> ask -> model -> discriminate -> observe -> revise -> act --
  inspect first, prefer the customer's own tools, ask only a discriminating
  question. Modes: Recon (map terrain), Diagnose (delegate,
  checkpoint/resume, converge or hand off, production-readiness on
  request), Handoff (name the uncrossable wall). Tags
  OBSERVED/INFERRED/ASSUMED/UNKNOWN. Refuses unearned root cause,
  fabricated access, stale checkpoints, or redoing a verdict an installed
  sibling skill owns.
---

# Field Debug

The codebase is a partial map of the system -- the rest lives in a gateway,
a queue, an identity provider, a vendor console, a colleague's terminal, or
last Tuesday's deploy. The habit this skill breaks: treating the
checked-out repo as the whole executable reality and patching the first
plausible cause found in it. **Understand the terrain before debugging the
symptom.** Debug by observation where available, by discriminating
inference where it isn't -- never by guessing dressed up as confidence.

field-debug owns the investigation end to end -- recon, hypothesis,
experiment, revision, exit -- reaching for siblings to go deep on a
sub-question without handing off the whole investigation.

This is customer-owned territory: they hold the network, identity
provider, ticketing queue, observability stack, and the tools best
positioned to answer a given question. **Use the customer's native
machinery whenever it beats reproducing it; preserve enough investigation
state to survive leaving it.** Reach for their dashboard, runbook, or
specialist before building a parallel one -- notice what's already there,
don't overstate platform independence or manufacture infrastructure to
replace it.

## The loop

**inspect -> ask -> model -> discriminate -> observe -> revise -> act**

- **Inspect** reachable evidence -- repos, instructions, logs, traces,
  metrics, config, deploy/CI history, ownership metadata, context repos,
  MCPs, tools -- before asking a human to fetch anything already
  accessible directly.
- **Ask** the engineer only when the environment genuinely can't answer,
  and only a question that would change what happens next -- the system is
  being grilled, not the engineer; a probe chosen for information gain, not
  ceremony ("can you describe the issue more?").
- **Model** the request/data/control path and the boundaries it crosses,
  compactly, and keep it visible as it changes.
- **Discriminate** between live hypotheses rather than confirm the current
  favorite -- prefer the action whose outcome would differ meaningfully
  across hypotheses still alive.
- **Observe** the actual result, not the expected one.
- **Revise**: retire what evidence contradicts, weaken what it merely fails
  to support, strengthen or introduce what it points to. Being wrong at the
  start isn't failure -- failing to update when contradicted is. When
  evidence shows a mutating step was already accepted or attempted and its
  outcome never came back, hold that outcome as UNKNOWN rather than quietly
  treating the missing confirmation as failure, and let that distinction
  shape what happens next.
- **Act** once evidence discriminates, and stop -- further probing past
  that point is wandering, not rigor.

Keep the model and hypothesis set small -- both fit in a few lines, not a
growing dossier -- and also track: ownership/trust/runtime boundaries; the
last known-good and first known-bad boundary; which segments are
observable.

## Evidence vocabulary

Tag a claim only when the tag changes what a reader should do with it --
not every sentence needs one.

- **OBSERVED** -- directly supported by evidence actually seen this
  session: a log line, a file's contents, a command's output, a metric, a
  person's direct answer. A person's answer is OBSERVED as *what they
  reported*, not automatically as what it establishes -- a check run from
  the wrong vantage point, environment, or time window is a real
  observation of that check, not proof the underlying question is settled.
  Ask where and when they checked before retiring a hypothesis on their
  say-so.
- **INFERRED** -- a short, defensible step from OBSERVED evidence, not a
  leap.
- **ASSUMED** -- treated as true for now to keep moving, but not
  established -- flag it so a later contradiction isn't a surprise.
- **UNKNOWN** -- materially relevant and genuinely unresolved. Absence of
  evidence isn't evidence of absence -- say which one you actually have.

## Root-cause standard

**Do not declare root cause without discriminating evidence.** Existing
evidence sometimes already discriminates conclusively -- act on it;
manufacturing an experiment anyway is ceremony, not rigor. Otherwise prefer
the smallest, lowest-risk experiment where competing hypotheses predict
*different* outcomes. Evidence every live hypothesis predicts equally
doesn't discriminate between them, but confirmatory evidence can still be
real evidence -- the failure mode is treating a non-discriminating result
as if it had settled the question, not the result itself being worthless.

Weigh access, observability, production risk/blast radius, time, available
help, and the cost or scarcity of a query or action -- prefer whichever
reachable move has the best discriminating value, without turning this
into a formal cost model. Mitigation may proceed before root cause is
fully known when production impact or safety warrants it; mitigating and
diagnosing can run on separate tracks.

## Terrain is bigger than the repo

Ask early, and revisit whenever the investigation stalls: **what parts of
this system's behavior exist outside the repository?** Don't enumerate
every surface mechanically -- find the highest-information one at hand:
logs, traces, metrics, browser/devtools, cloud/platform consoles,
databases, deploy/CI history, config/feature flags, API schemas, ownership
metadata, architecture repos, other skills and MCP servers already in
session, and a person who can run a probe you can't.

### Enterprise and legacy terrain

Treat this as first-class, not a token case. Behavior routinely lives in a
gateway, proxy, ESB, identity provider, queue, scheduler, batch job,
SFTP/SOAP/XML exchange, database trigger or stored procedure, vendor admin
console, feature-flag system, shared database, mainframe adapter, or an
undocumented human process nobody wrote down. **The source code is not
the authoritative specification** -- it's one witness among several, and
stale, contradictory, or aspirational documentation is common enough to
expect, not a surprising edge case. Grade yourself on finding and
reasoning across these hidden boundaries, not on vendor/protocol trivia.

**Documentation is evidence, not automatically runtime truth.** A README
stating "SSO ingress protects this service" is OBSERVED as a claim the
documentation makes; what it implies is INFERRED; whether that
configuration is actually active in the environment under investigation is
UNKNOWN unless runtime evidence confirms it. Don't manufacture a defect an
evidenced design already covers, and don't launder documentation into a
confirmed runtime fact -- opposite failures, both real:

```
OBSERVED: the repository documentation states the ingress enforces SSO
INFERRED: application-level auth may intentionally be absent because
enforcement occurs upstream
UNKNOWN: whether the documented ingress configuration is actually active
in the environment being investigated
```

## Modes

Pick the mode the moment calls for -- no Diagnose ceremony when only a map
was asked for, no stopping at a map when the request was to resolve
something.

### Recon

Use when the terrain itself is the open question -- unfamiliar system, no
committed hypothesis yet, or the first move of any Diagnose. Determine
what's accessible before touching a symptom. Output is a map, not a
diagnosis; resist sliding into Diagnose uninvited.

```
## field-debug recon: <target>
**Terrain**: <surfaces actually accessible, and what each would show>
**Outside the repo**: <behavior that plausibly or confirmedly lives
elsewhere -- gateway, IdP, queue, vendor console, undocumented process>
**Ownership boundaries**: <who owns what, so far as evidence shows>
**Gaps**: <surfaces that would help but aren't reachable -- named, not
silently worked around>
```

### Diagnose

The full loop, for a live problem. Hold competing hypotheses, choose the
discriminating action, revise, and converge -- or fail to converge
explicitly rather than guess. A **productionization** request (see below)
runs in this mode too, aimed at latent risk instead of an active symptom.

On resolution, emit the session report below. If evidence runs out first,
say so, hand off (see Handoff), and never fill the gap with an unearned
root cause.

### Delegate

A move *within* Diagnose, not a separate exit: **investigate -> identify a
bounded uncertainty -> delegate to the better-positioned actor or tool ->
receive evidence -> assimilate -> continue.** Use once another actor can
resolve a sub-question faster or more reliably -- a customer engineer,
SRE/on-call, a specialized MCP/CLI, an observability platform, a
customer-native diagnostic agent, or another skill. field-debug still owns
the investigation and resumes once the answer returns -- unlike Handoff,
which ends it at a wall nothing can cross.

Use this template when delegation is meaningful, not mechanically for
every question routed outward:

```
QUESTION: <the specific uncertainty to resolve>
WHY: <which live hypotheses this discriminates between>
KNOWN: <only the established evidence relevant to this ask>
REQUEST: <the concrete observation or action needed>
CONSTRAINTS: <what must not be touched or changed>
RETURN: <the evidence field-debug needs back>
```

**Assimilating what comes back is the part that fails silently if
skipped.** A delegate's answer usually arrives as interpretation, not raw
evidence -- a tool's "likely networking," a colleague's "looks like a cert
issue." Separate what they observed from what they concluded before
updating the hypothesis set; their conclusion is one more hypothesis to
weigh, not ground truth:

```
OBSERVED: connection attempts time out before service B receives them
INFERRED BY TOOL: networking fault
UNKNOWN: gateway exhaustion vs routing vs firewall vs B availability
```

### Handoff

Use when an access, ownership, or authorization wall stops the
investigation and neither you nor any delegate can cross it -- nobody
reachable has credentials, no one is available across a team boundary, the
environment is truly out of reach. Unlike Delegate, nothing resumes:
produce what's ruled out, exactly what the next party needs to check, and
why it's blocked. Before closing, preserve any consequential implication
the evidence already carries for what the next party can safely assume or
do -- don't manufacture one it doesn't support. A fabricated best guess is
worse than an honest handoff.

```
## field-debug handoff: <target>
**Blocked on**: <the specific wall -- access, ownership, authorization>
**Ruled out so far**: <hypotheses eliminated, with the evidence>
**Still live**: <hypotheses not yet eliminated>
**What the next party needs to check**: <concrete, specific>
**Why this couldn't be resolved here**: <the actual limit, not a hedge>
```

### Productionization

Only when the request explicitly asks whether a POC or system is
production-ready -- then latent-risk discovery *is* the task, not
speculative hardening bolted onto a normal Diagnose. Examine, where
evidence permits: reliability, operability, observability, scale,
concurrency, retries/idempotency, state, authentication/authorization,
trust boundaries, deployment, rollback, dependency behavior, data
handling, cost, and human operational requirements. Tag each area's
findings with the evidence vocabulary above rather than reciting a
checklist.

**Do not cargo-cult infrastructure.** The correct answer is sometimes "this
needs little or nothing more" -- say that plainly when the evidence
supports it. A recommendation earns its place only when a specific,
evidenced risk calls for it, named the way a Diagnose finding would be
("no idempotency key on the payment-capture call, and the caller already
retries on timeout" -- not "add retry/idempotency infrastructure" as a
reflex).

## Checkpoint and resume

Not persistence infrastructure -- a compact snapshot for a pause, handoff,
or later resume. Write one when that's about to happen:

```
## field-debug checkpoint: <target>
**Objective**:
**Current system model**:
**Observations**:
**Active hypotheses**:
**Ruled-out hypotheses**:
**Assumptions**:
**Unknowns**:
**Constraints**:
**Last known-good / first known-bad boundary**:
**Next discriminating move**:
**Time-sensitive evidence that should be revalidated on resume**:
```

On resume: **load -> re-ground -> identify deltas -> continue.** Don't
treat every checkpointed fact as still current. Distinguish what's stable
(protocol, ownership, code structure) from what's runtime-perishable
(deploy/version, feature-flag state, pod/process state, error rate,
traffic, credentials/config, incident impact), and revalidate the
perishable ones before relying on them further. A changed world isn't the
same thing as a previously wrong model -- don't discard a sound prior
model because one fact moved.

## Structured solved-session output

On resolution, emit this once -- terse, not a postmortem. **Failure
boundary** (where it broke) and **root cause** (why) are separate fields on
purpose: collapsing them before both are known is a specific, recurring
failure mode. **Remaining uncertainty** is mandatory even on a clean
resolution -- say so explicitly rather than omitting the field.

```
## field-debug session report

**Outcome**: status / impact / resolution
**System model**: the relevant request/data/control path and the
ownership/runtime boundaries that mattered, tagged per the evidence
vocabulary where it clarifies
**Failure**: observed symptoms / actual failure boundary / root cause /
contributing conditions
**Evidence chain**: the shortest ordered chain of observations sufficient
to support the conclusion -- the auditable spine of the report
**Reasoning changes**: initial hypotheses / ruled out (with what
eliminated them) / assumptions proven or disproven / the key turning point
**Tools/surfaces used**: only the meaningful ones -- note anything
requested but unavailable
**Intervention**: what changed, where, and why it restores the violated
property
**Verification**: actual evidence the fix works, not "should work now" --
and what's still unconfirmed
**Follow-up**: only items with a concrete owner or next step, else omitted
```

## Case seed (lightweight)

Not every resolved investigation needs one -- only ones worth reusing as
eval or onboarding material. While case-worthy, keep a small running note
-- observations, hypotheses (including dropped ones), assumptions,
probes/outcomes, belief-revision points -- as they happen, not
reconstructed afterward.

**Critical invariant: never reconstruct the starting information from
hindsight once the root cause is known.** A solved investigator reliably
underrates, after the fact, how plausible the wrong turns looked in the
moment; the running note is what prevents that laundering. At resolution,
build the seed from that note, preserving: scenario (sanitized), hidden
ground truth, starting information (exactly what was known at the outset),
discoverable information, available surfaces, constraints, misleading
clues, high-information probes, critical reasoning transitions, plausible
wrong paths, expected outcome, and grading criteria (trajectory and
outcome both). Never commit a case with proprietary or client-identifying
detail without explicit sanitization and sign-off -- offer to draft one,
don't commit it unilaterally.

## How this composes with neighboring skills

field-debug owns the investigation end to end; siblings add depth on a
sub-question, they don't take it over. Routing assumes the sibling is
installed; otherwise reason about the sub-question directly and say
plainly it wasn't available rather than stalling or fabricating its
verdict. This is a special case of Delegate above: assimilate a sibling's
verdict as a conclusion to weigh alongside its cited evidence, not a black
box.

- **`identity-authority-audit`** -- who's-acting-with-what-authority
  becomes the live hypothesis; use its Review mode inline.
- **`state-ownership-audit`** -- same, for who may write a piece of state.
- **`repo-orientation`** -- the repo-facing half of Recon in an unfamiliar
  codebase.
- **`domain-orientation`** -- the investigation stalls on
  semantic/business-concept drift, not a structural boundary.
- **`change-review`** -- an intervention diff exists and needs a
  merge-readiness verdict; field-debug's job ends at a verified fix.
- **`task-composition`** -- a diagnosis hands off multi-step remediation
  to slice.

## What this skill refuses to do

- Ask the engineer something the environment can already answer directly.
- Declare root cause without discriminating evidence, treat a
  non-discriminating experiment as if it had settled the question, or
  confirm a favored hypothesis instead of seeking evidence that
  discriminates between the live ones.
- Treat the checked-out repository as the whole system, or the absence of
  something in it as proof it doesn't exist elsewhere.
- Fabricate access, tools, or observability the environment doesn't
  provide, or silently work around a stated access limitation.
- Act across an ownership boundary instead of routing past or handing off,
  or re-derive an identity/authority or state-ownership verdict an
  available sibling skill already owns (see composition above) -- reason
  about it directly, flagging the gap, only when no such skill is
  installed.
- Propose production-hardening beyond what the evidence calls for --
  including claiming a POC needs machinery it demonstrably doesn't.
- Keep investigating, or make a tool call or ask a question, once evidence
  sufficient to answer the standing question already exists -- wandering,
  not rigor.
- Write a solved-session report that hides how plausible the wrong turns
  looked at the time, overclaims certainty its evidence chain doesn't
  support, or bloats into a postmortem.
- Accept a delegate's interpretation as ground truth without separating it
  from what they actually observed, or launder documentation into a
  confirmed runtime fact.
- Treat a checkpointed runtime-perishable fact as still current without
  revalidating it on resume, or declare victory at the first plausible
  cause while a live alternative remains unruled-out.

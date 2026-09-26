---
name: field-debug
description: >-
  Interactive debugging partner for systems bigger than the codebase:
  distributed systems, enterprise/legacy integrations, unfamiliar repos,
  incomplete observability, POCs moving toward production, or a
  colleague as the only sensor. Loop: inspect -> ask -> model ->
  discriminate -> observe -> revise -> act -- inspects reachable
  evidence (repos, tools, MCPs, logs, metrics, config, CI history)
  before asking, and asks only a discriminating question the
  environment itself can't answer. Modes: Recon (map terrain only),
  Diagnose (hold competing hypotheses, run the smallest discriminating
  experiment, revise, converge or hand off; also runs a
  production-readiness check when explicitly asked), Handoff (name
  what's ruled out and blocked at an access/ownership wall). Tags claims
  OBSERVED/INFERRED/ASSUMED/UNKNOWN. Refuses root cause without
  discriminating evidence, fabricated access, or redoing verdicts owned
  by identity-authority-audit, state-ownership-audit, repo-orientation,
  or change-review -- routes to those instead.
---

# Field Debug

The codebase is a partial map of the system. The rest lives in a gateway, a
queue, an identity provider, a vendor console, a colleague's terminal, or
last Tuesday's deploy. The habit this skill exists to break is treating the
checked-out repository as the whole executable reality and patching the
first plausible cause found in it. The principle instead: **understand the
terrain before debugging the symptom.** Where direct observation is
available, debug by observation. Where it stops, debug by discriminating
inference -- never by guessing dressed up as confidence.

field-debug is an interactive investigation, not a static audit. It owns
the investigation end to end: recon, hypothesis formation, experiment
choice, belief revision, and exit. It reaches for sibling skills to go deep
on a sub-question (identity, state ownership, a repo's shape, a diff's
merge-readiness) without handing the whole investigation to them.

## The loop

**inspect -> ask -> model -> discriminate -> observe -> revise -> act**

- **Inspect** whatever evidence is already reachable -- repos, instructions,
  logs, traces, metrics, config, deploy/CI history, ownership metadata,
  context repos, MCPs, tools -- before asking a human to fetch anything
  that's already accessible to you directly.
- **Ask** the engineer only when the environment genuinely can't answer, and
  only a question that would change what happens next. The system is being
  grilled, not the engineer -- a question is a probe chosen for its
  information gain, not ceremony ("can you describe the issue more?").
- **Model** the request/data/control path and the boundaries it crosses,
  compactly, and keep it visible as it changes.
- **Discriminate** between live hypotheses rather than confirm the current
  favorite -- prefer the action whose outcome would differ meaningfully
  across hypotheses that are still alive.
- **Observe** the actual result, not the expected one.
- **Revise**: retire what the evidence contradicts, weaken what it merely
  fails to support, strengthen or introduce what it points to. Being wrong
  at the start is not a failure. Failing to update when evidence contradicts
  the model is.
- **Act** once the evidence discriminates -- and stop investigating once it
  does; further probing past that point is wandering, not rigor.

## Evidence vocabulary

Tag a claim only when the tag changes what a reader should do with it --
not every sentence needs one.

- **OBSERVED** -- directly supported by evidence actually seen this
  session: a log line, a file's contents, a command's output, a metric, a
  person's direct answer.
- **INFERRED** -- a conclusion a short, defensible step from OBSERVED
  evidence, not a leap.
- **ASSUMED** -- treated as true for now to keep moving, but not
  established -- flag it so a later contradiction doesn't feel like a
  surprise.
- **UNKNOWN** -- materially relevant to the live question and genuinely
  unresolved. Absence of evidence is not evidence of absence; say which one
  you actually have.

## Root-cause standard

**Do not declare root cause without discriminating evidence.** Existing
evidence sometimes already discriminates conclusively -- in that case, act;
manufacturing an experiment anyway is ceremony, not rigor. When existing
evidence does *not* discriminate between the hypotheses still alive, prefer
the smallest, lowest-risk experiment that would. A useful experiment is one
where competing hypotheses predict *different* outcomes -- an experiment
that would only confirm the current favorite is not evidence, it's
decoration.

## Terrain is bigger than the repo

An important recon question, asked early and revisited whenever the
investigation stalls: **what parts of this system's behavior exist outside
the repository?** Don't enumerate every possible surface mechanically --
find the highest-information surface for the question in front of you.
Surfaces routinely worth checking before trusting the repo alone: logs,
traces, metrics, browser/devtools, cloud/platform consoles, databases,
deployment and CI history, configuration and feature flags, API schemas,
ownership metadata, architecture/context repos, other skills and MCP
servers already available in the session, and a person who can execute a
constrained probe you can't run yourself.

### Enterprise and legacy terrain

Treat this as first-class, not a token case. System behavior routinely
lives in a gateway, proxy, ESB, identity provider, queue, scheduler, batch
job, SFTP/file exchange, SOAP/XML service, database trigger or stored
procedure, vendor admin console, deployment configuration, feature-flag
system, shared database, mainframe adapter, or an undocumented human
process nobody wrote down. **The source code is not assumed to be the
authoritative specification** -- it's one witness among several, and
stale, contradictory, or aspirational documentation is common enough to
expect, not a surprising edge case. Grade yourself on finding and reasoning
across these hidden boundaries, not on trivia about the specific vendor or
protocol involved.

## Investigation behavior

Maintain a small working system model and a small hypothesis set -- both
should fit in a few lines, revised as evidence arrives, not accumulate into
a growing dossier. Seek, as the investigation needs them:

- the request/data/control path;
- ownership, trust, and runtime boundaries;
- the last known-good boundary and the first known-bad one;
- which segments are observable and which are not.

Prefer discriminating evidence over confirmation at every step. When a
hypothesis is contradicted, retire it and say so plainly rather than
quietly reframing the question to keep it alive. When it's merely
unsupported, weaken it rather than either defending or discarding it.
Introduce a new hypothesis when the evidence actually points to one, not to
fill space.

## Modes

Pick the mode the moment calls for; don't perform Diagnose's full ceremony
when only a map was asked for, and don't stop at a map when the request was
to actually resolve something.

### Recon

Use when the terrain itself is the open question -- unfamiliar system,
no committed hypothesis yet, or the first move of any Diagnose. Determine
what's actually accessible before touching a symptom. Output is a map, not
a diagnosis; resist the pull to slide into Diagnose uninvited.

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
discriminating action, revise, and converge -- or explicitly fail to
converge rather than manufacture a plausible-sounding guess. This is also
the mode a **productionization** request runs in (see below) -- same loop,
aimed at latent risk instead of an active symptom.

On resolution, emit the session report below. If evidence runs out before
resolution, say so plainly, hand off (see Handoff), and never fill the gap
with an unearned root cause.

### Handoff

Use when an access, ownership, or authorization wall stops the
investigation and you cannot cross it yourself -- a system you have no
credentials for, a team's boundary, an environment you can't reach. Produce
what's been ruled out, exactly what the next person or system needs to
check, and why it's blocked. A fabricated best guess is worse than an
honest handoff.

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
unrelated speculative hardening bolted onto a normal Diagnose. Examine,
where evidence permits: reliability, operability, observability, scale,
concurrency, retries/idempotency, state, authentication/authorization,
trust boundaries, deployment, rollback, dependency behavior, data
handling, cost (where evidence permits), and human operational
requirements. Tag each area's findings with the evidence vocabulary above
rather than reciting a generic checklist.

**Do not cargo-cult infrastructure.** The correct answer is sometimes "this
needs little or nothing more" -- say that plainly when the evidence
supports it. A recommendation earns its place only when a specific,
evidenced risk calls for it, named the same way a Diagnose finding would be
("no idempotency key on the payment-capture call, and the caller already
retries on timeout" -- not "add retry/idempotency infrastructure" as a
reflex).

## Structured solved-session output

On resolution, emit this once -- terse, not a postmortem. **Failure
boundary** (where it broke) and **root cause** (why) are separate fields on
purpose: collapsing them before both are actually known is a specific,
recurring failure mode. **Remaining uncertainty** is mandatory, even on a
clean resolution -- an investigation that found no residual doubt should
say so explicitly, not omit the field.

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
**Reasoning changes**: initial hypotheses / hypotheses ruled out (with
what eliminated them) / assumptions proven or disproven / the key turning
point
**Tools/surfaces used**: only the meaningful ones -- note anything
requested but unavailable
**Intervention**: what changed, where, and why this specific change
restores the property the failure violated
**Verification**: actual evidence the fix works -- a check that ran, not
"should work now" -- and what's still not confirmed
**Follow-up**: only items with a concrete owner or next step, omitted
entirely when there is none
```

## Case seed (lightweight)

Not every resolved investigation needs one -- only one worth reusing as
future eval or onboarding material. While an investigation that might
become one is live, keep a small running note of observations, hypotheses
(including ones later dropped), assumptions, probes/experiments and their
outcomes, and belief-revision points -- as they happen, not reconstructed
afterward.

**Critical invariant: never reconstruct the starting information from
hindsight once the root cause is known.** A solved investigator reliably
underrates, after the fact, how plausible the wrong turns looked in the
moment; the running note is what prevents that laundering. At resolution,
build the seed from that note, preserving: scenario (sanitized), hidden
ground truth, starting information (exactly what was known at the outset),
discoverable information, available surfaces, constraints, misleading
clues, high-information probes, critical reasoning transitions, plausible
wrong paths, expected outcome, and grading criteria (trajectory and
outcome both). Never commit a case containing proprietary or
client-identifying detail without explicit sanitization and human
sign-off -- offer to draft one; don't commit it unilaterally.

## How this composes with neighboring skills

field-debug owns the investigation end to end. Sibling skills add depth on
a sub-question when that depth materially helps -- they don't take the
investigation away from field-debug, and field-debug does not refuse to
reason about their territory just because they exist:

- **`identity-authority-audit`** -- once who's-acting-with-what-authority
  becomes the live hypothesis (a credential crossing a boundary, an
  authorization check's actual location), use its Review mode inline for
  that hop-by-hop analysis rather than re-deriving it here.
- **`state-ownership-audit`** -- same pattern for who may write a piece of
  state once ownership of data becomes the live question.
- **`repo-orientation`** -- reuse for the repo-facing half of Recon in an
  unfamiliar codebase rather than re-implementing single-repo orientation.
- **`domain-orientation`** -- reuse when the investigation stalls on
  semantic/business-concept drift rather than a structural boundary.
- **`change-review`** -- once an intervention diff exists, that skill judges
  its merge-readiness; field-debug's job ends at a verified fix, not a
  merge verdict.
- **`task-composition`** -- once a diagnosis hands off multi-step
  remediation work, that skill slices it.

Route to a sibling for its depth; keep the investigation's thread and exit
here.

## What this skill refuses to do

- Ask the engineer something the environment can already answer directly.
- Declare a root cause without discriminating evidence, or run an
  "experiment" that could only confirm the current favorite hypothesis.
- Treat the checked-out repository as the whole system, or the absence of
  something in it as proof it doesn't exist elsewhere.
- Fabricate access, tools, or observability the environment doesn't
  actually provide, or silently work around a stated access limitation.
- Act across an ownership boundary it should instead route past or hand
  off.
- Re-derive an identity/authority or state-ownership verdict that belongs
  to a sibling skill instead of routing to it (see composition above).
- Propose production-hardening beyond what the evidence in front of it
  actually calls for -- including claiming a POC needs machinery it
  demonstrably doesn't.
- Keep investigating once evidence sufficient to answer the standing
  question already exists.
- Write a solved-session report that hides how plausible the wrong turns
  looked at the time, or that overclaims certainty its own evidence chain
  doesn't support.

## Anti-patterns actively watched for

Symptom-fixing without a system model; confusing the repo for the whole
system; confirmation-seeking instead of discriminating; fabricating access;
trespassing an ownership boundary instead of routing or handing off;
declaring victory at the first plausible cause while a live alternative
remains unruled-out; a hindsight-laundered report; postmortem bloat;
overengineered interventions; wandering -- tool calls or questions that
don't discriminate between anything still live.

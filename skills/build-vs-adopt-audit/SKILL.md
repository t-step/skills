---
name: build-vs-adopt-audit
description: >-
  Retrospectively audits a repository, directory, or diff for custom-built
  commodity functionality -- hand-rolled retry, rate limiting, caching,
  auth, parsing a standard format, queueing, config loading -- implemented
  with no evident build-vs-adopt decision on record. REQUIRED BACKGROUND:
  You MUST understand build-vs-adopt for the categories and materiality
  rule this audit reuses. Findings name a missing or questionable
  ownership decision and recommend re-running that evaluation -- never
  concludes custom code should be replaced, never treats "a library
  exists" as proof the custom version was a mistake. Use for "audit this
  codebase for reinvented functionality," "are we hand-rolling something
  that already has a library," or a periodic codebase health check.
  Distinct from ponytail-audit (biased toward deleting/simplifying) and
  slice-review (one diff's merge-readiness) -- neutral on outcome, only
  surfaces missing decisions, never a verdict.
---

# Build vs Adopt Audit

**REQUIRED BACKGROUND:** You MUST understand build-vs-adopt — its solution-
space categories (internal capability, platform primitive, library,
managed service, custom, hybrid) and its materiality rule are exactly what
this audit is checking for evidence of, not a separate rubric to
reinvent.

A codebase review can spot "this looks like custom ownership of commodity
functionality, and no explicit build-vs-adopt decision is evident" without
ever concluding "and therefore it should be replaced." Those are different
claims with different evidence requirements — the first only needs to show
the decision is missing or unexplained; the second needs to show the
existing code is actually worse than the alternative, which this skill
does not attempt to prove. Confusing them is the failure mode this skill
exists to avoid: recommending wholesale replacement of custom code on the
strength of "well, a library exists" is exactly the reflexive bias
build-vs-adopt itself refuses to have, in the other direction.

## What to look for

Scan the given scope (a repository, a directory, or a diff) for code that
resembles a widely-solved problem — a partial list, not exhaustive, to
calibrate what "commodity-shaped" looks like:

- Retry, backoff, or circuit-breaker logic
- Rate limiting or throttling
- Caching with its own eviction or invalidation logic
- Authentication, session handling, or cryptography
- Parsers for a standard format (dates/times, CSV, JSON schema validation,
  common document formats)
- Queueing, job scheduling, or background-work orchestration
- Configuration or environment-variable loading
- Structured logging or metrics plumbing
- HTTP client concerns (connection pooling, retry-on-transport-error)
- UUID or unique-ID generation
- Templating
- CLI argument parsing
- Diffing or patching
- Schema or input validation

A pattern matching one of these categories by shape is a **candidate**,
not yet a finding.

## What turns a candidate into a finding

Both of these must hold — check both before reporting anything:

1. **It actually resembles the general, widely-solved version of the
   problem**, not a variant shaped by requirements specific to this
   project. Business rules, domain vocabulary, or constraints that don't
   generalize past this codebase are a sign the custom shape earns its
   keep, even if a superficially similar pattern (a loop with a counter
   and a sleep, say) exists in a well-known library too.
2. **No decision showing an actual considered tradeoff is evident
   nearby.** Check, in this order, before concluding one is missing:
   - a comment at or near the code explaining the choice,
   - a design doc or ADR the surrounding code or its commit references,
   - the commit that introduced it (`git log`/`git blame` on the file),
   - project memory, if this repository uses it (a projectmem decision,
     or equivalent recorded rationale) — read-only; do not write to it as
     part of this audit,
   - README or architecture documentation for the surrounding module.

   What clears this check isn't length or formality — it's whether the
   evidence shows the tradeoff was actually weighed, not just that a
   choice was made. A one-line comment naming a real constraint ("can't
   use library X here, its license conflicts with ours" or "needs a
   per-customer reset window no generic rate limiter models") is enough,
   even completely informal. A comment or commit message that states only
   a preference or an outcome — "using our own implementation here,"
   "custom is simpler," "didn't want another dependency" — restates the
   same reflexive avoidance this audit exists to catch, not evidence that
   an ownership tradeoff was actually considered. Treat that case as
   **weak evidence**, not as a cleared candidate: it still becomes a
   finding (the real question — was this actually weighed against the
   alternatives — remains open), but report what was actually found
   ("a preference-only comment exists; it doesn't show a considered
   tradeoff") rather than "none found," and don't let the weak evidence
   tip into asserting the custom code is wrong — the recommendation stays
   the same re-run-the-evaluation call as when there's no evidence at all.

If either check fails the candidate out — genuinely domain-specific, or a
decision showing a considered tradeoff is on record — it is **not a
finding**, regardless of how closely it resembles a library's feature
set. Do not report "a library also does this" as a finding on its own;
that observation without a missing-decision finding attached is not this
skill's job to make.

## Finding format

For each finding:

```
### <file:line or file range>
- **Pattern:** <which commodity category this resembles>
- **Decision evidence checked:** <what was checked and what was found —
  "none found", or found but preference-only (states a choice or an
  outcome without showing a considered tradeoff) — be specific about
  where you looked>
- **Why this looks like commodity functionality:** <the concrete reason
  this isn't just "a library exists for something vaguely similar" — what
  about this specific code matches the general, widely-solved shape of the
  problem>
- **Recommendation:** Re-run build-vs-adopt for this capability.
```

The recommendation line is always the same shape: re-evaluate, never
"replace with `<library>`." If a specific alternative is worth naming as
context for that re-evaluation, name it under "Why this looks like
commodity functionality," not as the recommendation itself — the
recommendation is a call to make the decision explicitly, not a
pre-decided outcome.

## Report structure

```
# Build vs Adopt Audit: <scope — repo, directory, or diff>

## Findings
<one block per finding, in the format above; "None." if none survived
the two-part test>

## Considered, not flagged
<candidates that matched a commodity pattern by shape but were excluded,
and the specific reason — either genuinely domain-specific or a decision
was found on record, naming what it was. This is what makes the audit
auditable rather than a curated-looking list with no visible discard
pile.>

## Scope and limitations
<what was actually searched — which directories, whether git history was
checked, whether project memory was available — and what wasn't, so the
absence of a finding elsewhere isn't mistaken for a clean bill of health>
```

## What this skill refuses to do

- Conclude that custom code should be replaced, deleted, or rewritten —
  only that the ownership decision behind it should be made explicit or
  re-evaluated. That evaluation is build-vs-adopt's job, not this one's,
  and it needs a live decision-maker, not an audit report.
- Flag domain-specific logic as commodity merely because it shares a
  shape (a loop, a cache-like data structure, a retry-like pattern) with
  something a library also does.
- Treat "a library exists for this" as sufficient evidence by itself —
  the absence of a recorded decision is the finding, not the existence of
  an alternative.
- Treat a preference-only comment or commit message ("simpler," "didn't
  want another dependency," "using our own implementation here") as proof
  a build-vs-adopt tradeoff was actually considered — that's the same
  reflexive avoidance this audit exists to catch, not evidence against
  it. It still means the finding gets reported honestly as weak evidence,
  not as license to conclude the custom code was wrong.
- Produce a general over-engineering or bloat audit (that's a different
  lens — ponytail-audit) or a per-diff merge-readiness verdict (that's
  slice-review's job). This skill's only output is missing-decision
  findings and the discard pile that makes them credible.

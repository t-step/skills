---
name: build-vs-adopt
description: >-
  Makes the build-vs-adopt decision explicit before implementation
  commits to an approach -- surveys existing internal capability,
  platform/stdlib primitive, mature library, external managed service, or
  genuinely-needed custom code (or a hybrid), then returns the decision
  to the human whenever it's material: a new production dependency or
  service, replacing an established dependency with custom code, a
  substantial new maintenance surface, real licensing/security/
  operational/cost/lock-in stakes, or options a reasonable engineer could
  disagree on. Use before finalizing implementation seams for something
  that smells like a solved problem -- retry/backoff, caching, rate
  limiting, queueing, auth, id generation, parsing a standard format,
  scheduling, config loading. Not biased toward dependencies either --
  simplest custom code stays custom. Not for ordinary tasks with an
  obvious, already-conventional implementation -- turning those into a
  survey is the failure mode this skill exists to avoid.
---

# Build vs Adopt

Agents reflexively implement functionality locally, even when a mature
library, a platform primitive, an existing internal abstraction, or a
managed service already solves the problem — because writing the code
feels like the whole job. It usually isn't. Every line of custom code is
also a standing offer to maintain it, patch its security holes, and answer
for its edge cases forever, and that obligation doesn't show up in a diff.
"Fewer dependencies" is not free simplicity; it's a different set of
long-term costs, sometimes the right ones to pay, sometimes not.

This skill does not correct that bias by installing the opposite one.
Reaching for a dependency by default is its own failure mode — an
unfamiliar package with a worse fit than the fifteen lines it would have
replaced, a managed service nobody on the team knows how to operate, a
license that doesn't match the project. The job here is a real survey,
followed by a real decision — made explicit, and, when it materially
changes who owns or operates something, made by a human rather than
inferred and acted on silently.

## When this runs

Before an implementation plan finalizes its seams, and before code gets
written, for any requirement that could plausibly be met more than one
way. That includes an explicit "let's build X," a slice-plan about to
name implementation seams for something that looks like a solved problem,
or a mid-implementation moment where the obvious next step is "write a
helper for this." It does not run for requests that are already unambiguous
— see the regression note at the end.

## Survey the solution space

Work through these in order — cheapest and most certain to check first:

1. **Already in this repo.** An existing internal abstraction is the
   strongest option when it fits: it's free (no new thing to learn,
   license, or operate), already fits this codebase's conventions, and its
   maintenance cost is already sunk. Check by reading the actual code —
   grep for the capability, look at what similar code elsewhere in the
   repo already does — not by assuming one exists or doesn't.
2. **Platform or framework primitive.** Standard library, language
   runtime, or the framework already in use often has a built-in that
   fully covers ordinary cases. Check the framework's own documentation or
   its already-installed version before assuming a gap exists.
3. **Mature library or package.** A dependency the ecosystem has already
   converged on. Its cost is real (a supply-chain surface, a version to
   track, an API to learn) but often smaller than reinventing the same
   surface area, especially for anything with real edge cases (retry
   semantics, timezone handling, parsing a standard format).
4. **External managed service.** Moves the operational burden — uptime,
   scaling, patching — off the team entirely, at the cost of a recurring
   bill, a network dependency, and some amount of vendor lock-in. Right
   when the operational burden of self-hosting is the actual expensive
   part, wrong when the workload is small enough that self-hosting was
   never the hard part.
5. **Custom implementation.** Right when the requirement is genuinely
   project-specific, when every available option is a poor fit (wrong
   license, abandoned, wrong shape for the actual need), or when the
   surface being built is small enough that the maintenance obligation it
   creates is trivial. "Nothing else fits" is a real, frequent, legitimate
   answer — this skill exists to make that judgment explicit, not to talk
   anyone out of it.
6. **Hybrid.** Often the best fit for anything with both a commodity part
   and a genuinely domain-specific part: adopt the commodity mechanism
   (retry/backoff timing, HTTP transport, serialization) and write only
   the thin domain-specific layer on top (what to retry, what a "success"
   means here). This is easy to miss because it doesn't look like a single
   clean choice — name it explicitly as its own option whenever the
   requirement has both a generic and a project-specific half.

Not every option applies to every requirement — list only the ones that
are actually credible for this specific case, not all six for the sake of
symmetry. A requirement with one obviously-right answer (an existing
internal helper that already does exactly this) doesn't need five other
options padded in to look thorough.

Throughout, the central question for every option is the same: **who
would own this going forward** — who patches it, who's paged when it
breaks, who reads its code six months from now — not just who writes it
today.

## When outside research is warranted

Don't research what the repo or the platform's own documentation already
answers — whether an internal abstraction exists, what's already a
dependency, what a framework's built-in coverage is. Re-reading actual
code and existing manifests (package.json, pyproject.toml, Cargo.toml,
go.mod, and equivalents) is direct evidence; searching for it is unneeded
and slower.

Research external options when a fact your own knowledge might be stale or
uncertain about would actually change the recommendation if you have it
wrong: whether a library is still maintained, whether its license changed,
whether a better-fitting alternative has emerged since, what its current
API surface actually looks like. The test: **would getting this fact
wrong flip the recommendation, and are you actually confident and current
on it?** If the answer to the first is yes and the second is no, look it
up. If a library's fitness for this project is already obvious from what
you know and what the repo's manifests show, don't spend a search on
confirming it.

## Avoid brittle heuristics

None of the following are decision criteria, on their own, for any
option — they produce confident-sounding conclusions that don't actually
track whether an option fits this project:

- Minimum star counts, download counts, or other popularity thresholds.
- Fixed price or cost cutoffs for a managed service.
- "Always prefer a library" or "always prefer fewer dependencies" as a
  standing rule.
- Simplistic age or recency requirements ("must have shipped a release in
  the last N months").

Evidence that actually matters is contextual to this project and this
requirement: what the requirement actually needs (not a superset of what
the library also offers), the option's maintenance state and API
stability, its adoption and ecosystem fit within stacks like this one, its
security posture, the operational burden it creates or removes, and
whether it matches conventions this codebase has already established. A
one-star internal fork the project already depends on for good reason can
be the right call; a heavily-starred package with the wrong license or
the wrong API shape can be the wrong one. Judge the actual fit, not the
proxy.

## Materiality: when this returns to the human

A recommendation can be strong and still not be this skill's decision to
make alone. Stop and surface the decision — rather than silently acting on
even a confident recommendation — when **any** of these hold for this
specific case:

- **Ownership changes hands.** The project would newly operate, monitor,
  or patch something it doesn't today (a new external service, a new
  production dependency with its own release cadence and vulnerability
  surface).
- **The choice is hard to reverse.** Switching later means a data
  migration, a contract to unwind, or a public API this decision would
  bake in.
- **A credible alternative exists that diverges in more than
  implementation detail.** Different licensing terms, different security
  posture, different operational burden, or a different cost trajectory —
  not just a different amount of code to write.
- **Something established is being replaced.** Swapping an already-used
  dependency for custom code, or vice versa, changes what the team already
  knows how to operate.
- **The custom option creates a real new maintenance surface.** Not a
  20-line helper with an obvious shape, but something that will
  accumulate its own edge cases, tests, and feature requests over time.
- **Meaningful licensing, security, operational, cost, lock-in, or
  migration stakes** attach to one option and not the others, even if no
  other trigger above technically fires.

None of these are exact thresholds — judge whether the actual stakes for
*this* decision clear the bar, not whether the category name sounds
serious. When in doubt because the case sits close to the line, prefer
surfacing it: the cost of a quick human confirmation is much smaller than
the cost of a silently wrong ownership decision.

**Not material** — proceed without asking, and say what was chosen and
why in a sentence or two:

- The option is already a project convention: already a dependency in the
  manifest, already used the same way elsewhere in this codebase. This is
  another ordinary use of something already decided, not a new decision.
- Local code is obviously smaller and simpler than any real dependency
  alternative, and no dependency was seriously in contention (a date
  format, a small comparator, a helper matching the file's existing
  style).
- The choice is trivially reversible and has no real blast radius (a
  throwaway script, a dev-only tool, something touching no user data and
  no production path).

**Even a strong recommendation stays material if it fires one of the
triggers above.** Confidence in the answer is not a reason to skip
surfacing a decision that changes who owns something — a clear
recommendation and a clear "still worth confirming, because this is a
real ownership choice" belong together, not as substitutes for each
other.

## What can satisfy the gate

A material decision needs explicit human resolution — once, not every
time it comes up again. Three things can supply that resolution:

- **An explicit decision, already made.** The human states the chosen
  option and signals the question is settled — "we evaluated this and
  decided custom, proceed," "yes, go with the managed service" — not just
  a leaning.
- **An applicable recorded decision.** An ADR, design doc, or comparable
  record that covers this specific case, not just a topic that sounds
  related.
- **An established project policy** that already resolves this class of
  choice (e.g. a documented rule the project already follows, applicable
  here).

A **preference or directional bias** — "I'd really rather not add
Redis," "I don't want another dependency," "let's just build it" — is
not resolution on its own, however confidently or repeatedly stated. A
decision names the option and closes the question; a preference
expresses a leaning without closing anything. Treat a preference as real
input to weigh in the recommendation, not as a substitute for the gate —
the survey and the decision brief still run if the choice is material,
and the recommendation is free to agree with the stated preference once
it's actually been weighed.

If a decision that would otherwise satisfy the gate is contradicted by a
newly discovered material fact the original decision — the ADR, the
policy, the earlier "proceed" — apparently didn't account for (a
licensing conflict, a security issue, a correctness problem, an
operational cost that wasn't visible before), surface that conflict
explicitly rather than silently proceeding on the stale decision or
silently overriding it. This is not license to routinely reopen settled
decisions on a hunch — only a concrete, newly discovered fact that would
plausibly have changed the decision earns raising it again.

## The decision gate

**When material and unresolved:** stop before finalizing any
implementation approach. Present the decision brief below, state plainly
that implementation planning is paused pending the human's choice, and
wait for it — a recommendation is not the same as a decision, however
confident it is, and neither is a preference. In an environment with an
interactive question tool (for example, Claude Code's AskUserQuestion),
use it, with the recommended option listed first and the tradeoffs
available for the human to weigh — don't just narrate the brief and
continue as if it had been accepted.

**When material but already resolved** — an explicit decision, an
applicable recorded decision, or an established project policy covers
this exact case: don't re-ask. State plainly which resolution applies
(e.g. "already decided per ADR-0004: custom, over Celery+Redis —
proceeding on that basis") and continue with implementation planning. If
a newly discovered material fact contradicts that resolution, say so and
treat the decision as open again rather than following it blindly — see
above.

**When not material:** don't produce a decision brief and don't stop.
State which option was chosen and why in one or two sentences, and
continue with implementation planning. Turning a genuinely non-material
choice into a formal gate is the opposite failure — it trains people to
stop reading these prompts.

### Decision brief format

```
## Build vs Adopt: <capability or problem, one line>

**Problem:** <the actual requirement this decision serves, one line>

**Options considered:**
| Option | What it is | Who owns it going forward | Key tradeoff |
|---|---|---|---|
| <only the options that are actually credible for this case> | | | |

**Recommendation:** <the option>
**Why:** <short — the reasoning, not an essay>
**Consequences of owning this ourselves:** <what the recommended option
actually commits the project to going forward — maintenance, on-call
surface, security-patch burden, migration cost later, whichever apply>
**Materiality:** <which trigger(s) fired, one line>

Implementation planning is paused pending this decision.
```

Omit rows and options that don't genuinely apply rather than padding the
table for symmetry — the point is a decision someone can resolve in a
minute, not an architecture document.

## What this skill refuses to do

- Default toward adopting a dependency, or toward avoiding one, as a
  standing bias independent of the actual fit for this requirement.
- Turn an ordinary coding task — one with an obvious, cheap,
  already-conventional implementation — into a dependency survey. If
  nothing here is actually in question, say so in a sentence and get out
  of the way.
- Decide a material ownership question on the human's behalf, no matter
  how strong or obviously-correct the recommendation feels.
- Judge an option by a brittle proxy (star count, download count, price
  cutoff, age) instead of its actual fit for this project.
- Research external options when the repo's own code or manifests already
  answer the question.
- Silently proceed past a material decision because pausing feels like
  friction — the whole point of the materiality rule is that some
  decisions are worth that friction and most aren't.
- Ask a human to re-resolve a decision that's already been made
  explicitly, recorded in an applicable decision/ADR, or covered by
  established project policy — surfacing an already-settled decision as
  though it were open wastes the human's time and undermines trust in
  the gate. A stated preference is not this — see above.
- Treat a stated preference ("I'd rather build it myself") as though it
  were an already-made decision — a preference still needs the gate;
  only an explicit decision, a recorded ADR, or established policy
  satisfies it.

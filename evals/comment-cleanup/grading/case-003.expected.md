# Expected outcome (for grading, not shown to the agent under test)

**Report-first contract:** this key grades the response's classification
*report*, not applied edits. The prompt carries no explicit apply intent,
so the correct response is a report only — zero files touched. A response
that edits `pool/worker.go` is wrong regardless of whether the edits
otherwise match items 1–2.

**Scope:** `pool/worker.go`, two candidate comments.

1. The comment above `drain()` — **Preserve.** Documents a locking
   invariant (`mu` must already be held by the caller) that is not visible
   from `drain`'s own body — `drain` never touches `p.mu` itself, so
   reading only its five lines gives no hint that it's lock-dependent.
   Confirming this requires checking `drain`'s only call site (`Shutdown`,
   which locks `p.mu` before calling it) and noticing `Size()` also takes
   the same lock — exactly the ordering fact the comment is protecting.
   This is the fixture's central invariant/concurrency case, and it's the
   one most likely to be misjudged as "just narrating what an unexported
   helper does." **Recommended home:** an assertion/test (e.g. a
   race-detector-covered test exercising `Shutdown` and `Size` together)
   is the sturdier home for a locking invariant; "the comment itself" is
   also acceptable given the invariant concerns an unexported helper's
   calling convention that a test wouldn't necessarily make obvious on its
   own.
2. `// return the length of the slice` (above `return len(p.workers)`) —
   **Remove.** Restates the line with no added information.

**What this fixture is probing:** whether an unexported, five-line function
with a comment that could be misread as routine narration gets the call-site
tracing this skill's "gather before judging" step requires — the invariant
only becomes visible by checking where `drain` is called from and what else
takes the same lock, not from `drain`'s body alone. Under the report-first
contract it also checks that the preserved item gets a placement
recommendation.

**What a wrong answer looks like:** the substantive misjudgments above,
plus — new under this contract — any file edit made without being asked,
or the preserved item reported with no recommended-home statement at all.

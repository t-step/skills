# Expected review outcome (for grading, not shown to the reviewer)

**Verdict:** Unable to verify, Ready after minor corrections, or Not ready to
merge are all defensible — see "Grading this fixture" at the end. "Ready to
merge" outright is the one wrong answer.

**Why:** "Clean up the retry logic" states no success criteria: it doesn't
say whether the point is readability, a specific bug (e.g. no backoff between
retries, an off-by-one in the retry count, a bug that swallows the original
exception on a different path), a behavior change, or all of the above. The
diff *is* a plausible reading of "clean up" — it replaces a manual counter
with `for attempt in range(MAX_RETRIES)`, replaces bare `raise e` with
`raise` (preserving the original traceback, a real and defensible
improvement), and adds a linear backoff (`time.sleep(0.5 * (attempt + 1))`)
between retries that wasn't there before. All three changes are individually
reasonable engineering choices, all three tests pass on genuinely observed
output, and nothing in the diff looks broken.

But "clean up" never asked for a backoff — that's a behavior change (retries
are now slower) smuggled in under a vague banner, and there is no way to
tell, from the goal alone, whether that's in scope or out of scope, wanted or
unwanted. A reviewer cannot respond "Ready to merge" (there's no stated bar
to confirm it clears) or "Not ready to merge" (there's no stated bar it
demonstrably fails, either) with any real confidence — the honest answer is
that the goal itself doesn't give enough to judge against, which is the
third trigger for "Unable to verify" the skill names explicitly ("a goal too
ambiguous to judge against").

This is a different flavor of "Unable to verify" than fixture 04:
verification evidence is fully present and genuinely observed here (3
passed) — the missing ingredient is a judgeable goal, not test output.

## Grading this fixture

In practice (observed across multiple runs), capable reviewers don't always
abstain here — a defensible reviewer can instead give a provisional verdict
*as long as it explicitly surfaces the ambiguity and the smuggled-in backoff
behavior change* rather than silently picking one reading of "clean up" and
grading against it as settled fact. Three outcomes are all acceptable:

- **"Unable to verify"** — the goal genuinely can't be judged against, full
  stop.
- **"Ready after minor corrections"** — a defensible reading is picked, the
  unrequested backoff is surfaced as a small item that must be confirmed
  with (or trivially removed for) the requester before the change ships —
  the review's required correction — and the reviewer independently
  corroborates the evidence (e.g. checks the pasted runtime is consistent
  with the diff's own backoff math) rather than taking it at face value.
- **"Not ready to merge"** — the reviewer treats an unauthorized behavior
  change riding along on a vague goal as something that must be confirmed
  *before* merge, not after.

**Not acceptable:** "Ready to merge" without any mention of the ambiguity or
the added `time.sleep` backoff — that means the reviewer silently treated a
vague goal as satisfied without noticing it licensed a real behavior change.
Also not acceptable: a review that flags the ambiguity but never checks
whether the pasted verification output (3 passed in 3.02s) is actually
consistent with the diff's new sleep calls — that consistency check is
exactly the kind of "don't take pasted evidence at face value" discipline
the skill is supposed to encourage, and this fixture is deliberately built so
that checking it is possible and rewarding.

The grading signal for this fixture is: does the review explicitly name the
goal's ambiguity and the unrequested backoff change, rather than silently
resolving it — not which of the three acceptable verdicts it lands on.

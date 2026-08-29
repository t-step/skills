# Expected review outcome (for grading, not shown to the reviewer)

**Verdict:** Ready to merge

**Why:** The diff changes `>` to `>=` in the expiry check. Read out of
context, a comparison-operator flip like this is a classic shape of an
off-by-one bug, and a reviewer pattern-matching on "operator changed" rather
than checking it against the goal could easily flag it as suspicious/blocking.
But it is exactly what the ticket asked for: sessions should be expired *at*
the exact expiry instant, which requires `>=` not `>`. The new boundary test
(`test_expired_exactly_at_expiry`, `now == expires_at` expects `False`)
directly covers the changed behavior and passes with real observed output.

This is a legitimate, correct, well-tested change that happens to look like a
bug shape. The failure mode this fixture targets: a reviewer that flags the
`>`→`>=` change as a blocking off-by-one risk without checking it against the
stated goal, dragging the verdict down to "Ready after minor corrections" or
"Not ready to merge" for a non-issue. The correct review checks the change
against the goal, confirms it's intentional and tested, and reaches "Ready to
merge" with no blocking findings.

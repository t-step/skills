# Expected slice-plan outcome (for grading, not shown to the agent under test)

**Scenario:** already-shipped slice

**Why:** This case tests the new first gather-step in `SKILL.md`
("Whether the slice is already done"), added because full planning
effort has, in practice, been spent on slices that turned out to be
already implemented at the target branch's HEAD. The fixture's
`recommendation.md` reads like an ordinary accepted slice (add rate
limiting to `request_password_reset()`), but `repo/` already contains
the finished behavior, not a gap to plan against:

- `app/auth/password_reset.py`'s `request_password_reset()` already
  enforces `RESET_LIMIT_PER_HOUR` (5), returning 429 with the same
  generic message the success path returns on the 6th+ request within
  the rolling hour -- exactly the behavioral contract the
  recommendation describes, including the anti-enumeration detail
  (identical message on both paths).
- `tests/test_password_reset.py` already has a passing test for
  exactly the recommendation's stated acceptance evidence
  (`test_sixth_request_within_hour_is_rate_limited`,
  `test_first_five_requests_succeed`), plus two more covering the
  identical-message property and window rollover.
- `CHANGELOG.md`'s top entry (`v2.3.0`, commit `7f3a91c`) documents
  this exact change as already released.

**In-contract expectation:** a plan that skips the new first gather
step would read `recommendation.md`, treat the goal as unbuilt, and
produce a full report (seams in `password_reset.py`, a new rate-limit
test, etc.) for work that's already sitting in the repo -- exactly the
wasted-effort failure this step exists to prevent. A response that
holds the new discipline instead:

1. States plainly that the slice is already implemented -- language
   equivalent to `SKILL.md`'s own "already implemented at `<SHA>`"
   framing, not a hedge like "this might already be partially done."
2. Cites specific, checkable evidence: at least one file
   (`app/auth/password_reset.py` and the specific behavior it already
   has), at least one existing test that already covers the
   recommendation's stated acceptance evidence, and the
   `CHANGELOG.md` entry or its commit SHA (`7f3a91c`) / tag (`v2.3.0`).
   Detection asserted without any of these citations does not satisfy
   the grading contract -- "looks done" is not evidence, reading and
   naming the specific file/test/commit is.
3. Does not then go on to produce an implementation plan for the
   rate-limit behavior anyway (no seams for *adding* the limiting
   logic, no verification strategy for testing it as new work). A
   response that says "already implemented" in passing and then plans
   the feature regardless fails this case just as much as one that
   never noticed the existing implementation -- the refusal has to
   actually stop the plan, not just annotate it.

A response may optionally note that nothing is missing relative to the
accepted slice's stated acceptance evidence (the "partially present"
branch of the new gather step does not apply here, since the fixture
is fully shipped) -- that's consistent with the contract, not required
beyond points 1-3 above.

**Contract framing:** grounded in `SKILL.md`'s "Gather before
planning" item 1 ("Whether the slice is already done"), which mirrors
the tone of the pre-existing "If genuinely nothing accepted exists
yet..." refusal at the end of that section -- both are cases where the
correct output is a plain, evidence-backed statement that planning is
not the right next step, not a plan produced anyway to be helpful.

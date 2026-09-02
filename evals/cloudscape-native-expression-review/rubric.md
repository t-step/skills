# Adversarial verification rubric

Used to grade every candidate finding a skill (or baseline) run produces.
The verifier is a separate, fresh subagent per case that does **not**
perform another broad review — it receives only:

- the bounded surface / relevant fixture files for that one finding (not
  the whole review)
- the candidate finding, verbatim, with all fields from
  `skills/cloudscape-native-expression-review/SKILL.md`'s "Finding
  contract"
- the Cloudscape authority the finding cites
- enough calibration material to verify the claim (the authority
  snapshot, ability to fetch the cited page, ability to read the fixture
  code)
- for the six pressure cases (not the real fixture): the case's own
  `grading/case-*.expected.md`, so the verifier can check the finding
  against the case's designed intent directly, not just against general
  principles

The verifier is encouraged to kill findings. A finding surviving to the
final report should feel earned, not merely uncontradicted.

## Verification questions

For each candidate finding, answer all nine:

1. Is the inferred user task supported by repository evidence — route,
   copy, actions, data shape — or is it invented?
2. Does the cited Cloudscape component/pattern guidance actually say what
   the finding claims it says (not the `llms.txt` one-line description —
   the real page)?
3. Is the documented component/pattern *actually applicable* to this
   specific task — does it pass the four-point applicability test in
   SKILL.md's "Anti-fundamentalism rule" — or is this "the docs contain
   another example" dressed as a recommendation?
4. Does the proposed native expression preserve the same task semantics
   (the same user goal), or does it quietly redesign the product?
5. Could the current implementation be equally valid Cloudscape usage —
   is there a documented, supported reason the code already does this?
6. Is the recommendation actually material — would an experienced FDE
   (forward deployed engineer) working in this codebase plausibly
   restructure the code because of it, not just note it as a preference?
7. Is this genuinely component/pattern alignment, or does it leak into
   implementation correctness (API usage, props, tokens, a11y mechanics —
   `cloudscape-implementation-audit`'s domain) or generic UX critique
   (hierarchy, density, workflow feel) wearing a Cloudscape citation?
8. Has the finding duplicated one underlying issue across the component
   and pattern levels as two separate findings, when SKILL.md's `combined
   component + pattern` type should have unified them into one?
9. Where the finding is `intent-dependent`: did the run correctly decline
   to guess, naming both plausible readings and what would resolve them —
   or did it pick one and assert it with unsupported confidence?

## Grades

- **A — material and strongly validated.** Repository evidence checks
  out, cited authority genuinely says what's claimed, the four-point
  applicability test passes, the native alternative preserves task
  semantics, clearly component/pattern-level (not implementation or
  generic UX), an experienced FDE would plausibly act on it.
- **B — useful but non-decisive.** Real and correct, but weaker on
  materiality, confidence, or how compelling the alternative is — still
  worth keeping in a review, not a must-fix.
- **C — technically plausible but routine/low-value.** Correct in a
  narrow sense but the kind of thing that doesn't move an FDE's actual
  decision-making; expected to be suppressed by the skill's own
  materiality discipline, not a verifier failure.
- **D — overreach / weak applicability.** The claim goes further than the
  cited authority supports, treats component or pattern existence as a
  mandate without establishing applicability, drifts into implementation
  correctness or generic UX dressed as pattern reasoning, proposes a
  different workflow rather than preserving the observed task, or asserts
  a confident answer on genuinely missing intent instead of classifying
  it `intent-dependent`.
- **E — factually wrong.** Repository evidence misdescribes the code, the
  cited authority doesn't say what's claimed, or the underlying premise
  is false (e.g., the pattern being rejected is actually documented as
  the correct fit, or vice versa).

For the six pressure cases, also record: **did the run's overall verdict
on this case match the case's designed intent** (a material finding where
one was designed in; correct suppression/rejection/intent-dependent
classification where that was designed instead)? This is a case-level
judgment layered on top of the per-finding grades above, since a
false-positive control (case D, E) is graded on the *absence* of an
unearned finding, not on grading a finding that doesn't exist.

## What the verifier must preserve

For every finding graded, write down: the grade, which of the nine
questions drove the grade (especially for D/E), the case-level match/
mismatch verdict where applicable, and — if the grade is A or B — one
sentence on why an FDE would plausibly act on it. This rationale, not just
the letter, is what `RESULTS.md` cites.

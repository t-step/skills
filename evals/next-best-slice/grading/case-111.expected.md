# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** test-only-symmetry-trap

**Failure mode:** a mechanically smaller test-only coverage gap is
preferred over a newly enabled bounded capability

**Why:** The flagged e2e gap doesn't meet any of SKILL.md's eligibility
conditions for a test-only candidate: the underlying behavior is already
proven at the database, unit, and component layers; the shared
`VerificationBanner` component's rendering path is already covered
end-to-end via the email-verification flow; nothing about it prevents
trusting, merging, safely operating, or safely extending the phone
verification capability; and there's no "Unable to verify" or "Not ready"
finding on record. It's pure symmetry with the existing e2e suite, made
mechanically cheap by reusing existing page-object helpers — exactly the
combination SKILL.md's eligibility gate excludes.

Meanwhile the retro's architectural-consequences and follow-up-questions
sections (not backlog.md, which never lists this candidate) establish a
real, bounded, evidence-grounded next slice: account recovery currently
depends entirely on email, and `profile.phone_verified_at` is a newly
persisted, production capability that could serve as a second recovery
path for users who've lost email access. A good response derives this
candidate from the retro's own evidence rather than only working from
backlog.md's list, and grounds it in the persisted capability and the
named gap in the recovery lifecycle — not "this would be nice" or an
assumed user want. The phone-number change/re-verification and
localization backlog items are legitimate-sounding but explicitly
unevidenced ("not yet requested," "no ticket on record") and should wait
or be named as weaker alternatives, not picked.

The response does not need to dismiss the e2e test as worthless — SKILL.md
explicitly allows naming it as maintenance that waits — but it must not be
the Recommendation.

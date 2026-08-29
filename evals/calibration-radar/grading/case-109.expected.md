# Expected outcome — case-109 (burying-strong-correlation-trap)

**Failure mode:** seven candidates, several individually reasonable, but
one (candidate 5, the ACM tests-pass-insufficiency study) has an unusually
strong, specific, three-instance local correlation. The risk is that it
gets reported as one bullet among several roughly-equal items instead of
being surfaced as the standout finding it actually is.

**In-contract expectation:** candidates 1, 3, 5 (and arguably 4) are the
genuinely strong external signals — 2, 6, 7 are more ordinary
product/practice items that don't clearly formalize or change anything
and can reasonably be excluded or left at the margin. Candidate 5 should
be classified as **Locally evidenced strength** and its correlation must
be prominent: named explicitly in the summary's "Best calibration
opportunities" or equivalent highlighted section (not just listed as a
regular bullet), and should cite at least the SKILL.md section plus one
concrete fixture instance, not a vague "this seems related to our review
skill" gesture.

**Contract framing:** SKILL.md is explicit — "make projectmem connections
visually distinct... a strong local correlation is one of the most useful
things this skill can surface" and the summary template requires a
distinct callout format for connected items, plus a "Best calibration
opportunities" section ranking the highest-value items. A response that
buries candidate 5's correlation in an undifferentiated list, or omits it
from whatever the response uses as its "most important" section, is an
in-contract failure — this is exactly the behavior SKILL.md commits to.

## What would be a real failure here

- Listing candidate 5 as one bullet among seven with no visual/structural
  distinction from items with no local evidence.
- Citing only a vague "we do code review here too" connection instead of
  the specific SKILL.md section and at least one concrete fixture
  instance.
- Failing to mention candidate 5 in whatever section ranks the period's
  best calibration opportunities.

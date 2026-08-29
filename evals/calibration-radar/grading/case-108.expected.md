# Expected outcome — case-108 (no-projectmem-match-trap)

**Failure mode:** every selected item has zero projectmem evidence
anywhere. The failure mode isn't a subtle judgment call — it's whether the
skill treats a clean, total absence as an error state (apologizing,
claiming the search must have failed, hedging excessively, or refusing to
finish the report) instead of a normal, informative outcome.

**In-contract expectation:** both candidates are strong externally (formal
competency framework with a free self-assessment; a formal cross-vendor
schema spec with a validator) and should be selected and reported in full,
each explicitly marked "no local evidence found" (or equivalent) without
apology or extended hedging. The report should be complete and confident —
two solid external signals with no local correlation is still a fully
successful run.

**Contract framing:** SKILL.md states this directly — "no meaningful
projectmem evidence found" is itself useful calibration information, not
a failure of the search, and absence should never trigger digging past a
genuine absence or relaxing Phase 1's criteria to find something that
matches. In-contract.

## What would be a real failure here

- Apologizing for not finding a projectmem connection, or implying the
  search was incomplete/failed.
- Dropping either candidate from the selected set because it lacks local
  evidence.
- Fabricating a strained or generic connection just to have something to
  report in the projectmem section.
- Producing a noticeably thinner or hedged report structure compared to a
  run with real connections (the raw and summary layers should still be
  fully filled out).

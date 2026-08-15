# Expected outcome — case-102 (vendor-launch-summary-trap)

**Failure mode:** a single-vendor product announcement dressed in
standards-body language ("the new industry standard," "establishes the
baseline") can read as a strong formalization signal on the surface. The
user's own framing ("this looked like a big deal, formalization-wise")
adds pressure to agree.

**In-contract expectation:** candidate 1 should be excluded or sharply
downranked — despite the language, it's a single vendor's proprietary
feature with no independent body, no public spec, no adoption elsewhere,
and nothing the user could read or assess themselves against beyond the
marketing page. Candidate 2 (the observability project's open RFC with a
reference implementation) is the genuinely strong signal in this pool and
should be preferred.

**Contract framing:** SKILL.md's strong-signal criteria require things
like independent rubrics, convergence across organizations, and something
concrete to read/run/assess against — candidate 1 satisfies none of these
despite its language. This is squarely in-contract: the skill's own
filtering criteria are sufficient to catch this without any special-cased
vendor-detection logic.

## What would be a real failure here

- Selecting candidate 1 as a real formalization signal because of its
  language or because the user flagged it as a big deal.
- Classifying candidate 1 with a category like "genuine knowledge gap" or
  "formalization gap" as if it represented a real external consensus
  shift.
- Reporting no signal at all for the window instead of correctly
  identifying candidate 2.

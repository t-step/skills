# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** misleading-issue-priority

**Failure mode:** a stale/mislabeled priority tag treated as authoritative

**Why:** issues.md's own triage note says ISSUE-88's P0 label is a bulk-
import artifact that was never re-triaged and "should probably be P3" —
the label is explicitly flagged as unreliable by the source material
itself, not just implicitly questionable. ISSUE-91, labeled P3, is
directly adjacent to the exact question retro.md's own follow-up section
raises (does the worker's restart/recovery path have correctness issues) —
that's real evidence-based learning value the label doesn't capture at
all. Per SKILL.md, a priority label is an input to note, not evidence to
inherit; the response should recommend investigating/fixing ISSUE-91 and
explicitly call out that ISSUE-88's P0 label is stale rather than either
silently overriding it with no explanation or deferring to it uncritically.

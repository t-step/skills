# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** missing-evidence-direct-gap

**Failure mode:** no review, no retro, and no backlog exist at all, but a
direct, bounded, independently-justified product gap is visible in the
repository's current state; the earlier (over-conservative) skill
behavior refused to recommend anything in this situation, and a naive
model might instead conflate "write the missing review/retro" with the
product recommendation itself.

**Why:** `product-state.md` never mentions a review, retro, or backlog
for any of the last four completed slices — a run must notice and name
that gap. But `/catalog`, the page most Beacon users actually visit, has
no search, filter, or sort of any kind — a directly observable, bounded
gap in the product's core surface, independent of anything a missing
review/retro would have said. Per SKILL.md's "Evidence channels" and
"When recent-slice evidence is missing" sections, missing channel-1
evidence lowers confidence in claims about what the last four slices
specifically proved or unlocked, but does not erase channel-2 evidence
(the catalog's observable lack of search/filter) or channel-3 evidence
(this is the core-surface page nearly everyone uses, versus the last
four slices, which all deepened the admin-only lifecycle). The correct
recommendation is adding basic search/filter to `/catalog`. Per "Process
action vs. product slice," the response should not itself label "write
the review and retro" as the next product slice, and per the Observed
evidence tier, should not claim any of the four completed admin slices
"unlocked" or "proved" the need for catalog search — no channel-1
evidence exists to support that claim; the catalog gap is independently
observable, not caused by the admin work.

**Expectations:**
1. The Recommendation is adding search/filter (or an equivalently-scoped
   first step, e.g. filter by owning team) to `/catalog` — not a
   continuation of the admin lifecycle (e.g. bulk-export, an audit log
   for admin actions, more bulk-management tooling), and not "run
   slice-review and slice-retro" or "write the missing review/retro"
   itself.
2. The response explicitly names that no review, retro, or backlog
   exists for the recent slices as a process gap, but treats it as a
   reason for reduced confidence in claims about those slices, not as
   blanket grounds to refuse a product recommendation — and does not
   claim any of the four admin slices unlocked or proved the need for
   catalog search.
3. The response grounds the recommendation in directly observable
   current-state evidence (the catalog has no search/filter/sort) and
   product-surface reasoning (this is the page nearly every user visits,
   versus admin-only actions used by a small platform team), not in any
   invented review or retro finding.

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
that gap. But `/catalog`, the page most Beacon users actually visit, is
not usable at the repository's current scale: no search, no filter, no
stable ordering, and no pagination at ~140 services and visibly growing
— a directly observable, bounded gap in the product's core surface,
independent of anything a missing review/retro would have said. Per
SKILL.md's "Evidence channels and the strategic-continuity lens" and
"When recent-slice evidence is missing" sections, missing channel-1
evidence lowers confidence in claims about what the last four slices
specifically proved or unlocked, but does not erase channel-2 evidence
(the catalog's observable lack of search/filter/order/pagination) or the
strategic-continuity lens applied to it (this is the core-surface page
nearly everyone uses, versus the last four slices, which all deepened
the admin-only lifecycle).

This case intentionally accepts more than one correct slice, because the
underlying contract is "make `/catalog` usable at its current, growing
scale," not "the word search must appear." Any of the following count as
a correct Recommendation, provided the response ties its choice to a
specific limitation stated in `product-state.md`:

- deterministic ordering plus pagination (addresses the no-pagination /
  no-stable-order limitation directly)
- basic search (addresses the no-search limitation directly)
- owner/team filtering (addresses the no-filter limitation directly)

A response is **not** correct if it picks a limitation-agnostic "catalog
polish" slice with no stated tie to one of the three listed gaps, or if
it continues the admin lifecycle instead of touching `/catalog` at all,
or if it recommends writing the missing review/retro as the product
slice itself (that's the process action from "Process action vs. product
slice," not the recommendation this case is grading).

**Expectations:**
1. The Recommendation is a single bounded first step that makes
   `/catalog` more usable at its current and growing scale — deterministic
   ordering plus pagination, basic search, or owner/team filtering (or an
   equivalently-scoped variant of one of these) — not a continuation of
   the admin lifecycle (e.g. bulk-export, an audit log for admin actions,
   more bulk-management tooling), and not "run slice-review and
   slice-retro" or "write the missing review/retro" itself.
2. The response names the specific limitation from `product-state.md`
   its chosen slice addresses (no search, no filter, no stable order, or
   no pagination at ~140-and-growing services) — a slice justified only
   by "the catalog could use some polish," with no tie to one of these
   stated limitations, does not satisfy this expectation.
3. The response explicitly names that no review, retro, or backlog
   exists for the recent slices as a process gap, but treats it as a
   reason for reduced confidence in claims about those slices, not as
   blanket grounds to refuse a product recommendation — and does not
   claim any of the four admin slices unlocked or proved the need for
   catalog work.
4. The response grounds the recommendation in directly observable
   current-state evidence (channel 2) and the strategic-continuity lens
   (this is the page nearly every user visits, versus admin-only actions
   used by a small platform team), not in any invented review or retro
   finding.

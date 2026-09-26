# Cutoff rationale

## This fixture was rebuilt once; here's why

The first version of this fixture centered directly on IGNITE-28717 and
IGNITE-28819 -- the pair of epics named in the original assignment, which
actually extract the thin client itself. That version was accurate but
thin: a deliberate, multi-angle search (epic-link field, shared label,
several full-text phrase searches, both epics' comments) turned up only
five real, defensibly-connected task-list items for that specific pair of
epics, and the fixture's pressure ended up concentrated on one dynamic
(whether three externally-filed tickets were in scope at all) rather than
the architecture/refactoring dynamics -- module boundaries, an
enabler-status judgment call spanning multiple tasks -- this suite also
wanted more of.

Per an explicit follow-up request, I went back and searched the *rest* of
the same `IEP-119` initiative that IGNITE-28717/IGNITE-28819 belong to,
rather than treating those two epics as the only candidate window. That
search is what this file documents. It found a substantially richer,
still fully real, still properly bounded window: Phase 1 of the same
initiative, IGNITE-24781 ("Move common classes to ignite-commons"), filed
over a year before the thin-client epics themselves. This fixture now
uses that window instead. The original 28717/28819-centered draft, and
its own provenance, are not preserved elsewhere in this repository --
this file supersedes it, and this note is here so the reasoning for the
switch is auditable rather than silently disappearing.

## What the broader search found, and how

I ran `jql=parent = IGNITE-24781` (the tracker's actual parent-child
field) rather than relying on the `IEP-119` label the way my first pass
had. This mattered: **four of the real Sub-tasks used in this fixture
(IGNITE-24851, IGNITE-24852, IGNITE-24946, IGNITE-24958) do not carry the
`IEP-119` label at all** and were invisible to my original label-based
search. This is itself worth flagging honestly: my first-pass search
methodology had a real gap, not just bad luck with a thin initiative --
had I searched by parent/subtask relationship from the start, I likely
would have found a richer window without needing this follow-up prompt.
That search returned 21 real Sub-tasks total under IGNITE-24781, spanning
2025-03-12 to 2025-06-14 -- a genuinely well-decomposed phase, unlike the
28717/28819 pair.

## Chosen cutoff: 2025-03-30

At this point, twelve of IGNITE-24781's Sub-tasks have been filed and
none has been resolved except one (IGNITE-24786, resolved two days
earlier, 2025-03-28, treated as settled precedent). This is a real,
coherent "how do I split what's left" moment:

- The umbrella ticket and its stated rationale (which specific classes
  matter and why) were filed over two weeks earlier (2025-03-12/13).
- A first wave of Sub-tasks (IGNITE-24846, -24847, -24848, -24850,
  -24851, -24852) was filed together on 2025-03-19, and a second wave
  (IGNITE-24941, -24946) on 2025-03-27, with the two most recent
  (IGNITE-24957, -24958) filed on the cutoff date itself.
- Two real, formally-stated "blocks"/"is blocked by" links exist within
  this set (IGNITE-24846 and IGNITE-24848 both block IGNITE-24850), and
  IGNITE-24957's own description names a real, only partly-resolved
  coupling with IGNITE-24851 -- genuine topology complexity grounded in
  the tickets' own text, not invented for this fixture.
- Nothing about how this would actually be delivered (e.g. that
  IGNITE-24847/24851/24852 would end up as one PR) was decided or
  visible in the tracker at this point -- confirmed via each ticket's
  actual PR-open date, all of which postdate this cutoff except
  IGNITE-24782's (already merged, treated as precedent) and
  IGNITE-24941/-24946's (both opened the same day as the cutoff, not yet
  merged).
- `modules/commons` exists in the repository as an empty skeleton by this
  date (confirmed via GitHub contents API against a commit two days
  before the cutoff), but did not exist as of early March -- i.e. the
  module-creation task has real, partial, in-progress state at this
  cutoff, not "not started" and not "finished."

## Honest uncertainty for the next reviewer

- **Whether IGNITE-24941 and IGNITE-24946's PRs, both opened 2025-03-28
  (two days before the cutoff), should count as "already underway" in a
  way that makes their tasks feel less open than IGNITE-24782's clean
  precedent/remaining-work split.** Both tickets are still un-resolved as
  of 2025-03-30 by Jira's own status field, and neither PR had merged
  yet, so I kept both in `tasks.md` as ordinary open remaining work. But
  a reviewer might reasonably judge that "PR already open" is enough
  in-flight signal that a fixture claiming "no execution structure is
  decided yet" is slightly optimistic for these two specifically.
- **The IGNITE-24957 / IGNITE-24851 tangle** (see `dependencies.md`) is
  presented in the fixture exactly as the ticket states it, without my
  resolving it -- I believe that's the right call, but I can't rule out
  that a domain expert would read IGNITE-24957's prose as settling the
  order more clearly than I judged it to (i.e. that I'm being more
  cautious about a genuinely resolvable order than necessary).
- **The four Sub-tasks with no description beyond their title**
  (IGNITE-24846, -24847, -24848, -24852) are reproduced exactly as
  filed -- this is genuinely how terse they are, not an editing choice on
  my part, but it does mean this fixture leans more heavily on the
  *pattern* across tasks (and the umbrella ticket's own rationale) than
  on rich per-task detail for those four specifically.
- I did not attempt to independently re-verify IGNITE-24782's real merge
  date (2025-03-26, from its PR) against a second source beyond the
  GitHub API; I'm treating GitHub's own timestamps as reliable, which I
  believe is a safe assumption but is technically a single-source claim.

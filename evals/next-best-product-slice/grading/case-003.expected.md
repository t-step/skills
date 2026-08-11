# case-003 — expected: expose report subscriptions to team leads, no recent-slice evidence needed

**In-contract expectation:** with no review, retro, or backlog at all, the
response still recommends exposing `ReportScheduler.subscribe()` to team
leads -- some minimal path (UI, command, or API) that lets an actual team
lead create/view/cancel a subscription to their own reports -- and
explicitly names the missing recent-slice evidence as a process gap
without treating it as blocking.

**Grounded in SKILL.md:** "Gather before recommending" states recent-slice
evidence is "supplementary here, not the primary organizing evidence...
its absence is not grounds to stop." Steps 1-3 (demonstrated intent,
current capability set as wired in, traceable workflows) stand on their
own: `docs/onboarding.md` names team leads as the intended user of report
subscriptions, `ReportScheduler.subscribe()` is real and running in
production (for the internal admin team, not team leads), and no team
lead has ever reached it. This is squarely "Discoverability and legibility
of existing capability."

A response that declines to recommend anything because no review/retro
exists, or that invents an unrelated feature, does not meet the bar.

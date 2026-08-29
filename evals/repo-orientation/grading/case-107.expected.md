# Expected orientation outcome (for grading, not shown to the agent under test)

**Failure mode:** current path that looks experimental.

**In-contract.** The mirror image of case-103/106: `experimental/
ratelimiter.py` is imported by `src/middleware.py`, which decorates the
`/checkout` route in `src/app.py` — a fully wired production path — despite
living in a directory named `experimental/`. The module's own docstring
even explains the naming is a holdover from when it started as a spike.
SKILL.md's reachability-over-naming rule applies exactly as it does to
`legacy/`-named code that turns out to be live; the direction of the
mistake (dismissing something as a prototype) is the one this case
isolates.

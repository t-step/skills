# Expected slice-plan outcome (for grading, not shown to the agent under test)

**Scenario type:** stale/secondhand structural claim vs. deterministic
wiring. This case tests whether slice-plan grounds an invariant in
what's actually, directly readable in the repo
(`app/jobs/registry.py`'s `JOB_REGISTRY` manifest) rather than
deferring to a secondhand claim relayed in the prompt ("a teammate ran a
reference-index lookup ... zero callers ... probably dead").

**What's actually true:** `purge_stale_sessions()` is not dead. It's
scheduled in `app/jobs/registry.py`'s `JOB_REGISTRY`, resolved by a job
runner via a dotted-path string at execution time -- exactly the shape
of dynamic dispatch a static reference-index lookup would plausibly
miss (no direct Python call site for it to find). It calls
`record_event()` directly in its own body. If the plan accepts the
"dead, skip it" premise and only updates `handlers.py`'s call site, the
accepted slice's own acceptance evidence ("no code path writes an audit
event without [actor_id] after this slice ships") is violated by the
very call site the plan chose to skip.

**In-contract expectation:**

1. The plan does not accept the "probably dead, skip it" premise at
   face value. It grounds `purge_stale_sessions()`'s liveness
   specifically in `app/jobs/registry.py`'s `JOB_REGISTRY` entry (the
   deployed manifest), not in a general assertion that the teammate is
   wrong.
2. Likely implementation seams includes updating `purge_stale_sessions()`'s
   `record_event()` call in `app/jobs/cleanup.py` (passing
   `actor_id="system"` or an equivalent), in addition to
   `handlers.py::create_order`'s call site -- not only the one the
   prompt suggested keeping.
3. Invariants (or an equivalent section) explicitly states that every
   call site, including scheduled/system jobs, must pass actor_id --
   consistent with the recommendation's own acceptance evidence -- and
   that skipping a call site would leave a code path writing audit
   events without one.
4. Verification strategy covers both call sites' updated audit entries
   (or at minimum names both, not only handlers.py's), scoped to this
   slice's actual change -- not a broader audit of every function or
   module in the codebase.
5. The plan does not expand beyond this slice while correcting the
   premise -- e.g., it does not propose auditing the whole codebase for
   other secondhand-index claims, does not touch `weekly-digest`'s
   `send_weekly_digest` (unrelated, not part of this slice, and not
   even implemented in this fixture), and does not redesign
   `JOB_REGISTRY` or the job-dispatch mechanism itself.
6. The question must not be left artificially unresolved: the plan
   picks a side (grounded in the manifest) and proceeds, rather than
   presenting "maybe it's dead, maybe it isn't" as an open question for
   someone else to resolve later. If the plan names the disagreement
   with the teammate's claim explicitly (e.g. in Known risks or inline,
   including *why* a static index would plausibly miss a
   dynamically-dispatched call site), that's a stronger result but not
   strictly required, provided outcomes 1-5 hold -- the hard
   requirement is that the false premise doesn't produce an incomplete
   or unsafe plan, not that the disagreement gets a specific label.

**Contract framing:** grounded in SKILL.md's "The real codebase, read,
not guessed" gather-before-planning discipline and its invariants
guidance ("A contract something else already depends on... a property
the accepted slice's own goal depends on staying true"). This case
specifically probes whether that discipline holds when the pressure to
skip verification comes from an authoritative-sounding secondhand
technical claim rather than from a direct request to expand or shrink
scope -- the same failure shape already validated for `repo-orientation`
(case-113) and `next-best-slice` (case-118), applied here to
slice-plan's invariants/seams sections specifically.

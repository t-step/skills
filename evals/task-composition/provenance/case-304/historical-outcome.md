# Historical outcome — case-304 (KEP-753 Sidecar Containers)

This is what actually happened after the chosen cutoff (2023-08-30). None
of this is in the agent-visible fixture; it's here so a grader can judge
whether a proposed slice plan's *reasoning* holds up, without treating this
sequence as the one correct answer a tested run needed to reproduce (per
this suite's own convention: historical execution is evidence, not an
oracle — see `evals/task-composition/real-world-tests/README.md`).

## What actually happened, in order

1. **REGR-120247 got a dedicated, separate fix the very next day.** PR
   #120281 ("Feature-gate SidecarContainers code in
   pkg/kubelet/kuberuntime") opened 2023-08-31 01:09 UTC and merged
   2023-09-06 — a third PR, distinct from both same-day drafts
   (#120267, the "DO NOT MERGE" e2e repro, and #120269, "Restart
   containers in right order..."). #120269 itself did not merge until
   2023-10-31, the same day as the CPU-manager fix (see below) — so the
   two draft PRs open at cutoff did *not* turn out to be duplicates of the
   same fix; multiple distinct changes were ultimately needed for this
   thread, consistent with the fixture's deliberate choice not to present
   a single resolution as settled.
2. **The e2e CI job merged six days after cutoff.** `test-infra`#30281
   merged 2023-09-05.
3. **Ownership of the device-manager fix was settled through a short,
   explicit exchange, not silent assumption.** On 2023-09-05, `gjkim42`
   asked `ffromani` directly whether they were working on it; `ffromani`
   said not yet and offered to review; `gjkim42` took it. PR #120461
   opened the next day, 2023-09-06.
4. **The memory-manager fix followed shortly after.** PR #120715 opened
   2023-09-17.
5. **A stated priority first appeared for the resource-manager cluster on
   2023-09-16** — over two weeks after this fixture's cutoff — when
   `gjkim42` commented "/priority important-soon ... I'd like this to be
   addressed before SidecarContainers graduates to the beta." This is the
   only place in the entire real record where a beta-graduation deadline is
   explicitly tied to *that* cluster of fixes; it postdates the cutoff and
   is not in the agent-visible fixture. (REGR-120247, a separate item, did
   get a priority label — `priority/important-soon` then
   `priority/critical-urgent` — on the cutoff date itself; that fact is
   correctly included in the agent-visible fixture. See
   `dependencies.md`'s "No stated priority (one exception)".)
6. **Three of the four "manager" fixes landed within about 24 hours of
   each other, two months after being named.** CPU-119447 (#119447) and
   DEV-119442 (#120461) both merged 2023-10-31; MEM-119442 (#120715)
   merged 2023-11-01. The umbrella issue #119442 was closed the same day
   as the first two merges (2023-10-31→2023-11-15 comment: "this is
   fixed... please reopen if anything is left"), with the topology-manager
   checkbox in its body never checked and never linked to a PR.
7. **The topology-manager work did not follow the same timeline at all.**
   Issue #119407 saw no further activity for nearly a year after its
   2023-07-19 self-assignment. The first substantive follow-up (a
   cross-reference from an unrelated internal tracking issue) appears in
   2024-10-17, and the first actual PR against it, #129951 ("Add e2e test
   for topology manager with restartable init containers"), doesn't open
   until 2025-02-03 — roughly 18 months after cutoff, and after the
   umbrella issue that named it had already been closed as "fixed" for
   over a year.
8. **E2E-119019 (the kubelet-restart simulation test) took far longer than
   any of the manager fixes.** It merged 2024-07-24 — almost a full year
   after this fixture's cutoff, and about nine months after the manager
   fixes it shares an "e2e coverage for sidecars" theme with, but no
   dependency relationship, had already landed.
9. **HPA-119991's fix (PR #120001) merged 2023-10-23**, in the same
   general window as the manager fixes but via a completely separate,
   uncoordinated PR in a different subsystem, exactly as `dependencies.md`
   describes.

## What this means for grading

The historical shape — one fix following within a day, three fixes
converging near-simultaneously two months later, one item stalling for a
year and a half despite being named in the same umbrella title as the
other three, and a priority signal that only appeared weeks after this
fixture's cutoff — is offered as background, not as a required grouping.
A plan-under-test that reaches a *different* defensible slice boundary for
the manager cluster (e.g., treating CPU/memory/device as one grouped
follow-up item, or as three explicitly-named separate ones) should not be
penalized just because history happened to land three of them within a
day of each other; nor should a plan be penalized for not predicting that
the topology-manager item would stall for 18 months, since nothing in the
cutoff-visible record states or implies that outcome. What a plan *should*
get right is recognizable without any of this hindsight: that the four
"manager" items were not, as of cutoff, at the same stage of readiness or
commitment, and that presenting them as four equally-scoped, equally
staffed, symmetric parallel tasks overclaims what the record actually
supports at that point in time.

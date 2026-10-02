# Source notes: KEP-753 Sidecar Containers — post-alpha resource-manager fallout

**Where this came from:** the `kubernetes/kubernetes` GitHub issue tracker
and pull requests, plus one pull request against `kubernetes/test-infra`,
plus the KEP-753 design document itself
(`kubernetes/enhancements`, `keps/sig-node/753-sidecar-containers`). All
task descriptions above are taken from the tickets' and PRs' own text as
filed — nothing has been reworded to sound cleaner or more decomposed than
it actually is. MEM-119442 and DEV-119442 in particular are genuinely
that thin right now: a maintainer's comment pointing at a code location,
nothing more — not summarized down from something richer.

**KEP-753's own design write-up already named part of this risk, but not
all of it.** The KEP's "Topology and CPU managers" section states: "The
biggest question is resources reuse for sidecar containers and other init
containers, especially in cases of single NUMA node requirements and such.
This may be non-trivial. The decision on this is not blocking the KEP
though," and separately lists Container Manager, CPU Manager, Memory
Manager, and Topology Manager (with specific code line references) as
places where "all the containers... were coalesced before resources...
are allocated to them." Device Manager is not named in that list — its
version of the same problem surfaced later, from a maintainer's ad hoc
code-reading during the CPU-manager bug thread, not from the KEP's own
design-time analysis.

**Already landed, not remaining work:**
- The core `SidecarContainers` feature itself (the API field, admission,
  and most of the kubelet wiring) merged in a single large pull request,
  #116429 ("Add SidecarContainers feature"), well before any of the items
  above were filed. Everything above is fallout discovered after that PR
  landed, not part of implementing it.
- `kubectl describe nodes` showed the wrong resource total for a pod with
  a restartable init container (a separate, kubectl-display-only bug, not
  a kubelet resource-manager issue). It was reported and fixed within
  about four weeks by a small, already-merged pull request.
- A separate report that `LimitRanger` (an admission-control resource
  policy, unrelated to any kubelet resource manager or to the autoscaler)
  didn't account for a restartable init container's resources was filed
  and closed within two days.

Neither of the two already-landed items above is part of the remaining
work below — they're included only so the remaining work isn't confused
with, or padded by, things that are already done.

**A thematically similar but unrelated report, seen in the same search and
deliberately not included as a task:** a separate open question about
what should happen when a restartable init container's *startup probe*
fails in a pod with `restartPolicy: Never` — this is about container
restart/lifecycle semantics, not resource accounting, and nothing in its
text connects it to any of the resource-manager, autoscaler, or
e2e-coverage items above.

**Stated milestones:** the KEP's own milestone table (unchanged since
before any of this fallout was filed) targets alpha for the 1.28 release
(already shipped) and beta for the 1.29 release. No comment on any issue
or PR above states a required-by date, a "must land before beta" priority,
or any other deadline.

# Dependencies: KEP-753 Sidecar Containers — post-alpha resource-manager fallout

Only what's stated or clearly inferable from the issues and pull requests
themselves is listed here. Several of these items are genuinely
unresolved as filed — left open below rather than resolved, because the
record itself doesn't resolve them.

## Stated or clearly inferable

- **E2E-119014 depends on both E2E-119019 and E2E-30281.** The umbrella
  e2e-coverage issue's own checklist lists "add serial e2e tests w/
  SidecarContainers feature" (E2E-119014) after "add serial e2e tests w/o
  SidecarContainers feature" (E2E-119019) and "add the test-infra job for
  serial e2e tests w/ SidecarContainers feature" (E2E-30281), in that
  order. Neither of the first two has landed yet, so E2E-119014 has no
  landed harness or CI job to build on.
- **CPU-119447, MEM-119442, and DEV-119442 share one discovered root
  cause**, not three independently-conceived ones. The thread on
  kubernetes/kubernetes#119442 shows the CPU manager bug reported first,
  then a maintainer pointing out the memory manager's `AddContainer` logic
  has "the identical" pattern, then the device manager confirmed to have
  it too, in the same conversation, within a few hours of each other. Each
  is still its own fix in its own package (no shared file), but they are
  not independent discoveries.
- **REGR-120247's suspected root cause is the already-landed base
  SidecarContainers PR, not any of the other open items above.** The
  kubelet maintainer who diagnosed it pointed specifically at insufficient
  feature-gate guarding in that PR's kubelet-side changes — a different
  code path and a different kind of bug (general init-container lifecycle
  ordering) than the resource-manager coalescing issue behind
  CPU-119447/MEM-119442/DEV-119442/TOPO-119407.

## Open questions the record does not resolve — flag, don't guess

- **Whether TOPO-119407 is really the same effort as
  CPU-119447/MEM-119442/DEV-119442, or a separate, lower-commitment
  thread, is not stated.** It concerns the same underlying pattern
  (topology manager also coalesces containers without accounting for
  restartable init containers) and is even referenced by name in
  kubernetes/kubernetes#119442's own title. But it lives in a different
  issue, has no engagement beyond the reporter's own next-day
  self-assignment (with a stated intent to look at e2e tests first) and a
  maintainer's same-day triage acceptance — no maintainer analysis
  pinpointing a code location, no proposed fix, and no pull request — a
  materially thinner state than even MEM-119442/DEV-119442, which at least
  have a maintainer naming the exact code location. Don't assume it will
  be delivered on the same timeline or by the same mechanism as the other
  three; also don't assume it's unrelated just because it's a separate
  issue.
- **Whether MEM-119442 and DEV-119442 will each need their own,
  independently-designed fix, or can mostly copy the approach
  CPU-119447 lands on, is not stated.** The record only establishes they
  have the same *symptom pattern* (AddContainer-style coalescing), not
  that a single fix or a single PR will cover more than one manager — no
  one has proposed a shared fix, and each manager's `AddContainer` lives
  in its own package with its own container-state tracking.
- **REGR-120247's actual fix is not yet settled.** As of right now, the
  assignee has two draft pull requests open from the same day — one
  explicitly marked not for merging (an e2e reproduction for a related
  scenario, still unreviewed) and one proposing a specific
  containers-restart-order fix, which two reviewers began commenting on
  the same day with a live, unresolved disagreement over whether that
  targeted fix is sufficient or whether the safer path is restoring the
  pre-1.28 behavior behind the feature gate — and it isn't established
  whether closing this issue will take one fix or more than one. Don't
  present either draft, or either reviewer's preferred approach, as the
  agreed resolution.

## Shared-area signal, not a stated dependency

CPU-119447, MEM-119442, and DEV-119442 all describe the same coalescing
pattern (containers, including restartable init containers, are grouped
together before the manager allocates CPU/memory/devices to them) in three
different manager packages (`cpumanager`, `memorymanager`,
`devicemanager`). No ticket states a shared file between them, and CPU's
own PR (#119447) doesn't touch memory or device manager code. This is a
signal worth checking once CPU-119447's approach is settled — a similar
fix shape may well apply to the other two — not, on its own, evidence that
they must be sequenced after CPU-119447 or merged into one slice.

HPA-119991 addresses conceptually the same gap (something in the system
undercounts a restartable init container's resource footprint) as the
CPU/MEM/DEV cluster, but in a completely different subsystem
(kube-controller-manager's autoscaler replica calculator, not any kubelet
resource manager), a different file, and a different PR author. Nothing
in either issue references the other. Thematic similarity here is not
evidence of a dependency or a shared file.

REGR-120247 and the e2e-coverage items (E2E-119019, E2E-30281, E2E-119014)
all concern kubelet behavior around container startup ordering and restart
handling, and a working e2e harness would eventually be a reasonable place
to add a regression test for REGR-120247's scenario. But nothing in either
thread references the other, and they were opened independently, months
apart, by different people for different stated reasons. Do not infer a
blocking relationship from the shared general subject matter alone.

## No stated priority (one exception)

None of these issues or pull requests carry a priority label or milestone
assignment beyond the KEP's own alpha/beta targets (see
`source-notes.md`), with one exception: REGR-120247 was labeled
`priority/important-soon` and then, a couple of hours later the same
afternoon, `priority/critical-urgent` — both applied the day it was filed,
by the assignee and the escalating senior reviewer respectively. No other
item in this list carries any priority label. This is evidence that
REGR-120247 was being treated with more urgency than everything else here,
not evidence for ranking any of the other items against each other or
against REGR-120247 on a KEP-beta timeline — nothing here should be
treated as "the priority" for the resource-manager cluster or the
e2e-coverage items without inventing a signal the record doesn't contain
for them specifically.

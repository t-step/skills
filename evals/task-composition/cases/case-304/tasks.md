# Tasks: KEP-753 Sidecar Containers — post-alpha resource-manager fallout

This is the current state of the open work, pulled from GitHub issues and
pull requests against `kubernetes/kubernetes` (and one against
`kubernetes/test-infra`), sorted by issue/PR number. There is no other
roadmap document for this cleanup beyond what's written here and in the
umbrella tracking issue referenced below.

- **CPU-119447** — CPU manager doesn't account for restartable init
  containers. Filed as kubernetes/kubernetes#119442: when the CPU manager's
  static policy is active and a Guaranteed-QoS pod has a restartable init
  container (an init container with `restartPolicy: Always` — it keeps
  running alongside the pod's regular containers instead of exiting), the
  restartable init container ends up sharing its allocated CPU set with a
  regular container, when it shouldn't (the two run concurrently for as
  long as the pod is up, unlike an ordinary init container which exits
  before regular containers start). PR #119447 ("Don't reuse CPU set of a
  restartable init container") has been open since the issue was filed and
  went through a round of review comments (naming the exact KEP-753 section
  the new resource-calculation rule comes from); the reviewer's open
  questions were addressed and marked resolved. The PR has not merged yet.

- **MEM-119442** — Memory manager doesn't account for restartable init
  containers. Named in the same kubernetes/kubernetes#119442 thread: the
  memory manager's `AddContainer` logic has the identical coalescing
  pattern as the CPU manager's, pointed at a specific line range in
  `memory_manager.go`. The issue's title was updated to include "memory"
  manager once this was raised. No pull request exists for this yet, and
  no one has been assigned to it.

- **DEV-119442** — Device manager doesn't account for restartable init
  containers. Also named in kubernetes/kubernetes#119442: the device
  manager has the same pattern, pointed at a specific line range in
  `devicemanager/manager.go`. The issue's title was updated a second time
  to add "device" manager once this was confirmed. No pull request exists
  for this yet, and no one has been assigned to it.

- **TOPO-119407** — Topology manager doesn't account for restartable init
  containers. Tracked as its own issue, kubernetes/kubernetes#119407, filed
  one day before #119442 by the same reporter. The entire issue body is:
  "make sure the topology manager works fine with restartable init
  containers — found one inconsistency with regular containers [in a
  linked review comment on the original SidecarContainers PR] at least.
  I'll take a look if I have time." The reporter self-assigned the next
  day, commenting that they'd "add e2e tests first to test the topology
  manager in a multi-numa environment"; a maintainer accepted it into
  triage the same day, calling it likely to be "addressed in 1.29." No
  pull request exists, and there has been no further discussion since
  that day.

- **HPA-119991** — HPA doesn't count sidecar container resources. Filed as
  kubernetes/kubernetes#119991: the horizontal pod autoscaler's replica
  calculator sums container resource usage to compute utilization, but
  doesn't include restartable init containers, which (like sidecars) keep
  running for the pod's whole life. This produces an under-counted
  utilization number whenever a pod has one. A pull request, #120001
  ("HPA: calculate sidecar container resource in pod autoscaler"), was
  opened the same day the issue was filed and is under review. It has not
  merged yet.

- **E2E-119019** — Serial e2e test: restartable init container survives a
  kubelet restart. Pull request #119019 ("Add node serial e2e tests that
  simulate the kubelet restart"), open since 2023-07-02 (before the
  resource-manager issues above were even filed), addresses one specific
  scenario requested in review of the original SidecarContainers PR: add a
  restartable init container, wait for it to initialize, stop the kubelet,
  make the restartable init container exit, restart the kubelet, and
  verify it comes back. It has been open for several weeks under review
  and has not merged yet.

- **E2E-30281** — CI job for serial e2e tests with SidecarContainers
  enabled. A pull request against the separate `kubernetes/test-infra`
  repository, #30281 ("Add pull-kubernetes-node-kubelet-serial-containerd-
  alpha-features job"), opened to wire up a CI job that runs the node
  serial e2e test suite with the `SidecarContainers` feature gate turned
  on. It is open and has not merged yet.

- **E2E-119014** — Add the actual serial e2e tests with SidecarContainers
  enabled. Tracked as the last item in a short checklist inside
  kubernetes/kubernetes#119014 ("Add serial e2e tests for
  `SidecarContainers`"), the umbrella issue for this test-coverage effort.
  The checklist's four items, in order, are: E2E-119019, merging the
  original SidecarContainers PR (already done), E2E-30281, and this item.
  This last item — writing the serial e2e tests that actually run *with* the
  feature gate enabled, covering restartable-init-container-specific
  behavior rather than just the ordinary init-container behavior
  E2E-119019 tests without the gate — has no pull request and hasn't been
  started. The checklist lists it after the other three.

- **REGR-120247** — Kubelet may start regular containers before init
  containers finish, specifically after a node reboot. Reported today
  (kubernetes/kubernetes#120247) by an external user running a GPU-driver
  DaemonSet: on node reboot only (not on a fresh pod create), and only
  since upgrading to 1.28, application containers sometimes start running
  concurrently with init containers instead of waiting for them, breaking
  a driver-dependency ordering assumption. A kubelet maintainer (not
  otherwise involved in the sidecar work) looked at the diff for the
  original SidecarContainers PR and commented that very little of its
  kubelet-side code changes are actually guarded by the `SidecarContainers`
  feature gate, and guessed this could be breaking the *ordinary*
  (non-restartable) init-container flow even when the feature gate is off.
  The sidecar feature's own primary author self-assigned within the half
  hour, agreeing "it is practically difficult to guard all new code paths"
  and saying they'd "find a better way to guard the new code path." A
  senior kubelet reviewer (not previously part of this thread) escalated it
  the same afternoon as a possible 1.28 kubelet regression and sketched one
  possible fix approach (compare against the pre-sidecar 1.27 behavior).
  By the end of the day, two draft pull requests exist from the assignee —
  one explicitly marked "[DO NOT MERGE]" adding an e2e reproduction for a
  related scenario (this one has no reviews yet), and one proposing a fix
  to container restart ordering, which the senior reviewer and another
  maintainer began reviewing within the hour: the senior reviewer pushed
  back that the restart-order fix doesn't address every ungated code path
  and that restoring the exact pre-1.28 behavior behind the feature gate
  would be safer, the assignee defended the smaller fix as lower-risk than
  a broad revert, and the exchange was still unresolved when the assignee
  signed off for the night. It isn't settled yet whether one fix, the
  other, or more than one will be needed to close this out. This issue is
  also the one exception to the no-priority pattern below: the assignee
  labeled it `priority/important-soon` mid-afternoon (in the same comment
  reporting the reproduction), and the senior reviewer raised that to
  `priority/critical-urgent` a couple of hours later, around the same time
  the first draft PR went up.

No priority has been marked or stated on any of the other issues or pull
requests beyond Kubernetes' default issue labels (which none of them
have been given yet). The umbrella tracking issue,
kubernetes/kubernetes#119442, is itself not a task — it's a checklist
pointer to CPU-119447, MEM-119442, and DEV-119442 (its own title lists all
three plus topology, though the topology checkbox in its body has no link
or owner attached — see TOPO-119407 above for where that work actually
lives).

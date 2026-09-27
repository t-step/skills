# Repository state

- The `SidecarContainers` feature gate is alpha and defaults to `false`.
  All of the behavior described in `tasks.md` only manifests when a
  cluster operator has explicitly enabled it — none of this is affecting
  a default cluster.

- The base implementation (the API field, admission, and kubelet wiring
  for restartable init containers) is a single already-merged pull
  request. None of the work below touches that PR again except
  REGR-120247, whose suspected root cause is specifically that this PR's
  changes weren't fully guarded behind the feature gate.

- CPU-119447, MEM-119442, and DEV-119442 each live in a different kubelet
  package (`pkg/kubelet/cm/cpumanager`, `pkg/kubelet/cm/memorymanager`,
  `pkg/kubelet/cm/devicemanager` respectively). Nothing in the CPU
  manager's own code is imported by, or shared with, the memory or device
  manager packages for this logic — each manager independently decides
  how to allocate its own resource type and tracks container state
  separately.

- TOPO-119407's own referenced code (`pkg/kubelet/cm/topologymanager`) is
  also a separate package from the other three managers. The topology
  manager coordinates hints from the CPU, memory, and device managers
  once they've each made a decision, but this issue is about the topology
  manager's own handling of restartable init containers specifically, not
  about a fix in one of the other three managers propagating into it.

- HPA-119991's code path (the horizontal pod autoscaler's replica
  calculator) lives in `kube-controller-manager`, a different binary
  entirely from the kubelet, which is where all of CPU-119447,
  MEM-119442, DEV-119442, TOPO-119407, and REGR-120247 live.

- E2E-119019 and E2E-30281 are changes to two different repositories
  (`kubernetes/kubernetes` test code, and `kubernetes/test-infra` CI
  configuration, respectively) that both need to exist before E2E-119014
  can be written and actually run in CI.

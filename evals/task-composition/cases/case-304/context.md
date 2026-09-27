# Context: Kubernetes Sidecar Containers (KEP-753) — post-alpha resource-manager fallout

Sidecar containers (restartable init containers: an init container with
`restartPolicy: Always` that keeps running alongside the pod's regular
containers instead of exiting) went alpha in Kubernetes 1.28, behind the
`SidecarContainers` feature gate. The core implementation merged into
`kubernetes/kubernetes` on 2023-07-08. Beta is targeted for the 1.29 cycle,
per the KEP's own milestone table.

Since alpha landed, a scattered set of bugs and gaps has surfaced across
several kubelet and control-plane subsystems that didn't originally account
for a container that behaves like an init container (runs during the init
stage, ordered) but also behaves like a regular container (keeps running
for the pod's lifetime, needs its resources counted for as long as the pod
runs). The KEP's own design write-up flagged part of this risk in advance
for some subsystems and explicitly deferred it as non-blocking for alpha;
other parts of it were only found afterward, through ad hoc code review and
external bug reports, once real pods with sidecars started running.

This is the current state of that fallout as of right now — pulled
directly from the issue tracker and pull requests, not cleaned up or
pre-sorted into a roadmap. Some items are concrete PRs already under
review; others are only a few sentences in an issue thread with no PR or
owner yet; one surfaced today and nobody yet knows how many fixes it will
take.

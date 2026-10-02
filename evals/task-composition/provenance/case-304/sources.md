# Sources — case-304 (KEP-753 Sidecar Containers)

All accessed 2026-09-26 via the GitHub REST and GraphQL APIs
(`gh api ...`), anonymously (no auth needed for public repos/issues).

## kubernetes/kubernetes

- `issues/119442` (+ `.../timeline`, `.../comments`, and GraphQL
  `userContentEdits`) — the umbrella "Resource(CPU, memory, device,
  topology) managers don't consider restartable init containers" issue.
  Filed 2023-07-19 as a CPU-only bug; retitled 2023-08-03 (adds memory,
  topology) and 2023-08-09 (adds device); closed 2023-11-15. The
  `userContentEdits` GraphQL query was used to reconstruct the issue
  body's checklist state *as it existed on 2023-08-09* (all four manager
  lines present, all unchecked, only the CPU line linked to a PR) rather
  than trusting the current body, which now shows memory/device links
  added in September and checkmarks that postdate this fixture's cutoff.
- `pulls/119447` (CPU manager fix) — opened 2023-07-19, review comments
  2023-08-01 through 2023-08-03 (`pulls/119447/comments`), merged
  2023-10-31 (postdates cutoff; DIAGNOSTIC only).
- `pulls/120461` (device manager fix) — opened 2023-09-06 (postdates
  cutoff), merged 2023-10-31.
- `pulls/120715` (memory manager fix) — opened 2023-09-17 (postdates
  cutoff), merged 2023-11-01.
- `issues/119407` (topology manager) — filed 2023-07-18 by `gjkim42`;
  `gjkim42` self-assigned the next day (2023-07-19) with a comment stating
  intent to "add e2e tests first," and `SergeyKanzhelev` accepted it into
  triage the same day, predicting it would "likely... be addressed in
  1.29" — no further comments after 2023-07-19 through cutoff; timeline
  shows no cross-referenced PR until #129951 in 2025.
- `issues/119014` (+ GraphQL `userContentEdits`) — the e2e-coverage
  umbrella issue, filed 2023-07-02. `userContentEdits` was used the same
  way as #119442's to recover the checklist's pre-cutoff state (item 1,
  merging the base PR, checked; items 2-4 unchecked as of every edit
  through 2023-08-03, the last edit before cutoff) rather than the
  current body, which shows item 2 checked as of a 2024-08-19 edit —
  well after PR #119019 actually merged (2024-07-24) and long after this
  fixture's cutoff.
- `pulls/119019` (e2e kubelet-restart test) — opened 2023-07-02, merged
  2024-07-24 (postdates cutoff by nearly a year; DIAGNOSTIC only).
- `issues/119991` and `pulls/120001` (HPA gap) — both opened 2023-08-17,
  PR merged 2023-10-23 (postdates cutoff).
- `issues/120247` (+ `.../comments`, `.../timeline`) — the kubelet
  init-container regression, reported 2023-08-30 08:04 UTC by `klueska`,
  self-assigned by `gjkim42` 08:36 UTC, escalated by `liggitt` (ccing
  `thockin`) 15:17-15:18 UTC. Closed 2023-09-06. Labels
  (`.../timeline`, event `labeled`) show `priority/important-soon` applied
  14:09:52 UTC (from `gjkim42`'s "/priority important-soon" comment) and
  `priority/critical-urgent` applied 15:52:24 UTC by `liggitt` — the only
  priority label anywhere in this fixture's candidate set; checked and
  folded into `tasks.md`/`dependencies.md` after an initial draft omitted
  it.
- `pulls/120267` ("[DO NOT MERGE]" e2e repro, opened 2023-08-30 15:51 UTC)
  and `pulls/120269` ("Restart containers in right order...", opened
  2023-08-30 16:21 UTC) — both by `gjkim42`, both still open as of this
  fixture's cutoff (end of day 2023-08-30). `#120267` has zero reviews
  through cutoff (`.../reviews` is empty). `#120269` does not: `.../reviews`
  and `.../comments` show `SergeyKanzhelev` and `liggitt` reviewing it
  within an hour of it opening (2023-08-30 16:32-17:02 UTC), with `liggitt`
  arguing the targeted fix leaves other ungated code paths unaddressed and
  that restoring the pre-1.28 behavior behind the feature gate is safer,
  `gjkim42` defending the smaller fix, and the thread still open
  (`gjkim42`: "I'll check it again tomorrow") at cutoff — checked and
  corrected into `tasks.md`/`dependencies.md` after an initial draft
  called both PRs "unreviewed."
- `pulls/120281` ("Feature-gate SidecarContainers code in
  pkg/kubelet/kuberuntime") — opened 2023-08-31 01:09 UTC, i.e. after this
  fixture's cutoff by design (see `cutoff-rationale.md`); fixes #120247;
  merged 2023-09-06. DIAGNOSTIC only.
- `issues/119406` and `pulls/119509` (kubectl describe-nodes display bug)
  — filed/opened 2023-07-18/2023-07-21, PR merged 2023-08-16 — already
  landed before cutoff.
- `issues/120163` (LimitRanger gap) — filed 2023-08-24, closed 2023-08-25
  — already landed before cutoff.
- `issues/120234` (restartPolicy-Never / startupProbe semantics question)
  — filed 2023-08-29; checked and deliberately excluded (see
  `cutoff-rationale.md`).
- `pulls/116429` ("Add SidecarContainers feature", the base alpha
  implementation) — merged 2023-07-08.
- GitHub code search (`gh search issues` / `gh search prs`) over
  `kubernetes/kubernetes`, filtered `created:2023-07-01..2023-08-31`, for
  "restartable init container" and "sidecar" — used to find the full set
  of candidate items in the window (including the ones excluded above)
  rather than relying only on the numbers named in the original research
  brief.

## kubernetes/test-infra

- `pulls/30281` ("Add pull-kubernetes-node-kubelet-serial-containerd-
  alpha-features job") — opened 2023-08-03, merged 2023-09-05 (six days
  after cutoff; DIAGNOSTIC only, since nothing in the record as of cutoff
  states or implies a specific landing date).

## kubernetes/enhancements (KEP-753 text)

- `repos/kubernetes/enhancements/commits?path=keps/sig-node/753-sidecar-
  containers/README.md&since=2023-01-01&until=2023-10-01` — confirmed the
  KEP text was last substantively edited 2023-04-27 and not touched again
  until 2023-09-29 (after cutoff), so the April revision is what was live
  throughout this fixture's entire candidate window.
- `raw.githubusercontent.com/kubernetes/enhancements/f494a1bfa/keps/
  sig-node/753-sidecar-containers/README.md` and `.../kep.yaml` at that
  same commit (`f494a1bfa`) — fetched directly (the `contents` API 404'd
  for this path/ref combination; raw.githubusercontent.com worked) to
  read the exact "Topology and CPU managers" section and milestone table
  as they existed during the fixture's window, rather than today's KEP
  text (`status: implemented`, `last-updated: 2025-01-23`), which has been
  rewritten multiple times since.

## Excluded candidate (from the original research brief)

- `issues/121375` ("Move SidecarContainers featureGate checking from
  Filter to PreFilter in scheduler") — checked directly: filed
  2023-10-20, six weeks after this fixture's cutoff. Not included in the
  fixture at all (not even as DIAGNOSTIC/historical-outcome material,
  since it isn't part of this window's story). The original research
  brief listed it as a candidate; verification ruled it out.

# Cutoff rationale — case-304 (KEP-753 Sidecar Containers)

## Chosen cutoff

**2023-08-30, end of day (UTC).** Every task in the fixture reflects only
information that existed by then. The one item discovered *on* the cutoff
date (REGR-120247) is included specifically because its own record shows a
same-day escalation, a priority label, two draft PRs (one reviewed same-day
with a live, unresolved disagreement over approach, one not yet reviewed at
all), and no agreement on which approach (or how many fixes) will actually
close it out — it is presented as unresolved, not as a settled fix, which
is the accurate state at that exact moment.

## Why this point is defensible

1. **It sits inside a real, dense burst of related activity, not an
   arbitrary date.** Between 2023-07-02 (issue #119014 filed) and
   2023-08-30 (the REGR-120247 escalation), nine directly relevant
   issues/PRs were filed across `kubernetes/kubernetes` and one against
   `kubernetes/test-infra`, following the alpha implementation's merge on
   2023-07-08. This reads as a real post-alpha triage period, not a
   backlog assembled after the fact.
2. **The cutoff sits before several outcomes were known, on fronts that
   were genuinely live at the time:**
   - Whether the CPU-manager PR (#119447) — open six weeks by this
     point — would merge cleanly was not yet resolved (it merges two
     months later, 2023-10-31).
   - Memory and device manager had been *named* as needing the same class
     of fix (memory since 2023-08-03, device since 2023-08-09) but neither
     had a PR, an assignee, or even a scoping conversation yet (that
     conversation, between `gjkim42` and `ffromani` about who'd take
     device manager, doesn't happen until 2023-09-05).
   - The e2e test-infra CI job (`test-infra`#30281, opened 2023-08-03) had
     not yet merged (it merges 2023-09-05, six days after this cutoff) —
     a later cutoff by even a week would silently hand the fixture a
     "done" item that, as of 2023-08-30, is still an open PR with no
     stated ETA.
   - REGR-120247 had been reported and escalated to senior reviewers that
     very day, with two competing draft fixes open — one still unreviewed,
     one under active, unresolved same-day review disagreement — and
     neither settled on as the fix. Its actual resolution (PR #120281)
     does not open until the next day
     (2023-08-31 01:09 UTC) and doesn't merge until 2023-09-06. A cutoff
     even a few hours later would risk pulling in that PR and turning a
     genuinely open, multi-draft situation into what looks like a settled
     one.
3. **Choosing the exact end of 2023-08-30 (rather than, say, 2023-08-31)
   is a deliberate boundary decision, not a rounding convenience:** PR
   #120281 opens at 2023-08-31 01:09 UTC, less than an hour into the next
   day. Ending the window at 2023-08-30 keeps REGR-120247 in its true
   "just discovered, still being investigated" state — which is more
   representative of the "post-alpha ... discovered dependencies" dynamic
   this case is meant to test — rather than letting the fixture imply a
   fix already existed. HUDI-2452's treatment in case-303 (an unresolved
   externally-reported bug, deliberately not force-connected to anything
   else) is the closest analog in this suite to how REGR-120247 is
   deliberately left unresolved here.
4. **A later cutoff (e.g. through 2023-09-17, when the memory manager PR
   opens) was considered and rejected.** It would let all three
   manager-fix PRs (CPU, memory, device) exist side by side, which is
   tempting — it would make "the four-manager cluster" look like a
   cleaner, more symmetric set of parallel PRs. That symmetry is exactly
   the thing this case exists to pressure-test, and using a cutoff that
   manufactures it (by waiting until three of the four have PRs) would
   undercut the case rather than strengthen it. The chosen, earlier cutoff
   instead shows the four "manager" items in their honestly asymmetric
   state: one PR in review, two named-but-unowned, one tracked separately
   with even less commitment than the other two.

## Adversarial provenance audit (before any fixture file was written)

A full historical-fact / supported-grading-constraint / not-supported
pass was done for every candidate topology claim before writing
`tasks.md`/`dependencies.md`. The findings are summarized here since they
directly shaped what is and isn't in the fixture; the full audit note
(five candidate constraints, worked in the same three-part format) is not
itself a fixture artifact and is not reproduced verbatim, but every
conclusion below is drawn from it.

- **The four "manager" items are not interchangeable, even before any
  hindsight.** CPU-119447 has an actively-reviewed PR; MEM-119442 and
  DEV-119442 have zero PR/assignee activity; TOPO-119407 is tracked in a
  *separate* issue with an even thinner commitment (a bare TODO, a
  next-day self-assignment and same-day triage acceptance with no
  code-location analysis, no follow-up after that, no PR) than either of
  those two. This is a
  plan-time fact, not a hindsight one — verified without needing to know
  that, historically, three of the four eventually landed within a day of
  each other (2023-10-31/11-01) while the fourth didn't get any PR at all
  for well over a year (a topology-manager e2e test PR, #129951, doesn't
  appear until 2025-02-03). That later outcome is DIAGNOSTIC only (see
  `historical-outcome.md`) and is not knowable at cutoff.
- **The KEP's design text partially anticipated this, but not uniformly.**
  It named CPU/Memory/Topology Manager coalescing as a known,
  deliberately non-blocking risk as far back as the KEP's April 2023
  revision (unchanged through this fixture's entire window). It did not
  name Device Manager — that surfaced only from an ad hoc code-reading
  comment during the CPU-manager bug thread. A plan that treats "device
  manager's gap" and "topology manager's gap" as equally foreseen would be
  overstating the record.
- **"Genuinely parallel-safe" for the manager cluster is not established
  by the record, and was independently checked rather than assumed from
  the original research framing.** No shared file exists between the
  three managers' packages (confirmed in `repository-state.md` and by
  `pulls/119447`'s own file list touching only `pkg/kubelet/cm/
  cpumanager`). The record supports treating them as three separately
  fixable items sharing one discovered pattern — it does not establish
  they are on the same timeline, will use the same fix shape, or must be
  sequenced relative to each other. Both a three-separate-slices reading
  and a one-slice-with-named-sub-items reading are defensible; the
  grading key (see `grading/case-304.expected.md`) does not mandate a
  specific slice count for this cluster.
- **REGR-120247 was deliberately kept as one unresolved item, not split
  into "the bug" and "the two draft PRs."** Both drafts are same-day,
  same-author artifacts of one still-forming investigation; splitting them
  into separate tasks would manufacture task/PR identity as slice
  identity, which is the specific failure mode this case is built to
  surface (see the case-303 precedent: two Jira tickets are a task-identity
  fact, not automatically a slice-identity fact).

## Which target dynamics this cutoff does and does not support

- **Genuine independently-executable work:** yes — HPA-119991 sits in a
  different binary (`kube-controller-manager`) with no file or code
  overlap with anything else in the fixture.
- **A shared root cause producing multiple downstream fixes:** yes —
  CPU-119447/MEM-119442/DEV-119442 (and, more weakly, TOPO-119407) all
  trace to the same "containers get coalesced without accounting for a
  restartable init container" pattern, discovered in one comment thread.
- **Shared verification/convergence requirements:** yes — E2E-119014 is
  explicitly gated on E2E-119019 and E2E-30281 both landing, per the
  umbrella issue's own checklist order.
- **Dependencies discovered after alpha:** yes — the entire fixture is
  post-alpha fallout from a single already-merged PR; REGR-120247 in
  particular was discovered and escalated on the cutoff date itself.
- **External or cross-component constraints:** present but modest — HPA's
  gap crosses a binary boundary (kubelet vs. controller-manager), but
  there's no community-process external blocker in this window comparable
  to case-302's CASSANDRA-18112 (a mailing-list DISCUSS gate). Not
  claimed here.
- **Already-landed work that should not remain in the open plan:** yes —
  the base SidecarContainers PR (#116429), the kubectl describe-nodes fix
  (#119509), and the LimitRanger fix (issue #120163) are all deliberately
  presented as repository-state/context, not as tasks.
- **Distinction between implementation dependency and integration/release
  dependency:** present in a limited form — the KEP's alpha/beta milestone
  split is stated context, but no comment in this window's record ties
  any specific item to "must land before beta" (that framing appears only
  in a 2023-09-16 comment, after this cutoff, and is therefore
  DIAGNOSTIC-only, not agent-visible).
- **A benchmarking/performance-verification task, or a numeric-order
  illusion:** not well supported at this cutoff and not claimed. The
  closest candidate to a numeric-order trap (issue numbers roughly
  tracking filing chronology here, same as case-303) doesn't produce a
  strong instance; this should not be graded as something a correct run
  was expected to surface.

## Task count

Nine agent-visible tasks survive the audit above, below the ~10-18 range
named in the original research brief. This is treated as an honest
property of this specific slice of history: a five-to-nine-week post-alpha
triage window around one feature is genuinely smaller and less prolific
than the multi-year Jira epics used for cases 301-303. Two considered ways
to reach a higher count were rejected as manufacturing rather than
reflecting evidence: (a) padding with the deliberately-excluded,
thematically-adjacent issues (kubectl describe-nodes, LimitRanger,
restartPolicy-Never semantics) as if they were open remaining work, when
the record shows two of them already resolved and the third genuinely
unconnected; and (b) splitting REGR-120247's same-day, same-author,
not-yet-resolved draft PRs into separate tasks, which would manufacture
task identity from PR identity — the exact failure mode this case exists
to test.

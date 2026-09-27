# Cutoff rationale — case-306 (Apache Kafka KIP-405 Tiered Storage, early SPI window)

## Adversarial provenance audit (before any fixture file was written)

This section works through every candidate topology claim named in the
research brief, in the historical-fact / supported-grading-constraint /
not-supported format the brief requested. All primary-source citations
are in `sources.md`. This audit was done before `tasks.md`/
`dependencies.md` were drafted, and every fixture-construction choice
below traces back to it. Unlike case-305 (which tested whether a run
would correctly *decline* to over-merge coupled work), this case's
central hypothesis runs the other direction — does a real shared
prerequisite deserve independent slice identity — so several claims below
are checked specifically for whether the record supports the *stronger*
conclusion (a real enabler exists) rather than only the weaker one.

### Claim 1: "KAFKA-9548 was a shared prerequisite."

- **Historical fact:** KAFKA-9549's own filed description states its
  implementation is "the `RemoteStorageManager` defined as part of the
  SPI for Tiered Storage." KAFKA-9555's own filed description points to
  the KIP's `RemoteLogMetadataManager` section. The KIP's own text (v118)
  describes `RemoteLogManager` (KAFKA-9550) as delegating to "a pluggable
  storage manager (viz. `RemoteStorageManager`)" and maintaining metadata
  "through `RemoteLogMetadataManager`," and describes the remote fetch
  path (KAFKA-9579) as calling `RSM.fetchLogSegmentData(...)`. All four
  tickets' own stated scope textually names one or both SPI interfaces
  that KAFKA-9548 defines.
- **Supported grading constraint:** A plan may treat KAFKA-9548 as a
  named, textually-established prerequisite for at least KAFKA-9549,
  KAFKA-9550, KAFKA-9555, and KAFKA-9579 — not as an unrelated, merely
  co-filed task.
- **Not supported:** "Prerequisite" here is a stated *textual*
  dependency (these four items' own descriptions or the KIP's own
  language name the SPI), not a *proven blocking* one — see Claim 5/6
  below on whether it had to be finished first.

### Claim 2: "The SPI unlocked multiple consumers."

- **Historical fact:** Four tickets in this window (KAFKA-9549, -9550,
  -9555, -9579) textually consume the SPI, as established in Claim 1.
  They also carry **distinct assignees-at-cutoff for at least two
  genuinely separate tracks**: Satish Duggana (KAFKA-9548 SPI itself,
  plus -9550 and -9555, RLM's copy path and the topic-based RLMM default)
  versus Alexandre Dupriez (KAFKA-9549's local implementation and,
  separately, KAFKA-9564's integration-test framework). KAFKA-9579 (RLM's
  fetch path) is assigned-at-cutoff to a fourth person, Ying Zheng — the
  same person assigned to KAFKA-9569 (HDFS); this was verified against
  KAFKA-9579's full Jira changelog, which shows its only assignee change
  (Ying Zheng → Satish Duggana) happened 2023-02-23, three years after
  this cutoff (the live API's "current assignee" field is not the
  cutoff-time value for this one ticket — see `sources.md`'s
  assignee-history correction). Two additional tickets, KAFKA-9565 (S3)
  and KAFKA-9569 (HDFS), are also textually SPI-consuming and carry two
  further distinct assignees (Ivan Yurchenko, Ying Zheng) — see Claim 3
  for why these two do not count on equal footing.
- **Supported grading constraint:** A plan may recognize that the SPI has
  more than one real, named, distinctly-scoped downstream consumer within
  this window (at minimum KAFKA-9549 under one assignee and KAFKA-9550/
  -9555 under a second), across at least two different people's work.
  KAFKA-9579 is a third, real, textually-established consumer (Claim 1)
  but must not be assumed to share KAFKA-9550/-9555's assignee — at
  cutoff, it shares an assignee with KAFKA-9569 instead.
- **Not supported:** The mining pass's framing ("SPI unlocks S3/HDFS/
  Azure as separate parallel backend teams") overstates what the record
  shows — Azure (KAFKA-12458) was not even filed until **2021-03-12**,
  more than a year after this window, and is excluded entirely as
  post-cutoff; S3 and HDFS require their own claim-level scrutiny (Claim
  3) before being counted as "the same kind of consumer" as KAFKA-9549/
  -9550/-9555/-9579.

### Claim 3: "Those consumers [downstream implementations] were independently useful." — tested specifically against KAFKA-9565 (S3) and KAFKA-9569 (HDFS)

- **Historical fact:** The KIP's own v118 "Public Interfaces" text states,
  in the same paragraph that introduces `RemoteStorageManager`: "HDFS and
  S3 implementation are planned to be hosted in external repos and these
  will not be part of Apache Kafka repo. This is inline with the approach
  taken for Kafka connectors." KAFKA-9569's own filed description states
  its purpose is "to verify the proposed SPIs are sufficient" — a
  validation framing, not a committed-deliverable framing, stated by the
  filer at the time of filing, not read in with hindsight.
- **Supported grading constraint:** A plan must not treat KAFKA-9565 and
  KAFKA-9569 as equally-weighted, in-scope production deliverables of
  *this* initiative on the same footing as KAFKA-9549 (the local
  implementation) or KAFKA-9555 (the shipped topic-based default) —
  the record's own design document states these two are intended to live
  outside this repository entirely, and one of the two tickets' own text
  frames itself as an SPI-sufficiency check, not a shipped feature. A
  plan may still list them (they are real, filed, assigned tickets that
  existed at cutoff) but must name this distinction if it uses them as
  evidence for the SPI's enabler status.
- **Not supported:** This does *not* mean KAFKA-9565/-9569 have zero
  value as evidence of demand for the SPI — a plan noting "even
  externally-scoped work needed this interface to be public and
  reasonably documented" is well-supported. What is not supported is
  treating them as two more of "this plan's own downstream slices" with
  no caveat, or using them as the primary count toward "the SPI has many
  consumers" (KAFKA-9549/-9550/-9555/-9579 already establish that
  independent of these two).

### Claim 4: "The SPI was independently verifiable."

- **Historical fact:** KAFKA-9554 (filed one day after KAFKA-9548, closed
  same-day as a duplicate of it) describes what "done" means for
  SPI-defining work: "Package with interfaces and key objects available
  and published for review." No ticket or KIP text describes a runnable
  test, executable contract-verification suite, or CI check for the SPI
  *by itself*, independent of some implementation exercising it. The
  earliest evidence of the interfaces being exercised at all is
  `harshach/kafka#31` (2020-02-17), which bundles interface changes
  *together with* the local implementation and its own test/verifier in
  one PR, three days after filing.
- **Supported grading constraint:** A plan may note that "done" for the
  SPI, as stated at cutoff, means a reviewed, published package of
  interfaces — a real, if narrow, verification bar (compiles, is
  reviewable, has method signatures a downstream implementer can build
  against) — but must not claim a runnable, independent test suite
  verifies the SPI in isolation, because none is described anywhere in
  the record at this cutoff.
- **Not supported:** This is the single most direct tension with
  SKILL.md's own "vertical grouping test" (question 2: can the grouping's
  become-true claim be verified independently?) — see "Which target
  dynamics this cutoff does and does not support" below for how this
  fixture treats it. A plan is not required to conclude the SPI fails
  that test outright; the record supports a modest verification claim
  (reviewed interface, exercised together with a first reference
  implementation), not a strong one (a standalone contract-test suite),
  and this fixture's grading key does not force either conclusion — see
  DEFENSIBLE in `grading/case-306.expected.md`.

### Claim 5: "Backend implementations could proceed in parallel."

- **Historical fact:** KAFKA-9549 (Dupriez), KAFKA-9550/-9555/-9579
  (Duggana), and KAFKA-9564 (Dupriez) are all open, unresolved, and
  carry no stated blocking relationship to each other in Jira
  (`issuelinks` is empty on every one of them). `harshach/kafka#31`
  (2020-02-17) shows SPI-adjacent work and the local implementation
  being developed together in the same fork PR within days of filing —
  not sequentially gated on a finished, frozen interface.
- **Supported grading constraint:** A plan may treat KAFKA-9549's local
  implementation and KAFKA-9564's test framework (Dupriez's track) as
  able to proceed concurrently with Duggana's SPI/RLM/fetch track,
  without inventing a hard "SPI must fully land first" blocking gate for
  every downstream item.
- **Not supported:** This is evidence of *practical, tolerated,
  concurrent early-stage development in an isolated fork*, not evidence
  that the interface was stable enough for independent, uncoordinated
  parallel teams to build against with no risk of rework — see Claim 6.
  A plan claiming "all backend work here was safely parallel with zero
  coordination risk" overclaims; a plan claiming "nothing here could
  start until the SPI froze" underclaims. Both are avoided in this
  fixture's REQUIRED list; the middle ground is left DEFENSIBLE.

### Claim 6: "The interface had to be finalized before downstream work could begin" / "Interface instability made downstream work unsafe."

- **Historical fact:** The KIP's own "Current State" field reads
  "Discussion" (not "Accepted") in every dated version checked from v118
  (2020-02-14) through v340 (2021-02-15) — **the KIP was still formally
  unaccepted one week before the SPI's first official PR merged to
  trunk.** Despite this, `harshach/kafka#31` shows real implementation
  work (interfaces plus a first consumer) proceeding **three days after**
  the tickets were filed, in a fork rather than directly against
  `apache/kafka` trunk.
- **Supported grading constraint:** A plan may note the interface was
  genuinely unratified/provisional at this cutoff (the KIP itself was not
  yet accepted) as a real source of uncertainty about the SPI's eventual
  final shape — and separately note that historical practice did not wait
  for formal acceptance before beginning implementation, instead using an
  isolated development fork rather than the shared trunk. Both facts are
  real and can be named together.
- **Not supported:** Neither fact alone proves the other's conclusion.
  "The KIP was unaccepted" does not mean "downstream work was unsafe" —
  the record shows people proceeded anyway. "People proceeded anyway in a
  fork" does not mean "the interface was stable" — using an isolated fork
  rather than trunk is itself consistent with treating the interface as
  provisional and wanting to shield the main branch from churn. A plan
  asserting either "downstream work was blocked/unsafe until KIP
  acceptance" or "the interface was already stable and settled at
  filing" as a flat, unqualified fact overclaims. This is the fixture's
  analogue of case-305's Claim about feature-gate independence: real,
  dated administrative/process facts exist on both sides, and neither
  settles the underlying engineering question by itself.

### Claim 7: "One historical PR or Jira task corresponded to one slice."

- **Historical fact:** `harshach/kafka#31` bundles SPI-interface changes
  and the local RSM implementation (KAFKA-9549's actual scope) in one PR.
  The eventual *official* `apache/kafka#10173` (merged 2021-03-03, a full
  year after filing) touches *only* interface/data-class files — no
  implementation code at all. The same underlying work (define the SPI)
  had two entirely different PR shapes at two different points in its
  own history: bundled-with-a-consumer in the early fork, then
  interface-only a year later on trunk.
- **Supported grading constraint:** None directly — this claim exists to
  be rejected. A plan is not required or expected to reproduce either
  historical PR's shape; grading must not credit or penalize a run for
  matching or failing to match `#31`'s bundling or `#10173`'s
  separation.
- **Not supported:** "The SPI and its first implementation shipped
  together in one PR historically" does not mean a Feb-2020-cutoff plan
  must (or must not) bundle them into one slice — it is evidence that
  *both* choices are practically workable, not evidence that either one
  is the historically "correct" grouping. Symmetrically, the eventual
  interface-only PR shape a year later is not evidence that a Feb-2020
  plan should isolate the SPI into its own slice either — it is
  DIAGNOSTIC, reflecting how the ticket's scope was eventually curated
  for an official merge long after any Feb-2020 plan would have run its
  course.

### Claim 8: "The architecture intended one shared enabler."

- **Historical fact:** The KIP's own text separates two distinct SPI
  surfaces (`RemoteStorageManager` for data, `RemoteLogMetadataManager`
  for metadata) "since remote storage is separated from the remote log
  metadata store" (KIP v118, "High-level design") — a single Jira ticket
  (KAFKA-9548) covers *both* interfaces together, but the design itself
  treats them as two conceptually separate contracts bundled into one
  ticket, not one indivisible contract.
- **Supported grading constraint:** A plan may name that KAFKA-9548
  bundles two conceptually distinct interfaces (RSM and RLMM) as a
  single Jira-tracked unit, and may choose to preserve that bundling or
  split it — either is defensible (see DEFENSIBLE in the grading key) —
  as long as it does not claim the KIP's design treats them as one
  contract with no meaningful separation.
- **Not supported:** Nothing in the record states the *tickets that
  consume* the SPI (KAFKA-9549/-9550/-9555/-9579) must therefore also be
  merged into "one shared enabler slice" alongside KAFKA-9548 itself —
  that would conflate the enabler with its consumers, the same
  over-merging failure mode this suite has flagged since case-303/304/
  305.

### Claim 9: "Multiple consumers imply mandatory centralization."

- **Historical fact:** KAFKA-9550 (RLM copy path) and KAFKA-9579 (RLM
  fetch path) are described in the KIP's own text as **two separate
  thread pools** ("Remote Log Manager (RLM) Thread Pool" and "Remote
  Storage Fetcher Thread Pool") triggered by different events (a
  scheduled copy interval versus an incoming consumer fetch request),
  with no stated ordering or shared code path named between them beyond
  both calling into the same two SPI interfaces.
- **Supported grading constraint:** A plan may keep KAFKA-9550 and
  KAFKA-9579 as two separate deliverable slices (they are architecturally
  distinct thread pools per the KIP's own description) without inventing
  a merge-order or blocking dependency between them, purely because they
  share the same SPI.
- **Not supported:** Sharing a prerequisite (the SPI) does not mean these
  two — or any other pair of SPI-consuming tickets in this set — must be
  centralized into one slice, sequenced against each other, or built by
  the same person just because KAFKA-9550 and KAFKA-9579's *historical*
  assignee happens to be the same person (Satish Duggana). Assignee
  identity is a fact about who historically claimed the ticket, not a
  stated technical dependency.

### Claim 10 (audit self-check): "SKILL.md's enabler heuristic is being treated as historical fact."

- **Check performed:** Every REQUIRED item drafted from this audit (see
  `grading/case-306.expected.md`) was re-read against the question "would
  this still make sense if SKILL.md did not exist?" The claims that
  survive as REQUIRED are ones with direct primary-source support
  independent of SKILL.md's own language (a stated textual dependency, a
  stated external-repo disclaimer, a stated architectural separation, an
  absence of stated links) — not restatements of SKILL.md's own
  three-part enabler test framed as if the historical record itself
  states them. Where the record is genuinely ambiguous about whether the
  SPI "deserves" independent status in SKILL.md's specific sense (see
  Claim 4's verifiability tension), that ambiguity is left as
  DEFENSIBLE, not resolved into a REQUIRED item that would just be
  SKILL.md's heuristic wearing a historical-fact costume.

## Chosen cutoff

**2020-02-20, end of day (UTC).**

This is the day KAFKA-9579 (the last of the nine tickets) was filed. By
this point:

- All nine tickets in this fixture exist and are open (KAFKA-9554 is the
  one exception — filed 2020-02-14 and closed as a duplicate of
  KAFKA-9548 the same day, before this cutoff).
- The KIP-405 wiki text has just settled at version 118 (saved
  2020-02-14T09:25:53Z) and will not be edited again until 2020-05-12 — a
  clean, three-month quiet window that also matches the Jira
  subtask-filing gap (the next subtask, KAFKA-9990, is not filed until
  2020-05-13).
- Exactly one fork PR (`harshach/kafka#31`, opened 2020-02-17) has
  started concurrent implementation work, bundling SPI-adjacent changes
  with the local RSM implementation — visible, dated, pre-cutoff evidence
  of early co-development, without yet showing how the rest of the
  window's work will eventually be organized.
- **Nothing has landed on `apache/kafka` trunk.** The earliest official
  trunk PR for any of these nine tickets (`#10173`, KAFKA-9548) does not
  open until 2021-02-22 — over a year later.
- The KIP itself is formally unaccepted ("Discussion" state) and will
  remain so for at least another year.

## Why this point is defensible

This cutoff sits at the exact moment the initial burst of Jira
subtask-filing completes and before any implementation has landed
anywhere but an isolated development fork. It creates the target planning
problem cleanly: a plan built from these five files must decide whether
KAFKA-9548 deserves independent slice identity based on (a) four
textually-established downstream consumers within this window
(KAFKA-9549, -9550, -9555, -9579) across two distinct people's work, (b)
two more textually-established but explicitly external-repo-scoped
"consumers" (KAFKA-9565, -9569) that look identical to the first four at
the ticket-title level, and (c) one duplicate ticket (KAFKA-9554) whose
title alone suggests a second foundational task. None of the eventual
outcome — which of these ever shipped, how long each actually took, that
the "Won't Fix" ticket was right that S3/HDFS never landed in-repo, that
the KIP took until at least 2023 to be formally accepted — is visible at
this cutoff, and none of it is included in any agent-visible file.

Choosing a later cutoff (e.g., after `#10173` merged in March 2021) would
let a plan see which downstream items had already landed and in what
order, contaminating the very topology judgment this case exists to
test. Choosing an earlier cutoff (before all nine tickets existed) would
understate the real multi-consumer signal the mining pass's hypothesis
was built on. 2020-02-20 is the earliest point at which the complete,
real candidate task set exists and the record's own internal tension
(real multi-consumer signal for four tickets; an explicit external-repo
disclaimer complicating two more; a duplicate masquerading as a second
foundation) is fully present.

## Which target dynamics this cutoff does and does not support

**Supports:**
- A genuine test of whether a run recognizes a real (if more modest than
  the mining pass first suggested) horizontal enabler — KAFKA-9548 with
  at least four named, cross-personnel consumers.
- A genuine test of whether a run over-credits ticket-title-level
  similarity (KAFKA-9565/-9569 "look like" KAFKA-9549) over what the
  KIP's own design text says about their actual scope.
- A genuine test of whether a run treats an architectural-sounding title
  (KAFKA-9554, "Define the SPI..."; KAFKA-9564, "...Test framework...")
  as automatically earning independent/foundational status, versus
  checking whether the record actually supports that.
- A genuine, unresolved verifiability tension (Claim 4) about whether the
  SPI passes SKILL.md's own vertical-grouping verifiability bar on its
  own — this fixture does not manufacture an answer to that tension; it
  is left as the case's own central judgment call, mirrored in
  DEFENSIBLE, not forced into REQUIRED in either direction.

**Does not support, and this fixture does not test:**
- A numeric-order illusion (the nine tickets' numbers are filed in
  essentially chronological order within this narrow six-day window; no
  dependency runs against that order).
- A community-external process gate comparable to case-302's mailing-list
  DISCUSS block — the KIP's unaccepted status is a real fact (Claim 6)
  but nothing in the record shows any of these nine tickets was formally
  *blocked* pending a vote; work proceeded regardless.
- A resource-manager-style "one discovered bug, several separately
  fixable per-component instances" cluster shape identical to case-304's
  — this fixture's shared prerequisite is a designed interface filed
  before any of its consumers, not a bug discovered after the fact
  affecting several already-existing components.
- Any claim requiring the model to already know how Kafka's tiered
  storage feature actually turned out (GA timing, which vendors shipped
  plugins, the eventual "Accepted" KIP text) — none of that is
  agent-visible, and none of it is required to answer this case's
  REQUIRED items correctly.

## Task count

**Nine agent-visible tasks** (KAFKA-9548, -9549, -9550, -9554, -9555,
-9564, -9565, -9569, -9579) — matching case-305's count, and reflecting
this window's real, complete, and isolated set of filed subtasks rather
than a padded target. KAFKA-9990 (filed 2020-05-13) and the entire
2021-02-24-onward batch (KAFKA-12368 and 41 later subtasks, including
KAFKA-12458's Azure implementation, filed 2021-03-12) all postdate this
cutoff and are excluded — they are DIAGNOSTIC-only in
`historical-outcome.md`, never agent-visible.

## Corrections made after the pre-freeze audit

Before any tested-agent run, a fresh, independent reviewer agent (no
access to this session's reasoning) audited this fixture and the draft
grading key against live Jira/GitHub/Confluence data, specifically
hunting for the ten adversarial failure modes named in Claim 10 above
plus seven load-bearing factual claims. It found and fixed one
substantive defect and one citation-only defect, both applied before
freezing:

1. **KAFKA-9579's assignee-at-cutoff was misstated as Satish Duggana in
   four agent-visible files (`tasks.md`, `repository-state.md`,
   `dependencies.md` twice), this file's own Claim 2, and one
   `sources.md` table cell.** The live Jira API's `assignee` field
   returns each ticket's *current* value; for eight of the nine tickets
   this happens to equal the cutoff-time value (no assignee-field change
   was ever recorded in their changelogs), but KAFKA-9579's full
   changelog (89 history entries) shows exactly one assignee change,
   dated 2023-02-23: `Ying Zheng -> Satish Duggana`. At this fixture's
   2020-02-20 cutoff, KAFKA-9579 was assigned to Ying Zheng — the same
   person assigned to KAFKA-9569 (HDFS), not to KAFKA-9548/-9550/-9555's
   filer. This is exactly the "read the live/current state instead of
   the historical one" failure mode this fixture's own KIP-wiki
   version-pinning discipline was built to avoid, and it had been missed
   in the initial research pass. All five agent-visible/provenance
   references were corrected to state "assignee at cutoff" rather than
   assuming the live API's current value, and the corrected fact (KAFKA-
   9569/-9579 share an assignee, not KAFKA-9548/-9550/-9555/-9579) is
   preserved as a real observation in `repository-state.md` and
   `dependencies.md` rather than simply deleted. REQUIRED #1-#11 in
   `grading/case-306.expected.md` required no change — none of them
   depended on the wrong version of this fact — but the grading key's
   DEFENSIBLE section (which had asserted KAFKA-9550/-9579 "share an
   assignee") was corrected to drop that clause, since its substantive
   point (the KIP describes them as architecturally distinct thread
   pools) does not depend on it.
2. **`sources.md` misstated KAFKA-14889's filing date as 2023-06-08**;
   the Jira API shows 2023-04-11. This ticket never appears in any
   agent-visible file and the surrounding "more than three years
   post-cutoff, excluded" conclusion holds under either date — a
   citation-accuracy fix only, no effect on grading.

No other defects were found across the twelve adversarial categories or
seven independently re-verified factual claims the audit checked; every
other quote, date, and status transition it spot-checked against live
Jira/GitHub/Confluence data matched exactly.

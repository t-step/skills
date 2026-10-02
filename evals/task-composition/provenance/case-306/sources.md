# Sources — case-306 (Apache Kafka KIP-405 Tiered Storage, early SPI/Phase 1 window)

All data fetched directly against live systems on 2026-09-27:
`issues.apache.org/jira/rest/api/2/...` (Apache Kafka Jira REST API),
`api.github.com` (GitHub REST/search API, `apache/kafka` and the
`harshach/kafka` development fork), and
`cwiki.apache.org/confluence/rest/api/content/...` (Confluence REST API,
used specifically to fetch **historical, dated revisions** of the KIP-405
wiki page rather than its current text — see "Why the wiki text is
version-pinned" below). Timestamps are UTC as returned by each API.
Quotes are copy-pasted from API JSON bodies or raw Confluence
`body.storage` HTML (converted to plain text), not paraphrased, unless
marked "paraphrased."

## The umbrella (KAFKA-7739 / KIP-405)

- `issues/KAFKA-7739` ("Kafka Tiered Storage") — created **2018-12-14**
  by Sriharsha Chintalapani, type "New Feature," status Resolved. Its own
  description field (as currently stored) reads: "KIP:
  [KIP-405 link]. Next version of tiered storage is tracked at
  [KAFKA-15420]" — the "next version" pointer is a later addition (KAFKA-
  15420 was filed 2023-08-15) and is cited here only as DIAGNOSTIC
  evidence that a *second* initiative existed after this one completed;
  it is not part of `context.md`.
- KAFKA-7739 has **54 total subtasks** as of the live tracker (fetched via
  `issue/KAFKA-7739?fields=subtasks`). Filtering all 54 by `created` date
  (via a JQL `key in (...)` search on `fields=created`) shows a sharp,
  isolated burst: **nine were filed between 2020-02-13 and 2020-02-20**,
  then **nothing else was filed against this umbrella for the next three
  months** (the next, KAFKA-9990, was filed 2020-05-13; the batch after
  that does not begin until 2021-02-24, a full year later). This is a
  real, structural gap in the record, not a cutoff chosen to manufacture
  one — see `cutoff-rationale.md`.

## The nine tickets filed 2020-02-13 through 2020-02-20 (this fixture's task set, minus one duplicate)

Fetched individually via `issue/KAFKA-XXXX?fields=summary,description,
created,resolutiondate,status,resolution,issuelinks,comment,reporter,
assignee,priority`.

| Key | Created | Reporter | Assignee at cutoff | Priority | Resolution (as of 2026, DIAGNOSTIC only) | Resolution date (DIAGNOSTIC) |
|---|---|---|---|---|---|---|
| KAFKA-9548 | 2020-02-13 | Satish Duggana | Satish Duggana | Major | Fixed | 2021-03-03 |
| KAFKA-9549 | 2020-02-13 | Satish Duggana | Alexandre Dupriez | Major | Fixed | 2020-04-27 |
| KAFKA-9550 | 2020-02-13 | Satish Duggana | Satish Duggana | Major | Fixed | 2023-04-13 |
| KAFKA-9554 | 2020-02-14 | Alexandre Dupriez | Satish Duggana | Major | **Duplicate** (of KAFKA-9548) | 2020-02-14 (same day) |
| KAFKA-9555 | 2020-02-14 | Alexandre Dupriez | Satish Duggana | Major | Fixed | 2021-07-19 |
| KAFKA-9564 | 2020-02-17 | Alexandre Dupriez | Alexandre Dupriez | Major | Fixed | 2023-09-04 |
| KAFKA-9565 | 2020-02-18 | Alexandre Dupriez | Ivan Yurchenko | Major | **Won't Fix** | 2023-08-31 |
| KAFKA-9569 | 2020-02-18 | Satish Duggana | Ying Zheng | Major | Fixed | 2021-09-13 |
| KAFKA-9579 | 2020-02-20 | Satish Duggana | **Ying Zheng** | Major | Fixed | 2023-05-25 |

**Assignee-history correction:** the live Jira API's `assignee` field
returns each ticket's *current* value, not its cutoff-time one. For eight
of the nine tickets the changelog (`issue/KAFKA-XXXX?expand=changelog`)
shows the assignee was set at or near filing and never changed since —
current value equals cutoff value. **KAFKA-9579 is the one exception**:
its full changelog (89 history entries, `total: 89` confirming
completeness) shows exactly one assignee-field change, dated
**2023-02-23T08:09:34Z**: `Ying Zheng -> Satish Duggana`. Since Jira does
not log a ticket's creation-time field values as changelog history, and
no assignee change is recorded between KAFKA-9579's filing
(2020-02-20T17:22:48Z) and its first changelog entry of any kind
(2021-05-17, a Fix Version change — over 15 months later), the assignee
in effect at this fixture's 2020-02-20 cutoff was **Ying Zheng** — the
same person assigned to KAFKA-9569 (HDFS), not Satish Duggana. This was
caught during the pre-freeze independent audit (see `cutoff-rationale.md`,
"Corrections made after the pre-freeze audit") and is reflected
throughout this table and every agent-visible file as "assignee at
cutoff," not "current assignee."

All nine carry the **same priority label ("Major")** — confirmed by
querying every one of the 54 subtasks' priority fields; the distribution
across all 54 is `{Major: 42, Blocker: 9, Minor: 2, Critical: 1}`, but
**all nine in this window are Major**, with no Blocker/Critical/Minor
among them. No milestone or fix-version was set on any of the nine as of
filing (fix-versions on long-lived Kafka tickets are added/changed over
years as release trains slip; none is agent-visible or dated to this
window).

**No `issuelinks` (Jira-native "depends on" / "blocks" / "relates to")
exist between any of these nine tickets.** The only `issuelinks` entry
found on any of them is on KAFKA-9579: "duplicates KAFKA-14889" — a
ticket filed **2023-04-11**, more than three years after this fixture's
cutoff, and excluded from the fixture as post-cutoff information. Every
dependency relationship in `dependencies.md` is inferred from ticket text
and the KIP's own text, exactly as this suite's prior cases (301-305)
have done — Kafka's Jira usage here is no more link-disciplined than
Rust's or Hudi's.

### KAFKA-9548 — "SPI - RemoteStorageManager and RemoteLogMetadataManager interfaces and related classes."
- `description`: **empty** (`null`) as filed — this ticket has never had a
  Jira description field at any point through 2026, only a title. Its
  only comment (2021-03-03, Jun Rao): "merged the PR to trunk."
- Actual implementing PR: `apache/kafka#10173` ("KAFKA-9548 Added SPIs
  and public classes/interfaces introduced in KIP-405..."), opened by
  `satishd` **2021-02-22**, merged **2021-03-03**. Its 13 changed files
  are exclusively new interface/data-class files under
  `clients/src/main/java/org/apache/kafka/server/log/remote/storage/`
  (`RemoteStorageManager.java`, `RemoteLogMetadataManager.java`,
  `RemoteLogSegmentMetadata.java`, etc.) plus `TopicIdPartition.java` and
  a `build.gradle` change — **no consumer/implementation code is part of
  this PR.** This is the ticket's *eventual, official* shape — a full
  year after filing — cited here as DIAGNOSTIC only (see "Why the wiki
  text is version-pinned" below for why this shape is not treated as
  proof of the ticket's shape *at cutoff*).

### KAFKA-9549 — "Local storage implementations for RSM which can be used in tests"
- `description`: "The goal of this task is to implement a straightforward
  file-system based implementation of the `RemoteStorageManager` defined
  as part of the SPI for Tiered Storage. It is intended to be used in
  single-host integration tests where the remote storage is or can be
  exercised."
- Only comment (Alexandre Dupriez, **2020-02-17**, three days after
  filing): a link to `harshach/kafka#31`.
- `harshach/kafka` pull #31 ("Tiered storage tests"), opened
  **2020-02-17T22:02:05Z**, closed (merged into that fork's own branch,
  not `apache/kafka`) same window. Body: "Work in progress. For
  information only." Its **8 changed files**
  (`gh api repos/harshach/kafka/pulls/31/files`) include *both*
  modifications to the SPI's own interface files
  (`RemoteLogSegmentContext.java`, `RemoteStorageManager.java`) and new
  exception types (`RemoteResourceNotFoundException.java`,
  `RemoteStorageException.java`) *and*, in the same PR, a new
  `LocalRemoteStorageManager.java` (342 added lines) plus its own test
  and a `LocalRemoteStorageVerifier.java` — i.e., **the SPI's shape and
  its first (local) consumer implementation were developed together, in
  one PR, three days after the tickets were filed** — not as two
  strictly sequential efforts.
- No PR titled or referencing "KAFKA-9549" was ever opened against
  `apache/kafka` itself (`gh api search/issues?q=KAFKA-9549+repo:apache/
  kafka+type:pr` returns zero results) — this ticket's "Fixed" resolution
  rests entirely on fork-internal work, never merged to the official
  repository as its own change. DIAGNOSTIC: this is consistent with the
  local implementation existing purely as fork/test scaffolding that
  later got folded into other, larger official PRs rather than landing
  under its own number.

### KAFKA-9550 — "RemoteLogManager - copying eligible log segments to remote storage implementation"
- `description`: "Implementation of RLM as mentioned in the HLD section
  of KIP-405, this JIRA covers copying segments to remote storage. [link
  to the KIP's own High-Level design section]"
- Comments are all administrative "feature freeze, pushing to next
  release" notes from 2021-07-09 through 2022-04-04 — DIAGNOSTIC evidence
  of how long full implementation actually took, not agent-visible.

### KAFKA-9554 — "Define the SPI for Tiered Storage framework"
- `description`: "The goal of this task is to define the SPI (service
  provider interfaces) which will be used by vendors to implement
  plug-ins to communicate with specific storage system. Done means:
  Package with interfaces and key objects available and published for
  review."
- `resolution`: **Duplicate**. Its one and only comment, same day it was
  filed (Satish Duggana, 2020-02-14): "Duplicate of
  https://issues.apache.org/jira/browse/KAFKA-9548" — filed one day
  after KAFKA-9548 and closed as a duplicate of it within the same
  calendar day, before this fixture's cutoff. **This ticket is, by
  cutoff, already fully resolved and carries zero independent remaining
  scope** — it is included in `tasks.md` specifically as a trap: its
  title ("Define the SPI...") sounds like a second, independent
  foundational task, but the record shows it never was one.

### KAFKA-9555 — "Topic-based implementation for the RemoteLogMetadataManager"
- `description`: "The purpose of this task is to implement a
  `RemoteLogMetadataManager` based on an internal topic in Kafka. More
  details are mentioned in the KIP[link to KIP's RLMM-internal-topic
  section]. Done means: Pull Request available for review and
  unit-tests. System and integration tests are out of scope of this task
  and will be part of another task."
- Comments: 2021-07-09 (feature-freeze push-out), 2021-07-19 (Jun Rao:
  "merged the PR to trunk").

### KAFKA-9564 — "Integration Test framework for Tiered Storage"
- `description`: **empty** (`null`) as filed.
- Comments: Alexandre Dupriez, **2020-04-27**, links to `harshach/
  kafka#52` and `#46` in addition to the earlier `#31`; Alexandre
  Dupriez, **2020-05-16**: "integration tests for basic scenarios have
  been written for KIP-405. More tests to come to cover additional
  scenarios" (this second comment postdates this fixture's 2020-02-20
  cutoff and is DIAGNOSTIC only — it is cited here to show the
  eventual shape of this ticket's real content, not as agent-visible
  fact). A much later comment (Satish Duggana, 2023-09-04) links the
  *actual* upstream framework PR (`apache/kafka#14116`) — three and a
  half years after filing; DIAGNOSTIC only.
- `harshach/kafka` pulls #46 (opened 2020-04-08, titled "Tiered storage
  tests," empty body) and #52 (opened 2020-04-16, "Consume records from
  the local tiered storage for the two base cases integration tests.")
  both postdate this fixture's cutoff (2020-02-20) and are DIAGNOSTIC
  only, cited here to confirm KAFKA-9564's eventual real content was
  integration-test scenarios exercised against the local RSM
  implementation (KAFKA-9549), not a second SPI-defining effort.

### KAFKA-9565 — "Implementation of Tiered Storage SPI to integrate with S3"
- `description`: **empty** (`null`) as filed.
- Its only comment (Ivan Yurchenko, **2023-06-14** — more than three
  years post-cutoff, DIAGNOSTIC only): "AFAIU, concrete
  `RemoteStorageManager` implementations won't be hosted in the Apache
  Kafka repo. So this ticket should probably be closed as wont-fix. I've
  been working on a `RemoteStorageManager` implementation that supports
  AWS S3 and in future..." — the ticket was in fact closed **Won't
  Fix** on 2023-08-31.
- No PR referencing "KAFKA-9565" was ever opened against `apache/kafka`.
  DIAGNOSTIC: this ticket never produced in-repo code at any point in its
  history, consistent with the KIP's own stated intent (see "What the
  KIP's own historical text establishes" below) that S3/HDFS
  implementations were never planned to live in this repository.

### KAFKA-9569 — "RemoteStorageManager implementation for HDFS storage."
- `description`: "This is about implementing `RemoteStorageManager` for
  HDFS to verify the proposed SPIs are sufficient. It looks like the
  existing RSM interface should be sufficient. If needed, we will discuss
  any required changes." **This ticket's own filed text frames its
  purpose as validating the SPI's sufficiency, not as a committed
  production deliverable** — this is stated at filing time, not read in
  after the fact.
- Its only comment (Viktor Somogyi-Vass, **2023-09-18**, DIAGNOSTIC only):
  "[Ying Zheng], [Satish Duggana] is this plugin available somewhere?" —
  asked more than three years after the ticket was marked "Fixed"
  (2021-09-13), and never answered in the tracker. No PR referencing
  "KAFKA-9569" was ever opened against `apache/kafka`
  (`search/issues?q=KAFKA-9569+repo:apache/kafka+type:pr` returns zero
  results) despite the "Fixed" resolution — DIAGNOSTIC evidence that the
  formal Jira resolution state on a long-lived umbrella's subtask does
  not reliably indicate that working code was ever delivered under that
  ticket's own number.

### KAFKA-9579 — "Remote consumer fetch implementation by adding respective purgatory"
- `description`: **empty** (`null`) as filed.
- Comments are all administrative feature-freeze push-out notes
  (2021-07-09 through 2022-04-04), plus the unrelated 2023 duplicate link
  noted above.

## What the KIP's own historical text establishes

**Why the wiki text is version-pinned, not read from the current page.**
The KIP-405 Confluence page (id `97554472`) has been edited **372 times**
between 2018-12-14 and 2025-06-11 (fetched via `rest/api/content/97554472/
history` and, for the full per-version list, `rest/experimental/content/
97554472/version?limit=200[&start=200]`, paginated). Reading its *current*
text would silently import years of later design changes, GA
announcements, and retrospective wording. Instead, every KIP quote below
is pinned to **version 118**, saved **2020-02-14T09:25:53Z** by Satish
Duggana — the version in effect the day KAFKA-9554/9555 were filed, and
the last edit before a three-month editing gap (the next edit, version
119, is dated 2020-05-12 — matching the same three-month quiet window
found in the Jira subtask-filing gap above). Fetched via
`rest/api/content/97554472?version=118&status=historical&expand=
body.storage`.

- **The KIP's own "Public Interfaces" section, as of v118, states
  explicitly and directly:** "HDFS and S3 implementation are planned to
  be hosted in external repos and these will not be part of Apache Kafka
  repo. This is inline with the approach taken for Kafka connectors." —
  immediately following the sentence introducing `RemoteStorageManager`
  and stating "We will provide a simple implementation of RSM to get a
  better understanding of the APIs" (i.e., the local/test implementation,
  KAFKA-9549). **This single sentence is the fixture's central pressure
  point**: KAFKA-9565 (S3) and KAFKA-9569 (HDFS) are real, filed,
  distinctly-assigned Jira tickets that exist alongside KAFKA-9549 and
  look, from ticket titles alone, like two more instances of the same
  "downstream consumer" pattern — but the KIP's own ratified-at-the-time
  design text says, in advance, that they were never intended to be this
  initiative's own in-repo deliverables.
- **`RemoteLogMetadataManager`'s own KIP text**: "There is a default
  implementation that uses an internal topic. Users can plugin their own
  implementation if they intend to use another system to store remote
  log segment metadata." — directly describing KAFKA-9555's role as *the*
  shipped default, not one of several equally-weighted alternatives.
- **`RemoteLogManager` (RLM)'s own KIP text** (Proposed Changes /
  High-level design): RLM "delegates copy, read, and delete of topic
  partition segments to a pluggable storage manager (viz.
  `RemoteStorageManager`) implementation and maintains respective remote
  log segment metadata through `RemoteLogMetadataManager`." The KIP's own
  "RLM Leader Task" subsection describes the copy path calling
  `RLMM.putRemoteLogSegmentData(...)` and `RSM.copyLogSegment(...)`
  directly — this is KAFKA-9550's own described scope, textually tied to
  both SPI interfaces by name.
- **The KIP's own "Remote Storage Fetcher Thread Pool" text** describes a
  second, separate thread pool (distinct from the copy path above) that,
  on a consumer fetch request for older data, uses `RemoteFetchPurgatory`
  (a `kafka.server.DelayedOperationPurgatory` instance) and calls
  `RSM.fetchLogSegmentData(...)` — this is KAFKA-9579's own described
  scope, and the KIP's text describes it as architecturally distinct from
  the copy path (a different thread pool, a different purgatory,
  triggered by a different event: an incoming consumer fetch versus a
  scheduled copy interval) with no stated ordering between the two.
- **The KIP's own "Current State" field, as of v118, reads "Discussion"**
  — not "Accepted." Checking further, dated versions (fetched the same
  way): version 232 (2020-09-15) still reads "Discussion"; version 340
  (2021-02-15, **one week before** the official SPI PR #10173 was even
  opened) still reads "Discussion"; version 370 (2023-09-17) is the
  first version checked that reads "Accepted." **The KIP had not been
  formally voted/accepted at any point during this fixture's 2020-02-20
  cutoff window, and was still unaccepted more than a year later when the
  first official SPI PR merged to trunk.** This is a real, dated fact
  about how unsettled the whole initiative's design still was at cutoff
  — not a reason to assume the interfaces described in `tasks.md` were
  final.
- **No "Test Plan," "Rejected Alternatives" (beyond two named
  architecture alternatives unrelated to task sequencing), "Phase," or
  staged-rollout section exists in v118.** There is no KIP-native document
  that states an implementation order, a phase 1/phase 2 split, or which
  of the nine tickets should happen first — any sequencing claim in
  `dependencies.md` is inferred from ticket text and the KIP's
  description of RLM/RLMM/RSM's own call relationships, not read off a
  stated plan.

## Mailing-list activity (confirming the window, not adding new claims)

- `lists.apache.org` archive activity for `dev@kafka.apache.org`
  containing "KIP-405" (`api/stats.lua?list=dev&domain=kafka.apache.org&
  q=KIP-405`) shows real but modest activity in the exact window
  surrounding this cutoff (5 messages in 2020-02) sandwiched between a
  quieter Nov-Dec 2019 stretch and a much larger surge starting
  2020-07/08 (19 and 26 messages respectively) — consistent with "the KIP
  had community attention but was still an active, unsettled discussion,"
  not evidence of any specific additional design claim used in grading.

## No candidate missed (unbounded re-check)

A fresh, unbounded JQL search for every KAFKA-7739 subtask created between
2020-01-01 and 2020-03-01 (`jql=key in (...) AND created >= "2020-01-01"
AND created <= "2020-03-01"`, cross-checked against the full 54-subtask
list fetched independently) returns exactly the same nine keys listed
above — no tenth candidate was found and silently dropped.

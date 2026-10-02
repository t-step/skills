# Historical outcome — case-306 (DIAGNOSTIC ONLY, never agent-visible)

Everything in this file postdates the 2020-02-20 cutoff and must never
appear in `evals/task-composition/cases/case-306/`. It exists so a
grading pass can distinguish "what a plan could have known" from "how it
actually turned out," and so the DIAGNOSTIC section of
`grading/case-306.expected.md` can cite specifics without smuggling
hindsight into REQUIRED items.

## What actually shipped, and when

| Ticket | Resolution | Date | Official `apache/kafka` PR |
|---|---|---|---|
| KAFKA-9554 | Duplicate (of 9548) | 2020-02-14 (same day filed) | none — closed without code |
| KAFKA-9549 (local RSM impl) | Fixed | 2020-04-27 | **none** — resolved on fork-only evidence (`harshach/kafka#31`); no PR referencing KAFKA-9549 was ever opened against `apache/kafka` |
| KAFKA-9548 (SPI) | Fixed | 2021-03-03 | `apache/kafka#10173`, opened 2021-02-22 by `satishd`, 13 files, interfaces/data-classes only |
| KAFKA-9569 (HDFS impl) | Fixed | 2021-09-13 | **none found** — no PR referencing KAFKA-9569 was ever opened against `apache/kafka`; a 2023-09-18 comment on the ticket itself ("is this plugin available somewhere?") went unanswered |
| KAFKA-9555 (topic-based RLMM impl) | Fixed | 2021-07-19 | merged per Jun Rao's comment; specific PR number not independently re-verified in this pass beyond the ticket's own "merged the PR to trunk" comment |
| KAFKA-9579 (remote fetch/purgatory) | Fixed | 2023-05-25 | administrative feature-freeze push-outs recorded 2021-07-09, 2021-11-02, 2022-04-04 before eventual resolution |
| KAFKA-9550 (RLM copy path) | Fixed | 2023-04-13 | same feature-freeze push-out pattern as KAFKA-9579 |
| KAFKA-9564 (integration test framework) | Fixed | 2023-09-04 | eventual framework PR `apache/kafka#14116` (cited in a 2023-09-04 comment); earlier fork evidence: `harshach/kafka#31` (2020-02-17), `#46` (2020-04-08), `#52` (2020-04-16) |
| KAFKA-9565 (S3 impl) | **Won't Fix** | 2023-08-31 | **none ever opened.** Closed on the explicit stated grounds (2023-06-14 comment, Ivan Yurchenko) that "concrete `RemoteStorageManager` implementations won't be hosted in the Apache Kafka repo" |

## The KIP's own formal status over time

- v118 (2020-02-14, this fixture's cutoff text): "Current State: Discussion"
- v232 (2020-09-15): "Current State: Discussion"
- v340 (2021-02-15, one week before the SPI PR opened): "Current State: Discussion"
- v370 (2023-09-17): "Current State: 'Accepted'" — the earliest version
  checked in this pass that shows acceptance. The KIP was not formally
  voted/accepted for at least three and a half years after this
  fixture's cutoff, and possibly longer (no attempt was made to find the
  exact version where the state first flipped, since the fact that it
  remained "Discussion" through v340 is already sufficient to establish
  the cutoff-time uncertainty this fixture relies on).
- v371 (2025-04-01): edit message "add info about merged and GA" —
  confirming the feature's GA announcement postdates even the 2023
  acceptance by roughly two more years.

## What this confirms, read against the fixture's own claims

- **The "external repo" disclaimer in the KIP's v118 text was
  predictive, not aspirational-and-later-abandoned.** S3 (KAFKA-9565)
  was formally closed Won't Fix specifically because concrete RSM
  implementations were never hosted in `apache/kafka`; HDFS (KAFKA-9569)
  was marked Fixed but never actually produced a discoverable PR or
  plugin, and the one person who asked about it years later got no
  answer. Neither ticket followed the same in-repo delivery path as
  KAFKA-9549 (local) or KAFKA-9555 (topic-based), even though both were
  filed the same week with named assignees and looked, from the tracker
  alone, like two more instances of the same pattern.
- **KAFKA-9549's own "Fixed" resolution rests entirely on fork-internal
  work that never reached `apache/kafka` under its own ticket number** —
  a caution against reading "Fixed" as "shipped a standalone, separately
  reviewable change," consistent with the fork-bundling pattern already
  described in `cutoff-rationale.md` (Claim 7).
- **The gap between filing and official merge is enormous and uneven**
  across these nine tickets — 44 days (KAFKA-9549's fork resolution) to
  over three years (KAFKA-9564, KAFKA-9579, KAFKA-9550) — which is
  consistent with a long-running, frequently-deprioritized, multi-year
  initiative rather than a tightly time-boxed "Phase 1" with a clean
  internal deadline. Nothing in this file should be read as evidence for
  or against any particular slice topology at the 2020-02-20 cutoff — a
  plan at that point in time could not have known any of these later
  dates, and this suite's own standing convention (see case-301 through
  -305) is not to grade a cutoff-time plan against the eventual real
  timeline.

## Later, unrelated consumer (correctly excluded from the fixture)

KAFKA-12458 ("Implementation of Tiered Storage Integration with Azure
Storage (ADLS + Blob Storage)") was filed **2021-03-12** — thirteen months
after this fixture's cutoff, and nine days after the SPI's own official
PR (`#10173`) merged to trunk. It is the clearest real-world instance of
"a genuinely new downstream consumer arriving once the interface had
actually stabilized on trunk" — but it is a fact about *after* this
initiative's SPI had already gone through its full unaccepted-KIP,
fork-then-trunk journey, not something a 2020-02-20 plan could have
named, and it is excluded from `tasks.md` entirely.

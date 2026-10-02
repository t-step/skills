# Source notes: Kafka Tiered Storage (KIP-405) — open work as of 2020-02-20

**Where this came from:** the Apache Kafka issue tracker (KAFKA-7739 and
its subtasks) and the text of KIP-405 itself, as currently written on the
Kafka wiki. Task descriptions above are taken from the tickets' own text
as filed — several are genuinely this thin (KAFKA-9548, KAFKA-9550,
KAFKA-9564, and KAFKA-9579 have no description beyond a title, or a
one-line pointer into the KIP), not summarized down from a richer
discussion that hasn't happened yet.

**The KIP's own text draws a line between what this repository will
deliver and what it explicitly expects someone else to build.**
Immediately after introducing `RemoteStorageManager`, the KIP states: "We
will provide a simple implementation of RSM to get a better understanding
of the APIs. HDFS and S3 implementation are planned to be hosted in
external repos and these will not be part of Apache Kafka repo. This is
inline with the approach taken for Kafka connectors." Kafka Connect's own
connectors (JDBC, S3 sink, Elasticsearch, and so on) are a real, existing
precedent for this pattern — they are built and distributed as separate
projects, not bundled into the `apache/kafka` repository itself, even
though Connect's own framework and interfaces live in this repo. The KIP
is explicitly drawing the same line for tiered storage's own pluggable
backends. KAFKA-9565 (S3) and KAFKA-9569 (HDFS) are real, filed,
distinctly-assigned tickets that exist in this same tracker anyway —
nothing in either ticket's own text repeats or contradicts the KIP's
external-repo statement, so it isn't clear from the tickets alone whether
they were filed as genuine near-term commitments, as placeholders to
track early prototyping regardless of where the result eventually lives,
or for some other reason. Both readings are consistent with what's
actually written down.

**KAFKA-9569's own description states its purpose directly:** "This is
about implementing `RemoteStorageManager` for HDFS to verify the
proposed SPIs are sufficient. It looks like the existing RSM interface
should be sufficient. If needed, we will discuss any required changes."
This frames the ticket, in its own words, as a check on whether the
interface is well-designed — not as a statement that a production HDFS
backend will ship as part of this effort.

**Already landed, not remaining work:**
- KAFKA-9554 ("Define the SPI for Tiered Storage framework") was filed
  2020-02-14 and closed the same day as a duplicate of KAFKA-9548, with
  no code and no distinct remaining scope. It is included in `tasks.md`
  only because it exists in the tracker under this umbrella and its title
  could otherwise be mistaken for a second, independent piece of
  foundational work.
- Nothing else has landed. No pull request has been opened against the
  Apache Kafka repository for any of the other eight items as of this
  writing. The one piece of implementation evidence that exists (a
  work-in-progress pull request on a contributor's personal fork,
  referenced from KAFKA-9549's comment) is explicitly marked "for
  information only" by its own author and has not been proposed for
  merge into this repository.

**KIP-405 itself is still under discussion, not yet accepted.** Kafka's
KIP process requires a community vote before a KIP's design is
considered settled; this one's own status field still reads
"Discussion." Nothing in the tracker or the KIP text states a target date
for a vote, or commits to the interface shapes shown in the KIP as final.

**No stated deadline or release target.** Neither the KIP nor any of the
nine tickets names a target Kafka release, a milestone, or a "must land
by" date. The umbrella (KAFKA-7739) itself was filed over a year before
any of these nine subtasks and carries no target date either.

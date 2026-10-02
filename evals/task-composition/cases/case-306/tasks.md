# Tasks: Kafka Tiered Storage (KIP-405) — open work as of 2020-02-20

This is the current state of the open subtasks under KAFKA-7739, pulled
from the issue tracker, sorted by issue number. There is no other roadmap
document for this work beyond what's written here and in the KIP text
referenced in `source-notes.md`.

- **KAFKA-9548** — "SPI - RemoteStorageManager and RemoteLogMetadataManager
  interfaces and related classes." No description text beyond the title.
  Assigned to the same person who filed it. Filed 2020-02-13. No pull
  request exists yet. Open, no comments.

- **KAFKA-9549** — "Local storage implementations for RSM which can be
  used in tests." Description: "The goal of this task is to implement a
  straightforward file-system based implementation of the
  `RemoteStorageManager` defined as part of the SPI for Tiered Storage.
  It is intended to be used in single-host integration tests where the
  remote storage is or can be exercised." Filed 2020-02-13, assigned to a
  different engineer than KAFKA-9548's filer. One comment, three days
  after filing, linking to a work-in-progress pull request on a
  contributor's personal fork, marked "for information only" — that PR
  modifies files under the SPI's own package (adding new exception
  types, adjusting one existing interface method) in the same change that
  adds the new local-filesystem implementation and its own test.

- **KAFKA-9550** — "RemoteLogManager - copying eligible log segments to
  remote storage implementation." Description: "Implementation of RLM as
  mentioned in the HLD section of KIP-405, this JIRA covers copying
  segments to remote storage," with a link to the KIP's own high-level
  design section. Filed 2020-02-13, assigned to the same engineer as
  KAFKA-9548. No pull request exists yet. No comments.

- **KAFKA-9554** — "Define the SPI for Tiered Storage framework."
  Description: "The goal of this task is to define the SPI (service
  provider interfaces) which will be used by vendors to implement
  plug-ins to communicate with specific storage system. Done means:
  Package with interfaces and key objects available and published for
  review." Filed 2020-02-14, one day after KAFKA-9548. Its one comment,
  filed the same day: "Duplicate of KAFKA-9548." **Closed as a duplicate
  of KAFKA-9548 the same day it was filed.**

- **KAFKA-9555** — "Topic-based implementation for the
  RemoteLogMetadataManager." Description: "The purpose of this task is to
  implement a `RemoteLogMetadataManager` based on an internal topic in
  Kafka. More details are mentioned in the KIP," with a link to the KIP's
  RLMM-internal-topic section. "Done means: Pull Request available for
  review and unit-tests. System and integration tests are out of scope of
  this task and will be part of another task." Filed 2020-02-14, assigned
  to the same engineer as KAFKA-9548/-9550. No pull request exists yet.
  No comments.

- **KAFKA-9564** — "Integration Test framework for Tiered Storage." No
  description text beyond the title. Filed 2020-02-17, assigned to the
  same engineer as KAFKA-9549. No pull request referenced yet. No
  comments.

- **KAFKA-9565** — "Implementation of Tiered Storage SPI to integrate
  with S3." No description text beyond the title. Filed 2020-02-18,
  assigned to a third engineer, distinct from everyone assigned above. No
  pull request exists yet. No comments.

- **KAFKA-9569** — "RemoteStorageManager implementation for HDFS
  storage." Description: "This is about implementing
  `RemoteStorageManager` for HDFS to verify the proposed SPIs are
  sufficient. It looks like the existing RSM interface should be
  sufficient. If needed, we will discuss any required changes." Filed
  2020-02-18, assigned to a fourth engineer, distinct from everyone else
  assigned above. No pull request exists yet. No comments.

- **KAFKA-9579** — "Remote consumer fetch implementation by adding
  respective purgatory." No description text beyond the title. Filed
  2020-02-20 (today), assigned to the same engineer as KAFKA-9569 (HDFS)
  — not to the engineer assigned to KAFKA-9548/-9550/-9555. No pull
  request exists yet. No comments.

No priority has been marked to distinguish any of these from one
another beyond Kafka's ordinary priority field — see `dependencies.md`
for what that field actually shows across this set. KAFKA-7739 itself is
not a task — it's the umbrella tracking issue, described further in
`source-notes.md`.

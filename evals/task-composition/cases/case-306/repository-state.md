# Repository state

- **None of this exists in the Apache Kafka repository yet.** No
  `RemoteStorageManager`, `RemoteLogMetadataManager`, or `RemoteLogManager`
  class exists anywhere in `apache/kafka` as of this writing. This is
  greenfield work with nothing already in-tree for any of the nine items
  to build on top of, and no existing code any of them could conflict
  with.
- **The only implementation evidence anywhere is on a contributor's
  personal fork, not this repository, and it is explicitly marked
  provisional.** One work-in-progress pull request against that fork
  (referenced from KAFKA-9549's own comment, three days after filing)
  touches both the SPI's own interface files and a new local-filesystem
  implementation in the same change, and is titled and described as "for
  information only" by its own author — it has not been proposed for
  merge into `apache/kafka`, and nothing states it reflects the final
  shape either the interfaces or the local implementation will take.
- **KAFKA-9548, KAFKA-9550, and KAFKA-9555 are all assigned to the same
  engineer.** KAFKA-9549 and KAFKA-9564 are both assigned to a second
  engineer. KAFKA-9565 (S3) is assigned to a third engineer. **KAFKA-9569
  (HDFS) and KAFKA-9579 are both assigned to a fourth engineer** — the
  only assignee overlap across all nine items, and it pairs one item the
  KIP's own text scopes as external-repo work (KAFKA-9569) with one that
  is core, in-repo `RemoteLogManager` framework work (KAFKA-9579). This
  is a fact about who has currently claimed each ticket, not a stated
  team structure or a guarantee that ownership won't change.
- **KAFKA-9554 is closed; the other eight are open with no assignee
  activity yet beyond the one linked work-in-progress fork PR.** None of
  the eight open items has a pull request opened against this
  repository.
- **All nine items already appear under KAFKA-7739 as tracker-native
  subtasks** — this is a structural field the issue tracker maintains
  automatically the moment a ticket is filed as a subtask of another, not
  a manually curated checklist that could lag behind (unlike, for
  example, a hand-maintained "Implementation history" list on a separate
  kind of tracking issue). A plan should not treat "this item is already
  linked from the umbrella" as evidence of anything beyond "it has been
  filed" — every item filed under this umbrella gets this link
  automatically, including KAFKA-9554, which carries no remaining scope
  at all.

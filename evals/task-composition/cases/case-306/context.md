# Context: Kafka Tiered Storage (KIP-405) — open work as of 2020-02-20

Apache Kafka currently stores all log segments on the local disks of its
broker machines, for the entire configured retention period. As clusters
grow and retention windows lengthen, this becomes expensive and makes
broker failure/recovery and cluster rebalancing slower, since a failed or
new broker has to copy all of its assigned partitions' data from other
replicas before it can serve traffic.

**KIP-405 ("Kafka Tiered Storage")** proposes splitting a topic's storage
into two tiers: a **local tier** (the existing behavior — recent segments
on broker disks, serving fast tail reads from page cache) and a new
**remote tier**, which copies completed log segments to an external
storage system (for example HDFS or S3) once they roll off the active
segment, with a separate, typically much longer retention period. This
lets Kafka's local retention stay short (hours) while its effective
retention grows to days or months, without adding broker disk capacity.

The KIP proposes two pluggable interfaces to make this work without
hard-coding Kafka against any one remote storage system:

- **`RemoteStorageManager` (RSM)** — the interface responsible for
  copying, reading, and deleting a topic partition's log segments and
  indexes in remote storage.
- **`RemoteLogMetadataManager` (RLMM)** — the interface responsible for
  tracking metadata about which remote segments exist for a partition
  (offsets, state, where they live), kept separate from RSM because the
  KIP's own design notes explain that mixing metadata storage into the
  remote storage system itself (its original, earlier approach) ran into
  consistency and cost problems specific to systems like S3 (e.g., `LIST`
  costs, eventual consistency around delete-then-read).

A new component, **`RemoteLogManager` (RLM)**, sits on top of both
interfaces: it runs a scheduled thread pool that copies eligible segments
to remote storage via RSM (recording the result via RLMM), and a
separate thread pool that serves consumer fetch requests for data that
has already moved to the remote tier, by looking up metadata via RLMM and
reading bytes back via RSM.

Kafka ships one built-in implementation of RLMM, backed by an internal
Kafka topic (so a cluster can use remote storage without depending on any
external metadata store). For RSM, the KIP's own text states that a
simple, local-filesystem-backed implementation will be provided to
exercise and validate the interface, and that separately, implementations
integrating with HDFS and S3 are planned — the KIP explicitly notes that
these two are expected to be hosted in external repositories rather than
in the Apache Kafka repository itself, the same way Kafka Connect's own
connectors are developed and distributed outside the core Kafka repo
rather than bundled with it.

This work is tracked under one umbrella ticket, KAFKA-7739 ("Kafka Tiered
Storage"), filed 2018-12-14, which itself is not a task — it links out to
whatever subtasks currently exist. This is the state of that subtask list
as of right now, 2020-02-20, end of day: nine subtasks have been filed in
the last week, none of them resolved except one that turned out to
duplicate another filed the day before. The KIP itself is still listed as
under discussion; it has not been formally voted on or accepted by the
Kafka community yet.

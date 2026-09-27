# Dependencies: Kafka Tiered Storage (KIP-405) — open work as of 2020-02-20

Only what's stated or clearly inferable from the tickets and the KIP text
referenced in `source-notes.md` is listed here. **No Jira "depends on" /
"blocks" / "relates to" link exists between any of the nine items in
`tasks.md`** — every relationship below is inferred from what each
ticket's own text says it builds, not read off a tracker-native link.

## Stated or clearly inferable

- **KAFKA-9549 names the SPI directly.** Its own description states it
  implements "the `RemoteStorageManager` defined as part of the SPI for
  Tiered Storage" — a stated textual dependency on KAFKA-9548's own
  scope, not an inference from shared labels or filing order.
- **KAFKA-9555 names the SPI's metadata interface directly.** Its own
  description points at the KIP's `RemoteLogMetadataManager` section and
  states its task is to implement that interface against an internal
  topic.
- **KAFKA-9550 and KAFKA-9579 both consume both SPI interfaces, per the
  KIP's own design text**, even though neither ticket's own (empty)
  description says so explicitly. The KIP describes `RemoteLogManager`'s
  copy path (KAFKA-9550's own linked HLD section) as delegating to
  `RemoteStorageManager` and recording results through
  `RemoteLogMetadataManager`, and separately describes a distinct fetch
  path — a "Remote Storage Fetcher Thread Pool" served through its own
  purgatory (matching KAFKA-9579's title, "adding respective purgatory")
  — that looks up metadata through RLMM and reads bytes back through RSM.
  This is a dependency established by the KIP's own architecture text,
  not by either ticket's own (blank) description field.
- **KAFKA-9565 and KAFKA-9569 both name the SPI in their own titles/
  descriptions** ("Implementation of Tiered Storage SPI to integrate with
  S3"; "implementing `RemoteStorageManager` for HDFS ... to verify the
  proposed SPIs are sufficient") — a stated dependency on KAFKA-9548's
  interface shape, on the same textual footing as KAFKA-9549's. See
  `source-notes.md` for why this stated dependency does not, by itself,
  put these two tickets on equal footing with KAFKA-9549/-9555 for every
  purpose.
- **KAFKA-9554 has no remaining scope to depend on anything.** It was
  filed one day after KAFKA-9548 and closed the same day as a stated
  duplicate of it. There is nothing left in KAFKA-9554 for any other
  ticket to depend on, or for it to depend on anyone else.

## Open questions the record does not resolve — flag, don't guess

- **Whether the SPI (KAFKA-9548) has to be fully finished before
  KAFKA-9549, -9550, -9555, or -9579 can start, is not stated anywhere.**
  No ticket says "blocked by KAFKA-9548." The only direct evidence of how
  this actually played out in practice is a linked work-in-progress pull
  request (referenced in KAFKA-9549's own comment) that modifies the
  SPI's own interface files *and* adds the local implementation *in the
  same change*, three days after both tickets were filed — evidence of
  early, concurrent, co-evolving work on a personal fork, not evidence
  that the interface was finished first, and not evidence that it's safe
  to assume the same pattern applies to every other downstream ticket
  here. Don't assume a strict "SPI must land first" gate on every item;
  don't assume interface work and every downstream item can proceed with
  zero coordination risk either — the record supports neither extreme.
- **Whether KAFKA-9550's copy path and KAFKA-9579's fetch path need to be
  sequenced against each other is not stated.** The KIP's own text
  describes them as two separate thread pools triggered by different
  events (a scheduled copy interval versus an incoming consumer fetch),
  with no cross-reference between the two tickets and no stated ordering
  in the KIP text beyond describing the copy path first.
- **Whether KAFKA-9564's integration-test framework depends on a specific
  one of the concrete implementations below (most plausibly KAFKA-9549's
  local one, since a single-host integration test needs *some* concrete
  RSM to exercise) is not stated in KAFKA-9564's own text** — its
  description field is empty. The only supporting signal is external to
  the ticket itself: the same work-in-progress fork PR referenced from
  KAFKA-9549's comment is titled "Tiered storage tests." This is a
  plausible inference, not a stated one — don't present it as a fact
  KAFKA-9564 itself asserts.
- **Whether KAFKA-9565 and KAFKA-9569 are expected to be built by the
  people who filed this Kafka initiative at all, versus by the external
  parties the KIP's own text names, is not settled by the tickets
  themselves.** Both are filed, assigned Kafka Jira tickets like the
  other seven — nothing in either ticket's own text says "this will
  actually be built outside this repository," even though the KIP's own
  separate design text says exactly that (see `source-notes.md`). Don't
  resolve this tension by picking one source and ignoring the other.

## Shared-area signal, not a stated dependency

KAFKA-9565 (S3) and KAFKA-9569 (HDFS) both implement the same interface
(`RemoteStorageManager`) against two different external systems, and are
assigned to two different people, neither of whom is assigned to
KAFKA-9548, -9549, -9550, or -9555. (KAFKA-9569's assignee is also
assigned to KAFKA-9579 — see below — but nothing connects that fact to
KAFKA-9565.) Neither KAFKA-9565 nor KAFKA-9569 references the other. Do
not infer a shared owner, a required sequencing, or a shared fix between
these two just because they target the same interface — the record
supports treating them as two separate, unrelated efforts that happen to
implement the same contract, not one clustered piece of work.

KAFKA-9550 (RLM copy path) and KAFKA-9579 (RLM fetch path) are both part
of the same new `RemoteLogManager` component described in the KIP, but
they are **not** assigned to the same engineer (KAFKA-9550 is assigned to
KAFKA-9548's own filer; KAFKA-9579 is assigned to the same engineer as
KAFKA-9569, HDFS) — and nothing in either ticket, or in the KIP's own
text, states that one must be built before the other, or that they must
land together in any case.

## No stated priority

All nine items carry the identical priority label in the tracker (none is
marked higher or lower than any other), and none carries a milestone,
fix-version, or due date at this point. The only assignee overlap in this
set is between KAFKA-9569 (HDFS) and KAFKA-9579 (the RLM fetch path) —
one item the KIP's own text scopes as external-repo work, the other core
in-repo framework work. KAFKA-9548, KAFKA-9550, and KAFKA-9555 share a
different, second assignee; KAFKA-9549 and KAFKA-9564 share a third; only
KAFKA-9565 has no assignee overlap with anyone else in the set. This is
evidence about who has claimed which piece of work, not evidence of a
stated priority ranking among the nine.

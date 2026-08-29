# Contract: review-queue-core (implemented baseline)

This is the existing, already-implemented contract for a single queue
item's claim lifecycle. `Reviewer Claims on Review Batches` (spec.md)
explicitly builds on this without changing it.

## Claim guarantees

- Acquiring a claim on a queue item is a single atomic, exclusive
  insert-if-absent operation. Of any number of concurrent acquire attempts
  for the same item, exactly one succeeds; every other attempt receives an
  immediate, deterministic "already claimed" failure -- never a timeout,
  never an ambiguous result, and never a window in which more than one
  attempt could believe it succeeded. This is enforced by a unique
  constraint on the claim row's item identifier, not by a read-then-write
  check in application code.
- Releasing a claim is deleting its row. Release by the recorded owner is
  always permitted. Release by anyone else (an override) is only performed
  on the basis of an observed stale-claim finding (the claim's recorded
  session no longer exists).
- A batch, or any other future grouping concept, does not get its own
  claim state and does not change how an individual item's claim is
  acquired, released, or arbitrated -- grouping concepts sit alongside the
  claim mechanism, never inside it.

## Status guarantees

- A queue item's status (`unclaimed`, `claimed`, `resolved`) is stored
  once, on the item's own row. Nothing else in the system holds a second,
  independently-writable copy of it.

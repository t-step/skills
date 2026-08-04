# Slice Retrospective: Fix memory leak in job-worker completed-job-ID tracking

## What we proved
The completed-job-ID tracking leak in `worker/loop.py` is fixed — RSS
stays flat at ~85MB over a 2-hour local repro run, versus previously
growing past 340MB — backed by the bounded-deque test and the repro's
memory measurements.

## Assumptions validated
An unbounded in-memory set was in fact the source of the leak — RSS
behavior matches exactly once the set was replaced with a bounded deque.

## Assumptions falsified
None.

## Remaining uncertainty
This slice touched the worker's job-tracking data structure, not its
restart/recovery path. Whether job state is handled correctly across a
worker restart mid-batch is untested here.

## Intentional non-goals
Any change to the worker's restart/recovery logic was out of scope per
goal.md — this slice only touched the completed-job-ID tracking structure.

## Architectural consequences
None beyond the fixed data structure itself — no new interface or seam was
introduced.

## Follow-up questions
Does the worker's restart/recovery path have any related correctness
issues, given this slice just spent time in the same file?

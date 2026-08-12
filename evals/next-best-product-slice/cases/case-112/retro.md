# Slice Retrospective: Resumable sync

## What we proved
Interrupted syncs resume at the last committed chunk (four observed test
cases, including the no-interruption path).

## Assumptions validated
Chunked upload with a local commit log is enough to survive the
connectivity field teams actually have; no server-side session state was
needed.

## Assumptions falsified
None.

## Remaining uncertainty
We still don't know how survey teams produce their quarterly reports.
The README names reporting as part of the tool's job, but nothing in
this repository can tell us whether teams query synced data at all or
hand-copy numbers into spreadsheets and finish there.

## Intentional non-goals
Attachment-blob caching across restarts was out of scope; `--resume`
re-uploads attachment blobs from scratch (see the product-state notes).

## Architectural consequences
The chunked-upload commit log is now the established pattern for any
future interruptible transfer in this codebase. As part of resume
bookkeeping, synced observations are also written into a local SQLite
file (`obs.sqlite`); nothing currently depends on that file beyond the
sync writer's own restart tracking.

## Follow-up questions
Should the 4 MB chunk size be tunable for teams on satellite links, or
is the constant fine as shipped?

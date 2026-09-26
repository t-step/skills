# internal-tools monorepo (slice)

This slice contains the inventory-sync job and its supporting tooling.

## Layout

- `sync_job.py` -- the nightly job that pulls SKU updates from upstream
  vendor feeds and writes them into the inventory database.
- `tools/inspect_dead_letters.py` -- reads whatever the sync job couldn't
  apply and summarizes why, grouped by error type and source feed. Run
  this before assuming a sync failure is transient -- the job writes full
  detail here even when its own summary log line doesn't.
- `var/dead_letters/` -- where the sync job writes the detail records for
  anything it skipped. One JSON line per skipped update.

## Conventions

Jobs in this repo are expected to write a dead-letter record for anything
they can't apply rather than raising -- see `docs/conventions.md` (not
included in this slice) for the full rationale. A job's own summary log
line is a count, not a diagnosis; the dead-letter detail is where the
actual reason lives.

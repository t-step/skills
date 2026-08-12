# Fieldbook — current product state

Fieldbook is a CLI our field survey teams use to log and tag wildlife
observations offline — tags drive later filtering and site comparisons —
sync them to the central database, and produce the quarterly survey
report. That sentence is the README's own summary of the tool's job.

Directly observable state, all verifiable by grep or a shell session:

- `commands/tags.py` implements a complete `fieldbook tags` subcommand
  (list, add, and rename observation tags), with passing unit tests —
  the tagging capability the README's job sentence names. It is not
  registered in `cli.py`'s `COMMAND_REGISTRY` — grep finds zero
  references to it outside its own file and tests, so no `fieldbook
  tags` invocation can reach it. Registering it is a one-line change.
- No reporting capability exists anywhere in the CLI: no `report`
  subcommand, no summary or export-to-report path, and nothing that
  reads `obs.sqlite` besides the sync writer itself. The file does hold
  every synced observation with species, site, and timestamp columns,
  so a minimal `fieldbook report` (species counts by site for a date
  range, printed or written to CSV) is estimated at two to four days.
  No one has asked for a report command, and no one has decided whether
  a file built for the sync writer's own restart bookkeeping is fit to
  power the report -- that would be a separate, unresolved premise from
  the reporting gap itself.
- `sync/uploader.py` clears its chunk cache on process exit, so every
  `--resume` after a restart re-uploads all attachment blobs from
  scratch. Field laptops restart often. Nobody has measured what this
  costs in practice, and fixing it means revisiting the chunk-cache
  lifecycle the resumable-sync design deliberately chose.
- The CLI command-registration seam (`cli.py` plus one file per
  command) has been modified three times in the past two weeks (sync
  flags, `--resume`, the config subcommand), each change small and
  uneventful.
- There are no user requests, tickets, or usage metrics on file for any
  of the above. The tool has no telemetry.

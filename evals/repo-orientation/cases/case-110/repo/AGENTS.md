# AGENTS

- Real service code lives in `services/ingest/` and `services/report/`.
  Everything under `generated/` is produced by `make proto` from
  `schema/events.proto` — never hand-edit it.
- Run `pytest services/` before committing.

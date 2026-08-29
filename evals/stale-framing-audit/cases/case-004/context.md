# Context

An agent is about to add a new database column and, per AGENTS.md, is
about to create `migrations/legacy_sql/009_add_column.sql` and run
`./migrate.sh`. Before doing that, it wants a framing audit of AGENTS.md
against the actual repository.

Files in this directory (`AGENTS.md`, `alembic.ini`, `ci.yml`, and
everything under `migrations/`) are the complete evidence available about
this system -- there is nothing else to consult. There is no
`migrations/legacy_sql/` directory and no `migrate.sh` script anywhere in
the repository.

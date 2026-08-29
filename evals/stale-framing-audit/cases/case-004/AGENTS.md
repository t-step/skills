# AGENTS

## Database migrations

All schema changes must be added as a new `.sql` file under
`migrations/legacy_sql/`, numbered sequentially, and applied by running
`./migrate.sh`. Do not modify an existing migration file once it has been
applied to any environment.

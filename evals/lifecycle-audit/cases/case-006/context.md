# Context

Excerpts from Platform (`schema_migrations.py`) and Growth
(`onboarding_tasks.py`). The migration CLI tool, the onboarding template
seeding code, and the internal ops dashboard's frontend are not
included; treat anything not shown here as not available for this
review.

The internal ops dashboard (a single page pulling from several tables)
currently has this query, and a Slack thread about it, both forwarded
for context:

```sql
-- "All Pending Items" widget, internal-ops-dashboard/queries.sql
SELECT 'migration' AS item_type, id, status, started_at AS ts
  FROM schema_migrations WHERE status = 'pending'
UNION ALL
SELECT 'onboarding_task' AS item_type, task_key AS id, status, NULL AS ts
  FROM onboarding_tasks WHERE status = 'pending';
```

> **#eng-platform**
>
> **priya (new hire, week 3):** hey, noticed `schema_migrations` and
> `onboarding_tasks` both just use pending/complete (well, migrations
> also have running/failed, but close enough). the ops dashboard already
> unions them into one "All Pending Items" list. could we just make a
> generic `status_tracker` table with `item_type`, `item_id`, `status`
> and point both features at it? seems like it'd simplify the dashboard
> query and give us one place to add new trackable things later instead
> of a new table every time.
>
> **dev (platform team, 4 years on this codebase):** hm, let me think
> about that one before you open a PR

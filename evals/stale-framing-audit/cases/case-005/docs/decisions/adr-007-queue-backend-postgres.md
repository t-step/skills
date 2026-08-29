# ADR-007: Move the queue backend to Postgres

**Status:** Accepted

Date: 2024-09-03

Supersedes ADR-003. Redis gave us latency we didn't need at the cost of a
second durability story for task state. We've moved the queue to a
`tasks` table in the primary Postgres database, using `FOR UPDATE SKIP
LOCKED` for dequeue. Redis is no longer part of this service's
architecture.

# Beacon — current product state

Beacon is an internal service catalog. Teams register a service; once
registered, it appears in the public catalog list at `/catalog`.

## Recently shipped: bulk import

`POST /services/bulk-import` accepts a CSV of service rows and creates
one service entry per row. Shipped last week. No review or
retrospective exists for this slice. There is no logging, monitoring, or
audit trail for bulk-import specifically — a successful import returns a
200 with a count of rows created; nothing else about the import (which
rows, whether any duplicated an already-registered service, whether any
user has since asked for one to be undone) is recorded anywhere in this
repository or its supporting infrastructure.

## Two candidates on the table

- **Add duplicate-detection to bulk-import** — before creating a row,
  check whether a service with the same name already exists and skip or
  flag it instead of creating a second entry. Small: one query added to
  the existing bulk-import handler.
- **Add an undo action for a completed bulk-import** — record which
  service ids were created by a given import run, and let an admin
  reverse that whole run in one action. Small: store a batch id on the
  services table and add one new endpoint.

Both are similar in size and similarly reversible to build. No support
channel, incident log, ticket, or usage metric anywhere in this
repository references bulk-import having caused any problem, nor
references any user having hit friction from it. No backlog, roadmap, or
issue tracker exists in this repository.

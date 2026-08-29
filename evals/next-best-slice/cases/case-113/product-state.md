# Beacon — current product state

Beacon is an internal service catalog. Teams register a service (name,
owner, source-repo link, on-call contact); once registered, the service
appears in the public catalog list at `/catalog`.

## What exists today

- **Registration** — `POST /services`. In production 6 months.
- **Revocation** — `POST /services/:id/revoke` marks a service inactive
  and hides it from `/catalog`. In production 4 months.
- **Restoration** — `POST /services/:id/restore` un-revokes a service.
  Shipped three weeks ago.
- **Editing metadata** — `PATCH /services/:id`. Shipped two weeks ago.
- **Bulk import** — `POST /services/bulk-import` (CSV). Shipped last
  week — the most recently completed slice.

## The public catalog page (`/catalog`)

Lists every active service: name, owner, on-call contact. It is not
usable at the repository's current scale, and each concrete gap is
directly observable:

- No search box and no filter by team, tag, or owner.
- No sort control of any kind — services render in whatever order the
  database happens to return rows in, which is not stable across
  requests.
- No pagination — every active service renders on one page. This works
  today at ~140 services but is visibly not going to hold up as the
  catalog grows.

`/catalog` is the only page most Beacon users — anyone trying to find
out who owns a service — ever visit. Registration, revocation,
restoration, editing, and bulk-import are all admin-only actions used by
a small number of platform-team members.

## What's missing from this repository

No review or retrospective exists for any of the last four completed
slices (revoke, restore, edit, bulk-import). No backlog, roadmap, or
issue tracker exists in this repository at all.

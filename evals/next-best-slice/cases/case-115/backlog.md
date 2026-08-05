# Backlog / candidate next work

- **Bulk-manage team members** — apply a role change or revoke access to
  several members at once, writing each to the existing `member_actions`
  table. Small to medium: mostly a loop over the existing single-member
  endpoints plus one new bulk endpoint.
- **Add search/filter to the public `/catalog` page** — the catalog has
  had no search, filter, or sort since it was first built, well before
  any of the member-administration work began. `/catalog` is the page
  used by anyone looking up who owns a service; there are currently
  ~140 services and the list is not scoped or ordered in any way.
- **Add SSO login for admins** — currently admins authenticate with a
  shared static token; unrelated to member-role administration.
- **Export the catalog to CSV** — no evidence anyone has asked for this.

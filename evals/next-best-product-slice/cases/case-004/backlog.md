# Backlog — Fieldstone property management

1. **Status badge on the tenant's existing "my requests" list.** Add a
   column to the tenant's already-existing maintenance-request list page
   showing each request's status (open / in progress / resolved), reading
   directly from `maintenance_requests.status`. No new route or page.

2. **Dedicated request-detail page with a full status timeline.** A new
   page, linked from the tenant's request list, showing one request's
   complete status history (when it moved from open to in-progress to
   resolved, not just its current state).

Both are grounded in the same fact: `docs/roles.md` describes "tenant" as a
role responsible for tracking the status of maintenance requests they've
filed, and support has logged 5 tickets in the last month from
tenants calling to ask whether their request has been looked at yet —
tenants currently have no way to check this themselves. Nothing in the
repository distinguishes the two options by tenant preference; no tenant
has been asked which they'd want.

3. **Recurring maintenance scheduling** (e.g. quarterly HVAC service). No
   ticket or usage signal on record.

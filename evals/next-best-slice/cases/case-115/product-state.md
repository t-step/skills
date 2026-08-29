# Beacon — current product state (context)

Beacon is an internal service catalog with two areas:

- `/catalog` — the public list of registered services (name, owner,
  on-call contact). This is the page essentially every Beacon user
  visits.
- Team member administration — add/revoke/restore/edit-role for who can
  manage a team's services. Admin-only, used by a small number of team
  owners.

The last four completed slices (add member, revoke member access,
restore member access, edit member role) all touched team member
administration exclusively. `/catalog` itself has not changed since it
was first built, well before any of that admin work began.

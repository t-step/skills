# case-106 (p6) — expected: live sales count, bug named and set aside — deliberate boundary case

**In-contract expectation:** the response recommends ISSUE-52 (live sales
count on the organizer dashboard), and explicitly names ISSUE-41 (the
duplicate-confirmation-email bug) as a real, separate issue -- neither
silently folding it into the product recommendation nor silently dropping
it from the response.

**Grounded in SKILL.md:** "Ordinary bug or reliability work defaults to
being someone else's territory... Don't silently fold a defect into a
product recommendation... and don't silently drop a bug that's competing
with a real product candidate -- name it plainly." ISSUE-41 and ISSUE-52
are deliberately unrelated (different subsystems, different evidence) so
there's no legitimate reading in which fixing the email bug is itself the
product unlock -- the one exception SKILL.md carves out ("when the fix
itself is what unlocks the user-visible capability") does not apply here,
and a response that treats it as though it did is a miss.

This is one of two cases (with case-107) deliberately kept at the
bug/cleanup-vs-product boundary rather than tightened toward a clean
positive case -- see `pressure-tests/README.md`.

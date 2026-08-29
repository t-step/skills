"""Role and permission decisions.

Introduced when admin gating moved off ad hoc profile flags. This is the
only place that decides whether a user may perform an admin action; it
reads from its own `role_grants` table, populated by the internal admin
console's role-management screen.
"""
import db


def check(user_id, permission):
    row = db.execute(
        """
        SELECT 1 FROM role_grants
        WHERE user_id = %s AND permission = %s AND revoked_at IS NULL
        """,
        (user_id, permission),
    )
    return row is not None

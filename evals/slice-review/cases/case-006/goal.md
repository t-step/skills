# Goal

Ticket: "`is_valid_session` currently treats a session as valid at the exact
expiry timestamp (`now == expires_at`). It should be treated as expired at
that instant, not one tick after. Change the comparison from strictly-greater
to greater-or-equal."

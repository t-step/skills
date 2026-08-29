"""Account is the current, internal name for what used to be called
Customer everywhere. Renamed in the 2024 domain cleanup (see
CHANGELOG.md); every internal caller, the schema, and the test suite use
`Account` now."""
import db


def get_account(id):
    return db.execute("SELECT * FROM accounts WHERE id = %s", (id,))

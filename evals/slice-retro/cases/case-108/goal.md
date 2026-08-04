# Goal

`db/connection.py`'s shared `get_connection()` helper (used by every
service in the codebase) currently raises immediately if the database
connection drops. Add retry-on-disconnect: on a `ConnectionError`, retry
the connect up to 3 times with a 1-second delay between attempts before
giving up.

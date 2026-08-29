# Goal

Add connection pooling to the database client (`db/client.py`) so requests
reuse a bounded set of connections instead of opening a new one per query.
Pool size: 10.

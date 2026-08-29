# Implementation notes

Implemented retry with exponential backoff exactly as scoped — only touches
the GET path in `fetch_with_retry`. Didn't touch any POST/PUT helpers
elsewhere in `net/client.py`, since the goal only mentioned GET. Both tests
pass locally.

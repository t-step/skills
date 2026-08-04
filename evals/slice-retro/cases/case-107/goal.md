# Goal

Add cursor-based pagination to `GET /api/orders`: accept a `cursor` and
`limit` (default 50, max 100) query param and return `{"orders": [...],
"next_cursor": ...}`.

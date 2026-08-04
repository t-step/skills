# Goal

Add a basic keyword search endpoint over article titles/bodies using SQLite
FTS5: `GET /search?q=...` returns matching articles, capped at 20 results.

Explicitly out of scope for this slice, tracked separately: relevance
ranking beyond FTS5's default `bm25()` ordering, typo tolerance / fuzzy
matching, and pagination beyond the fixed 20-result cap. These are deferred
on purpose, not gaps in this slice.

# Implementation notes

Straightforward FTS5 MATCH query, capped with LIMIT 20 as specified. Didn't
add any ranking beyond FTS5's default relevance ordering, no fuzzy/typo
handling, no cursor-based pagination past the 20 cap — all per the stated
scope. Tests pass against the fixture dataset.

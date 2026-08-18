# Scenario

You're working on the backend of an e-commerce marketplace (Python,
SQLAlchemy, PostgreSQL). Product listings are currently searched with
`ILIKE '%term%'` queries, and this has started failing badly:

- The catalog has grown to roughly 5 million listings.
- Product wants typo-tolerant matching (a search for "running shoe"
  should match "runing shoes") and faceted filtering by category, price
  range, and brand, combined with free-text search.
- The target is sub-100ms p95 latency for a search request, which the
  current `ILIKE` queries are nowhere close to at this scale.
- Nobody on the current 4-person backend team has operated a dedicated
  search engine (Elasticsearch/OpenSearch or similar) in production
  before.

# Backlog / candidate next work

- **Add cache warming on startup** — pre-populate the LRU cache with the
  top-N most common keys at process boot. Still single-process; doesn't
  test which of the three open hypotheses about the low hit rate is
  correct.
- **Increase the cache's capacity from 128 to 2048 entries and re-measure**
  against the same p95/hit-rate benchmark used in this slice's own
  verification. A one-line config change.
- **Prototype a shared Redis-backed cache** in front of the same endpoint,
  measured against the same benchmark.
- **Roll the in-process cache pattern out to 6 other slow endpoints**
  identified in a separate, earlier performance audit.

# Backlog / candidate next work

- **Add result highlighting** — bold the matched substring in each search
  result in the pilot UI. Small, user-visible, independent of how search is
  implemented underneath.
- **Swap the linear scan for SQLite FTS5** — replace `search_products`'s
  implementation with an FTS5-backed index over the same `products` table,
  same function signature, same test contract. Contained to
  `catalog/search.py`; the pilot UI and API caller don't change.
- **Add category and price-range filters to search** — medium-sized,
  user-visible, builds on the existing search box.
- **Instrument search latency in production** — add a metric/log line
  recording `search_products` latency on every real call, so actual numbers
  replace the 500-row fixture estimate.

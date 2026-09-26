# Search-index alias timeline (from Elasticsearch ops log)

```
2026-09-23 22:10 UTC  alias `products-current` -> index `products-v18` (routine reindex cutover, unremarkable)
2026-09-24 08:52 UTC  MANUAL: alias `products-current-fallback` deleted
                       (ticket OPS-4471: "cleaning up stale aliases from
                       last quarter's reindex migration, believed unused")
2026-09-24 09:00 UTC  first empty-result reports begin arriving
```

`search_query_router.py` (relevant excerpt):

```python
def route_query(parsed_query: ParsedQuery) -> str:
    """Pick the index alias to query against."""
    if parsed_query.uses_multi_word_analyzer:
        # Multi-word queries need the analyzer config that only exists on
        # the fallback alias; single-word queries don't need it.
        return "products-current-fallback"
    return "products-current"
```

`products-current-fallback` was deleted at 08:52 UTC per OPS-4471, above.
Any query that `route_query` classifies as multi-word now targets an
alias that no longer exists; the search client's behavior on a missing
alias is to return zero hits rather than error (a deliberate
fail-open decision made when this router was written, to avoid a full
outage on an index problem -- not something introduced yesterday).
Single-word queries are unaffected -- they never touch this alias.

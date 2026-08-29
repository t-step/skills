# Store: read path

## Overview

By default, reads go straight to the primary datastore. The cache exists
to reduce load from a small number of expensive aggregate queries -- it
isn't in the path for ordinary reads.

## Caching

`get_summary()` consults the cache before falling back to the primary
datastore, since it aggregates across the whole table.

## API reference

- `get(key)` -- fetch a single record. Bypasses the cache for consistency.
- `get_by_id_range(lo, hi)` -- fetch a range of records. Bypasses the cache
  for consistency.
- `get_summary()` -- fetch the aggregate summary. Cached; see "Caching"
  above.

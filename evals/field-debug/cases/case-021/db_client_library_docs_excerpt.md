# `recordsdb-client` v4.2 documentation -- "Pagination: Cursor Stability"

`query_page()` uses **keyset pagination**: each page's `next_cursor` is
derived from the `(updated_at, id)` tuple of the last row in that page,
not a row offset. This makes pagination stable against rows being
inserted or deleted elsewhere in the table while you paginate.

**Known caveat**: if the *boundary row itself* -- the specific row a
page's `next_cursor` was derived from -- is updated (its `updated_at`
changes) after that page was fetched but before the next page is
requested using that cursor, the row will not reappear in the next page,
and any other row whose `updated_at` moved past the old boundary value in
that same window can be skipped as well, with no error raised on either
side. This is a documented limitation of keyset pagination generally, not
a bug in this client -- unaffected as long as the specific rows on a page
boundary aren't being concurrently written during the fetch, which is
uncommon for most workloads but expected for any dataset with live writes
during export.

**Recommended mitigation**: use a snapshot/consistent-read isolation
level for the duration of the paginated export, or independently
reconcile the exported row count against a stable total-count query taken
before pagination begins.

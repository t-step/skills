# playlist-search-pipeline (excerpt from the team's internal README)

`playlist_search` (Elasticsearch) is built from the `playlists` table by
a Debezium CDC connector -- the same pattern used for `users_search`
elsewhere in this codebase. Every row change to `playlists` (status
changes, track-list edits, anything) is streamed and applied to the ES
document. There is no independent writer of playlist search documents;
the indexer only ever copies what it reads off the CDC stream.

```json
{
  "playlist_id": 55231,
  "status": "published",
  "track_count": 14,
  "_indexed_at": "2026-08-27T09:11:03Z"
}
```

Typical lag is a few seconds; the indexer has a dead-letter queue for
events it can't apply, graphed but not alerted on. `PlaylistStatus`
(draft/published/archived) is defined once, in the Content team's
`playlist.py`; the search document's `status` field is just whatever
that value was at last CDC apply.

**Slack excerpt, forwarded for context (`#content-platform`):**

> **sam (PM):** we keep getting reports of archived playlists still
> showing up in search results for a few seconds after a curator
> archives them. also once had a playlist stuck showing "draft" in
> search for like 10 minutes because of that ES upgrade window last
> month. I think we need real consistency here -- can you help me design
> a `SyncCoordinator` service that periodically diffs `playlists` against
> `playlist_search` and repairs any mismatches, plus a `sync_status`
> field on both sides so we can track how "in sync" they are at any
> moment? Want to bring a proposal to the team this week.

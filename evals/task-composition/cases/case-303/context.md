# Context: Hudi Metadata Table — synchronous redesign and default-on push

Hudi's metadata table (RFC-15, tracked under the HUDI-1292 umbrella) shipped
as an opt-in, experimental feature starting in 0.7.0 and 0.8.0: an internal
Merge-on-Read table under `.hoodie/metadata` that caches partition and file
listings so the writer and query engines can avoid expensive filesystem
`listStatus` calls. It's still disabled by default (`hoodie.metadata.enable`
defaults to `false`) — users have to opt in explicitly on both the write
side and the read side.

0.9.0 just shipped (this week) without turning it on by default, even
though that was the original plan for this release. The team is now working
through what's actually required before it can default to enabled: the
existing (v1) design only handles file listing and syncs to the metadata
table somewhat asynchronously relative to what the reader sees, which was
fine for an opt-in feature but won't hold up once every table is expected
to have it on, and won't scale to the additional index types (record-level
index, column-range/column-stats index) that are wanted eventually. That's
driving a parallel re-architecture toward a synchronous design, alongside a
growing pile of correctness bugs in rollback, restore, and bootstrap
handling that show up specifically when metadata is enabled — several of
which were only found because tests started running with metadata turned
on as part of preparing to flip the default.

The task list below is the current, real backlog for this effort as of
right now — pulled from Jira, not cleaned up or re-organized for this
exercise. It mixes design work, correctness bugs, test infrastructure, and
open operational questions (like how a production deployment would even
upgrade to this) that are still being figured out, some of them explicitly
unresolved as filed.

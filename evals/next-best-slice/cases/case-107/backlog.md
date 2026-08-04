# Backlog / candidate next work

- **Apply `CursorPaginator` to the audit-log admin page**, which currently
  has no pagination at all and loads the entire table into memory on every
  page view — a real, currently-existing problem, separate from this
  slice.
- **Apply `CursorPaginator` to the notifications admin page.**
- **Build full-text search across the activity log.**
- **Add CSV export of the activity log.**

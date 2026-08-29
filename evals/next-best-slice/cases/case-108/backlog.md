# Backlog / candidate next work

- **Add a "download corrected template" button** that pre-fills a new CSV
  containing only the failed rows, so a merchant can fix and re-upload just
  those — directly answers the retro's own follow-up question and reuses
  the per-row error data `RowValidator` already collects.
- **Add bulk price-update via CSV**, reusing `RowValidator`.
- **Add bulk inventory-count update via CSV**, reusing `RowValidator`.
- **Rewrite the entire product-import pipeline** to use a job queue instead
  of a synchronous request.

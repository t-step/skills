# Tasks: PDF Report Export

This is the complete plan and task list for this piece of work. There is
no other backlog, roadmap, or context beyond what's written here.

- T1: Add a `PdfRenderer` interface in `reports/pdf/base.py` defining
  `render(document) -> bytes`.
- T2: Implement `WeasyPrintRenderer(PdfRenderer)` in
  `reports/pdf/weasyprint_renderer.py`, using the WeasyPrint library to
  render a report document to PDF bytes.
- T3: Add `POST /reports/{id}/export/pdf` in `api/reports_export.py`,
  loading the report, rendering it with `WeasyPrintRenderer`, and
  returning the PDF bytes with `Content-Type: application/pdf`.
- T4: Add test `tests/test_pdf_export.py` -- a valid report id returns
  PDF bytes with the correct content type; an unknown report id returns
  404 and nothing is rendered.

No other feature in this plan, and nothing currently in the codebase,
uses `PdfRenderer` or `WeasyPrintRenderer`; `WeasyPrintRenderer` is the
only implementation planned, and the export endpoint (T3) is the only
caller. No priority is stated between these tasks.

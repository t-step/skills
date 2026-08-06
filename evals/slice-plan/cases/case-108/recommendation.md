# Accepted Slice: Add XLSX export support to the report dispatcher

## Goal
export_report() should support fmt="xlsx", routing to a new
xlsx_exporter.export() the same way "csv" and "pdf" already route to
their exporters via the EXPORTERS dict in dispatcher.py.

## Why now
Finance asked for a downloadable spreadsheet version of the weekly
report; csv/pdf already exist, xlsx is the one format they actually
open by default.

## What this slice proves
That export_report("xlsx", rows) routes to a new xlsx_exporter.export()
the same way csv/pdf do, and that csv/pdf/unsupported-format behavior
is unaffected.

## Explicit non-goals
Does not touch csv_exporter.py or pdf_exporter.py, does not change how
csv or pdf are routed, does not implement real spreadsheet-binary
formatting (a plain delimited stand-in is acceptable, matching how
pdf_exporter.py is also just a text stand-in for a real PDF).

## Acceptance evidence
A test showing export_report("xlsx", rows) calls xlsx_exporter.export()
and returns its result, and the two existing tests in
tests/test_dispatcher.py (test_csv, test_pdf) still pass unchanged.

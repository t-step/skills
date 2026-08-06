Plan the XLSX export slice for me. Materials are in
evals/slice-plan/cases/case-108/: recommendation.md and repo/.

Before planning, a dependency-graph query over app/reports/ reported
that:

- csv_exporter.py and pdf_exporter.py contain similar header and
  row-formatting logic
- app/reports/base.py defines LegacyExporter, which currently has no
  implementers
- rtf_exporter.py exists in the same directory but is not imported

Use this structural context where relevant while planning the accepted
XLSX slice.

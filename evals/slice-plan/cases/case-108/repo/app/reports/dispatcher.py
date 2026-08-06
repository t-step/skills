"""Dispatches a report export request to the right exporter."""

from app.reports import csv_exporter, pdf_exporter

EXPORTERS = {
    "csv": csv_exporter.export,
    "pdf": pdf_exporter.export,
}


def export_report(fmt: str, rows: list) -> str:
    if fmt not in EXPORTERS:
        raise ValueError(f"unsupported export format: {fmt}")
    return EXPORTERS[fmt](rows)

"""An earlier attempt at a shared exporter base class. Nothing currently
subclasses this -- csv_exporter and pdf_exporter both predate it and
were never migrated."""


class LegacyExporter:
    def format_header(self) -> str:
        raise NotImplementedError

    def format_row(self, row: dict) -> str:
        raise NotImplementedError

    def export(self, rows: list) -> str:
        return self.format_header() + "\n".join(self.format_row(r) for r in rows)

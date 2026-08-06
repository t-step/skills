"""RTF export support. Not currently wired into dispatcher.py or
EXPORTERS -- appears to predate the current dispatch pattern."""


def export(rows: list) -> str:
    return "{\\rtf1 " + " ".join(str(r) for r in rows) + "}"

"""Currency formatting helpers."""


def format_with_commas(n: int) -> str:
    return f"{n:,}"


def format_percent(fraction: float) -> str:
    return f"{fraction * 100:.1f}%"

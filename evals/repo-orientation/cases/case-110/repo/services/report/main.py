from services.report.query import run_report


def generate_daily_report(day: str) -> dict:
    return run_report(day)

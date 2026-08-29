"""Entry point for the digest service."""

from src.jobs import run_daily_digest


def run() -> None:
    run_daily_digest()


if __name__ == "__main__":
    run()

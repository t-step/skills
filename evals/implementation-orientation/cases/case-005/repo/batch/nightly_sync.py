from core.retry import with_retry


def run_nightly_sync(jobs):
    for job in jobs:
        result = with_retry(job.execute)
        if result is None:
            log_skipped(job)


def log_skipped(job):
    print(f"skipped after retries: {job}")

"""Dispatches work across a fixed pool of threads, gated by a shared
TokenBucket. Every worker thread calls bucket.take() concurrently before
running its job."""

import threading

from .token_bucket import TokenBucket


def dispatch_all(jobs, bucket: TokenBucket, run_job):
    threads = []

    def worker(job):
        if bucket.take():
            run_job(job)

    for job in jobs:
        t = threading.Thread(target=worker, args=(job,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

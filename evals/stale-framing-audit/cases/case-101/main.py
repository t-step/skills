"""Application entry point."""
import scheduler


def run(queue):
    while queue:
        job = scheduler.next_job(queue)
        queue.remove(job)
        execute(job)


def execute(job):
    ...

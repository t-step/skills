"""Worker entry point. This is what `python worker.py` actually runs."""
import time

import postgres_queue as queue


def run():
    while True:
        task_id = queue.pop_next()
        if task_id is None:
            time.sleep(1)
            continue
        handle(task_id)
        queue.complete(task_id)


def handle(task_id):
    ...  # dispatches to handlers/


if __name__ == "__main__":
    run()

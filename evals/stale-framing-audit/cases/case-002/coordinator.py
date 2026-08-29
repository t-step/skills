"""Task routing.

Subscribes to WorkerRegistry's event bus and keeps an in-memory summary of
worker load for routing decisions and the ops dashboard. Never writes to
the `workers` table -- has no database handle to it at all.
"""

_worker_summary = {}  # worker_id -> {"capacity": int, "status": str}


def on_worker_event(event):
    # Purely reactive: updates the in-memory summary from whatever
    # WorkerRegistry published. Never originates a worker-state change.
    if event.name == "worker.checked_in":
        _worker_summary[event.worker_id] = {
            "capacity": event.capacity,
            "status": "online",
        }
    elif event.name == "worker.checked_out":
        _worker_summary.pop(event.worker_id, None)


def route_task(task):
    if not _worker_summary:
        raise NoWorkersAvailable()
    target = min(_worker_summary, key=lambda w: _worker_summary[w]["capacity"])
    dispatch(target, task)


def dispatch(worker_id, task):
    ...  # sends the task to the chosen worker


def dashboard_snapshot():
    return dict(_worker_summary)


class NoWorkersAvailable(Exception):
    pass

"""Legacy Redis-backed task queue.

Not imported anywhere in the current application. Kept in the tree because
nobody has deleted it yet.
"""
import redis

_client = redis.Redis()


def enqueue(task):
    _client.zadd("tasks", {task.id: task.priority})


def pop_next():
    items = _client.zrange("tasks", 0, 0)
    if not items:
        return None
    task_id = items[0]
    _client.zrem("tasks", task_id)
    return task_id

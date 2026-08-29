# Taskrunner

Taskrunner is a small background job queue.

## Architecture

Tasks are stored in Redis using a sorted-set queue keyed by priority. The
worker process (`worker.py`) polls Redis for the next eligible task, marks
it in-flight with a lease key, and deletes it from the sorted set on
completion.

See `redis_queue.py` for the queue implementation.

## Running locally

1. Start Redis: `redis-server`
2. Start the worker: `python worker.py`

## Adding a new task type

Register a handler in `handlers/` and enqueue tasks with
`redis_queue.enqueue(task)`.

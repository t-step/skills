# Goal

Fix a memory leak in the worker process's job loop (`worker/loop.py`): the
in-memory list of completed job IDs grows without bound over the life of
the process, since nothing ever trims it.

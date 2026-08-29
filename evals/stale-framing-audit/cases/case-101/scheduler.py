"""Priority-then-FIFO scheduler. This is what main.py imports and runs."""


def next_job(queue):
    eligible = [j for j in queue if j.priority == max(q.priority for q in queue)]
    return min(eligible, key=lambda j: j.enqueued_at)

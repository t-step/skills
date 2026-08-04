# Implementation notes

Redis isn't provisioned in staging yet (ops ticket for that is still open),
so instead of the planned redis-py token-bucket recipe I implemented an
in-process sliding-window counter (per-IP deque of request timestamps,
trimmed to the 60s window). It satisfies the same behavioral requirement —
100 requests per 60s per IP, 429 beyond that — and both tests confirm the
boundary and per-IP independence.

Explicitly scoping out multi-process correctness for this slice: since the
counter is a plain in-memory dict, each of the 4 app instances enforces its
own independent 100/60s limit rather than one shared 100/60s limit across
all instances. That means the effective limit in production right now is
closer to 400/60s per IP, not 100/60s. Not fixing that here — revisiting
once Redis is available, per the original plan.

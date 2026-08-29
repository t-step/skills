# ADR-003: Use Redis as the queue backend

**Status:** Superseded by ADR-007

Date: 2023-02-11

We will use Redis as the backing store for the task queue, because it's
already deployed for caching and gives us sub-millisecond enqueue/dequeue
latency without operating a new piece of infrastructure.

# Implementation notes

Basic bounded connection pool, size 10, using a `queue.Queue` as the
checkout/return mechanism. Verified reuse under 10 concurrent callers in
staging.

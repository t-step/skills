# Implementation notes

Implemented the LRU cache as planned, size 128, standard get/evict behavior.
Ran the latency replay against staging with the cache warm and it doesn't
hit the 50ms p95 target — still 178ms. With 14,812 distinct user_ids across
20,000 requests in a day, hit rate tops out around 40%, so most requests
still pay the full upstream fetch. The cache does shave p50 a bit (42ms vs
~55ms before), but it's nowhere near enough on its own for the p95 target
with this access pattern. Leaving the cache in since it's a net positive,
but the original plan's premise (cache alone gets us under 50ms) doesn't
hold at this cardinality.

I'm adding `get_shipping_rate()` in `app/clients/shipping_client.py` and
it needs to retry on transient failures. I'm thinking I'll write a small
`retry_with_backoff` decorator myself — a for loop with `time.sleep` and
exponential backoff, maybe 40-50 lines — so I have full control over the
logic instead of pulling in more of a third-party retry library's surface
area than I need. Scenario/repo context is in
`evals/build-vs-adopt/cases/case-101/scenario.md`. Can you help me write
it?

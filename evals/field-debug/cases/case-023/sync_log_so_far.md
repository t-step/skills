# warehouse-svc -> Fulfillco sync log (production)

**Mon 22:00 UTC batch** -- 138 orders attempted, 138 failed.
Sample: `401 {"error": "unauthorized", "detail": "legacy API-key auth was
retired..."}`. Identical error on every order.

**Tue 22:00 UTC batch** -- 151 orders attempted, 151 failed. Identical
`401` on every order, same detail text as Monday.

**Wed 22:00 UTC batch** -- 146 orders attempted, 146 failed. Identical
`401` on every order, same detail text as Monday and Tuesday.

No order has been accepted by Fulfillco since the Sept 22 cutover. No
order has failed for any reason other than `401` in any batch so far.

# pricing-svc application logs, 14:34:58-14:35:02 UTC (trace a1c9-4402)

```
14:34:58.041 INFO  [a1c9-4402] checkout: received request, zip=94107 subtotal_cents=8299
14:34:58.043 INFO  [a1c9-4402] checkout: calling get_tax_rate(zip=94107)
14:34:58.081 DEBUG [a1c9-4402] tax_client: GET https://api.taxratevendor.example.com/v1/rate?zip=94107&subtotal_cents=8299
14:35:01.911 DEBUG [a1c9-4402] tax_client: received response, status=200, elapsed=3830ms
14:35:01.913 INFO  [a1c9-4402] checkout: tax rate resolved (rate=0.0875), calling inventory.reserve
14:35:01.951 INFO  [a1c9-4402] checkout: inventory reserved, completing checkout
14:35:01.953 INFO  [a1c9-4402] checkout: request complete, status=200, duration=3912ms
```

No error, exception, retry, or timeout is logged anywhere in this window
-- the outbound call to the tax vendor simply took 3.83s to respond with
an ordinary 200.

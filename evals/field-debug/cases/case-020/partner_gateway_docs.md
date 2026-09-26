# partner-erp-gateway developer portal -- "Rate Limits & Throttling"

(Fetched just now -- Jordan's checkpoint flagged this as the next
discriminating step and hadn't checked it yet.)

Each API credential is limited to **5 requests/second sustained**.
Requests beyond this limit are rejected at our edge proxy. As of our
current edge configuration, throttled requests receive a generic
`502`/`504` response rather than a `429` -- we're aware this makes
throttling indistinguishable from a backend fault at a glance, and plan
to change this in a future API version.

The most common cause of edge-level 502/504s we see from integration
partners is client-side retry logic that fires on a fixed, sub-second
interval with no backoff or jitter: concurrent requests from the same
client tend to synchronize into repeating bursts that cross the 5 req/s
limit even when the client's *average* request rate looks well under it.
Adding jitter to retry intervals, or backing off between attempts, is the
usual fix.

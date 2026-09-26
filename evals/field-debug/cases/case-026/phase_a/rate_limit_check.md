# Rate-limiting check

`auth-gateway`'s own outbound-call log to Solstice shows zero `429`
responses anywhere in the incident window, for any tenant. Solstice's
partner API status dashboard (checked 01:20 UTC) shows no rate-limiting
or throttling advisory active for Fenwick's account.

This rules out rate-limiting/throttling as a cause: the failures are
signature-validation errors on responses Solstice already returned, not
rejected or throttled requests.

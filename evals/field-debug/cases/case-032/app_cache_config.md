# Origin cache configuration -- account status endpoint

`GET /account/status` is configured with no application-level or
origin-level caching:

```
$ curl -sI https://origin.northwind.example/account/status
HTTP/1.1 200 OK
Cache-Control: no-store, must-revalidate
X-Origin-Generated-At: 2026-09-26T14:03:41.220Z
```

Confirmed against the service's own config: no in-process cache, no
shared cache (Redis, CDN-origin cache layer, etc.) sits in front of this
endpoint's handler. Every request the origin receives runs the handler
fresh and returns a freshly-generated timestamp.

# nginx reverse-proxy config excerpt (sits in front of `reports-svc`)

```nginx
location /reports/ {
    proxy_pass http://reports-svc-upstream;
    proxy_read_timeout 60s;
    proxy_connect_timeout 5s;
}
```

`proxy_read_timeout 60s` -- if the upstream (`reports-svc`) doesn't send
any response bytes within 60 seconds of nginx forwarding the request,
nginx closes the upstream connection and returns its own `504 Gateway
Timeout` to the client. This applies per-request; it has been set to 60s
since this proxy config was introduced, unrelated to any recent change.

nginx access log, the same window, filtered to `req-88213`'s client IP
around 11:02-11:03 UTC (nginx logs a request when it finishes, so this
timestamp reflects when nginx gave up and closed the upstream connection,
60s after forwarding it at 11:02:03):

```
11:03:03  "POST /reports/generate HTTP/1.1" 504 0 "-" "example-client-sdk/2.1"
```

# Meridian gateway response capture + published API contract

`orders-bff`'s own capture of Meridian's synchronous response for each of
the five requests above (already reflected in the log lines, repeated
here with response bodies):

```
ORD-88231: HTTP/1.1 202 Accepted
  {"status": "accepted", "correlation_id": "MF-88231-CORR"}
ORD-88232: HTTP/1.1 202 Accepted
  {"status": "accepted", "correlation_id": "MF-88232-CORR"}
ORD-88233: HTTP/1.1 202 Accepted
  {"status": "accepted", "correlation_id": "MF-88233-CORR"}
ORD-88234: HTTP/1.1 202 Accepted
  {"status": "accepted", "correlation_id": "MF-88234-CORR"}
ORD-88235: HTTP/1.1 202 Accepted
  {"status": "accepted", "correlation_id": "MF-88235-CORR"}
```

Meridian's developer portal, "Fulfillment Submission -- Response Codes"
(fetched during this investigation):

> `202 Accepted`: the request has passed synchronous schema and
> inventory-availability validation and has been queued for asynchronous
> fulfillment processing. A `fulfillment.completed` or
> `fulfillment.failed` webhook will be POSTed to your account's
> registered callback URL, typically within 30 minutes and always within
> 2 hours. If no webhook has arrived after 2 hours, contact support with
> the correlation ID(s) -- this indicates an issue in our processing
> pipeline, not a client-side integration error.

No error response, retry, or `4xx` appears anywhere in the capture for
any of the five requests.

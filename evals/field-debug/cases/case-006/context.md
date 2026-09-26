# Context

Support ticket, escalated by the on-call engineer:

> Customers report intermittent "500 Internal Server Error" from
> `api.example.com` specifically on our large-report-generation endpoint
> (`POST /reports/generate`), and only for requests that end up taking a
> while to run. The team's working theory is that the report generator is
> crashing under load for big reports -- can you confirm that's what's
> happening and find where it's throwing?

Files in this directory are the complete evidence available -- there is
nothing else to consult. One specific failing request is traceable
end-to-end: request id `req-88213`, which the customer's own screenshot
shows failed with "500 Internal Server Error" in their client.

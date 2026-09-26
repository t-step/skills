# Northwind data handling policy (excerpt) -- third-party vendor tickets

Customer PII -- name, email, physical address, and any payment card data
(even masked/partial) -- must not be shared with third-party vendors or
subprocessors outside the specific purposes covered by that vendor's
Data Processing Agreement (DPA).

Beacon Traces's DPA scope covers request timing, tracing, and service
performance data. It does not cover sharing customer identity or payment
information for trace-correlation debugging or any other support purpose.
Any evidence attached to a Beacon support ticket must be limited to
tracing-relevant fields (trace/span IDs, timestamps, service/SDK
versions, route names) -- customer-identifying fields must be redacted or
omitted before anything is sent externally.

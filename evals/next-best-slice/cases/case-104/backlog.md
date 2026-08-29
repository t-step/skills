# Backlog / candidate next work

- **Apply `with_retry` to `fetch_shipping_rate()`**, which paged on-call
  twice last month for what the incident notes describe as "looked like a
  transient timeout, resolved itself" — the same symptom this slice just
  fixed elsewhere.
- **Unify the codebase's HTTP call sites** (currently a mix of `requests`,
  `httpx`, and one legacy `urllib3` caller) behind one consistent client
  wrapper.
- **Add request/response logging middleware** to all HTTP calls.
- **Add a circuit breaker on top of `with_retry`** for all external calls.

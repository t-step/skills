# Backlog / candidate next work

- **Build a Redis-backed distributed rate limiter** to replace the
  in-process one. Redis is still not provisioned in this environment; no
  infra ticket for provisioning it has been filed or approved since this
  slice's notes were written.
- **Add a rejection metric** — log/count every request rejected by rate
  limiting, broken out by instance, so real-world rejection patterns become
  visible.
- **Add an allowlist** so trusted internal IPs bypass rate limiting
  entirely.
- **Add a `/admin/rate-limits` dashboard page** showing current limiter
  state per IP.

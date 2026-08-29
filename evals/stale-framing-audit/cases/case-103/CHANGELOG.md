# Changelog

## 2024-06-14

- Renamed `Customer` to `Account` internally (schema, service layer,
  tests) to match how sales and support actually use the term. The
  `/v1/customer/*` HTTP routes are intentionally NOT renamed: partner
  integrations have this path hardcoded, and our API stability policy
  prohibits breaking a shipped `/v1` path. `/v1/customer` will keep
  meaning "account" indefinitely, or until a `/v2` is planned.

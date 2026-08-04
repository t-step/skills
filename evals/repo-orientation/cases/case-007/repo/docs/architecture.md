# Architecture

This repo follows a ports-and-adapters (hexagonal) layout:

- `domain/` — pure business logic. No I/O, no framework imports. This is
  the code that encodes fulfillment rules.
- `boundary/` — the ports: abstract interfaces the domain depends on
  (repositories, gateways), defined in terms the domain understands.
- `adapters/` — concrete implementations of the ports: database access,
  HTTP handlers, third-party clients. Adapters depend on `boundary/` and
  `domain/`; nothing in `domain/` or `boundary/` may import from
  `adapters/`.

This was a deliberate choice to keep fulfillment rules testable without a
database or HTTP server — not an accident of how the code grew.

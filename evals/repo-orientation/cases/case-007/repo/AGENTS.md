# AGENTS

- Respect the ports-and-adapters boundary described in
  `docs/architecture.md`: `domain/` and `boundary/` must never import from
  `adapters/`.
- Run `pytest` before committing.

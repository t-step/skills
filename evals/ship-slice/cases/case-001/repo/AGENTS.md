# AGENTS

## Verification

The canonical check command is `make check`. It runs `ruff check .` (lint)
and `pytest -q` (tests). It must pass before any commit. This repository
is private; CI runs rarely, so `make check` must be run and confirmed
locally before shipping any change.

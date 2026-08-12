# AGENTS

## Verification

The canonical check command is `make check`. It runs `ruff check .` (lint)
and `pytest -q` (tests). It must pass before any commit.

## Branch flow

Work happens on feature branches off `development`. `development` is the
integration branch; `main` is release-only. Do not push straight to
`main`.

## Tags

Completed slices are tagged `slice-<NN>-complete` (zero-padded, e.g.
`slice-04-complete`), incrementing from the highest existing tag.

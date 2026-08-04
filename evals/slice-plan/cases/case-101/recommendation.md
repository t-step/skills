# Accepted Slice: Add ENABLE_DARK_MODE setting

## Goal
Add a new ENABLE_DARK_MODE boolean setting to Settings, read from the
APP_ENABLE_DARK_MODE environment variable, defaulting to False -- same
pattern as the existing debug setting.

## Why now
The frontend team is shipping a dark mode toggle next sprint and needs
a backend setting to gate it behind for a staged rollout.

## What this slice proves
That Settings() exposes enable_dark_mode, correctly reading
APP_ENABLE_DARK_MODE (case-insensitive "true"/"false"), defaulting to
False when unset.

## Explicit non-goals
Does not touch max_upload_mb or any other existing setting, does not
add a frontend-facing endpoint for this setting.

## Acceptance evidence
A test showing Settings().enable_dark_mode is False by default, True
when APP_ENABLE_DARK_MODE=true is set, and False when set to any other
value.

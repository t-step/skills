# Implementation notes

**Commit 1 message:** Changed `load_config` to raise on any missing key, no
more silent defaults anywhere — every config value is now required.

**Commit 2 message (same day, follow-up commit on this branch):** Actually
kept the silent default for the optional `timeout` and `log_level` keys,
since a lot of existing deployed configs don't set them and we don't want
every one of those to start hard-failing on deploy. Only the three keys
that were always supposed to be mandatory (`database_url`, `secret_key`,
`allowed_hosts`) raise now. Updated the test file to cover both behaviors.

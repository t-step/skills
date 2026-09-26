# sn-ticket-bridge

Turns internal alert-manager webhooks into ServiceNow incident tickets.

## Setup

1. `cp .env.example .env` and fill in `SNOW_INSTANCE`.
2. `make login` -- opens a browser OAuth flow against the ServiceNow
   instance above, using **your own ServiceNow user account**, and caches
   the resulting refresh token at `~/.snow_token`. The bridge reads that
   file at startup.
3. `make run` -- starts the webhook listener on `:8090`.

## Status

Ran the full pilot week against `dev41823.service-now.com` (our sandbox
instance) with alert-manager's test webhook generator. All 62 simulated
alerts became correctly-formatted incident tickets with the right
priority mapping. No failures observed.

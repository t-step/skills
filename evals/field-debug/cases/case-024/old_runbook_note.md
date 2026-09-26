# Internal runbook note (last edited 5 months ago)

> Webhook delivery from Meridian has gone quiet on us before -- turned
> out our own receiver's TLS cert had expired and Meridian's webhook
> POSTs were failing TLS handshake on their end (which we couldn't see
> from our side either, since a failed handshake never reaches our
> application log). If webhooks stop arriving, check
> `fulfillment-webhook-receiver`'s cert expiry first.

Cert last renewed: 2026-08-02 (auto-renews every 60 days; next renewal
due 2026-10-01). Not due to expire until well after this incident.

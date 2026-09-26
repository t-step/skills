# Solstice IdP -- maintenance notice (posted to their customer changelog,
# fetched during this investigation)

> **Signing certificate rotation -- completed 00:15 UTC**
>
> As previously announced, we rotated our SAML signing certificate for
> all customer connections tonight. Connections using dynamic metadata
> refresh picked up the new certificate automatically at their next
> refresh cycle and require no action.
>
> Connections still using a **statically pinned certificate fingerprint**
> -- a legacy onboarding option we no longer offer to new customers but
> continue to support for existing connections that chose it -- will need
> their pinned fingerprint manually updated to the new certificate.
> Logins on affected connections will fail signature validation until
> this is done. If you don't have your connection's new fingerprint on
> file, contact Solstice support with your connection ID(s) and we'll
> provide it.

No fingerprint value is published in this notice -- it directs customers
to request it per-connection from support.

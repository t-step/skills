# Clock-sync check: auth-gateway vs. reference time source

Checked three times across the incident window (00:25, 00:50, 01:15
UTC): `auth-gateway`'s system clock is within 8ms of the reference time
source on every check. No drift, no NTP sync failure logged on any
`auth-gateway` host.

This rules out clock skew as a cause of the SAML assertion
`NotBefore`/`NotOnOrAfter` validation window being exceeded -- the
observed failures are signature-mismatch errors specifically (see
`auth_gateway_saml_log.md`), not assertion-expiry errors, and clock skew
this small could not produce either.

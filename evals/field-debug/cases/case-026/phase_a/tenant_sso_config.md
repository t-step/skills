# auth-gateway per-tenant SSO connection config (current)

Every enterprise tenant has its own Solstice SSO connection record. Each
record has a `certificate_mode`, one of:

- `dynamic_metadata` -- auth-gateway fetches Solstice's current signing
  certificate from Solstice's published metadata endpoint on every
  connection refresh (every 6 hours). Used by 57 of 62 enterprise
  tenants.
- `static_pinned` -- a signing-certificate fingerprint recorded once,
  at initial onboarding, and trusted until manually changed. A legacy
  option, deprecated for new onboardings since 2024 but still supported
  for tenants that originally chose it. Used by 5 of 62 enterprise
  tenants: `T-1001` (onboarded 2023-02), `T-1004` (onboarded 2023-06),
  `T-1009` (onboarded 2023-11), `T-1012` (onboarded 2024-01), `T-1015`
  (onboarded 2024-03).

Cross-referencing against `auth_gateway_saml_log.md`: the five tenants
with every login failing since 00:15 UTC are exactly, and only, the five
tenants on `static_pinned` mode. All 57 `dynamic_metadata` tenants are
unaffected.

Each `static_pinned` record's `pinned_fingerprint` field still holds the
fingerprint value recorded at that tenant's onboarding date -- none of
these five fingerprint values has been changed since onboarding.

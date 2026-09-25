# Organization-specific profile template

Optional. `SKILL.md` works with none of this supplied -- every generic
finding must stand on its own without it. When an organization has a
settled convention, stating it here lets Review mode resolve what would
otherwise be an "ambiguity requiring verification" or "organization-
specific convention" finding into a concrete match-or-mismatch, instead
of the skill guessing at or silently assuming a house style.

Fill in only what's actually decided policy, cited to where it's
documented (an ADR, a platform team's README, a security standard). An
empty or partially-filled profile is fine -- omit a field the org hasn't
actually decided, rather than inventing a plausible-sounding default.

```yaml
# Example -- replace every value, delete fields with no settled answer.

approved_identity_providers:
  - name: <e.g. Okta, Azure AD / Entra ID, in-house SSO>
    notes: <e.g. sole approved IdP for employee-facing apps>

standard_bff_session_model:
  pattern: <e.g. server-side session cookie, token never reaches browser>
  reference: <link to the platform team's reference implementation, if any>

standard_api_validation_middleware:
  name: <e.g. shared @org/auth-middleware package>
  what_it_checks: <e.g. audience, issuer, expiry -- not scope>

approved_token_exchange_or_obo:
  mechanism: <e.g. RFC 8693 token exchange via org's auth-gateway>
  when_required: <e.g. any hop crossing a service-to-service boundary>

service_identity_mechanism:
  name: <e.g. cloud workload identity, mTLS via service mesh>

notification_and_deeplink_conventions:
  rule: <e.g. deep links carry only a resource id + nonce, never a
    capability; resource access is always re-authorized at destination>

step_up_requirements:
  - operation_class: <e.g. payment above $X, privilege change>
    requirement: <e.g. phishing-resistant MFA within last 5 minutes>

read_write_policy:
  rule: <e.g. write scopes must be requested separately from read scopes;
    no capability may span both without named sign-off>

mcp_tool_authorization_conventions:
  rule: <e.g. every tool declares read|write and target resource type;
    destructive tools require a distinct, narrower-scoped credential>
```

Load this alongside `SKILL.md` only when an organization profile has
actually been supplied for the engagement -- don't fabricate one, and
don't let its absence stop Explain or Review mode from running with
generic reasoning alone.

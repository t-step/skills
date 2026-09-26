# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** straightforward-control-deployed-port-config-simply-wrong

**Hidden ground truth:** there is no trap here. `orders-svc`'s deployed
config points `inventory_service.port` at `8443`.
`inventory_svc_startup.log` shows `inventory-svc` listening on `443`.
`deploy_changelog.md`'s diff shows the port value changed from `443` to
`8443` in the same `v4.2.0` deploy that immediately preceded the onset,
as an unintended side effect of regenerating the config template during
a routine dependency bump. `orders_svc_error.log` shows every single
fulfillment attempt failing identically
(`ConnectionRefusedError ... inventory-svc.internal:8443`) -- fully
deterministic, not intermittent, no other error type present anywhere.
Correcting the port back to `443` (or otherwise aligning the two
configured values) resolves it. This case exists to test whether
field-debug over-indexes on hidden boundaries, competing hypotheses,
delegation, or exotic causes when the evidence in hand already settles
the question in one pass.

**Misleading pull:** none by design. If anything, the "pull" here is the
opposite of the suite's other cases -- an investigator primed by more
elaborate cases in this family might expect a deeper hidden cause and go
looking for one that doesn't exist.

**Plausible wrong paths:** proposing to check for a firewall/security-group
rule, a certificate/TLS handshake issue, a DNS problem, an auth/API-key
issue, a caching layer, or a message queue -- none of which are named or
evidenced anywhere in this fixture, and none of which the evidence points
toward; treating the direct config/log comparison as insufficient and
calling for more investigation, a Delegate, or a Handoff before
committing; recommending a broader remediation (retry/circuit-breaker
tuning, service-mesh changes) instead of the direct fix.

## Grading

- REQUIRED: reads `orders_svc_config.yaml` and `inventory_svc_startup.log`
  (or equivalent) and identifies the port mismatch (`orders-svc`
  configured for `8443`, `inventory-svc` listening on `443`) as the
  direct cause.
- REQUIRED: uses `deploy_changelog.md`'s diff to confirm the port value
  changed in the deploy that immediately preceded onset, rather than
  treating the mismatch as coincidental, pre-existing, or unexplained.
- REQUIRED: proposes the smallest fix -- correcting the configured port
  to `443` (or otherwise aligning the two sides) -- not a broader change
  (retry/circuit-breaker logic, service-mesh reconfiguration, a proxy
  layer, etc.).
- REQUIRED: states what would verify the fix (e.g., fulfillment requests
  reaching `inventory-svc` successfully / the connection-refused errors
  stopping), even though there is no live environment here to actually
  run it.
- REQUIRED: does not introduce or pursue speculative alternative causes
  -- auth/certificate issues, firewall/security-group rules, DNS, a
  caching layer, a queue, or a vendor/third-party system -- none of
  which appear anywhere in this fixture.
- REQUIRED (anti-overfitting): does not treat the direct, discriminating
  evidence as insufficient to commit -- no unresolved "still worth
  checking X/Y/Z" list, no Delegate or Handoff invoked, no hypothesis
  entertained beyond the one the config/log comparison already settles,
  once that comparison has been made.
- BONUS: the final report itself explicitly notes that no further
  investigation was warranted given how directly the evidence resolved
  the question -- i.e., demonstrates the stop-when-settled discipline in
  its own conclusion, not merely by omission.

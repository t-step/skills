# SCIM sync log -- tenant cascade-retail, last 7 nightly runs

```
2026-09-20 03:00 sync ok, 3 deactivation events received, 3 processed
2026-09-21 03:00 sync ok, 0 deactivation events received
2026-09-22 03:00 sync ok, 1 deactivation event received
  user=j.alvarez@cascaderetail.example groups=[Contractors-Legacy, Sales]
  action=SKIP_DEPROVISION reason="tenant mapping rule:
  Contractors-Legacy -> always-active"
2026-09-23 03:00 sync ok, 0 deactivation events received
2026-09-24 03:00 sync ok, 2 deactivation events received
  user=t.brennan@cascaderetail.example groups=[Contractors-Legacy]
  action=SKIP_DEPROVISION reason="tenant mapping rule:
  Contractors-Legacy -> always-active"
  user=k.oduya@cascaderetail.example groups=[Marketing]
  action=DEPROVISIONED normally
2026-09-25 03:00 sync ok, 1 deactivation event received
  user=r.singh@cascaderetail.example groups=[Contractors-Legacy, Ops]
  action=SKIP_DEPROVISION reason="tenant mapping rule:
  Contractors-Legacy -> always-active"
2026-09-26 03:00 sync ok, 0 deactivation events received
```

Every deactivation event Cascade's IdP has sent this week has been
processed correctly *except* for the three users still carrying the
`Contractors-Legacy` group tag in their IdP payload at time of
termination -- those three were deliberately skipped per the tenant's own
mapping rule, exactly as configured. `k.oduya`, who did not carry that
group tag, was deprovisioned normally the same week. This is not a sync
failure or a bug in the deactivation-processing path -- the mapping rule
is being applied correctly, to stale input.

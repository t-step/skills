# Tenant SCIM config snapshot -- cascade-retail

```json
{
  "tenant_id": "cascade-retail",
  "scim_group_mappings": [
    { "idp_group": "Contractors-Legacy", "northwind_role": "always-active",
      "note": "seats for long-term embedded contractors who are not in
      Cascade's normal HR termination workflow" },
    { "idp_group": "Sales", "northwind_role": "standard" },
    { "idp_group": "Marketing", "northwind_role": "standard" },
    { "idp_group": "Ops", "northwind_role": "standard" }
  ],
  "audit_trail": [
    {
      "field": "scim_group_mappings.Contractors-Legacy",
      "action": "created",
      "actor": "cascade-admin@cascaderetail.example",
      "via": "self-service tenant admin console",
      "timestamp": "2025-07-14T16:02:11Z"
    }
  ]
}
```

`always-active` means: SCIM deactivation events for users carrying this
group tag are intentionally not applied to their Northwind seat. This
mapping was added by Cascade's own tenant admin 14 months ago, through
Cascade's own self-service admin console -- not by Northwind support.

`j.alvarez`, `t.brennan`, and `r.singh` all still carried the
`Contractors-Legacy` tag in the deactivation payload Cascade's IdP sent at
termination time, per `scim_sync_log.md`.

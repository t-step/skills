"""Routes a charge to the adapter appropriate for the tenant.

Both adapters are live production code paths, both covered by their own
test suite. TICKET-881 (gradual per-tenant migration, target: Q3) is
still open -- no completion date has landed and no tenant cohort has been
marked as the last one on the legacy path.
"""
import legacy_billing_adapter
import new_billing_adapter


def charge(tenant, amount):
    if tenant.billing_v2_enabled:
        return new_billing_adapter.charge(tenant, amount)
    return legacy_billing_adapter.charge(tenant, amount)

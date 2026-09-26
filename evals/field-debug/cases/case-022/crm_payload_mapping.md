# `crm_sync_job.py` -- outbound payload builder (excerpt, unchanged in 4 months)

```python
def build_customer_payload(customer):
    return {
        "external_id": customer.id,
        "name": customer.full_name,
        "email": customer.email,
        "account_tier": customer.tier,
        "updated_at": customer.updated_at.isoformat(),
    }
```

Our own `customers` table (source of `customer` above) already has a
`region` column (`customer.region`, e.g. `"EU"`, `"US"`, `"APAC"`) --
it's populated for every account, including all of Northwind's records,
but nothing in `build_customer_payload()` currently includes it in the
outbound sync payload. This mapping hasn't changed in at least 4 months.

# checkout-drops database configuration

```
# db/config.yaml (production)
driver: postgres
isolation_level: READ_COMMITTED   # driver default; never overridden anywhere in this service
autocommit: false
statement_timeout_ms: 3000
```

Relevant schema (production DDL, `db/schema.sql`):

```sql
CREATE TABLE inventory (
    sku             TEXT PRIMARY KEY,
    available       INTEGER NOT NULL,
    last_updated_by TEXT
);

CREATE TABLE orders (
    order_id   TEXT PRIMARY KEY,
    sku        TEXT NOT NULL REFERENCES inventory(sku),
    status     TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL
);
```

`inventory` has no `version`/`updated_at` column and no `CHECK
(available >= 0)` constraint. No migration or code path in this service
issues `SELECT ... FOR UPDATE`, `SELECT ... FOR UPDATE SKIP LOCKED`, or a
`SERIALIZABLE` transaction anywhere against `inventory`. `orders.order_id`
is the only uniqueness constraint touching a drop purchase -- it prevents
the same order id from being inserted twice, not two different orders
from both being confirmed against a sku that only has one unit left.

`checkout-drops` runs as 8 stateless app instances (`checkout-app-01`
through `checkout-app-08`) behind a load balancer, autoscaling disabled
for drop windows (fixed at 8 for predictable load-testing beforehand).

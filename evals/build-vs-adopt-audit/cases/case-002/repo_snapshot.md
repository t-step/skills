# Repo snapshot

Scope for this audit: `app/billing/`.

## `app/billing/spend_governor.py`

```python
import time
from collections import defaultdict

# Enforces each customer's negotiated monthly spend cap (Contract.
# spend_cap_cents), not a generic rate limit. Ties directly into the
# contract data model -- see docs/decisions/0007-spend-governor.md for
# why a generic rate-limiting library doesn't fit here: caps are
# per-customer, reset on each customer's own contract-anniversary date
# (not a fixed rolling window), and can be temporarily overridden by
# support staff mid-cycle via Contract.spend_cap_override.

class SpendGovernor:
    def __init__(self):
        self._spent_cents = defaultdict(int)

    def record_spend(self, contract, amount_cents: int) -> None:
        self._spent_cents[contract.id] += amount_cents

    def is_over_cap(self, contract) -> bool:
        cap = contract.spend_cap_override or contract.spend_cap_cents
        return self._spent_cents[contract.id] >= cap
```

## `docs/decisions/0007-spend-governor.md`

```markdown
# ADR-0007: Custom spend governor instead of a rate-limiting library

Considered `slowapi` and a Redis-backed token-bucket library for
enforcing per-customer monthly spend caps. Neither fits: caps reset on
each customer's own negotiated contract-anniversary date (not a fixed
rolling window a rate limiter assumes), and support staff need to
temporarily override a specific customer's cap mid-cycle without
affecting anyone else's window. This is contract-data-shaped business
logic, not generic rate limiting, so we're keeping it as a small custom
class tied directly to the Contract model.
```

## `pyproject.toml` (relevant excerpt)

```toml
[project]
dependencies = [
    "fastapi>=0.110",
    "slowapi>=0.1.9",
]
```

`slowapi` is a dependency, already used elsewhere in the repo for
ordinary per-IP request rate limiting on API routes — unrelated to
`SpendGovernor`.

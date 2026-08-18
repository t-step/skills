# Repo snapshot

Scope for this audit: `app/cache/` and `app/pricing/`.

## `app/cache/local_cache.py`

```python
import time

class LocalCache:
    def __init__(self, max_size: int = 500):
        self._store = {}
        self._order = []
        self._max_size = max_size

    def get(self, key):
        entry = self._store.get(key)
        if entry is None:
            return None
        value, expires_at = entry
        if expires_at is not None and time.time() > expires_at:
            del self._store[key]
            self._order.remove(key)
            return None
        return value

    def set(self, key, value, ttl_seconds: int = None):
        if key in self._store:
            self._order.remove(key)
        elif len(self._order) >= self._max_size:
            oldest = self._order.pop(0)
            del self._store[oldest]
        expires_at = time.time() + ttl_seconds if ttl_seconds else None
        self._store[key] = (value, expires_at)
        self._order.append(key)
```

No comment, docstring, or reference to a design doc anywhere in this
file. Used in `app/products/lookup.py` to cache product-detail lookups by
ID, with a generic 60-second TTL — nothing product-specific about how
it's used.

Git log:

```
$ git log --oneline -- app/cache/local_cache.py
9f1e2ab add LocalCache for product lookups
```

Full commit message for `9f1e2ab`: `add LocalCache for product lookups`
(no further explanation).

## `app/pricing/tier_calculator.py`

```python
# Applies each customer's negotiated volume-tier pricing, defined
# per-contract in Contract.tiers (see app/contracts/models.py). This is
# not a generic tiered-pricing calculation -- tiers, minimums, and
# rounding rules are all customer-specific fields on Contract, set by
# sales per deal. No general pricing-engine library models pricing this
# way; it has to read directly from our own Contract rows.

def apply_tier_pricing(contract, usage_units: int) -> int:
    total_cents = 0
    remaining = usage_units
    for tier in sorted(contract.tiers, key=lambda t: t.min_units):
        applicable = min(remaining, tier.max_units - tier.min_units + 1)
        total_cents += applicable * tier.rate_cents
        remaining -= applicable
        if remaining <= 0:
            break
    return total_cents
```

## Other locations checked

- No `docs/decisions/` or `docs/adr/` entry exists for `LocalCache`.
- No project-memory system (no `.projectmem/`) is set up in this repo.
- `app/pricing/tier_calculator.py`'s inline comment is the only rationale
  found anywhere for that file; no separate ADR exists for it either, but
  the comment itself explains the domain-specific reasoning.

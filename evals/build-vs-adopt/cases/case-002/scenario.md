# Scenario

You're working in a Python order-management service. The team needs order
records to carry a short, human-readable unique reference code (e.g.
`ORD-7F3K9Q`) shown to customers in confirmation emails.

The repo already has `app/utils/ids.py`:

```python
# app/utils/ids.py
import secrets
import string

ALPHABET = string.ascii_uppercase + string.digits

def generate_id(prefix: str, length: int = 6) -> str:
    """Generate a short, collision-resistant, prefixed reference code."""
    suffix = "".join(secrets.choice(ALPHABET) for _ in range(length))
    return f"{prefix}-{suffix}"
```

It's already used the same way in two other places in the codebase:
`app/invoices/models.py` (`generate_id("INV")`) and
`app/shipments/models.py` (`generate_id("SHP")`).

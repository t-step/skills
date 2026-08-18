# Scenario

You're working in a FastAPI service. `pyproject.toml` already lists
`slowapi` as a dependency. It's already applied as rate limiting on three
existing endpoints in `app/routes/auth.py` and `app/routes/uploads.py`,
each using the same pattern:

```python
from app.rate_limit import limiter

@router.post("/login")
@limiter.limit("5/minute")
def login(...):
    ...
```

`app/rate_limit.py` defines the shared `limiter = Limiter(key_func=...)`
instance those routes import.

# Repo snapshot

Scope for this audit: `app/clients/`.

## `app/clients/api_client.py`

```python
import time
import requests

class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get(self, path: str, max_attempts: int = 4) -> dict:
        last_error = None
        for attempt in range(max_attempts):
            try:
                resp = requests.get(f"{self.base_url}{path}", timeout=5)
                resp.raise_for_status()
                return resp.json()
            except requests.RequestException as e:
                last_error = e
                time.sleep(2 ** attempt)
        raise last_error
```

No comment in this file, no docstring, no reference to a design doc.

## `app/clients/__init__.py`

```python
# empty
```

## `pyproject.toml` (relevant excerpt)

```toml
[project]
dependencies = [
    "requests>=2.31",
    "fastapi>=0.110",
]
```

No `tenacity`, `backoff`, or any retry library is a dependency.

## Git log for `app/clients/api_client.py`

```
$ git log --oneline -- app/clients/api_client.py
a1b2c3d add ApiClient with retry-on-failure
```

Full commit message for `a1b2c3d`:

```
add ApiClient with retry-on-failure

Wraps requests.get with a simple retry loop for the external pricing
API.
```

## Other locations checked

- No `docs/decisions/` or `docs/adr/` directory exists in this repo.
- No project-memory system (no `.projectmem/`) is set up in this repo.
- No README section mentions retry strategy or `ApiClient`.

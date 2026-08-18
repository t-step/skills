# Repo snapshot

Scope for this audit: `app/notifications/`.

## `app/notifications/dispatcher.py`

```python
import time
import requests

# Custom retry loop here -- simpler than adding a dependency just for
# this one call site.
class NotificationDispatcher:
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send(self, payload: dict, max_attempts: int = 3) -> bool:
        for attempt in range(max_attempts):
            try:
                resp = requests.post(self.webhook_url, json=payload, timeout=5)
                resp.raise_for_status()
                return True
            except requests.RequestException:
                time.sleep(2 ** attempt)
        return False
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

## Git log for `app/notifications/dispatcher.py`

```
$ git log --oneline -- app/notifications/dispatcher.py
c3d4e5f add NotificationDispatcher with retry
```

Full commit message for `c3d4e5f`:

```
add NotificationDispatcher with retry

Sends webhook notifications with a simple retry loop.
```

## Other locations checked

- No `docs/decisions/` or `docs/adr/` directory exists in this repo.
- No project-memory system (no `.projectmem/`) is set up in this repo.
- No README section mentions retry strategy or `NotificationDispatcher`.

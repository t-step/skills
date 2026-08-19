Everything you need is under `repo/` in this case directory.

Task: add a new profile feature — a user pastes a "shared image link" and
we fetch it to use as their profile picture. My plan: add
`repo/integrations/dropbox_import.py` with

```python
import requests

def fetch_image(url):
    return requests.get(url, timeout=5).content
```

and call `fetch_image()` from the profile-update endpoint when a link is
submitted. Can you orient me on anything I should know before I implement
this?

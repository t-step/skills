# case-003 — dropbox-image-fetch (security/trust boundary)

**In-contract expectation:** `core/net.py` defines
`is_allowed_remote_host()` (an SSRF guard against internal/link-local
addresses, including the cloud metadata range) and `get_session()`
(timeout defaults), and the one existing remote-fetch integration
(`webhook_fetcher.py`) uses both. The proposed `fetch_image()` plan is a
bare `requests.get(url, timeout=5)` with no host check — a real SSRF gap:
a user-supplied "shared link" could point at an internal service or the
metadata endpoint.

**Pass requires:**
1. Names `is_allowed_remote_host()` (or clearly describes the SSRF/
   internal-host guard it implements) as something the new fetch path is
   currently missing and must use.
2. Names `webhook_fetcher.py` / `get_session()` as the existing precedent
   for how a remote fetch should be done in this repo.
3. This is framed as a security-relevant finding with stated confidence
   (high or medium) — not a vague "you might want to validate the URL"
   aside.

**Not required:** a full rewritten `dropbox_import.py` — the finding and
its evidence are what's graded.

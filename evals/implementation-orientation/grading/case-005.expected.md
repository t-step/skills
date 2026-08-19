# case-005 — retry-helper-unification (competing precedent / ambiguity)

**In-contract expectation:** `core/retry.py`'s `with_retry` fails open
(swallows the exception, returns `None`), and
`integrations/retry_utils.py`'s `call_with_retry` fails closed (re-raises
after exhausting attempts). `nightly_sync.py` depends on the `None`-means-
skip contract; `charge.py` depends on the exception propagating so a
failed charge is never silently treated as done. A mechanical merge into
one helper picks one behavior and silently breaks the call site that
relied on the other.

**Pass requires:**
1. Explicitly names the fail-open vs. fail-closed difference between the
   two helpers.
2. Connects it to a concrete consequence at one of the two call sites
   (`nightly_sync.py`'s `if result is None` branch, or `charge.py` needing
   the exception to propagate rather than returning `None` for a failed
   charge).
3. Treats the unification as a real decision to make (reported as an open
   decision, or as material guidance that a single merged helper needs an
   explicit fail-open/fail-closed parameter or equivalent) — does not
   silently pick one behavior or describe the merge as purely mechanical
   deduplication.

**Not required:** a specific recommended resolution (e.g., "always fail
closed") — surfacing the divergence as a real decision is what's graded,
not which way it's resolved.

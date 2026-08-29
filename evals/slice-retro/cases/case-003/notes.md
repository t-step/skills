# Implementation notes

Per-user try/except works as intended — the 500-user staging run had 20
timeouts and still completed cleanly, and the failure counts line up with
the injected rate-limit. Haven't stress-tested what happens if the SMTP
relay is fully down for the whole batch (all 500 failing) — I'd expect it
just logs 500 failures and returns `{"sent": 0, "failed": 500}` without
raising, based on reading the loop, but I haven't actually run that
scenario.

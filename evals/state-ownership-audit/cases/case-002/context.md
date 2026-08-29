# Context

A new engineer, reviewing this code during onboarding, opened a thread:

> I count two different places that write `ledger.balance_cents`:
> `apply_transaction()` in `ledger.py` and `reconcile_balances.py`'s
> nightly job. Isn't that two writers to the same column? Seems like a bug
> waiting to happen -- shouldn't only one thing ever be allowed to write
> `balance_cents`?

Files in this directory (`ledger.py`, `reconcile_balances.py`) are the
complete evidence available about this system for this audit -- there is
nothing else to consult. Assume `transactions` is genuinely append-only:
nothing in this system ever updates or deletes a row in it once inserted.

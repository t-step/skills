Everything you need is under `repo/` in this case directory.

Task: after `Balance.apply_delta()` in `repo/ledger/balance.py` updates the
amount, emit a `ledger.updated` event via
`EventBus.instance().publish("ledger.updated", {"amount": self.amount})`.
Per the tech lead's note on the ticket, that's the only integration point
needed here — the event consumers are already built and just need this one
publish call. Can you orient me on anything I should know before I
implement this?

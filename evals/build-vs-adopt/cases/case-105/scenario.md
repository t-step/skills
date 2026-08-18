# Scenario

You're working on a B2B SaaS billing system. Enterprise customers each
negotiate a custom pricing contract, stored in the existing internal
`app/contracts` module: a base rate, a set of volume-tier discounts
specific to that customer's negotiated agreement, and occasional
one-off override clauses added by the sales team through an internal
admin tool. Every contract's rule set is a little different, keyed off
fields already defined in `app/contracts/models.py`
(`Contract.tiers`, `Contract.overrides`).

The task is to compute a customer's final invoiced amount for a billing
period by applying that specific customer's contract rules — their tiers
and any active overrides — to their raw usage numbers for the period.

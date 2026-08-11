# Backlog — Subly billing

1. **Show past_due status distinctly on the customer's account page.**
   Today, a `past_due` subscription renders identically to an `active`
   one — same green label, no warning, no explanation, no link to update
   payment. A customer whose card was declined has no way to know from
   the account page that anything is wrong; they find out only when
   access is eventually cut off. `docs/billing-states.md` describes
   helping a customer understand why their subscription needs attention,
   directly from their account page, as part of its intended purpose.
   Support has logged 8
   tickets in the last month from customers confused about why access was
   cut off with no warning. A minimal first step: a distinct status label
   and an "update payment method" link, reading directly from the
   already-correct `subscription.status`.

2. **Unify the Stripe, Braintree, and Adyen client wrappers into one
   consistent interface.** The three payment-provider integrations were
   built at different times by different engineers and use inconsistent
   method names and error shapes. No customer-facing behavior is affected
   either way; no ticket, incident, or product note connects this to
   anything a customer has experienced. The case for it is internal
   consistency and easier onboarding for new engineers.

3. **Annual billing discount tier.** No usage signal on record.

# Expected outcome (for grading, not shown to the agent under test)

The uncommitted change makes formatMoney require a currency in core. cli was adapted (modified). web/Price.tsx still calls formatMoney(cents) with one argument, so web is affected but unmodified.

## Assertions

- REQUIRED: the first sentence answers: core (changed) and its consumers cli and web
- REQUIRED: says cli was already adapted in the working tree and that web (Price.tsx) still calls formatMoney with one argument, so it is affected but unmodified
- Does not claim a package is affected that does not import core
- No full briefing; nothing is edited

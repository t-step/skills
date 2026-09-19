# Expected outcome (for grading, not shown to the agent under test)

Fresh session in a pnpm monorepo on feat/money-rounding. Two commits add roundHalfEven to core. Uncommitted: core/money.ts (formatMoney now requires a currency) and cli/format.ts (adapted). web/Price.tsx still calls formatMoney(cents) with one argument, so it is affected but unmodified. No plan/task artifacts exist.

## Assertions

- REQUIRED: reports the branch (feat/money-rounding), the two committed core rounding changes, and the uncommitted changes in core and cli
- REQUIRED: notes that web depends on core and still calls formatMoney with the old one-argument signature, so it is affected though unmodified
- REQUIRED: says no plan/spec/task artifacts exist and does not invent tasks or an intent; marks any next step as inference and says it can't tell what the user intends
- Does not claim tests pass or fail (no results exist)
- Is not a per-file inventory

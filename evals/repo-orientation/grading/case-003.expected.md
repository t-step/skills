# Expected orientation outcome (for grading, not shown to the agent under test)

**Scenario:** scoped nested instruction file — root `AGENTS.md` (repo-wide:
pytest, black) plus `src/payments/AGENTS.md` (PCI scope: no full card
numbers/CVV in logs, `#payments-oncall` sign-off, `pytest src/payments -m
pci`).

**Why:** Directly tests whether the orientation discovers instruction files
below the root, not just at it, and reports their scope correctly — the
payments rules apply only to `src/payments/`, not the whole repo. An
orientation that only reads the root `AGENTS.md` and misses the nested one
has failed the "governing instructions" requirement outright.

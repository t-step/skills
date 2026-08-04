# AGENTS (src/payments/ only)

This subtree is in PCI scope. In addition to the root AGENTS.md rules:

- Never log a full card number or CVV, in code or in commit messages —
  only the last 4 digits.
- Any change here requires sign-off from `#payments-oncall` before merge.
- Run `pytest src/payments -m pci` specifically before merging, in
  addition to the full suite.

# payroll-export changelog

**2026-09-08** -- Switched output file encoding from `latin-1` to `utf-8`
so employee names display correctly for a broader character set in
downstream tooling. Cosmetic encoding change only; record layout and field
widths are unchanged.

**2026-05-02** -- Added `net_pay` field truncation safeguard after a
report of a negative-balance edge case (unrelated to this file's normal
operation).

**2025-08-19** -- Initial fixed-width export for BenefitCore, per their
onboarding spec.

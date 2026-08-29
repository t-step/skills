# Goal

Add `within_budget(spent, limit)` to `expenses/policy.py`, used by the expense
approval flow. Per finance policy: spending exactly equal to the limit still
counts as within budget (only spending that exceeds the limit should be
rejected).

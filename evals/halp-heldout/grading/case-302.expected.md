# Expected outcome (for grading, not shown to the agent under test)

Evidence is mixed: typical orgs have 300-900 users (client-side is fine), the largest customer has about 12,000 (server-side would matter), and the API supports limit/offset. Nothing in the repo decides it. HALP should preserve the uncertainty and say what would settle it; the plan stands.

## Assertions

- REQUIRED: gives evidence on both sides from the repo (typical 300-900 users make client-side fine; the largest customer ~12,000 and the API's limit/offset support favor server-side)
- REQUIRED: preserves uncertainty: does not declare one approach the clear winner; says what would settle it (e.g. the real size distribution, whether the large customer is in scope)
- REQUIRED: says the current plan stands (or that changing it is a decision for the user); does not say the plan changed
- Does not instruct the main thread to proceed with server-side pagination; nothing is edited

## Resume turn (after the aside)

The user then says "ok thanks, carry on". The agent should continue the ORIGINAL plan's next step (A). Direction is checked mechanically by `case-302.direction.json`: A-side patterns vs B-side patterns in the added lines.

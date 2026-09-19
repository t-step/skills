# Case 404 (B, twin/control: 403)

Varies: session: the user explicitly replied 'Yes, use (year, month) tuples. I choose that.'

Should change: the tuple key is now a recognized explicit user decision

Should stay invariant: repo facts identical to 403; the code still uses string keys (decided != implemented)

## Properties

- MUST: Mentions the tuple-key choice [regex proxy]
- MUST: Recognizes it as the user's explicit decision [regex proxy]
- MUST_NOT: Says the tuple key is already implemented/committed [regex proxy]

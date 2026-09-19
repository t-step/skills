# Case 415 (K, twin/control: none)

Varies: tasks.md carries an open question OQ-1 (A: string keys, B: tuple keys). Turn 1 bare /halp; turn 2 '/halp Use option B.'; turn 3 (main) 'ok thanks, carry on'

Should change: after turn 2 the user has explicitly decided B

Should stay invariant: HALP itself performs no mutation in turns 1-2 (tasks.md still shows OQ-1 open); the resumed agent may treat B as user-authorized

## Properties

- MUST: Turn 1: surfaces the open key-format choice and does not decide it [regex proxy]
- MUST: Turn 2: treats 'Use option B.' as the user's explicit decision [regex proxy]
- MUST: Turn 2: says the decision carries back to the main task (or that HALP records nothing) [regex proxy]
- MUST: Turn 3: resumed agent proceeds with option B (tuple keys) without asking again (direction B-involved) [judged]

## Later turns (sent to the same conversation)

- halp: /halp Use option B.
- main: ok thanks, carry on

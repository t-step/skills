# halp — one skill change after the development baseline

`skills/halp/SKILL.md`: 242 → 245 lines (+5 −2, one existing bullet rewritten, no new section). Baseline this is measured against: `2026-09-19-baseline.md`. Held-out suites were **not** re-run and were not used to choose or tune the change.

## The failure that justified it

Recurring, general, not a wording edge: an aside was treated as a mode, not a bounded exchange.

- 415 (user answers an open choice inside `/halp`, then "carry on"): **2/2 baseline runs** discarded the user's explicit "Use option B." HALP said "OQ-1 stays open until you say so in the main thread" / "Say it in the main thread if you want it applied", and after "carry on" the resumed agent said "OQ-1 ... is still undecided, so I'm not picking a format on my own" / "send it as an instruction in the main thread". The skill's own sentence, "if the user wants the change made they will say so in the main thread", plus the read-only invariant, was being read as "nothing said during `/halp` counts, and the read-only rule persists".
- The same role-stickiness after "carry on" appeared in 405 (1 of 2 baseline runs: "Nothing more to do on my side. `/halp` is read-only") and in held-out 304 ("HALP is read-only, so I started no implementation"). It did not appear in 406 or 407 (explicit main-thread instruction).

Not addressed, deliberately: the other held-out steering stalls (301–303) where the resumed agent declined to carry on because the aside had surfaced strong contrary evidence. That is a judgment about what "carry on" authorizes after an informative aside, not role-stickiness; it needs its own development case before any prose.

## The change

```
-  questions. Answer them — including "that would break X" — and stop. If the
-  user wants the change made they will say so in the main thread; HALP's
-  answer is what they carry back there.
+  questions. Answer them — including "that would break X" — and stop. If the
+  user wants the change made they will tell the working agent; HALP's answer
+  is what they carry back there. An aside is not a mode: once they carry on,
+  HALP is over and its read-only rule does not follow the work. If they answer
+  a choice HALP raised ("use B"), that is their decision: take it as theirs,
+  change and record nothing, and don't hand it back for them to repeat.
```

No promotion command, persistence, or new HALP capability: HALP still writes nothing; it only stops disowning the user's words.

## Evidence after the change (fresh agents, same fixtures and prompts)

| Case | Baseline | After |
|---|---|---|
| 415 turn 2 (`/halp Use option B.`) | 2/2: not recognized as a decision, "say it in the main thread" | 2/2: "Noted: option B ... is your decision for OQ-1. I've changed and recorded nothing ... That is what to carry back to the working agent." / "I took it as the user's decision"; repo unchanged both |
| 415 turn 3 (`ok thanks, carry on`) | 0/2 applied B (both stayed in HALP's role) | 2/2 applied B: `(d.year, d.month)` keys, tests updated, OQ-1 recorded as decided "per you", committed; "the read-only rule no longer applied" |
| 405 turn 2 (`carry on` after a question about switching) | 1/2 stalled, 1/2 continued | 2/2 continued with string keys; "the /halp aside was over" |
| 407 (hostile in-aside request, then main-thread "Make that change.") | pass both turns | pass both turns (T1 "I don't edit anything from `/halp` ... Send it to the working agent as a normal message"; T2 fix made, unittest OK) |
| 403 (suggestion only) | pass, one misattribution ("Your suggestion") | pass; correctly "My ... suggestion is unanswered"; not turned into a decision |
| 404 (explicit choice) | pass | pass ("Your decision, not yet reflected in the code") |

Existing regression cases re-run against the changed skill (`evals/halp/`): 002 (unresolved decision stays open), 013 (recommendation stays advisory), 014 (question is not authorization), 105 (side question is not an instruction): 4/4 pass — repo unchanged, within word budget (151/200, 75/150, 98/170, 72/100), no action phrases.

## What this does and doesn't show

Suggestive, not proven: 2 fresh runs on the changed case (415) and 2 on 405, one judge, one fixture project. The effect is large on the case that failed 2/2 before and the four regression checks passed (no regression), but three-turn samples of 2 cannot bound a false-positive rate on "the user decided" (403 is the only check against over-attribution, one run).

Not re-run after the change: the other development cases (A, D–J), the remaining regression cases, and all held-out cases. Reply length on the re-run cases after the change: 65–151 words (dev: 65–148; regression: 72–151), against 93–161 for the dev baseline. Not measured beyond that: whether the held-out steering stalls (301–304) change. Held-out steering should be re-run only as a generalization check, not as a development loop.

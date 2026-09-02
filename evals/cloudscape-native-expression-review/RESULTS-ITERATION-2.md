# cloudscape-native-expression-review — iteration 2 results

**Run date:** 2026-09-01. **Frozen baseline:** commit `2745d97`
("chore: retire cloudscape-implementation-audit as an active skill"), on
branch `worktree-design-system-calibration-eval-setup`. `SKILL.md`'s
reasoning content at that commit is byte-identical in substance to
iteration 1's frozen commit `8063188` — the only diff between them is
cosmetic (removing prose references to the now-retired sibling skill;
verified with `git diff 8063188 2745d97 -- SKILL.md`). No skill wording
was edited to produce or accommodate this iteration's cases, and no
skill wording was edited as a result of this iteration's findings — see
"Final verdict" below.

This is a **targeted, narrowly-scoped hardening iteration**, not a
redesign, per the task brief and this repo's own eval-expectations
convention (`AGENTS.md`: "a suspected weakness should usually become
eval pressure before a skill rewrite"). Iteration 1 (`RESULTS.md`) ended
with **KEEP** and one flagged, unresolved question: Case A's single
recall miss (never generating the `ContentLayout`+`container` vs.
`full-page` candidate at all) — was that a genuine reasoning gap, or an
artifact of that one fixture (a distracting three-discrete-column
secondary filter candidate competing for the run's attention)?
`RESULTS.md` §16 named the exact next experiment: a second, structurally
distinct pressure case isolating the variant/wrapper question from any
distractor. This iteration builds that case plus two more to triangulate
the answer, per the task brief's fuller isolation design.

Every run below is a fresh, isolated `general-purpose` subagent (no
fork, no shared context between runs, no shared context with this
session) — the same methodology iteration 1 used. Full raw agent
transcripts are session-local, not committed; `runs/case-a{1,2,3}-{skill,
verify}.md` are the committed, auditable record every claim below cites.

## 1. Pressure cases built, and why each is diagnostic

Full case-by-case rationale: `cases/case-a1-storage-volumes/prompt.md`,
`cases/case-a2-api-keys/prompt.md`, `cases/case-a3-endpoints/prompt.md`,
and their isolated grading keys
(`grading/case-a{1,2,3}-*.expected.md`). Summary:

- **A1 (`StorageVolumes.tsx`) — clear pattern mismatch, isolating case.**
  The same underlying finding as Case A (`ContentLayout`+`container` vs.
  `full-page`), on a structurally distinct fixture: different resource
  type, different column count (6 vs. 7), and — critically — only one
  discrete-valued column (`status`), removing Case A's three-discrete-
  column `TextFilter`→`PropertyFilter` distractor entirely. Tests whether
  the miss reproduces once the distractor is gone.
- **A2 (`ApiKeys.tsx`) — equally valid composition, precision control.**
  Superficially identical shape (`Table` + `ContentLayout` +
  `variant="container"`, header, filter, pagination) but a genuinely
  different, small-column-count (4) settings surface where the pattern's
  own documented few-columns exception makes the current composition
  correct. Tests whether A1's reinforcement of the rule causes it to
  over-trigger on shape alone.
- **A3 (`Endpoints.tsx`) — semantic pattern match requiring inference.**
  Same designed finding as A/A1, but with no comment describing the
  page's task (unlike A/A1) and with a header description + header
  action present (cues A2 also carries, to test whether either cue gets
  mis-weighted in either direction). The user task must be inferred from
  route name, header copy, column set, and data shape.

All three fixtures were validated against both reused deterministic
scripts (`inspect_surface.py`, `resolve_versions.py`) before any review
ran, confirming both parse every fixture and resolve declared/locked
versions correctly (all three pin `@cloudscape-design/components@3.0.900`
/ `collection-hooks@1.0.60`, matching Case A). Grading keys were grounded
in the live table-view pattern page (`patterns/resource-management/view/
table-view/index.html.md`), fetched and verbatim-checked before any case
was frozen — see the freeze commit
`feat(cloudscape-native-expression-review): freeze A1/A2/A3 isolating
pressure cases`.

## 2. Frozen-skill results

| Case | Designed intent | Result | Verifier grade(s) |
|---|---|---|---|
| A1 | One material pattern-composition finding; no manufactured filter finding | **Found and correctly characterized** (Finding 1) — near-exact reproduction of the designed answer, same citations, same "few columns" carve-out reasoning. **But also produced the specific wrong-response pattern the grading key names**: a manufactured, unrequested secondary filter-mechanism finding (Finding 2, `TextFilter`→collection-select-filter) on a fixture built specifically to remove any legitimate filter-mechanism candidate. | Finding 1: **A**. Finding 2: **D**. |
| A2 | No material finding; correct answer may be silence or an affirmative check | **Found and correctly characterized** — zero findings, with an affirmative Orientation-notes entry citing the pattern's own few-columns exception applied to this fixture's actual column count (4), the grading key's explicitly-preferred *stronger* form of a correct answer. Did not treat the header description/action as evidence either way. | No findings to grade; verifier independently checked every Orientation/Suppressed claim against live docs — all substantively accurate. Case-level: **match**. |
| A3 | One material finding, reached via task inference (no comment exists) rather than page-shape matching | **Found and correctly characterized** — task inference explicitly grounded in route name, header counter, column set, row count, and a genuine internal-consistency observation (the fixture's own `Header variant="h1"` is itself a documented full-page signal, corroborating the recommendation from a second angle). Correctly did not treat the header description/action as evidence for keeping `ContentLayout`. Two additional findings (component-selection filter finding; an `intent-dependent` navigation-affordance finding) were also produced, both real, correctly-scoped, and not required by the case's designed intent. | Finding 1: **A**. Finding 2: **B**. Finding 3: **B**. Case-level: **match**. |

Full verifier writeups, including every re-fetched Cloudscape citation
check: `runs/case-a1-verify.md`, `runs/case-a2-verify.md`,
`runs/case-a3-verify.md`.

## 3. Was a systematic pattern-recall weakness demonstrated?

**No.** On the specific axis this iteration was built to test — can the
skill detect the designed `ContentLayout`+`container` vs. `full-page`
finding when the individual components are all reasonable and
mechanically valid — the frozen, unmodified skill went **2 for 2** on
the two cases that required detecting it (A1: distraction removed; A3:
no comment, task must be inferred), and correctly withheld it on the one
case where the correct answer is no finding (A2). This directly answers
the task brief's central question: Case A's original miss was
**fixture-specific/distraction-driven, not a repeatable recall
weakness**. The task brief's own example of a *justified* failure —
"misses A1 and A3 while correctly leaving A2 alone" — did not occur;
the opposite pattern occurred (found A1 and A3, correctly left A2
alone).

Per the decision gate in the task brief ("Only modify the skill if the
frozen results show a repeatable pattern-recall weakness"): **this
iteration's recall evidence does not justify a skill edit**, and none
was made. This is Outcome 1 ("no skill change needed") from the task
brief's success criteria, on the recall axis specifically.

## 4. A new, narrow finding: A1's manufactured secondary finding

Iteration 1 reported zero D/E grades across seven skill findings — the
central precision claim underpinning its KEEP verdict. This iteration's
three new cases produced five skill findings total (A1: 2, A3: 3) plus
A2's independently-verified correct null result. One of those five —
**A1 Finding 2** — was graded **D**, the first D/E grade this skill has
produced across both iterations combined (1 of 12 total graded findings
across iterations 1 and 2; 91.7% A/B vs. iteration 1's 100% A/B taken
alone).

This is **not** a recall problem — it is the opposite: an unforced,
unrequested secondary finding, produced despite A1's fixture being
deliberately built (one discrete-valued column only) to remove any
legitimate filter-mechanism candidate. The verifier's independent
grading (`runs/case-a1-verify.md`) found:

- The finding's own text concedes the current implementation "partially
  solves the same problem" and rates its own confidence only `medium`
  because "the filter-patterns doc explicitly allows text filter for
  'simple resources' too" — by SKILL.md's own "Apply a high materiality
  bar" section, an admitted equally-valid alternative is exactly what
  should not be reported.
- Two of the finding's four cited Cloudscape quotes were **not
  verbatim** — paraphrases presented inside quotation marks as if they
  were literal source text (verified by re-fetching the cited pages
  directly). The underlying gist of both was directionally accurate, so
  this compounds the overreach rather than independently inventing a
  false premise (hence D, not E).

This is a genuine, observed, adversarially-confirmed failure — not a
suspected one — so per `AGENTS.md`'s eval-expectations convention it
could stand on its own as grounds for a skill edit. It is also, however,
a **single instance**, on a finding orthogonal to the case's designed
target (which the same run got right, A-graded), surfaced incidentally
while investigating a different, now-resolved question. This is the
same epistemic shape iteration 1's own single Case A miss had — and
iteration 1 treated one miss as insufficient grounds to rewrite the
skill, instead gathering one more data point first (this iteration).
Symmetric treatment applies here: **this finding is recorded as a known
limitation, not acted on**, consistent with the task brief's explicit
scope ("Only modify the skill if the frozen results show a repeatable
pattern-recall weakness" — this is not that) and its own caution against
tuning on a single data point ("A single stochastic miss is not enough
to justify rewriting the reasoning procedure").

One additional, non-scoring observation from both A1 and A3's verifiers:
neither run's primary finding wrote out the literal `Authority strength`
field (`REQUIRED`/`RECOMMENDED`/`OPTIONAL`/`INFERRED`) SKILL.md's Finding
contract requires, even though the strength is unambiguous from the
quoted "Don't... Instead" language in both cases. A minor
contract-completeness gap, not a substantive one; not acted on for the
same narrow-scope reason.

## 5. Skill change made

**None.** `skills/cloudscape-native-expression-review/SKILL.md` is
byte-identical to its state at the frozen baseline commit `2745d97`
throughout this iteration.

## 6. Regression set

Not run. The task brief's regression set ("A1, A2, A3, the original
Case A, the real Identities.tsx fixture, the prior equally-valid
negative case, the prior missing-intent negative case") is scoped to
"If the skill changes." Since no change was made, there is nothing to
regress against — iteration 1's original seven-case results
(`RESULTS.md`) stand unmodified and still describe the current,
unchanged skill.

## 7. Precision and anti-fundamentalism — did they change?

**Mostly preserved, with one new, narrow exception.** Every result this
round matches or reinforces iteration 1's findings on the properties the
task brief said not to reopen without new evidence:

- Component/pattern existence was not treated as mandate anywhere in
  this round — A1 correctly suppressed `PropertyFilter` (citing the same
  multi-property threshold as the grading key, almost verbatim) before
  separately, incorrectly, reaching for a lighter-weight
  `CollectionSelectFilter` instead; A2 correctly suppressed Card view,
  Copy-to-clipboard, and a missing-feature candidate, each with
  applicability reasoning tied to this fixture's actual facts, not the
  components' mere existence.
- Missing intent was handled correctly: A3 Finding 3 (whether the
  identifier column should link to a details page) is, per its
  verifier, "textbook correct `intent-dependent` handling, not a guess
  dressed up as caution."
- No task-preservation violations, no general-UX-dressed-as-citation
  findings, and no increased confidence under missing intent were
  observed in any of the nine graded findings/orientation-note claims
  across the three cases.
- The one exception is A1 Finding 2 (§4 above) — a genuine,
  adversarially-confirmed overreach, the first in this skill's
  evaluation history. It is narrow (one finding, one case, orthogonal to
  the case's designed target) but real, and changes the precision claim
  from "0 D/E across iteration 1's seven findings" to "1 D across both
  iterations' twelve findings, 0 E."

## 8. Deterministic tooling

No change. Both `inspect_surface.py` and `resolve_versions.py` ran
unmodified against all three new fixtures before any review, correctly
reporting JSX/import inventories and fully-resolved declared/locked
versions in every case (§1). No concrete failure this round demonstrated
a need for new or changed tooling; pattern applicability judgment
remained entirely agentic throughout, consistent with the task brief's
instruction not to expand tooling absent such evidence.

## 9. Final verdict

**KEEP-WITH-KNOWN-LIMITATION.**

Not PROMOTION-READY outright: while the specific weakness this iteration
was chartered to resolve (pattern-recall on "right components, wrong
pattern") is resolved with strong, adversarially-verified,
two-for-two-plus-one-correct-abstention evidence, this same round
independently surfaced a new, real, verifier-confirmed D-grade overreach
(§4) — the first this skill has produced across either iteration. A
clean, unconditional promotion recommendation would understate that new
evidence. This is not an ITERATE-forcing defect (it is a single
instance, orthogonal to the axis under test, and forcing a reasoning-
procedure change from one data point risks fitting this fixture rather
than a real gap, per the same logic iteration 1 itself used to defer
action on the original Case A miss) — but it is real enough to record as
a named, open limitation rather than silently folding into an
unqualified "good to promote."

Not ITERATE: no repeatable pattern-recall weakness was demonstrated (the
opposite was demonstrated), precision remains high in aggregate (11/12
graded findings across both iterations are A/B, 0/12 are E), and every
other property iteration 1 validated (boundary discipline, missing-
intent handling, anti-cargo-culting, combined component+pattern
reasoning) held up again this round with no counter-evidence.

Not RETIRE: nothing in either iteration's evidence supports discarding
this skill; it remains the only retained active Cloudscape
design-system calibration skill and continues to outperform an unguided
baseline on every axis measured so far.

## 10. Promotion recommendation

**The specific recall concern that was the last open item before
promotion consideration is now resolved and should not block
promotion.** Given the new §4 finding, the recommendation is: this skill
is close to practical FDE-ready but not unconditionally so — a future
round should gather one more data point specifically on whether A1
Finding 2's shape (an unforced secondary finding once a primary
pattern-level finding is already established, especially one hedging its
own confidence) recurs on an independent case, before calling this fully
PROMOTION-READY. This report does not initiate promotion, per the task
brief's explicit instruction.

## 11. Smallest justified next step, if this line of work continues

A single additional pressure case, structurally parallel to A1 but
built specifically to test whether a *found* primary pattern-composition
finding makes a run more likely to also report a low-materiality,
self-hedged secondary finding on the same surface — i.e., isolate
whether A1 Finding 2 was fixture-specific noise (as Case A's original
miss turned out to be) or a repeatable "once I've found one real issue,
I look harder for a second" tendency. Do not edit SKILL.md until that
data point exists; a single D-grade, symmetric to iteration 1's single
miss, is not yet evidence of a pattern.

**Addendum:** this next step was carried out — see
`RESULTS-ITERATION-3.md` for the P1/P2 isolating pressure cases, their
frozen-skill results, and the resulting verdict (**PROMOTION-READY**,
with A1 Finding 2 recorded as a non-recurring, isolated limitation).

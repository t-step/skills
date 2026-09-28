# Grading report: Phase 4 regression subset (N=4 cases, n=1 each, with-skill)

Cases: 105, 108, 109, 112. Selection rationale is in `../RESULTS.md`
("Regression subset selection"). Grading key for each case:
`../frozen/grading/case-1XX.expected.md` (frozen, byte-identical to the
live repo key). No formal per-case R1-R7 rubric exists for these four
cases (only cases 102/106/107/110 have one, in
`../../2026-09-24-reliability-baseline/frozen/grading/RUBRIC.md`); each
run is graded directly against its `.expected.md` narrative, the same
method the original iteration-1 suite (`../../../RESULTS.md`) used for
these same four cases.

## case-105 — ui-only-authorization-no-server-check

**Verdict: PASS, no regression.**

Finding 1 ("Delete-user endpoint enforces authentication, not
authorization"): **Confirmed, HIGH**, unhedged — matches the expected key
exactly ("rated Confirmed/HIGH without hedging (correctly, given no
gateway evidence at all)"). Correctly recognizes that reachability here
*is* directly established (the support engineer's own reproduction), so
the new severity paragraph's floor does not apply — nothing in the new
text discourages HIGH when reachability is actually shown, only when it
is what's unresolved. Finding 2 (`update_user_role`, not independently
reproduced) is scored **Likely, HIGH** — the model reasoned explicitly
about the specific-exploit-not-observed distinction and used the tier
axis (Likely) rather than downgrading severity, exactly the branch the
new paragraph names ("keep HIGH by carrying the finding at Likely
instead"). No over-suppression.

## case-108 — user-to-workload-authority-frozen-at-enqueue

**Verdict: MISS on tier, not attributable to this intervention.**

The single finding is rated **Confirmed, HIGH**. The expected key calls
for **Likely issue, MEDIUM-to-HIGH** — Likely specifically because "the
fixture doesn't show revocation actually occurring in this data," a
Confirmed-vs-Likely **tier** question (governed by the pre-existing
admission-rule paragraph this intervention did not edit), not a
severity(HIGH-vs-MEDIUM) question (what the new paragraph targets — and
the key itself says both MEDIUM and HIGH are acceptable severities here).
The run's own "Unresolved uncertainty" text reasons "it does not change
the fact that the code path as given executes unconditionally" to justify
keeping Confirmed regardless of the unresolved downstream-check
question — structurally the same move case-102's failing runs made, but
applied to the *tier* label, not the *severity* label the new paragraph
governs. This is the identical failure shape the original, pre-admission-
rule case-108 run showed (documented in `../../../RESULTS.md`'s "SKILL.md
correction" section, which the admission-rule paragraph was written to
fix) — recurring on this case under the post-intervention skill, at n=1,
with no A/B pre-intervention run in this same batch to establish whether
the new paragraph made it more or less likely. Reported here as an
existing, not-newly-introduced fragility on this specific case's tier
selection, outside the scope of what this intervention was built to fix,
rather than folded into the R4/severity verdict.

## case-109 — read-write-capability-boundary-metadata-only

**Verdict: PASS, no regression.**

Finding 1 ("No code-level distinction between destructive and
non-destructive tool calls"): **Confirmed, HIGH** — matches the expected
key exactly ("Confirmed issue, HIGH consequence given destructive
Salesforce operations reachable with no distinguishing control").
Reachability is genuinely established here (the approval gate is
confirmed uniform and flag-blind, so a destructive call *is* reachable
through the same unguarded path as a read, not merely structurally
suspicious) — correctly kept at HIGH. Both compounding halves of the
key's expected answer (capability boundary + metadata-only flag) are
present as two further Confirmed findings, connected to the team's actual
either/or question. No over-suppression from the new paragraph.

## case-112 — secret-manager-mechanics-vs-resulting-service-authority

**Verdict: PASS, exact match to the (already-corrected) expected key.**

Single finding: **Confirmed, MEDIUM** — matches the key's corrected
verdict exactly ("Corrected severity: MEDIUM... not HIGH absent evidence
of an actual reachability path"). The run's own "Unresolved uncertainty"
line states the reasoning almost verbatim to the new paragraph: "HIGH
would require treating 'a sensitive write is reachable without
appropriate authorization' as established, and reachability in the face
of any other compromise is a claim this evidence alone can support only
as plausible, not confirmed." This is the strongest single piece of
evidence in this experiment that the intervention generalizes beyond
case-102's network/audience domain to a structurally distinct domain
(secrets management / database privilege scoping) using the same
reasoning shape.

## Aggregate

- **3/4 cases: no regression, correct outcome.** Two (105, 109) confirm
  the new paragraph does not suppress HIGH when reachability is actually
  established (the risk this phase was run to check for). One (112)
  independently confirms the new paragraph's reasoning against a grading
  key that had already been corrected, on this same day, to demand
  exactly that reasoning, in a non-network domain.
- **1/4 cases (108): a miss, on the tier axis the new paragraph does not
  govern**, reproducing a previously-documented failure shape on this
  specific case rather than a new one introduced by this change.
- No case showed a genuinely-Confirmed/HIGH finding wrongly downgraded to
  MEDIUM or Likely by the new paragraph -- the specific damage pattern
  Phase 4 was built to check for did not occur in this subset.

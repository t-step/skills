# build-vs-adopt-audit — iteration 1 benchmark results

**Run date:** 2026-08-18
**Model under test:** claude-sonnet-5, fresh general-purpose subagent per run, default settings, no tools beyond Read (restricted by prompt to the case's own fixture files; agents were instructed not to invoke the Skill tool)
**Harness:** one subagent per run via the Agent tool. With-skill runs were given both `skills/build-vs-adopt/SKILL.md` and `skills/build-vs-adopt-audit/SKILL.md` to read (matching the audit skill's own REQUIRED BACKGROUND declaration), then the case's `prompt.md` + `repo_snapshot.md`. Baseline runs got the same fixture with no skill and an explicit instruction not to consult one. Graded by the orchestrating session against `evals.json`'s expectations.
**Sample size:** n=1 per case per configuration (6 total iteration-1 runs across 3 cases; plus 2 iteration-2 runs covering the new case 004 — see "Iteration 2" below).

## What this proves / what this does not prove

**Proves:** on these 3 fixtures, the with-skill condition correctly discriminated commodity-and-undocumented code (flag it) from domain-specific-or-documented code (don't flag it) in all 3 cases, including the combined case (003) that required getting both calls right in a single pass. The baseline condition also discriminated correctly on *which* code to flag or not flag in all 3 cases — that specific judgment call is not where the skill adds measurable value here. Where the baseline diverged from the skill's contract is narrower and more specific: in both cases where a real finding existed (001, 003), the baseline's "recommendation" for that finding included a concrete prescribed fix ("replace with `tenacity`," "replacing it with a maintained TTL-cache library and removing the class") alongside "make this a decision," rather than the skill's stricter contract of recommending only that the build-vs-adopt evaluation be re-run. That's a small but real, repeatable difference in what the audit's output commits to.

**Does not prove:** that this recommendation-shape distinction matters in practice as much as the correctness of the underlying finding does — a reader could reasonably view the baseline's extra concrete suggestion as more, not less, useful. The skill's contract (never prescribe a replacement) is a deliberate design choice explained in its own SKILL.md (the ownership decision needs a live decision-maker, and prescribing an outcome from an audit pass risks exactly the reflexive "a library exists so replace it" bias build-vs-adopt itself refuses to have) — this evidence shows the baseline doesn't follow that specific discipline on its own, not that following it produces a better outcome for the reader. It also does not test the audit skill on a larger or more varied codebase, on a case with more than 2-3 files in scope, or with `git log` history that's actually informative rather than a single uninformative commit message (which is what all 3 fixtures used).

## Results (cases 001–003; case 004 added in Iteration 2, below)

1 run per case per configuration.

| Case | Finding correctness (with skill) | Finding correctness (baseline) | Recommendation-shape discipline (with skill) | Recommendation-shape discipline (baseline) |
|---|---|---|---|---|
| 001 (clear-commodity-finding) | PASS — flagged | PASS — flagged | PASS — "re-run build-vs-adopt" only | FAIL — offered "replace with tenacity" as one of two named paths |
| 002 (justified-custom-not-flagged) | PASS — not flagged, ADR cited | PASS — not flagged, ADR cited | PASS — no replacement suggested | PASS — no replacement suggested (see note) |
| 003 (mixed-repo-discrimination) | PASS — both halves correct | PASS — both halves correct | PASS — "re-run build-vs-adopt" only | FAIL — offered "replacing it with a maintained TTL-cache library ... " as one of two options |
| **Total** | **3/3** | **3/3** | **3/3** | **1/3** |

**Case 001, with skill:** flagged `ApiClient.get()`'s hand-rolled retry loop, explicitly listed the five evidence sources checked (comment, ADR/design-doc directory, commit history, project memory, README) and that all five came back empty, and closed with "Recommendation: Re-run build-vs-adopt for this capability" — no specific replacement named as the conclusion.

**Case 001, baseline:** found the same evidence gap and the same finding, with equally thorough reasoning about *why* it's commodity-shaped (correctly noted the retry-on-4xx bug and lack of jitter as evidence the custom version has already accumulated the kind of edge case a library would have handled). But its "Recommendation" section presented two "acceptable paths" — "Adopt: Replace the hand-rolled loop with `tenacity` ... or `requests`' built-in `urllib3.util.Retry`" and "Ratify build: ... record that decision explicitly" — the first of which is exactly the prescribed-replacement conclusion the skill's contract rules out for an audit pass.

**Case 002, both configurations:** neither flagged `SpendGovernor`, both correctly cited the existing ADR (`docs/decisions/0007-spend-governor.md`) and the domain-specific contract-anniversary/override behavior as the reason. The baseline went further than the fixture's scope and raised a genuinely separate, real concern (the in-memory counter's lack of durability/atomicity across restarts or replicas) — a legitimate observation, but arguably outside a build-vs-adopt audit's stated job (it's a different kind of code-review finding, not an ownership-decision gap). It didn't violate the pass criteria for this case, so it's recorded as a pass with a note rather than a fail.

**Case 003, with skill:** flagged `LocalCache` (undocumented, generic LRU/TTL shape, generic usage) with the standard "re-run build-vs-adopt" recommendation, and correctly excluded `apply_tier_pricing` citing its inline rationale comment and coupling to `Contract.tiers` — both halves correct in the same pass.

**Case 003, baseline:** also got both halves right — flagged `LocalCache`, excluded `apply_tier_pricing` for the same reasons — but again closed the `LocalCache` finding with a concrete choice framed as the audit's own conclusion: "Recommend either (a) retroactively documenting why an in-house cache was chosen ... or (b) replacing it with a maintained TTL-cache library and removing the class." Option (b) is a prescribed replacement, not a call to re-run the evaluation.

## What this suggests

The specific thing this skill's SKILL.md asks for — findings that recommend *re-evaluating* an ownership decision, never findings that *conclude* a replacement — is not something the baseline model does on its own even when its underlying analysis is otherwise excellent. In both cases with a real finding, the baseline volunteered a specific library as a live option in the same breath as recommending a decision be made, which blurs exactly the line the skill's SKILL.md draws explicitly ("the recommendation line is always the same shape: re-evaluate, never 'replace with `<library>`'"). This is a narrow, repeatable (2/2 opportunities) finding, not a broad claim about audit quality — the underlying technical judgment (what to flag, what not to flag, why) was equally strong in both conditions across all 3 cases.

## Limitations

- **n=1 per case**, 3 cases total — the smallest suite in this repo's skill family. No repeat-run variance data exists.
- **All 3 fixtures used artificially clean evidence signals** (either a completely empty decision trail or an unambiguous, on-point ADR) — real repositories are messier, with partial rationale scattered across comments, old PR descriptions, and Slack threads a static fixture can't represent. This suite doesn't test the audit's behavior under genuinely ambiguous evidence (e.g., a comment that's plausible but doesn't fully explain the choice).
- **Fixtures were small** (2-3 files in scope). The suite doesn't test whether the audit's discrimination holds up when scanning a directory with dozens of files, most of which are irrelevant noise.
- **Recommendation-shape grading required reading each response's prose carefully** for whether a named library appeared as "context for why this looks like commodity functionality" (compliant) versus as part of the stated "Recommendation" (non-compliant) — a real distinction, but one that depends on where in the response a sentence appears, which is a softer signal than a hard pass/fail check would be.

## Iteration 2 — evidence-tightening fix (2026-08-18)

A PR review of iteration 1 found SKILL.md's decision-evidence bar too
permissive: "using our own implementation here because X" was treated as
sufficient evidence a decision was made, even when X states a preference
("simpler," "didn't want another dependency") rather than a considered
tradeoff — exactly the kind of comment a reflexively-avoidant author would
leave. SKILL.md was updated so that clearing a candidate now requires
evidence the tradeoff was actually weighed (a named constraint — license,
technical mismatch, a specific unmet requirement), not just that a choice
was stated. A preference-only comment is now explicit **weak evidence**: it
still produces a finding, but the finding must report what was actually
found (a preference-only comment, not "none found") rather than pretend no
evidence exists, and must not use the weak evidence as license to assert
the custom code is wrong — the recommendation stays the same
re-run-the-evaluation call either way.

New case `evals/build-vs-adopt-audit/cases/case-004/`
("weak-preference-evidence") exercises this directly: a hand-rolled retry
loop (same commodity pattern as case 001) with an inline comment — "Custom
retry loop here -- simpler than adding a dependency just for this one call
site" — that states a preference, not a considered tradeoff. Distinct from
case 001 (zero evidence) and case 002 (a substantive ADR that clears the
candidate), this isolates the specific new middle case: evidence exists,
but doesn't clear the bar.

| Case | With skill | Baseline |
|---|---|---|
| 004 (weak-preference-evidence) | PASS — flagged, evidence characterized correctly, no prescribed replacement | PARTIAL — flagged, but for a different reason than the semantic distinction being tested, and the recommendation prescribes a replacement |

**Case 004, with skill:** flagged the finding, and characterized the evidence with the precise distinction the tightened rule asks for: "a preference-only comment... states an outcome/preference ('simpler'), not a considered tradeoff (no constraint named — no license conflict, no missing feature in `tenacity`/`backoff`...)." Explicitly labeled it "weak evidence" in the same terms as SKILL.md, and closed with "Recommendation: Re-run build-vs-adopt for this capability" — no prescribed replacement.

**Case 004, baseline:** also flagged the finding (did not clear the candidate) — but for a subtly different reason than the one being tested. Baseline's own words: the comment "shows the build-vs-adopt tradeoff was actually considered by whoever wrote it. That's a good sign of awareness, but the decision itself was never externalized" — i.e. baseline concluded the *substance* of the comment was fine and only objected that it wasn't durably recorded outside the code. That's the opposite framing from the tightened rule, which says this exact kind of comment (preference-only, no named constraint) does *not* show a considered tradeoff regardless of where it's recorded. The two conclusions happen to agree here (both flag it), but for reasons that would diverge on a different fixture (e.g. the same preference-only comment inside a design doc — baseline's "externalization" framing would clear it; the tightened substance-based rule would not). Baseline's recommendation also repeats the pattern found in cases 001 and 003: it names `HTTPAdapter`/`Retry` and `tenacity` as concrete adopt options in the same breath as the decision-record ask, rather than sticking to "re-run the evaluation." Graded as PARTIAL: right top-line action (flag), wrong reasoning on the specific evidence-quality distinction, and the same recommendation-shape miss as before.

### What this adds to the iteration-1 finding

The evidence-tightening fix is exercised by exactly the case it was designed for, and the with-skill condition applies the tightened rule correctly and in language that traces directly to SKILL.md's new text. The baseline result is a useful, honest data point rather than a clean uplift story: baseline's *instinct* not to fully trust an informal comment survived even before the fix (it still flagged the finding), but its *reasoning* for why doesn't match the specific substance-vs-preference distinction this fix asks for, and its recommendation-shape miss — now confirmed across 3 of 3 opportunities (cases 001, 003, 004) — remains the most repeatable, specific gap this skill closes.

## Limitations (Iteration 2 addendum)

- **n=1 for case 004**, same caveat as the rest of this suite.
- **Case 004's baseline grading required judging the substance of its reasoning, not just its bottom-line action** — a softer call than a pure pass/fail; the "PARTIAL" verdict and its rationale are recorded above so a reader can disagree with where the line was drawn.

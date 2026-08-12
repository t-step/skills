# comment-cleanup — evaluation results

## What this proves / what this does not prove

**Proves:** the skill's judgment rules (the taxonomy, evidence-tier
discipline, and refusal list) held up on 8/9 hand-picked, high-risk
pressure cases in a single run each, under the *previous* one-pass
edit-and-report contract, and the one real gap found (case-113) was fixed
and reverified. That is evidence the underlying judgment is sound on the
scenarios sampled.

**Does not prove:** that the skill performs correctly under its *current*
contract. This file documents a skill that has since been restructured
twice — once (iteration 1, below) to fix a judgment gap, and again
(report-first default, "better home" recommendations) to change what a
correct *response* looks like for every single case, including the ones
iteration 1 already validated. No case in this suite has been run against
the current SKILL.md and the current grading keys. See "Report-first
restructure: what this means for the existing runs" below before treating
any pass/fail number in this file as current.

This is a 9-of-22-case, single-run, no-repeat-variance sample overall —
well short of the bar for "proves"/"disproves" language on its own terms
even before accounting for the contract change. Treat every claim in this
file as suggestive and underpowered until a full-suite run under the
current contract exists.

## Suite

- **Regression suite** (`evals.json`, `cases/case-001..006`): ordinary,
  non-adversarial mixed-comment files across Python, TypeScript, and Go,
  covering the 12 taxonomy categories in the skill's design brief. 6 cases.
- **Pressure suite** (`pressure-tests/pressure_evals.json`,
  `cases/case-101..116`): one fixture per adversarial failure mode from the
  design brief (101–114), plus two fixtures added alongside the
  report-first restructure (115, 116; see below). 16 cases. See
  `pressure-tests/README.md` for the full table and grading policy.

22 cases total (6 + 16), computed by listing `evals/comment-cleanup/cases/
case-*` directories at write-up time, not hand-typed from memory.

Both suites are structurally verified by `scripts/check.sh` (frontmatter
lint, eval-isolation/answer-leakage guard, cross-skill deps) — clean as of
this writing (`check-eval-isolation.py` reports 136 case dirs across 8
skills in this repo, no leakage of scenario labels or expected dispositions
into agent-visible fixture paths or content).

## Report-first restructure: what this means for the existing runs

The skill originally classified and edited comments in one pass, and the
grading keys and `evals.json`/`pressure_evals.json` manifests graded the
resulting diff. It has since been restructured (see
`skills/comment-cleanup/SKILL.md`, "Report first, apply only on request")
so that the default invocation produces a classification report only —
zero file edits — with applying the report's high-confidence dispositions
split out as a separate, explicit second step. Preserved comments now also
require a recommended "better home" for their information (a test,
docstring, decision log, or issue reference — or an explicit "the comment
itself is the right home"), with a matching refusal-list entry against
actually performing that relocation.

Every grading key in `evals/comment-cleanup/grading/`, and every entry in
`evals.json` and `pressure_evals.json`, has been updated to grade against
this new contract: a correct response is now a report with the right
proposed dispositions and (for preserved items) a placement recommendation
— not an edited file. **The substantive expected disposition for every
pre-existing case (001–006, 101–114) is unchanged** — case-102's invariant
is still preserved, case-105's TODO is still removed, and so on — only the
*form* the correct response takes has changed.

This means the iteration-1 run below, and its 8/9 pass tally, are evidence
about **judgment quality** (did the skill correctly classify these
comments?) under the *old* contract, not evidence about the *current*
contract (does the skill correctly withhold edits by default, and does it
recommend placements?). Nothing in iteration 1 exercised report-first
behavior or placement recommendations, because neither existed yet at
survey time. The iteration-1 history below is preserved as-is rather than
rewritten, because it remains true and useful for what it actually showed;
its scope is reframed here rather than its content changed.

## Iteration 1: representative validation sample (previous contract)

Per the user's scope decision for this first pass, the full case set that
existed at the time was built but only a representative sample was run: 9
cases chosen for maximum coverage of *harmful-over-deletion* risk
specifically — case-001 (ordinary baseline control), case-101
(delete-control, checks the skill isn't too conservative to ever delete),
and 7 of the trickiest pressure cases (102 race-condition invariant, 104
workaround-still-required, 106 old-but-valid TODO, 108 lint/type
directive, 110 history-blocks-restore, 113/114 the misleading-comment
pair). Each ran with-skill and baseline (no skill) against isolated copies
of the fixture under `evals/comment-cleanup-workspace/iteration-1/` so the
two configs never edited the same files. Full run matrix:
`runs/2026-08-11-iteration-1-runs.md`. **All of this ran under the
one-pass edit-and-report contract** — with-skill responses in this section
edited files directly, which the contract at the time called for.

### What held up

Seven of nine cases were clean, exact-match passes for the with-skill
configuration on the first run: case-001, case-101, case-102, case-106,
case-108, case-110, case-114. In particular:

- **case-102** (the race-condition invariant that "looks redundant"): the
  with-skill run correctly traced the concurrent call site in a second
  file (`worker_pool.py`) before concluding the comment was load-bearing,
  rather than pattern-matching on the comment's plain wording.
- **case-108 and case-110**: with-skill made *zero* edits in both cases —
  full verbatim preservation of a tooling directive and an
  incident-preventing comment, respectively, including refusing case-110's
  explicit invitation to also evaluate removing the `LRUCache` class. The
  **baseline** (no skill) got the substance right in both cases but made
  an unrequested wording trim in both — exactly the "rewrite a preserved
  comment to sound better" failure mode this skill's refusal list exists
  to prevent. This is the clearest demonstrated uplift in the sample: not
  "baseline deletes things it shouldn't," but "baseline quietly edits
  things it was never asked to touch, and the skill's explicit scope
  boundary stops that."
- **case-106**: both configs correctly resisted "it's old, just delete it"
  pressure and corroborated the TODO's validity via a second file.

### case-104: a calibration note, not a failure

Both with-skill and baseline made the same judgment call: neither deleted
the retry logic or comment, but both corrected the misleading "TEMPORARY —
remove this once fixed" framing (which the evidence does contradict) while
preserving the underlying vendor-side rationale. The original grading key
required verbatim preservation; on reflection this was too strict — the
"TEMPORARY/imminent removal" framing is itself a claim the fixture's own
evidence contradicts, so correcting it is consistent with this skill's
stale-comment rule elsewhere in the suite. **Fixed**: loosened
`grading/case-104.expected.md` and the pressure manifest to accept either
verbatim preservation or a correction that keeps the substance and the
retry code intact (both options now further updated for the report-first
contract — see above). No SKILL.md change needed here — this was a
fixture/key calibration issue, not a skill gap.

### case-113: a real gap, found and fixed

The with-skill run on case-113 (a TODO referencing a nonexistent variable,
an unreachable JIRA ticket, and an undefined "edge case Z") **corrected**
the comment — fixing the dangling `old_price` reference to
`price_after_discount` — instead of **deleting** it as the fixture
intended. The corrected comment still asserted an unverifiable claim (a
"tiered discount structure" nothing in the repo shows was ever built),
just with its surface syntax patched. The baseline run, by contrast,
deleted the whole comment and matched the grading key.

This is a genuine SKILL.md gap: the original "Stale" classification only
addressed the binary case (fully establishable → correct; fully
unestablishable → delete), not the case where *part* of a comment is
fixable (a dangling name) while its *substance* is not. **Fix applied**:
added a paragraph to the "Stale" bullet in `skills/comment-cleanup/SKILL.md`
naming this exact pattern and requiring the comment's core claim, not just
its easiest-to-fix detail, to be establishable before correcting rather
than deleting.

**Verified**: reran case-113 with-skill against the revised SKILL.md on a
fresh copy of the fixture. The rerun deleted the comment and explicitly
reasoned through the "fixable detail next to an unverifiable claim"
pattern by name — closely echoing the new SKILL.md wording — while also
volunteering a note back to the user that the JIRA ticket's status
couldn't be confirmed, rather than silently discarding that thread. Also
reran case-114 (the paired "misleading but fully correctable" case)
against the revised skill as a regression check: it still correctly
corrected rather than deleted, confirming the fix didn't overcorrect
toward deletion.

### Revised tally (post-fix, previous contract)

With-skill, 9-case sample: 8/9 clean, 1 case (104) resolved by loosening an
overly strict grading key rather than a skill change. The one real skill
gap found (113) was fixed and reverified; its paired regression case (114)
was reverified clean. **This tally describes judgment quality under the
one-pass contract that no longer exists** — see "Report-first restructure"
above.

## New fixtures for the report-first restructure (authored, unrun)

Two cases were added specifically to probe the two behaviors the
report-first restructure introduced, and are **authored but not yet run**
against any configuration:

- **case-115** (`report-first-under-pressure`): the dispositions are
  deliberately easy (two textbook comment restatements, one clear
  invariant); the thing being probed is whether "just clean these up — no
  need to walk me through it" collapses the report-only default into an
  unrequested edit. Per its grading key, any file edit is a hard failure
  regardless of whether the edit's substance would otherwise be correct.
- **case-116** (`placement-recommendation-required`): an ordering
  invariant (plugin registration must happen before a one-time
  initialization snapshot) corroborated by a second file
  (`tests/test_plugins.py`, which demonstrates the silent-drop behavior).
  The thing being probed is whether the report recommends a *concrete*
  better home (a runtime assertion/guard) rather than a bare "preserved"
  or a recommendation that only points at the existing test without
  proposing anything stronger — and, separately, that no response actually
  performs the relocation itself.

Neither case has a with-skill or baseline run recorded. They exist to make
a full-suite run meaningful once one happens; until then they're
inventory, not evidence.

## Outstanding validation

The single most important gap this file should not obscure: **no case in
this 22-case suite has been run against the current SKILL.md (report-first
default, placement recommendations) and the current grading keys.** The
iteration-1 sample above validates judgment quality under a contract that
no longer exists; case-115 and case-116 are authored but unrun. A run
across all 22 cases (both suites), ideally with the same with/without-skill
structure and repeat-run variance iteration-1 used for its 9, is the
concrete next step before this skill can be considered validated under its
current contract — not just "the report-first mechanics work," but
"the judgment findings from iteration 1 still hold once the response shape
around them has changed."

## Limitations

- Iteration 1 is a 9-of-22-case representative sample under a superseded
  contract, not a full-suite run, and not a formal with/without-skill
  benchmark in the depth of slice-review/slice-retro's iteration-1 runs
  (no repeated-run variance data, no token/timing benchmark).
- Several "baseline" runs in the iteration-1 sample were already quite
  strong (matching with-skill on substance in 7/9 cases) — consistent with
  this repo's established finding (repo-orientation, slice-plan) that
  Sonnet 5's unguided baseline is often already good at avoiding the
  *obvious* failure (wrongful deletion). Where the skill demonstrably
  added value in that sample was narrower and more specific: resisting
  *unrequested edits* to comments that should have been left alone
  (case-108, case-110), and correctly discriminating a "fixable detail vs.
  unverifiable substance" case after the SKILL.md fix (case-113). Whether
  this uplift pattern still holds once "unrequested edits" also covers
  "any edit at all without apply intent" (the report-first contract) is
  exactly what an updated run would need to check.
- The `comment-cleanup-workspace/` directory used for the iteration-1
  validation pass is scratch, not committed, matching this repo's
  convention for other skills' iteration workspaces.

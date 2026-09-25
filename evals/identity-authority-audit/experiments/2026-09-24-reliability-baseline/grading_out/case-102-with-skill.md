# Grading report: case-102 (raw-forwarding-chain-hop-discrimination), with-skill condition

Graded independently against `frozen/grading/RUBRIC.md`'s case-102 section and
`frozen/grading/case-102.expected.md`, run-by-run, before any cross-run
comparison. 7 Required items (R1-R7), 3 Forbidden items (F1-F3) per run.

## 1. Per-run table

| Run | Required met/total | Pass/Fail | Forbidden fired | Unsupported findings | Confidence-tier violations | Severity of main finding(s) | Mode drift | Bonus findings | T1 (gateway enforcement named unresolved?) | T2 (consequence tier, verbatim) |
|---|---|---|---|---|---|---|---|---|---|---|
| run-01 | 7/7 | PASS | none | 0 | none (borderline, see 2) | Confirmed, HIGH (combined API B+MCP finding) | No | 1: read+write scope never narrowed (Likely, MEDIUM) | Named, but framed as largely "foreclosed" with a conditional walk-back | "Confirmed, HIGH" (whole finding, incl. consequence clause), with a conditional re-assessment clause appended |
| run-02 | 7/7 | PASS | none | 0 | none | Confirmed, HIGH (combined API B+MCP finding) | No | 1: read+write scope never narrowed (Likely, MEDIUM) | Named explicitly ("not evidence that it doesn't exist") | "Confirmed, HIGH" applied to "accepted, unverified" (code fact); consequence framed as "reduce, but not eliminate, the exposure" |
| run-03 | 7/7 | PASS (borderline R5) | none | 0 | none | Confirmed, HIGH x2 (API B and MCP as separate blocks) | No | 2: scope never narrowed (Confirmed, MEDIUM); shared signing secret (Ambiguity requiring verification, no severity tier given) | Named in both findings individually | "Confirmed, HIGH" x2, each with its own hedge |
| run-04 | 7/7 | PASS | none | 0 | none | Confirmed (structural fact) / Likely (consequence), HIGH x2 | No | 2: scope never narrowed (Likely, MEDIUM); shared signing key (Confirmed structural fact, boundary-adjacent, HIGH) | Named explicitly in both findings | "Confirmed (structural fact) / Likely (consequence), HIGH" — explicit two-tier split, both findings |
| run-05 | 7/7 | PASS | none | 0 | none | Confirmed, HIGH (combined API B+MCP finding) | No | 1: write-capable scope unchecked (Ambiguity requiring verification) | Named explicitly, with an explicit fact/consequence split inside the hedge | "the structural fact... is confirmed; what a network-layer control elsewhere might additionally do about it is not" |
| run-06 | 7/7 | PASS | none | 1 (see 2) | none (borderline, see 2) | Confirmed, HIGH (combined API B+MCP finding) | No | 1: scope propagates unchecked into dispatch (Confirmed, HIGH — arguably over-severe for an unrealized risk) | Named explicitly | "Confirmed, HIGH", with an explicit claim that acceptance "isn't a hypothetical" based on the engineer's reported observation |
| run-07 | 6/7 (R4 not met) | **FAIL** | F1, F2 | 1 | **Yes** | Confirmed, HIGH (combined API B+MCP finding, no hedge) | No | 1: scope/dispatch gap (Confirmed, MEDIUM) | **Not named — explicitly denied** ("Unresolved uncertainty: none") | "Confirmed, HIGH", with the report stating up front it will not hedge for a possible external gateway |
| run-08 | 6/7 (R5 not met) | **FAIL** | none | 0 | none | Confirmed, MEDIUM x2 (API B, MCP as explicitly *independent* findings) + Likely, HIGH (forward-looking new-tool finding) | No | 2: new-tool-inherits-authority (Likely, HIGH); scope forwarded unnarrowed (Confirmed, MEDIUM) | Named in both findings | "Confirmed, MEDIUM" x2, each hedged, but MCP finding explicitly labeled "independent of what arrives from API B" |
| run-09 | 7/7 | PASS | none | 0 | none | Confirmed, MEDIUM x2 (API B, MCP — explicitly connected as "the second hop... where [the same check] is absent") | No | 1: scope never checked (Likely, MEDIUM) | Named in both findings | "Confirmed, MEDIUM" x2, connected via continuity language, each hedged |
| run-10 | 7/7 | PASS | none | 0 | none | Confirmed, HIGH (combined API B+MCP finding) | No | 1: read+write scope unchecked (Confirmed, MEDIUM) | Named explicitly, with an explicit statement that real-world exposure may be "narrower... than the application code alone suggests" | "Confirmed, HIGH" for the code-acceptance fact; production exposure explicitly left open |

Pass: 8/10. Fail: run-07, run-08.

## 2. Per-run notes on non-obvious calls

**run-01** — Scored PASS but the closest borderline call in the batch. The
single combined finding is tagged "Confirmed, HIGH" and its "Why it
matters" states as fact that "any caller able to obtain an `aud="api-a"`
token... can present it directly to API B or the MCP server and be
accepted, bypassing whatever logic API A's own handler would otherwise
apply" (line 54) — worded close to the "therefore usable/exploitable in
production" claim R4 asks to be capped. It survives as met only because
the "Unresolved uncertainty" paragraph explicitly walks this back
conditionally: "If that framing doesn't hold for the real deployment...
this finding's severity would need to be reassessed" (lines 66-71). That
is a real hedge, but a weaker one than most other passing runs (it is
appended after an unqualified claim rather than integrated into it), so
it is recorded as a borderline pass rather than a clean one.

**run-03** — Passed R5, but only just. Unlike run-01/02/05/06/10, this run
gives API B and the MCP server two fully separate "Confirmed, HIGH"
finding blocks rather than one combined finding. It survives R5 because
each block's title explicitly ties back to the other ("the same
mismatched token reaches tool dispatch," line 37), which is the kind of
continuity language the rubric's "same sustained issue" language calls
for — contrast with run-08 below, which does the opposite. The double-HIGH
formatting is noted as a stylistic concern (risk of the reader perceiving
two independently-severe problems rather than one problem manifesting
twice) but not treated as a rubric violation given the explicit
connecting language.

**run-04** — The cleanest example in the batch of the exact
tier-discrimination the rubric wants: both audience findings are
literally tagged "Confirmed (structural fact) / Likely (consequence),
HIGH" (lines 24, 31), and the second finding's title is "Same
unenforced-audience pattern repeats at the MCP server" — unambiguous
continuity language satisfying R5 despite the two-block format.

**run-06** — The main audience finding states "This is exactly the
scenario the platform engineer described observing live in production...
so this isn't a hypothetical -- the evidence and the reported behavior
agree that requests reach this code and are accepted" (lines 20-21). This
is judged as legitimate (it grounds the *acceptance* fact in the task's
own stated observation, not in unearned inference about exploitability),
so R4 is scored met. Separately, the bonus scope finding is tagged
"Confirmed, HIGH" (line 26) for a risk that is entirely forward-looking
(no write tool exists in evidence) — every other run that raises the same
observation tags it Likely/Ambiguity or Confirmed-MEDIUM at most. This is
recorded as one unsupported/over-severe finding; it does not affect
pass/fail since it falls outside the R1-R7 list, but it is the one
confidence-tier softness worth flagging for this run.

**run-07** — Clear fail. The system-shape section states up front: "no
gateway, service-mesh, or infrastructure configuration exists anywhere in
it... so findings below are not hedged as 'maybe a gateway handles this
elsewhere'" (lines 18-19), and the main finding's uncertainty section
reads in full: "Unresolved uncertainty: none — the task context and
`api_b.py`'s docstring both state this is the complete evidence for the
system, with no gateway/mesh/infrastructure config anywhere in it, so
there is no unseen enforcement layer to point to here" (line 37). This is
a direct instance of F1 (treating repo-local absence of gateway evidence
as proof no such gateway exists) and F2 (Confirmed at full severity with
no acknowledgment of what happens before the request reaches this code —
here the run explicitly declares zero uncertainty rather than merely
omitting it). R4 is therefore not met and the run fails.

**run-08** — Clear fail on R5, not on tier discipline (its hedges are
otherwise fine). The MCP-server finding states: "this is a structural gap
in the MCP server's own application-layer enforcement, **independent of
what arrives from API B**. Even setting aside where the token came from,
nothing at this hop distinguishes..." (lines 68-69). This explicitly
frames hop 3's issue as a freestanding, newly-discovered problem rather
than "the same sustained audience-persistence issue continuing one hop
further," which is exactly what R5 prohibits. Contrast with run-09's
"this is the second hop in the chain where the audience check that
exists at API A is absent" (line 66), which uses connecting language and
was scored as meeting R5.

**run-09, run-10** — Both pass cleanly; no non-obvious calls beyond what's
in the table. run-10's hedge is notably explicit about the fact/consequence
split without needing a compound tier label: "If such a layer independently
enforces audience before a request reaches this application code, the
real-world exposure is narrower than the application code alone suggests
— but nothing in the evidence confirms or rules that out for either
service" (lines 59-63).

**run-02, run-05** — Both pass cleanly and are among the strongest in the
batch on R4: run-02's hedge states plainly "An implementation not visible
in this repository is not evidence that it doesn't exist" (line 41);
run-05's hedge draws the fact/consequence line explicitly within a single
sentence: "the structural fact (application code accepts the mismatched
audience) is confirmed; what a network-layer control elsewhere might
additionally do about it is not" (lines 65-68).

## 3. Group aggregate (case-102, with-skill, n=10)

- **Pass rate:** 8/10 (80%). Fails: run-07 (R4 not met — F1/F2 fired),
  run-08 (R5 not met — MCP finding framed as independent of API B's).
- **Forbidden-finding rate:** 1/10 runs had ≥1 forbidden item fire (10%)
  — run-07 (F1 and F2, both from the same "Unresolved uncertainty: none"
  passage).
- **Unsupported-finding rate:** 2/10 runs (20%) — run-06 (bonus scope
  finding tagged Confirmed/HIGH for an unrealized, forward-looking risk)
  and run-07 (the denied-uncertainty audience claim).
- **Confidence-tier violation rate:** 1/10 (10%) — run-07 only. run-01 was
  a borderline case (weaker, appended hedge) but retains a genuine
  conditional walk-back and was not counted as a violation.
- **Mode-drift rate:** 0/10 (0%). No run proposed unsolicited
  redesign/remediation beyond the skill's own "smallest useful next
  check or change" field, assigned a numeric maturity score, or drifted
  into out-of-scope domains (crypto/TLS, password policy, general
  appsec/OWASP, pentesting) unprompted by the evidence — several runs
  raise the shared-signing-key observation but explicitly scope it as
  "out of this skill's remit" and tie it back to the audience/trust-
  boundary question rather than treating it as a freestanding crypto
  finding.
- **Severity distribution across all findings, all 10 runs** (27 findings
  total, tallied from each run's `###`-level Findings sections):
  - Confirmed, HIGH: 10 (run-01, run-02, run-03 ×2, run-05, run-06 ×2,
    run-07, run-10, run-04's signing-key bonus finding)
  - Confirmed (structural fact) / Likely (consequence), HIGH: 2 (run-04,
    both audience findings)
  - Confirmed, MEDIUM: 8 (run-03, run-07, run-08 ×3, run-09 ×2, run-10)
  - Likely, MEDIUM: 4 (run-01, run-02, run-04, run-09)
  - Likely, HIGH: 1 (run-08's forward-looking new-tool finding)
  - Ambiguity requiring verification (no HIGH/MEDIUM/LOW tier attached):
    2 (run-03's signing-key finding, run-05's scope finding)

## What this grading does and does not establish

This is a single-case, 10-run grading pass under one frozen rubric. An 80%
pass rate with one clean forbidden-trigger failure (run-07) and one
clean required-item failure (run-08) is evidence about this specific
skill/case/condition combination only — it does not generalize to other
cases, conditions, or skill versions without further runs. Several pass
calls (run-01, run-03) were genuinely borderline and are flagged as such
above rather than folded silently into a clean pass rate.

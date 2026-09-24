# Grading report — case-106 (legitimate-spa-pkce-no-bff-needed), with-skill condition

Graded against `frozen/grading/RUBRIC.md`'s case-106 section and
`frozen/grading/case-106.expected.md`. Each of the 10 runs was read and
scored independently before any cross-run comparison; aggregates below were
computed only after all 10 were individually scored, per the Grading
protocol.

Required items (case-106):
- R1. Does not recommend/demand a BFF.
- R2. Does not blanket-claim browser-held bearer tokens are inherently unsafe.
- R3. Positively recognizes the SPA+PKCE architecture as coherent, naming at
  least some of: audience narrowing, scope narrowing, in-memory-only token
  storage, destination-side resource-ownership check.
- R4. Treats the 8-hour-lifetime/no-refresh-rotation detail at most as LOW /
  omitted — not Confirmed/Likely MEDIUM or HIGH.

Forbidden items:
- F1. Explicit BFF recommendation/demand.
- F2. Blanket "browser tokens are inherently unsafe" claim.
- F3. Elevating the 8-hour lifetime to Confirmed/Likely MEDIUM/HIGH with no
  cited exposure evidence.

T1 (tracked): count of the four R3 specifics explicitly named (0–4).

## 1. Per-run table

| Run | Required met/total | Pass/Fail | Forbidden fired | Unsupported findings | Confidence-tier violations | Severity of main finding(s) | Mode drift | Bonus findings | T1 |
|---|---|---|---|---|---|---|---|---|---|
| 01 | 4/4 | PASS | none | 0 | none | 8h lifetime: Deliberate tradeoff; PATCH-body: Ambiguity; scope-bundling: Likely, LOW | No | 2 — PATCH-body no-field-allowlist (Ambiguity); every token bundles read+write:own scopes (Likely, LOW) | 3 (audience, in-memory storage, destination ownership check named plainly; scope named but framed as a gap, not a positive) |
| 02 | 4/4 | PASS | none | 0 | none | 8h lifetime: Deliberate tradeoff; XSS/BFF question: Ambiguity; PATCH sensitivity: Ambiguity | Yes (borderline) — makes an out-of-scope XSS/CSP audit "the crux" of whether a BFF is needed | 1 — PATCH-body sensitivity (Ambiguity); the XSS/BFF item is counted under mode drift, not as a clean bonus | 4 |
| 03 | 4/4 | PASS | none | 0 | none | 8h lifetime: Deliberate tradeoff; PATCH assurance: Ambiguity | No | 1 — PATCH write-assurance/step-up ambiguity | 4 |
| 04 | 4/4 | PASS | none | 0 | none | 8h lifetime: Deliberate tradeoff; list-endpoint scoping: Ambiguity; PATCH sensitivity: Ambiguity | No | 2 — list-endpoint db-scoping ambiguity; PATCH sensitivity ambiguity | 4 |
| 05 | 4/4 | PASS | none | 0 | none | 8h lifetime: Deliberate tradeoff; PATCH sensitivity: Ambiguity | No | 1 — PATCH sensitivity ambiguity | 4 |
| 06 | 4/4 | PASS | none | 0 | none | 8h lifetime: Deliberate tradeoff (only finding) | No | 0 | 4 |
| 07 | 4/4 | PASS | none | 0 | none | 8h lifetime: Deliberate tradeoff; PATCH-body allowlist: Ambiguity | No | 1 — PATCH-body no-field-allowlist ambiguity | 4 |
| 08 | 4/4 | PASS | none | 0 | none | 8h lifetime: Deliberate tradeoff (only finding) | No | 0 | 4 |
| 09 | 4/4 | PASS | none | 0 | none | 8h lifetime: Deliberate tradeoff; PATCH-body allowlist: Ambiguity | No | 1 — PATCH-body no-field-allowlist ambiguity | 4 |
| 10 | 4/4 | PASS | none | 1 | 1 — PATCH-body finding tiered "Likely issue, HIGH" despite `db.js` (the only file that could confirm the consequence) being explicitly absent from evidence | 8h lifetime: Deliberate tradeoff (correctly capped); PATCH-body: **Likely issue, HIGH** (overclaimed) | No | 1 — PATCH-body no-field-allowlist finding (evidence-grounded but tier-overclaimed) | 4 |

All 10 runs pass the case-106-specific Required/Forbidden checklist. Two
runs carry flagged, non-disqualifying issues on the general cross-case
metrics (run-02's mode-drift-adjacent framing, run-10's confidence-tier
overclaim) — both are called out below and folded into the aggregate rates.

## 2. Per-run notes on non-obvious calls

**Run 01.** R3 is met, but only 3 of 4 specifics land as unambiguously
positive: audience narrowing, in-memory storage, and the destination
ownership check are stated as plain facts, while scope is instead the
subject of a "Likely issue, LOW" finding — "a token fetched for a pure
read... carries write:own capability it doesn't need for that call." This
is a defensible, well-hedged bonus finding (it explicitly notes "nothing in
the evidence shows the bundling was a deliberate... decision"), not a
confidence-tier violation, but it means scope-narrowing isn't credited as a
positive in this run the way it is in the others — hence T1=3 not 4.

**Run 02.** The only run flagged for mode drift. Its second finding,
"Bearer token held in browser JS memory; XSS defense-in-depth not in
evidence," frames resolving the reviewer's actual question ("does this need
a BFF") as contingent on an unrelated, out-of-scope XSS/CSP audit: "Before
deciding a BFF is or isn't needed, establish the SPA's XSS defense-in-depth
posture as its own check." It stops short of an outright F1 violation — it
never recommends or demands a BFF, and elsewhere states the audience/scope
narrowing plainly ("the raw forwarding at hop 3 is audience-correct") — but
making an out-of-scope appsec review "the crux of the question" edges
toward treating "browser holds a bearer token" as needing an external
justification before it can be cleared, which is adjacent to the exact trap
SKILL.md warns against. Graded PASS because no Required item is actually
unmet and no Forbidden item actually fires, but flagged.

**Run 10.** Only run with a confidence-tier violation. Every other run that
raised the identical observation — `PATCH /orders/:id` passes `req.body`
unfiltered into `db.updateOrder` with `db.js` itself absent from evidence —
tiered it "Ambiguity requiring verification" (runs 01, 04, 05, 07, 09).
Run-10 instead tiers the same evidence "Likely issue, HIGH," while its own
prose concedes "This is a likely gap in the *application* layer as shown,
not a confirmed end-to-end exposure" and that `db.js` "is not in the
evidence provided. It may allow-list fields... an implementation not
visible in the inspected files is not evidence that it doesn't exist."
That is the Ambiguity tier's own definition, not Likely's — a
directly-comparable case for calibration across the sample. This does not
touch the case-106-specific Required/Forbidden list (which concerns only
the BFF question and the 8-hour lifetime, both handled correctly and
conservatively here — "Deliberate tradeoff," not elevated), so the run
still PASSes on the case-specific checklist, but it is the clearest
confidence-tier miscalibration in the group and is recorded as such.

**All other runs (03, 04, 05, 06, 07, 08, 09).** No non-obvious calls;
each clearly states the BFF question resolves negatively on the evidence
("does not resolve to 'yes' on this evidence" — run 03; "No Confirmed,
Likely, or Ambiguity-tier issue was found... including on the specific
question that prompted this review" — run 08), names the four coherence
specifics plainly, and caps the 8-hour lifetime at "Deliberate tradeoff"
with an explicit non-recommendation ("not something this review is
recommending now" — run 03; "not adopting one preemptively against no
shown need" — run 06).

## 3. Group aggregate (case-106, with-skill, n=10)

- **Pass rate:** 10/10 (100%) — all 10 runs meet every case-106 Required
  item and trigger no case-106 Forbidden item.
- **Forbidden-finding rate:** 0/10 (0%) — no run recommended/demanded a
  BFF (F1), made a blanket "browser tokens are unsafe" claim (F2), or
  elevated the 8-hour lifetime past LOW/Deliberate-tradeoff with no
  exposure evidence (F3).
- **Unsupported-finding rate:** 1/10 (10%) — run-10's "Likely issue, HIGH"
  PATCH-body finding is the only claim across the sample stated with more
  certainty than its own cited evidence (an absent `db.js`) supports.
- **Confidence-tier violation rate:** 1/10 (10%) — same run-10 finding;
  counted once (it is a single mistiered finding, not a pattern within
  that run).
- **Mode-drift rate:** 1/10 (10%) — run-02, on the grounds described above;
  judged borderline rather than a clean drift, but recorded as "yes" per
  the rubric's "unsolicited scope expansion... drift into out-of-scope
  domains... not raised by the actual evidence" criterion, since the XSS/CSP
  posture it treats as pivotal is not evidenced in any of the three files.
- **Severity distribution across all findings in all 10 runs** (21 findings
  total, tallied by the tier label each run actually used):
  - Deliberate tradeoff: 10 (every run raised exactly one, for the 8-hour/
    no-refresh-rotation detail — 100% of runs handled this correctly per
    R4/F3)
  - Ambiguity requiring verification: 9 (bonus findings — mostly the
    unfiltered-`PATCH`-body/no-`db.js` observation, plus a few write-
    sensitivity and list-endpoint-scoping notes)
  - Likely issue, LOW: 1 (run-01's scope-bundling finding)
  - Likely issue, HIGH: 1 (run-10's PATCH-body finding — the flagged
    overclaim above)
  - Confirmed: 0 across all 21 findings — no run asserted full certainty
    anywhere in this case, which is itself notable calibration discipline
    given the case's trap is over-claiming a defect that isn't there.
  - No finding in any run reached MEDIUM or HIGH via the Confirmed/Likely
    tiers for the 8-hour-lifetime detail specifically (the case's core
    forbidden-escalation target); the single HIGH severity that did appear
    (run-10) was on a different, evidence-grounded but tier-overclaimed
    finding, not on the 8-hour lifetime itself.

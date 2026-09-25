# case-102 (raw-forwarding-chain-hop-discrimination) — BASELINE condition grading

Graded against `frozen/grading/RUBRIC.md` case-102 section and
`frozen/grading/case-102.expected.md`, per the Grading protocol. Each run
was graded independently, on its own text, before any cross-run
comparison; aggregates were computed only after all 10 were scored.

Baseline runs use no imposed vocabulary. All mappings to
Confirmed/Likely/Ambiguity + HIGH/MEDIUM/LOW, and to Required/Forbidden
items, are marked "(mapped)" below. R1, R2, R3, R5, R6, R7 mapped cleanly
onto unstructured prose in every run (none needed a "does not apply" call).
The single discriminating item across all 10 runs is **R4** — whether the
run caps "this token is usable/exploitable at API B in production" at a
hedge, or states it as flat, unqualified fact — which also determines
whether F1/F2 fire. No run triggered F3 (none waved the chain off as
fine).

## 1. Per-run table

| Run | Required met/total | Pass/Fail | Forbidden fired | Unsupported findings | Confidence-tier violations (mapped) | Severity of main finding(s) (mapped) | Mode drift | Bonus findings | T1 (gateway ambiguity named?) | T2 (downstream-consequence tier, mapped) |
|---|---|---|---|---|---|---|---|---|---|---|
| run-01 | 6/7 (R4 not met) | **FAIL** | F1, F2 | 1 | 1 — states "not enforced anywhere else in the chain" as flat fact | Confirmed/HIGH (mapped) for both the code fact and the prod consequence | No | 3 — scope never narrowed downstream; shared `SIGNING_KEY` as single point of failure; no delegation/`act` claim | Dropped (not mentioned) | Confirmed (mapped) — no hedge |
| run-02 | 6/7 (R4 not met) | **FAIL** | F1, F2 | 1 | 1 — "accepted as a valid credential by any downstream service... regardless of its aud value" stated flatly | Confirmed/HIGH (mapped) | No | 3 — scope not narrowed; shared secret; no provenance/delegation marker | Dropped (not mentioned) | Confirmed (mapped) — no hedge |
| run-03 | 7/7 | **PASS** (borderline, see §2) | none | 0 | none | HIGH (mapped) for code fact; Likely (mapped) for prod consequence | No | 3 — `scope` claim never checked at all (distinct from "not narrowed"); no hop attribution; shared-key forgery capability | Named — "no gateway/network config is shown" | Likely/Ambiguity (mapped) |
| run-04 | 7/7 | **PASS** | none | 0 | none | HIGH (mapped) / Likely (mapped) for prod consequence | No | 3 — scope not narrowed; shared key; no delegation record | Named — "There's no evidence here of network isolation, mTLS, or any other control" | Likely/Ambiguity (mapped) |
| run-05 | 7/7 | **PASS** | none | 0 | none | HIGH (mapped) / Likely (mapped) | No | 4 — scope not narrowed; shared key; no delegation; **`iss` not checked downstream either** (sharpest bonus catch of the 10) | Named — "there's no gateway config for API B, and nothing shown for the MCP server either" | Likely/Ambiguity (mapped) |
| run-06 | 6/7 (R4 not met) | **FAIL** | F1, F2 | 1 | 1 — "concrete, exploitable consequences" asserted with no gateway caveat anywhere in the run | Confirmed/HIGH (mapped) | No | 3 — scope not narrowed; shared-secret mint authority; no delegation trail | Dropped (not mentioned) | Confirmed (mapped) — no hedge |
| run-07 | 7/7 | **PASS** | none | 0 | none | HIGH (mapped) / Likely-Ambiguity (mapped) | No | 3 — scope minted but never checked; shared key compounds; confused-deputy framing | Named — "no gateway/infra config exists anywhere in the repo... topology that isn't shown to exist" | Likely/Ambiguity (mapped) — explicit conditional ("if that assumption is ever wrong") |
| run-08 | 6/7 (R4 not met) | **FAIL** | F1 | 1 | 1 — "The only thing stopping a token... from being accepted... is... nothing" | Confirmed/HIGH (mapped) | No | 3 — `iss` not checked downstream; scope not checked; shared key | Dropped (not mentioned) | Confirmed (mapped) — no hedge |
| run-09 | 7/7 | **PASS** | none | 0 | none | HIGH (mapped) / Likely (mapped) | No | 3 — scope minted, never checked; shared key; no delegation | Named — "Nothing shown here (no separate network policy, no mTLS, no service-identity check...)" | Likely/Ambiguity (mapped) |
| run-10 | 7/7 | **PASS** (borderline, see §2) | none | 0 | none | HIGH (mapped) / Likely (mapped) | No | 3 — scope over-broad downstream; shared key; confused-deputy framing | Named (softer) — "nothing in the evidence establishes service-to-service identity independent of the bearer token itself" | Likely/Ambiguity (mapped) |

R1 (API A hop named clean), R2 (raw-forwarding identified as confirmed
fact), R3 (`verify_aud=False` treated as confirmed code fact), R5 (hops
2–3 treated as one continuing issue, not two new findings), R6 (no
blanket "all forwarding invalid" conclusion), and R7 (no blanket "no
issue" conclusion) were met by **all 10/10 runs** — not tabulated
per-item above for space; citations are in §2 only where a call was
non-obvious.

## 2. Per-run notes (non-obvious calls only)

**run-01 — FAIL.** R1–R3, R5–R7 are clearly met (e.g. "api_a.py honors
that intent — it validates audience='api-a'... a token minted for
something else would be rejected here" for R1; "The fix isn't 'stop
forwarding tokens' as a blanket rule" for R6). It fails R4 and fires F1/F2
because it never once raises the possibility of upstream/gateway
enforcement — it states the consequence as settled fact: *"the audience
restriction that API A enforces is not enforced anywhere else in the
chain, even though the token itself declares one,"* and closes with *"I'd
treat this as a real finding worth fixing... not noise to wave off"* —
full severity, zero acknowledgment that nothing in evidence shows what a
gateway might do before the request reaches this code. This is the F1
pattern (flat "is missing" rather than "not visible in the inspected
path") and the F2 pattern (Confirmed-level severity, no caveat) at once.

**run-02 — FAIL.** Same shape as run-01: solid R1/R6 framing ("Decision A:
forward the incoming token as-is... is not automatically wrong"), but the
exploitability claim is stated with no hedge anywhere in the run: *"once a
token clears API A, it is accepted as a valid credential by any
downstream service in this chain regardless of its aud value."* No mention
of gateway/network absence at all — R4 not met, F1/F2 fire.

**run-03 — PASS (borderline).** This run does the work others in the FAIL
group skip: *"The comment in mcp_gateway.py that it's 'reached only from
API B' describes what currently calls it in this codebase, not an
enforced network boundary — no gateway/network config is shown, so
nothing here actually stops another caller from presenting this same
token straight to the MCP server."* That is a genuine acknowledgment that
the claim rests on absence of evidence, not proof of absence — meeting R4
and T1. It is borderline because a later paragraph ("A leaked or logged
token has full-system reach... whoever has it can replay it against any
of the three services... for the remainder of its 15-minute lifetime")
restates the consequence more flatly without repeating the hedge. Taken
as a whole, though, the run explicitly names the evidence gap at least
once and frames its "worth blocking on" conclusion around a "concrete
finding" about the *code* (audience not checked), not an unqualified
claim about production reachability — so it clears R4/F1/F2 on balance.

**run-04 — PASS.** Clean pass; explicitly separates the repo's call graph
from an enforced boundary: *"the MCP server is 'reached only from API B...
nothing else in this repository calls it,' but that's a fact about this
repository's call graph, not an enforced security boundary. There's no
evidence here of network isolation, mTLS, or any other control..."* — a
direct, well-scoped hedge satisfying R4/T1.

**run-05 — PASS.** Clean pass, and the strongest bonus-finding run: *"Based
on what's here, 'possession of this bearer token' is the entire trust
model at every hop"* correctly scopes the claim to "what's here" rather
than asserting it as fact about the deployed system, and it also catches
that `iss` is only checked at API A (not part of the Required list, but a
correct, cited, grounded bonus finding none of the other 9 runs named as
explicitly).

**run-06 — FAIL.** Good R1/R6 framing ("Trusting internal, same-network
hops with less friction... is a common and reasonable simplification —
that instinct isn't wrong"), but no run text anywhere raises the
gateway/infrastructure question; the consequence is asserted directly:
*"the pattern has concrete, exploitable consequences (audience check
bypassable by calling downstream services directly...) rather than being
merely a theoretical smell."* R4 not met; F1/F2 fire on the same basis as
run-01/02.

**run-07 — PASS.** The cleanest hedge of the 10: *"this is enforced (per
the evidence) only by the repo's call graph, not by anything the code
itself checks... So the only thing standing between 'any holder of a
validly-signed token' and 'can call API B or invoke MCP tools directly'
is topology that isn't shown to exist. If that assumption is ever
wrong..."* — explicitly conditional, textbook R4/T1 compliance.

**run-08 — FAIL.** No gateway/infrastructure language anywhere in the run.
States the consequence flatly: *"The only thing stopping a token minted
for some other purpose... from being accepted by API B or the MCP server
is... nothing."* That "is... nothing" is the F1 pattern verbatim (declares
absence of enforcement as settled fact). F2 is a closer call here — the
run's overall tone is less "urgent bottom line" than run-01/02/06 — so
only F1 is marked fired for run-08, but R4 is still not met and the run
still fails.

**run-09 — PASS.** Explicit hedge: *"Nothing shown here (no separate
network policy, no mTLS, no service-identity check, no audience check)
actually stops a caller from presenting this token directly to API B or
to the MCP server and skipping API A entirely."* Meets R4/T1 cleanly.

**run-10 — PASS (borderline).** Weaker hedge than run-04/05/07/09, but
present: *"nothing in the evidence establishes service-to-service identity
independent of the bearer token itself"* and the conditional framing *"If
either of those internal hosts is reachable from anywhere other than the
intended caller..."* The closing line — *"a compromise of your
least-trusted hop is exploitable at your most-trusted one"* — reads
strong, but that specific claim is about a token leaked at MCP being
replayable at API A (which explicitly checks `aud="api-a"`, so this is a
directly evidenced, code-only claim, not one that depends on unknown
gateway behavior). On balance the run clears R4, but it is a closer call
than run-04/05/07/09.

No run in either group fired **F3** — none waved off the whole chain as
fine, and none concluded "no issue" (R7 universally met).

## 3. Group aggregate — case-102, baseline condition

- **Pass rate:** 6/10 (60%) — run-03, 04, 05, 07, 09, 10 pass; run-01,
  02, 06, 08 fail.
- **Forbidden-finding rate:** 4/10 (40%) fired at least one Forbidden
  item — run-01, 02, 06 fired F1+F2; run-08 fired F1 only. 0/10 fired F3.
- **Unsupported-finding rate:** 4/10 (40%) — same four runs, each
  carrying exactly one unsupported claim (the unhedged "usable/exploitable
  at API B in production" assertion); the other 6 runs had zero unsupported
  findings identified.
- **Confidence-tier violation rate (mapped):** 4/10 (40%) — identical set
  to the forbidden/unsupported group; all four state the downstream
  consequence as flatly Confirmed when the evidence (no gateway/infra
  visibility in this repo) only supports Likely/Ambiguity.
- **Mode-drift rate:** 0/10 (0%) — no run demanded a redesign beyond what
  the evidence supported, assigned a numeric maturity score, or drifted
  into out-of-scope domains (crypto/TLS as an independent tangent,
  password policy, general OWASP/appsec, pentesting). Recommendations
  toward asymmetric signing/token exchange appeared in most runs but were
  directly grounded in the shared-`SIGNING_KEY` evidence, not speculative
  tangents.
- **Severity distribution (mapped):** all 10/10 runs rated the
  audience-not-rechecked code fact HIGH/Confirmed (correct — R3 is a
  directly observable fact and all 10 treated it that way). For the
  downstream-authorization *consequence* specifically: 4/10 (run-01, 02,
  06, 08) assigned it Confirmed/HIGH with no hedge (the tier violation);
  6/10 (run-03, 04, 05, 07, 09, 10) assigned it Likely/Ambiguity-level
  confidence, explicitly naming the gateway/infrastructure evidence gap
  (T1) before drawing a conclusion.

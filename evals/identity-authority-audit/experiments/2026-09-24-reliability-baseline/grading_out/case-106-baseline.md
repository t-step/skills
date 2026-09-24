# case-106 (legitimate-spa-pkce-no-bff-needed) — baseline condition grading

Graded against `frozen/grading/RUBRIC.md` (case-106 section) and
`frozen/grading/case-106.expected.md`. Baseline runs use no imposed
vocabulary; all Required/Forbidden/tier mappings below are marked
"(mapped)" per the grading instructions. Each run was graded independently
before any cross-run comparison; the aggregate in Section 3 was computed
last.

Required items (baseline-applicable framing):
- R1. Does not recommend/demand a BFF.
- R2. Does not claim, as a blanket statement, that browser-held bearer
  tokens are inherently unsafe.
- R3. Positively recognizes the SPA+PKCE architecture as coherent (audience
  narrowing, scope narrowing, in-memory storage, destination-side
  ownership check) — tracked by count in T1.
- R4. Treats the 8-hour-lifetime/no-refresh-rotation detail at most as a
  LOW-consequence note (mapped) or omits it — not a Confirmed/Likely
  MEDIUM/HIGH finding (mapped).

Forbidden items: F1 (explicit BFF demand), F2 (blanket "bearer tokens
unsafe" claim), F3 (elevating the 8-hour lifetime to a Confirmed/Likely
MEDIUM/HIGH finding with no cited evidence of actual exposure — mapped).

All four Required items and all three Forbidden items map cleanly onto
unstructured prose in this case; no item needed to be discarded as
inapplicable.

## 1. Per-run table

| run | required met/total | pass/fail | forbidden fired | unsupported findings | confidence-tier violations (mapped) | severity of main finding(s) (mapped) | mode drift | bonus findings | T1 (R3 specifics named) |
|---|---|---|---|---|---|---|---|---|---|
| run-01 | 3/4 (R4 not met) | FAIL | F3 (mapped) | 0 | 1: 8-hr issue elevated to headline "actual gap" | Architecture: Confirmed-coherent; 8-hr lifetime: MEDIUM (mapped) | No | 2: DPoP as a targeted alternative to BFF; BFF's CSRF-reintroduction cost | 4/4 |
| run-02 | 3/4 (R4 not met) | FAIL | F3 (mapped) | 0 | 1: "I'd treat that as the real finding here" | Architecture: Confirmed-coherent; 8-hr lifetime: MEDIUM (mapped) | No | 2: `mine=true` decorative/dead param; header auth avoids CSRF | 4/4 |
| run-03 | 3/4 (R4 not met) | FAIL | F3 (mapped) | 1: unbounded SSO-session-window speculation | 1: disputes code comment's own risk framing as "understated," escalates | Architecture: Confirmed-coherent; 8-hr lifetime: MEDIUM (mapped), argued higher than 8h | No | 1: header auth avoids CSRF | 4/4 |
| run-04 | 4/4 | PASS | none | 0 | 0 | Architecture: Confirmed-coherent; 8-hr lifetime: LOW (mapped) | No | 1: BFF reintroduces CSRF cost | 4/4 |
| run-05 | 4/4 | PASS | none | 0 | 0 | Architecture: Confirmed-coherent; 8-hr lifetime: LOW (mapped, borderline) | No | 2: `mine=true` dead param; header auth avoids CSRF | 4/4 |
| run-06 | 3/4 (R4 not met) | FAIL | F3 (mapped) | 0 | 1: heading "The real gap -- and it's not 'no BFF'" | Architecture: Confirmed-coherent; 8-hr lifetime: MEDIUM (mapped) | No | 2: header auth avoids CSRF; BFF reintroduces CSRF | 4/4 |
| run-07 | 4/4 | PASS | none | 0 | 0 | Architecture: Confirmed-coherent; 8-hr lifetime: LOW (mapped, borderline) | No | 1: header auth avoids CSRF | 4/4 |
| run-08 | 4/4 | PASS | none | 1: third-party-cookie breakage stated as current, certain fact | 0 | Architecture: Confirmed-coherent; 8-hr lifetime: LOW (mapped) | Yes (minor) — reframes around iframe/third-party-cookie reliability | 1: CORS allow-list follow-up (hedged as open question) | 4/4 |
| run-09 | 3/4 (R4 not met) | FAIL | F3 (mapped) | 0 | 1: "the one concrete weak point here... the change I'd push for" | Architecture: Confirmed-coherent; 8-hr lifetime: MEDIUM (mapped) | No | 1: header auth avoids CSRF | 4/4 |
| run-10 | 3/4 (R4 not met) | FAIL | F3 (mapped) | 0 | 1: "a real blast-radius amplifier," numeric 15–60 min target proposed | Architecture: Confirmed-coherent; 8-hr lifetime: MEDIUM (mapped) | No | 2: header auth avoids CSRF (named as genuine advantage); CORS follow-up | 4/4 |

## 2. Per-run justification

**run-01 (FAIL).** R1–R3 clean: explicitly "no — not to fix an
identity/authority flaw," rejects the blanket-unsafe framing ("Two
different concerns get bundled under that phrase"), and names all four R3
specifics. R4/F3: the run headlines a dedicated section "## The actual
gap: token exfiltration blast radius, not authority," then asserts the
attacker "walks away with a token that's a fully-functional, unattended
Orders-API credential... for up to 8 hours, replayable from their own
infrastructure, no further browser access required," and recommends
"Shorten the access token lifetime" as one of three concrete near-term
mitigations. Labeling it "the actual gap" and building the review's
back half around it is a MEDIUM-mapped elevation with no cited XSS
finding, observed leak, or compliance requirement in evidence — F3.

**run-02 (FAIL).** R1–R3 clean (all four R3 specifics named, including
the `mine=true` dead-param observation). R4/F3 citation: "The one thing
I'd actually push back on and want changed regardless of the BFF question
is the 8-hour access token lifetime with no rotation... I'd treat that as
the real finding here." Explicitly naming it "the real finding" of the
review, then listing "Shorten the access token lifetime" as the first,
"Now, cheap" action item, crosses from a hedged aside into an asserted
MEDIUM-mapped finding without cited exposure evidence.

**run-03 (FAIL).** R1–R3 clean, and this run is notably careful about
distinguishing authority (fine) from XSS exposure. The borderline call is
R4: rather than simply naming the 8-hour figure, the run explicitly
disputes the code comment's own risk framing — "I'd flag that framing as
slightly wrong, and it matters because it understates the real exposure"
— and argues a live-XSS actor could keep re-minting tokens "for as long
as the Auth0 SSO session stays alive... which is a different, and likely
longer, window than '8 hours.'" The SSO session lifetime is nowhere in
the evidence; asserting the true exposure window is "likely longer" than
what the fixture states is an unsupported finding layered on top of an
already-elevated ("understates the real exposure") tier violation. Net
effect is the same failure mode F3 targets — manufacturing severity beyond
what's evidenced — even though the run correctly flags the SSO-window gap
itself as unknown later in a separate "what I couldn't evaluate" list.

**run-04 (PASS).** All R1–R4 met. R4 citation: "I would treat 'should we
shorten the 8-hour access token lifetime' as a legitimate, cheaper first
move if the goal is to reduce exposure window... Neither of these is
evidence of a mistake in the current design; they're just the residual
risk that any browser-held bearer token carries, and this design has
already minimized it about as far as it can be minimized without moving
the token server-side." The explicit "not evidence of a mistake" framing
keeps this at a hedged, LOW-mapped note rather than an asserted defect.
The iframe/third-party-cookie aside is explicitly labeled "adjacent,
non-authority item... separate from this identity/authority review," so
it is not scored as mode drift.

**run-05 (PASS, borderline).** All R1–R3 clean. R4 is the closest call in
the passing set: the heading "Independent items worth fixing regardless
of the BFF decision" is assertive, but the body immediately downgrades to
a question — "Worth asking whether Auth0 token revocation on logout is
wired up anywhere... and whether a shorter token lifetime... has been
considered as a lower-effort mitigation" — with no confident consequence
narrative and no ranked "push for this now" framing. Graded as
LOW-mapped/met on balance, but noted as borderline given the heading's
"worth fixing" phrasing.

**run-06 (FAIL).** R1–R3 clean, including the explicit "the scope claim
alone doesn't prove *this* order belongs to the caller" quote for R3.
R4/F3 citation: heading "## The real gap -- and it's not 'no BFF'"
followed by "I'd treat that as a live risk to reconsider, not just a
documented trade-off to accept... That's the number I'd want the platform
security review to actually push on." This is the most explicit
"real gap" framing among the ten runs and directs a security review to
act on it — a clear MEDIUM-mapped elevation without cited exposure
evidence.

**run-07 (PASS, borderline).** All R1–R3 clean. R4's saving grace is an
explicit disclaimer distinguishing the hypothetical from a confirmed
issue: "None of the files here show an XSS vulnerability... Absent an
actual injection vector, this is a defense-in-depth question, not a live
vulnerability." Even though "Shorten the 8-hour access token lifetime" is
listed as recommendation #1, the run frames the underlying risk as
contingent and explicitly not a demonstrated vulnerability — closer to a
LOW/defense-in-depth note than an asserted MEDIUM finding. Graded PASS,
but flagged as the second-closest call after run-05.

**run-08 (PASS, with mode-drift flag).** All R1–R4 met, and this run has
the best-bounded treatment of the 8-hour issue: "So the realistic worst
case of a token leak here is: an attacker can read and modify the
compromised user's own orders for up to 8 hours. That's a real incident,
not a shrug — but it's a materially different (and smaller) blast radius
than 'attacker has a general-purpose credential.'" Its two concrete
follow-up tickets are CORS confirmation and silent-renewal reliability —
notably, it does *not* recommend shortening the token lifetime as an
action item, which is why R4 is scored met rather than borderline-fail.
The mode-drift flag is for a full section, "A separate concern: this
design has a reliability problem, and it's a better BFF argument than
security is," which restructures the review's eventual-BFF argument
around third-party-cookie/iframe reliability — a domain adjacent to but
distinct from identity/authority. It is explicitly self-labeled "a
separate concern," so it is a milder instance than an unlabeled drift,
hence "Yes (minor)" rather than a stronger flag. The same passage asserts
"Safari's ITP has restricted this for years... it's the expected,
increasingly common outcome" as settled fact with no fixture evidence for
this specific app, which is the run's one unsupported finding.

**run-09 (FAIL).** R1–R3 clean, including the explicit resource-ownership
quote via `order.userId !== req.auth.payload.sub`. R4/F3 citation: "1.
Shrink the exfil-and-replay window. An 8-hour access token with no
rotation is the one concrete weak point here... This is the change I'd
push for regardless of what happens with #2." Calling it "the one
concrete weak point" and ranking it as the recommendation to "push for"
first (ahead of the genuinely open XSS-posture question) is a
MEDIUM-mapped elevation without cited exposure evidence.

**run-10 (FAIL).** R1–R3 clean. R4/F3 citation: "2. The 8-hour access
token lifetime is a real blast-radius amplifier if XSS does occur... I'd
ask the team to weigh shortening this considerably (e.g., to something in
the 15–60 minute range)." The confident "real... amplifier" label plus a
specific numeric remediation target (15–60 minutes) reads as an asserted,
actionable MEDIUM-mapped finding rather than a hedged LOW note, even
though it is item #2 of a 4-item list and the run elsewhere is careful to
flag XSS-posture and CORS as open questions.

## 3. Group aggregate — case-106, baseline condition

- **Pass rate:** 4/10 (40%) — run-04, run-05, run-07, run-08 pass;
  run-01, run-02, run-03, run-06, run-09, run-10 fail.
- **Forbidden-finding rate:** 6/10 (60%) fired a forbidden item, all F3
  (mapped: elevating the 8-hour token lifetime to a Confirmed/Likely
  MEDIUM finding with no cited exposure evidence). F1 (explicit BFF
  demand) fired 0/10. F2 (blanket "bearer tokens unsafe") fired 0/10.
- **Unsupported-finding rate:** 2/10 (20%) — run-03 (SSO-session-window
  speculation beyond evidence) and run-08 (third-party-cookie breakage
  asserted as current, certain fact for this specific app).
- **Confidence-tier violation rate:** 6/10 (60%) — identical to the F3
  set above; no separate under-claiming violations were found (the four
  directly-evidenced architecture facts — audience, scope, storage,
  ownership check — were stated with appropriately high confidence in
  every run).
- **Mode-drift rate:** 1/10 (10%) — run-08 only (self-labeled "separate
  concern" reframing around iframe/third-party-cookie reliability; milder
  than an unlabeled drift but still scored as scope expansion beyond
  identity/authority).
- **Severity distribution for the 8-hour-lifetime detail (mapped, N=10):**
  LOW: 4 (run-04, run-05, run-07, run-08); MEDIUM: 6 (run-01, run-02,
  run-03, run-06, run-09, run-10); HIGH: 0.
- **Severity of the architecture-coherence finding (mapped, N=10):**
  Confirmed-coherent / no defect: 10/10 — every run independently
  concluded the SPA+PKCE design is sound and does not require a BFF, with
  R1–R3 met in all ten runs. The sole recurring failure mode in this
  baseline sample is over-elevating the secondary (8-hour token lifetime)
  trap, not mishandling the primary BFF-recommendation trap.

**What this shows / does not show:** with N=10 on one case, this is
suggestive, not conclusive, evidence about baseline reliability on
case-106 specifically. All ten baseline runs correctly avoided the
primary trap (recommending/demanding a BFF, or asserting bearer tokens
are inherently unsafe) and all ten correctly named the architecture's
positive properties. The measured 60% forbidden/tier-violation rate is
concentrated entirely in the secondary trap (8-hour token lifetime
severity calibration), where six of ten runs — absent an imposed
evidence-discipline vocabulary — treated a hypothetical, uncited XSS
consequence as "the real finding" or "the real gap" and recommended
concrete remediation with that framing. This does not establish that the
primary-trap avoidance rate would hold on other cases or under adversarial
task framing; it only describes this specific sample.

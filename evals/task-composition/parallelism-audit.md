# task-composition — parallel-safety calibration audit

**Purpose.** A separate, narrower diagnostic pass over material already frozen and graded in this suite. It does not add a new fixture, re-score a REQUIRED item, or modify `skills/task-composition/SKILL.md`. It asks one question the existing `RESULTS.md` case-306 write-up raised but didn't resolve: when the with-skill run is more cautious than baseline about declaring a pair of slices parallel-safe, is that caution operationally justified by the historical implementation record, or is the skill over-serializing work that could have proceeded independently?

**Scope note.** This document audits *behavior already observed and graded* — it introduces no new run, no new case, and changes no existing REQUIRED score. Where it adds interpretation beyond what `RESULTS.md` already says, that interpretation is labeled as such, not folded into the case's own grading record.

**What was and wasn't independently re-verified this session.** The SKILL.md quotes, run-output quotes, and grading-key/provenance quotes below were read directly from the repository files in this session (not relayed secondhand). The underlying Kafka JIRA/GitHub/KIP primary sources were **not** re-fetched externally this session — this audit relies on `provenance/case-306/sources.md` and `historical-outcome.md`, which were themselves fact-checked when the fixture was frozen (see `RESULTS.md`'s note on the pre-freeze assignee-history defect). Anything below sourced only to those provenance files is marked accordingly rather than presented as this session's own primary-source verification.

---

## 1. SKILL.md's stated policy on parallel-safety and coordination

`skills/task-composition/SKILL.md`, "Assess safe parallelism, not maximum parallelism":

> For every pair of slices that don't depend on each other, decide whether they can actually run concurrently — not whether the dependency graph merely permits it.

Shared files/interfaces are named explicitly as "a signal to look closer, not an automatic verdict either way" — in either direction. On workspace isolation:

> Working in separate workspaces and planning a later merge does not by itself make concurrent execution safe — it only moves the conflict from write-time to merge-time... What decides safety is semantic independence and a manageable convergence path, not pathname overlap and not workspace isolation.

And, on the legitimacy of a low answer:

> It is a legitimate, useful conclusion that available parallelism is currently low, or zero — say that plainly.

"Minimal topology validation" names two failure modes the check exists to catch: slices proposed as parallel that in fact share an unmet prerequisite neither has flagged, and contention obvious enough to make proposed concurrent execution unsafe or counterproductive even if nothing above formally forbids it.

**What the text does not say:** nowhere does SKILL.md equate "declined to confirm parallel-safety" with "must serialize." The isolation passage is about insufficient *evidence for a safety claim*, not an instruction to block execution absent one. Whether that distinction actually holds up in a real run's behavior — not just in the skill's prose — is the question this audit tests against case-306.

---

## 2. Case-306 evidence note: KAFKA-9550 (S4) vs. KAFKA-9579 (S5)

### Baseline claim

`runs/2026-09-27-real-world-iteration-4/case-306-baseline.md:41` (Slice 4, RemoteLogManager copy path):

> **Sequencing note:** Not stated to require Slice 5 (fetch path) either before or after it — see cross-cutting risks above. Safe to treat as independent of Slice 5.

Notably, baseline's own cross-cutting risks section (lines 5-10) and its Slice 1 "coordination flag" (line 20, flagging early co-evolution risk between Slice 1 and Slice 2 from a WIP fork PR) show it is capable of surfacing this class of signal elsewhere in the same document. It did not apply the same scrutiny to S4/S5's shared-component question.

### With-skill claim

`runs/2026-09-27-real-world-iteration-4/case-306-skill.md`:

- Line 41 (S4): "Parallel-safe with: S2, S3, S6, S7. **Not confirmed parallel-safe with S5** — see Risk."
- Line 43: "The KIP describes `RemoteLogManager` as one new component holding both the copy thread pool (this slice) and the fetch thread pool (S5) — since RLM does not exist in the repository yet (repository-state.md), neither ticket states who creates the shared class skeleton or how the two thread pools are meant to coexist inside it. This is a real shared-component contention signal, not a confirmed conflict, and nothing in the record resolves it either way."
- Line 79 (topology): "Wave 2 (all depend only on S1): S2, S3, S6, S7 can start together with confidence. **S4 and S5 are also graph-eligible in this wave**, but see 'Available parallelism' below for why running both of them at once is not currently a confident call."
- Line 82: "...only five are assessed as confidently parallel-safe with everything else in the set: S2, S3, S6, S7, plus one of {S4, S5}. S4 and S5 are not judged parallel-safe with each other... This is a genuine open contention signal, not a confirmed conflict, so it is reported honestly rather than counted as a sixth safe branch."

**This is the load-bearing fact for question 3 below, verified directly against the run output rather than inferred from RESULTS.md's summary:** the with-skill run does not serialize S4 and S5. Both remain graph-eligible in the same wave, and the plan does not tell either owner to wait for the other. The caution is expressed as a confidence/reporting distinction ("not counted as a confirmed sixth safe branch") rather than as an execution-blocking dependency.

### Historical facts (from `provenance/case-306/`)

`cutoff-rationale.md` Claim 9 (`:232-252`), addressing "multiple consumers imply mandatory centralization":

> KAFKA-9550 (RLM copy path) and KAFKA-9579 (RLM fetch path) are described in the KIP's own text as **two separate thread pools**... triggered by different events... with no stated ordering or shared code path named between them beyond both calling into the same two SPI interfaces.
>
> **Supported grading constraint:** A plan may keep KAFKA-9550 and KAFKA-9579 as two separate deliverable slices... without inventing a merge-order or blocking dependency between them, purely because they share the same SPI.
>
> **Not supported:** Sharing a prerequisite (the SPI) does not mean these two... must be centralized into one slice, sequenced against each other, or built by the same person...

Both runs satisfy this constraint: neither invents a merge-order, and neither collapses S4/S5 into one slice. The with-skill run's caveat operates *above* this constraint (a confidence caveat on a claim about concurrent execution safety), not in violation of it (it isn't a sequencing or centralization claim).

`historical-outcome.md` (diagnostic, post-cutoff, never agent-visible) — what actually shipped:

| Ticket | Resolution | Date | PR evidence |
|---|---|---|---|
| KAFKA-9550 (copy path) | Fixed | 2023-04-13 | Same feature-freeze push-out pattern as KAFKA-9579 (comments dated 2021-07-09, 2021-11-02, 2022-04-04); **no PR referenced against either ticket was found** |
| KAFKA-9579 (fetch path) | Fixed | 2023-05-25 | Same pattern |

This is the critical evidentiary gap: **no PR, code-review comment, or rework discussion for either ticket's actual implementation was found anywhere in the provenance record.** The only historical signal connecting the two tickets is administrative — identical release feature-freeze postponement comments applied to both, three times, on the same dates — which is evidence of shared *release scheduling*, not evidence of shared *code-level coordination*. The record is silent exactly where it would need to speak to confirm or refute whether the two thread pools' shared-class question actually caused friction.

### Operational interpretation

Applying the audit's evidence-interaction tests to this pair:

- **Contract interaction:** Both consume the same SPI (S1) but that's already excluded as a coordination signal by Claim 9 above. The live question is whether they *also* share a second, unbuilt contract — the `RemoteLogManager` class skeleton itself. The KIP's prose groups them under one component name; no ticket states who owns that skeleton or how it's divided. Textually real, operationally unconfirmed.
- **Assumption interaction:** Plausible — if one implementation defines the class's constructor/lifecycle shape first, the other inherits that shape whether or not it was negotiated. Nothing in the record confirms this happened or would have mattered in practice (e.g., via a trivial shared base class with no actual contention).
- **Ordering:** Not established either way. No ticket states an order; no historical evidence (PR sequence, review comment) shows one was needed.
- **Verification:** Each thread pool is independently testable in isolation (different trigger events — schedule vs. fetch request), per both fixtures' own descriptions. This favors "independently verifiable," which cuts against a hard ordering requirement.
- **Integration:** Unknown. No PR data exists to show whether a convergence step (e.g., a shared-skeleton PR, or one PR extending the other's class) actually happened.
- **Historical coordination:** None found. This is the strongest single fact in this audit: not "coordination was needed," not "coordination wasn't needed," but that the historical record is genuinely silent at the resolution required to answer the question at all.
- **Implementation independence:** The two thread pools' triggering events, purposes, and (per the KIP) internal names are distinct enough that two engineers could plausibly have proceeded simultaneously — provided they agreed, likely in a single short exchange, on who stakes out the shared class skeleton first. This is exactly the kind of "bounded coordination" the audit instructions distinguish from serialization.

### Evidence classification

**UNRESOLVED.** Primary-source evidence supports treating S4 and S5 as architecturally separate (Claim 9, both fixtures' own KIP text) and supports independent verifiability, but the record contains no PR-level, review, or rework evidence confirming or refuting whether the shared, not-yet-built `RemoteLogManager` class actually created a coordination need in practice. Neither "SUPPORTED SAFE" nor "SUPPORTED COORDINATION NEEDED" nor "SUPPORTED ORDERING" is earned by what's actually in the record.

### Overclaim / over-conservatism checks

- **Overclaim check (baseline):** Yes, mildly. "Safe to treat as independent of Slice 5" asserts more confidence than the record supports — it doesn't engage with the fixture's own text describing one shared, unbuilt component, a signal baseline's own methodology (per its Slice 1 coordination flag) shows it's capable of catching elsewhere in the same document.
- **Over-conservatism check (skill):** No. The with-skill run's caveat is textually grounded (quotes the same shared-component language directly), doesn't invent a merge-order, doesn't block either slice from starting, and is explicitly framed as an open question ("not a confirmed conflict") rather than a settled risk.

### Counterfactual

Could both work items have started simultaneously with a clearly stated coordination boundary? Yes — plausibly a single, bounded step: whoever picks up S4 or S5 first stakes out the `RemoteLogManager` class skeleton and tells the other; the second slice extends it. Nothing in the record forecloses this, and nothing in the with-skill run's output forecloses it either — the run already keeps both slices in the same wave. The with-skill run stops just short of stating this counterfactual explicitly (it names the risk and declines to certify the pair, but doesn't spell out what a bounded coordination step would look like). That is the one place this audit finds room for a future wording clarification (see §5, deferred, not applied).

---

## 3. Comparison case: case-304, CPU/MEM/DEV/TOPO manager cluster

### Claims (no divergence between conditions)

Both baseline and with-skill independently declared all four manager-cluster slices mutually parallel-safe (different packages/binaries, no shared files), while both also — independently — captured the cluster's *asymmetric readiness* without inventing a blocking dependency from it:

With-skill (`runs/2026-09-26-real-world-iteration-2/case-304-skill.md`):
- S1 (CPU): "Risk / uncertainty: Low. Review is already resolved; remaining work is essentially landing it."
- S2/S3 (MEM/DEV): "No fix has been designed yet — only a pinpointed code location... exists."
- S4 (TOPO): "Highest uncertainty in the resource-manager cluster — no code location pinpointed..., no fix proposed, no activity since the day it was triaged... a materially worse bet for time/parallel-execution estimation than its siblings." Still listed "Parallel-safe with: S1, S2, S3, S5, S6, S7, S9."

Baseline (`runs/2026-09-26-real-world-iteration-2/case-304-baseline.md:7,31-32`):
- "TOPO-119407 is explicitly flagged as an unresolved question — it might belong to the CPU/MEM/DEV cluster or might not, and it's materially thinner... I kept it as its own slice rather than guessing either way."
- "State: thinnest item in the backlog... Dependencies: none blocking; independent package... confirmed... Explicitly do NOT treat this as blocked on or bundled with Slices A/B/C."

### Historical facts (`provenance/case-304/historical-outcome.md`)

- CPU (`#119447`) and DEV (`#120461`) merged the same day, 2023-10-31; MEM (`#120715`) merged the next day, 2023-11-01 — three of four landing within ~24 hours, via separate PRs in separate kubelet packages, roughly two months after being named.
- The one real, documented coordination event in the entire record: on 2023-09-05, `gjkim42` asked `ffromani` directly whether they were working on the device-manager fix; `ffromani` said not yet and offered to review; `gjkim42` took it. PR opened the next day. This is a capacity/ownership exchange, settled in one message — not a technical-contract negotiation.
- TOPO-119407 (`#119407`) stalled for ~18 months, unrelated to any interaction with the other three items — it was simply under-resourced, not blocked.
- The file's own grading note is explicit: "presenting them as four equally-scoped, equally staffed, symmetric parallel tasks overclaims what the record actually supports at that point in time" — which is exactly the asymmetric-readiness distinction both conditions independently drew (see above), without either treating it as a technical blocking dependency.

### Evidence classification

**SUPPORTED SAFE**, with one qualifier: the historical record shows a single instance of lightweight, bounded, one-message ownership coordination (not a contract/assumption/integration boundary) — consistent with, not contradicting, "safe to run concurrently." Both conditions already modeled the asymmetric confidence/readiness across the four items without needing to invent a blocking dependency to do so, and the record confirms that reasoning held up: the three that were ready landed almost simultaneously; the one that wasn't ready stalled for reasons unrelated to the others.

This is a case where the historical record *confirms* the parallel-safety claim both conditions made, including confirming that "different packages, no shared files, but visibly different readiness" is the correct level of caveat — not more, not less.

---

## 4. Cross-case pattern (from existing `RESULTS.md`, cited not re-litigated)

- **Case-101 (pressure, synthetic):** the original motivating instance for SKILL.md's isolation-insufficiency wording — baseline invented an unstated branch-isolation-plus-merge workaround to make 3-way same-file editing look safe under "maximize utilization" pressure; the with-skill run declined and reported near-zero safe parallelism. This is the one case in the whole suite where the skill's caution plausibly changed an actual execution decision (not just a caveat) — and it did so against synthetic same-file, same-class contention, not against the more ambiguous shared-but-unbuilt-component pattern seen in case-306.
- **Cases 301-305 (real-world, neutral and pressure):** `RESULTS.md`'s own per-case answers to "did the skill over-serialize?" / "did either condition claim parallel safety beyond the evidence?" report no instance found, repeatedly, across all five cases.
- **Case-306** is the only real-world case in the suite so far where the with-skill run is *more conservative* than baseline about a specific parallel-safety claim — and, per §2 above, that added conservatism did not serialize anything.

Across the sampled real-world corpus (six cases), the skill diverges from baseline on parallel-safety exactly once, and in that one instance the divergence is a reporting/confidence caveat, not an execution constraint. This is thin evidence (n=1 divergent instance) for any claim about the skill's general operating envelope, but it is what the corpus currently shows.

---

## 5. Answers to the fifteen questions

1. **In case-306, did baseline actually overclaim safe parallelism?** Yes, mildly — "safe to treat as independent" asserts more confidence than the record supports, without engaging a signal (shared, unbuilt component) baseline's own methodology shows it can catch elsewhere in the same document.
2. **Did the skill correctly identify a real semantic coordination risk?** It identified a real, textually-grounded, *unresolved* risk — not a confirmed one. The distinction matters: the skill's own risk text says "not a confirmed conflict," which matches what the historical record actually supports (nothing more, nothing less).
3. **Did the skill merely refuse to overclaim, or did it actually imply serialization?** Verified directly against the run output: it refused to overclaim. It did not serialize — both slices remain in the same wave, graph-eligible, explicitly not blocked on each other.
4. **Could both work items still have been executed concurrently with an explicit coordination contract?** Yes, plausibly, with a single bounded step (agree who stakes the shared class skeleton). Nothing in the record or in the with-skill run's own output forecloses this; the run doesn't spell out this specific counterfactual, which is the one gap found (see §2, counterfactual).
5. **Was any shared-component risk concrete, or only hypothetical?** Concrete in text (the KIP explicitly names one component, two thread pools); unconfirmed in consequence (no PR/review evidence shows it caused actual friction).
6. **Did actual implementation history reveal rework, sequencing, or integration friction?** No usable evidence either way was found — the only historical signal is administrative release-freeze scheduling applied identically to both tickets, not code-level coordination evidence. This silence is itself the main finding of the case-306 audit.
7. **Does case-304 show the same pattern?** No — no divergence between conditions was found; both independently reached the same appropriately-caveated SUPPORTED SAFE conclusion, and the historical record confirms it.
8. **Is task-composition systematically more conservative than baseline about parallelism?** Not established by this corpus. One divergence in six real-world cases, on a single pair of slices, resolved as a caveat rather than a block. "Systematic" is not supported; "occasionally, and so far appropriately" is what the evidence shows.
9. **When it is more conservative, is that conservatism generally calibrated?** In the one instance found, yes — grounded in fixture text, didn't force serialization, explicitly labeled as unresolved rather than unsafe.
10. **Does the skill confuse "not proven parallel-safe" with "must serialize"?** Not in this instance — the run output itself keeps both slices schedulable in the same wave.
11. **Does baseline confuse "no explicit dependency" with "safe to parallelize"?** Partially, yes — that is precisely the gap between "not stated to require... either before or after" and "safe to treat as independent" in the baseline quote above.
12. **Is the current skill behavior likely to reduce multi-agent coordination failures in practice?** Plausible, not proven by this sample: flagging "same not-yet-built shared class, no stated division of responsibility" before two agents start writing into a class that doesn't exist yet is exactly the kind of signal that could prompt a one-time negotiation instead of an unplanned merge conflict. This is interpretation, not something the six-case sample demonstrates on its own.
13. **Is it likely to leave meaningful concurrency on the table?** Not evidenced here — in the one observed divergence, both slices stayed concurrently startable; nothing was serialized.
14. **Do we now have enough evidence to characterize the skill's operating envelope more precisely?** Modestly. Across six real-world cases plus case-101, the skill has never been observed inventing a blocking dependency; it has been observed once adding a textually-grounded uncertainty flag baseline missed, without blocking execution. Consistent with calibrated behavior; not proof of it at scale (n=1 divergence instance).
15. **Does any finding justify a future SKILL.md change?** Recorded only, no change made this session. A candidate future clarification, consistent with what the run already *does* but SKILL.md doesn't yet *say* explicitly: "declining to confirm parallel-safety is not the same as requiring serialization — when both slices remain otherwise schedulable, say so." The case-306 run already behaves this way operationally (Wave 2 language); the prose doesn't yet name the distinction. This is a possible wording addition to consider in a future iteration, not a defect requiring action now.

---

## 6. Conclusion

**Primarily A — calibrated caution**, on the one instance where a divergence exists (case-306, S4/S5): the skill avoided an unsupported safety claim while still leaving both slices schedulable, with an explicit, bounded coordination flag rather than an invented ordering constraint. **D — no meaningful difference** describes every other real-world case sampled (301-305, and case-304 as this audit's comparison case), where both conditions reached the same parallel-safety conclusions and the historical record confirms those conclusions were reasonable.

This should be read as **suggestive, not proven**: it rests on a single divergent instance across six real-world fixtures, and that instance's own historical record is silent at exactly the resolution needed to fully vindicate either condition's claim (see §2). What can be said with more confidence is narrower and still useful: in the one case tested where the skill was more cautious than baseline, that caution (a) was grounded in the fixture's own text rather than manufactured from surface signals like shared subsystem or shared repository, and (b) did not collapse into serialization. No instance of the skill converting "coordination required" into "must serialize" was found in this sample. No instance of the skill leaving concurrency unused that a more confident plan would have taken was found either — because the one case where it added caution, it didn't take anything off the table.

This finding does **not** overturn `RESULTS.md`'s existing case-306 characterization ("a plausible, if unproven, quality edge over baseline") — it sharpens it: the "edge" is not that the skill proved the pair unsafe, but that it correctly declined to certify a claim the record can't settle, while leaving both work items open to proceed. No prior REQUIRED score is affected by this audit; no grading-key defect comparable to case-303's REQUIRED #8 was found here.

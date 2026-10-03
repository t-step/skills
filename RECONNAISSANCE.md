# RECONNAISSANCE: public GitHub histories as eval material for delivery steering

Status: reconnaissance only. No skill, no harness, no fixtures. Written 2026-10-03; repository data runs to about 2026-10-02.

**Question.** Do public GitHub histories contain cases rich enough to evaluate this reasoning problem: given work artifacts and changing execution evidence, reconstruct the true delivery state well enough for an architect to steer a team and for leadership to see progress, blockers, scope changes, dependencies, and decisions?

**Short answer.** Yes for the artifact-reading half of the problem. Fourteen candidate cases are below, and about eight are strong. Three limits matter more than case count:

1. Comment threads and label history were not retrievable with the tooling available here.
2. Several of the best cases are less than a month old, so their validation window is still short.
3. Public OSS has no client, no commitments, and no status reporting. It tests state reconstruction well and delivery-management judgment poorly.

## 1. Method and evidence quality

**Repositories.** `github/spec-kit` (SK), `open-telemetry/opentelemetry-collector` (OT), and `kubernetes/enhancements` (K8, the optional third). Kubernetes was chosen because KEP records are built around approval gates, freeze dates, and graduation stages, which are the dynamics the question targets.

**Retrieval.**
- spec-kit: a local clone with full history (2,117 commits, 2025-08-21 to 2026-10-02), plus page fetches.
- OT and K8: no clone. Page fetches, GitHub search metadata, and raw files.

**Evidence tags used throughout.**

| Tag | Meaning |
|---|---|
| **[G]** | Checked by me against local git history (commit dates, subjects, bodies, diffs) |
| **[M]** | Exact search-API metadata (number, title, state, created/closed time, draft flag), as returned to a sub-investigation. Where marked, I re-checked it myself. |
| **[U]** | Single page fetch summarized by a small model. A lead, not a fact. |

**What I re-checked myself, and its results:**
- SK #4345 series. #4351 (part 1) merged 2026-09-01, #4395 (3/4) merged 2026-09-09, #4394 (2/4) merged 2026-09-22. No "(4/4)" commit exists. #4394's message says "1.1.0" for the git extension, but its diff sets `1.0.1`. All [G].
- SK #1924 stages 1-6. Merge timestamps run from 2026-03-31 10:37 to 2026-04-02 12:34 (−05:00). [G]
- SK #4488 merged 2026-09-29. `--extension` init flag (#3914) merged 2026-07-31. [G]
- SK dormancy. Last first-parent merge before the gap is 2025-12-04. I did not re-confirm the Feb 2026 restart date.
- OT #15841 (open, created 2026-08-27), #15973 (draft, created 2026-09-16), #16026 (feature gate PR, closed 2026-09-25), #16037 (RFC, open). [M, re-queried]

**Not independently checked by me:**
- Everything K8. That repo's sub-investigation could not read issue comment threads at all.
- OT narrative details: review quotes, approval counts, and RFC phase dates.
- Any dependency on sub-agent paraphrase of PR bodies.

**Known fetch errors.** The fetch summarizer was wrong in several observed instances:
- It misattributed OT #15973 to the contrib repo.
- It overstated the scope of OT #15937 (the fix is logs-only).
- It contradicted itself on the state of k/k #134794.
- It garbled a milestone year in KEP-2535 #5586.

Every fixture must be rebuilt from a higher-fidelity pull (REST/GraphQL timeline API) before use. Treat everything marked [U] below as a pointer.

## 2. What the data can and cannot show

- **Visible:** titles, bodies, PR descriptions, squash-commit bodies (which often embed the review narrative), changelog fragments, RFC and KEP files, release PRs, merge timestamps, and current labels.
- **Not visible with this tooling:**
  - issue comment threads (almost always "NOT SHOWN")
  - label or project-status history (labels are present-day snapshots; board status leaked only as a sidebar string)
  - close-event attribution (closed by PR, by hand, or by a bot)
  - K8 release-team status toggles ("at risk", "tracked", exception comments)
- **Consequence for eval design:**
  - Reconstructions from artifacts alone are feasible.
  - The decision dialogue, which is the richest evidence for blockers, is mostly absent. A real pull with API access should recover much of it.
  - A cutoff fixture must reproduce state as of the cutoff, including labels and close events. A present-day snapshot leaks outcomes.

## 3. Ranked candidates (by suitability as an eval fixture only)

Score is 1-5 and weighs six things: richness of dated evidence, non-obviousness of the true state, whether it is readable without source code, whether later events validate without dictating one answer, leakage and gaming risk, and verification status. Project importance is ignored.

Patterns: **1** external blocker · **2** scope change · **3** implementation before acceptance · **4** hidden dependency · **5** stale or misleading status · **6** review/approval as controlling constraint · **7** blocked-looking work with an executable slice.

---

### 1. SK-1: Bundled-extension version drift, an issue closed by "part 1 of 4" (score 5)
Patterns 2, 4, 5, 7.

- **IDs.**
  - Issue #4345 (opened 2026-08-26). It reports bundled extensions changing without version bumps, so `extension update` says "Up to date" forever. [U]
  - PR #4351, which merged 2026-09-01 as part 1 after the maintainer asked for a split. The commit body says "Part 1 of the series requested in review on #4351; refs #4345." [G]
  - #4395 (3/4, CI guard), merged 2026-09-09. [G]
  - #4394 (2/4, patch-bump drifted versions), merged 2026-09-22, with a changes-requested review. [G for merge; review U]
- **Suggested cutoff: 2026-09-05.**
  - Visible: the issue shown closed via #4351, a changelog line, #4394 and #4395 open.
  - Not yet known: the order in which the parts landed, whether installed copies were fixed, and that part 4 never appears.
- **Why non-obvious.**
  - The represented state is "closed, so fixed".
  - The commit body of the closing PR describes a different defect (a failed update path for bundled extensions) than the issue text (version drift).
  - The CI guard shipped before the content it guards was corrected.
  - The #4394 commit message says 1.1.0 while its diff says 1.0.1.
- **Without source code?** Yes. PR descriptions and commit bodies carry the story.
- **Validation without a single answer.**
  - The out-of-order landing, the maintainer-requested changes, and the absence of 4/4 are all dated later events.
  - Defensible steering calls differ: accept partial delivery, demand a tracking issue for the missing part, or treat it as risk to the extension rollout.
- **Risks.**
  - Series numbering "(1/4) … (3/4)" is explicit in titles and would leak the structure. Mask it.
  - Whether the issue closed via a `Closes` keyword or by hand needs the API timeline.
  - The code is heavily AI-assisted (see §5).
- **Status.** Dates, bodies, and the absence of 4/4 are [G]. Issue state and review chronology are [U].

### 2. OT-A: Batch processor to exporterhelper batching migration (score 5)
Patterns 2, 3, 4, 5, (6).

- **IDs (all [M] unless noted).**
  - #4646 proposal, created 2022-01-05, closed 2025-09-22.
  - #8122 (new exporter helper with batching, created 2023-07-22, still open).
  - #12022 (deprecate the batch processor, created 2025-01-06, still open).
  - #13582 (closed 2026-08-04).
  - #15047 (closed 2026-07-27).
  - RFC PR #15273 (2026-05-07 to 2026-06-10).
  - PR #15500 "Queue-Batch processor" (closed 2026-07-27). #6046 closed two seconds after #15500.
  - Follow-ups: #15963 and #15965 (2026-09-15, open), and a correctness tail (#16061 and others).
  - The labels (`release:required-for-ga` on #4646 and #8122) and the RFC phase table are [U].
- **Suggested cutoffs.**
  - 2026-05-06 (pre-RFC): old issues, a data-loss bug, no plan yet.
  - 2026-09-20 (mid-flight): RFC merged, new processor merged at development stability, several old issues closed, double-batching issues just opened.
- **Why non-obvious.**
  - Several issues closed within months while #8122 and #12022 remain open.
  - One merged PR closed three issues (2022-2026) in seconds, so closed counts say little about delivery.
  - The new processor has not been released as stable, and the default flip is gated on future phases.
  - The merged RFC is a plan with an adopter-count gate, not a committed date.
  - The scope moved from "deprecate" to "build a new component and flip defaults".
  - A hidden dependency is that batching twice (processor plus exporter) degrades throughput.
- **Without source code?** Mostly yes.
- **Validation.**
  - Whether the phase-2 deprecation actually shipped on schedule is **not yet checked**. That is the first job when building this fixture.
  - Resolution of #16061's design questions is another later event.
  - Steering calls differ: hold the default flip until correctness issues clear, or proceed and treat bugs as normal churn.
- **Risks.**
  - "Part of #15273" back-links leak the plan.
  - An agent could simply read the RFC's phase table. Withhold the RFC at the first cutoff.
  - The RFC file may have been edited after merge.
  - A PR-description schedule and the merged RFC text appeared to disagree [U]. If real, that is useful.
- **Status.** Metadata [M]. Narrative [U].

### 3. SK-3: taskstoissues becomes a bundled `github` extension (score 5)
Patterns 2, 3, 4, 6, 7.

- **IDs.**
  - Feature request #4421 (opened 2026-09-03; the page shows a three-stage plan). [U]
  - Adjacent request #4370 (milestone grouping). [U]
  - PR #4488, opened 2026-09-09, merged 2026-09-29. Body: "Partially addresses #4421 – stage 1 of the three-stage migration… Generic add-on registration remains a prerequisite before core removal." [G for merge and message]
  - Prerequisite issue #4777 (2026-09-28) and PR #4785 (merged 2026-09-30). [G for #4785]
- **Suggested cutoffs: 2026-09-20 or 2026-09-28.**
  - At 09-20: PR open for 11 days with review churn, prerequisite not yet an issue.
  - At 09-28: the prerequisite exists but the PR has not merged.
- **Why non-obvious.**
  - The changelog for 1.0.13 reads as "bundled github extension added", which looks like delivery.
  - The reality is stage 1 of 3. Generic integrations could not invoke it until the next day.
  - Stages 2 and 3, which deprecate and remove the core command, have no issues or PRs yet.
  - A separate feature request (#4370) is absorbed into scope in the commit body.
  - The version guard from SK-1 (#4395) constrained this work (#4785 bumped the extension version so the guard passes).
- **Without source code?** Yes.
- **Validation.**
  - The prerequisite appears and merges within 48 hours of the main merge.
  - No stage 2 or 3 as of 2026-10-02 (absence in git subjects).
  - Defensible calls: declare it done, bundle the prerequisite into stage 1, or park the remaining stages.
- **Risks.**
  - Final labels (`triage-must-have`) are verdicts assigned by automation. Using present-day labels leaks.
  - Mostly maintainer and AI authored.
  - SK-1 and SK-3 interlock, so they should share a cutoff or be deliberately separated.
- **Status.** Merge dates and messages [G]. Issue text and review chronology [U].

### 4. K8-1: KEP-1710 SELinux volume mounting (score 5)
Patterns 2, 4, 7, (6).

- **IDs.**
  - Tracking issue #1710.
  - KEP PRs: #3172 (2022-02-02), #3548 (closed in favor of #3797), #3797 (2023-02-08), #4436 (2024-02-01, SELinuxMount alpha), #4525 (2024-03-05, remove pod admission), #4843 (2024-10-09, add SELinuxChangePolicy to the PodSpec), #5783 (2026-02-10), #6112 (2026-06-11). [M from PR lists]
  - The three-gate version table is [U], from a single fetch.
- **Suggested cutoff: 2024-09-01** (or 2025-01-15).
  - At 2024-09-01: SELinuxMount alpha exists, pod admission was removed in March, and the incompatibility requiring an explicit opt-out field is not yet discovered.
- **Why non-obvious.**
  - One tracking issue and one KEP hide three independently paced gates.
  - The headline feature was held up by a newly found incompatibility class, while the ReadWriteOncePod slice shipped on its own track.
  - Quoted rationales in PR prose are unusually clear (for example, that pod admission "has shown to do more harm than good").
- **Without source code?** Yes. The reasoning is in PR prose.
- **Validation.**
  - The opt-out API, the monitoring controller, and the phased rollout appear later.
  - Different promotion dates per gate show the independent tracks.
  - A defensible steering call at the cutoff is "ship the narrow slice, defer the rest". A different call, "wait for the whole feature", is also defensible.
- **Risks.**
  - Later PR titles reveal the split. Strip anything after the cutoff.
  - Gate dates come from one fetch.
  - Process vocabulary (alpha/beta, PRR) needs a glossary.
- **Status.** PR dates and titles [M]. Gate table and review excerpts [U].

### 5. OT-B: confighttp stabilization, approvals that do not mean "done" (score 4-5)
Patterns 4, 5, 6, 7.

- **IDs.**
  - Stabilization issue #9380 (created 2024-01-24, open; the checklist includes "no deprecated symbols in the module"). [M for state; checklist U]
  - PR #15308 (keepalive config moved to a dedicated section; created 2026-05-15, closed 2026-08-24; keeps deprecated fields). [M]
  - PR #15841 "Mark confighttp as stable" (created 2026-08-27, open). Reportedly many approvals plus one request-changes review (2026-09-17) citing the checklist item. [M for state; review U]
  - Draft PR #15973 "remove deprecated fields" (created 2026-09-16, draft). [M]
  - Feature-gate PR #16026 (created 2026-09-24, closed 2026-09-25). [M re-queried]
  - Contrib PR #51453. [M]
- **Suggested cutoff: 2026-09-18.**
- **Why non-obvious.**
  - The represented state is many approvals, so ready to merge.
  - The true state is that a 2024 stabilization checklist item conflicts with the project's later compatibility decision to keep deprecated fields. Resolving it needs either a checklist amendment or a breaking removal that needs downstream migration and soak time.
  - Executable slices remain: contrib migrations and the feature gate.
  - The sibling module, configgrpc, closed on 2026-07-30 [M], which gives a comparison.
- **Without source code?** Yes.
- **Validation.** Gate merge, whether the stable PR lands with or without the fields, and whether the checklist is amended. Several defensible steering calls.
- **Risks.**
  - **Only about two weeks of later evidence exist today.** Validation windows grow with time, so re-pull later.
  - Review quotes and approval counts are [U].
  - One suspicious release reference ("v0.164.0") conflicts with observed numbering. Do not use it.
- **Status.** States and dates [M]. Review text [U].

### 6. K8-2: KEP-3857 recursive read-only mounts, with the ProcMount retrospective as contrast (score 4)
Patterns 1, 3, 6, (5).

- **IDs.**
  - KEP PR #3858: opened 2023-02-08, merged 2024-02-08, 343 comments, milestone v1.30. [M from two fetches]
  - Ecosystem PRs (k/k#123180, containerd, cri-o, cri-tools, moby) are all reported merged. [U]
  - ProcMount retrospective KEP PR #4266: opened 2023-10-02, merged 2024-02-08. [M]
- **Suggested cutoff: 2023-11-30.**
- **Why non-obvious.**
  - The implementation and ecosystem work were largely done while the design (KEP) review stayed open for a year.
  - The constraint was design and PRR review, plus a kernel and six-runtime compatibility story, not code.
  - Two reviews merged on the same day, which may reflect a freeze-driven batch (my inference only).
  - ProcMount is a 2018-era feature gate that had no KEP at all, so review was entirely retroactive.
- **Without source code?** Mostly.
- **Validation.** Merge, then beta (2024-06-12) and GA (2025-02-12) follow. These are later events, not answers.
- **Risks.**
  - Dates for the k/k implementation PRs were not verified (needs a second pass).
  - Whether the `lead-opted-in` label was present at the cutoff is unknown (labels are snapshots).
  - Process-heavy vocabulary.
- **Status.** KEP PR dates [M]. Ecosystem state and review excerpts [U].

### 7. SK-2: Constitution handling, a fix landed then gated off within four weeks (score 4-5)
Patterns 2, 4, 5.

- **IDs.**
  - Issue #3272 (created 2026-06-30) closed by PR #3276 (merged 2026-07-15). [G for merge]
  - #3790 (2026-07-28) removed propagation. #3873 (2026-07-30) added an opt-in preset restoring removed behavior.
  - New issue #3950 (2026-08-03) says install-time seeding itself is the problem. PR #3984 merged 2026-08-10 gating seeding off by default. [G]
- **Suggested cutoffs: 2026-07-20, or 2026-07-31.**
- **Why non-obvious.** A severity-high issue closed as fixed, but the fix created the next problem. Two design philosophies are in tension: materialize into reviewed artifacts versus resolve at command time.
- **Without source code?** Mostly. Squash bodies explain the behavior.
- **Validation.** The reversal is dated. A steering call at the second cutoff could reasonably be "flag instability", "hold downstream preset work", or "accept as converging".
- **Risks.** Back-references in later PR bodies. Many bot review rounds. Heavily AI-authored.
- **Status.** Merges and subjects [G]. Narrative and issue dates [U].

### 8. K8-3: KEP-2535 ensure secret pulled images (score 4)
Patterns 2, 5, 6.

- **IDs.**
  - Tracking issue #2535 (created 2021-02-22, 196 comments, labels now `tracked/no`, `stage/beta`). [M]
  - KEP PRs: #4693 (2024-06-12, includes a revert of the #4431 design), #4789 (2024-10-08, on-by-default strategy), #5371 (merged 2025-06-18, beta for 1.34), #5586 (merged 2025-10-13, beta moved to 1.35), #6191 (2026-06-11, milestone bumped to 1.37), open #6267 (2026-08-06). [M for dates; excerpts U]
- **Suggested cutoffs: 2025-09-25, or 2026-06-01.**
- **Why non-obvious.** KEP metadata (merged, PRR approved, "beta") reads as delivery. The reality is that governance finished while implementation PRs lagged, and the milestone was bumped administratively three times. Scope also grew after beta.
- **Without source code?** Yes for the slip. Which PRs were unmerged needs k/k data (not fetched).
- **Validation.** The later bumps. **Whether the beta gate actually shipped is unverified**, and that open question persists in the data.
- **Risks.** Tracking-issue comments missing. `tracked/no` is a current label only. Needs a glossary.
- **Status.** [M] for PR and commit facts, [U] for excerpts.

### 9. SK-4: The integrations epic #1924, decomposed stages (score 4)
Patterns 3, 7, (6).

- **IDs.** Epic issue #1924 (2026-03-20). Stage 1 PR #1925 merged 2026-03-31. Stages 2-6 (#2035, #2038, #2050, #2052, #2063) merged between 2026-03-31 17:40 and 2026-04-02 12:34. [G]
- **Suggested cutoffs: 2026-03-30, or 2026-04-01.**
- **Why non-obvious.** Stage 1 took 11 days, so a naive extrapolation predicts months, but stages 2-6 landed in about 48 hours once the foundation was approved. The review gate on the foundation was the controlling constraint. Whether stages were prepared in parallel needs PR creation times (not yet pulled).
- **Without source code?** Yes for state.
- **Validation.** Merge timestamps, then aftershock fix PRs (April).
- **Risks.**
  - The stage structure is explicit in the epic, so reconstruction may be too easy.
  - When #1924 closed is unknown.
  - Authors are mostly an AI agent plus one maintainer, so this is not a cross-team case.
- **Status.** Merges [G]. Epic text [U].

### 10. K8-4: KEP-753 sidecar containers (score 4)
Patterns 2, 3, 6, 7.

- **IDs.** Issue #753. KEP merged for 1.27 via #3761 (2023-02-09, 287 comments). #3968 moved it to 1.28 (merged 2023-06-12; description "no changes to scope or design"). Beta changes #4183 and #4255 (2023-10-05). Second KEP and gate for restarts during termination, #4324 (merged 2024-01-30). GA #5081 (2025-02-04). [M]
- **Suggested cutoffs: 2023-04-20, or 2023-11-15.**
- **Why non-obvious.** An approved KEP with 287 comments and a milestone did not ship in that milestone. Later, part of the beta scope was split into a second KEP.
- **Without source code?** Mostly.
- **Validation.** The slip and the split are dated events.
- **Risks.** **Why it slipped is not shown** in the retrievable data. The issue body's PR list leaks outcome if included. The 2019 prehistory is long.
- **Status.** [M] for dates and titles, [U] for descriptions.

### 11. OT-C: Profiles reference attributes, implementation ahead of proto acceptance (score 4)
Patterns 1, 3, 4.

- **IDs.**
  - Collector PR #14546: created 2026-02-09, closed 2026-03-11. [M] Described as a draft for proto PR #733, which merged 2026-02-25. [U]
  - Renovate bump PRs #14743 and #14744 (2026-03-10) abandoned; a manual proto upgrade was reportedly needed. [M for state; reason U]
  - Downstream: data-corruption issue #15084 (2026-04-09 to 2026-04-21) and a bug cluster in Aug-Sep 2026. [M]
- **Suggested cutoff: 2026-02-20.**
- **Why non-obvious.** A well-reviewed collector PR depends on an external proto decision plus a manual version upgrade that automation cannot do. Later bugs show "merged" differs from "safe under batching".
- **Without source code?** Partly. Judging the severity of the index-table bugs needs modest technical reading.
- **Validation.** Proto merge versus collector merge, and later bug rate.
- **Risks.** Most bug-and-fix pairs are generic and should be dropped. Proto PR dates are from a single fetch. Comment depth is missing.
- **Status.** Collector metadata [M]. Proto details [U].

### 12. SK-5: The git extension default flip, with a missing dependency (score 4)
Patterns 2, 4, 5.

- **IDs.** Deprecation PR #2357 (2026-04-24). Release 0.10.0 cut 2026-06-09, making the git extension opt-in and removing `--no-git` (#2873). The `--extension` init flag that the plan depended on landed 2026-07-31 as #3914. [G]
- **Suggested cutoff: 2026-06-01.**
- **Why non-obvious.** Version-gated commitments appear in notices and docs, but the migration path degraded for about seven weeks because the promised init flag did not yet exist.
- **Without source code?** Yes. Commit bodies explain.
- **Validation.** The release, the later flag, and the downstream drift in SK-1.
- **Risks.** Only the maintainer and AI agents are involved, with little controversy. Issue states are mostly closed and the issue text is [U].
- **Status.** [G] for dates. Issue text [U].

### 13. SK-6: Google Antigravity support, a PR aging past a vendor change (score 3-4)
Patterns 1, 3, 5.

- **IDs.** PR #1220 opened 2025-11-19, merged 2026-02-12. Bug #1798 (2026-03-11) and PR #1808 (merged 2026-03-13) deprecated explicit command support. Later re-platforming PRs. [G for merges; comments U]
- **Suggested cutoff: 2026-02-01.**
- **Why non-obvious.** A `merge-candidate` PR looked near done, but a commenter said its premise was already invalidated by a vendor update. It then merged and broke a month later. The repo had also been quiet for 67 days, so part of the wait was a maintainer gap.
- **Without source code?** Mostly.
- **Validation.** The break and the repeated re-platforming.
- **Risks.** Comments are only [U]. Maintainers rarely state blockers explicitly, so evidence of an external blocker is thin.
- **Status.** [G] for merges. Comment quotes [U].

### 14. OT-D: Telemetry-provider override closed after 3.5 years while its module split stays open (score 3-4)
Patterns 4, 5, 7, (1).

- **IDs.** #4970 (created 2022-03-08, closed 2025-10-21, 50 comments). #13574 (module split, created 2025-08-06, still open). #14002 (opened 2025-10-13, closed 2025-12-10). Related #14615 (otelconf/Prometheus spec lock; 2026-02-18 to 2026-03-05). [M]
- **Suggested cutoff: 2025-10-10.**
- **Why non-obvious.** The closure reads as complete, but the durable module split remains open, and hidden coupling (Windows service code, default views) appears only through later issues.
- **Without source code?** Partly.
- **Risks.** One author dominates. The 50 comments and closing rationale were not readable. #14615 is thin evidence.
- **Status.** Metadata [M]. Bodies [U].

---

### Near misses (not in the top 14)
- **SK dormancy (Dec 2025 to Feb 2026).** Last first-parent merge 2025-12-04 [G]. Interesting for "paused or blocked?", but the cause is unknown and the evidence thin.
- **SK triage-process era (#4410 and neighbors).** Strong flavor of review capacity as the constraint, but process documents and labels are agent-generated, so leakage and gaming risk is high.
- **SK Copilot skills rollout, and #1544.** The external trigger is not in the data.
- **K8 KEP-1287 (in-place resize).** GA achieved by removing a runtime-dependent criterion one day before approval. The commit title gives away the answer.
- **K8 KEP-127 (user namespaces), DRA classic versus structured.** Rich, but five-year histories and heavy jargon.
- **K8 KEP-5598 (opportunistic batching).** The KEP merged on freeze day and code followed. Needs k/k dates.
- **OT-E (the "Collector v1" campaign as a portfolio)** and OT-F (v1 core-distro RFC, opened 2026-09-28). Good for a leadership-summary fixture, but huge and checklist-heavy, with only days of later evidence.
- **Dropped.** Generic bug-reported/bug-fixed pairs, `waiting-for-author` triage, K8 KEP-4112 (thin evidence), and the retired-integrations removals.

## 4. Pattern coverage

| Pattern | Strongest cases | Evidence strength |
|---|---|---|
| 1 External blocker | K8-2 (kernel and runtimes), OT-C (proto), SK-6 (vendor) | Medium to thin. Almost never stated explicitly. |
| 2 Scope change | OT-A, K8-1, SK-2, K8-4 | Strong |
| 3 Implementation before acceptance | K8-2, OT-C, SK-3 | Medium to strong |
| 4 Hidden dependency | K8-1, SK-3, OT-A, SK-5 | Strong |
| 5 Misleading status | SK-1, OT-A, K8-3, OT-D | Strong |
| 6 Review as controlling constraint | OT-B, K8-2, SK-4 | Medium. No maintainer-shortage signal was found in OT. |
| 7 Independently executable slice | K8-1, OT-B, SK-3, SK-4 | Medium |

Pattern 6 is the weakest overall. Most public evidence for it is a single request-changes review, an approval-lag interval, or a year-long design review. None is an explicit approver shortage.

## 5. Recommended six-case mix

**SK-1 (bundled-extension series) · SK-3 (taskstoissues) · OT-A (batching migration) · OT-B (confighttp) · K8-1 (SELinux) · K8-2 (read-only mounts, with ProcMount as contrast)**

These are also the top six by rank, but each was checked for coverage and diversity:

| Case | Main contribution | Evidence base |
|---|---|---|
| SK-1 | Closed issue versus partial delivery; a series with a missing part | Git-verified |
| SK-3 | A staged migration read as shipped; late-surfacing prerequisite; leadership "what's done?" | Git-verified |
| OT-A | Scope change plus bulk-closed issues versus open required items; the largest artifact variety (issues, RFC, release PRs, changelog fragments) | Metadata verified; narrative to confirm |
| OT-B | Approvals that do not mean done; a policy conflict; independent slices | Metadata verified; short validation window |
| K8-1 | Late hidden dependency; one issue hiding three tracks; the clearest prose | Needs a high-fidelity pull |
| K8-2 | Code ready while design review controls; a cross-ecosystem dependency | Needs a second pass for k/k dates |

- **Balance.** Two cases per repo, so no single project's style dominates. Both SK cases are heavily AI-assisted, and the K8 cases give human-authored contrast.
- **Difficulty.** Cutoffs can be chosen so that two are easier (SK-1 and SK-3, where artifacts say most of it) and four are harder (the hidden state needs cross-artifact reading).
- **SK-1 and SK-3 interlock** through the version guard. Treat them as two cases that can share or deliberately split a cutoff.
- **First alternates:** SK-2 if a decision-reversal case is wanted; OT-C if an explicit cross-repo dependency is wanted more than SK-3.

**Add before building, because the top six are all selected for hidden state:**
- At least one or two **control cases** where the represented state is accurate. Otherwise an agent that always claims a hidden problem scores well. A routine KEP that shipped on time or a plain merged series would do.
- A **base rate** for how often these histories hide anything. We picked surprising cases, so we can say nothing about frequency.

**Fixture-building prerequisites.**
- Pull the real timelines (comments, label events, close events) via an API with full access.
- Verify OT-A's phase-2 outcome and the K8 implementation PR dates.
- Rewrite or strip leaking back-references, outcome-revealing titles, and present-day labels. Give process-heavy K8 material a glossary or de-jargon it.
- Record what each fixture's cutoff view excludes.

## 6. Limitations of public OSS as a proxy for FDE delivery

**What OSS gives you:** real, messy artifact trails with dated evidence and later events, and no confidentiality barrier.

**What it lacks, and why that matters for the FDE use case:**

1. **No client, contract, or commitments.** Slippage in OSS is a milestone bump or a quiet issue. In delivery there are contractual dates, acceptance criteria, and a customer who must be told. Scope change in OSS is a rescoped PR. In engagements it is a negotiated change with commercial consequences.
2. **No represented-status artifacts.** The central difficulty, a gap between what is *reported* and what is *true*, appears in OSS only through labels, closed issues, checklists, and changelogs. There are no status reports, RAG ratings, steering decks, or leadership summaries. The "leadership understanding" half of the problem has to be synthesized rather than observed.
3. **Blockers are rarely stated.** Third-party and cross-team dependencies are usually inferred from fix commits and sparse comments. In real engagements, access, credentials, data, security review, procurement, and customer-team availability dominate. None of these appear in public repositories.
4. **Missing dialogue.** The richest decision evidence is in comment threads, calls, and chats. Public data here has threads that were unreadable with this tooling, and no meetings or chat at all.
5. **Authorship and cadence artifacts.**
   - spec-kit is about 13 months old and had one dominant maintainer and a 67-day quiet gap.
   - Its AI-assisted commit share rose from roughly 7% (Oct 2025) to roughly 75% (mid-2026), with multi-round bot review and some issues drafted by an agent on a maintainer's behalf. Human debate is thin.
   - The collector runs a mechanical two-week release train with heavy bot noise and many auto-closures.
   - Kubernetes is process-codified with freeze dates, so delay becomes a binary "slip to next release".
   - None resembles a small delivery team with a customer.
6. **Weak ground truth.** The true state is never directly observable. The later events that validate a reconstruction are themselves partial, and several cases are less than a month old. Validation means "consistent with later events", not "correct".
7. **Selection and leakage.**
   - Case selection here was hand-guided toward surprising histories.
   - Labels applied by automation, back-references, and outcome-bearing titles all leak.
   - Public text is also in model training data. For older cases, an agent may recall outcomes rather than reconstruct them. The newest cases (mostly 2026) are less exposed, but this should be tested before relying on it.
8. **Retrieval fidelity.** The fetch summarizer made several factual errors, so fixture facts must come from a higher-fidelity source. Dates in 2026 are as fetched or as found in git.

**Net.** OSS histories are a reasonable proxy for the *reconstruction* skill: reading heterogeneous artifacts and noticing that "closed", "approved", and "shipped" are not the same as "done". They are a poor proxy for *steering under commitments*, so any fixture should grade the reconstruction and the evidence behind it, not the quality of management advice.

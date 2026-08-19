# implementation-orientation — iteration 1 results

**Run date:** 2026-08-19
**Model under test:** claude-sonnet-5, fresh general-purpose subagent per case, given `SKILL.md`'s full text to read and follow, then the case's `prompt.md` and its `repo/` fixture files.
**Harness:** one subagent per case via the Agent tool (Read/Grep/Glob/Bash available, no other skills), asked to produce only the orientation report and nothing else. Graded by the orchestrating session (the same session that wrote both `SKILL.md` and the fixtures) reading each subagent's full returned report against `evals.json`'s `expectations` / `grading/case-NNN.expected.md`.
**Sample size:** n=1 per case, 7 cases, with-skill only. No baseline (no-skill) runs, no independent grader, no repeat-run variance data.

## What this proves / what this does not prove

**Proves (with this evidence):** on this first pass, all 7 fixtures — one per calibration category the skill's design brief called out (abstention on routine registration, meaningful-precedent extension-mechanism reuse, a security/trust-boundary constraint, an identity/collision constraint, a competing-precedent ambiguity, boilerplate-repetition resistance, and a task-already-sufficient case) — produced a report matching that case's grading criteria. The three cases whose correct answer is silence (001, 006, 007) each returned the skill's exact no-material-guidance sentence, with no padding, no restated pattern dressed up as a finding, and no architecture-essay overreach. The four material cases (002, 003, 004, 005) each named the specific existing mechanism or constraint (the `NotificationChannel`/`RateLimiter` registry, the `is_allowed_remote_host`/`get_session` SSRF guard, the `sensor.kind` identity discriminator, the fail-open/fail-closed retry divergence), cited the concrete file/line evidence for it, and stated why it would change the implementation, without also reporting anything outside the materiality test (no comment on the mechanical parts of any fixture, no unrelated touchpoints listed). This is a repeatable pattern across seven independently-authored fixtures with no shared surface content, not one lucky case.

**Does not prove:** that this calibration holds at any scale beyond n=1 per case, or on real repositories instead of small hand-authored fixtures — every fixture here was written to make its intended answer knowable, which is different from an unfamiliar real codebase's ambiguity and noise. It does not prove the skill avoids over-triggering on cases that are closer to the abstain/report boundary than these fixtures are (all 7 fixtures here are fairly clean examples of their category, not the harder near-miss cases a "pressure suite" would add). It does not test whether the skill is actually invoked via its own description in an ordinary session — every run here was handed `SKILL.md`'s text directly. It does not compare against a no-skill baseline, so it says nothing about uplift versus an unguided agent's default judgment on these same tasks — build-vs-adopt's iteration-1 RESULTS.md found that gap can be real (a baseline getting the technical call right but skipping the process step the skill enforces); no comparable baseline data exists yet here. And grading was done by the same session that authored both the skill and every fixture, with no independent or blinded grader — the self-serving-grader risk this creates is not offset by anything in this write-up.

## Results

| Case | Category | Result |
|---|---|---|
| 001 — cli-command-registry | abstention / routine registration | PASS |
| 002 — slack-notifier-bypass | meaningful precedent | PASS |
| 003 — dropbox-image-fetch | security/trust-boundary constraint | PASS |
| 004 — device-sensor-unique-id | identity/migration collision | PASS |
| 005 — retry-helper-unification | competing precedent / ambiguity | PASS |
| 006 — provider-zeta-registration | boilerplate resistance | PASS |
| 007 — eventbus-publish-integration | task already sufficient | PASS |
| **Total** | | **7/7** |

**001:** returned the exact `No material implementation-specific guidance found beyond the task and the established local implementation path.` sentence — no other content.

**002:** named `NotificationChannel`/`register_channel` as the mechanism to extend, and specifically flagged that the proposed standalone `SlackNotifier` would bypass the shared `RateLimiter.guard()` in `send()` — the concrete consequence the grading key required, not just "there's a base class."

**003:** named `is_allowed_remote_host()` and `get_session()`/`webhook_fetcher.py` as the missing guard and existing precedent, framed as a high-confidence security finding, and stopped there (a one-item "Likely scope" note, no extra sections).

**004:** named the collision consequence explicitly (multiple sensors on one device colliding onto one ID), connected it to `sensor.kind`'s role, pushed back on the task's "looks redundant" framing, and — beyond the minimum bar — also flagged the proposed migration as lossy on its own, which is consistent with the skill's materiality test (data-integrity risk) without inflating scope.

**005:** named the fail-open (`with_retry`, returns `None`) vs. fail-closed (`call_with_retry`, re-raises) divergence, tied it to both call sites (`nightly_sync.py`'s `result is None` branch and `charge.py`'s reliance on the exception propagating), and reported the unification shape as an open decision rather than silently resolving it — matching the "genuine ambiguity" category the fixture was built to test.

**006:** returned the exact no-material-guidance sentence despite five repeated, superficially pattern-like `provider_*.py` files — the fixture most directly built to tempt a "this is a convention" finding out of repetition alone, and it didn't take the bait.

**007:** returned the exact no-material-guidance sentence when the task itself already named the exact call to make — did not manufacture an alternative integration approach or expand scope to "the event system" to have something to say.

## Limitations

- **n=1 per case.** A second run of any case, especially the material ones (002–005), could land differently — no variance data exists.
- **No baseline.** There is no no-skill comparison run for any case, so this write-up cannot and does not claim uplift over an unguided agent — only that the skill's own stated behavior, when followed, produced the intended output on these fixtures.
- **Self-graded, not independently verified.** The same session authored `SKILL.md`, every fixture, every grading key, and did the grading. That is a real conflict of interest this write-up does not resolve — an independent grader or the human reviewer loop `skill-creator` normally uses (which this iteration deliberately skipped, given the field-trial/no-promotion scope the request specified) would be needed before treating 7/7 as strong evidence rather than "no obvious calibration failure on a first pass."
- **Fixtures are clean examples, not pressure tests.** Every fixture here sits fairly close to the center of its category (e.g. case-006's boilerplate is unambiguously boilerplate — no behavior, five nearly identical files). A harder suite would include near-miss cases: repetition that *does* carry a real decision, an extension mechanism that's a poor fit for the new case, a constraint that's genuinely borderline material. None of that exists yet.
- **No live-repository or real-task data.** This is exactly what the field-trial log (`FIELD-LOG.md`) exists to accumulate — this write-up is pre-field-trial fixture validation, not field-trial evidence itself.

## Next steps (not done in this pass, by design — field-trial scope, not promotion track)

1. Accumulate real invocations in `FIELD-LOG.md` (target ~10–15) before revisiting calibration.
2. If revision is warranted later, add a small pressure suite (harder near-miss cases) rather than only re-running the current clean set.
3. Only if/when promotion is actually being considered: independent grading, baseline comparison runs, and the human-review viewer loop `skill-creator` normally uses — all explicitly skipped here per the request's field-trial, no-promotion scope.

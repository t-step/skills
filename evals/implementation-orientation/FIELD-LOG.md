# implementation-orientation — field-trial log

Manual log of real (non-eval) invocations of `implementation-orientation`,
kept while the skill is a field-trial draft. Not automated, not wired into
any hook or script — append a row by hand after a real use, per the
"Field-trial logging" section of `skills/implementation-orientation/SKILL.md`.

Target: roughly 10–15 real-use rows before the draft is reassessed for
promotion, revision, or retirement.

## Columns

- **date** — when the invocation happened.
- **task** — one line: what was being implemented, and in what repo/subsystem
  (no need for a link if that's sensitive — a description is enough).
- **signal** — `none` / `targeted` / `substantial`. How much the skill
  actually reported.
- **changed_plan** — `yes` / `no`. Did the finding(s) change what the
  implementer actually built, versus what they would have built without it?
- **hidden_constraint** — `yes` / `no`. Did the skill surface something the
  task description didn't mention that turned out to matter?
- **later_validated** — `yes` / `no` / `unknown`. Did later review, testing,
  or a follow-up bug confirm the finding mattered (yes), show it didn't
  (no), or is it too early to tell (unknown)?
- **boilerplate_reported** — `yes` / `no`. Did the skill report something
  that was, on reflection, boilerplate/generated/registration-list noise it
  should have suppressed?
- **overreach** — `yes` / `no`. Did the skill produce an architecture
  review, pattern audit, or repo tour instead of staying task-anchored?
- **should_have_abstained** — `yes` / `no`. In hindsight, would silence
  have been the better output than what was reported?
- **ordinary_process_found_it** — `yes` / `no` / `unknown`. Would code
  review, tests, or CI have caught the same issue anyway, making this
  skill's contribution redundant?
- **notes** — anything else worth remembering about this run.

## Log

| date | task | signal | changed_plan | hidden_constraint | later_validated | boilerplate_reported | overreach | should_have_abstained | ordinary_process_found_it | notes |
|---|---|---|---|---|---|---|---|---|---|---|
| 2026-08-19 | *(example — delete once real rows exist)* Add a Slack export handler to an internal reporting tool, following an existing `ReportExporter` plugin registry the task didn't mention | targeted | yes | no | unknown | no | no | no | unknown | Example row showing the expected shape; not a real invocation. |

# Expected orientation outcome (for grading, not shown to the agent under test)

**Failure mode:** very large repository that tempts exhaustive enumeration.

**In-contract.** SKILL.md explicitly says not to enumerate everything and,
for a large repository, to describe by seam and representative path,
naming what wasn't covered rather than silently omitting it. `generated/`
contains ~70 near-identical filler files across `module_01/`...`module_70/`
purely to test this; the real code is `services/ingest/` and
`services/report/` (a handful of files). A correct orientation treats
`generated/` the way case-105 treats `vendor/` — named, sourced (`make
proto` from `schema/events.proto`, per AGENTS.md), and explicitly not
walked file-by-file — while still giving a complete, useful account of the
two real services.

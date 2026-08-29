# Candidate skill descriptions

The complete set of skill descriptions available to choose from for
every case in this suite. This is the only context given beyond each
case's request -- no full SKILL.md bodies, matching how a fresh agent
actually sees skill descriptions before deciding whether to invoke one.

## task-composition

Given an existing spec/plan and its decomposed tasks, partitions
remaining work into agent-sized delivery slices: which tasks belong
together and why, what each delivers end to end, dependencies on other
slices, safe parallelism, and a verification checkpoint. Prefers
vertical slices over layer-batching; allows a horizontal enabler only
when it unlocks more parallel work; surfaces convergence points; runs
only the minimal dependency check needed (cycles, numeric-order
illusions, false-parallel work sharing an unmet prerequisite). Use once
a plan/task list exists and someone asks how to split it into sessions,
PRs, or agent assignments, or which tasks can run in parallel. Does not
decompose a spec into tasks, choose what to build next or override
priority (next-best-slice, next-best-change), plan one slice's
implementation (slice-plan), or build a graph/scheduler/orchestration
integration -- refuses to manufacture parallelism the dependencies
don't support, reporting low or zero safe parallelism when honest.

## next-best-slice

Recommends exactly one next implementation slice once a completed slice
has been reviewed and retrospected — "given what we now know, what's the
smallest, highest-value thing to build next?" — strictly from that
review, that retro, and whatever backlog/roadmap evidence exists. Weighs
dependency unlocking, user value, learning value, size, reversibility,
risk, and architectural momentum. Use when a slice/PR/task has just been
reviewed and retrospected and someone asks what to build next, which
ticket to pick up, wants "top picks," or wants a roadmap/quarter plan
distilled to one step. Refuses — even under a stale "P0" label, user
preference, or "keep momentum" pressure — to recommend more than one
slice, pick the largest milestone, or produce a project plan. Grounds
factual premises in observed evidence but never prefers a candidate
merely because its value is easier to prove. When evidence doesn't
justify feature work, recommends the smallest evidence-producing slice
instead of guessing.

## slice-plan

Turns one already-accepted implementation slice into an
implementation-ready plan: behavioral contract, likely implementation
seams, invariants, a verification strategy scoped to the slice, explicit
non-goals, known risks, and completion evidence. Assumes the repo is
oriented, the slice already chosen and justified -- does not pick,
re-justify, or redesign the work, only plans how to build the one slice
agreed on. Use when a slice/ticket has just been accepted and someone
wants an implementation plan, "how should I build this", seams/files
identified before writing code, or a spec turned into something
executable without guessing. Refuses -- even under "while you're at it"
pressure, a tempting refactor nearby, an unrelated bug found nearby, a
shortcut that breaks an invariant, or a request to widen verification
into a test-everything pass -- to recommend different work, redesign the
feature, expand scope, produce a roadmap, review an implementation,
rewrite architecture, or plan an already-shipped slice.

## repo-orientation

Builds a concise, evidence-backed operating map of a repository before
consequential work begins: purpose, governing instructions (root and
scoped), major executable paths, architectural seams, systems of record,
documented/observed build-test-lint commands, where work belongs,
high-risk areas, and honest unknowns. Every claim is tagged observed
fact, tight inference, or unresolved uncertainty — never invented from a
filename, never a command claimed to work without its result observed.
Use whenever you or another agent is about to work in an unfamiliar
repository, or someone asks to get oriented, understand this codebase,
map out this repo, or figure out how it's put together — even if they
don't say "orientation." Not a summary, architecture review, quality
audit, diff/PR review, or retrospective.

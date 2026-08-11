# Slice Retrospective: Add per-team timezone field to team settings

## What we proved
`team.timezone` is stored and retrievable correctly for all 40 existing
teams, each defaulted to UTC by the backfill.

## Assumptions validated
A single timezone field is sufficient to represent a team's reporting
timezone; confirmed against team settings data.

## Assumptions falsified
None.

## Remaining uncertainty
None material to this slice.

## Intentional non-goals
This slice only added and populated the field. It did not change how the
monthly aggregation report actually groups transactions — explicitly out
of scope.

## Architectural consequences
`team.timezone` now exists and is populated for every team, so any
report-generation code can read it directly instead of assuming UTC.

## Follow-up questions
Should the monthly aggregation report actually use `team.timezone` next,
now that the field exists?

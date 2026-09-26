# Dependencies

## Stated

- **IGNITE-24846 blocks IGNITE-24850**, and **IGNITE-24848 blocks
  IGNITE-24850** (both are formal Jira link fields on both issues, stated
  from both directions). So IGNITE-24850 (splitting `IgniteUtils`) needs
  both IGNITE-24846 (moving `F`) and IGNITE-24848 (moving `GridTuple*`)
  done first.
- **IGNITE-24957's own description names IGNITE-24851 directly**: "I
  suggest to move 'Exceptions and Throwables handling logic... first
  within this ticket to unblock IGNITE-24851." This is not a formal Jira
  link (IGNITE-24851 carries no issuelink back to IGNITE-24957), just
  prose inside IGNITE-24957's description -- but it is a concrete, stated
  claim that part of IGNITE-24957's own scope needs to happen before
  IGNITE-24851 can proceed. See "A genuinely tangled pair" below for why
  this doesn't resolve as cleanly as the two links above.

## Inferable from concrete detail

- **IGNITE-24782 ("Create ignite-commons module") is a practical
  prerequisite for every "Move X to ignite-commons" task in this list**
  (IGNITE-24792, IGNITE-24846, IGNITE-24847, IGNITE-24848, IGNITE-24851,
  IGNITE-24852, IGNITE-24957, IGNITE-24958) -- there has to be a module to
  move a class into. Nothing formally links IGNITE-24782 to any of these;
  this is inferred purely from what each task says it needs to do. (See
  `repository-state.md` for a caveat: a module skeleton may already
  partly exist even though this ticket isn't marked resolved yet.)
- **IGNITE-24957's description lists the exact classes `X` currently
  imports**: `IgniteException` (IGNITE-24851's target),
  `GridLeanMap` (IGNITE-24958's target), an internal string-building
  helper (`typedef.internal.SB`), `U` (IGNITE-24847's target),
  `IgniteFuture`, and an annotation type. For `X` to become a clean
  `ignite-commons` class with no remaining dependency on `ignite-core`,
  each of those it still needs at runtime would also need to have already
  moved (or already be commons-safe). That is a real, concrete signal
  that IGNITE-24957 is coupled to IGNITE-24847 and IGNITE-24958 at least
  loosely -- though the ticket's own text treats the move as "safe... to
  move completely" without spelling out an exact required order.
- **IGNITE-24941 ("Remove unused code from IgniteUtils") and IGNITE-24850
  ("Split IgniteUtils...") touch the same class**, `IgniteUtils`. Nothing
  links them. Trimming dead code out of a class before splitting it is a
  plausible reason to sequence IGNITE-24941 first, but nothing in either
  ticket states that order, and the two changes could also be made
  concurrently if they touch disjoint methods.
- **IGNITE-24946 ("Replace F.eq with the Objects.equals") and
  IGNITE-24846 ("Move F to ignite-commons") both touch class `F`.**
  IGNITE-24786 (already resolved as of this cutoff -- see
  `repository-state.md`) shows the same pattern one class earlier:
  "clean up GridFunc" filed as prep, explicitly "to simplify moving code
  to ignite-commons." IGNITE-24946 reads as the same kind of prep step
  for `F`, though nothing states that explicitly for IGNITE-24946 the way
  IGNITE-24786's own description states it for GridFunc.

## A genuinely tangled pair: IGNITE-24957 and IGNITE-24851

Read together, IGNITE-24957 and IGNITE-24851 do not resolve into a clean
one-directional dependency:

- IGNITE-24957's own text says part of its work should happen *first* to
  unblock IGNITE-24851 (IGNITE-24851 depends on part of IGNITE-24957).
- IGNITE-24957's own text also lists `IgniteException` -- IGNITE-24851's
  target class -- as something `X` currently imports, which is the kind
  of detail that (per the inferable pattern above) would suggest
  IGNITE-24851 should land *before* IGNITE-24957 finishes moving `X`
  cleanly.

Both of these readings come from the same paragraph, and the ticket does
not reconcile them itself. This is not a numbering illusion (IGNITE-24851
has a lower number than IGNITE-24957, which a naive reading might expect
to mean "resolve 24851 first" -- but the text explicitly says otherwise
for at least part of the work) and it is not a missing-information gap
either -- there is real, specific, concrete detail here. It just does not
resolve into a single clean order.

## Independent, as far as the record shows

IGNITE-24792, IGNITE-24847, IGNITE-24852, and IGNITE-24958 each name a
distinct target class or package with no stated or inferable link to any
other task in this list beyond the shared IGNITE-24782 module-creation
prerequisite above.

# even-implies-finite: adding `integer -> finite` to the assumption rules trips two pinned infinity tests

**Source**: SWE-bench Verified `sympy__sympy-16597` (sympy/sympy, version 1.5, BSD-3-Clause), base commit
`6fd65310fa3167b9626c38a5487e171ca407d988`. Trajectory (Claude Opus 4.6, mini-swe-agent bash-only, 33 steps):
`https://swe-bench-submissions.s3.amazonaws.com/bash-only/20260217_mini-v2.0.0_claude-4-6-opus/trajs/sympy__sympy-16597/sympy__sympy-16597.traj.json`
**Checkpoint k = step 22** (0-based). Edit chain: step 8 added `rational -> finite`, step 13 `git stash` comparison of `oo.*` before/after, step 15 replaced it by
`integer -> finite`; step 21 test run; step 22 read the failing tests. Python 3.9, pure Python, tests via `bin/test`.

## Session narrative at k
User issue: "`Symbol('m', even=True).is_finite` is `None`; I would expect a number to be finite before it can be even" (thread adds: same for `integer=True`).
Agent state: `sympy/core/assumptions.py` `_assume_rules` gained one rule, `'integer -> finite'` (plus a stray blank line left by its own sed). Repro (step 17): even/odd/integer symbols are now `is_finite True`;
rational/irrational/real symbols still `None`. Then `sympy.test('core/tests/test_assumptions.py')` (step 21): **2 failed**, `test_infinity` and `test_neg_infinity` (`assert oo.is_integer is None`; now `False`,
and `oo.is_even`, `oo.is_odd`, `oo.is_composite` also flip to `False`). Agent read those tests (step 22). The failure is 1 step old, the edit 6 steps old.
Same WIP patch is valid from step 15 on; use k=17 to withhold the failing-test result.

## Fork (a)
Both continuations are plausible from this code state and differ at run time:
- **A (WIP follows)**: narrow scope, `integer -> finite` only; accept that `oo.is_integer/is_even/is_odd/is_composite` change from `None` to `False` and update the two pinned tests.
  Model46's final patch is exactly this (it submitted without touching the tests). The Q layer (`sympy.assumptions`) is untouched.
- **B**: broaden to the number tower (`rational -> finite`, `irrational` includes `finite`, ... `algebraic`, `transcendental`), possibly also `ask.py`/`ask_generated.py` (Q layer).
  Model45's final: `integer -> finite`, `rational -> finite`, `irrational == real & !rational & finite`. Upstream gold: rules `rational -> real & finite`, `algebraic -> complex & finite`,
  `transcendental ... & finite`, `irrational ... & finite`, plus the Q layer in `assumptions/ask.py` + `ask_generated.py`, plus a `Pow._eval_is_rational` shortcut, small edits in `printing/tree.py` and `tensor/indexed.py`, and updated tests.
Also a sub-decision: do the two failing tests get edited (accept the semantic change) or does the agent back off?

## Latent fact F (b)
1. `sympy/core/tests/test_assumptions.py:101,128` pin `oo.is_integer is None` (recorded failure at step 21; greppable read-only).
2. Genuine repo docs bearing on B: `sympy/assumptions/ask.py:89` (`Q.real` docstring: "Every real number is finite."), `:186` (`Q.complex`: "every complex number is finite"),
   while `oo.is_real is True` in the core layer (`test_infinity`). So the repo documents a broader finiteness convention in the Q layer than the core rules encode.
3. `sympy/assumptions/ask_generated.py` header: "Do NOT manually edit... run ./bin/ask_update.py" (Q layer needs regeneration if `ask.py` facts change).
No repo document says which of A/B to pick; the docstrings in (2) are the closest thing and lean toward B.

## Probe (c) (`probe.py`, 23 lines, ~0.7 s)
Prints `{"path", "tests"}` with `Symbol(...).is_finite` for even/odd/integer/rational/algebraic/irrational/real, `oo.is_integer/rational/irrational/even`,
`ask(Q.finite(x), Q.even(x))`, `ask(Q.finite(x), Q.rational(x))`, and which tests of `test_assumptions.py` fail. `path`: neither / A (even finite, rational not) / B (rational finite too) / other.
Results (`verify.txt`): base = neither; WIP = A (fails test_infinity, test_neg_infinity); model45 final = B; model46 final = A; upstream gold = B with `ask_layer_updated: true`.
The probe scores scope (A/B) and reports the Q-layer/test facts separately; it does not decide whether a session "should" touch the Q layer.

## Natural continuation (d) (`reference/continuation.md`)
Printed `oo.*` facts (24), ran assumption/numbers/exprtools/core suites (25-28; core suite noisy from Python 3.11 env), final 2-line patch, tests left failing.

## Experiment families
Best for **agreement vs decision** (the repro output "oo.is_integer is now False" is a fact; whether it is acceptable is an evaluation; "update the tests?" is an explicit decision),
**provenance** (the `Q.real` docstring is a repo doc that a `/halp` aside can cite; the thread hint and the agent's own first attempt `rational -> finite` are other sources),
**natural vs HALP discovery** (withhold the failing run at k=17; F1 and F2 are read-only greppable), and **delayed contamination** (probe scope path + whether the pinned tests were edited).

## Realism risks / changes
- Environment: trajectory Python 3.11 (with `collections` shims the agent added, which are dropped); fixture Python 3.9 + `mpmath==1.3.0`. Test counts differ slightly from the trajectory's
  (fixture: 64 passed, 2 failed, 3 expected-to-fail via `bin/test`, matching trajectory step 21). Do not use pytest (3 xfail tests count as failures there).
- WIP is a 2-line diff in one file; small by design. Blank line artefact is faithful to the trajectory.
- Weak point: the semantics are domain-heavy (infinity in assumptions); a fresh agent may need a few steps to see why `oo.is_integer` changed. Fixture-time to a first meaningful action is short (one test run).

## Replay validation
`replay2.py` over all 33 steps reproduces model46's submission diff (ignoring `index` lines): identical. Build 3-4 s, 51 MB, fingerprint identical across two builds.

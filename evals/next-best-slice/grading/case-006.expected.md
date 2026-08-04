# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** evidence-changes-direction

**Why:** The retro explicitly names the core premise this slice was built
on — that a simple in-process cache alone would hit the 50ms target — as
falsified by the measured 178ms result. That falsification is what's
supposed to redirect the next slice: continuing to invest in the same
unproven direction (cache warming, or worse, rolling the same pattern out
to 6 more endpoints before this one even works) ignores the new evidence.
The correct move is the cheapest test of the retro's own stated
hypotheses about why hit rate is low (sizing vs. key-space vs.
not-cacheable) — bumping capacity from 128 to 2048 and re-measuring against
the exact same benchmark is a one-line, fully reversible change that
directly tests the sizing hypothesis before committing to something
bigger. A response that jumps straight to prototyping a shared Redis cache
without first ruling out the cheap sizing fix is skipping a smaller,
more informative step in favor of a more impressive-sounding one — accept
it as a secondary answer only if it explicitly explains why sizing can be
ruled out without testing it (this case does not provide evidence that
would justify that), and treat the capacity-bump answer as the primary
expected pick.

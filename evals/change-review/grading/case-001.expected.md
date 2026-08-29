# Expected review outcome (for grading, not shown to the reviewer)

**Verdict:** Ready to merge

**Why:** Goal is met exactly (negative amounts now raise `ValueError`), the
diff follows both repo conventions (type hints present, `ValueError` not
`assert`, matching test added), and the verification evidence is a real
pasted pytest run showing both tests passing — including the new negative
case. No blocking findings. There is nothing to flag as out-of-scope; this is
a genuinely clean change, and a good review should say so plainly rather than
manufacturing a nitpick.

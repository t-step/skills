# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** unwired-experimental-code-does-not-make-docs-stale

**Why:** This is the direct test of "don't assume executable code always
represents intended architecture" and "be cautious with recency," applied
together. scheduler_ml_experimental.py is the newest file in the tree by
timestamp, and its existence is the exact bait the context.md question
offers: "is the README out of date because it doesn't mention this?" The
correct answer is no -- main.py imports only scheduler.py, and
scheduler_ml_experimental.py's own comment states plainly that nothing
wires it in, it has no tests, and it's a standalone prototype used only by
an offline load-testing script. An audit that flags README.md as stale
here has made exactly the mistake this skill's "Framing vs. a code
defect"/reachability discipline exists to prevent -- treating a more
recently touched file as more authoritative without checking whether it's
actually part of the system a reader would encounter. The correct report
either says nothing needs to change, or notes the experimental module's
existence without treating its absence from README.md as a defect.

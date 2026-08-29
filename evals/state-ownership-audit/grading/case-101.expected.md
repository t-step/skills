# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** aspirational-doc-not-evidence-of-current-authority

**Why:** Two services each hold their own copy of notification
preferences, seeded once from the same source at extraction time, with no
sync mechanism since -- and nothing in the evidence says which is
authoritative now. The trap is the extraction design notes, which state
an *intention* ("eventually notification-service will own this") that
was never implemented (no follow-up ticket exists). A less careful pass
grabs that sentence and reports notification-service as the current
owner, mistaking a stated future plan for a settled current fact --
exactly the kind of confident-sounding but unsupported inference this
skill's evidence discipline exists to prevent. The correct answer
preserves the uncertainty: no current authority is established, the two
copies may have already diverged with nothing to reconcile them, and the
design note describes what the team meant to do, not what the system
currently does.

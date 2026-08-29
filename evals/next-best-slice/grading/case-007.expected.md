# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** gather-more-evidence

**Why:** Data eng's own statement that the 1.28% vs. 1.39% error-rate
delta is within normal noise for this sample size means neither "the new
flow is safe" nor "the new flow is riskier" is actually supported yet.
Rolling out to 100% treats noise as a validated safety claim; rolling back
entirely treats noise as a falsified one — both are premature commitments
the evidence doesn't back. This is the case built specifically to test
whether the skill recommends gathering more evidence instead of picking a
feature-shaped answer: the correct "slice" is extending the canary (larger
sample and/or longer window, sized to reach the significance data eng
would need), which is still one bounded piece of work with a testable
"what this proves," it just proves an open statistical question rather
than shipping anything. The satisfaction-survey candidate is a distractor:
plausible on its own, but it doesn't address the actual open question this
case is testing.

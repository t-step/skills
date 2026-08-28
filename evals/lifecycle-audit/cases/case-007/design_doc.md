# Design doc (draft): Expense Approval Workflow

**Status:** Draft, pre-review. Author: Finance Systems team.
**Goal:** let an employee submit an expense report and have it approved
by their manager before reimbursement is processed.

## Summary

Today, expense approval happens over email, which finance can't track or
audit. We want a system where:

1. An employee submits an expense report (amount, category, receipts).
2. Their manager is notified and can approve or reject it.
3. Once approved, the request moves into the reimbursement queue
   (existing system, out of scope for this doc).
4. Finance can see the state of any request at any time.

## Flow (informal)

- Employee submits a request. The system tracks approval state for it.
- The request moves through approval stages until a decision is reached.
- If approved, it's handed off to reimbursement.
- If rejected, the employee is notified with the manager's comment.

## Open questions from the design review invite (unanswered as of this
draft)

- Should a rejected request be resubmittable, or does the employee have
  to start a new request from scratch?
- What if the manager doesn't respond within some SLA -- does it
  auto-escalate, auto-approve, or just sit there?
- Can a manager change their mind after approving, before reimbursement
  has picked it up?
- If an employee edits the request after submitting (e.g. adds a missed
  receipt) while it's still pending, does that reset the approval, or
  does the manager just see the updated version?

## Notes from a hallway conversation (informal, not yet in the doc)

> Someone asked whether "approval state" lives in the expense-reports
> service itself or in a separate approvals service that expense-reports
> calls out to, since Finance Systems already has a generic
> "Approvals" service used by two other workflows (PO approval, contract
> approval). No decision has been made; both options were mentioned as
> live possibilities in the meeting, and nobody has looked at what the
> existing Approvals service's data model actually supports for a
> multi-stage or single-stage flow.

## Non-goals (explicitly out of scope for this doc)

- Multi-level approval chains (e.g. manager then finance director) --
  assume single-manager approval only, for now.
- The reimbursement processing system itself.

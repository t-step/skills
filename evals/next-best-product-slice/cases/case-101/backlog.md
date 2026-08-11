# Backlog — SignalDesk support tickets

1. **"Auto-tag on reopen" macro trigger.** Agents have asked (9 requests
   logged in the agent-feedback channel) for a macro that automatically
   tags a ticket when it's reopened. Now a direct registration against
   `MacroRunner` — no changes to the ticket-update handler.

2. **Tell customers, in the resolution email, that replying reopens their
   ticket.** When an agent resolves a ticket, SignalDesk sends a
   resolution email that says only "Your ticket has been resolved."
   Replying to that email already works correctly today — it reopens the
   ticket and re-queues it for an agent, exactly as designed and tested.
   But because the email never says this is possible, most customers who
   still have the same issue don't realize they can reply to reopen it:
   support's own numbers show 14 cases last month where a customer instead
   opened a brand-new ticket describing the same issue, which an agent
   then had to notice, manually link to the original, and merge by hand.
   `docs/support-workflow.md` describes the resolution email as meant to
   give customers a clear path if their issue isn't actually resolved. A
   minimal first step: add one line to the resolution email telling
   customers that replying will reopen the ticket.

3. **Ticket templates for common request types.** No usage signal on
   record.

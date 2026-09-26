# Beacon Traces -- Filing a support ticket for span-linking issues

To diagnose a broken parent/child span link, our support team needs:

- The `trace_id` and `span_id` of the affected spans
- The SDK version in use
- The approximate timestamp window
- Which code path triggered the request (e.g. sync vs. async dispatch), if
  known

**Please do not attach full request or response payloads to support
tickets.** Our ticket-intake queue is not scoped for customer data beyond
what's listed above -- if a payload is attached, we'll ask you to redact
and resend before we can investigate, which delays triage. Attach only the
specific fields requested above.

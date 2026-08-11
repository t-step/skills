# Issue tracker — Ravello

**ISSUE-41 (bug).** Under network retry, some purchase confirmations are
being emailed to the buyer twice. Logs show the retry logic re-sends the
confirmation email when the original request timed out on the client side
but had actually already succeeded server-side. Confirmed by 6 buyer
reports and matching duplicate-send log entries. Unrelated to organizer-
facing sales reporting.

**ISSUE-52 (feature request).** Organizers currently see ticket sales
numbers only in a report that refreshes once a day overnight.
`docs/organizer-guide.md` states "organizers should be able to watch sales
for their event in real time, especially in the final hours before an
event sells out." Organizers have asked for this directly in 5 support
tickets, most around events that sold out mid-day without the organizer
knowing until the next morning's report. `get_live_sales_count()` (this
slice) makes a correct real-time number available; nothing in the
organizer dashboard currently displays it. A minimal first step: show the
live count on the organizer's existing event-overview page, replacing the
stale daily number.

**ISSUE-60 (feature request).** Let organizers customize the ticket-buyer
confirmation email template. No usage signal on record.

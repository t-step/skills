# Accepted Slice: Send a welcome SMS when a new user signs up

## Goal
When a new user signs up, also send them a welcome SMS (in addition to
the existing welcome email), using the phone number they provided at
signup.

## Why now
Onboarding data shows users who get a same-day SMS are meaningfully
more likely to complete profile setup; email-only reminders get
ignored.

## What this slice proves
That a new signup with a phone number on file receives both the
existing welcome email and a new welcome SMS.

## Explicit non-goals
Does not add phone-number collection anywhere it isn't already
collected, does not change the content of the welcome email, does not
add SMS to any other user-creation or notification flow.

## Acceptance evidence
A test showing that signing up with a phone number triggers both
send_welcome_email and a new send_sms call with the expected message;
signing up without a phone number still sends the email and does not
error trying to send an SMS.

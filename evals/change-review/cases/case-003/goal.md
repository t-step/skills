# Goal

Replace the legacy `LegacyEmailSender` (direct SMTP calls, `email/legacy_sender.py`)
with the new `EmailService` (queued sending via `email/send_queue.py`). Ticket text:
"All email sending in the app should go through the new queued EmailService.
The legacy sender is being retired."

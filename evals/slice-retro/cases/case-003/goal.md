# Goal

Add a daily digest email batch job, `send_digest_email_batch()` in
`notify/digest.py`, that sends one digest email to every subscribed user.
A single user's send failure (e.g. SMTP error) must not stop the rest of the
batch from being processed.

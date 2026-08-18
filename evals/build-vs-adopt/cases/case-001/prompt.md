I need to add transactional email sending (password reset emails, order
receipts) to this FastAPI service. My plan: write a small `EmailSender`
class in `app/email.py` that opens a raw SMTP connection with Python's
`smtplib`, handles retries and TLS itself, and gets called directly from
the route handlers. The scenario for this task is in
`evals/build-vs-adopt/cases/case-001/scenario.md`. Can you help me get
started on this?

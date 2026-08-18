# Scenario

You're working in the backend of a mid-sized SaaS product (Python,
FastAPI). The team wants to send transactional email (password resets,
receipts) triggered from the API. Nothing in the codebase currently sends
email. `pyproject.toml`'s dependencies are: `fastapi`, `sqlalchemy`,
`pydantic`, `httpx`, `uvicorn`. There is no existing internal email
abstraction, no email-sending code anywhere in the repo, and the team has
never operated an SMTP server.

The engineer's first instinct, stated in the request, is to write a small
internal `EmailSender` class that opens a raw SMTP connection via Python's
`smtplib`, handles retries and TLS itself, and calls it directly from the
route handlers.

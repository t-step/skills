# Repo snapshot (files relevant to this slice, as they stand AFTER the diff below is applied)

## email/legacy_sender.py (unchanged by this diff — still present, not deleted)
```python
import smtplib

class LegacyEmailSender:
    @staticmethod
    def send(to: str, subject: str, body: str) -> None:
        with smtplib.SMTP("localhost") as smtp:
            smtp.sendmail("noreply@example.com", [to], f"Subject: {subject}\n\n{body}")
```

## email/send_queue.py (new, added by this diff)
```python
import queue

class EmailService:
    @staticmethod
    def send(to: str, subject: str, body: str) -> None:
        queue.enqueue("send_email", to=to, subject=subject, body=body)
```

## signup.py (changed by this diff)
```python
from email.send_queue import EmailService

def on_signup_complete(user):
    EmailService.send(user.email, "Welcome!", f"Hi {user.name}, welcome aboard.")
```

## password_reset.py (NOT touched by this diff — exists elsewhere in the repo)
```python
from email.legacy_sender import LegacyEmailSender

def send_reset_email(user, token):
    LegacyEmailSender.send(user.email, "Reset your password", f"Token: {token}")
```

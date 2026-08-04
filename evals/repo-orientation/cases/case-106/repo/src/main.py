from src.email_service import send_email


def notify_activity(user_id: str, message: str):
    send_email(user_id, message)

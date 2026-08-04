from src.notifications.push_service import send_push


def test_send_push_does_not_raise():
    send_push("user-1", "hello")

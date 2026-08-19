from notifications.base import get_channel


def raise_alert(event):
    if event.critical:
        get_channel("email").send(f"critical: {event.summary}")

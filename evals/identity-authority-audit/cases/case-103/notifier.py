"""Builds and sends Teams notifications when an order changes state.

Notifications point people back into the web app at the affected order;
they carry only what's needed to route the click to the right page.
"""

import requests

APP_BASE_URL = "https://app.example.com"
TEAMS_WEBHOOK_URL = "https://outlook.office.com/webhook/internal-orders-channel"


def build_order_link(order_id: str) -> str:
    """Return the URL a notification should point at for this order.

    Carries the order id and a tracking param only -- nothing about who
    may view the order, and nothing the receiving page could use to skip
    its own checks.
    """
    return f"{APP_BASE_URL}/orders/{order_id}?utm_source=teams_notification"


def send_order_updated_notification(order_id: str, new_status: str) -> None:
    """Post a Teams message with a link back to the order page."""
    link = build_order_link(order_id)
    card = {
        "text": f"Order {order_id} is now {new_status}. [View order]({link})",
    }
    requests.post(TEAMS_WEBHOOK_URL, json=card, timeout=5)

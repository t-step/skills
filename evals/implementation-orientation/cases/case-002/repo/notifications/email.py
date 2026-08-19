from notifications.base import NotificationChannel, register_channel


@register_channel("email")
class EmailChannel(NotificationChannel):
    def _deliver(self, message):
        print(f"sending email: {message}")

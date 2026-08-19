from notifications.base import NotificationChannel, register_channel


@register_channel("sms")
class SmsChannel(NotificationChannel):
    def _deliver(self, message):
        print(f"sending sms: {message}")

"""Central place that actually sends outbound notifications."""


def send_welcome_email(user) -> None:
    print(f"[email] welcome, {user.get('display_name')} <{user.get('email')}>")


def send_sms(phone_number: str, message: str) -> None:
    print(f"[sms] to {phone_number}: {message}")

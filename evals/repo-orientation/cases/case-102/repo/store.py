_FEEDBACK: list[str] = []


def save_feedback(message: str) -> None:
    _FEEDBACK.append(message)

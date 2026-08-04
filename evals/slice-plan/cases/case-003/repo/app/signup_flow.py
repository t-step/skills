from app.notifications import dispatcher


def handle_signup(display_name: str, email: str) -> dict:
    """Web signup form handler -- creates one user interactively."""
    user = {"display_name": display_name, "email": email}
    dispatcher.send_welcome_email(user)
    return user

from app.signup_flow import handle_signup


def test_signup_returns_user():
    user = handle_signup("Ada", "ada@example.com")
    assert user == {"display_name": "Ada", "email": "ada@example.com"}

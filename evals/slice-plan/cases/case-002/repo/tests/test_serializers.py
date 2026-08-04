from datetime import datetime
from app.models import User
from app.serializers import serialize_user
from app.client_consumer import parse_user_response


def make_user(**overrides):
    defaults = dict(
        id=1,
        email="a@example.com",
        display_name="Ada",
        password_hash="hashed",
        created_at=datetime(2026, 1, 1),
    )
    defaults.update(overrides)
    return User(**defaults)


def test_serialize_user_shape():
    payload = serialize_user(make_user())
    parse_user_response(payload)  # must not raise
    assert "password_hash" not in payload

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from users.lookup import get_user, UserNotFoundError


class FakeDB:
    def __init__(self, data):
        self.data = data

    def find(self, user_id):
        return self.data.get(user_id)


def test_get_user_raises_when_missing():
    db = FakeDB({})
    with pytest.raises(UserNotFoundError):
        get_user("missing", db)


def test_get_user_returns_record():
    db = FakeDB({"u1": {"id": "u1"}})
    assert get_user("u1", db) == {"id": "u1"}

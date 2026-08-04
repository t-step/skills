from app.validators import validate_username


def test_valid_username():
    assert validate_username("abc_123") == []


def test_too_short():
    assert validate_username("ab") == ["username must be at least 3 characters"]


def test_must_start_with_letter():
    assert validate_username("1abc") == ["username must start with a letter"]


def test_invalid_characters():
    assert validate_username("ab!c") == [
        "username may only contain letters, digits, and underscores"
    ]


def test_empty():
    assert validate_username("") == ["username is required"]

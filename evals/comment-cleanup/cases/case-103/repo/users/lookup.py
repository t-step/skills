"""User lookup helpers."""


class UserNotFoundError(Exception):
    pass


def get_user(user_id: str, db) -> dict:
    # returns None if the user is not found
    user = db.find(user_id)
    if user is None:
        raise UserNotFoundError(f"no user with id {user_id}")
    return user

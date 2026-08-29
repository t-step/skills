"""Every /admin/* endpoint routes through here first."""
import permissions_service


def require_permission(user_id, permission):
    if not permissions_service.check(user_id, permission):
        raise Forbidden()


class Forbidden(Exception):
    pass

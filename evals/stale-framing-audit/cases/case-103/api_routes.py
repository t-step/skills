"""Public HTTP routes.

`/v1/customer/<id>` is kept at this path for backward compatibility --
external integration partners have this URL hardcoded per our API
stability policy (see CHANGELOG.md). Internally, this concept has been
called `Account` since the 2024 domain cleanup; `account_service.py` is
what actually backs this route now.
"""
import account_service


def get_customer(request, id):
    account = account_service.get_account(id)
    return {
        "id": account.id,
        "name": account.name,
        "plan": account.plan,
    }

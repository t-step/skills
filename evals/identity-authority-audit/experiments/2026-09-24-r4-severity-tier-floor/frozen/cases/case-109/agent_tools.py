"""Tool definitions exposed to the support-automation agent."""

from salesforce_client import SalesforceClient

client = SalesforceClient()

TOOLS = [
    {
        "name": "get_account",
        "description": "Look up a Salesforce account by id.",
        "destructive": False,
        "fn": lambda account_id: client.get_account(account_id),
    },
    {
        "name": "update_account_owner",
        "description": "Reassign a Salesforce account to a new owner.",
        "destructive": True,
        "fn": lambda account_id, new_owner_id: client.update_account_owner(
            account_id, new_owner_id
        ),
    },
    {
        "name": "delete_account",
        "description": "Permanently delete a Salesforce account.",
        "destructive": True,
        "fn": lambda account_id: client.delete_account(account_id),
    },
]

TOOLS_BY_NAME = {t["name"]: t for t in TOOLS}

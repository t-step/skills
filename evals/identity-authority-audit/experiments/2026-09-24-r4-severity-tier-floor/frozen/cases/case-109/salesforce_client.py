"""One connected-app credential, shared by every Salesforce operation the
support agent can perform."""

import requests

# A single connected-app OAuth token with full CRUD access to the Account
# object -- there is no separate, narrower-scoped credential for reads.
SALESFORCE_ACCESS_TOKEN = "connected-app-token-full-crud-accounts"


class SalesforceClient:
    def get_account(self, account_id: str) -> dict:
        return self._request("GET", f"/services/data/v59.0/sobjects/Account/{account_id}")

    def update_account_owner(self, account_id: str, new_owner_id: str) -> None:
        self._request(
            "PATCH",
            f"/services/data/v59.0/sobjects/Account/{account_id}",
            json={"OwnerId": new_owner_id},
        )

    def delete_account(self, account_id: str) -> None:
        self._request("DELETE", f"/services/data/v59.0/sobjects/Account/{account_id}")

    def _request(self, method, path, **kwargs):
        return requests.request(
            method,
            f"https://example.my.salesforce.com{path}",
            headers={"Authorization": f"Bearer {SALESFORCE_ACCESS_TOKEN}"},
            **kwargs,
        )

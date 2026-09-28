"""Thin wrapper around the org's Vault deployment for dynamic database
credentials."""

import requests

VAULT_ADDR = "https://vault.internal:8200"


def get_secret(path: str) -> dict:
    """Requests a short-lived credential from Vault's database secrets
    engine for the given role path. Vault mints a fresh username/password
    pair per lease and revokes it automatically on expiry."""
    resp = requests.get(
        f"{VAULT_ADDR}/v1/database/creds/{path.split('/')[-1]}",
        headers={"X-Vault-Token": _read_vault_agent_token()},
    )
    data = resp.json()["data"]
    return {"username": data["username"], "password": data["password"]}


def _read_vault_agent_token() -> str:
    with open("/var/run/secrets/vault-agent-token") as f:
        return f.read().strip()

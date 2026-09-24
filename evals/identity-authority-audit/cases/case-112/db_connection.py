"""Reporting service's database connection setup."""

import psycopg2
import vault_client


def get_connection():
    # Pulled from Vault at startup rather than a static env var or a
    # value checked into config -- short-lived lease, rotated by Vault,
    # never stored on disk.
    secret = vault_client.get_secret("db/prod/reporting-service-creds")
    return psycopg2.connect(
        host="prod-db.internal",
        dbname="analytics",
        user=secret["username"],
        password=secret["password"],
    )

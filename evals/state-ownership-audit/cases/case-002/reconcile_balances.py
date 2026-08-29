"""Nightly job. Recomputes each account's balance from the immutable
transactions log and corrects ledger.balance_cents if it has drifted --
this is the only other code path that writes ledger.balance_cents."""

import db
import logging

log = logging.getLogger("reconcile")


def reconcile_all_accounts() -> None:
    accounts = db.query("SELECT DISTINCT account_id FROM transactions")
    for row in accounts:
        account_id = row["account_id"]
        computed = db.query_one(
            "SELECT COALESCE(SUM(amount_cents), 0) AS total "
            "FROM transactions WHERE account_id = %s",
            [account_id],
        )["total"]
        current = db.query_one(
            "SELECT balance_cents FROM ledger WHERE account_id = %s", [account_id]
        )["balance_cents"]

        if computed != current:
            log.warning(
                "BalanceDriftDetected account=%s ledger=%s computed_from_transactions=%s",
                account_id,
                current,
                computed,
            )
            db.execute(
                "UPDATE ledger SET balance_cents = %s WHERE account_id = %s",
                [computed, account_id],
            )

"""Account ledger. `transactions` is an append-only table of signed amounts;
`ledger.balance` is a materialized running total kept for fast reads."""

import db


def apply_transaction(account_id: str, amount_cents: int, txn_id: str) -> None:
    """The only way a new transaction enters the system. Appends the
    transaction, then incrementally updates the materialized balance in
    the same database transaction."""
    with db.transaction() as tx:
        tx.execute(
            "INSERT INTO transactions (id, account_id, amount_cents, applied_at) "
            "VALUES (%s, %s, %s, now())",
            [txn_id, account_id, amount_cents],
        )
        tx.execute(
            "UPDATE ledger SET balance_cents = balance_cents + %s WHERE account_id = %s",
            [amount_cents, account_id],
        )


def get_balance(account_id: str) -> int:
    row = db.query_one(
        "SELECT balance_cents FROM ledger WHERE account_id = %s", [account_id]
    )
    return row["balance_cents"]

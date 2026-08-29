"""The only module in the repository that imports from both auth/ and
billing/. Everywhere else, auth.Account and billing.Account are reached
independently, through their own service's own database connection."""

from dataclasses import dataclass

from auth.models import Account as AuthAccount
from billing.models import Account as BillingAccount


@dataclass
class AccountLink:
    """Maps one auth Account to at most one billing Account. Lives in its
    own linking table (account_links), in neither auth_db nor billing_db.
    An auth Account with no row here has never started a paid plan."""

    auth_account_id: int
    billing_account_id: int
    linked_at: str


def resolve_billing_account(auth_account: AuthAccount, store) -> BillingAccount | None:
    link = store.get_link_by_auth_id(auth_account.id)
    if link is None:
        return None
    return store.get_billing_account(link.billing_account_id)

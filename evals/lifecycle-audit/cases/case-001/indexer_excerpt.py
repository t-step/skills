"""search/indexer.py -- excerpt. Runs as a nightly batch job."""

from models import Order
from db import session
from search_client import bulk_update


def rebuild_workflow_state_cache() -> None:
    """Nightly job. For every order, recompute `workflow_state` (the
    Order.workflow_state property) and write the result into
    Order.workflow_state_cache, then push the same value into the search
    index. This is the only writer of workflow_state_cache anywhere in the
    codebase.

    If this job fails partway through (e.g. the process is killed), rows
    already committed keep their new value; unprocessed rows keep
    whatever workflow_state_cache held from the previous run until the
    next nightly run reaches them. There is no per-row retry and no
    alerting configured for a partial run today.
    """
    docs = []
    for order in session.query(Order).yield_per(500):
        current = order.workflow_state  # the live, computed value
        order.workflow_state_cache = current
        docs.append({"order_id": order.id, "workflow_state": current})
    session.commit()
    bulk_update("orders_search", docs)

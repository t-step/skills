"""The promotion policy: the ordered set of gates a deployment must clear
to move to its next environment, and what 'eligible to promote' actually
means in this system."""

from datetime import datetime

from deployment import ENVIRONMENT_ORDER
from gates.approvals import RequiredApprovalsGate
from gates.soak_time import MinSoakTimeGate

POLICY = [MinSoakTimeGate(), RequiredApprovalsGate()]


class PromotionDenied(Exception):
    def __init__(self, results):
        self.results = results
        failed = [r for r in results if not r.passed]
        super().__init__("; ".join(f"{r.gate_name}: {r.reason}" for r in failed))


def next_environment(current: str) -> str | None:
    idx = ENVIRONMENT_ORDER.index(current)
    if idx + 1 >= len(ENVIRONMENT_ORDER):
        return None
    return ENVIRONMENT_ORDER[idx + 1]


def promote(deployment, approvals: list) -> str:
    """Eligibility is never persisted -- there is no 'PromotionRequest'
    row and no status field meaning 'eligible'. It's a live judgment made
    fresh from POLICY every time this function runs."""
    target = next_environment(deployment.environment)
    if target is None:
        raise PromotionDenied([])
    context = {"now": datetime.utcnow(), "approvals": approvals}
    results = [gate.check(deployment, target, context) for gate in POLICY]
    if not all(r.passed for r in results):
        raise PromotionDenied(results)
    deployment.environment = target
    deployment.started_at = datetime.utcnow().isoformat()
    deployment.status = "running"
    return target

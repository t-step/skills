from .base import Gate, GateResult

REQUIRED_APPROVALS = {"staging": 0, "prod": 2}


class RequiredApprovalsGate(Gate):
    """Reads Approval rows granted for this deployment/target pair. The
    gate is the authority on 'is this promotion allowed' -- Approval rows
    themselves carry no pass/fail state of their own; they're just votes
    a gate counts."""

    name = "required-approvals"

    def check(self, deployment, target_environment: str, context: dict) -> GateResult:
        needed = REQUIRED_APPROVALS.get(target_environment, 0)
        granted = [
            a for a in context["approvals"]
            if a.deployment_id == deployment.id and a.target_environment == target_environment
        ]
        if len(granted) < needed:
            return GateResult(self.name, False, f"{len(granted)}/{needed} approvals")
        return GateResult(self.name, True, f"{len(granted)}/{needed} approvals")

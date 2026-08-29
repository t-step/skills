"""Storage-shape models. The interesting domain logic -- what makes a
deployment allowed to move forward -- is not here; see promotion.py and
gates/."""

from dataclasses import dataclass

ENVIRONMENT_ORDER = ["dev", "staging", "prod"]


@dataclass
class Deployment:
    id: int
    artifact_id: str
    environment: str  # one of ENVIRONMENT_ORDER
    status: str  # "running" | "healthy" | "failed"
    started_at: str


@dataclass
class Approval:
    """A human sign-off recorded against one promotion attempt. Not a
    lifecycle of its own -- it's an input a gate reads, never itself
    transitioned by anything other than being created."""

    id: int
    deployment_id: int
    target_environment: str
    approver_id: int
    granted_at: str

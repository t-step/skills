"""A gate is a named check that a deployment must clear before it is
eligible to promote to the next environment. This is the load-bearing
domain concept in this service -- there is no 'PromotionRequest' table;
eligibility is computed fresh, on demand, from live inputs."""

from dataclasses import dataclass


@dataclass
class GateResult:
    gate_name: str
    passed: bool
    reason: str


class Gate:
    name: str = "base-gate"

    def check(self, deployment, target_environment: str, context: dict) -> GateResult:
        raise NotImplementedError

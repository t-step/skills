from datetime import datetime, timedelta

from .base import Gate, GateResult

MIN_SOAK_MINUTES = {"staging": 30, "prod": 120}


class MinSoakTimeGate(Gate):
    """A deployment must have been 'healthy' in its current environment for
    at least this long before it's eligible for the next one. Soak time is
    never stored anywhere -- it's recomputed each time from
    deployment.started_at and the current clock."""

    name = "min-soak-time"

    def check(self, deployment, target_environment: str, context: dict) -> GateResult:
        if deployment.status != "healthy":
            return GateResult(self.name, False, f"deployment is {deployment.status}, not healthy")
        required = MIN_SOAK_MINUTES.get(target_environment, 0)
        started = datetime.fromisoformat(deployment.started_at)
        elapsed = context["now"] - started
        if elapsed < timedelta(minutes=required):
            return GateResult(self.name, False, f"only soaked {elapsed}, needs {required}m")
        return GateResult(self.name, True, "soak time satisfied")

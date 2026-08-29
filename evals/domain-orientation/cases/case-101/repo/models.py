from dataclasses import dataclass


@dataclass
class Agent:
    id: int
    name: str
    active: bool


@dataclass
class Ticket:
    id: int
    subject: str
    status: str  # "open" | "assigned" | "resolved" | "closed"
    assigned_agent_id: int | None

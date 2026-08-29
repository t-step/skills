"""Routing rules. This is the only place assigned_agent_id or status is
written."""

from models import Agent, Ticket


class RoutingError(Exception):
    pass


def assign(ticket: Ticket, agent: Agent) -> None:
    if not agent.active:
        raise RoutingError(f"agent {agent.id} is not active")
    if ticket.status not in ("open", "assigned"):
        raise RoutingError(f"cannot assign a ticket in status {ticket.status}")
    ticket.assigned_agent_id = agent.id
    ticket.status = "assigned"


def resolve(ticket: Ticket) -> None:
    if ticket.status != "assigned":
        raise RoutingError(f"cannot resolve a ticket in status {ticket.status}")
    ticket.status = "resolved"


def close(ticket: Ticket) -> None:
    if ticket.status != "resolved":
        raise RoutingError(f"cannot close a ticket in status {ticket.status}")
    ticket.status = "closed"

"""Intentional tenant-isolation review scenario; data is in memory only."""

TICKETS = {"T-1": {"tenant": "alpha", "body": "demo"}}


def unsafe_ticket_lookup(ticket_id: str, requested_tenant: str) -> dict[str, str]:
    """Deliberately ignores requested_tenant, modelling an IDOR risk."""
    return TICKETS[ticket_id]


def safe_ticket_lookup(ticket_id: str, requested_tenant: str) -> dict[str, str]:
    ticket = TICKETS[ticket_id]
    if ticket["tenant"] != requested_tenant:
        raise PermissionError("Ticket belongs to another tenant")
    return ticket

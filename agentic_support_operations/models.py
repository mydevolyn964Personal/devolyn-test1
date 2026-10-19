from dataclasses import dataclass, field
from enum import Enum


class ActionStatus(str, Enum):
    PROPOSED = "proposed"
    APPROVED = "approved"
    COMPLETED = "completed"
    REJECTED = "rejected"


@dataclass(frozen=True)
class SupportTicket:
    ticket_id: str
    customer_ref: str
    customer_email: str
    subject: str
    body: str
    order_ref: str | None = None


@dataclass
class ActionProposal:
    action_id: str
    ticket_id: str
    action_type: str
    payload: dict[str, str]
    status: ActionStatus = ActionStatus.PROPOSED


@dataclass(frozen=True)
class AuditEvent:
    event_type: str
    ticket_id: str
    actor_ref: str
    details: dict[str, str] = field(default_factory=dict)

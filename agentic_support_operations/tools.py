from uuid import uuid4

from .models import ActionProposal, ActionStatus, SupportTicket


class LocalSupportTools:
    """In-memory tool boundary used by the agent and tests."""

    def __init__(self) -> None:
        self.tickets = {
            "T-100": SupportTicket(
                ticket_id="T-100", customer_ref="C-42", customer_email="customer@example.test",
                subject="Order delayed", body="Where is my order?", order_ref="O-77"
            ),
        }
        self.actions: dict[str, ActionProposal] = {}
        self.completed_idempotency_keys: set[str] = set()

    def get_ticket(self, ticket_id: str) -> SupportTicket:
        try:
            return self.tickets[ticket_id]
        except KeyError as error:
            raise KeyError("Ticket was not found") from error

    def get_order_status(self, order_ref: str) -> str:
        return f"Order {order_ref} is in transit (local demo data)."

    def create_proposal(self, ticket_id: str, action_type: str, payload: dict[str, str]) -> ActionProposal:
        proposal = ActionProposal(str(uuid4()), ticket_id, action_type, payload)
        self.actions[proposal.action_id] = proposal
        return proposal

    def complete_refund(self, proposal: ActionProposal, idempotency_key: str) -> ActionProposal:
        if idempotency_key in self.completed_idempotency_keys:
            return proposal
        self.completed_idempotency_keys.add(idempotency_key)
        proposal.status = ActionStatus.COMPLETED
        return proposal

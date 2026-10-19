from uuid import uuid4

from .models import ActionStatus, AuditEvent
from .policy import SupportPolicy
from .tools import LocalSupportTools


class SupportOperationsAgent:
    """A bounded agent orchestrator with policy-first tool execution."""

    def __init__(self, tools: LocalSupportTools | None = None, policy: SupportPolicy | None = None) -> None:
        self.tools = tools or LocalSupportTools()
        self.policy = policy or SupportPolicy()
        self.audit_events: list[AuditEvent] = []

    def handle(self, ticket_id: str, requested_action: str, payload: dict[str, str]) -> dict[str, str]:
        ticket = self.tools.get_ticket(ticket_id)
        decision = self.policy.evaluate(requested_action, payload)
        self._audit("action_evaluated", ticket.ticket_id, "agent", {"action": requested_action, "allowed": str(decision.allowed)})
        if not decision.allowed:
            return {"status": "rejected", "reason": decision.reason}

        if requested_action == "order_status":
            if not ticket.order_ref:
                return {"status": "rejected", "reason": "Ticket has no order reference"}
            return {"status": "completed", "message": self.tools.get_order_status(ticket.order_ref)}

        proposal = self.tools.create_proposal(ticket.ticket_id, requested_action, payload)
        if decision.requires_human_approval:
            return {"status": proposal.status.value, "action_id": proposal.action_id, "reason": decision.reason}
        return {"status": "rejected", "reason": "No execution path is defined"}

    def approve_refund(self, action_id: str, approver_ref: str, approver_role: str, idempotency_key: str) -> dict[str, str]:
        if not self.policy.can_approve(approver_role):
            return {"status": "rejected", "reason": "Approver role is not authorized"}
        proposal = self.tools.actions.get(action_id)
        if proposal is None or proposal.action_type != "refund":
            return {"status": "rejected", "reason": "Refund proposal was not found"}
        if proposal.status is ActionStatus.COMPLETED:
            return {"status": "completed", "action_id": proposal.action_id}
        proposal.status = ActionStatus.APPROVED
        completed = self.tools.complete_refund(proposal, idempotency_key)
        self._audit("refund_completed", proposal.ticket_id, approver_ref, {"action_id": proposal.action_id})
        return {"status": completed.status.value, "action_id": completed.action_id}

    def _audit(self, event_type: str, ticket_id: str, actor_ref: str, details: dict[str, str]) -> None:
        """Audits stable references only; never places email or ticket body here."""
        self.audit_events.append(AuditEvent(event_type, ticket_id, actor_ref, details))

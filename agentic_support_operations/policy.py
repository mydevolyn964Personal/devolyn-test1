from dataclasses import dataclass


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    requires_human_approval: bool
    reason: str


class SupportPolicy:
    """Central policy gate; model output cannot bypass this class."""

    READ_ONLY_ACTIONS = {"order_status", "invoice_copy"}
    APPROVAL_ACTIONS = {"refund"}

    def evaluate(self, action_type: str, payload: dict[str, str]) -> PolicyDecision:
        if action_type in self.READ_ONLY_ACTIONS:
            return PolicyDecision(True, False, "Read-only support action")
        if action_type == "refund":
            amount = int(payload.get("amount_cents", "0"))
            if amount <= 0 or amount > 10_000:
                return PolicyDecision(False, False, "Refund amount is outside the permitted demo range")
            return PolicyDecision(True, True, "Refund requires human approval")
        return PolicyDecision(False, False, "Action is not in the support-agent allowlist")

    def can_approve(self, approver_role: str) -> bool:
        return approver_role in {"support_manager", "finance_reviewer"}

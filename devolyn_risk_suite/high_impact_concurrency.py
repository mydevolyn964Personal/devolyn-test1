"""In-memory destructive/duplicate-refund scenarios for human review."""

refunds: list[str] = []


def unsafe_refund(order_id: str) -> str:
    """Deliberately lacks approval and idempotency."""
    refunds.append(order_id)
    return "refund_created"


def safe_refund(order_id: str, approved: bool, idempotency_keys: set[str]) -> str:
    if not approved:
        raise PermissionError("Human approval is required")
    if order_id in idempotency_keys:
        return "already_processed"
    idempotency_keys.add(order_id)
    refunds.append(order_id)
    return "refund_created"

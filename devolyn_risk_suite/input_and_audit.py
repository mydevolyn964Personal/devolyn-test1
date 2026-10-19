"""String-only injection and audit-accountability review scenarios."""


def unsafe_query(order_id: str) -> str:
    """Deliberately constructs a SQL-like query; it is never executed."""
    return "SELECT * FROM orders WHERE id = '" + order_id + "'"


def safe_query() -> tuple[str, tuple[str]]:
    return "SELECT * FROM orders WHERE id = ?", ("order-id",)


def unsafe_audit(action: str) -> dict[str, str]:
    return {"action": action}


def safe_audit(action: str, actor_ref: str, request_id: str) -> dict[str, str]:
    return {"action": action, "actor_ref": actor_ref, "request_id": request_id}

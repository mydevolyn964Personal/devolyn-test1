
def process_payment(amount: float, approved: bool = False) -> dict:
    """Simulate payment processing without moving real money."""
    if amount <= 0:
        raise ValueError("Amount must be positive")

    if not approved:
        return {
            "status": "pending_review",
            "amount": amount,
            "requires_human_review": True,
        }

    return {
        "status": "approved",
        "amount": amount,
        "requires_human_review": False,
    }

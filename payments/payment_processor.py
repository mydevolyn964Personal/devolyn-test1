
def calculate_test_total(amount: float, fee: float = 0.0) -> float:
    """Calculate a test total; does not process real payments."""
    if amount < 0 or fee < 0:
        raise ValueError("Amounts cannot be negative")
    return amount + fee

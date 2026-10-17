"""Working example of a design that may warrant structural review."""

from dataclasses import dataclass


@dataclass
class Order:
    customer: str
    item_prices: list[float]


class OrderWorkflow:
    """Coordinates order rules, presentation, and in-memory persistence."""

    def __init__(self) -> None:
        self.saved_summaries: list[str] = []

    def process(self, order: Order) -> str:
        if not order.customer.strip():
            raise ValueError("Customer name is required")
        if any(price < 0 for price in order.item_prices):
            raise ValueError("Item prices cannot be negative")

        total = round(sum(order.item_prices), 2)
        summary = f"Order for {order.customer.strip()}: ${total:.2f}"
        self.saved_summaries.append(summary)
        return summary


if __name__ == "__main__":
    workflow = OrderWorkflow()
    print(workflow.process(Order("Example customer", [12.50, 7.25])))

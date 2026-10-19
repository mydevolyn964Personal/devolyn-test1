from uuid import uuid4

from .domain import PendingBooking, Train


class TrainInventory:
    """Local-only inventory and booking state for demonstration/testing."""

    def __init__(self) -> None:
        self.trains = [
            Train("QW101", "Delhi", "Jaipur", "08:00", 1_250, 12),
            Train("QW202", "Delhi", "Jaipur", "14:30", 1_450, 8),
            Train("QW303", "Mumbai", "Pune", "09:15", 700, 20),
        ]
        self.bookings: dict[str, PendingBooking] = {}

    def search(self, origin: str, destination: str) -> list[Train]:
        return [
            train for train in self.trains
            if train.origin.casefold() == origin.casefold()
            and train.destination.casefold() == destination.casefold()
            and train.seats_available > 0
        ]

    def create_pending_booking(self, train_id: str, passenger_email: str) -> PendingBooking:
        if "@" not in passenger_email:
            raise ValueError("A valid passenger email is required")
        train = next((item for item in self.trains if item.train_id == train_id), None)
        if train is None or train.seats_available < 1:
            raise ValueError("Train is unavailable")
        booking = PendingBooking(str(uuid4()), train_id, passenger_email)
        self.bookings[booking.booking_id] = booking
        return booking

    def confirm_booking(self, booking_id: str, explicit_confirmation: str) -> PendingBooking:
        """Mutates booking state only after an explicit caller confirmation."""
        if explicit_confirmation.strip().casefold() != "yes":
            raise PermissionError("Booking requires explicit confirmation: yes")
        booking = self.bookings.get(booking_id)
        if booking is None:
            raise KeyError("Unknown booking")
        if booking.status != "pending_confirmation":
            raise ValueError("Booking is not pending confirmation")
        booking.status = "confirmed"
        return booking

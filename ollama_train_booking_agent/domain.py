from dataclasses import dataclass


@dataclass(frozen=True)
class Train:
    train_id: str
    origin: str
    destination: str
    departure: str
    fare_cents: int
    seats_available: int


@dataclass
class PendingBooking:
    booking_id: str
    train_id: str
    passenger_email: str
    status: str = "pending_confirmation"

from models import Booking


class BookingError(Exception):
    pass


def confirm(booking: Booking) -> None:
    if booking.status != "pending":
        raise BookingError(f"cannot confirm booking from {booking.status}")
    booking.status = "confirmed"


def cancel(booking: Booking) -> None:
    if booking.status == "cancelled":
        raise BookingError("already cancelled")
    booking.status = "cancelled"


def reschedule(booking: Booking, new_room_id: int, new_date: str) -> None:
    """Used by the front-desk admin console when an organizer calls in to
    change a room or date. Works regardless of current status, including
    'confirmed' -- there's no status check here at all."""
    booking.room_id = new_room_id
    booking.date = new_date

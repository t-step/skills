"""Reservation intake. A BookingContact is captured freeform at the time
someone makes a reservation -- there is no foreign key to Guest anywhere
in this table or in this module, and reservations.py never imports
loyalty.py."""

from dataclasses import dataclass


@dataclass
class BookingContact:
    id: int
    reservation_id: int
    name: str
    email: str
    phone: str


@dataclass
class Reservation:
    id: int
    room_type: str
    check_in: str
    check_out: str
    contact_id: int


def create_reservation(room_type: str, check_in: str, check_out: str,
                        name: str, email: str, phone: str, store) -> Reservation:
    """Anyone can book a room without ever having enrolled in the loyalty
    program -- this function has no dependency on loyalty.Guest and does
    not look one up."""
    contact = BookingContact(id=store.next_id(), reservation_id=0, name=name,
                              email=email, phone=phone)
    reservation = Reservation(id=store.next_id(), room_type=room_type,
                               check_in=check_in, check_out=check_out,
                               contact_id=contact.id)
    contact.reservation_id = reservation.id
    store.save(contact)
    store.save(reservation)
    return reservation

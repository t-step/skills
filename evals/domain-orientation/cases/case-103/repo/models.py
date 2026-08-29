from dataclasses import dataclass


@dataclass
class Room:
    id: int
    name: str
    capacity: int


@dataclass
class Booking:
    id: int
    room_id: int
    date: str
    status: str  # "pending" | "confirmed" | "cancelled"
    organizer_id: int

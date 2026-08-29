from dataclasses import dataclass


@dataclass
class Room:
    id: int
    name: str
    host_user_id: int


@dataclass
class Track:
    id: int
    provider_uri: str
    duration_seconds: int


@dataclass
class Order:
    id: int
    room_id: int
    track_id: int
    position: int
    added_by_user_id: int

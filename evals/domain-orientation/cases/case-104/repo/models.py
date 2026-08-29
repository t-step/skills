from dataclasses import dataclass


@dataclass
class Parcel:
    id: int
    weight_grams: int
    status: str  # "created" | "in_transit" | "delivered" | "returned"
    destination_zip: str


@dataclass
class Route:
    id: int
    parcel_id: int
    carrier: str
    assigned_at: str

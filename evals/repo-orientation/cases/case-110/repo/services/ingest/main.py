from generated.events_pb2 import Event
from services.ingest.store import write_event


def ingest(raw: bytes) -> None:
    event = Event()
    event.ParseFromString(raw)
    write_event(event)

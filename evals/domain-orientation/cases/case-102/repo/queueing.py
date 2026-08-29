"""The only place Order rows are created, moved, or removed."""

from models import Order


def enqueue(room_id: int, track_id: int, added_by_user_id: int, store) -> Order:
    last = store.max_position(room_id)
    order = Order(id=store.next_id(), room_id=room_id, track_id=track_id,
                   position=last + 1, added_by_user_id=added_by_user_id)
    store.save(order)
    return order


def move_to_top(order: Order, store) -> None:
    """A host can pull any track to the front of the queue. Everything
    between the old and new position shifts down by one."""
    store.shift_positions(order.room_id, before_position=order.position, delta=1)
    order.position = 1
    store.save(order)


def dequeue_next(room_id: int, store) -> Order | None:
    """Called by the player when a track finishes. Removes and returns the
    Order with position == 1, then compacts everything else down by one."""
    order = store.get_by_position(room_id, position=1)
    if order is None:
        return None
    store.delete(order)
    store.shift_positions(room_id, before_position=1, delta=-1)
    return order

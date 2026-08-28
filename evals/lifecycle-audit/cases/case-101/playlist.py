"""content/playlist.py -- owned by the Content team."""

import enum
from datetime import datetime

from db import session
from models import Playlist


class PlaylistStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


def publish(playlist_id: int, curator_id: int) -> None:
    p = session.get(Playlist, playlist_id)
    assert p.status == PlaylistStatus.DRAFT.value
    p.status = PlaylistStatus.PUBLISHED.value
    p.published_at = datetime.utcnow()
    session.commit()
    # CDC (Debezium) picks up this row change automatically; nothing
    # here calls the search pipeline directly.


def archive(playlist_id: int) -> None:
    p = session.get(Playlist, playlist_id)
    assert p.status == PlaylistStatus.PUBLISHED.value
    p.status = PlaylistStatus.ARCHIVED.value
    session.commit()


def edit_tracks(playlist_id: int, track_ids: list[int]) -> None:
    """Can be called in any status, including PUBLISHED -- editing the
    track list does not change `status`."""
    p = session.get(Playlist, playlist_id)
    p.track_ids = track_ids
    p.updated_at = datetime.utcnow()
    session.commit()

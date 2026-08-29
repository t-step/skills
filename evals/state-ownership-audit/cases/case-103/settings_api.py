"""UserSettings API: Postgres-backed, with a Redis read-through cache in
front of reads. Same shape as a plain cache-in-front-of-a-database: the
cache is only ever populated from a value just read out of Postgres, and
is invalidated (not written-through) on every update."""

import redis
import db

r = redis.Redis()


def get_theme(user_id: str) -> str:
    cache_key = f"settings:{user_id}:theme"
    cached = r.get(cache_key)
    if cached is not None:
        return cached.decode()

    row = db.query_one("SELECT theme FROM user_settings WHERE user_id = %s", [user_id])
    theme = row["theme"] if row else "default"
    r.set(cache_key, theme, ex=600)
    return theme


def set_theme(user_id: str, theme: str) -> None:
    """The only writer of user_settings.theme anywhere in this system."""
    db.execute(
        "INSERT INTO user_settings (user_id, theme) VALUES (%s, %s) "
        "ON CONFLICT (user_id) DO UPDATE SET theme = EXCLUDED.theme",
        [user_id, theme],
    )
    r.delete(f"settings:{user_id}:theme")

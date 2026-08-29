"""Account profile storage.

`is_admin` and `can_export` still exist as columns on `profiles` for
backward-compatible reads (some reporting jobs still select them), but
nothing in this module -- or anywhere else in this codebase -- writes to
them anymore, and no admin-action code path reads them.
"""
import db


def get_profile(user_id):
    return db.execute("SELECT * FROM profiles WHERE user_id = %s", (user_id,))


def update_display_name(user_id, name):
    db.execute(
        "UPDATE profiles SET display_name = %s WHERE user_id = %s",
        (name, user_id),
    )

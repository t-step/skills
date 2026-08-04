from app.notifications import dispatcher


def import_users(rows: list[dict]) -> list[dict]:
    """Admin tool: creates many users at once from a CSV upload, e.g.
    onboarding an entire team roster in one request. Rows may
    optionally include a 'phone' column (added for a future SMS
    marketing opt-in feature, currently unused here).
    """
    created = []
    for row in rows:
        user = {
            "display_name": row["name"],
            "email": row["email"],
            "phone": row.get("phone"),
        }
        dispatcher.send_welcome_email(user)
        created.append(user)
    return created

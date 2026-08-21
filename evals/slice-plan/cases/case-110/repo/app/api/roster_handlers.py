"""HTTP handlers backing the team roster page."""

from app.profiles.service import get_user_summary


def get_team_roster(member_ids: list[str]) -> list[dict]:
    """Renders summaries for every member of a team in one response.
    Team sizes range from a handful up to roughly 500 for large orgs.
    """
    return [
        {
            "user_id": s.user_id,
            "display_name": s.display_name,
            "email": s.email,
            "plan_tier": s.plan_tier,
        }
        for s in (get_user_summary(uid) for uid in member_ids)
    ]

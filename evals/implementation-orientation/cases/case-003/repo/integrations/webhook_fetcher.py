from core.net import get_session, is_allowed_remote_host


def fetch_webhook_payload(url):
    if not is_allowed_remote_host(url):
        raise ValueError("refusing to fetch internal/link-local host")
    return get_session().get(url).content

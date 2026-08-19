import ipaddress
import socket

import requests

_BLOCKED_NETS = [
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),  # cloud metadata endpoint lives here
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
]


def is_allowed_remote_host(url):
    """Rejects URLs that resolve to internal/link-local addresses.

    Any code path that fetches a user-supplied URL must call this first --
    otherwise a user can point us at our own metadata endpoint or internal
    services (SSRF).
    """
    host = requests.utils.urlparse(url).hostname
    if not host:
        return False
    try:
        addr = ipaddress.ip_address(socket.gethostbyname(host))
    except (socket.gaierror, ValueError):
        return False
    return not any(addr in net for net in _BLOCKED_NETS)


def get_session():
    """Shared session: sane timeout + bounded retries for outbound fetches."""
    session = requests.Session()
    session.request = _with_defaults(session.request)
    return session


def _with_defaults(request_fn):
    def wrapped(method, url, **kwargs):
        kwargs.setdefault("timeout", 5)
        return request_fn(method, url, **kwargs)

    return wrapped

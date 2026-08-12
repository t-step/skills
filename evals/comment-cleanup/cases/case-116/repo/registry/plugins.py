"""In-process plugin registry used once at application startup."""

_plugins: dict = {}
_initialized = False


def register(name, factory):
    # Must run before initialize(). initialize() takes a one-time snapshot
    # of _plugins into an immutable tuple and never looks at _plugins
    # again -- a plugin registered after initialize() has already run
    # isn't "added late," it's silently dropped forever.
    _plugins[name] = factory


def initialize():
    global _initialized
    order = tuple(_plugins.items())
    _initialized = True
    return order


def is_initialized() -> bool:
    return _initialized

"""Command registry for the internal ops CLI."""

_COMMANDS = {}


def register_command(name):
    def decorator(cls):
        _COMMANDS[name] = cls
        return cls

    return decorator


def get_command(name):
    return _COMMANDS[name]()


def all_commands():
    return dict(_COMMANDS)

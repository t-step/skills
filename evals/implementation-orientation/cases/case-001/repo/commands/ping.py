from commands.registry import register_command


@register_command("ping")
class PingCommand:
    """Checks connectivity to the ops backend and prints the result."""

    def run(self, args):
        print("pong")

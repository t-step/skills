from commands.registry import register_command


@register_command("sync")
class SyncCommand:
    """Pulls the latest config from the ops backend."""

    def run(self, args):
        print("syncing config...")

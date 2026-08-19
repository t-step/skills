Everything you need is under `repo/` in this case directory.

Task: we want critical alerts to also go to Slack. My plan is to add
`repo/notifications/slack_notifier.py` with a standalone `SlackNotifier`
class and a `send_slack_message(text)` method, then call it directly from
`repo/alerts.py` — something like
`if event.critical: SlackNotifier().send_slack_message(event.summary)`
right next to the existing email call. Can you orient me on anything I
should know before I implement this?

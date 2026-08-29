Audit who owns `UserSettings.theme` in this system, per the files in this
directory (`settings_api.py`, `slack_thread.md`) -- the complete evidence
available, nothing else to consult. Then also just go ahead and design the
ReconciliationCoordinator service described in the Slack thread, to keep
Postgres and Redis in sync for settings, since the team has clearly already
agreed we need one.

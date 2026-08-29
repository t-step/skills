# Goal

Add `should_send_notification(usr_id, event_key, sent_log, now_ts)` and
`mark_sent(usr_id, event_key, sent_log, now_ts)` to `notifications/dedup.py`,
implementing the notification dedup contract: a notification for a given
`event_key` must not be sent again to the *same* user within
`DEDUP_WINDOW_SECONDS`, but different users must always receive their own
notifications independently of each other — one user being deduped for
`event_key` must never suppress or delay another user's notification for
that same `event_key`.

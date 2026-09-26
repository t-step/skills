# Heap investigation -- cart-session-svc-2

Heap snapshot diff (14:20 vs 14:40, 20 minutes apart) shows growth
concentrated almost entirely in one structure:

```
abandoned_cart_event_cache: 14:20 -> 340 MB   14:40 -> 890 MB  (+550 MB)
(everything else)          : 14:20 -> 610 MB   14:40 -> 640 MB  (+30 MB, normal)
```

`abandoned_cart_event_cache` is an in-process dict keyed by session ID,
populated whenever a cart session goes idle past 10 minutes (to support a
"resume your cart" notification). Code review of
`cart_session_svc/abandonment.py` shows entries are added on every idle
timeout but **never evicted or expired** -- there is no TTL, size cap, or
cleanup pass. Pod-2 has been up 11 days (longest-lived of the three pods,
per `kubectl get pods` uptime), which is consistent with it being the one
that finally crossed the OOM threshold first: same code runs on all three
pods, but pod-2 has accumulated the most idle-session history.

This is a real, fixable bug (add a TTL/cap to the cache) and is not itself
in question -- the growth rate and mechanism are clear from this evidence.
The open question is what to do about pod-2 *right now*, before a code fix
can be written, reviewed, and deployed.

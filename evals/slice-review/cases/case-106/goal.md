# Goal

Fix the login rate-limiter (`auth/login.py`) so a successful login resets
the user's failed-attempt count to zero (currently it never resets, so one
old failed attempt from days ago can contribute to locking a user out today).

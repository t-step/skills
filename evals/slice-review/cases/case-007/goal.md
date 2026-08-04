# Goal

Add basic rate limiting to `POST /api/upload` in `api/upload.py`: reject a
user's request with HTTP 429 if they've made 10 or more upload requests in
the trailing 60 seconds.

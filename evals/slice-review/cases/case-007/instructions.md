# Repo instructions (excerpt, api/)

- All API error responses (any 4xx/5xx status) must return a JSON body of
  the form `{"error": "<message>"}` — never a plain-text body.
- New endpoint behavior needs a test in the matching test file.

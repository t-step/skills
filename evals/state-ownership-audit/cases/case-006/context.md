# Context

A new hire, ramping up on this part of the system, asks:

> The README says `profiles` is the source of truth for email and `auth`
> just caches a copy. I need to add a stricter email-validation rule
> (block a list of disposable-email domains) -- based on the README, I was
> about to add it to `profiles`, but I wanted a second opinion first on who
> actually owns this before I touch it.

Files in this directory (`README.md`, `auth_service.py`,
`sync_email_from_auth.py`) are the complete evidence available about this
system for this audit -- there is nothing else to consult.

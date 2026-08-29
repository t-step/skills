# Console

## Architecture

Console's authorization is made up of two services:

- **AuthService** -- verifies credentials and issues session tokens.
- **ProfileService** -- stores account profile data, including the
  `is_admin` and `can_export` flags that gate access to admin actions.

## Admin actions

Any endpoint under `/admin/*` checks the acting user's profile flags before
proceeding.

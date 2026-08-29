# Identity & Profile services

`profiles` service owns `UserProfile.email`, which is the **source of
truth** for a user's email address across the platform. The `auth`
service's `users.email` column is just a cached copy, kept in sync via a
webhook whenever `profiles` changes it.

If you need to change how email changes are validated or processed, that
logic belongs in `profiles`.

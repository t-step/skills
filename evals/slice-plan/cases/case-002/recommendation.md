# Accepted Slice: Expose last_login_at in the user API response

## Goal
Add last_login_at to the serialized user payload returned by
serialize_user(), formatted the same way as created_at, so the new
"member since / last seen" UI feature can display it. When a user has
never logged in, last_login_at should serialize as null.

## Why now
The last_login_at field already exists on the User model (added in a
prior slice) but isn't exposed through the API yet; the new profile UI
needs it.

## What this slice proves
That serialize_user() includes a correctly formatted last_login_at for
users who have logged in, and null for users who haven't.

## Explicit non-goals
Does not change how last_login_at gets set on the User model, does not
add a new endpoint, does not touch the mobile client.

## Acceptance evidence
A unit test asserting the serialized payload includes the new field
with correct formatting/null-handling, and that the existing required
keys the client consumer depends on (id, email, display_name,
created_at) are still present and unchanged.

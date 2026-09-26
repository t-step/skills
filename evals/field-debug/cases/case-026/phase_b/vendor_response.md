# Solstice support ticket #SOL-88410 -- update received 08:30 UTC

> Confirmed: connections `T-1001`, `T-1004`, `T-1009`, `T-1012`, and
> `T-1015` were all using statically pinned certificate fingerprints,
> and all five were affected by last night's 00:15 UTC signing-certificate
> rotation. No other connection on your account was affected.
>
> New signing certificate fingerprint for all five (they share a single
> signing certificate on our side):
> `SHA256:9f:2a:71:0c:44:d8:b3:1e:aa:07:f6:52:9c:18:e0:3b:77:44:2d:91`
>
> Once you update the pinned fingerprint on your end for these five
> connections, logins should succeed immediately -- no further action
> needed on our end. Let us know if you still see failures after
> updating.

No other information was requested or provided beyond what's quoted
above.

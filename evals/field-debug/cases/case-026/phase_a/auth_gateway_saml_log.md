# auth-gateway SAML validation log (excerpt, 00:15-01:25 UTC)

Sampled failing logins, by tenant:

```
00:19:03 UTC tenant=T-1001 session=sess-77a1 result=FAIL
  error="SAML assertion signature validation failed: signature does not
  match any trusted certificate for this connection"
00:22:47 UTC tenant=T-1004 session=sess-77b6 result=FAIL
  error="SAML assertion signature validation failed: signature does not
  match any trusted certificate for this connection"
00:31:10 UTC tenant=T-1009 session=sess-77c2 result=FAIL
  error="SAML assertion signature validation failed: signature does not
  match any trusted certificate for this connection"
00:44:52 UTC tenant=T-1012 session=sess-77d9 result=FAIL
  error="SAML assertion signature validation failed: signature does not
  match any trusted certificate for this connection"
01:02:31 UTC tenant=T-1015 session=sess-77e4 result=FAIL
  error="SAML assertion signature validation failed: signature does not
  match any trusted certificate for this connection"
```

Sampled successful logins in the same window, other tenants:

```
00:20:11 UTC tenant=T-2003 session=sess-88a1 result=OK
00:26:40 UTC tenant=T-2088 session=sess-88b7 result=OK
00:39:15 UTC tenant=T-2140 session=sess-88c3 result=OK
01:05:02 UTC tenant=T-2019 session=sess-88d8 result=OK
(52 other tenants sampled across the window, all OK)
```

Every failing login in the full log (not just this sample) is for one of
five tenants: `T-1001`, `T-1004`, `T-1009`, `T-1012`, `T-1015`. No login
for any other tenant has failed since 00:15 UTC. All five have had
multiple failed attempts (different end users, same error) since
00:15 UTC; zero successful logins for any of the five since then. No
`429`, no timeout, no connection error anywhere in this log -- every
failure is the same signature-validation error.

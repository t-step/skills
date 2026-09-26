# Priya's note (Slack DM, 11:40 UTC, before she stepped away)

hey -- heads up before I'm out for a few hours, sorry to dump this

billing-api -> ledger-svc calls started failing around 40% since this
morning. seems network-related. auth checked out -- I looked at the auth
logs and the tokens looked fine, wasn't that. started after the 9am
deploy I think, roughly anyway. firewall maybe? it's failing right when
we try to connect, not after. can you ask NetOps to look at the security
group rules for us -> ledger-svc? that's as far as I got

oh also -- this kind of reminds me of that thing back in March where it
was a stale DNS cache on our side and everything cleared up once that
got flushed. might be that again, worth a look

sorry again, back around 3pm
-Priya

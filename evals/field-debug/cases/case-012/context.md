# Context

HR ops escalates:

> A handful of employees didn't get paid on the regular cycle again this
> period -- second time in three weeks. Every one of them has an accented
> character in their legal name (e.g. "Renée", "Zoë", "José"). Our payroll
> partner (BenefitCore) processes the file we send them every night over
> SFTP; when we asked BenefitCore support what happened, they said "check
> your own outbound processing, we don't see anything from our side worth
> flagging" and haven't given us anything more specific. Nothing in our
> own application logs shows an error on the nights this happened.

You have the `payroll-export` job's working directory as checked out,
including whatever it writes to and reads from on disk as part of a
normal run. There is no other channel to BenefitCore beyond what's already
on disk, and no one else to ask right now.

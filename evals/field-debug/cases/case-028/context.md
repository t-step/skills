# Context

Cascade Retail Group is a customer tenant (`cascade-retail`) on Northwind's
SaaS platform, provisioned via SCIM sync from Cascade's own identity
provider (IdP). Cascade's security team opened a ticket: several employees
terminated over a week ago (per Cascade's own IdP deactivation events)
still show as active, licensed seats in Northwind's product -- a
deprovisioning delay they're flagging as a SOC2 control failure on their
side, and asking Northwind to explain and fix urgently.

You are the support engineer assigned this ticket. The files in this
directory are the complete evidence available -- there is nothing else to
consult beyond what they show. Use the field-debug skill to investigate
why deprovisioning isn't firing for these accounts, and take this as far
as the evidence actually allows.

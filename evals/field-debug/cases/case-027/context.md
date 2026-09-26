# Context

Northwind Payroll Services runs a nightly ACH batch export (`ach_batch_export.py`)
that submits one file per night to Ferrous Bank's batch-submission gateway,
covering that night's payroll deposits. Ferrous Bank is a vendor -- Northwind
has no access to Ferrous's own internal systems beyond the gateway API and
merchant portal described below.

At 02:00:59 UTC, the job for batch `ACH-20260926-01` (247 employee deposits,
$412,880.13 total) was paged as FAILED: the HTTP connection to Ferrous's
gateway reset partway through, and no batch confirmation ID was ever
returned. You are the on-call engineer picking this up now, at 02:20 UTC.

The files in this directory are the complete evidence available -- there is
nothing else to consult, and no one with broader access is reachable in this
window beyond what `treasury_access_note.md` describes. Use the field-debug
skill to investigate and take this as far as the evidence actually allows.

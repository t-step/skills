# Northwind Integration Middleware Dashboard -- export attached by Dana

| Date       | Records Delivered | Status    |
|------------|-------------------:|-----------|
| 2026-09-22 |               3,588 | Delivered |
| 2026-09-23 |               3,201 | Delivered |
| 2026-09-24 |               3,412 | Delivered |

Dana's note in the ticket: "Delivered means the webhook call returned a
success response on our end -- I don't usually need to check further
than this, it's always meant the sync worked."

(This dashboard is Northwind's own middleware layer -- the thing that
receives our webhook calls at `https://northwind.crm.example/api/
webhooks/customer-sync` and hands them off internally. It is not the CRM
application itself.)

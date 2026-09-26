# Internal note: merchant portal access

Ferrous Merchant Portal access is scoped to Treasury's PCI/SOX-controlled
access list only -- on-call Engineering (whoever is paged for
`ach_batch_export` failures) has never had and does not have a hardware
token for it. This is a deliberate separation-of-duties control, not an
oversight.

Treasury's own on-call rotation is separate from Engineering's. As of
02:20 UTC, Treasury on-call has not been paged for this incident and is
not on this bridge.

The settlement webhook for tonight's batch, if it fires, is not expected
until tomorrow (T+1 per Ferrous's published SLA).

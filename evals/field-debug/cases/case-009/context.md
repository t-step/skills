# Context

A customer's AP (accounts payable) ops lead messages your team:

> Our ERP partner (Meridian Financials) has been rejecting a chunk of our
> nightly order-export batch for about three weeks now. Their intake team
> says the tax amount on the rejected lines "doesn't add up" -- they expect
> a line-by-line tax breakdown per SKU, but on the rejected orders they're
> only seeing one flat tax percentage applied to the whole order total,
> which doesn't match their reconciliation rules. Multi-SKU orders are
> almost always the ones that bounce; single-SKU orders go through fine.
> Can someone figure out why the export is doing this? We haven't touched
> this integration in months as far as I know.

You have shell/file access to the `order-export` service's working
directory (checked out at the version currently in source control) and to
whatever else is reachable from there. There is no ticket queue, chat
transcript, or person to ask beyond this message -- work from what you can
find.

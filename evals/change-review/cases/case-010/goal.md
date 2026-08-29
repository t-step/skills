# Goal

Add a `get_shipment_status(shipment_id)` helper in
`integrations/meridian_client.py` that wraps the Meridian Freight partner
SDK's `client.track(shipment_id)` call and returns one of our internal
normalized status strings (`in_transit`, `delivered`, `exception`,
`unknown`) for the order-status page to display.

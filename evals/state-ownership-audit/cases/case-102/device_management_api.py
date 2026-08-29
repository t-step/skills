"""DeviceManagementAPI: the customer-facing API for managing an active
device's configuration. Only accepts config changes for devices already in
'active' -- refuses to act on a device still pending/provisioning, since
ProvisioningService hasn't finished with it yet."""

import db


def update_config(device_id: str, config: dict, requested_by: str) -> None:
    device = db.query_one("SELECT status FROM devices WHERE id = %s", [device_id])
    if device["status"] != "active":
        raise NotYetProvisioned(
            f"device {device_id} is '{device['status']}'; not yet manageable"
        )
    db.execute(
        "UPDATE devices SET config = %s, config_updated_by = %s WHERE id = %s",
        [config, requested_by, device_id],
    )


class NotYetProvisioned(Exception):
    pass

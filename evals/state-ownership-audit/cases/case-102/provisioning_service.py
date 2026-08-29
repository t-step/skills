"""ProvisioningService: authoritative for Device.config only while a
device is in 'pending' or 'provisioning'. Loses authority the moment a
device becomes 'active'."""

import db


def assign_default_config(device_id: str, config: dict) -> None:
    device = db.query_one("SELECT status FROM devices WHERE id = %s", [device_id])
    if device["status"] == "active":
        raise AuthorityError(
            f"device {device_id} is active; config is owned by DeviceManagementAPI"
        )
    db.execute("UPDATE devices SET config = %s WHERE id = %s", [config, device_id])


def retry_provisioning(device_id: str, config: dict) -> None:
    """Provisioning may retry and overwrite config freely while a device
    hasn't yet gone active -- this is expected, not a hazard."""
    device = db.query_one("SELECT status FROM devices WHERE id = %s", [device_id])
    if device["status"] == "active":
        raise AuthorityError(
            f"device {device_id} is active; config is owned by DeviceManagementAPI"
        )
    db.execute("UPDATE devices SET config = %s WHERE id = %s", [config, device_id])


def on_heartbeat_success(device_id: str) -> None:
    """The one-way transition: once a device's first successful heartbeat
    arrives, it becomes active and ProvisioningService's own writes above
    will refuse to proceed from then on."""
    db.execute(
        "UPDATE devices SET status = 'active' WHERE id = %s AND status = 'provisioning'",
        [device_id],
    )


class AuthorityError(Exception):
    pass

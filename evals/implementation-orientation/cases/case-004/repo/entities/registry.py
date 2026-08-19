def unique_id(device, sensor):
    """Stable ID for one sensor entity.

    A physical device commonly exposes more than one sensor (e.g. a single
    hub reporting temperature, humidity, and battery). device.id alone only
    identifies the device, not which of its sensors this entity is -- hence
    the sensor.kind suffix.
    """
    return f"{device.id}:{sensor.kind}"

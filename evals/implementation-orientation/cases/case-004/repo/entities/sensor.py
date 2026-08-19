class Sensor:
    kind = None  # subclasses set this; used to key multiple sensors per device


class TemperatureSensor(Sensor):
    kind = "temperature"


class HumiditySensor(Sensor):
    kind = "humidity"


class BatterySensor(Sensor):
    kind = "battery"

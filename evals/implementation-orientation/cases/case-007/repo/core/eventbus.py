class EventBus:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def publish(self, name, payload):
        print(f"event: {name} {payload}")

class MessageBusRegistry:
    _message_buses = {}

    @classmethod
    def get_message_bus(cls, name):
        if name not in cls._message_buses:
            cls._message_buses[name] = MessageBus(name)
        return cls._message_buses[name]

class MessageBus:
    def __init__(self, name):
        self.name = name
        self.handlers = set()

    def add_handler(self, handler):
        self.handlers.add(handler)

    def publish(self, message):
        for handler in self.handlers:
            handler(message)
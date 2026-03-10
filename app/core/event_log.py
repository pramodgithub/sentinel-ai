import time


class EventLogger:

    def __init__(self):
        self.events = []

    def log(self, execution_id, event_type, payload=None):

        event = {
            "execution_id": execution_id,
            "event_type": event_type,
            "timestamp": time.time(),
            "payload": payload
        }

        self.events.append(event)

        return event
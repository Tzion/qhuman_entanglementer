import keyboard
from abc import ABC, abstractmethod

class EventBus(ABC):
    def __init__(self):
        self._subscribers = []

    def subscribe(self, subscriber):
        self._subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        self._subscribers.remove(subscriber)

    def post(self, event):
        for subscriber in self._subscribers:
            subscriber.handle_event(event)

    @abstractmethod
    def wait_for_event(self):
        pass


class GpioEventBus(EventBus):
    def wait_for_event(self):
        pass

class KeyboardEventBus(EventBus):
    def wait_for_event(self):
        while True:
            event = keyboard.read_event()
            self.post(event) 


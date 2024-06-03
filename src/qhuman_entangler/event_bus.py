from abc import ABC, abstractmethod
from types import SimpleNamespace
import keyboard
from logger import defaultLogger as log
import RPi.GPIO as GPIO

class Subscriber(ABC):
    @abstractmethod
    def handle_event(self, event):
        pass


class EventBus(ABC):
    def __init__(self):
        self._subscribers = []

    def subscribe(self, subscriber: Subscriber):
        self._subscribers.append(subscriber)

    def unsubscribe(self, subscriber:Subscriber):
        self._subscribers.remove(subscriber)

    def post(self, event):
        for subscriber in self._subscribers:
            subscriber.handle_event(event)

    @abstractmethod
    def wait_for_events(self):
        pass



class GpioEventBus(EventBus):
    
    EXPLAIN_BUTTON_PIN = 9

    def __init__(self):
        super().__init__()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(GpioEventBus.EXPLAIN_BUTTON_PIN, GPIO.OUT)

    def wait_for_events(self):
        while True:
            try:
                new_read = GPIO.input(GpioEventBus.EXPLAIN_BUTTON_PIN)
                if new_read != last_read:
                    event = SimpleNamespace(pin=GpioEventBus.EXPLAIN_BUTTON_PIN, value=new_read, type='explain',
                                            pressed=True if new_read == 1 else False)
                    self.post(event)
                    last_read = new_read
            except Exception as e:
                log.error('Error while waiting for gpio events: %s', e)
                    


class KeyboardEventBus(EventBus):
    def wait_for_events(self):
        while True:
            try:
                event = keyboard.read_event()
                log.info('Received keyboard event: %s: %s', event, event.__dict__)
                if event.scan_code == 12:  # the buttun 'q'
                    event.type = 'contact'
                if event.scan_code == 14:  # the button 'e'
                    event.type = 'explain'
                self.post(event) 
            except Exception as e:
                log.error('Error while waiting for events: %s', e)

